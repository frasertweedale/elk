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
    def around1(self, orig, *args, **kwargs):
        self.s += 'r1'
        result = orig(*args, **kwargs)
        self.s += "r1'"
        return result

    @elk.before('orig')
    def before2(self, *args, **kwargs):
        self.s += 'b2'

    @elk.after('orig')
    def after2(self, *args, **kwargs):
        self.s += 'a2'

    @elk.around('orig')
    def around2(self, orig, *args, **kwargs):
        self.s += 'r2'
        result = orig(*args, **kwargs)
        self.s += "r2'"
        return result


class B(A):
    @elk.before('orig')
    def before3(self, *args, **kwargs):
        self.s += 'b3'

    @elk.after('orig')
    def after3(self, *args, **kwargs):
        self.s += 'a3'

    @elk.around('orig')
    def around3(self, orig, *args, **kwargs):
        self.s += 'r3'
        result = orig(*args, **kwargs)
        self.s += "r3'"
        return result


class AroundExample(elk.Elk):
    x = elk.ElkAttribute(default=0)

    def orig1(self, *args, **kwargs):
        return args, kwargs

    @elk.around('orig1')
    def _around_orig1(self, orig, *args, **kwargs):
        return orig('hehe', modified='args')

    def orig2(self, *args, **kwargs):
        return args, kwargs

    @elk.around('orig2')
    def _around_orig2(self, orig, *args, **kwargs):
        result = orig(*args, **kwargs)
        return ('hehe',), {'modified': 'return'}

    def orig3(self):
        self.x += 1

    @elk.around('orig3')
    def _around_orig3(self, orig, call):
        if call:
            orig()


class MethodModifiersTestCase(unittest.TestCase):
    def test_modifiers_modify_sibling_method(self):
        a = A()
        self.assertEqual(a.orig(1, k=2), ((1,), {'k': 2}))
        self.assertEqual(a.s, "b2b1r2r1or1'r2'a1a2")

    def test_modifiers_modify_superclass_method(self):
        b = B()
        self.assertEqual(b.orig(), ((), {}))
        self.assertEqual(b.s, "b3r3b2b1r2r1or1'r2'a1a2r3'a3")

    def test_around_modifier_can_modify_args(self):
        x = AroundExample()
        self.assertEqual(x.orig1(1, k=2), (('hehe',), {'modified': 'args'}))

    def test_around_modifier_can_modify_return_value(self):
        x = AroundExample()
        self.assertEqual(x.orig2(1, k=2), (('hehe',), {'modified': 'return'}))

    def test_around_modifier_can_optionally_execute_orig(self):
        x = AroundExample()
        x.orig3(False)
        self.assertEqual(x.x, 0)
        x.orig3(True)
        self.assertEqual(x.x, 1)
