# -*- coding: utf-8 -*-
"""Installer for the eea.restapi package."""

from os.path import join
from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open(join("docs", "HISTORY.txt")).read(),
    ]
)

NAME = "eea.restapi"
PATH = ["src"] + NAME.split(".") + ["version.txt"]
VERSION = open(join(*PATH)).read().strip()

setup(
    name=NAME,
    version=VERSION,
    description="plone.restapi for EEA websites",
    long_description_content_type="text/x-rst",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Tiberiu Ichim",
    author_email="tiberiu.ichim@eaudeweb.ro",
    url="https://github.com/collective/eea.restapi",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/eea.restapi",
        "Source": "https://github.com/collective/eea.restapi",
        "Tracker": "https://github.com/collective/eea.restapi/issues",
        # 'Documentation': 'https://eea.restapi.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["eea"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "collective.folderishtypes",
        "plone.api>=1.8.4",
        "plone.restapi",
        "plone.app.dexterity",
        "requests",
        "xlsxwriter",
        "moz-sql-parser",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = eea.restapi.locales.update:update_locale
    """,
)
