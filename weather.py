#!/usr/bin/env python3
"""
Weather CLI Application

A command-line interface for getting weather information and location data.
"""

import click
from weather_api import WeatherService


@click.group()
def weather():
    """Weather CLI application for getting current weather and location information."""
    pass


@weather.command()
@click.option("--zipcode", help="Zip code to get location information for")
def where_is(zipcode):
    """Display the city and state for a given location."""
    weather_service = WeatherService()

    try:
        if zipcode:
            location_info = weather_service.get_location_by_zipcode(zipcode)
            if location_info:
                city, state = location_info
                click.echo(f"{zipcode} is in {city}, {state}.")
            else:
                click.echo(
                    f"Could not find location information for zipcode {zipcode}."
                )
        else:
            location_info = weather_service.get_current_location()
            if location_info:
                city, state = location_info
                click.echo(f"Your current location is {city}, {state}.")
            else:
                click.echo("Could not determine your current location.")
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@weather.command()
@click.option("--zipcode", help="Zip code to get weather information for")
def current(zipcode):
    """Display the current temperature and weather conditions for a given location."""
    weather_service = WeatherService()

    try:
        if zipcode:
            weather_info = weather_service.get_weather_by_zipcode(zipcode)
            location_info = weather_service.get_location_by_zipcode(zipcode)
        else:
            weather_info = weather_service.get_current_weather()
            location_info = weather_service.get_current_location()

        if weather_info and location_info:
            temperature, condition = weather_info
            city, state = location_info
            click.echo(
                f"It is currently {temperature}ºF, and {condition} in {city}, {state}."
            )
        else:
            if zipcode:
                click.echo(f"Could not get weather information for zipcode {zipcode}.")
            else:
                click.echo(
                    "Could not get weather information for your current location."
                )
    except Exception as e:
        click.echo(f"Error: {str(e)}")


if __name__ == "__main__":
    weather()
