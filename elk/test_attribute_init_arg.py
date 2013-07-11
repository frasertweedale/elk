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
    y = elk.ElkAttribute(init_arg='init_y')
    z = elk.ElkAttribute(init_arg=None)


class InitArgTestCase(unittest.TestCase):
    def test_init_arg(self):
        """``init_arg`` parameter overrides init argument."""
        a = A(init_y=20)
        self.assertEqual(a.y, 20)

    def test_init_arg_non_str(self):
        """Non-str ``init_arg`` value raises TypeError."""
        with self.assertRaises(TypeError):
            class B(elk.Elk):
                x = elk.ElkAttribute(init_arg=10)

    def test_none_disables_setting_via_constructor(self):
        with self.assertRaises(TypeError):
            A(z='zed')
