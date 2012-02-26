# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
import unittest2 as unittest
import doctest
from plone.testing import layered
from archetypes.multilingual.tests._testing import (
    ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING,
    ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING,
    optionflags,
)
integration_tests = [
    'languageindependentfields.txt',
    'multilingual.txt',
    'monkey.txt',

]
functional_tests = [
]


def test_suite():
    return unittest.TestSuite(
        [layered(doctest.DocFileSuite('%s' % f,
                    package='archetypes.multilingual.tests',
                    optionflags=optionflags),
                 layer=ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING)
            for f in integration_tests]
        +
        [layered(doctest.DocFileSuite('%s' % f,
                    package='archetypes.multilingual.tests',
                    optionflags=optionflags),
                 layer=ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING)
            for f in functional_tests]
        )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
