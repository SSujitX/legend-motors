# AutoMall Scraper

A high-performance asynchronous scraper for AutoMall.ae, the UAE's leading automotive marketplace. This scraper extracts comprehensive vehicle data including specifications, pricing, and availability information.

## 🚗 About AutoMall

AutoMall.ae is a prominent automotive marketplace in the UAE that specializes in used automobiles. The platform offers a wide range of vehicles with detailed specifications and competitive pricing.

## ✨ Features

- **Asynchronous Processing**: Built with async/await for optimal performance
- **Authentication Handling**: Automatic AUTH_TOKEN extraction and management
- **Configurable Concurrency**: Adjustable concurrent request limits (default: 100)
- **Comprehensive Data Extraction**: Vehicle specs, pricing, location, and status information
- **CSV Export**: Automatic data export with timestamp
- **Error Handling**: Robust error handling and retry mechanisms

## 📊 Data Fields Extracted

### Vehicle Information
- **ID**: Unique vehicle identifier
- **Price**: Vehicle price in AED
- **Discount**: Available discount amount
- **EMI**: Equated Monthly Installment details
- **Model Year**: Manufacturing year
- **Make**: Vehicle manufacturer
- **Model**: Vehicle model
- **Engine Capacity**: Engine size specification
- **Odometer**: Mileage reading
- **Vehicle Status**: Availability status (AV, CT)
- **Location**: Vehicle location in UAE
- **Model Grade**: Trim level
- **Exterior Colors**: Available color options
- **Body Type**: Vehicle body style
- **Hot Offer Status**: Special promotion indicator

## 🚀 Usage

### Standalone Execution

```powershell
# Navigate to the automall_scraper directory
cd automall_scraper

# Run the scraper
uv run automall_scraper.py
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
from automall_scraper import Automall

async def main():
    # Custom concurrency setting
    async with Automall(concurrency=50) as scraper:
        await scraper.run_scraper()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 Configuration

### Concurrency Settings

- **Default Concurrency**: 100 concurrent requests
- **Timeout**: 120 seconds per request
- **Impersonation**: Chrome browser simulation

### API Endpoints

- **Main URL**: `https://www.automall.ae/en/used-cars-shop/`
- **API Endpoint**: `https://www.automall.ae/bff/v2/vehicles`
- **Authentication**: Bearer token from AUTH_TOKEN cookie

## 📁 Files

- **`automall_scraper.py`**: Main scraper implementation
- **`auto.py`**: Additional utilities and helper functions
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

1. **Authentication**: Extracts AUTH_TOKEN from AutoMall.ae cookies
2. **API Discovery**: Uses the BFF (Backend for Frontend) API endpoint
3. **Pagination**: Automatically handles paginated results
4. **Data Processing**: Extracts and normalizes vehicle information
5. **Export**: Saves data to timestamped CSV file

## 📈 Performance

- **Concurrent Requests**: Up to 100 simultaneous API calls
- **Rate Limiting**: Respectful request timing
- **Memory Efficient**: Streaming data processing
- **Error Recovery**: Automatic retry on failed requests

## 🚨 Important Notes

- **Authentication Required**: Scraper automatically handles AUTH_TOKEN extraction
- **Rate Limiting**: Built-in respectful rate limiting
- **Data Accuracy**: Real-time data from AutoMall.ae API
- **Legal Compliance**: Ensure compliance with AutoMall.ae terms of service

## 🛠️ Development

### Adding New Fields

To extract additional vehicle fields, modify the query string in the `__init__` method:

```python
self.query = (
    "q=type=auto_used_automobiles|price%3E0|attributes.auto_sap_vehicle_status.values.EN=AV,CT"
    "&fields=id|price|discount|your_new_field"  # Add new fields here
    "&sort=price=1"
)
```

### Custom Filters

Modify the query parameters to add filters:

```python
# Example: Filter by price range
query_with_filter = self.query + "|price%3E50000|price%3C200000"
```

## 📄 Output Format

The scraper generates CSV files with the following naming convention:
```
automall_YYYY-MM-DD.csv
```

Example output structure:
```csv
id,price,discount,modelYear,make,model,engineCapacity,odometer,vehicleStatus,vehicleLocation
12345,85000,5000,2020,Toyota,Camry,2.5L,45000,AV,Dubai
```

## 🆘 Troubleshooting

### Common Issues

1. **Authentication Errors**: 
   - Ensure internet connection is stable
   - Check if AutoMall.ae is accessible

2. **No Data Retrieved**:
   - Verify API endpoints are still valid
   - Check if website structure has changed

3. **Performance Issues**:
   - Reduce concurrency setting
   - Check system resources

### Debug Mode

Enable detailed logging by modifying the scraper:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

**Part of the Legend Scrapers collection - Built for automotive data professionals**