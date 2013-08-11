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
Delegation
**********

What is delegation?
===================

Delegation is a feature that lets you create "proxy" attributes that
do nothing more than access some other attribute or method on an
attribute.  This lets you simplify a complex set of "has-a"
relationships and present a single unified API from one class.

With delegation, consumers of a class don't need to know about all
the objects it contains, reducing the amount of API they need to
learn.

Delegations are defined as a mapping between one or more attributes
provided by the "real" class (the *delegatee*), and a set of
corresponding attributes in the delegating class. The delegating
class can re-use the attribute names provided by the delegatee or
provide its own names.

Delegation is also a great way to wrap an existing class, especially
a non-Elk class or one that is somehow hard (or impossible) to
subclass.


Defining delegations
====================

Elk offers a couple of ways to define delegations.

The simplest form is to simply specify a sequence of attribute
names::

    class Website(elk.Elk):
        uri = elk.ElkAttribute(
            type=URI,
            handles=['host', 'path']
        )

With this definition, we can read ``website.host`` and it "just
works".  Under the hood, Elk will read ``website.uri.host`` for you.

.. note::

  Methods accessed through delegations are bound to the *delegatee*.


Delegations can also be declared with a mapping type, allowing
attribute renaming::

    class Website(elk.Elk):
        uri = elk.ElkAttribute(
            type = URI,
            handles={'hostname': 'host', 'path': 'path'}
        )

This examples creates a a ``website.hostname`` attribute rather than
using the name of the URI attribute, ``host``.


Missing attributes
==================

It is perfectly valid to delegate to attributes that are not
required and therefore may be undefined.  Elk will raise
``AttributeError`` when this situation occurs at runtime.
