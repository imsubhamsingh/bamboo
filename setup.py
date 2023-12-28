#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bambo",
    version="0.1.0",
    author="Shubham Singh",
    author_email="geekysubham@gmail.com",
    description="A simple HTTP load testing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imsubhamsingh/bamboo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "argparse",
        'concurrent.futures; python_version=="2.7"',
        "requests",
        "prettytable",
    ],
    entry_points={"console_scripts": ["bambo = bambo.bamboo:main"]},
)
