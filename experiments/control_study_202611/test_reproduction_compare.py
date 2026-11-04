import unittest
from .reproduction_compare import assert_equivalent


class ReproductionComparisonTests(unittest.TestCase):
    def test_arithmetic_roundoff_only(self):
        assert_equivalent({'n': 800, 'pass': False, 'score': .3 + 5e-15},
                          {'n': 800, 'pass': False, 'score': .3})

    def test_changed_decisions_denominators_or_score_rejected(self):
        for actual, expected in [(801, 800), (True, False), (1.0, 1),
                                 ({'x': .301}, {'x': .3}), ([1], [1, 2])]:
            with self.assertRaises(AssertionError):
                assert_equivalent(actual, expected)
