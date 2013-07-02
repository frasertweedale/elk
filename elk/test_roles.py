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


class Role(elk.ElkRole):
    role_attr = elk.ElkAttribute(default='a')

    def role_method(self):
        return 'value'


class AnotherRole(elk.ElkRole):
    another_role_attr = elk.ElkAttribute(default='b')

    def another_role_method(self):
        return 'another value'


class Consumer(object):
    __metaclass__ = elk.ElkMeta
    __with__ = Role


class SubConsumer(Consumer):
    pass


class MultiConsumer(object):
    __metaclass__ = elk.ElkMeta
    __with__ = Role, AnotherRole


class NonConsumer(object):
    __metaclass__ = elk.ElkMeta


class RoleTestCase(unittest.TestCase):
    def test_consumer_does_role(self):
        self.assertTrue(isinstance(Consumer(), Role))
        self.assertTrue(issubclass(Consumer, Role))

    def test_subconsumer_does_role(self):
        self.assertTrue(isinstance(SubConsumer(), Role))
        self.assertTrue(issubclass(SubConsumer, Role))

    def test_multi_consumer_does_all_roles(self):
        for role in [Role, AnotherRole]:
            self.assertTrue(isinstance(MultiConsumer(), Role))
            self.assertTrue(issubclass(MultiConsumer, Role))

    def test_non_consumer_does_not(self):
        self.assertFalse(isinstance(NonConsumer(), Role))
        self.assertFalse(isinstance(Consumer(), AnotherRole))
        self.assertFalse(issubclass(NonConsumer, Role))
        self.assertFalse(issubclass(Consumer, AnotherRole))

    def test_consumer_receives_attributes(self):
        self.assertTrue(hasattr(Consumer(), 'role_attr'))
        self.assertEqual(Consumer().role_attr, 'a')

        self.assertTrue(hasattr(MultiConsumer(), 'role_attr'))
        self.assertTrue(hasattr(MultiConsumer(), 'another_role_attr'))
        self.assertEqual(MultiConsumer().role_attr, 'a')
        self.assertEqual(MultiConsumer().another_role_attr, 'b')

    def test_subconsumer_receives_attributes(self):
        self.assertTrue(hasattr(SubConsumer(), 'role_attr'))
        self.assertEqual(SubConsumer().role_attr, 'a')

    def test_consumer_receives_methods(self):
        self.assertTrue(hasattr(Consumer, 'role_method'))
        self.assertEqual(Consumer().role_method(), 'value')

        self.assertTrue(hasattr(MultiConsumer, 'role_method'))
        self.assertTrue(hasattr(MultiConsumer, 'another_role_method'))
        self.assertEqual(MultiConsumer().role_method(), 'value')
        self.assertEqual(
            MultiConsumer().another_role_method(),
            'another value'
        )

    def test_subconsumer_receives_methods(self):
        self.assertTrue(hasattr(SubConsumer, 'role_method'))
        self.assertEqual(SubConsumer().role_method(), 'value')

    def test_consume_non_role(self):
        class NonRole(object):
            a = 1

        with self.assertRaises(TypeError):
            class BogoConsumer(object):
                __metaclass__ = elk.ElkMeta
                __with__ = NonRole

    def test_cannot_instantiate_role(self):
        with self.assertRaises(TypeError):
            Role()


class Breakable(elk.ElkRole):
    is_broken = elk.ElkAttribute(mode='rw', type=bool, default=False)

    def break_(self):
        self.is_broken = True


class Engine:
    pass


class Car:
    __metaclass__ = elk.ElkMeta
    __with__ = Breakable

    engine = elk.ElkAttribute(mode='ro', type=Engine)


class MooseRolesTestCase(unittest.TestCase):
    """Test case based on Moose::Manual::Roles."""
    def test_car(self):
        car = Car(engine=Engine())
        self.assertFalse(car.is_broken)
        car.break_()
        self.assertTrue(car.is_broken)
        self.assertTrue(isinstance(car, Breakable))
