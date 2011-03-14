# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.Meta.M_Auto_Combine_Nested_Classes
#
# Purpose
#    Meta class for auto-combining the class-valued attributes mentioned in
#    `_nested_classes_to_combine` between a class and it's ancestors.
#
# Revision Dates
#    10-Feb-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                import TFL
import _TFL._Meta.M_Class

class M_Auto_Combine_Nested_Classes (TFL.Meta.M_Base) :
    """Meta class for auto-combining the class-valued attributes mentioned in
       `_nested_classes_to_combine` between a class and it's ancestors.
    """

    _nested_classes_to_combine = ()

    def __init__ (cls, name, bases, dct) :
        for cn in cls._nested_classes_to_combine :
            cls._m_combine_nested_class (cn, bases, dct)
        cls.__m_super.__init__ (name, bases, dct)
    # end def __init__

# end class M_Auto_Combine_Nested_Classes

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.M_Auto_Combine_Nested_Classes
