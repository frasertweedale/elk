# This file is part of elk
# Copyright (C) 2012, 2013 Fraser Tweedale
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


class A(object):
    __metaclass__ = elk.ElkMeta
    x = elk.ElkAttribute(default=10)
    y = elk.ElkAttribute(default=None)
    z = elk.ElkAttribute()


class DefaultTestCase(unittest.TestCase):
    def test_without_arg(self):
        """Test default value when no init arg provided."""
        a = A()
        self.assertEqual(a.x, 10)

    def test_with_arg(self):
        """Test that init arg preferred to default."""
        a = A(x=20)
        self.assertEqual(a.x, 20)

    def test_default_is_none(self):
        """Test that a default of ``None`` sets the value."""
        a = A()
        self.assertIsNone(a.y)

    def test_no_default(self):
        """Test that no specified default does not set the attribute."""
        a = A()
        with self.assertRaises(AttributeError):
            a.z

    def test_callable_receives_obj_and_returns_value(self):
        """Callable default is called to generate default."""
        class B(elk.Elk):
            x = elk.ElkAttribute(default=lambda self: self)
            lazy_x = elk.ElkAttribute(default=lambda self: self, lazy=True)
            y = elk.ElkAttribute(default=lambda self: 'hi')

        b = B()
        self.assertEqual(b.x, b)
        self.assertEqual(b.lazy_x, b)
        self.assertEqual(b.y, 'hi')

    def test_nonhashable_default(self):
        """Nonhashable default raises TypeError."""
        with self.assertRaises(TypeError):
            class B(object):
                __metaclass__ = elk.ElkMeta
                x = elk.ElkAttribute(default=[])
