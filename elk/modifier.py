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

import functools
import itertools


@functools.total_ordering
class Modifier(object):
    counter = itertools.count()

    def __init__(self, name, f):
        self._name = name
        self._f = f
        self._seq = next(self.counter)

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        # around modifiers are the "innermost" modifiers
        order = (AroundModifier, BeforeModifier, AfterModifier)
        order_cmp = order.index(type(self)) - order.index(type(other))
        return self._seq < other._seq if order_cmp == 0 else order_cmp < 0


class BeforeModifier(Modifier):
    def apply(self, dict, bases):
        if self._name in dict:
            o = dict[self._name]
            get_orig = lambda i: functools.partial(o, i)
        else:
            get_orig = lambda i: getattr(super(type(i), i), self._name)
        def wrapped(instance, *args, **kwargs):
            self._f(instance, *args, **kwargs)
            return get_orig(instance)(*args, **kwargs)
        dict[self._name] = wrapped


class AfterModifier(Modifier):
    def apply(self, dict, bases):
        if self._name in dict:
            o = dict[self._name]
            get_orig = lambda i: functools.partial(o, i)
        else:
            get_orig = lambda i: getattr(super(type(i), i), self._name)
        def wrapped(instance, *args, **kwargs):
            result = get_orig(instance)(*args, **kwargs)
            self._f(instance, *args, **kwargs)
            return result
        dict[self._name] = wrapped


class AroundModifier(Modifier):
    def apply(self, dict, bases):
        if self._name in dict:
            o = dict[self._name]
            get_orig = lambda i: functools.partial(o, i)
        else:
            get_orig = lambda i: getattr(super(type(i), i), self._name)
        def wrapped(instance, *args, **kwargs):
            return self._f(instance, get_orig(instance), *args, **kwargs)
        dict[self._name] = wrapped


def before(name):
    return functools.partial(BeforeModifier, name)


def after(name):
    return functools.partial(AfterModifier, name)


def around(name):
    return functools.partial(AroundModifier, name)
