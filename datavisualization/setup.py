#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="telemetry",
    version="0.2",
    description="Data pipeline for Olin Electric Motorsports telemetry.",
    author="Richard Li",
    author_email="rli@olin.edu",
    packages=find_packages(),
    install_requires=["redis==3.5.3", "redistimeseries==1.4.3", "pyserial==3.4"],
    extras_require={"test": ["pytest==5.3.0"]},
)
