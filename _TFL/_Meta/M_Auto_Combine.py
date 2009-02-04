# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.M_Auto_Combine
#
# Purpose
#    Metaclass for autocombining lists, dictionaries and sets between a class
#    and its ancestors
#
# Revision Dates
#    13-Jan-2003 (CT)  Creation (factored from TOM.Meta.ATS_Type.py)
#     4-Feb-2003 (CT)  `_lists_to_combine` moved to `ATS_Type`
#    20-Feb-2003 (CT)  `_dicts_to_combine` added
#    20-Feb-2003 (CT)  Empty defaults for `_lists_to_combine` and
#                      `_dicts_to_combine` added
#     1-Apr-2003 (CT)  s/M_Class/M_Class_SW/ (optimize, optimize)
#     7-Jul-2003 (CED) `_m_combine_lists` fixed
#    23-Jul-2004 (CT)  `TFL.Meta.M_Auto_Combine_Dicts` and
#                      `TFL.Meta.M_Auto_Combine_Lists` factored
#    18-Feb-2005 (CT)  Moved to `TFL.Meta`
#    13-Jul-2005 (CED) `M_Auto_Combine_Sets` added to bases
#    13-Jul-2005 (CED) Missing import added
#     3-Feb-2009 (CT)  Documentation added
#    ««revision-date»»···
#--

from   _TFL                import TFL

import _TFL._Meta.M_Auto_Combine_Dicts
import _TFL._Meta.M_Auto_Combine_Lists
import _TFL._Meta.M_Auto_Combine_Sets
import _TFL._Meta.M_Class

class M_Auto_Combine ( TFL.Meta.M_Auto_Combine_Dicts
                     , TFL.Meta.M_Auto_Combine_Lists
                     , TFL.Meta.M_Auto_Combine_Sets
                     , TFL.Meta.M_Class
                     ) :
    """Meta class for auto-combining

       * the list-attributes mentioned in `_lists_to_combine`
         (see :class:`~_TFL._Meta.M_Auto_Combine_Lists.M_Auto_Combine_Lists`)
       * the dict-attributes mentioned in `_dicts_to_combine`
         (see :class:`~_TFL._Meta.M_Auto_Combine_Dicts.M_Auto_Combine_Dicts`)
       * the set-attributes  mentioned in `_sets_to_combine`
         (see :class:`~_TFL._Meta.M_Auto_Combine_Sets.M_Auto_Combine_Sets`)

       between a class and its ancestors.

       Module `M_Auto_Combine_Dicts`
       =============================

       .. automodule:: _TFL._Meta.M_Auto_Combine_Dicts
          :members:

       Module `M_Auto_Combine_Lists`
       =============================

       .. automodule:: _TFL._Meta.M_Auto_Combine_Lists
          :members:

       Module `M_Auto_Combine_Sets`
       ============================

       .. automodule:: _TFL._Meta.M_Auto_Combine_Sets
          :members:

    """
# end class M_Auto_Combine

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.M_Auto_Combine
