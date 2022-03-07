#!/usr/bin/env python3

from setuptools import find_packages, setup


setup(
    name="kpimon",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["onos-ric-sdk-python>=0.2.3"],
)
