# NxtCarsUAE Scraper

A sophisticated asynchronous scraper for NxtCarsUAE.com, a prominent automotive marketplace in the United Arab Emirates. This scraper efficiently extracts comprehensive vehicle data, pricing information, and detailed specifications from the NxtCarsUAE platform with advanced authentication handling.

## 🚗 About NxtCarsUAE

NxtCarsUAE.com is a leading digital automotive platform in the UAE that connects car buyers and sellers through a modern, user-friendly interface. The platform features a diverse inventory of new and used vehicles with detailed specifications, competitive pricing, and comprehensive seller information.

## ✨ Features

- **Asynchronous Architecture**: High-performance async/await implementation
- **Advanced Authentication**: Automatic bearer token management and refresh
- **Smart Pagination**: Intelligent handling of paginated vehicle listings
- **Configurable Concurrency**: Adjustable concurrent request limits (default: 100)
- **Comprehensive Data Mining**: Vehicle details, pricing, specifications, and seller data
- **CSV Export**: Timestamped data export with rich formatting
- **Robust Error Handling**: Built-in retry mechanisms and error recovery
- **API Integration**: Direct API access for reliable data extraction

## 📊 Data Fields Extracted

### Vehicle Information
- **ID**: Unique vehicle identifier
- **Title**: Complete vehicle listing title
- **Price**: Current market price in AED
- **Currency**: Price currency (AED)
- **Model Year**: Manufacturing year
- **Make**: Vehicle manufacturer (Toyota, BMW, Mercedes, etc.)
- **Model**: Specific vehicle model
- **Variant**: Trim level and engine specifications
- **Mileage**: Odometer reading in kilometers
- **Fuel Type**: Petrol, Diesel, Hybrid, Electric
- **Transmission**: Manual or Automatic
- **Body Type**: Sedan, SUV, Hatchback, Coupe, etc.
- **Engine**: Engine specifications and capacity
- **Cylinders**: Number of engine cylinders
- **Horsepower**: Engine power output
- **Color**: Exterior color
- **Interior Color**: Interior color scheme
- **Doors**: Number of doors
- **Seating**: Seating capacity

### Technical Specifications
- **Drive Type**: FWD, RWD, AWD, 4WD
- **Fuel Economy**: Fuel consumption ratings
- **Emissions**: CO2 emissions data
- **Safety Rating**: Vehicle safety scores
- **Features**: Comprehensive feature list
- **Options**: Available options and packages
- **Condition**: Vehicle condition assessment
- **Regional Specs**: UAE, GCC, or other specifications

### Location & Seller Information
- **Location**: Vehicle location in UAE
- **City**: Specific city
- **Area**: Neighborhood or area
- **Seller Type**: Dealer or Individual
- **Seller Name**: Name of the seller/dealer
- **Seller Rating**: Seller reputation score
- **Contact Information**: Available contact details
- **Showroom**: Dealer showroom information

### Listing Details
- **Listing Date**: When the vehicle was posted
- **Last Updated**: Most recent update timestamp
- **View Count**: Number of times viewed
- **Favorites**: Number of users who favorited
- **Status**: Active, Sold, Reserved
- **Verification**: Listing verification status

## 🚀 Usage

### Standalone Execution

```powershell
# Navigate to the nxtcarsuae_scraper directory
cd nxtcarsuae_scraper

# Run the scraper
uv run nxtcarsuae_scraper.py
```

### Integration with Main App

The scraper is automatically included when running the main application:

```powershell
# From the root directory
uv run app.py
```

### Custom Configuration

```python
import asyncio
from nxtcarsuae_scraper import NxtCarsUae

async def main():
    # Custom configuration with specific parameters
    async with NxtCarsUae(concurrency=80, timeout=100) as scraper:
        await scraper.fetch_data()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 Configuration

### Performance Settings

- **Default Concurrency**: 100 concurrent requests
- **Request Timeout**: 120 seconds
- **Authentication**: Bearer token management
- **Rate Limiting**: Respectful request timing

### API Endpoints

- **Base URL**: `https://www.nxtcarsuae.com/`
- **Authentication**: `/api/auth/token`
- **Search API**: `/api/vehicles/search`
- **Vehicle Details**: `/api/vehicles/{vehicle_id}`
- **Filters**: Advanced filtering capabilities

## 📁 Files

- **`nxtcarsuae_scraper.py`**: Main scraper implementation
- **`requirements.txt`**: Module-specific dependencies
- **`pyproject.toml`**: Module configuration
- **`uv.lock`**: Dependency lock file

## 📦 Dependencies

```toml
[dependencies]
curl-cffi = ">=0.11.1"
pandas = ">=2.2.3"
rich = ">=14.0.0"
selectolax = ">=0.3.29"
```

## 🔍 How It Works

1. **Authentication**: Obtains bearer token for API access
2. **Initial Request**: Accesses NxtCarsUAE homepage
3. **Vehicle Discovery**: Identifies all available vehicle listings
4. **Parallel Processing**: Concurrently fetches detailed vehicle information
5. **Data Extraction**: Parses comprehensive vehicle data from API responses
6. **Data Normalization**: Standardizes and validates extracted data
7. **CSV Export**: Saves comprehensive data to timestamped file

## 📈 Performance Metrics

- **Concurrent Requests**: Up to 100 simultaneous API calls
- **Data Processing**: Efficient memory usage with streaming
- **Error Recovery**: Automatic retry on network failures
- **Authentication**: Automatic token refresh and management
- **Rate Limiting**: Built-in respectful request timing

## 🚨 Important Notes

- **Legal Compliance**: Ensure adherence to NxtCarsUAE.com terms of service
- **Authentication Required**: Automatic bearer token management
- **Rate Limiting**: Built-in respectful scraping practices
- **Data Accuracy**: Real-time data from NxtCarsUAE platform
- **API Access**: Direct API integration for reliable data

## 🛠️ Development

### Adding Custom Filters

Modify search parameters to add specific filters:

```python
# Example: Filter by price range and specific criteria
search_filters = {
    "price_min": 35000,
    "price_max": 180000,
    "year_min": 2019,
    "make": "toyota",
    "body_type": "suv",
    "fuel_type": "petrol"
}
```

### Extending Data Fields

To extract additional vehicle information:

```python
def extract_vehicle_details(self, vehicle_json):
    # Add new fields to extraction
    details = {
        # ... existing fields ...
        "insurance_included": vehicle_json.get("insurance", False),
        "financing_available": vehicle_json.get("financing_options", []),
        "trade_in_accepted": vehicle_json.get("trade_in", False),
        "home_delivery": vehicle_json.get("delivery_options", {})
    }
    return details
```

### Authentication Management

Custom authentication handling:

```python
async def refresh_token(self):
    """Refresh bearer token when expired"""
    auth_response = await self.session.post(
        "https://www.nxtcarsuae.com/api/auth/refresh",
        headers=self.headers
    )
    if auth_response.status_code == 200:
        token_data = auth_response.json()
        self.bearer_token = token_data.get("access_token")
        self.headers["Authorization"] = f"Bearer {self.bearer_token}"
```

### Custom Output Formats

Support additional export formats:

```python
# JSON export with nested structure
import json
with open(f"nxtcarsuae_{date}.json", "w") as f:
    json.dump(vehicles_data, f, indent=2, ensure_ascii=False)

# Excel export with multiple sheets
with pd.ExcelWriter(f"nxtcarsuae_{date}.xlsx") as writer:
    df.to_excel(writer, sheet_name="Vehicles", index=False)
    sellers_df.to_excel(writer, sheet_name="Sellers", index=False)
    specs_df.to_excel(writer, sheet_name="Specifications", index=False)
```

## 📄 Output Format

The scraper generates CSV files with the following naming convention:
```
nxtcarsuae_YYYY-MM-DD.csv
```

Example output structure:
```csv
id,title,price,currency,modelYear,make,model,variant,mileage,fuelType,transmission,location,sellerType
12345,"2020 Toyota Camry 2.5L SE",85000,AED,2020,Toyota,Camry,2.5L SE,45000,Petrol,Automatic,Dubai,Dealer
```

## 🔍 Advanced Features

### Authentication System

NxtCarsUAE's authentication features:

- **Bearer Token**: Automatic token acquisition and management
- **Token Refresh**: Automatic token renewal when expired
- **Session Management**: Persistent session handling
- **API Access**: Direct API endpoint access
- **Rate Limiting**: Respectful API usage

### Search Filtering

The scraper supports comprehensive filtering:

- **Price Range**: Minimum and maximum price filters
- **Year Range**: Model year filtering
- **Mileage Range**: Kilometer-based filtering
- **Location**: City and area-specific searches
- **Make/Model**: Brand and model filtering
- **Fuel Type**: Petrol, Diesel, Hybrid, Electric
- **Transmission**: Manual or Automatic
- **Body Type**: Vehicle category filtering
- **Seller Type**: Dealer or individual seller
- **Condition**: New, Used, Certified Pre-Owned

### Data Validation

Built-in validation ensures data quality:

- **Price Validation**: Numeric price verification
- **Date Validation**: Proper timestamp formatting
- **Required Fields**: Essential data presence checking
- **Data Types**: Automatic type conversion
- **Duplicate Detection**: Removal of duplicate listings
- **Authentication**: Token validity checking

## 🆘 Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Check bearer token validity
   - Verify API endpoint accessibility
   - Ensure proper header formatting

2. **Connection Timeouts**:
   - Reduce concurrency setting
   - Increase timeout duration
   - Check network stability

3. **No Data Retrieved**:
   - Verify NxtCarsUAE.com accessibility
   - Check if API endpoints have changed
   - Validate authentication credentials

4. **Rate Limiting Errors**:
   - Reduce request frequency
   - Implement exponential backoff
   - Add random delays between requests

### Debug Mode

Enable comprehensive logging:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nxtcarsuae_scraper.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Optimization

Optimize for different scenarios:

```python
# High-speed configuration
scraper = NxtCarsUae(
    concurrency=150,  # Increase for powerful systems
    timeout=60,       # Reduce for faster failures
    retry_attempts=2  # Minimize retries for speed
)

# Reliable configuration
scraper = NxtCarsUae(
    concurrency=50,   # Reduce for stability
    timeout=180,      # Increase for reliability
    retry_attempts=5  # More retries for completeness
)
```

## 📊 Data Quality Assurance

The scraper implements multiple quality checks:

- **Completeness**: Ensures all required fields are populated
- **Consistency**: Validates data format consistency
- **Accuracy**: Cross-references data points for accuracy
- **Freshness**: Tracks listing dates and updates
- **Deduplication**: Removes duplicate entries automatically
- **Authentication**: Validates API access and permissions

## 🔒 Security & Privacy

- **Secure Authentication**: Bearer token-based API access
- **Public Data Only**: Extracts only publicly available information
- **Respectful Scraping**: Adheres to robots.txt guidelines
- **Secure Communication**: HTTPS-only connections
- **Local Storage**: All data stored locally
- **No Personal Data**: Avoids collecting personal information

## 📈 Market Insights

The scraper provides valuable automotive market data:

- **Price Trends**: Track NxtCarsUAE pricing patterns
- **Popular Models**: Identify most listed vehicle types
- **Geographic Distribution**: Analyze listing distribution by location
- **Seller Analysis**: Compare dealer vs. individual listings
- **Market Activity**: Monitor listing frequency and updates
- **Feature Popularity**: Analyze most requested vehicle features

## 🌟 NxtCarsUAE Advantages

Unique benefits of scraping NxtCarsUAE data:

- **API Access**: Direct API integration for reliable data
- **Comprehensive Data**: Detailed vehicle specifications
- **Seller Information**: Rich seller and dealer data
- **Real-time Updates**: Current market information
- **Professional Platform**: High-quality listings
- **UAE Focus**: Specialized for UAE automotive market

---

**Part of the Legend Scrapers collection - Advanced automotive marketplace data extraction with API integration**