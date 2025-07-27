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


class NxtCarsUae:
    """
    NxtCarsUae is a website that sells cars.
    """

    def __init__(self, concurrency: int = 100):
        """
        Initialize the NxtCarsUae class.
        """
        print(f"--------- NxtCarsUae Scraper Started ---------\n")
        self.session = AsyncSession(timeout=120, impersonate="chrome")

        today_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.csv_file = f"nxtcarsuae_{today_date}.csv"

        self.cars_url = "https://nxtcarsuae.com/sales"
        self.car_make_url = "https://nxtcarsuae.com/sales/car/"

        self.access_token = None
        self.headers = {}

    async def __aenter__(self):
        """Enter the context manager."""
        self.access_token = await self._get_bearer_token()
        if self.access_token and isinstance(self.access_token, str):
            self.headers = {"authorization": f"Bearer {self.access_token}"}
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

    async def _get_bearer_token(self):
        """
        Get the bearer token from the NxtCarsUae website.
        """

        response_data = await self._make_request(
            "post",
            "https://nxtcarsuae.com/api/generateToken",
        )
        if not response_data.get("status"):
            return response_data

        response = response_data.get("response")
        json_data: dict = response.json()
        access_token = json_data.get("access_token")
        return access_token

    async def fetch_car_ids(self) -> dict:
        """
        Fetch the car IDs from the NxtCarsUae website.
        """
        response_data = await self._make_request(
            "get",
            "https://nxtcarsuae.com/api/getCarIds",
        )

    async def get_car_data(self, id: str):
        """
        Get the car data from the NxtCarsUae website.
        Args:
            id (str): The ID of the car to get the data for.

        Returns:
            dict: The car data.
            status (bool): Whether the request was successful.
            message (str): The message from the request.
        """
        print(f">= NxtCarsUae: Scraping car details for {id}")

        response_data = await self._make_request(
            "get",
            f"https://api.nxt-website.awr-api.com/vehicles/{id}?origin=web",
            headers=self.headers,
        )

        response = response_data.get("response")
        if response.status_code != 200:
            return {
                "status": False,
                "message": f"NxtCarsUae API request failed for get_car_data: {response.text}",
            }

        json_data: dict = response.json()
        if json_data.get("code") != 200:
            return {
                "status": False,
                "message": f"NxtCarsUae API request failed for get_car_data: {json_data}",
            }

        get_response: dict = json_data.get("response")

        id = get_response.get("_id")
        price = get_response.get("vhlPrice")
        abs = get_response.get("abs")
        availableStatus = get_response.get("availableStatus")
        bodyColor = get_response.get("bodyColorDesc")
        bodyType = get_response.get("bodyType")
        brand = get_response.get("brand")
        currentOrganizationName = get_response.get("currentOrganizationName")

        engineSize = get_response.get("engineSize").strip()
        engineType = get_response.get("engineType")
        exteriorColor = get_response.get("exterior_color_description")
        fuelType = get_response.get("fuelType")
        installmentAmount = get_response.get("installmentAmount")
        inventoryItemId = get_response.get("inventoryItemId")
        itemCode = get_response.get("itemCode")
        make_description = get_response.get("make_description")
        mileage = get_response.get("mileage")
        model = get_response.get("model")
        modelDesc = get_response.get("modelDesc")
        modelYear = get_response.get("modelYear")
        noOfDoors = get_response.get("noOfDoors")
        noOfSeats = get_response.get("noOfSeats")
        saleType = get_response.get("saleType")
        serialNumber = get_response.get("serialNumber")
        specs = get_response.get("specs")
        transmission = get_response.get("transmission")
        trimColor = get_response.get("trimColorDesc")
        trimType = get_response.get("trimType")
        variant = get_response.get("variant")

        vehicleGender = get_response.get("vehicleGender")
        vehicleLocation = get_response.get("vehicleLocation")
        vin_last_5_digits = get_response.get("vin_last_5_digits")
        webBodyColorDesc = get_response.get("webBodyColorDesc")
        webBodyType = get_response.get("webBodyType")
        webBrand = get_response.get("webBrand")
        hasOffer = get_response.get("hasOffer")
        tagline = get_response.get("tagline")
        webDescription = get_response.get("webDescription")
        webTrimColorDesc = get_response.get("webTrimColorDesc")

        if webDescription:
            url = f"{self.car_make_url}{webDescription}"

        else:
            url = None

        car_data = {
            "title": webDescription,
            "url": url,
            "scrapedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "id": id,
            "price": price,
            "abs": abs,
            "availableStatus": availableStatus,
            "bodyColor": bodyColor,
            "bodyType": bodyType,
            "brand": brand,
            "currentOrganizationName": currentOrganizationName,
            "engineSize": engineSize,
            "engineType": engineType,
            "exteriorColor": exteriorColor,
            "fuelType": fuelType,
            "installmentAmount": installmentAmount,
            "inventoryItemId": inventoryItemId,
            "itemCode": itemCode,
            "make_description": make_description,
            "mileage": mileage,
            "model": model,
            "modelDesc": modelDesc,
            "modelYear": modelYear,
            "noOfDoors": noOfDoors,
            "noOfSeats": noOfSeats,
            "saleType": saleType,
            "serialNumber": serialNumber,
            "specs": specs,
            "transmission": transmission,
            "trimColor": trimColor,
            "trimType": trimType,
            "variant": variant,
            "vehicleGender": vehicleGender,
            "vehicleLocation": vehicleLocation,
            "vin_last_5_digits": vin_last_5_digits,
            "webBodyColorDesc": webBodyColorDesc,
            "webBodyType": webBodyType,
            "webBrand": webBrand,
            "hasOffer": hasOffer,
            "tagline": tagline,
            "webDescription": webDescription,
            "webTrimColorDesc": webTrimColorDesc,
        }

        return car_data

    async def run_scraper(self) -> None:
        """
        Run the scraper.
        """
        data = await self.get_car_data("46727577")
        print(data)


async def main():
    async with NxtCarsUae() as nxtcarsuae:
        await nxtcarsuae.run_scraper()


if __name__ == "__main__":
    asyncio.run(main())
