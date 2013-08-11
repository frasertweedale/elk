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

Besides defining their own methods and attributes, roles can also
require that the consuming class define certain attributes
(including methods) of its own.  You could have a role that
consisted only of a list of required attributes, in which case the
role would be very much like a Python abstract base class (i.e. via
the :py:mod:`abc` module) or a Java interface.


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
  times will override the earlier declarations.  Assign an interable
  to consume multiple roles.


Required methods
================

As mentioned previously, a role can require that consuming classes
provide certain attributes (any Python attributes, including but not
necessarily Elk attributes).  There is no distinction between Python
attributes and methods in this regard (a method is simply a callable
attribute).

Using our Breakable example, let's make it require that consuming
classes implement their own break methods::

    class Breakable(elk.ElkRole):
        __require__ = 'break_'

        is_broken = elk.ElkAttribute(type=bool, default=False)

        @elk.after('break_')
        def _after_break(self):
            self.is_broken = True


If we try to consume this role in a class that does not have the
``break_`` attribute, ``TypeError`` will be raised.  This role
expects ``break_`` to be a method, but this is not enforced.

You can see that we added a method modifier on ``break_``. We want
classes that consume this role to implement their own logic for
breaking, but we make sure that the ``is_broken`` attribute is
always set to ``True`` when ``break_`` is called.

::

    class Car(elk.Elk):
        __with__ = Breakable

        engine = elk.ElkAttribute(type=Engine)

        def break_(self):
            if self.is_moving:
                self.stop()


.. note::

  ``__require__`` must be specified only once.  Declaring it
  multiple times will override the earlier declarations.  Assign an
  interable of strings to require multiple attributes


Roles versus Abstract Base Classes
----------------------------------

If you are familiar with the concept of abstract base classes in
Python or other languages, you may be tempted to use roles in the
same way.

You can define an "interface-only" role—one that contains just a
list of required attributes.

Any class that consumes such a role must provide all of the required
attributes, either directly, through inheritance, or via other roles
it consumes.  You cannot delay the attribute requirement check so
that they can be implemented by future subclasses.
