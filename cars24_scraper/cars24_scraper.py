import pandas as pd
from rich import print
import sys, os
from datetime import datetime, timedelta, timezone
from curl_cffi import AsyncSession
import asyncio
from typing import Optional, Type, Any, Dict
from types import TracebackType
from selectolax.parser import HTMLParser


class CarScraper:
    def __init__(self) -> None:
        print(f"--------- Cars24 Scraper Started ---------\n")

        self.session = AsyncSession(timeout=120, impersonate="chrome")

        today_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.csv_file = f"cars24_{today_date}.csv"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "X_COUNTRY": "AE",
            "X_VEHICLE_TYPE": "CAR",
            "X_PLATFORM": "desktop",
            "Origin": "https://www.cars24.ae",
            "Connection": "keep-alive",
            "Referer": "https://www.cars24.ae/",
        }

    async def __aenter__(self):
        """Enter the context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        """
        Exit the context manager.
        """
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

    async def fetch_page_data(self, page_number):
        params = {
            "isSeoFilter": "true",
            "sf": ["city:DU_DUBAI", "gaId:"],
            "size": "25",
            "spath": "buy-used-cars-dubai",
            "page": str(page_number),
            "variant": "filterV5",
        }
        print(f">= Cars24: Fetching page {page_number}...\n")

        try:
            # response = curl_cffi.get(
            #     "https://listing-service.c24.tech/v3/vehicle",
            #     headers=self.headers,
            #     params=params,
            #     impersonate="chrome",
            # )
            response_data: dict = await self._make_request(
                "get",
                "https://listing-service.c24.tech/v3/vehicle",
                headers=self.headers,
                params=params,
            )
            if not response_data["status"]:
                return response_data

            response_json: dict = response_data.get("json")
            return response_json.get("results", [])

        except Exception as e:
            print(f"Cars24: Error fetching page {page_number}: {e}")
            return []

    async def process_car_data(self, result: dict):
        # Step 1: Extract all raw data fields from result and its nested structures
        emiDetails = result.get("emiDetails", {})
        parentHubLocation = result.get("parentHubLocation", {})

        make = result.get("make")
        model = result.get("model")
        year = result.get("year")
        variant = result.get("variant")
        api_city = result.get("city")
        appointment_id = result.get("appointmentId")

        specs = result.get("specs")
        engine_size = result.get("engineSize")
        no_of_cylinders = result.get("noOfCylinders")

        emi = emiDetails.get("emi")
        down_payment = emiDetails.get("downPayment")
        roi = emiDetails.get("roi")
        tenure = emiDetails.get("tenure")

        discounted = result.get("discounted")
        discount_amount = result.get("discountAmount")
        target_price = result.get("targetPrice")
        assortment_flag = result.get("assortmentFlag")
        assortment_category = result.get("assortmentCategory")
        location_name = parentHubLocation.get("locationName")
        body_type = result.get("bodyType")
        fuel_type = result.get("fuelType")
        inventory_type = result.get("inventoryType")
        car_card_tag = result.get("carCardTag")
        price = result.get("price")
        odometer_reading = result.get("odometerReading")
        transmission_type = result.get("transmissionType")

        formatted_title = None
        formatted_url = None

        if year and make and model and variant:
            formatted_title = f"{year} {make.upper()} {model.upper()} {variant.upper()}"
        elif year and make and model:
            formatted_title = f"{year} {make.upper()} {model.upper()}"

        if make and model and year and api_city and appointment_id:
            city_name_parts = api_city.split("_")
            city_slug = (
                city_name_parts[-1].lower()
                if len(city_name_parts) > 1
                else api_city.lower()
            )
            url_make = make.lower().replace(" ", "-")
            url_model = model.lower().replace(" ", "-")
            formatted_url = f"https://www.cars24.ae/buy-used-{url_make}-{url_model}-{year}-cars-{city_slug}-{appointment_id}/"

        car_data = {
            "title": formatted_title,
            "url": formatted_url,
            "scrapedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "appointmentId": appointment_id,
            "make": make,
            "model": model,
            "year": year,
            "variant": variant,
            "specs": specs,
            "engineSize": engine_size,
            "noOfCylinders": no_of_cylinders,
            "city": api_city,
            "emi": emi,
            "downPayment": down_payment,
            "roi": roi,
            "tenure": tenure,
            "discounted": discounted,
            "discountAmount": discount_amount,
            "targetPrice": target_price,
            "assortmentFlag": assortment_flag,
            "assortmentCategory": assortment_category,
            "locationName": location_name,
            "bodyType": body_type,
            "fuelType": fuel_type,
            "inventoryType": inventory_type,
            "carCardTag": car_card_tag,
            "price": price,
            "odometerReading": odometer_reading,
            "transmissionType": transmission_type,
        }

        df = pd.DataFrame([car_data])
        df.to_csv(
            self.csv_file,
            mode="a",
            index=False,
            header=not os.path.exists(self.csv_file),
        )

        print(f">= Cars24: {car_data.get('title', 'Unknown Car')}")

    async def run_scraper(self, max_pages=50):
        total_cars_processed = 0
        for page_num in range(max_pages):
            results = await self.fetch_page_data(page_num)

            if not results:
                print(f">= Cars24: No more results found at page {page_num}")
                break

            print(f">= Cars24: Found {len(results)} results on page {page_num}")
            for car_result in results:
                await self.process_car_data(car_result)
                total_cars_processed += 1

        print(f"\n>= Cars24: Total cars processed and saved - {total_cars_processed}")


async def main():
    async with CarScraper() as scraper:
        await scraper.run_scraper(max_pages=50)


if __name__ == "__main__":
    asyncio.run(main())
