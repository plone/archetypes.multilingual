from setuptools import setup, find_packages
import os

version = '1.0b3'

setup(name='archetypes.multilingual',
      version=version,
      description="Multilingual support for archetypes",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
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
          'plone.multilingual',
          'collective.monkeypatcher',
          'Products.PloneLanguageTool'
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing', 'archetypes.testcase']
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
