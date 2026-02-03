#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# خواندن README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# خواندن requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

# خواندن ورژن از فایل
version = "2.0.0"

setup(
    name="rpt-swi",
    version=version,
    author="Raptor-1996",
    author_email="EbiRom1996@gmail.com",
    description="RPT See Who Is In - Professional Network Security Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raptor-1996/rpt-swi",
    project_urls={
        "Bug Tracker": "https://github.com/Raptor-1996/rpt-swi/issues",
        "Documentation": "https://github.com/Raptor-1996/rpt-swi/wiki",
        "Source Code": "https://github.com/Raptor-1996/rpt-swi",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rpt-swi=src.main:main",
            "rptswi=src.main:main",
        ],
    },
    package_data={
        "": ["*.yaml", "*.json", "*.db"],
    },
    data_files=[
        ("share/doc/rpt-swi", ["README.md", "LICENSE", "INSTALL.md", "QUICKSTART.md"]),
        ("share/rpt-swi/config", ["config/settings.example.yaml"]),
        ("share/man/man1", ["docs/rpt-swi.1"]),
    ],
    scripts=[
        "install.sh",
        "uninstall.sh",
        "quickstart.sh",
        "test_installation.sh",
    ],
    keywords=[
        "network",
        "security",
        "monitoring",
        "scanner",
        "firewall",
        "administration",
        "python",
        "linux",
    ],
    license="MIT",
    platforms=["Linux"],
)
