"""
Weather CLI Application

A command-line interface for getting weather information and location data using free APIs.
"""

from setuptools import setup, find_packages

# Read requirements
with open("requirements.txt") as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith(("#", "//"))
    ]

# Filter out development/build dependencies
main_requirements = [
    req
    for req in requirements
    if not any(
        dep in req.lower()
        for dep in ["pytest", "flake8", "black", "setuptools", "wheel", "twine"]
    )
]

setup(
    name="weather-cli",
    version="1.0.0",
    description="A CLI tool for getting weather information using free APIs",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    author="Assaf Stone",
    author_email="devopsjester@github.com",
    url="https://github.com/devopsjester/ubiquitous-octo-spork",
    packages=find_packages(exclude=["tests*"]),
    py_modules=["weather", "weather_api"],
    install_requires=main_requirements,
    entry_points={
        "console_scripts": [
            "weather=weather:weather",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
)
