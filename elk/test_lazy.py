import unittest

from . import elk


class LazyDefaultChecker(object):
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return 42


checker = LazyDefaultChecker()


class A(object):
    __metaclass__ = elk.ElkMeta
    non_lazy = elk.ElkAttribute(lazy=True)
    trivial_default = elk.ElkAttribute(lazy=True, default='hi')
    default = elk.ElkAttribute(lazy=True, default=checker)
    builder = elk.ElkAttribute(lazy=True, builder='_build')
    built = elk.ElkAttribute(default=False)

    def _build(self):
        self.built = True
        return 'buttercup'


class BuilderTestCase(unittest.TestCase):
    def test_builder(self):
        a = A()
        self.assertFalse(a.built)
        self.assertEqual(a.builder, 'buttercup')
        self.assertTrue(a.built)

    def test_default(self):
        a = A()
        count = checker.count
        self.assertEqual(a.default, 42)
        self.assertEqual(checker.count, count + 1)

    def test_trivial_default(self):
        a = A()
        self.assertEqual(a.trivial_default, 'hi')
