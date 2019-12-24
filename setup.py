# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = "2.1.1"

setup(
    name="archetypes.multilingual",
    version=version,
    description="Multilingual support for archetypes.",
    long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
    # Get more strings from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 6 - Mature",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 4.3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="archetypes multilingual i18n translation",
    author="awello",
    author_email="awello@gmail.com",
    url="https://github.com/plone/archetypes.multilingual",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["archetypes"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "Products.ATContentTypes",
        "plone.app.multilingual >= 2.0.4, < 3.0",
        "collective.monkeypatcher",
        "plone.api",
    ],
    extras_require={"test": ["plone.app.testing", "plone.app.multilingual[test]",]},
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
