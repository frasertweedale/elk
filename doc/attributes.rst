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


**********
Attributes
**********

Elk attributes have many properties.  You can create a powerful
class simply by declaring attributes.

An attributes is a property that every member of a class has.  For
example, every ``Person`` might have a name and a date of birth.
Attributes can be optional, so some ``Person`` objects might have a
tax file number, and some might not.

At its simplest, an attribute can be thought of as a named value
that can be read and set.  However, attributes can also have
defaults, type constraints, delegation and much more.


Attribute options
=================

The options passed to ``ElkAttribute`` define the properties of the
attribute.  There are many options but none are required.

Read-write versus read-only
---------------------------

The ``mode`` option is used to control whether an attribute is
read-only (``"ro"``) or read-write (``"rw"``).  When an attribute is
read-only, attempting to set or delete its value raises
``AttributeError``.

Required or not?
----------------

By default, all attributes are optional and do not need to be
provided when an object is constructed.  If you want to make an
object required, simply set the ``required`` option to ``True``::


    class Person(elk.Elk):
        name = elk.ElkAttribute(required=True)


Constructing an object without supplying required attributes (as
keyword arguments) will raise ``AttributeError``.  Attempting to
delete a required attribute will also raise ``AttributeError``::

    person = Person()               # raises AttributeError
    person = Person(name='Alice')   # ok
    del person.name                 # raises AttributeError


Using ``required`` alongside ``default`` or ``builder`` relaxes the
need to supply a value to the constructor, but if a value is given
it is preferred over the default value.


Default and builder methods
---------------------------

Attributes can have default values, and Elk provides two ways to
specify that default.

In the simplest form, simply provide a value for the ``default``
option::

    class TeeShirt(elk.Elk):
        size = elk.ElkAttribute(default="medium")


If the size attribute is not provided to the constructor, it will be
set to ``"medium"``::

    shirt = TeeShirt()
    shirt.size           # "medium"


You can also provide a callable for ``default``.  The callable will
be called with the object as the single argument and its return
value will be the value of the attribute::

    import random

    class TeeShirt(elk.Elk):
        size = elk.ElkAttribute(
            default=lambda self: random.choice(['small', 'medium', 'large'])
        )

This is a trivial example, but it illustrates the point that the
callable will be called for every new object created.

When the ``default`` is called during object construction, it may be
called before other attributes have been set.  if your default is
dependent on other parts of the object's state, you can make the
attribute ``lazy``.

As an alternative to directly using a callable, you can supply a
``builder`` method for your attribute::

    class TeeShirt(elk.Elk):
        size = elk.ElkAttribute(builder='_build_size')

        def _build_size(self):
            return random.choice(['small', 'medium', 'large'])


This has several advantages.  First, it moves a chunk of code to its
own named method, which improves readability and separation of
concerns.  Second, because this is a *named* method, it can be
extended or overridden by a subclass.

It is strongly recommended to use a ``builder`` instead of a
``default`` for anything beyond the most trivial default.

A ``builder``, just like a ``default``, is called with the object as
the single argument.

Builders allow subclassing
^^^^^^^^^^^^^^^^^^^^^^^^^^

Because the ``builder`` is called *by name*, builder methods are
both inheritable and overridable.

If we subclass our our ``TeeShirt`` class, we can override
``_build_size``::

    class SmallTeeShirt(TeeShirt):
        def _build_size(self):
            return 'small'


Builders work well with roles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Because builders are called by name, they work well with
:doc:`roles`. For example, a role could provide an attribute but
require that the consuming class provide the builder::


    class HasSize(elk.ElkRole):
        size = elk.ElkAttribute(builder='_build_size')

    class Thing(elk.Elk):
        __with__ = HasSize

        def _build_size(self):
            return 'small'

.. TODO update example when "role requires" has been implemented


Laziness
--------

Elk lets you defer attribute population by making an attribute
``lazy``::

    class TeeShirt(elk.Elk):
        size = elk.ElkAttribute(builder='_build_size', lazy=True)

When ``lazy`` is true, the default is not generated until the
attribute is read, rather than at object construction time.  There
are several reasons why you might choose to do this:

* If the value depends on other attributes, then the attribute
  *must* be lazy because the order in which attribute values are set
  during object construction is not specified.
* Making an attribute ``lazy`` lets you defer the cost of computing
  its value until it is needed.  If the attribute is never read, you
  avoid doing the work at all.

It is recommended to make any attribute with a builder or
non-trivial default ``lazy`` as a matter of course.

Constructor parameters
----------------------

By default, each attribute can be passed by name to the class's
constructor. On occasion, you may want to use a different name for
the constructor parameter. You may also want to make an attribute
unsettable via the constructor.

You can do either of these things with the ``init_arg`` option::

    class TeeShirt(elk.Elk):
        bigness = elk.ElkAttribute(init_arg='size')


Now we have an attributed named ``"bigness"``, but we pass ``size``
to the constructor.

Even more useful is the ability to disable setting an attribute via
the constructor.  This is particularly handy for private
attributes::

    _genetic_code = elk.ElkAttribute(
        lazy=True,
        builder='_build_genetic_code',
        init_arg=None
    )

By setting the ``init_arg`` to ``None`` we make it impossible to set
this attribute when creating a new object.  Attempting to do so
raises ``TypeError``.


Type constraints
----------------

Attributes can be restricted to only accept certain types.  For
example, to restrict an attribute to strings::

    first_name = elk.ElkAttribute(type=str)


It is also possible to restrict values to one of a set of types by
specifying a ``tuple``::

    x = elk.ElkAttribute(type=(float, complex))

Constructing with or assigning a value of the wrong type will raise
``TypeError``.


Delegation
----------

An attribute can define names that will be added to the object and
will delegate to the attribute's value::

    color = elk.ElkAttribute(type=Color, handles=['as_hex_string'])

This will add the ``as_hex_string`` method to the object containing
the attribute, which when called will call ``as_hex_string`` on the
attribute value, as if ``obj.color.as_hex_string`` had been called.

You can delegate to methods, Elk attributes or regular attributes.
Attribute assignment and deletion works as normal through
delegations (even through multiple levels of delegation).

See :doc:`delegation` for documentation on how to set up delegation.


Attribute inheritance
=====================

A subclass inherits all of its base class(es)' attributes as-is.
However, you can override the inherited attribute.
