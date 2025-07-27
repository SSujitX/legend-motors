# Kavak Scraper

A high-performance asynchronous scraper for Kavak.com, Latin America's leading used car marketplace with a growing presence in the UAE. This scraper efficiently extracts comprehensive vehicle data, pricing information, and detailed specifications from Kavak's UAE platform.

## 🚗 About Kavak

Kavak is a revolutionary used car marketplace that has transformed the automotive industry across Latin America and is expanding into the Middle East. The platform offers a curated selection of quality used vehicles with transparent pricing, comprehensive inspections, and digital-first customer experience.

## ✨ Features

- **Asynchronous Architecture**: High-performance async/await implementation
- **Smart Pagination**: Automatic handling of paginated vehicle listings
- **Configurable Concurrency**: Adjustable concurrent request limits (default: 100)
- **Comprehensive Data Extraction**: Vehicle specifications, pricing, condition reports
- **CSV Export**: Timestamped data export with comprehensive formatting
- **Robust Error Handling**: Built-in retry mechanisms and error recovery
- **Browser Impersonation**: Chrome simulation for reliable platform access

## 📊 Data Fields Extracted

### Vehicle Information
- **ID**: Unique vehicle identifier
- **Title**: Complete vehicle listing title
- **Price**: Current market price in AED
- **Original Price**: Initial listing price
- **Discount**: Available discount amount
- **Model Year**: Manufacturing year
- **Make**: Vehicle manufacturer (Toyota, BMW, Mercedes, etc.)
- **Model**: Specific vehicle model
- **Variant**: Trim level and engine specifications
- **Mileage**: Odometer reading in kilometers
- **Fuel Type**: Petrol, Diesel, Hybrid, Electric
- **Transmission**: Manual or Automatic
- **Body Type**: Sedan, SUV, Hatchback, Coupe, etc.
- **Engine**: Engine specifications and capacity
- **Color**: Exterior color
- **Interior Color**: Interior color scheme
- **Doors**: Number of doors
- **Seating**: Seating capacity

### Condition & Quality
- **Condition Score**: Kavak's proprietary condition rating
- **Inspection Report**: Comprehensive vehicle inspection details
- **Accident History**: Accident-free certification
- **Service History**: Maintenance records availability
- **Warranty**: Kavak warranty information
- **Certification**: Quality certification status

### Location & Availability
- **Location**: Vehicle location in UAE
- **Showroom**: Specific Kavak showroom location
- **Availability**: Current availability status
- **Reserved Status**: Reservation information

### Seller Information
- **Seller Type**: Always Kavak (certified dealer)
- **Listing Date**: When the vehicle was listed
- **Last Updated**: Most recent update timestamp
- **View Count**: Number of times viewed

## 🚀 Usage

### Standalone Execution

```powershell
# Navigate to the kavak_scraper directory
cd kavak_scraper

# Run the scraper
uv run kavak_scraper.py
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
from kavak_scraper import KavakScraper

async def main():
    # Custom configuration with specific parameters
    async with KavakScraper(concurrency=75, timeout=90) as scraper:
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

- **Base URL**: `https://www.kavak.com/ae/`
- **Search API**: `/api/search/vehicles`
- **Vehicle Details**: `/api/vehicles/{vehicle_id}`
- **Filters**: Advanced filtering capabilities

## 📁 Files

- **`kavak_scraper.py`**: Main scraper implementation
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

1. **Initial Request**: Accesses Kavak UAE homepage
2. **Vehicle Discovery**: Identifies all available vehicle listings
3. **Parallel Processing**: Concurrently fetches detailed vehicle information
4. **Data Extraction**: Parses comprehensive vehicle data from API responses
5. **Quality Assessment**: Extracts Kavak's quality scores and certifications
6. **Data Normalization**: Standardizes and validates extracted data
7. **CSV Export**: Saves comprehensive data to timestamped file

## 📈 Performance Metrics

- **Concurrent Requests**: Up to 100 simultaneous API calls
- **Data Processing**: Efficient memory usage with streaming
- **Error Recovery**: Automatic retry on network failures
- **Rate Limiting**: Built-in respectful request timing
- **Data Quality**: High accuracy due to Kavak's standardized data

## 🚨 Important Notes

- **Legal Compliance**: Ensure adherence to Kavak.com terms of service
- **Rate Limiting**: Built-in respectful scraping practices
- **Data Accuracy**: Real-time data from Kavak's certified inventory
- **Quality Assurance**: All vehicles are Kavak-certified with quality scores

## 🛠️ Development

### Adding Custom Filters

Modify search parameters to add specific filters:

```python
# Example: Filter by price range and specific criteria
search_filters = {
    "price_min": 40000,
    "price_max": 200000,
    "year_min": 2018,
    "make": "toyota",
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
        "financing_options": vehicle_json.get("financing", {}),
        "trade_in_value": vehicle_json.get("trade_in_estimate", ""),
        "delivery_options": vehicle_json.get("delivery", [])
    }
    return details
```

### Custom Output Formats

Support additional export formats:

```python
# JSON export with nested structure
import json
with open(f"kavak_{date}.json", "w") as f:
    json.dump(vehicles_data, f, indent=2, ensure_ascii=False)

# Excel export with multiple sheets
with pd.ExcelWriter(f"kavak_{date}.xlsx") as writer:
    df.to_excel(writer, sheet_name="Vehicles", index=False)
    condition_df.to_excel(writer, sheet_name="Condition_Reports", index=False)
    pricing_df.to_excel(writer, sheet_name="Pricing_Analysis", index=False)
```

## 📄 Output Format

The scraper generates CSV files with the following naming convention:
```
kavak_YYYY-MM-DD.csv
```

Example output structure:
```csv
id,title,price,originalPrice,discount,modelYear,make,model,variant,mileage,conditionScore,location
12345,"2020 Toyota Camry 2.5L SE",85000,90000,5000,2020,Toyota,Camry,2.5L SE,45000,8.5,Dubai
```

## 🔍 Advanced Features

### Quality Assessment

Kavak's unique quality features:

- **200-Point Inspection**: Comprehensive vehicle inspection
- **Condition Scoring**: Numerical quality rating (1-10)
- **Certification Process**: Kavak quality certification
- **Warranty Coverage**: Comprehensive warranty information
- **Accident History**: Detailed accident reporting
- **Service Records**: Complete maintenance history

### Search Filtering

The scraper supports advanced filtering:

- **Price Range**: Minimum and maximum price filters
- **Year Range**: Model year filtering
- **Mileage Range**: Kilometer-based filtering
- **Make/Model**: Brand and model specific searches
- **Fuel Type**: Petrol, Diesel, Hybrid, Electric
- **Transmission**: Manual or Automatic
- **Body Type**: Vehicle category filtering
- **Condition Score**: Quality-based filtering
- **Location**: Showroom-specific searches

### Data Validation

Built-in validation ensures data quality:

- **Price Validation**: Numeric price verification
- **Date Validation**: Proper timestamp formatting
- **Required Fields**: Essential data presence checking
- **Quality Scores**: Condition score validation (1-10)
- **Duplicate Detection**: Removal of duplicate listings

## 🆘 Troubleshooting

### Common Issues

1. **Connection Timeouts**:
   - Reduce concurrency setting
   - Increase timeout duration
   - Check network stability

2. **No Data Retrieved**:
   - Verify Kavak.com accessibility
   - Check if API endpoints have changed
   - Validate search parameters

3. **Rate Limiting Errors**:
   - Reduce request frequency
   - Implement exponential backoff
   - Add random delays between requests

4. **Quality Score Issues**:
   - Verify condition score extraction logic
   - Check for API response format changes
   - Validate scoring methodology

### Debug Mode

Enable comprehensive logging:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kavak_scraper.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Optimization

Optimize for different scenarios:

```python
# High-speed configuration
scraper = KavakScraper(
    concurrency=150,  # Increase for powerful systems
    timeout=60,       # Reduce for faster failures
    retry_attempts=2  # Minimize retries for speed
)

# Quality-focused configuration
scraper = KavakScraper(
    concurrency=50,   # Reduce for stability
    timeout=180,      # Increase for reliability
    retry_attempts=5  # More retries for completeness
)
```

## 📊 Data Quality Assurance

Kavak's standardized approach ensures high data quality:

- **Standardized Listings**: Consistent data format across all vehicles
- **Quality Certification**: All vehicles undergo 200-point inspection
- **Verified Information**: Accurate mileage, condition, and history
- **Professional Photography**: High-quality vehicle images
- **Transparent Pricing**: Clear pricing with no hidden fees

## 🔒 Security & Privacy

- **Public Data Only**: Extracts only publicly available information
- **Respectful Scraping**: Adheres to robots.txt guidelines
- **Secure Communication**: HTTPS-only connections
- **Local Storage**: All data stored locally
- **No Personal Data**: Avoids collecting personal information

## 📈 Market Insights

The scraper provides valuable automotive market data:

- **Price Trends**: Track Kavak pricing patterns
- **Quality Distribution**: Analyze condition score distributions
- **Popular Models**: Identify most available vehicle types
- **Market Positioning**: Compare Kavak vs. market pricing
- **Inventory Turnover**: Monitor listing frequency and updates

## 🌟 Kavak Advantages

Unique benefits of scraping Kavak data:

- **Quality Assurance**: All vehicles are certified and inspected
- **Standardized Data**: Consistent information format
- **Transparent Pricing**: Clear, upfront pricing
- **Warranty Information**: Comprehensive warranty details
- **Professional Service**: Dealer-level service quality
- **Digital Experience**: Modern, user-friendly platform

---

**Part of the Legend Scrapers collection - Premium automotive marketplace data extraction**