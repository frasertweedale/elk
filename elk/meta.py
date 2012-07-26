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

from . import attribute


class ElkMeta(type):
    def __new__(mcs, name, bases, dict):
        attrdescs = {
            k: v for k, v in dict.items()
            if isinstance(v, attribute.AttributeDescriptor)
        }
        for k in attrdescs:
            attrdescs[k].init_class(k, dict)
        return type.__new__(mcs, name, bases, dict)

    def __call__(self, *args, **kwargs):
        # build a mapping of attribute descriptors
        attrdescs = {
            k: v for k, v in self.__dict__.items()
            if isinstance(v, attribute.AttributeDescriptor)
        }

        # extract attribute values from kwargs
        init_args = set(v._init_arg or k for k, v in attrdescs.viewitems())
        values = {k: kwargs.pop(k) for k in set(kwargs) & init_args}

        # create new object with leftover args
        obj = type.__call__(self, *args, **kwargs)

        # initialise attributes
        obj.__elk_attrs__ = {}
        obj.__elk_lazy__ = {}
        for method in (
            'init_instance_value',
            'init_instance_default',
            'init_instance_builder',
            'init_instance_required',
        ):
            finished = []
            for k, v in attrdescs.viewitems():
                kwargs = {}
                init_arg = v._init_arg or k
                if init_arg in values:
                    kwargs['value'] = values[init_arg]
                if getattr(v, method)(obj, **kwargs):
                    finished.append(k)
            for k in finished:
                del attrdescs[k]

        return obj
