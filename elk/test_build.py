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


class BuildTestCase(unittest.TestCase):
    def test_build_can_raise(self):
        class Person(elk.Elk):
            def __build__(self, **kwargs):
                raise UserWarning

        with self.assertRaises(UserWarning):
            Person()

    def test_build_receives_obj_and_buildargs_kwargs(self):
        class A(elk.Elk):
            @classmethod
            def __buildargs__(cls, *args, **kwargs):
                return {'foo': 'bar'}

            def __build__(self, **kwargs):
                self._self = self
                self._build_args = kwargs

        a = A(1, quux='xyzzy')
        self.assertIs(a._self, a)
        self.assertEqual(a._build_args, {'foo': 'bar'})

    def test_build_called_after_attribute_initialisation(self):
        class A(elk.Elk):
            x = elk.ElkAttribute(default=1234)

            def __build__(self, **kwargs):
                self.x += 1

        self.assertEqual(A().x, 1235)
