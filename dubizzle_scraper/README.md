# Dubizzle Scraper

A powerful asynchronous scraper for Dubizzle.com, the Middle East's largest online marketplace. This scraper specializes in extracting comprehensive automotive listings from Dubizzle's UAE platform with high efficiency and accuracy.

## 🏪 About Dubizzle

Dubizzle.com is the leading online marketplace in the Middle East, connecting millions of users across the region. The UAE platform features an extensive automotive section with thousands of vehicle listings from dealers and private sellers.

## ✨ Features

- **Asynchronous Processing**: High-performance async/await architecture
- **Smart Data Extraction**: Advanced JSON parsing and data normalization
- **Configurable Concurrency**: Adjustable concurrent request limits (default: 100)
- **Comprehensive Vehicle Data**: Detailed specifications, pricing, and seller information
- **CSV Export**: Automatic timestamped data export
- **Robust Error Handling**: Built-in retry mechanisms and error recovery
- **Browser Simulation**: Chrome impersonation for reliable access

## 📊 Data Fields Extracted

### Vehicle Information
- **ID**: Unique listing identifier
- **Title**: Vehicle listing title
- **Price**: Listed price in AED
- **Currency**: Price currency (AED)
- **Make**: Vehicle manufacturer
- **Model**: Vehicle model
- **Trim**: Specific trim level
- **Year**: Model year
- **Kilometers**: Odometer reading
- **Regional Specs**: UAE, GCC, or other specifications
- **Body Type**: Sedan, SUV, Hatchback, etc.
- **Fuel Type**: Petrol, Diesel, Hybrid, Electric
- **Transmission**: Manual or Automatic
- **Engine Capacity**: Engine size specification
- **Cylinders**: Number of engine cylinders
- **Horsepower**: Engine power output
- **Warranty**: Warranty information
- **Color**: Exterior color
- **Doors**: Number of doors
- **Seating Capacity**: Number of seats

### Location & Seller Information
- **Location**: Vehicle location in UAE
- **City**: Specific city
- **Area**: Neighborhood or area
- **Seller Type**: Dealer or Individual
- **Seller Name**: Name of the seller
- **Contact Information**: Available contact details

### Additional Details
- **Listing Date**: When the vehicle was posted
- **Last Updated**: Most recent update timestamp
- **View Count**: Number of times viewed
- **Features**: Additional vehicle features and equipment
- **Condition**: Vehicle condition description
- **Accident History**: Accident-free status
- **Service History**: Maintenance records availability

## 🚀 Usage

### Standalone Execution

```powershell
# Navigate to the dubizzle_scraper directory
cd dubizzle_scraper

# Run the scraper
uv run dubizzle_scraper.py
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
from dubizzle_scraper import DubizzleScraper

async def main():
    # Custom configuration
    async with DubizzleScraper(concurrency=80, timeout=100) as scraper:
        await scraper.run_scraper()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 Configuration

### Performance Settings

- **Default Concurrency**: 100 concurrent requests
- **Request Timeout**: 120 seconds
- **Browser Impersonation**: Chrome latest version
- **Rate Limiting**: Respectful request timing

### API Endpoints

- **Base URL**: `https://dubai.dubizzle.com/`
- **Motors Section**: `/motors/`
- **Search API**: `/api/search/`
- **Listing Details**: `/api/listings/{listing_id}`

## 📁 Files

- **`dubizzle_scraper.py`**: Main scraper implementation
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

1. **Initial Request**: Accesses Dubizzle motors section
2. **Listing Discovery**: Identifies all available vehicle listings
3. **Parallel Processing**: Concurrently fetches detailed information
4. **JSON Parsing**: Extracts structured data from API responses
5. **Data Normalization**: Standardizes and cleans extracted data
6. **CSV Export**: Saves comprehensive data to timestamped file

## 📈 Performance Metrics

- **Concurrent Requests**: Up to 100 simultaneous API calls
- **Data Processing**: Efficient memory usage with streaming
- **Error Recovery**: Automatic retry on network failures
- **Rate Limiting**: Built-in respectful request timing

## 🚨 Important Notes

- **Legal Compliance**: Ensure adherence to Dubizzle.com terms of service
- **Rate Limiting**: Built-in respectful scraping practices
- **Data Accuracy**: Real-time data from Dubizzle platform
- **Regional Focus**: Optimized for UAE listings

## 🛠️ Development

### Adding Custom Filters

Modify search parameters to add specific filters:

```python
# Example: Filter by price range and location
search_filters = {
    "price_min": 30000,
    "price_max": 150000,
    "location": "dubai",
    "make": "toyota"
}
```

### Extending Data Fields

To extract additional vehicle information:

```python
def extract_vehicle_details(self, listing_json):
    # Add new fields to extraction
    details = {
        # ... existing fields ...
        "insurance_type": listing_json.get("insurance", ""),
        "financing_available": listing_json.get("financing", False),
        "trade_in_accepted": listing_json.get("trade_in", False)
    }
    return details
```

### Custom Output Formats

Support additional export formats:

```python
# JSON export
import json
with open(f"dubizzle_{date}.json", "w") as f:
    json.dump(listings_data, f, indent=2)

# Excel export with multiple sheets
with pd.ExcelWriter(f"dubizzle_{date}.xlsx") as writer:
    df.to_excel(writer, sheet_name="Vehicles", index=False)
    summary_df.to_excel(writer, sheet_name="Summary", index=False)
```

## 📄 Output Format

The scraper generates CSV files with the following naming convention:
```
dubizzle_YYYY-MM-DD.csv
```

Example output structure:
```csv
id,title,price,currency,make,model,year,kilometers,location,seller_type,fuel_type,transmission
12345,"2020 Toyota Camry 2.5L",85000,AED,Toyota,Camry,2020,45000,Dubai,Dealer,Petrol,Automatic
```

## 🔍 Advanced Features

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

### Data Validation

Built-in validation ensures data quality:

- **Price Validation**: Numeric price verification
- **Date Validation**: Proper timestamp formatting
- **Required Fields**: Essential data presence checking
- **Data Types**: Automatic type conversion
- **Duplicate Detection**: Removal of duplicate listings

### Geographic Filtering

Location-based filtering options:

```python
# UAE cities and areas
locations = {
    "dubai": ["downtown", "marina", "jlt", "deira"],
    "abu_dhabi": ["khalifa_city", "al_reem", "yas_island"],
    "sharjah": ["al_nahda", "al_qasimia", "al_majaz"],
    "ajman": ["al_nuaimiya", "al_rashidiya"],
    "ras_al_khaimah": ["al_nakheel", "al_hamra"]
}
```

## 🆘 Troubleshooting

### Common Issues

1. **Connection Timeouts**:
   - Reduce concurrency setting
   - Increase timeout duration
   - Check network stability

2. **No Data Retrieved**:
   - Verify Dubizzle.com accessibility
   - Check if API endpoints have changed
   - Validate search parameters

3. **Rate Limiting Errors**:
   - Reduce request frequency
   - Implement exponential backoff
   - Add random delays between requests

4. **Memory Issues**:
   - Process data in smaller batches
   - Implement streaming for large datasets
   - Monitor system resources

### Debug Mode

Enable comprehensive logging:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dubizzle_scraper.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Optimization

Optimize for different scenarios:

```python
# High-speed configuration
scraper = DubizzleScraper(
    concurrency=200,  # Increase for powerful systems
    timeout=60,       # Reduce for faster failures
    retry_attempts=1  # Minimize retries for speed
)

# Conservative configuration
scraper = DubizzleScraper(
    concurrency=25,   # Reduce for stability
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

## 🔒 Security & Privacy

- **Public Data Only**: Extracts only publicly available information
- **Respectful Scraping**: Adheres to robots.txt guidelines
- **Secure Communication**: HTTPS-only connections
- **Local Storage**: All data stored locally
- **No Personal Data**: Avoids collecting personal information

## 📈 Analytics & Insights

The scraper can provide valuable market insights:

- **Price Trends**: Track pricing patterns over time
- **Popular Models**: Identify most listed vehicle types
- **Geographic Distribution**: Analyze listing distribution by location
- **Seller Analysis**: Compare dealer vs. individual listings
- **Market Activity**: Monitor listing frequency and updates

---

**Part of the Legend Scrapers collection - Comprehensive automotive marketplace data extraction**