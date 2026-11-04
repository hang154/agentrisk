"""Exact discrete comparison with a fixed floating-point roundoff allowance."""
import math


def assert_equivalent(actual, expected, path='result'):
    if isinstance(expected, dict):
        assert isinstance(actual, dict) and actual.keys() == expected.keys(), path
        for key in expected:
            assert_equivalent(actual[key], expected[key], path + '.' + key)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), path
        for i, (a, b) in enumerate(zip(actual, expected)):
            assert_equivalent(a, b, path + '[' + str(i) + ']')
    elif type(expected) is float:
        assert type(actual) is float and math.isfinite(actual) and math.isfinite(expected), path
        assert abs(actual - expected) <= 1e-12, (path, actual, expected)
    else:
        assert type(actual) is type(expected) and actual == expected, (path, actual, expected)
