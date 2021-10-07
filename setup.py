# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import sys


if sys.version_info[0] != 2:
    # Prevent creating or installing a distribution with Python 3.
    raise ValueError("archetypes.multilingual is based on Archetypes, which is Python 2 only.")

version = '3.0.9'

setup(
    name='archetypes.multilingual',
    version=version,
    description='Multilingual support for archetypes.',
    long_description=u'\n'.join([
        open('README.rst').read(),
        open('CHANGES.rst').read(),
    ]),
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 6 - Mature',
        'Framework :: Plone',
        'Framework :: Plone :: Addon',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ],
    keywords='archetypes multilingual i18n translation',
    author='awello',
    author_email='awello@gmail.com',
    url='https://github.com/plone/archetypes.multilingual',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['archetypes'],
    include_package_data=True,
    zip_safe=False,
    python_requires='==2.7.*',
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
            'plone.app.contenttypes[archetypes]',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
