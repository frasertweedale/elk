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


****************
Method Modifiers
****************

Elk provides a feature called "method modifiers".  You can also
think of these as "hooks" or "advice".

It's probably easiest to understand this feature with a few
examples::

    class Example(elk.Elk):
        def foo(self):
            print "    foo"

        @elk.before('foo')
        def _before_foo(self):
            print "about to call foo"

        @elk.after('foo')
        def _after_foo(self):
            print "just called foo"

        @elk.around('foo')
        def _around_foo(self, orig):
            print "  I'm around foo"
            orig()
            print "  I'm still around foo"


Calling ``Example().foo()`` will produce the following output::

  about to call foo
    I'm around foo
      foo
    I'm still around foo
  just called foo

As you can see, the ``before`` modifiers come before ``around``
modifiers, and ``after`` modifiers come last.

When there are multiple modifiers of the same type, the ``before``
and ``around`` modifiers run from the last added to the first, and
``after`` modifiers run from first added to last::

  before 2
   before 1
    around 2
     around 1
      primary
     around 1
    around 2
   after 1
  after 2


``before``, ``after`` and ``around``
====================================

Method modifiers can be used to add behavior to methods without
modifying the definition of those methods.

``before`` and ``after`` modifiers
----------------------------------

One use the ``before`` modifier would be to do some sort of
prechecking on a method call.  For example::

    def set_size(self, size):
        self.size = size

    @elk.before('set_size')
    def _before_set_size(self, size):
        if self.is_growing:
            raise AttributeError('cannot set size while person is growing')

Similarly, an ``after`` modifier could be used for logging an action
that was taken.

.. note::

  The name of the method modifier *must be unique*.  Beyond this the
  name is of little consequence, but it is recommended to begin with
  an underscore if it is not part of the class' public API (it
  probably isn't).

.. note::

  The return values of both ``before`` and ``after`` modifiers are
  ignored.

.. note::

  The method modifier must accept the same arguments as the original
  method.


``around`` modifiers
--------------------

An ``around`` modifier is more powerful than either a ``before`` or
``after`` modifier.  It can modify the arguments being passed to the
original method, and you can even decide to simply not call the
original method at all. You can also modify the return value with an
``around`` modifier.

An ``around`` modifier receives the original method as the first
positional argument after ``self``.  By convention, the original
method is referred to as ``orig``::

    @elk.around('set_size')
    def _around_set_size(self, orig, size):
        if self.likes_small_things():
            size /= 2
        return orig(size)

.. note::

  ``orig`` is a *bound method*, meaning that it is called directly
  without passing ``self`` as the first argument.
