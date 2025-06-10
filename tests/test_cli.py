"""
Tests for the Weather CLI application command structure.

These tests verify the general CLI functionality without testing specific commands.
"""

import pytest
from click.testing import CliRunner
from weather import weather


@pytest.fixture
def runner():
    """Fixture providing a Click CLI test runner."""
    return CliRunner()


def test_cli_exists(runner):
    """Test that the CLI exists and can be invoked."""
    result = runner.invoke(weather)
    # Click returns exit code 2 for command groups with no subcommand
    assert result.exit_code == 2
    assert "Usage:" in result.output


def test_cli_help(runner):
    """Test that the help option works for the main command."""
    result = runner.invoke(weather, ["--help"])
    assert result.exit_code == 0
    assert "where-is" in result.output
    assert "current" in result.output


def test_where_is_help(runner):
    """Test that the help option works for the where-is command."""
    result = runner.invoke(weather, ["where-is", "--help"])
    assert result.exit_code == 0
    assert "--zipcode" in result.output


def test_current_help(runner):
    """Test that the help option works for the current command."""
    result = runner.invoke(weather, ["current", "--help"])
    assert result.exit_code == 0
    assert "--zipcode" in result.output


def test_weather_group_command():
    """Test that the main command group exists and returns help information."""
    runner = CliRunner()
    result = runner.invoke(weather, ["--help"])

    assert result.exit_code == 0
    assert "Weather CLI application" in result.output
    assert "where-is" in result.output
    assert "current" in result.output


def test_weather_group_command_no_args():
    """Test that invoking the command with no arguments shows help text."""
    runner = CliRunner()
    result = runner.invoke(weather)

    # Click returns exit code 2 for command groups with no subcommand
    assert result.exit_code == 2
    assert "Usage:" in result.output
    assert "Usage:" in result.output
    assert "Commands:" in result.output


def test_invalid_command():
    """Test that an invalid command returns an error message."""
    runner = CliRunner()
    result = runner.invoke(weather, ["invalid-command"])

    assert result.exit_code != 0
    assert "Error: No such command" in result.output


def test_nested_commands_structure():
    """Test that all expected sub-commands exist."""
    expected_commands = ["where-is", "current"]

    runner = CliRunner()
    result = runner.invoke(weather, ["--help"])

    for cmd in expected_commands:
        assert cmd in result.output, f"Command '{cmd}' not found in CLI output"
