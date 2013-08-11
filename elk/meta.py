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

import collections

from . import attribute
from . import modifier


class ElkMeta(type):
    def __new__(mcs, name, bases, dict):
        # initialise roles
        roles = dict.get('__with__', ())
        if not isinstance(roles, collections.Iterable):
            roles = (roles,)
        badroles = [
            role for role in roles
            if not issubclass(type(role), ElkRoleMeta)
        ]
        if badroles:
            raise TypeError(
                'Non-roles in __roles__: {}'.format(badroles)
            )
        dict['__elk_roles__'] = roles
        for role in roles:
            ElkRoleMeta.apply_to_class_dict(dict, role)

        # initialise attributes
        attrdescs = {}
        for base in reversed(bases):
            if hasattr(base, '__elk_attrs__'):
                attrdescs.update(base.__elk_attrs__)
        attrdescs.update({
            k: v for k, v in dict.items()
            if isinstance(v, attribute.AttributeDescriptor)
        })
        for k in attrdescs:
            attrdescs[k].init_class(k, dict)
        dict['__elk_attrs__'] = attrdescs

        init_args = set(
            v._init_arg or k for k, v in attrdescs.viewitems()
            if not v._has_init_arg or v._init_arg is not None
        )
        dict['__elk_init_args__'] = init_args

        cls = type.__new__(mcs, name, bases, dict)

        # check role requirements
        for role in roles:
            ElkRoleMeta.check_requirements(cls, role)

        # apply method modifiers
        modifiers = sorted(
            v for v in dict.viewvalues()
            if isinstance(v, modifier.Modifier)
        )
        for mod in modifiers:
            mod.apply(cls)

        return cls

    def __call__(cls, *args, **kwargs):
        try:
            buildargs = cls.__buildargs__
        except AttributeError:
            buildargs = lambda **kwargs: kwargs
        kwargs = buildargs(*args, **kwargs)

        # build a mapping of attribute descriptors
        attrdescs = cls.__elk_attrs__

        # extract attribute values from kwargs
        values = {k: kwargs[k] for k in set(kwargs) & cls.__elk_init_args__}

        # create new object
        obj = type.__call__(cls)

        # initialise attributes
        obj.__elk_attrs__ = {}
        obj.__elk_lazy__ = {}
        finished = set()
        for method in (
            'init_instance_value',
            'init_instance_default',
            'init_instance_builder',
            'init_instance_required',
        ):
            for k in attrdescs.viewkeys() - finished:
                init_arg = attrdescs[k]._init_arg or k
                value = (values[init_arg],) if init_arg in values else ()
                if getattr(attrdescs[k], method)(obj, value):
                    finished.add(k)

        # call __build__
        obj.__build__(**kwargs)
        return obj


class ElkRoleMeta(type):
    def __new__(mcs, name, bases, role_dict):
        # IronPython 2.7.0.40 does not expose descriptors in
        # dictproxy iteration, so copy the dict.
        role_dict['__elk_role_attrs__'] = dict(role_dict)
        return type.__new__(mcs, name, bases, role_dict)

    def __call__(self, *args, **kwargs):
        raise TypeError('Roles cannot be instantiated directly.')

    def __instancecheck__(cls, instance):
        return issubclass(type(instance), cls)

    def __subclasscheck__(cls, subclass):
        roles = getattr(subclass, '__with__', ())
        if not isinstance(roles, collections.Iterable):
            roles = (roles,)
        return cls in roles

    @classmethod
    def apply_to_class_dict(mcs, dict, role):
        """Apply a role to a class."""
        for k, v in role.__elk_role_attrs__.viewitems():
            if k not in dict:
                dict[k] = v

    @classmethod
    def check_requirements(mcs, cls, role):
        requires = getattr(role, '__require__', ())
        if isinstance(requires, str):
            requires = (requires,)
        for require in requires:
            if not hasattr(cls, require):
                raise TypeError('{} requires {}'.format(role, require))


class Elk(object):
    __metaclass__ = ElkMeta

    def __build__(self, **kwargs):
        unknown_attrs = kwargs.viewkeys() - self.__elk_init_args__
        if unknown_attrs:
            raise TypeError("unknown attributes: {}".format(unknown_attrs))


class ElkRole(object):
    __metaclass__ = ElkRoleMeta
