import json
import curl_cffi
from curl_cffi import AsyncSession
from selectolax.parser import HTMLParser
from rich import print
import asyncio


def get_car_data(data: dict) -> dict:

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
        "price": price,
        "priceMonthly": priceMonthly,
        "isHotOffer": isHotOffer,
        "basicExteriorColours": basicExteriorColours,
        "number_of_doors": number_of_doors,
        "number_of_seats": number_of_seats,
        "warranty": warranty,
    }

    print(car_data)


async def main():
    async with AsyncSession(impersonate="chrome", timeout=120) as session:
        response = await session.get(
            "https://www.automall.ae/en/used-cars-shop/details/knab25129lt575164/"
        )
        parser = HTMLParser(response.text)
        script = parser.css_first('script[id="__NEXT_DATA__"]')
        data: dict = json.loads(script.text())
        get_car_data(data)


if __name__ == "__main__":
    asyncio.run(main())
