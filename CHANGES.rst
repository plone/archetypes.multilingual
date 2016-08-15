Changelog
=========

3.0.3 (2016-08-15)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


3.0.2 (2016-02-26)
------------------

Fixes:

- Removed transaction commit in integration test.  [gforcada]


3.0.1 (2015-07-18)
------------------

- Any AT object can be adapted to ILanguage (not just ATContentTypes).
  [ebrehault]


3.0 (2015-03-26)
----------------

- Adapt archetypes.multilingual to work on Plone 5
  [bloodbare]


1.3dev - Unreleased
-------------------

- Remove archetypes.testcase test dependency.
  [timo]

- Remove PloneLanguageTool dependency.
  [timo]


1.2 - 2013-09-24
----------------

- Add french translations

1.0 - 2013-04-16
----------------

- Correct js url on portal_factory babel view [ramon]
- Show selector if num languages is large [pysailor]

1.0rc1 - 2013-01-26
-------------------

- Update .po files and .pot
- Fix some failing tests
- Bumped version to match the others [sneridagh]

1.0b3 - 2012-10-04
------------------

- Added tests [sneridagh]
- Solved bugs on subscribers [ramon]
- Tuned AT babel view [ramon]
- Monkey language field [ramon]

1.0a1 - 2012-04-03
------------------

- Added needed babel view template [sneridagh]
- Language independent field implementation [jcbrand]
- ILanguage implementation [awello]
