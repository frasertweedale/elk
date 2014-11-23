# This file is part of elk
# Copyright (C) 2012-2014  Fraser Tweedale
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

"""Convenience module for loading public API."""

from .attribute import AttributeDescriptor as ElkAttribute
from .meta import ElkRole, Elk
from .modifier import before, after, around

attr = ElkAttribute

__version__ = '0.2.1'
