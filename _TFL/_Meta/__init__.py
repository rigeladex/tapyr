#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2001-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.Meta.__init__
#
# Purpose
#    `TFL.Meta` provides meta-classes and property-helpers
#
# Revision Dates
#    13-May-2002 (CT) Creation
#     2-Feb-2009 (CT) Documentation added
#     3-Feb-2009 (CT) Documentation added..
#     4-Feb-2009 (CT) Documentation added...
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TFL.Package_Namespace import Package_Namespace

Meta = Package_Namespace ()
TFL._Export ("Meta")

del Package_Namespace

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

`TFL.Meta` provides a generic base-class and various meta-classes and
property-helpers:

- New-style classes should be derived (directly or indirectly) from
  :class:`Object<_TFL._Meta.Object.Object>` instead of
  Python's builtin `object`.

- Classes derived from other builtin types (like `dict`, `list`,
  `set`, etc.) should declare their metaclass to be
  :class:`M_Class<_TFL._Meta.M_Class.M_Class>`.

- Metaclasses should be derived (directly or indirectly) from
  :class:`M_Base<_TFL._Meta.M_Class.M_Base>`
  (most commonly, from :class:`M_Class<_TFL._Meta.M_Class.M_Class>`).

Module `Object`
===============

.. automodule:: _TFL._Meta.Object
   :members:

Module `M_Class`
================

.. automodule:: _TFL._Meta.M_Class
   :members:

Module `M_Data_Class`
=====================

.. automodule:: _TFL._Meta.M_Data_Class
   :members:

Module `M_Auto_Combine`
=======================

.. automodule:: _TFL._Meta.M_Auto_Combine
   :members:

Module `Property`
=================

.. automodule:: _TFL._Meta.Property
   :members:


Module `Once_Property`
======================

.. automodule:: _TFL._Meta.Once_Property
   :members:

Module `Lazy_Method`
====================

.. automodule:: _TFL._Meta.Lazy_Method
   :members:

"""

### To use Sphinx for generating the documentation for TFL.Meta, one
### needs a file `index.rst` with the contents::

index_rst = """
Welcome to the `TFL.Meta` documentation!
========================================

.. toctree::
   :maxdepth: 2

Package-NS `TFL.Meta`
---------------------

.. automodule:: _TFL._Meta

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

### __END__ TFL.Meta.__init__
