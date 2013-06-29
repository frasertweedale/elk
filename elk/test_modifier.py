# This file is part of elk
# Copyright (C) 2013 Fraser Tweedale
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

    s = elk.ElkAttribute(default='')

    def orig(self, *args, **kwargs):
        self.s += 'o'
        return args, kwargs

    @elk.before('orig')
    def before1(self, *args, **kwargs):
        self.s += 'b1'

    @elk.after('orig')
    def after1(self, *args, **kwargs):
        self.s += 'a1'

    @elk.around('orig')
    def around1(self, *args, **kwargs):
        self.s += 'r1'
        yield
        self.s += "r1'"

    @elk.before('orig')
    def before2(self, *args, **kwargs):
        self.s += 'b2'

    @elk.after('orig')
    def after2(self, *args, **kwargs):
        self.s += 'a2'

    @elk.around('orig')
    def around2(self, *args, **kwargs):
        self.s += 'r2'
        yield
        self.s += "r2'"


class B(A):
    @elk.before('orig')
    def before3(self, *args, **kwargs):
        self.s += 'b3'

    @elk.after('orig')
    def after3(self, *args, **kwargs):
        self.s += 'a3'

    @elk.around('orig')
    def around3(self, *args, **kwargs):
        self.s += 'r3'
        yield
        self.s += "r3'"


class MethodModifiersTestCase(unittest.TestCase):
    def test_modifiers_modify_sibling_method(self):
        a = A()
        self.assertEqual(a.orig(1, k=2), ((1,), {'k': 2}))
        self.assertEqual(a.s, "b2b1r2r1or1'r2'a1a2")

    def test_modifiers_modify_superclass_method(self):
        b = B()
        self.assertEqual(b.orig(), ((), {}))
        self.assertEqual(b.s, "b3r3b2b1r2r1or1'r2'a1a2r3'a3")
