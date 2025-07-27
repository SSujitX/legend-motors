import json
from curl_cffi import AsyncSession
from selectolax.parser import HTMLParser
from typing import Optional, Type, Dict, Any
from types import TracebackType
import asyncio
from rich import print


class kavakScraper:
    def __init__(self) -> None:
        self.session = AsyncSession(timeout=120)

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.session.close()

    def _clean_price(self, price_str: Optional[str]) -> Optional[int]:
        if not price_str:
            return None
        try:
            # Remove currency symbol, whitespace, and commas
            cleaned = "".join(c for c in price_str if c.isdigit())
            return int(cleaned) if cleaned else None
        except (ValueError, TypeError):
            return None

    async def parserOrResponse(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        allow_redirects: bool = True,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        timeout: int = 120,
        verify: bool = True,
        impersonate: str = "chrome",
    ) -> Dict[str, Any]:
        """
        Send a request via the given HTTP method on self.session and return
        an HTMLParser or an error dict.


        Args:
            method (str): HTTP method to use (e.g., "get", "post").
            url (str): URL to send the request to.
            params (dict, optional): Query parameters for the request.
            data (dict, optional): Data to send in the body of the request.
            json (dict, optional): JSON data to send in the body of the request.
            allow_redirects (bool, optional): Whether to follow redirects.
            headers (dict, optional): Custom headers to include in the request.
            cookies (dict, optional): Cookies to include in the request.
            timeout (int, optional): Timeout for the request.
            verify (bool, optional): Whether to verify SSL certificates.
            impersonate (str, optional): Browser to impersonate.
        Returns:
            dict: A dictionary containing the status and message of the request.
                If successful, it also contains the HTMLParser object.

        """
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
                return {
                    "status": False,
                    "message": f"Invalid method in parser: {method}.",
                }
            func = getattr(self.session, method_lower)
            response = await func(
                url,
                params=params,
                data=data,
                json=json,
                impersonate=impersonate,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                verify=verify,
                allow_redirects=allow_redirects,
            )
            return {
                "status": True,
                "message": "Request successful in parser.",
                "parser": HTMLParser(response.text),
                "response": response,
            }
        except Exception as e:
            return {"status": False, "message": f"Request failed in parser: {e}"}

    async def _fetch_api_page(
        self,
        page_to_fetch_local: int,
    ) -> Dict[str, Any]:
        """Fetches and processes a single page of car data."""
        kavak_api_endpoint = (
            "https://www.kavak.com/api/advanced-search-api/v2/advanced-search"
        )
        headers = {
            "kavak-country-acronym": "ae",
            "kavak-client-type": "web",
        }

        params_local = {"page": page_to_fetch_local}
        response_data_local = await self.parserOrResponse(
            "get", kavak_api_endpoint, params=params_local, headers=headers
        )

        if not response_data_local["status"]:
            return {
                "status": False,
                "message": f"Request failed for page {page_to_fetch_local}: {response_data_local.get('message', 'Unknown error')}",
                "cars": [],
                "page_fetched": page_to_fetch_local,
            }

        actual_response_object_local = response_data_local.get("response")
        if actual_response_object_local is None:
            return {
                "status": False,
                "message": f"No response object for page {page_to_fetch_local}",
                "cars": [],
                "page_fetched": page_to_fetch_local,
            }

        try:
            json_data_local = actual_response_object_local.json()
        except Exception as e_local:
            return {
                "status": False,
                "message": f"JSON decode error for page {page_to_fetch_local}: {e_local}",
                "cars": [],
                "page_fetched": page_to_fetch_local,
            }

        cars_local: list[dict] = json_data_local.get("cars", [])
        if cars_local:
            print(f">= Found {len(cars_local)} cars on page {page_to_fetch_local}.")
        # else:
        #     print(f">= No cars found on page {page_to_fetch_local}.") # Less verbose for empty pages
        return {
            "status": True,
            "cars": cars_local,
            "page_fetched": page_to_fetch_local,
        }

    async def _fetch_product_urls(self, url):
        """
        Fetches product URLs from the given URL.
        """
        response = await self.parserOrResponse("get", url)
        if not response["status"]:
            return {
                "status": False,
                "message": f"Request failed for URL {url}: {response.get('message')}",
            }

        parser_object = response.get("parser")
        if parser_object is None:
            return {
                "status": False,
                "message": f"No parser object for URL {url}",
            }

        return {
            "status": True,
            "message": "Request successful",
            "parser": parser_object,
        }

    async def scrape_stage_1(self) -> Dict[str, Any]:
        """
        Scrapes car data from Kavak API, fetching pages concurrently using asyncio.gather.
        """

        all_cars_data: list[dict] = []
        current_page_offset = 0
        CONCURRENCY_LIMIT = 25

        while True:
            tasks = []
            for i in range(CONCURRENCY_LIMIT):
                page_to_fetch = current_page_offset + i
                tasks.append(self._fetch_api_page(page_to_fetch))

            page_results_batch = await asyncio.gather(*tasks, return_exceptions=True)

            cars_found_in_this_batch = 0

            for result_or_exc in page_results_batch:
                if isinstance(result_or_exc, Exception):
                    print(f"Exception during page fetch task: {result_or_exc}")
                    continue

                if result_or_exc.get("status") and result_or_exc.get("cars"):
                    all_cars_data.extend(result_or_exc["cars"])
                    cars_found_in_this_batch += len(result_or_exc["cars"])
                elif result_or_exc.get("status") is False:
                    # Log specific error message from a failed page processing
                    page_fetched_num = result_or_exc.get("page_fetched", "unknown")
                    error_msg = result_or_exc.get(
                        "message", "No specific error message"
                    )
                    print(f">= Failed to process page {page_fetched_num}: {error_msg}")

            if cars_found_in_this_batch == 0:
                print(f">= No cars found in this batch. Stopping scraping.")
                break

            current_page_offset += CONCURRENCY_LIMIT
            print(
                f">= Found {cars_found_in_this_batch} cars in this batch. Moving to next pages."
            )
            await asyncio.sleep(1)

        if not all_cars_data:
            print(">= No cars found after attempting to fetch all pages.")
            return {
                "status": False,
                "message": "No cars found after attempting to fetch all pages.",
            }

        print(f">= Successfully scraped {len(all_cars_data)} cars in total.")
        return {
            "status": True,
            "data": all_cars_data,
            "message": f"Successfully scraped {len(all_cars_data)} cars.",
        }

    async def scraper(self) -> Dict[str, Any]:
        """
        This method orchestrates the scraping process by calling the
        scrape_stage_1 method and handling any errors that may occur.
        """
        try:
            scraped_data = await self.scrape_stage_1()
            if not scraped_data["status"]:
                return {
                    "status": False,
                    "message": f"Scraping failed: {scraped_data['message']}",
                }
            datas: list[dict] = scraped_data.get("data")
            if datas is None:
                return {
                    "status": False,
                    "message": "Scraping failed: No data found.",
                }
            for data in datas:

                # ---------------------- #
                url = data.get("url")
                if url is None:
                    return {
                        "status": False,
                        "message": "Scraping failed: No URL found in data.",
                    }
                car_new_data = await self._fetch_product_urls(url)
                if not car_new_data["status"]:
                    return {
                        "status": False,
                        "message": f"Scraping failed: {car_new_data['message']}",
                    }
                parser_object: HTMLParser = car_new_data.get("parser")

                script = parser_object.css_first("script[id='vip-snippet']").text(
                    strip=True
                )
                json_loads: dict = json.loads(script)
                graph: dict = json_loads.get("@graph", [])
                if len(graph) == 0:
                    print("No @graph found in the script.")

                graph = graph[0]
                name = graph.get("name")
                url = graph.get("url")

                offers = graph.get("offers", {})
                offerprice = offers.get("price")
                offerpriceCurrency = offers.get("priceCurrency")

                model = graph.get("model")

                mileageFromOdometer = graph.get("mileageFromOdometer", {})
                mileageunitCode = mileageFromOdometer.get("unitCode")
                mileageValue = mileageFromOdometer.get("value")

                vehicleConfiguration = graph.get("vehicleConfiguration")
                vehicleModelDate = graph.get("vehicleModelDate")
                bodyType = graph.get("bodyType")
                vehicleIdentificationNumber = graph.get("vehicleIdentificationNumber")
                vehicleTransmission = graph.get("vehicleTransmission")

                numberOfAxles = graph.get("numberOfAxles")

                bodyStyle = graph.get("body_style.local_number_of_doors")

                seats = graph.get("seats.capacity")

                vehicleEngine = graph.get("vehicleEngine", {})
                vehiclename = vehicleEngine.get("name")
                vehiclefuelType = vehicleEngine.get("fuelType")

                vehicleengineDisplacement = vehicleEngine.get("engine.liters", {})
                vehicleengineDisplacementunitCode = vehicleengineDisplacement.get(
                    "unitCode"
                )
                vehicleengineDisplacementValue = vehicleengineDisplacement.get("value")

                vehiclePerformance = vehicleEngine.get("performance.max_power_hp", {})
                vehiclePerformancemaxPowerunitCode = vehiclePerformance.get("unitCode")
                vehiclePerformancemaxPowervalue = vehiclePerformance.get("value")

                # car_info = {
                #     "name": name,
                #     "url": url,
                #     "offerprice": offerprice,
                #     "offerpriceCurrency": offerpriceCurrency,
                #     "mileageunitCode": mileageunitCode,
                #     # "mileageValue": mileageValue,
                #     # "vehicleConfiguration": vehicleConfiguration,
                #     # "vehicleModelDate": vehicleModelDate,
                #     "bodyType": bodyType,
                #     "vehicleIdentificationNumber": vehicleIdentificationNumber,
                #     # "vehicleTransmission": vehicleTransmission,
                #     "numberOfAxles": numberOfAxles,
                #     "doors": bodyStyle,
                #     "passenger": seats,
                #     # "vehiclename": vehiclename,
                #     "type": vehiclefuelType,
                #     # "vehicleengineDisplacementunitCode": vehicleengineDisplacementunitCode,
                #     "liters": vehicleengineDisplacementValue,
                #     # "vehiclePerformancemaxPowerunitCode": vehiclePerformancemaxPowerunitCode,
                #     "maxPower": vehiclePerformancemaxPowervalue,
                # }
                # print(car_info)
                # ---------------------- #

                car_data = {
                    "url": data.get("url"),
                    "name": data.get("name"),
                    "make": data.get("make"),
                    "model": data.get("model"),
                    "trim": data.get("trim"),
                    "year": data.get("year"),
                    "transmission": data.get("transmission"),
                    "price": self._clean_price(data.get("price")),
                    "id": data.get("id"),
                    "badge": data.get("badge", {}).get("text"),
                    "kmNoFormat": data.get("kmNoFormat"),
                }
                print(car_data)

        except Exception as e:
            return {"status": False, "message": f"Scraping failed: {e}"}


async def main():
    async with kavakScraper() as scraper:
        results = await scraper.scraper()
        # print(results)


if __name__ == "__main__":
    asyncio.run(main())
