import curl_cffi
from selectolax.parser import HTMLParser
from rich import print
import json

url = "https://www.kavak.com/ae/cars-for-sale/toyota-veloz-gx-suv-2023"
# script[id="vip-snippet"]

response = curl_cffi.get(url, impersonate="chrome")
parser = HTMLParser(response.text)
script = parser.css_first("script[id='vip-snippet']").text(strip=True)
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
vehicleengineDisplacementunitCode = vehicleengineDisplacement.get("unitCode")
vehicleengineDisplacementValue = vehicleengineDisplacement.get("value")

vehiclePerformance = vehicleEngine.get("performance.max_power_hp", {})
vehiclePerformancemaxPowerunitCode = vehiclePerformance.get("unitCode")
vehiclePerformancemaxPowervalue = vehiclePerformance.get("value")


car_info = {
    "name": name,
    "url": url,
    "offerprice": offerprice,
    "offerpriceCurrency": offerpriceCurrency,
    "mileageunitCode": mileageunitCode,
    # "mileageValue": mileageValue,
    # "vehicleConfiguration": vehicleConfiguration,
    # "vehicleModelDate": vehicleModelDate,
    "bodyType": bodyType,
    "vehicleIdentificationNumber": vehicleIdentificationNumber,
    # "vehicleTransmission": vehicleTransmission,
    "numberOfAxles": numberOfAxles,
    "doors": bodyStyle,
    "passenger": seats,
    # "vehiclename": vehiclename,
    "type": vehiclefuelType,
    # "vehicleengineDisplacementunitCode": vehicleengineDisplacementunitCode,
    "liters": vehicleengineDisplacementValue,
    # "vehiclePerformancemaxPowerunitCode": vehiclePerformancemaxPowerunitCode,
    "maxPower": vehiclePerformancemaxPowervalue,
}
print(car_info)
