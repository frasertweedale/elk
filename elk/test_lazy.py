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


class LazyDefaultChecker(object):
    def __init__(self):
        self.count = 0

    def __call__(self, obj):
        self.count += 1
        return 42


checker = LazyDefaultChecker()


class A(object):
    __metaclass__ = elk.ElkMeta
    non_lazy = elk.ElkAttribute(lazy=True)
    trivial_default = elk.ElkAttribute(lazy=True, default='hi')
    default = elk.ElkAttribute(lazy=True, default=checker)
    builder = elk.ElkAttribute(lazy=True, builder='_build')
    built = elk.ElkAttribute(default=False)

    def _build(self):
        self.built = True
        return 'buttercup'


class BuilderTestCase(unittest.TestCase):
    def test_builder(self):
        a = A()
        self.assertFalse(a.built)
        self.assertEqual(a.builder, 'buttercup')
        self.assertTrue(a.built)

    def test_default(self):
        a = A()
        count = checker.count
        self.assertEqual(a.default, 42)
        self.assertEqual(checker.count, count + 1)

    def test_trivial_default(self):
        a = A()
        self.assertEqual(a.trivial_default, 'hi')
