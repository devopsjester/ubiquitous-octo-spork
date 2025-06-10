# Weather CLI Application

[![CI/CD](https://github.com/${{ github.repository }}/actions/workflows/python-publish.yml/badge.svg)](https://github.com/${{ github.repository }}/actions/workflows/python-publish.yml)

A command-line interface application for getting current weather information and location data using free APIs.

## Features

- **Location Detection**: Find city and state information by ZIP code or current location
- **Weather Information**: Get current temperature and weather conditions
- **Free APIs**: Uses only free APIs that don't require registration or API keys
- **Simple Interface**: Easy-to-use command-line interface built with Click

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The application provides two main commands: `where-is` and `current`.

### Basic Usage

```bash
python weather.py --help
```

### Commands

#### `where-is` - Location Information

Get city and state information for a location.

**With ZIP code:**
```bash
python weather.py where-is --zipcode 10001
```
Output: `10001 is in New York, NY.`

**Current location** (based on IP address):
```bash
python weather.py where-is
```
Output: `Your current location is Seattle, WA.`

#### `current` - Weather Information

Get current temperature and weather conditions.

**With ZIP code:**
```bash
python weather.py current --zipcode 90210
```
Output: `It is currently 72ºF, and partly cloudy in Beverly Hills, CA.`

**Current location** (based on IP address):
```bash
python weather.py current
```
Output: `It is currently 65ºF, and light rain in Portland, OR.`

### Examples

```bash
# Get location info for ZIP code 02101
python weather.py where-is --zipcode 02101

# Get current weather for ZIP code 33101
python weather.py current --zipcode 33101

# Get your current location
python weather.py where-is

# Get current weather for your location
python weather.py current
```

## Testing

This application comes with automated tests to ensure reliability and correctness.

### Setting up Test Environment

1. **Install test dependencies**:
   ```bash
   python3 -m pip install -r dev-requirements.txt
   ```

### Running Tests

To run all tests:
```bash
pytest
```

To run tests with verbose output:
```bash
pytest -v
```

To run a specific test file:
```bash
pytest tests/test_cli.py
pytest tests/test_where_is.py
pytest tests/test_current.py
```

### Test Structure

The test suite is organized into three main files:

- `test_cli.py`: Tests for general CLI structure and command help messages
- `test_where_is.py`: Tests for the `where-is` command functionality
- `test_current.py`: Tests for the `current` command functionality

All external API calls are mocked in tests to ensure reliability and quick execution.

## APIs Used

This application uses the following free APIs:

1. **Open-Meteo** (https://open-meteo.com/) - Weather data
   - No API key required
   - Free for non-commercial use
2. **IP-API** (http://ip-api.com/) - IP geolocation
   - No API key required
   - Free tier available
3. **Zippopotam.us** (https://api.zippopotam.us/) - ZIP code lookup
   - No API key required
   - Free to use

2. **Zippopotam.us** (http://api.zippopotam.us/) - ZIP code to location mapping
   - No API key required
   - Free service

3. **IP-API** (http://ip-api.com/) - IP-based geolocation
   - No API key required
   - Free for non-commercial use (up to 1000 requests/month)

## Error Handling

The application includes basic error handling for:

- Invalid ZIP codes
- API request failures
- Network connectivity issues
- Unable to determine current location

## File Structure

```
├── weather.py          # Main CLI application
├── weather_api.py      # Weather service and API interactions
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

- **click** (>=8.1.0) - Command-line interface framework
- **requests** (>=2.31.0) - HTTP library for API requests

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## License

This project is open source and available under the MIT License.

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and delivery. The pipeline:

- Runs on every push to `main` and when new version tags are created
- Tests the package on multiple Python versions (3.9, 3.10, 3.11)
- Runs code quality checks (flake8 and black)
- Builds and packages the application
- Publishes releases to GitHub Packages when version tags are pushed

### Release Process

To create a new release:

1. Update the version in your package files
2. Create and push a new tag:
   ```bash
   git tag v1.0.0  # Use appropriate version number
   git push origin v1.0.0
   ```
3. The GitHub Actions workflow will automatically build and publish the package

### Installing from GitHub Packages

To install the package from GitHub Packages:

1. Authenticate with GitHub Packages
2. Add this to your `~/.pip/pip.conf`:
   ```
   [global]
   index-url=https://pypi.pkg.github.com/${{ github.repository_owner }}
   ```
3. Install the package:
   ```bash
   pip install weather-cli
   ```
