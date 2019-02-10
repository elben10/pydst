#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "pandas==0.23.4",
    "cerberus==1.2",
    "requests==2.21.0",
]

setup_requirements = [
    "pip==10.0.1",
    "bumpversion==0.5.3",
    "wheel==0.31.1",
    "watchdog==0.8.3",
    "flake8==3.5.0",
    "tox==3.0.0",
    "Sphinx==1.7.5",
    "twine==1.11.0",
    "pytest==3.6.2",
    "pytest-runner==4.2",
    "pytest-cov==2.5.1",
    "codecov==2.0.15",
    "pluggy==0.6.0",
]

setup(
    author="Jakob Jul Elben, Kristian Urup Larsen",
    author_email='elbenjakobjul@gmail.com, kristianuruplarsen@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Provides a simple API for retrieving data from Statistics Denmark",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pydst',
    name='pydst',
    packages=find_packages(include=['pydst']),
    setup_requires=setup_requirements,
    test_suite='tests',
    url='https://github.com/elben10/pydst',
    version='0.1.0.9000',
    zip_safe=False,
)
