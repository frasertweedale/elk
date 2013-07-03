Synopsis
--------

::

    import elk


    class Point(elk.Elk):
        x = elk.ElkAttribute(mode='rw', type=int)
        y = elk.ElkAttribute(mode='rw', type=int)

        def clear(self):
            self.x = 0
            self.y = 0


    class Point3D(Point):
        z = elk.ElkAttribute(mode='rw', type=int)

        @elk.after('clear')
        def clear_z(self):
            self.z = 0


What is Elk?
------------

Elk (homepage_) is an object system for Python inspired by Moose_
for Perl.  It implements many of the features of Moose including:

* attribute delegation
* default attribute values
* lazy attribute initialisation
* read-only attributes
* required attributes
* attribute type constraints
* roles
* method modifiers

.. _homepage: http://frasertweedale.github.io/elk
.. _Moose: https://metacpan.org/module/Moose

Elk is written in pure Python and there are no dependencies beyond
the standard library.


How does Elk differ from Moose?
-------------------------------

Moose has many features that are not (yet) implemented in Elk.

While Elk tries to faithfully implement Moose paradigms and patterns
in Python, it uses Python idioms and language features as much as
possible.  There are also some differences in terminology in order
to be consistent with Python terminology or idioms.

There is not yet a namespace for Elk extensions, nor any convenient
mechanism for extending it.


Installation
------------

::

    pip install elk


License
-------

Elk is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.


Contributing
------------

The Elk source code is available from
https://github.com/frasertweedale/elk.

Bug reports, patches, feature requests, code review and
documentation are welcomed.

To submit a patch, please use ``git send-email`` or generate a pull
request.  Write a `well formed commit message`_.  If your patch is
nontrivial, update the copyright notice at the top of each changed
file.

.. _well formed commit message: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
