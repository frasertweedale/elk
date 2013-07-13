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


class BuildargsTestCase(unittest.TestCase):
    def test_moose_manual_construction_example(self):
        class Person(elk.Elk):
            tfn = elk.ElkAttribute()

            @classmethod
            def __buildargs__(cls, *args, **kwargs):
                if len(args) == 1:
                    kwargs['tfn'] = args[0]
                return kwargs

        self.assertEqual(Person('1234').tfn, '1234')

    def test_position_arg_without_buildargs_raises_TypeError(self):
        class A(elk.Elk):
            pass

        with self.assertRaises(TypeError):
            A(1)
