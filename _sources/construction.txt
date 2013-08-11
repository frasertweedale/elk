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


************
Construction
************

Where's the constructor?
========================

**Do not define an __init__ method for your classes!**

Subclasses of ``elk.Elk`` are automatically initialised by the Elk
metaclass.  Use the `__build__`_ hook for post-construction
validation or behaviour.


Object construction and attributes
==================================

Elk classes accept keyword arguments matching your attributes
(actually, matching their ``init_arg``).  You don't need to worry
about setting attributes yourself—simply define a class and you're
ready to start creating objects.


Object construction hooks
=========================

Elk lets you hook into object construction.  You can validate an
object's state, do logging or customise construction from parameters
which do not match your attributes by defining the ``__buildargs__``
and/or ``__build__`` methods.

If your Elk class defines these methods, the Elk metaclass will
arrange for them to be called as part of the object construction
process.


``__buildargs__``
-----------------

The ``__buildargs__`` method is called as a class method *before* an
object is created.  It will receive all of the positional and
keyword arguments that were passed to the constructor *as-is*, and
must return a ``dict``.  The ``dict`` will be used to construct the
object, so it should contain keys matching your attributes' names
(or ``init_arg``).

One common use for ``__buildargs__`` is to accomodate a non-keyword
args calling style.  For example, we might want to allow our
``Person`` class to be called with a single positional argument, the
Tax File Number::

    Person(tfn)

A ``__buildargs__`` method can be used to accomodate this calling
style::

    class Person(elk.Elk):
        tfn = elk.ElkAttribute()

        @classmethod
        def __buildargs__(cls, *args, **kwargs):
            if len(args) == 1:
                kwargs['tfn'] = args[0]
            return kwargs

.. note::

  Without a ``__buildargs__`` method, Elk will raise ``TypeError``
  if positional arguments are passed.


``__build__``
-------------

The ``__build__`` method is called *after* an object is created.
There are several reasons to use a ``__build__`` method.  One of the
most common is to check that the object state is valid.  While we
can validate individual attributes through type constraints, we
can't validate the state of a whole object that way.

::

    def __build__(self, **kwargs):
        if self.country_of_residence == 'AUS' and not hasattr(self, 'tfn'):
            raise RuntimeError('AUS residents must have a Tax File Number')


Another use of a ``__build__`` method could be for logging or
tracking object creation::

    def __build__(self, **kwargs):
        logger.debug('Made a new Person; tfn={}'.format(self.tfn))


The ``__build__`` method is called with the parameters passed to the
constructor (after munging by ``__buildargs__``).  This gives you a
chance to do something with parameters that do not represent object
attributes::


    def __build__(self, **kwargs):
        self.add_friend(User(user_id=kwargs['user_id']))


.. note::

  The default ``__build__`` method raises ``TypeError`` if any
  arguments are received that do not correspond to Elk
  attributes::

    class Person(elk.Elk):
        tfn = elk.ElkAttribute()

    person = Person(tfn='123456789', name='Bob')  # raises TypeError
