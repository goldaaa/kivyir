#!/usr/bin/env python
# coding=utf-8

from setuptools import setup
import os
import io

with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kivyir",
    description="Improving the display of Persian text for Persian speakers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.0.0',
    platforms="ALL",
    license="MIT",
    packages=['kivyir'],
    install_requires=['configparser; python_version <"3"', 'future'],
    extras_require={
        'with-fonttools': ['fonttools>=4.0; python_version >="3"',
                           'fonttools>=3.0,<4.0; python_version <"3"']
    },
    author="navid nasiri",
    author_email="goldaaa.program@gmail.com",
    maintainer="navid nasiri",
    maintainer_email="goldaaa.program@gmail.com",
    package_dir={'kivyir': 'kivyir'},
    test_suite='kivyir.test',
    include_package_data=True,
    keywords="kivy persian farsi iran",
    url="https://github.com/goldaaa/kivyir",
    download_url="https://github.com/goldaaa/kivyir/tarball/master",
    classifiers=[
        "Natural Language :: Persian",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
