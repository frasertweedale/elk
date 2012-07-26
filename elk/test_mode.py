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


class A(object):
    __metaclass__ = elk.ElkMeta
    ro = elk.ElkAttribute(mode='ro')
    ro_default = elk.ElkAttribute(mode='ro', default=10)
    rw = elk.ElkAttribute(mode='rw')
    default = elk.ElkAttribute()


class ModeTestCase(unittest.TestCase):
    def test_bogus_mode(self):
        """Only 'ro' and 'rw' are valid."""
        with self.assertRaises(TypeError):
            class B(object):
                __metaclass__ = elk.ElkMeta
                attr = elk.ElkAttribute(mode='bogus')

    def test_ro(self):
        a = A()
        with self.assertRaises(AttributeError):
            a.ro
        self.assertEqual(a.ro_default, 10)
        with self.assertRaises(AttributeError):
            a.ro = 20
        with self.assertRaises(AttributeError):
            a.ro_default = 30

    def test_rw(self):
        a = A()
        with self.assertRaises(AttributeError):
            a.rw
        a.rw = 40
        self.assertEqual(a.rw, 40)

    def test_default_mode(self):
        """The default mode is 'rw'."""
        a = A()
        with self.assertRaises(AttributeError):
            a.default
        a.default = 50
        self.assertEqual(a.default, 50)
