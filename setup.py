from io import open
import json
import os
import pathlib
import sys
from shutil import rmtree

from setuptools import find_packages, setup

ROOT_PATH = pathlib.Path(__file__).parent
PROJECT_PATH = ROOT_PATH / "discorgeous"
VERSION_PATH = PROJECT_PATH / "__version__.py"
PIPFILE = ROOT_PATH / "Pipfile.lock"
README_FILE = ROOT_PATH / "README.md"

# Package meta-data.
NAME = "Discorgeous"
DESCRIPTION = (
    "A discord bot that sends google text to speech voice messages to discord voice channels."
)
URL = "https://github.com/dgnsrekt/Discorgeous"
EMAIL = "dgnsrekt@pm.me"
AUTHOR = "Degennosaurus REKT"
REQUIRES_PYTHON = ">=3.6.0"

# Parses version
about = {}
with open(VERSION_PATH) as version_file:
    exec(version_file.read(), about)

# Parses pipfile.lock to get requirements
with open(PIPFILE, encoding="utf-8") as pipfile_lock:
    pipfile_json = json.loads(pipfile_lock.read())
    require = pipfile_json["default"]
    develop = pipfile_json["develop"]


REQUIRES = []
for package, v in require.items():
    REQUIRES.append(package + v["version"])


EXTRAS_REQUIRES = []
for package, v in develop.items():
    EXTRAS_REQUIRES.append(package + v["version"])

with open(README_FILE, encoding="utf-8") as readme_file:
    LONG_DESCRIPTION = "\n" + readme_file.read()

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    entry_points={"console_scripts": ["discorgeous=discorgeous:core"]},
    install_requires=REQUIRES,
    extras_require={"dev": EXTRAS_REQUIRES},
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
