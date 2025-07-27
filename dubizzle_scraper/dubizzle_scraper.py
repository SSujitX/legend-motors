import json
import os
from curl_cffi import AsyncSession
import pandas as pd
from selectolax.parser import HTMLParser
from typing import Optional, Type, Dict, Any, List
from types import TracebackType
import asyncio
from datetime import datetime, timezone
from rich import print


class DubizzleScraper:
    def __init__(self):
        print(f"--------- Dubizzle Scraper Started ---------\n")

        self.today_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.csv_file = f"dubizzle_{self.today_date}.csv"

        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Origin": "https://uae.dubizzle.com",
            "Pragma": "no-cache",
            "Referer": "https://uae.dubizzle.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

    async def __aenter__(self):
        self.session = AsyncSession(impersonate="chrome", timeout=120)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.session:
            await self.session.close()

    def __attributes_to_retrieve(self) -> list[str]:
        """
        Attributes to retrieve from the API
        """
        attributes_to_retrieve = [
            "is_premium",
            "is_featured_agent",
            "location_list",
            "objectID",
            "name",
            "price",
            "neighbourhood",
            "agent_logo",
            "can_chat",
            "has_whatsapp_number",
            "details",
            "photo_thumbnails",
            "photos",
            "highlighted_ad",
            "absolute_url",
            "id",
            "category_id",
            "uuid",
            "category",
            "has_phone_number",
            "category_v2",
            "photos_count",
            "created_at",
            "site",
            "permalink",
            "has_vin",
            "auto_agent_id",
            "is_trusted_seller",
            "show_trusted_seller_logo",
            "trusted_seller_logo",
            "trusted_seller_id",
            "created_at",
            "added",
            "jobs_logo",
            "vas",
            "seller_type",
            "is_verified_user",
            "is_verified_business",
            "has_video",
            "is_super_ad",
            "categories",
            "city",
            "bedrooms",
            "bathrooms",
            "size",
            "neighborhoods",
            "agent",
            "room_type",
            "is_reserved",
            "is_coming_soon",
            "user.id",
            "business",
            "inventory_type",
            "is_ecommerce_listing",
            "has_variants",
        ]
        return attributes_to_retrieve

    async def _extract_data(self, hit: dict) -> list[dict]:

        details = hit.get("details", {})

        # --- Extract all data into variables ---
        posting_date_ts = hit.get("created_at")
        posting_date = (
            datetime.fromtimestamp(posting_date_ts).strftime("%Y-%m-%d %H:%M:%S")
            if posting_date_ts
            else None
        )
        added_ts = hit.get("added")
        added_date = (
            datetime.fromtimestamp(added_ts).strftime("%Y-%m-%d %H:%M:%S")
            if added_ts
            else None
        )

        full_name = hit.get("name", {}).get("en")
        description = hit.get("name", {}).get("en")
        location = ", ".join(hit.get("location_list", {}).get("en", []))
        price = hit.get("price")
        item_id = hit.get("id")
        category_id = hit.get("category_id")
        category_path = hit.get("category_v2", {}).get("slug_paths", [])
        permalink = hit.get("permalink")
        object_id = hit.get("objectID")
        uuid = hit.get("uuid")
        photos = hit.get("photos", {})
        # photo_thumbnails = hit.get("photo_thumbnails", [])
        photos_count = hit.get("photos_count")
        city = hit.get("site", {}).get("en")
        auto_agent_id = hit.get("auto_agent_id")
        business = hit.get("business")
        inventory_type = hit.get("inventory_type")
        vas = hit.get("vas")
        user_id = hit.get("user", {}).get("id")

        # Boolean and status fields
        is_premium = hit.get("is_premium")
        is_reserved = hit.get("is_reserved")
        is_coming_soon = hit.get("is_coming_soon")
        has_phone_number = hit.get("has_phone_number")
        has_whatsapp_number = hit.get("has_whatsapp_number")
        has_vin = hit.get("has_vin")
        is_verified_user = hit.get("is_verified_user")
        is_verified_business = hit.get("is_verified_business")
        has_video = hit.get("has_video")
        is_super_ad = hit.get("is_super_ad")
        is_featured_agent = hit.get("is_featured_agent")
        can_chat = hit.get("can_chat")
        highlighted_ad = hit.get("highlighted_ad")
        is_ecommerce_listing = hit.get("is_ecommerce_listing")
        has_variants = hit.get("has_variants")

        # Details from the 'details' object
        car_make = details.get("Make", {}).get("en", {}).get("value")
        car_model = details.get("Model", {}).get("en", {}).get("value")
        trim = details.get("Trim", {}).get("en", {}).get("value")
        motors_trim = details.get("Motors Trim", {}).get("en", {}).get("value")
        agent = details.get("Agent", {}).get("en", {}).get("value")
        vehicle_reference = (
            details.get("Vehicle Reference", {}).get("en", {}).get("value")
        )
        year = details.get("Year", {}).get("en", {}).get("value")
        kilometers = details.get("Kilometers", {}).get("en", {}).get("value")
        regional_specs = details.get("Regional Specs", {}).get("en", {}).get("value")
        doors = details.get("Doors", {}).get("en", {}).get("value")
        body_type = details.get("Body Type", {}).get("en", {}).get("value")
        fuel_type = details.get("Fuel Type", {}).get("en", {}).get("value")
        seller_type = details.get("Seller type", {}).get("en", {}).get("value")
        seating_capacity = (
            details.get("Seating Capacity", {}).get("en", {}).get("value")
        )
        transmission_type = (
            details.get("Transmission Type", {}).get("en", {}).get("value")
        )
        engine_capacity_cc = (
            details.get("Engine Capacity (cc)", {}).get("en", {}).get("value")
        )
        horsepower = details.get("Horsepower", {}).get("en", {}).get("value")
        no_of_cylinders = details.get("No. of Cylinders", {}).get("en", {}).get("value")
        warranty = details.get("Warranty", {}).get("en", {}).get("value")
        exterior_color = details.get("Exterior Color", {}).get("en", {}).get("value")
        interior_color = details.get("Interior Color", {}).get("en", {}).get("value")
        target_market = details.get("Target Market", {}).get("en", {}).get("value")
        steering_side = details.get("Steering Side", {}).get("en", {}).get("value")

        # Correctly handle lists for extras and technical_features
        extras_list = details.get("Extras", {}).get("en", {}).get("value", [])
        extras = extras_list if isinstance(extras_list, list) else []

        tech_features_list = (
            details.get("Technical Features", {}).get("en", {}).get("value", [])
        )
        technical_features = (
            tech_features_list if isinstance(tech_features_list, list) else []
        )

        # # --- Construct car_data from variables ---
        car_data = {
            "posting_date": posting_date,
            "added_date": added_date,
            "scrape_date": self.today_date,
            # "full_name": full_name,
            "name": f"{car_make} {car_model} {trim}",
            "description": description,
            "location": location,
            "city": city,
            "car_make": car_make,
            "car_model": car_model,
            "price": price,
            "trim": trim,
            "motors_trim": motors_trim,
            "agent": agent,
            "year": year,
            "kilometers": kilometers,
            "regional_specs": regional_specs,
            "doors": doors,
            "item_id": item_id,
            "category_id": category_id,
            "category_path": category_path,
            "vehicle_reference": vehicle_reference,
            "body_type": body_type,
            "fuel_type": fuel_type,
            "seller_type": seller_type,
            "seating_capacity": seating_capacity,
            "transmission_type": transmission_type,
            "engine_capacity_cc": engine_capacity_cc,
            "extras": extras,
            "technical_features": technical_features,
            "horsepower": horsepower,
            "no_of_cylinders": no_of_cylinders,
            "warranty": warranty,
            "exterior_color": exterior_color,
            "interior_color": interior_color,
            "target_market": target_market,
            "steering_side": steering_side,
            "permalink": permalink,
            "object_id": object_id,
            "uuid": uuid,
            "photos": photos,
            # "photo_thumbnails": photo_thumbnails,
            "photos_count": photos_count,
            "auto_agent_id": auto_agent_id,
            "business": business,
            "inventory_type": inventory_type,
            "vas": vas,
            "user_id": user_id,
            "is_premium": is_premium,
            "is_reserved": is_reserved,
            "is_coming_soon": is_coming_soon,
            "has_phone_number": has_phone_number,
            "has_whatsapp_number": has_whatsapp_number,
            "has_vin": has_vin,
            "is_verified_user": is_verified_user,
            "is_verified_business": is_verified_business,
            "has_video": has_video,
            "is_super_ad": is_super_ad,
            "is_featured_agent": is_featured_agent,
            "can_chat": can_chat,
            "highlighted_ad": highlighted_ad,
            "is_ecommerce_listing": is_ecommerce_listing,
            "has_variants": has_variants,
        }
        # print(car_data)

        df = pd.DataFrame([car_data])
        df.to_csv(
            self.csv_file,
            mode="a",
            index=False,
            header=not os.path.exists(self.csv_file),
        )

    async def fetch_data(self):
        """
        Fetch data from dubizzle
        """
        page = 1
        while True:

            url = "https://wd0ptz13zs-1.algolianet.com/1/indexes/*/queries"

            params = {
                "x-algolia-agent": "Algolia for JavaScript (4.24.0); Browser (lite)",
                "x-algolia-api-key": "cef139620248f1bc328a00fddc7107a6",
                "x-algolia-application-id": "WD0PTZ13ZS",
            }

            data = {
                "requests": [
                    {
                        "indexName": "motors_textualized.com",
                        "query": "",
                        "params": f'page={page}&attributesToHighlight=[]&hitsPerPage=25&attributesToRetrieve={json.dumps(self.__attributes_to_retrieve())}&filters=("category_v2.slug_paths":"motors/used-cars")&ruleContexts=["all_user"]',
                    },
                    {
                        "indexName": "motors_textualized.com",
                        "query": "",
                        "params": 'hitsPerPage=1000&attributesToRetrieve=["uuid"]&attributesToHighlight=[]&distinct=0&filters=("category_v2.slug_paths":"motors/used-cars") AND (is_cotw_booked: true)',
                    },
                ]
            }

            response = await self.session.post(
                url, params=params, headers=self.headers, json=data
            )
            response.raise_for_status()

            json_response: dict = response.json()
            results: list[dict] = json_response.get("results")
            hits: list[dict] = results[0].get("hits")
            if len(hits) == 0:
                print(f">= Dubizzle: No hits found in page {page}")
                break

            print(f">= Dubizzle: Found {len(hits)} hits in page {page}")

            for hit in hits:
                await self._extract_data(hit)

            page += 1


async def main():
    async with DubizzleScraper() as scraper:
        await scraper.fetch_data()


if __name__ == "__main__":
    asyncio.run(main())
