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


*******
Classes
*******

Making a class with Elk is simple::

    import elk

    class Person(elk.Elk):
        ...


The ``elk.Elk`` base class simply ensures that your class uses the
Elk metaclass and—on its own—has no other functionality.

The Elk metaclass will notice when you are using Elk attributes,
roles or method modifiers and do some work to initialise your class
properly.  For example, you might define an :doc:`attribute
<attributes>`::

    class Person(elk.Elk):
        tfn = elk.ElkAttribute(mode='ro', type=str)


Subclassing
===========

Subclassing an Elk class is done in the usual way.  The metaclass
will be inherited from the base class::

    class User(Person):
        username = elk.ElkAttribute(mode='rw')
