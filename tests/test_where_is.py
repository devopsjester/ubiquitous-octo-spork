"""
Tests for the 'where-is' command of the Weather CLI application.

These tests verify the functionality of the location lookup features.
"""

import pytest
from click.testing import CliRunner
from weather import weather
from weather_api import WeatherService


@pytest.fixture
def runner():
    """Fixture providing a Click CLI test runner."""
    return CliRunner()


def test_where_is_with_valid_zipcode(runner, mocker):
    """Test where-is command with a valid zipcode."""
    # Mock the WeatherService.get_location_by_zipcode method
    mock_location = mocker.patch.object(WeatherService, "get_location_by_zipcode")
    mock_location.return_value = ("San Francisco", "CA")

    result = runner.invoke(weather, ["where-is", "--zipcode", "94105"])
    assert result.exit_code == 0
    assert "94105 is in San Francisco, CA" in result.output
    mock_location.assert_called_once_with("94105")


def test_where_is_current_location(runner, mocker):
    """Test where-is command without zipcode (current location)."""
    # Mock the WeatherService.get_current_location method
    mock_location = mocker.patch.object(WeatherService, "get_current_location")
    mock_location.return_value = ("Seattle", "WA")

    result = runner.invoke(weather, ["where-is"])
    assert result.exit_code == 0
    assert "Your current location is Seattle, WA" in result.output
    mock_location.assert_called_once()


def test_where_is_with_invalid_zipcode(runner, mocker):
    """Test where-is command with an invalid zipcode."""
    # Mock the WeatherService.get_location_by_zipcode method
    mock_location = mocker.patch.object(WeatherService, "get_location_by_zipcode")
    mock_location.return_value = None

    result = runner.invoke(weather, ["where-is", "--zipcode", "00000"])
    assert result.exit_code == 0  # CLI returns 0 even for invalid zipcodes
    assert "Could not find location information for zipcode 00000" in result.output
    mock_location.assert_called_once_with("00000")


def test_where_is_current_location_failure(runner, mocker):
    """Test where-is command when current location cannot be determined."""
    # Mock the WeatherService.get_current_location method
    mock_location = mocker.patch.object(WeatherService, "get_current_location")
    mock_location.return_value = None

    result = runner.invoke(weather, ["where-is"])
    assert result.exit_code == 0  # CLI returns 0 even for location failures
    assert "Could not determine your current location" in result.output
    mock_location.assert_called_once()


def test_where_is_api_error(runner, mocker):
    """Test where-is command when API throws an error."""
    # Mock the WeatherService.get_location_by_zipcode method to raise an exception
    mock_location = mocker.patch.object(WeatherService, "get_location_by_zipcode")
    mock_location.side_effect = Exception("API Error")

    result = runner.invoke(weather, ["where-is", "--zipcode", "94105"])
    assert result.exit_code == 0  # CLI handles errors gracefully
    assert "Error: API Error" in result.output
    mock_location.assert_called_once_with("94105")
