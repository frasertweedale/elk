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

import functools
import types


class DelegationDescriptor(object):
    """Delegate to an attribute on the value of the given descriptor."""
    def __init__(self, name, attrdesc):
        self.name = name
        self.attrdesc = attrdesc

    def __get__(self, instance, owner):
        return getattr(self.attrdesc.__get__(instance, None), self.name)

    def __set__(self, instance, value):
        setattr(self.attrdesc.__get__(instance, None), self.name, value)

    def __delete__(self, instance):
        delattr(self.attrdesc.__get__(instance, None), self.name)


def _key_error_to_attribute_error(method):
    """Descriptor method wrapper that raises AttributeError on KeyError."""
    def wrapped(self, instance, *args):
        try:
            return method(self, instance, *args)
        except KeyError:
            raise AttributeError(
                '{!r} object {!r} attribute is not set'
                .format(type(instance).__name__, self._name)
            )
    return wrapped


class AttributeDescriptor(object):
    def __init__(
        self,
        mode='rw',
        required=False,
        lazy=False,
        builder=None,
        type=None,
        handles=None,
        **kwargs
    ):
        # check mode
        if mode not in ('ro', 'rw'):
            raise TypeError("mode must be one of 'ro', 'rw'")
        self._mode = mode

        # store required
        self._required = required

        # store lazy
        self._lazy = lazy

        # check and store default
        self._has_default = True if 'default' in kwargs else False
        self._default = kwargs.get('default')
        if self._has_default:
            try:
                hash(self._default)
            except:
                raise TypeError(
                    "unhashable default must be wrapped in callable"
                )

        # check and store builder
        if builder is not None and not isinstance(builder, str):
            raise TypeError('builder must be a str')
        self._has_builder = True if builder else False
        self._builder_name = builder

        # store type
        self._type = type

        # check and store init_arg
        self._has_init_arg = True if 'init_arg' in kwargs else False
        self._init_arg = kwargs.get('init_arg')
        if not isinstance(self._init_arg, (str, types.NoneType)):
            raise TypeError('init_arg must be str or None')

        # store delegation list
        handles = handles if handles is not None else []
        self._handles = handles

        # perform whatever checks we can right now (compile-time!)
        if self._type is not None and self._has_default \
                and not isinstance(self._default, self._type):
            raise TypeError('Attribute default has bad type.')

    def init_class(self, name, dict):
        """Initialise the attribute descriptor with respect to the class.

        Store the name of this attribute inside the descriptor.  It
        could be looked up when it's needed but since we know it
        right now, we save the trouble and just remember it.

        If a builder method is named, check that it exists on the
        class.

        Set up descriptors required to handle attribute delegations.

        """
        # store name
        self._name = name

        # check builder
        if self._has_builder:
            if self._builder_name not in dict:
                raise AttributeError(
                    '{!r} attribute builder method {!r} not found'
                    .format(self._name, self._builder_name)
                )
            if not callable(dict[self._builder_name]):
                raise AttributeError(
                    '{!r} attribute builder {!r} is not callable'
                    .format(self._name, self._builder_name)
                )

        # set up delegation
        for name in self._handles:
            dict[name] = DelegationDescriptor(name, self)

    def init_instance_value(self, instance, **kwargs):
        """Initialise the attribute with respect to the instance.

        ``value``
          If supplied, the initial value will be set to this value,
          in preference to any default that may have been specified.
        """
        if 'value' in kwargs:
            self.__set__(instance, kwargs['value'], force=True)
            return True

    def init_instance_default(self, instance, **kwargs):
        if self._has_default:
            default = self._default
            if self._lazy:
                if callable(default):
                    f = functools.partial(default, instance)
                else:
                    f = lambda: default
                instance.__elk_lazy__[id(self)] = f
            else:
                self.__set__(
                    instance,
                    default(instance) if callable(default) else default,
                    force=True
                )
            return True

    def init_instance_builder(self, instance, **kwargs):
        if self._has_builder:
            builder = getattr(instance, self._builder_name)
            if self._lazy:
                instance.__elk_lazy__[id(self)] = builder
            else:
                self.__set__(instance, builder(), force=True)
            return True

    def init_instance_required(self, instance, **kwargs):
        if self._required:
            # value required, but not provided, and no default or builder
            raise AttributeError('required attribute not provided')

    @_key_error_to_attribute_error
    def __get__(self, instance, owner):
        _id = id(self)
        if _id not in instance.__elk_attrs__ and _id in instance.__elk_lazy__:
            self.__set__(instance, instance.__elk_lazy__[_id](), force=True)
        return instance.__elk_attrs__[id(self)]

    def __set__(self, instance, value, force=False):
        if self._mode == 'ro' and not force:
            raise AttributeError('{!r} attribute is read-only')
        if self._type is not None and not isinstance(value, self._type):
            raise TypeError(
                '{!r} attribute must be a {!r}'
                .format(self._name, self._type)
            )
        instance.__elk_attrs__[id(self)] = value

    @_key_error_to_attribute_error
    def __delete__(self, instance):
        if self._required:
            raise AttributeError('cannot delete required attribute')
        del instance.__elk_attrs__[id(self)]
