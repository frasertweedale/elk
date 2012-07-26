import unittest

from . import elk


class A(object):
    __metaclass__ = elk.ElkMeta
    x = elk.ElkAttribute(builder='_build_x')
    y = elk.ElkAttribute(builder=None)

    def _build_x(self):
        return 'buttercup'


class BuilderTestCase(unittest.TestCase):
    def test_builder(self):
        a = A()
        self.assertEqual(a.x, 'buttercup')

    def test_builder_none(self):
        a = A()
        with self.assertRaises(AttributeError):
            a.y
        a.y = 'foo'
        self.assertEqual(a.y, 'foo')

    def test_builder_bogus_arg(self):
        with self.assertRaises(TypeError):
            class B(object):
                __metaclass__ = elk.ElkMeta
                x = elk.ElkAttribute(builder=3.14)

    def test_builder_no_method(self):
        """Unknown builder method is handled properly."""
        with self.assertRaises(AttributeError):
            class C(object):
                __metaclass__ = elk.ElkMeta
                x = elk.ElkAttribute(builder='nonexistant')
