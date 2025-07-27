import curl_cffi
from rich import print

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    "content-type": "application/x-www-form-urlencoded",
    "Origin": "https://nxtcarsuae.com",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": "https://nxtcarsuae.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}

page = 0
total_hits = 0

while True:
    # Update the page number in the data string
    data = f'{{"requests":[{{"indexName":"Autotrust_Car","params":"facetFilters=%5B%5B%22bodyType%3A%22%5D%2C%5B%22brand%3A%22%5D%2C%5B%22modelDesc%3A%22%5D%2C%5B%22variant%3A%22%5D%5D&facets=%5B%22availableStatus%22%2C%22bodyColorDesc%22%2C%22bodyType%22%2C%22brand%22%2C%22driveType%22%2C%22engineSize%22%2C%22fuelType%22%2C%22hasOffer%22%2C%22mileage%22%2C%22modelDesc%22%2C%22modelYear%22%2C%22noOfDoors%22%2C%22noOfSeats%22%2C%22saleType%22%2C%22variant%22%2C%22vhlPrice%22%5D&filters=(saleType%3ARETAIL%20OR%20saleType%3ALUXURY%20OR%20saleType%3ACOMMERCIALS%20OR%20saleType%3A%22VALUE%20MILES%22)%20AND%20NOT%20attribute3%3A2%20AND%20NOT%20brand%3AJetour&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=300&maxValuesPerFacet=2000&page={page}&query=&tagFilters="}},{{"indexName":"Autotrust_Car","params":"analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22brand%3A%22%5D%2C%5B%22modelDesc%3A%22%5D%2C%5B%22variant%3A%22%5D%5D&facets=bodyType&filters=(saleType%3ARETAIL%20OR%20saleType%3ALUXURY%20OR%20saleType%3ACOMMERCIALS%20OR%20saleType%3A%22VALUE%20MILES%22)%20AND%20NOT%20attribute3%3A2%20AND%20NOT%20brand%3AJetour&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=2000&page=0&query="}},{{"indexName":"Autotrust_Car","params":"analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22bodyType%3A%22%5D%2C%5B%22modelDesc%3A%22%5D%2C%5B%22variant%3A%22%5D%5D&facets=brand&filters=(saleType%3ARETAIL%20OR%20saleType%3ALUXURY%20OR%20saleType%3ACOMMERCIALS%20OR%20saleType%3A%22VALUE%20MILES%22)%20AND%20NOT%20attribute3%3A2%20AND%20NOT%20brand%3AJetour&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=2000&page=0&query="}},{{"indexName":"Autotrust_Car","params":"analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22bodyType%3A%22%5D%2C%5B%22brand%3A%22%5D%2C%5B%22variant%3A%22%5D%5D&facets=modelDesc&filters=(saleType%3ARETAIL%20OR%20saleType%3ALUXURY%20OR%20saleType%3ACOMMERCIALS%20OR%20saleType%3A%22VALUE%20MILES%22)%20AND%20NOT%20attribute3%3A2%20AND%20NOT%20brand%3AJetour&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=2000&page=0&query="}},{{"indexName":"Autotrust_Car","params":"analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22bodyType%3A%22%5D%2C%5B%22brand%3A%22%5D%2C%5B%22modelDesc%3A%22%5D%5D&facets=variant&filters=(saleType%3ARETAIL%20OR%20saleType%3ALUXURY%20OR%20saleType%3ACOMMERCIALS%20OR%20saleType%3A%22VALUE%20MILES%22)%20AND%20NOT%20attribute3%3A2%20AND%20NOT%20brand%3AJetour&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=2000&page=0&query="}}]}}'

    response = curl_cffi.post(
        "https://75bazz5eei-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.24.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.14.0)%3B%20react%20(18.3.1)%3B%20react-instantsearch%20(6.40.4)&x-algolia-api-key=df42305d17c6341ba1fd8f021ceaf06b&x-algolia-application-id=75BAZZ5EEI",
        headers=headers,
        data=data,
    )
    json_data: dict = response.json()

    if json_data.get("status") and json_data.get("status") != 200:
        print(json_data.get("message"))
        break

    results: list = json_data.get("results", [])
    hits: list = results[0].get("hits", [])

    # Break if no hits found
    if len(hits) == 0:
        print(f">= No more hits found. Total hits scraped: {total_hits}")
        break

    print(f">= Page {page}: {len(hits)} hits found")
    total_hits += len(hits)

    # Process each hit
    for get_response in hits:
        id = get_response.get("_id")
        webDescription = get_response.get("webDescription")
        price = get_response.get("vhlPrice")
        brand = get_response.get("brand")
        modelYear = get_response.get("modelYear")

        # Just print the basic info
        print(
            f"ID: {id}, Brand: {brand}, Model: {webDescription}, Year: {modelYear}, Price: {price}"
        )

    # Increment page for next iteration
    page += 1
    print(f"\n>= Moving to page {page}...\n")

print(f"\n>= Scraping completed! Total vehicles found: {total_hits}")
