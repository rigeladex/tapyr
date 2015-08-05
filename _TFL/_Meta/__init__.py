# -*- coding: utf-8 -*-
# Copyright (C) 2001-2015 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    14-Oct-2013 (CT) Add `Single_Dispatch`
#     5-Aug-2015 (CT) Add `M_Auto_Update_Combined`
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

Module `M_Auto_Update_Combined`
================================

.. automodule:: _TFL._Meta.M_Auto_Update_Combined
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

Module `Mixin_NS`
====================

.. automodule:: _TFL._Meta.Mixin_NS
   :members:

Module `Single_Dispatch`
=========================

.. automodule:: _TFL._Meta.Single_Dispatch
   :members:

Module `totally_ordered`
=========================

.. automodule:: _TFL._Meta.totally_ordered
   :members:

"""

### __END__ TFL.Meta.__init__
