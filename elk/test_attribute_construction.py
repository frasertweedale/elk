# This file is part of Elk
# Copyright (C) 2013 Fraser Tweedale
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


class ConstructionTestCase(unittest.TestCase):
    def test_constructing_with_no_options_succeeds(self):
        self.assertIsInstance(elk.ElkAttribute(), elk.ElkAttribute)

    def test_constructing_with_unrecognised_option_raises_TypeError(self):
        with self.assertRaises(TypeError):
            elk.ElkAttribute(no_such_option='whatever')
