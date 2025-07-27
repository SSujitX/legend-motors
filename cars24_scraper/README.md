# Cars24 Scraper

A sophisticated asynchronous scraper for Cars24.ae, one of the UAE's premier online automotive marketplaces. This scraper efficiently extracts detailed vehicle information, pricing data, and comprehensive specifications.

## 🚗 About Cars24

Cars24.ae is a leading digital automotive platform in the UAE that revolutionizes the car buying and selling experience. The platform offers a curated selection of quality used vehicles with transparent pricing and detailed vehicle histories.

## ✨ Features

- **Asynchronous Architecture**: High-performance async/await implementation
- **Smart Pagination**: Automatic handling of paginated results
- **Configurable Concurrency**: Adjustable concurrent request limits (default: 100)
- **Comprehensive Data Mining**: Vehicle details, pricing, specifications, and seller information
- **CSV Export**: Timestamped data export functionality
- **Robust Error Handling**: Built-in retry mechanisms and error recovery
- **Browser Impersonation**: Chrome browser simulation for reliable access

## 📊 Data Fields Extracted

### Vehicle Information
- **ID**: Unique vehicle identifier
- **Title**: Vehicle listing title
- **Price**: Current market price in AED
- **Original Price**: Initial listing price
- **Discount**: Available discount amount
- **Model Year**: Manufacturing year
- **Make**: Vehicle manufacturer (Toyota, BMW, etc.)
- **Model**: Specific vehicle model
- **Variant**: Trim level and specifications
- **Mileage**: Odometer reading
- **Fuel Type**: Petrol, Diesel, Hybrid, Electric
- **Transmission**: Manual or Automatic
- **Body Type**: Sedan, SUV, Hatchback, etc.
- **Engine**: Engine specifications
- **Color**: Exterior color
- **Location**: Vehicle location in UAE
- **Seller Type**: Dealer or Individual
- **Listing Date**: When the vehicle was listed
- **Features**: Additional vehicle features and equipment

## 🚀 Usage

### Standalone Execution

```powershell
# Navigate to the cars24_scraper directory
cd cars24_scraper

# Run the scraper
uv run cars24_scraper.py
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
from cars24_scraper import CarScraper

async def main():
    # Custom concurrency and timeout settings
    async with CarScraper(concurrency=75, timeout=90) as scraper:
        await scraper.fetch_data()

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

- **Base URL**: `https://www.cars24.ae/`
- **Search API**: `/api/search/cars`
- **Vehicle Details**: `/api/cars/{vehicle_id}`
- **Filters**: Advanced filtering capabilities

## 📁 Files

- **`cars24_scraper.py`**: Main scraper implementation
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

1. **Initial Request**: Fetches the main Cars24.ae page
2. **Car ID Extraction**: Identifies all available vehicle listings
3. **Parallel Processing**: Concurrently fetches detailed information for each vehicle
4. **Data Normalization**: Processes and standardizes extracted data
5. **CSV Export**: Saves comprehensive data to timestamped file

## 📈 Performance Metrics

- **Concurrent Requests**: Up to 100 simultaneous API calls
- **Data Processing**: Efficient memory usage with streaming
- **Error Recovery**: Automatic retry on network failures
- **Rate Limiting**: Built-in respectful request timing

## 🚨 Important Notes

- **Legal Compliance**: Ensure adherence to Cars24.ae terms of service
- **Rate Limiting**: Built-in respectful scraping practices
- **Data Accuracy**: Real-time data from Cars24.ae platform
- **Network Requirements**: Stable internet connection required

## 🛠️ Development

### Adding Custom Filters

Modify the search parameters to add specific filters:

```python
# Example: Filter by price range and fuel type
search_params = {
    "min_price": 50000,
    "max_price": 200000,
    "fuel_type": "petrol",
    "body_type": "suv"
}
```

### Extending Data Fields

To extract additional vehicle information, modify the data extraction logic:

```python
def extract_vehicle_data(self, vehicle_json):
    # Add new fields to extraction
    data = {
        # ... existing fields ...
        "new_field": vehicle_json.get("new_field", ""),
        "custom_attribute": self.parse_custom_attribute(vehicle_json)
    }
    return data
```

### Custom Output Formats

Extend the scraper to support additional output formats:

```python
# JSON export
import json
with open(f"cars24_{date}.json", "w") as f:
    json.dump(vehicle_data, f, indent=2)

# Excel export
df.to_excel(f"cars24_{date}.xlsx", index=False)
```

## 📄 Output Format

The scraper generates CSV files with the following naming convention:
```
cars24_YYYY-MM-DD.csv
```

Example output structure:
```csv
id,title,price,originalPrice,discount,modelYear,make,model,variant,mileage,fuelType,transmission
12345,"2020 Toyota Camry 2.5L",85000,90000,5000,2020,Toyota,Camry,2.5L SE,45000,Petrol,Automatic
```

## 🔍 Advanced Features

### Search Filtering

The scraper supports advanced filtering options:

- **Price Range**: Minimum and maximum price filters
- **Year Range**: Model year filtering
- **Mileage**: Odometer reading filters
- **Location**: Geographic filtering within UAE
- **Make/Model**: Brand and model specific searches
- **Fuel Type**: Petrol, Diesel, Hybrid, Electric
- **Transmission**: Manual or Automatic

### Data Validation

Built-in data validation ensures:

- **Price Validation**: Numeric price verification
- **Date Validation**: Proper date format checking
- **Required Fields**: Ensures essential data is present
- **Data Types**: Proper type conversion and validation

## 🆘 Troubleshooting

### Common Issues

1. **Connection Timeouts**:
   - Reduce concurrency setting
   - Increase timeout duration
   - Check internet connection stability

2. **No Data Retrieved**:
   - Verify Cars24.ae accessibility
   - Check if website structure has changed
   - Validate API endpoints

3. **Memory Issues**:
   - Reduce batch size
   - Implement data streaming
   - Monitor system resources

4. **Rate Limiting**:
   - Increase delays between requests
   - Reduce concurrent connections
   - Implement exponential backoff

### Debug Mode

Enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Performance Optimization

For better performance:

```python
# Optimize for speed
scraper = CarScraper(
    concurrency=150,  # Increase if system can handle
    timeout=60,       # Reduce for faster failures
    retry_attempts=2  # Reduce retry attempts
)
```

## 📊 Data Quality

The scraper ensures high data quality through:

- **Duplicate Detection**: Automatic removal of duplicate entries
- **Data Cleaning**: Standardization of formats and values
- **Validation Rules**: Comprehensive data validation
- **Error Logging**: Detailed error tracking and reporting

## 🔒 Security & Privacy

- **No Personal Data**: Only publicly available vehicle information
- **Respectful Scraping**: Adheres to robots.txt and rate limits
- **Secure Connections**: HTTPS-only communication
- **Data Protection**: Local data storage only

---

**Part of the Legend Scrapers collection - Professional automotive data extraction**