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

import unittest

from . import elk


class A(elk.Elk):
    x = elk.ElkAttribute(builder='_build_x')
    y = elk.ElkAttribute(builder=None)

    def _build_x(self):
        return 'buttercup'


class B(A):
    def _build_x(self):
        return 'let me down'


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

    def test_subclass_can_override_builder_method(self):
        self.assertEqual(B().x, 'let me down')


    def test_role_consumer_can_supply_builder_for_role_attribute(self):
        class HasSize(elk.ElkRole):
            size = elk.ElkAttribute(builder='_build_size')

        class Thing(elk.Elk):
            __with__ = HasSize

            def _build_size(self):
                return 'small'

        self.assertEqual(Thing().size, 'small')
