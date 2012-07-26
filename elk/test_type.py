"""Test attribute type restriction."""

import unittest

from . import elk


class A(object):
    pass


class Thing(object):
    __metaclass__ = elk.ElkMeta
    any_type = elk.ElkAttribute()
    none = elk.ElkAttribute(type=None)
    one_type = elk.ElkAttribute(type=int)
    multiple_types = elk.ElkAttribute(type=(int, str))
    a_only = elk.ElkAttribute(type=A)


class TypeTestCase(unittest.TestCase):
    def test_any_type(self):
        """Unspecified type allows any type."""
        x = Thing()
        x.any_type = 'a string'
        self.assertEqual(x.any_type, 'a string')
        x.any_type = 10
        self.assertEqual(x.any_type, 10)

    def test_none(self):
        """Type of ``None`` allows any type."""
        x = Thing()
        x.none = 'a string'
        self.assertEqual(x.none, 'a string')
        x.none = 10
        self.assertEqual(x.none, 10)

    def test_one_type(self):
        x = Thing()
        x.one_type = 10
        self.assertEqual(x.one_type, 10)
        with self.assertRaises(TypeError):
            x.one_type = 'a string'

    def test_multiple_types(self):
        x = Thing()
        x.multiple_types = 10
        self.assertEqual(x.multiple_types, 10)
        x.multiple_types = 'a string'
        self.assertEqual(x.multiple_types, 'a string')
        with self.assertRaises(TypeError):
            x.multiple_types = []

    def test_a_only(self):
        """Instances of subtypes are allowed."""
        x = Thing()
        a = A()
        x.a_only = a
        self.assertIs(x.a_only, a)

        class B(A):
            pass

        b = B()
        x.a_only = b
        self.assertIs(x.a_only, b)

        with self.assertRaises(TypeError):
            x.a_only = 10


class BadDefaultTestCase(unittest.TestCase):
    def test_bad_default(self):
        with self.assertRaises(TypeError):
            class BadDefaultThing(object):
                __metaclass__ = elk.ElkMeta
                bad = elk.ElkAttribute(type=bool, default=10)
