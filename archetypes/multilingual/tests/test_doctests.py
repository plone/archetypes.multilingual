# -*- coding: utf-8 -*-
from archetypes.multilingual.testing import \
    ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING
from archetypes.multilingual.testing import optionflags
from plone.testing import layered

import doctest
import unittest

integration_tests = [
    'languageindependentfields.txt',
    'multilingual.txt',
]


def test_suite():
    return unittest.TestSuite([
        layered(
            doctest.DocFileSuite(
                filename,
                package='archetypes.multilingual.tests',
                optionflags=optionflags
            ),
            layer=ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING
        ) for filename in integration_tests
    ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
