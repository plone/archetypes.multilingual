# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '3.0.3'

setup(
    name='archetypes.multilingual',
    version=version,
    description='Multilingual support for archetypes.',
    long_description=u'\n'.join([
        open('README.rst').read(),
        open('CHANGES.rst').read(),
    ]),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='archetypes multilingual i18n translation',
    author='awello',
    author_email='awello@gmail.com',
    url='https://github.com/plone/archetypes.multilingual',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['archetypes'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.ATContentTypes',
        'plone.app.multilingual',
        'collective.monkeypatcher',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.multilingual[test]',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
