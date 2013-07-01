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
    b = elk.ElkAttribute(handles=['attr', 'method'])


class B(object):
    __metaclass__ = elk.ElkMeta
    c = elk.ElkAttribute(handles=['attr', 'method'])


class C(object):
    __metaclass__ = elk.ElkMeta
    attr = elk.ElkAttribute(default=10)

    def method(self):
        return 'yay'


class DelegationTestCase(unittest.TestCase):
    def test_can_getattr_through_delegation(self):
        a = A()
        b = B()
        c = C()
        a.b = b
        b.c = c
        self.assertEqual(b.attr, 10)
        self.assertEqual(a.attr, 10)

    def test_can_setattr_through_delegation(self):
        a = A()
        b = B()
        c = C()
        a.b = b
        b.c = c
        b.attr = 20
        self.assertEqual(b.attr, 20)
        self.assertEqual(c.attr, 20)
        a.attr = 30
        self.assertEqual(a.attr, 30)
        self.assertEqual(b.attr, 30)
        self.assertEqual(c.attr, 30)

    def test_can_delattr_through_delegation(self):
        b = B()
        c = C()
        b.c = c
        del b.attr
        self.assertFalse(hasattr(b, 'attr'))
        self.assertFalse(hasattr(c, 'attr'))
        a = A()
        b = B()
        c = C()
        a.b = b
        b.c = c
        del a.attr
        self.assertFalse(hasattr(a, 'attr'))
        self.assertFalse(hasattr(b, 'attr'))
        self.assertFalse(hasattr(c, 'attr'))

    def test_can_delegate_to_method(self):
        a = A()
        b = B()
        c = C()
        a.b = b
        b.c = c
        self.assertEqual(b.method(), 'yay')
        self.assertEqual(a.method(), 'yay')
