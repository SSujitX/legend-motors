# Legend Scrapers

A comprehensive collection of high-performance web scrapers for automotive platforms in the UAE and international markets. This project provides asynchronous scrapers for multiple car trading websites with concurrent processing capabilities.

## 🚗 Supported Platforms

- **Kavak** - International used car marketplace
- **Cars24** - Online car buying and selling platform
- **AutoMall** - UAE automotive marketplace
- **Dubizzle** - UAE's leading classifieds platform
- **NxtCarsUAE** - UAE car trading platform

## ✨ Features

- **Asynchronous Processing**: High-performance async/await implementation
- **Concurrent Execution**: Multiple scrapers running in parallel using multiprocessing
- **Configurable Concurrency**: Adjustable API and detail page concurrency limits
- **Data Export**: Automatic CSV export for all scraped data
- **Rich Console Output**: Beautiful terminal output with progress tracking
- **Modern Python**: Built with Python 3.13+ and modern dependencies

## 📋 Prerequisites

### 1. Install Python 3.13+

Download and install Python 3.13 or higher:

- Visit [python.org](https://www.python.org/downloads/)
- Download the latest Python version for your operating system
- During installation, make sure to check "Add Python to PATH"
- Verify installation:
  ```powershell
  python --version
  ```

### 2. Install UV Package Manager

UV is a fast Python package installer and resolver:

```powershell
pip install uv
```

## 🚀 Quick Start

### 1. Clone and Setup

```powershell
# Navigate to project directory
cd "k:\Python Projects\Client Individual Projects\Baz Legend Projects\Legend Scrapers"

# Install dependencies
uv sync
```

### 2. Run All Scrapers (Parallel Execution)

Execute all scrapers simultaneously using multiprocessing:

```powershell
uv run app.py
```

### 3. Run Individual Scrapers

#### Kavak Scraper
```powershell
uv run kavak_scraper/kavak_scraper.py
```

#### Cars24 Scraper
```powershell
uv run cars24_scraper/cars24_scraper.py
```

#### AutoMall Scraper
```powershell
uv run automall_scraper/automall_scraper.py
```

#### Dubizzle Scraper
```powershell
uv run dubizzle_scraper/dubizzle_scraper.py
```

#### NxtCarsUAE Scraper
```powershell
uv run nxtcarsuae_scraper/nxtcarsuae_scraper.py
```

## 📁 Project Structure

```
Legend Scrapers/
├── app.py                      # Main application - runs all scrapers in parallel
├── pyproject.toml             # Project configuration and dependencies
├── requirements.txt           # Legacy requirements file
├── uv.lock                   # Dependency lock file
├── .gitignore                # Git ignore patterns
├── automall_scraper/         # AutoMall scraper module
│   ├── automall_scraper.py   # Main scraper implementation
│   ├── auto.py              # Additional utilities
│   └── requirements.txt     # Module-specific dependencies
├── cars24_scraper/          # Cars24 scraper module
│   ├── cars24_scraper.py    # Main scraper implementation
│   └── requirements.txt     # Module-specific dependencies
├── dubizzle_scraper/        # Dubizzle scraper module
│   ├── dubizzle_scraper.py  # Main scraper implementation
│   ├── pyproject.toml       # Module configuration
│   └── requirements.txt     # Module-specific dependencies
├── kavak_scraper/           # Kavak scraper module
│   ├── kavak_scraper.py     # Main scraper implementation
│   ├── api_test.py          # API testing utilities
│   ├── single_test.py       # Single item testing
│   └── requirements.txt     # Module-specific dependencies
└── nxtcarsuae_scraper/      # NxtCarsUAE scraper module
    ├── nxtcarsuae_scraper.py # Main scraper implementation
    ├── test.py              # Testing utilities
    ├── pyproject.toml       # Module configuration
    └── requirements.txt     # Module-specific dependencies
```

## 🔧 Configuration

### Concurrency Settings

Each scraper supports configurable concurrency levels:

- **Kavak**: API concurrency (25), Detail concurrency (200)
- **Cars24**: Configurable max pages (default: 50)
- **AutoMall**: Optimized for UAE market
- **Dubizzle**: UAE-specific implementation
- **NxtCarsUAE**: Local UAE platform optimization

### Environment Variables

Create a `.env` file for configuration (optional):

```env
# Concurrency settings
KAVAK_API_CONCURRENCY=25
KAVAK_DETAIL_CONCURRENCY=200
CARS24_MAX_PAGES=50

# Output settings
OUTPUT_FORMAT=csv
OUTPUT_DIRECTORY=./scraped_data
```

## 📊 Output

All scrapers generate CSV files with comprehensive car data including:

- Vehicle specifications (make, model, year, mileage)
- Pricing information
- Location data
- Seller information
- Vehicle condition details
- Images and media links
- Platform-specific metadata

Output files are saved in the project directory with timestamps.

## 🛠️ Development

### Adding Dependencies

```powershell
# Add a new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update dependencies
uv sync
```

### Code Style

The project follows modern Python practices:

- Type hints where applicable
- Async/await for I/O operations
- Context managers for resource management
- Rich console output for user experience

### Testing

```powershell
# Run individual scraper tests
uv run kavak_scraper/single_test.py
uv run kavak_scraper/api_test.py
uv run nxtcarsuae_scraper/test.py
```

## 📦 Dependencies

### Core Dependencies

- **curl-cffi** (≥0.11.1) - Fast HTTP client with curl backend
- **pandas** (≥2.2.3) - Data manipulation and analysis
- **rich** (≥14.0.0) - Rich text and beautiful formatting
- **selectolax** (≥0.3.29) - Fast HTML parsing

### Development Tools

- **UV** - Fast Python package installer and resolver
- **Python 3.13+** - Latest Python features and performance

## 🚨 Important Notes

- **Rate Limiting**: Scrapers implement respectful rate limiting
- **Legal Compliance**: Ensure compliance with website terms of service
- **Data Usage**: Scraped data is for personal/research use only
- **Performance**: Concurrent execution may impact system resources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please respect the terms of service of the scraped websites.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Run `uv sync` to ensure all dependencies are installed
2. **Permission Errors**: Ensure Python and UV are properly installed with PATH access
3. **Network Issues**: Check internet connection and firewall settings
4. **Memory Issues**: Reduce concurrency levels in scraper configurations

### Getting Help

- Check individual scraper modules for specific documentation
- Review error logs in the console output
- Ensure all prerequisites are properly installed

---

**Built with ❤️ for the automotive data community**
