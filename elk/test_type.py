# This file is part of elk
# Copyright (C) 2012 Fraser Tweedale
#
# elk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

    def test_init_with_wrong_type_raises_TypeError(self):
        with self.assertRaises(TypeError):
            Thing(one_type='wrong')


class BadDefaultTestCase(unittest.TestCase):
    def test_bad_default(self):
        with self.assertRaises(TypeError):
            class BadDefaultThing(object):
                __metaclass__ = elk.ElkMeta
                bad = elk.ElkAttribute(type=bool, default=10)
