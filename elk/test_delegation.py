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
    b = elk.ElkAttribute(handles=['c', 'd'])


class B(object):
    __metaclass__ = elk.ElkMeta
    c = elk.ElkAttribute(handles=['d'])


class C(object):
    __metaclass__ = elk.ElkMeta
    d = elk.ElkAttribute(default=10)


class DelegationTestCase(unittest.TestCase):
    def test_b_get_d(self):
        """Test single-level delegation: get."""
        b = B()
        b.c = C()
        self.assertEqual(b.d, 10)

    def test_b_set_d(self):
        """Test single-level delegation: set."""
        b = B()
        b.c = C()
        b.d = 20
        self.assertEqual(b.d, 20)

    def test_b_del_d(self):
        """Test single-level delegation: del."""
        b = B()
        b.c = C()
        del b.d
        self.assertFalse(hasattr(b, 'd'))

    def test_a_get_d(self):
        """Test multi-level delegation: get."""
        a = A()
        a.b = B()
        a.c = C()
        self.assertEqual(a.d, 10)

    def test_a_set_d(self):
        """Test multi-level delegation: set."""
        a = A()
        a.b = B()
        a.c = C()
        a.d = 20
        self.assertEqual(a.d, 20)

    def test_a_del_d(self):
        """Test multi-level delegation: del."""
        a = A()
        a.b = B()
        a.c = C()
        del a.d
        self.assertFalse(hasattr(a, 'd'))
