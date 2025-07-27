import asyncio
import json
from selectolax.parser import HTMLParser
import os
from curl_cffi import AsyncSession
import pandas as pd
from datetime import datetime, timezone
from rich import print
from typing import Optional, Type, Any, Dict
from types import TracebackType


class Automall:
    """
    Automall is a website that sells cars.
    """

    def __init__(self, concurrency: int = 100):
        """
        Initialize the Automall class.
        """
        print(f"--------- Automall Scraper Started ---------\n")

        self.session = AsyncSession(timeout=120, impersonate="chrome")

        today_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.csv_file = f"automall_{today_date}.csv"
        self.concurrency = concurrency

        self.cars_url = "https://www.automall.ae/en/used-cars-shop/"

        self.base_url = "https://www.automall.ae/bff/v2/vehicles"

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en",
            "referer": self.cars_url,
        }

        self.query = (
            "q=type=auto_used_automobiles|price%3E0|attributes.auto_sap_vehicle_status.values.EN=AV,CT"
            "&fields=id|price|discount|equatedMonthlyInstallment|attributes.auto_sap_model_year.values.EN%20as%20modelYear"
            "|attributes.auto_sap_model.values.EN%20as%20model|attributes.auto_sap_engine_capacity.values.EN%20as%20engineCapacity"
            "|attributes.auto_sap_odometer.values.EN%20as%20odometer|attributes.auto_used_car_image1.values.EN%20as%20image"
            "|attributes.auto_sap_vehicle_status.values.EN%20as%20vehicleStatus|attributes.auto_vehicle_location.values.EN%20as%20vehicleLocation"
            "|attributes.auto_sap_model_grade.values.EN%20as%20modelGrade|attributes.auto_basic_exterior_colours.values.EN%20as%20exteriorColours"
            "|attributes.auto_IsHotOffer.values.EN%20as%20isHotOffer|attributes.auto_sap_make.values.EN%20as%20make"
            "|attributes.auto_sap_model_code.values.EN%20as%20modelCode|attributes.auto_sap_body_type.values.EN%20as%20bodyType"
            "&sort=price=1"
        )

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
        """
        Make a request to the Automall API.

        Args:
            method (str): The HTTP method to use.
            url (str): The URL to request.
            params (Optional[Dict[str, Any]]): The parameters to send with the request.
            data (Optional[Dict[str, Any]]): The data to send with the request.
            json_payload (Optional[Dict[str, Any]]): The JSON payload to send with the request.
            allow_redirects (bool): Whether to allow redirects.
            headers (Optional[Dict[str, Any]]): The headers to send with the request.
            cookies (Optional[Dict[str, Any]]): The cookies to send with the request.
            timeout (int): The timeout for the request.
            verify (bool): Whether to verify the SSL certificate.

        Returns:
            Dict[str, Any]: The response from the request.
            status (bool): Whether the request was successful.
            message (str): The message from the request.
            json (Optional[Dict[str, Any]]): The JSON response from the request.
            parser (Optional[HTMLParser]): The HTML parser from the request.
            text (Optional[str]): The text response from the request.
            response_obj (Optional[Response]): The response object from the request.
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

            return {
                "status": True,
                "message": "Request successful.",
                "response": response,
            }
        except Exception as e:
            return {"status": False, "message": f"Request failed: {e}"}

    async def get_auth_token(self) -> str:
        """
        Get the auth token from the Automall API.
        """
        response_data: dict = await self._make_request("get", self.cars_url)
        if not response_data["status"]:
            return response_data

        response = response_data.get("response")
        if response.status_code != 200:
            return {
                "status": False,
                "message": f"Automall: API request failed for get_auth_token: {response.text}",
            }

        cookies = response.cookies.jar
        for cookie in cookies:
            if cookie.name == "AUTH_TOKEN":
                auth_token = cookie.value
                return auth_token

        return None

    async def fetch_car_ids(self) -> dict:
        """
        Fetch a page of cars from Automall.

        Returns:
            dict: A dictionary containing the status, message, and cars.
            status (bool): Whether the request was successful.
            message (str): The message from the request.
            cars (list): A list of car ids.
        """
        print(">= Automall: Fetching car ids")

        start_index = 0
        no_of_records = 28

        ids = []

        auth_token = await self.get_auth_token()
        if not auth_token:
            return {
                "status": False,
                "message": "Automall: No auth token found.",
            }
        auth_token = f"Bearer {auth_token}"
        self.headers["authorization"] = auth_token

        while True:

            paging_info = f"start-index={start_index}|no-of-records={no_of_records}"

            print(f">= Scraping page {start_index} to {start_index + no_of_records}")

            self.headers["paging-info"] = paging_info

            api_url = f"{self.base_url}?{self.query}"

            response_data: dict = await self._make_request(
                "get", api_url, headers=self.headers
            )
            if not response_data["status"]:
                return {
                    "status": False,
                    "message": f"API request failed for page: {response_data.get('message')}",
                    "cars": [],
                }

            response = response_data.get("response")
            if response.status_code != 200:
                return {
                    "status": False,
                    "message": f"Automall API request failed for fetch_car_ids: {response.text}",
                }

            json_responses: list[dict] = response.json()
            if len(json_responses) == 0:
                print(">= Automall: No more cars pages to scrape")
                break

            for json_response in json_responses:

                id = json_response.get("id")
                ids.append(id)

                # price = json_response.get("price")
                # equatedMonthlyInstallment = json_response.get(
                #     "equatedMonthlyInstallment"
                # )
                # modelYear = json_response.get("modelYear")
                # model = json_response.get("model")
                # engineCapacity = json_response.get("engineCapacity")
                # odometer = json_response.get("odometer")
                # image = json_response.get("image")
                # vehicleStatus = json_response.get("vehicleStatus")
                # vehicleLocation = json_response.get("vehicleLocation")
                # modelGrade = json_response.get("modelGrade")
                # exteriorColours = json_response.get("exteriorColours")
                # isHotOffer = json_response.get("isHotOffer")
                # make = json_response.get("make")
                # modelCode = json_response.get("modelCode")
                # bodyType = json_response.get("bodyType")
                # quantity = json_response.get("quantity")

                # if make:
                #     title = f"{make} {model} {modelGrade} {modelYear}"
                # else:
                #     title = None

                # if id:
                #     url = f"https://www.automall.ae/en/used-cars-shop/{id.lower()}"
                # else:
                #     url = None

                # car_data = {
                #     "title": title,
                #     "url": url,
                #     "price": price,
                #     "equatedMonthlyInstallment": equatedMonthlyInstallment,
                #     "modelYear": modelYear,
                #     "model": model,
                #     "engineCapacity": engineCapacity,
                #     "odometer": odometer,
                #     "vehicleStatus": vehicleStatus,
                #     "vehicleLocation": vehicleLocation,
                #     "modelGrade": modelGrade,
                #     "exteriorColours": exteriorColours,
                #     "isHotOffer": isHotOffer,
                #     "make": make,
                #     "modelCode": modelCode,
                #     "bodyType": bodyType,
                # }

            start_index += no_of_records

        return {
            "status": True,
            "message": "Car ids fetched successfully.",
            "cars": ids,
        }

    async def get_car_data(self, id: str) -> dict:
        """
        Get the car data from the Automall API.

        Args:
            id (str): The id of the car to get the data from.


        """
        print(f">= Automall: Scraping car details for {id}")

        car_url = f"https://www.automall.ae/en/used-cars-shop/details/{id.lower()}/"

        response_data: dict = await self._make_request(
            "get",
            car_url,
        )
        if not response_data["status"]:
            return response_data

        response = response_data.get("response")
        if response.status_code != 200:
            return {
                "status": False,
                "message": f"Automall API request failed for get_car_data: {response.text}",
            }

        parser = HTMLParser(response.text)
        script = parser.css_first('script[id="__NEXT_DATA__"]')
        data: dict = json.loads(script.text())

        pageProps: dict = data.get("props", {}).get("pageProps", {})
        detailCarInfo: dict = pageProps.get("detailCarInfo", {})

        trimName = detailCarInfo.get("trimName")
        gradeName = detailCarInfo.get("gradeName")
        id = detailCarInfo.get("id")
        model = detailCarInfo.get("model")
        bodyType = detailCarInfo.get("bodyType")
        modelYear = detailCarInfo.get("modelYear")
        engineCapacity = detailCarInfo.get("engineCapacity")
        modelGrade = detailCarInfo.get("modelGrade")
        material = detailCarInfo.get("material")
        make = detailCarInfo.get("make")
        makeCode = detailCarInfo.get("makeCode")
        modelCode = detailCarInfo.get("modelCode")
        vehicleType = detailCarInfo.get("vehicleType")
        transmissionType = detailCarInfo.get("transmissionType")
        exteriorColours = detailCarInfo.get("exteriorColoursValue")
        interiorColours = detailCarInfo.get("interiorColoursValue")
        vehicleLocation = detailCarInfo.get("vehicleLocation")
        internalVehicleNumber = detailCarInfo.get("internalVehicleNumber")
        vehicleStatus = detailCarInfo.get("vehicleStatus")
        vehicleUsage = detailCarInfo.get("vehicleUsage")
        odometer = detailCarInfo.get("odometer")
        fuelType = detailCarInfo.get("fuelType")
        price = detailCarInfo.get("Price_From")
        priceMonthly = detailCarInfo.get("Price_Monthly")
        isHotOffer = detailCarInfo.get("isHotOffer")
        basicExteriorColours = detailCarInfo.get("basicExteriorColoursValue")

        attributes: list[dict] = detailCarInfo.get("attributes", {})

        number_of_doors = None
        number_of_seats = None
        warranty = None

        for attribute in attributes:
            label = attribute.get("label")
            value = attribute.get("value")

            if label == "Number Of Doors":
                number_of_doors = value
            elif label == "Number Of Seats":
                number_of_seats = value
            elif label == "Warranty":
                warranty = value

        if make:
            title = f"{make} {model} {modelGrade} {modelYear}"
        else:
            title = None

        if id:
            url = f"https://www.automall.ae/en/used-cars-shop/details/{id.lower()}"
        else:
            url = None

        car_data = {
            "title": title,
            "url": url,
            "scrapedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "price": price,
            "priceMonthly": priceMonthly,
            "trimName": trimName,
            "gradeName": gradeName,
            "id": id,
            "model": model,
            "bodyType": bodyType,
            "modelYear": modelYear,
            "engineCapacity": engineCapacity,
            "modelGrade": modelGrade,
            "material": material,
            "make": make,
            "makeCode": makeCode,
            "modelCode": modelCode,
            "vehicleType": vehicleType,
            "transmissionType": transmissionType,
            "exteriorColours": exteriorColours,
            "interiorColours": interiorColours,
            "vehicleLocation": vehicleLocation,
            "internalVehicleNumber": internalVehicleNumber,
            "vehicleStatus": vehicleStatus,
            "vehicleUsage": vehicleUsage,
            "odometer": odometer,
            "fuelType": fuelType,
            "isHotOffer": isHotOffer,
            "basicExteriorColours": basicExteriorColours,
            "number_of_doors": number_of_doors,
            "number_of_seats": number_of_seats,
            "warranty": warranty,
        }

        return car_data

    async def run_scraper(self) -> None:
        """Run the scraper."""
        car_results: dict = await self.fetch_car_ids()
        if not car_results["status"]:
            print(f">= Automall: Error fetching car IDs: {car_results.get('message')}")
            return

        cars_ids = car_results.get("cars")
        if not cars_ids:
            print(">= Automall: No car IDs found to process.")
            return

        all_car_data = []

        for i in range(0, len(cars_ids), self.concurrency):
            batch_ids = cars_ids[i : i + self.concurrency]
            print(
                f">= Automall: Processing batch {i // self.concurrency + 1} with {len(batch_ids)} cars"
            )
            tasks = [self.get_car_data(id) for id in batch_ids]

            print(
                f">= Automall: Processing batch {i // self.concurrency + 1} with {len(batch_ids)} cars"
            )
            batch_results = await asyncio.gather(*tasks)

            for result in batch_results:
                all_car_data.append(result)

                df = pd.DataFrame([result])
                df.to_csv(
                    self.csv_file,
                    mode="a",
                    index=False,
                    header=not os.path.exists(self.csv_file),
                )

        print(f"\n>= Total cars processed and saved: {len(all_car_data)}")


async def main():
    async with Automall() as automall:
        await automall.run_scraper()


if __name__ == "__main__":
    asyncio.run(main())
