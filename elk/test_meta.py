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


class A(elk.Elk):
    x = elk.ElkAttribute(default=10)


class B(A):
    pass


class ElkMetaTestCase(unittest.TestCase):
    def test_subclasses_inherit_elk_attributes(self):
        self.assertEqual(B().x, 10)
