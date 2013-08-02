..
  This file is part of the Elk Manual
  Copyright (C) 2013 Infinity Interactive, Inc.
  Copyright (C) 2013 Fraser Tweedale

  elk is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.


*****
Roles
*****

A role encapsulates some piece of behavior or state that can be
shared between classes. It is something that classes do. It is
important to understand that *roles are not normal classes*. You
cannot inherit from a role, and a role cannot be instantiated. We
sometimes say that roles are *consumed*, either by classes or other
roles.

Instead, a role is *composed* into a class. In practical terms, this
means that all of the methods, method modifiers, and attributes
defined in a role are added directly to (we sometimes say "flattened
into") the class that consumes the role. These attributes and
methods then appear as if they were defined in the class itself. A
subclass of the consuming class will inherit all of these methods
and attributes.

Elk roles are similar to mixins in other languages.


A simple role
=============

Creating a role looks a lot like creating a Moose class::

    class Breakable(elk.ElkRole):
        is_broken = elk.ElkAttribute(type=bool, default=False)

        def break_(self):
            print "I broke"
            self.is_broken = True


This looks just like a regular Elk class, except that we extend
``ElkRole``.  Attempting to instantiate ``Breakable`` will raise
``TypeError``.

The attributes and methods of a role will be composed into classes
that use the role::

    class Car(elk.Elk):
        __with__ = Breakable

        engine = elk.ElkAttribute(type=Engine)


The ``__with__`` declaration specifies the roles to be composed into
a class.  It can be a single ``ElkRole`` or an iterable of roles.
When the class is defined, the ``ElkMeta`` metaclass composes the
attributes and methods in the role into the consumer.
``isinstance(Consumer(), Role)`` and ``issubclass(Consumer, Role)``
will also return ``True``::

    car = Car(engine=Engine())

    print 'Busted' if car.is_broken else 'Still working'
    car.break_()
    print 'Busted' if car.is_broken else 'Still working'

    isinstance(car, Breakable)  # True

This prints::

    Still working
    I broke
    Busted

We could use this same ``Breakable`` role in a ``Bone`` class::

    class Bone(elk.Elk):
        __with__ = Breakable

        marrow = elk.ElkAttribute(type=Marrow)

.. note::

  ``__with__`` must be specified only once.  Declaring it multiple
  times will override the earlier declarations.
