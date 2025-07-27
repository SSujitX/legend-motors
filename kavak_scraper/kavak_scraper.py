import json
import os
from curl_cffi import AsyncSession
import pandas as pd
from selectolax.parser import HTMLParser
from typing import Optional, Type, Dict, Any, List
from types import TracebackType
import asyncio
from datetime import datetime, timezone


class KavakScraper:
    def __init__(
        self, concurrency_api: int = 25, concurrency_details: int = 25
    ) -> None:
        print(f"--------- Kavak Scraper Started ---------\n")

        self.session = AsyncSession(timeout=120, impersonate="chrome")

        self.concurrency_api = concurrency_api
        self.concurrency_details = concurrency_details

        today_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.csv_file = f"kavak_{today_date}.csv"
        self.json_file = f"kavak_{today_date}.json"

        self.api_headers = {
            "kavak-country-acronym": "ae",
            "kavak-client-type": "web",
        }
        self.kavak_api_endpoint = (
            "https://www.kavak.com/api/advanced-search-api/v2/advanced-search"
        )

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.session.close()

    async def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
        allow_redirects: bool = True,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        timeout: int = 120,
        verify: bool = True,
    ) -> Dict[str, Any]:
        try:
            method_lower = method.lower()
            if method_lower not in [
                "get",
                "post",
                "put",
                "delete",
                "patch",
                "head",
                "options",
            ]:
                return {"status": False, "message": f"Invalid HTTP method: {method}."}

            response = await getattr(self.session, method_lower)(
                url,
                params=params,
                data=data,
                json=json_payload,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                verify=verify,
                allow_redirects=allow_redirects,
            )

            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return {
                    "status": True,
                    "message": "Request successful, JSON response.",
                    "json": response.json(),
                    "response_obj": response,
                }
            elif "text/html" in content_type:
                return {
                    "status": True,
                    "message": "Request successful, HTML response.",
                    "parser": HTMLParser(response.text),
                    "response_obj": response,
                }
            else:
                return {
                    "status": True,
                    "message": "Request successful, text response.",
                    "text": response.text,
                    "response_obj": response,
                }
        except Exception as e:
            return {"status": False, "message": f"Request failed: {e}"}

    def _clean_price(self, price_str: Optional[str]) -> Optional[int]:
        if not price_str:
            return None
        try:
            # Remove currency symbol, whitespace, and commas
            cleaned = "".join(c for c in price_str if c.isdigit())
            return int(cleaned) if cleaned else None
        except (ValueError, TypeError):
            return None

    async def fetch_cars_from_api_page(self, page_to_fetch: int) -> Dict[str, Any]:
        params = {"page": page_to_fetch}
        response_data = await self._make_request(
            "get", self.kavak_api_endpoint, params=params, headers=self.api_headers
        )

        if not response_data["status"]:
            return {
                "status": False,
                "message": f"API request failed for page {page_to_fetch}: {response_data.get('message', 'Unknown error')}",
                "cars": [],
                "page_fetched": page_to_fetch,
            }

        json_content = response_data.get("json")
        if not json_content:
            return {
                "status": False,
                "message": f"No JSON content for page {page_to_fetch}.",
                "cars": [],
                "page_fetched": page_to_fetch,
            }

        cars_on_page: List[Dict[str, Any]] = json_content.get("cars", [])
        if cars_on_page:
            print(
                f">= Kavak: Fetched {len(cars_on_page)} car listings from API page {page_to_fetch}."
            )

        return {
            "status": True,
            "cars": cars_on_page,
            "page_fetched": page_to_fetch,
            "message": f"Successfully fetched page {page_to_fetch}.",
        }

    async def fetch_all_car_listings_from_api(self) -> Dict[str, Any]:
        all_car_listings: List[Dict[str, Any]] = []
        current_page_offset = 0

        while True:
            tasks = [
                self.fetch_cars_from_api_page(current_page_offset + i)
                for i in range(self.concurrency_api)
            ]
            page_results_batch = await asyncio.gather(*tasks, return_exceptions=True)

            cars_found_in_this_batch = 0
            for result_or_exc in page_results_batch:
                if isinstance(result_or_exc, Exception):
                    print(
                        f">= Kavak: Exception during API page fetch task: {result_or_exc}"
                    )
                    continue

                if result_or_exc.get("status") and result_or_exc.get("cars"):
                    all_car_listings.extend(result_or_exc["cars"])
                    cars_found_in_this_batch += len(result_or_exc["cars"])
                elif not result_or_exc.get("status"):
                    page_num = result_or_exc.get("page_fetched")
                    error_msg = result_or_exc.get(
                        "message", "No specific error message"
                    )
                    print(
                        f">= Kavak: Failed to process API page {page_num}: {error_msg}"
                    )

            if cars_found_in_this_batch == 0 and current_page_offset > 0:
                print(
                    f">= Kavak: No new cars found in the last batch (pages {current_page_offset} to {current_page_offset + self.concurrency_api -1}). Stopping API fetch."
                )
                break
            if current_page_offset == 0 and cars_found_in_this_batch == 0:
                print(
                    f">= Kavak: No cars found on initial API pages. Stopping API fetch."
                )
                break

            current_page_offset += self.concurrency_api
            print(
                f">= Kavak: Processed batch. Total listings so far: {len(all_car_listings)}. Moving to next set of pages from {current_page_offset}.\n"
            )
            await asyncio.sleep(1)

        if not all_car_listings:
            return {
                "status": False,
                "message": "No car listings found from API.",
                "data": [],
            }

        print(
            f">= Kavak: Successfully fetched {len(all_car_listings)} car listings in total from API."
        )
        return {
            "status": True,
            "data": all_car_listings,
            "message": "API fetch successful.",
        }

    async def fetch_and_parse_product_details(
        self, car_api_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        url = car_api_data.get("url")
        if not url:
            return {
                "status": False,
                "message": "Missing URL in car API data.",
                "original_api_data": car_api_data,
                "details": {},
            }

        default_return = {
            "status": False,
            "message": "Unknown error during product detail fetching.",
            "original_api_data": car_api_data,
            "details": {},
        }

        try:
            response_data = await self._make_request("get", url)
            if not response_data["status"]:
                default_return["message"] = (
                    f"Request failed for product URL {url}: {response_data.get('message')}"
                )
                return default_return

            parser = response_data.get("parser")
            if not parser:
                default_return["message"] = f"No HTML parser object for URL {url}."
                return default_return

            script_node = parser.css_first("script[id='vip-snippet']")
            if not script_node:
                default_return["message"] = (
                    f"Script 'vip-snippet' not found on page {url}."
                )
                return default_return

            script_text = script_node.text(strip=True)
            if not script_text:
                default_return["message"] = (
                    f"Script 'vip-snippet' is empty on page {url}."
                )
                return default_return

            json_data = json.loads(script_text)
            graph_list = json_data.get("@graph", [])

            if (
                not graph_list
                or not isinstance(graph_list, list)
                or len(graph_list) == 0
            ):
                default_return["message"] = (
                    f"No @graph data or invalid format in script on page {url}."
                )
                return default_return

            graph = graph_list[0]

            offers = graph.get("offers", {})
            mileage_from_odometer = graph.get("mileageFromOdometer", {})
            vehicle_engine = graph.get("vehicleEngine", {})

            # Adhering to original script's specific key access patterns where possible
            doors_info = graph.get("body_style.local_number_of_doors")
            seats_info = graph.get("seats.capacity")

            displacement_obj = vehicle_engine.get("engine.liters", {})
            displacement_value = (
                displacement_obj.get("value")
                if isinstance(displacement_obj, dict)
                else None
            )

            performance_obj = vehicle_engine.get("performance.max_power_hp", {})
            performance_value = (
                performance_obj.get("value")
                if isinstance(performance_obj, dict)
                else None
            )

            details = {
                "title": graph.get("name"),
                "url": car_api_data.get("url"),
                "name": car_api_data.get("name"),
                "scrapedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "id": car_api_data.get("id"),
                "make": car_api_data.get("make"),
                "model": car_api_data.get("model"),
                "trim": car_api_data.get("trim"),
                "year": car_api_data.get("year"),
                "badge": car_api_data.get("badge", {}).get("text"),
                "transmission": car_api_data.get("transmission"),
                "price": self._clean_price(car_api_data.get("price")),
                "kmNoFormat": car_api_data.get("kmNoFormat"),
                "offerPrice": offers.get("price"),
                "offerPriceCurrency": offers.get("priceCurrency"),
                "mileageUnitCode": mileage_from_odometer.get("unitCode"),
                "mileageValue": mileage_from_odometer.get("value"),
                "vehicleModelDate": graph.get("vehicleModelDate"),
                "bodyType": graph.get("bodyType"),
                "vehicleIdentificationNumber": graph.get("vehicleIdentificationNumber"),
                "numberOfAxles": graph.get("numberOfAxles"),
                "doors": doors_info,
                "passengerCapacity": seats_info,
                # "engineDetailName": vehicle_engine.get("name"),
                # "engineFuelType": vehicle_engine.get("fuelType"),
                # "engineDisplacementValue": displacement_value,
                "MaxPowerValue": performance_value,
            }

            return {
                "status": True,
                "message": "Successfully extracted product details.",
                "details": details,
            }

        except json.JSONDecodeError as e_json:
            default_return["message"] = f"JSON decode error for {url}: {e_json}"
            return default_return
        except Exception as e:
            default_return["message"] = (
                f"Unexpected error processing product page {url}: {e}"
            )
            return default_return

    async def run_scraper(self) -> None:
        api_listings_response = await self.fetch_all_car_listings_from_api()

        if not api_listings_response["status"]:
            print(
                f">= Kavak: Halting: Failed to fetch car listings from API: {api_listings_response['message']}"
            )
            return api_listings_response

        api_cars = api_listings_response.get("data", [])
        if not api_cars:
            print(">= Kavak: Halting: No car listings found from API.")
            return

        print(
            f"\n>= Kavak: Fetched {len(api_cars)} car listings. Now fetching product details concurrently...\n"
        )

        product_detail_tasks = [
            self.fetch_and_parse_product_details(car_data) for car_data in api_cars
        ]

        all_combined_car_data: List[Dict[str, Any]] = []

        for i in range(0, len(product_detail_tasks), self.concurrency_details):
            batch_tasks = product_detail_tasks[i : i + self.concurrency_details]
            results_batch = await asyncio.gather(*batch_tasks, return_exceptions=True)

            print(
                f"\n--- Kavak: Processing Batch {i // self.concurrency_details + 1} of Product Details ---"
            )
            for result_or_exc in results_batch:
                if isinstance(result_or_exc, Exception):
                    print(f"Error during product detail fetch task: {result_or_exc}")
                    continue

                if result_or_exc["status"]:
                    product_details = result_or_exc["details"]

                    # print(product_details)

                    df = pd.DataFrame([product_details])
                    df.to_csv(
                        self.csv_file,
                        mode="a",
                        index=False,
                        header=not os.path.exists(self.csv_file),
                    )

                    all_combined_car_data.append(product_details)
                    print(
                        f">= Kavak: Successfully processed {product_details.get('name')}"
                    )

                else:
                    print(
                        f">= Kavak: Failed to fetch/parse details for {result_or_exc['message']}"
                    )

            if i + self.concurrency_details < len(product_detail_tasks):
                print(
                    f"--- Kavak: Batch {i // self.concurrency_details + 1} done. Sleeping for 2 seconds before next batch... ---"
                )
                await asyncio.sleep(2)

        # print(f"\n\n--- Scraping Complete ---")
        print(
            f">= Kavak: Successfully processed and combined data for {len(all_combined_car_data)} out of {len(api_cars)} cars.\n"
        )

        # if all_combined_car_data:

        #     with open(self.json_file, "w") as f:
        #         json.dump(all_combined_car_data, f, indent=2)
        #     print(f">= Saved all combined data to {self.json_file}")


async def main():
    async with KavakScraper(concurrency_api=25, concurrency_details=200) as scraper:
        await scraper.run_scraper()


if __name__ == "__main__":
    asyncio.run(main())
