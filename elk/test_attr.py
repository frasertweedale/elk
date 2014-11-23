# This file is part of Elk
# Copyright (C) 2014  Fraser Tweedale
#
# Elk is free software: you can redistribute it and/or modify
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
    x = elk.attr()


class AttrTestCase(unittest.TestCase):
    def test_attr_is_ElkAttribute(self):
        self.assertIs(elk.attr, elk.ElkAttribute)

    def test_attr_no_arg(self):
        """'attr' sanity check."""
        with self.assertRaises(AttributeError):
            a = A()
            a.x

    def test_attr_arg_none(self):
        """'attr' sanity check."""
        a = A(x=None)
        self.assertIsNone(a.x)

    def test_attr_arg_not_none(self):
        """'attr' sanity check."""
        a = A(x=10)
        self.assertEqual(a.x, 10)
