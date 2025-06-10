"""
Tests for the 'current' command of the Weather CLI application.

These tests verify the functionality of the current weather features.
"""

import pytest
from click.testing import CliRunner
from weather import weather
from weather_api import WeatherService


@pytest.fixture
def runner():
    """Fixture providing a Click CLI test runner."""
    return CliRunner()


def test_current_with_valid_zipcode(runner, mocker):
    """Test current command with a valid zipcode."""
    # Mock both the weather and location service methods
    mock_weather = mocker.patch.object(WeatherService, "get_weather_by_zipcode")
    mock_location = mocker.patch.object(WeatherService, "get_location_by_zipcode")

    mock_weather.return_value = (72, "sunny")
    mock_location.return_value = ("San Francisco", "CA")

    result = runner.invoke(weather, ["current", "--zipcode", "94105"])
    assert result.exit_code == 0
    assert "It is currently 72ºF, and sunny in San Francisco, CA" in result.output
    mock_weather.assert_called_once_with("94105")
    mock_location.assert_called_once_with("94105")


def test_current_without_zipcode(runner, mocker):
    """Test current command without zipcode (current location)."""
    # Mock both the weather and location service methods
    mock_weather = mocker.patch.object(WeatherService, "get_current_weather")
    mock_location = mocker.patch.object(WeatherService, "get_current_location")

    mock_weather.return_value = (65, "cloudy")
    mock_location.return_value = ("Seattle", "WA")

    result = runner.invoke(weather, ["current"])
    assert result.exit_code == 0
    assert "It is currently 65ºF, and cloudy in Seattle, WA" in result.output
    mock_weather.assert_called_once()
    mock_location.assert_called_once()


def test_current_with_invalid_zipcode(runner, mocker):
    """Test current command with an invalid zipcode."""
    # Mock both service methods to return None for invalid zipcode
    mock_weather = mocker.patch.object(WeatherService, "get_weather_by_zipcode")
    mock_location = mocker.patch.object(WeatherService, "get_location_by_zipcode")

    mock_weather.return_value = None
    mock_location.return_value = None

    result = runner.invoke(weather, ["current", "--zipcode", "00000"])
    assert result.exit_code == 0
    assert "Could not get weather information for zipcode 00000" in result.output
    mock_weather.assert_called_once_with("00000")
    mock_location.assert_called_once_with("00000")


def test_current_location_failure(runner, mocker):
    """Test current command when current location cannot be determined."""
    # Mock both service methods to simulate location failure
    mock_weather = mocker.patch.object(WeatherService, "get_current_weather")
    mock_location = mocker.patch.object(WeatherService, "get_current_location")

    mock_weather.return_value = None
    mock_location.return_value = None

    result = runner.invoke(weather, ["current"])
    assert result.exit_code == 0
    assert (
        "Could not get weather information for your current location" in result.output
    )
    mock_weather.assert_called_once()
    mock_location.assert_called_once()


def test_current_weather_api_error(runner, mocker):
    """Test current command when weather API throws an error."""
    # Mock the weather service to raise an exception
    mock_weather = mocker.patch.object(WeatherService, "get_weather_by_zipcode")
    mock_location = mocker.patch.object(WeatherService, "get_location_by_zipcode")

    mock_weather.side_effect = Exception("Weather API Error")
    mock_location.return_value = ("San Francisco", "CA")

    result = runner.invoke(weather, ["current", "--zipcode", "94105"])
    assert result.exit_code == 0  # CLI handles errors gracefully
    assert "Error: Weather API Error" in result.output
    mock_weather.assert_called_once_with("94105")


def test_current_location_api_error(runner, mocker):
    """Test current command when location API throws an error."""
    # Mock the location service to raise an exception
    mock_weather = mocker.patch.object(WeatherService, "get_weather_by_zipcode")
    mock_location = mocker.patch.object(WeatherService, "get_location_by_zipcode")

    mock_weather.return_value = (72, "sunny")
    mock_location.side_effect = Exception("Location API Error")

    result = runner.invoke(weather, ["current", "--zipcode", "94105"])
    assert result.exit_code == 0  # CLI handles errors gracefully
    assert "Error: Location API Error" in result.output
    mock_location.assert_called_once_with("94105")
