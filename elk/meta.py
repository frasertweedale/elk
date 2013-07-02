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

        # apply method modifiers
        modifiers = sorted(
            v for v in dict.viewvalues()
            if isinstance(v, modifier.Modifier)
        )
        for mod in modifiers:
            mod.apply(dict, bases)

        return type.__new__(mcs, name, bases, dict)

    def __call__(self, *args, **kwargs):
        # build a mapping of attribute descriptors
        attrdescs = self.__elk_attrs__

        # extract attribute values from kwargs
        init_args = set(
            v._init_arg or k for k, v in attrdescs.viewitems()
            if not v._has_init_arg or v._init_arg is not None
        )
        values = {k: kwargs.pop(k) for k in set(kwargs) & init_args}

        # create new object with leftover args
        obj = type.__call__(self, *args, **kwargs)

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
                kwargs = {}
                init_arg = attrdescs[k]._init_arg or k
                if init_arg in values:
                    kwargs['value'] = values[init_arg]
                if getattr(attrdescs[k], method)(obj, **kwargs):
                    finished.add(k)

        return obj


class ElkRoleMeta(type):
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
        for k, v in role.__dict__.items():
            if k not in dict and not k.startswith('__'):
                dict[k] = v


class Elk(object):
    __metaclass__ = ElkMeta


class ElkRole(object):
    __metaclass__ = ElkRoleMeta
