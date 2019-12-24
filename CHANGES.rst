Changelog
=========

2.1.1 (2019-12-24)
------------------

Bug fixes:

- Add test for fix regarding "Insufficient Privileges" errors.
  See https://github.com/plone/plone.app.multilingual/pull/351
  [witsch]


2.1.0 (2019-05-31)
------------------

- Remove archetypes.testcase test dependency.
  [timo]

- The ``ILanguage`` implementation for Archetypes was broken. This close #13.
  [keul, frisi]

- Add tests when content is added with portal_factory (old way)
  [bsuttor]

- Override Dexterity add transalation for Archetypes
  [bsuttor]


2.0 (2015-03-26)
----------------

- Compatibility release for PAM 2.0.

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
