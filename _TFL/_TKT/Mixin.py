# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.TKT.Mixin
#
# Purpose
#    Mixin for TFL.TKT classes
#
# Revision Dates
#    18-Jan-2005 (CT) Creation
#    20-Jan-2005 (CT) Setting of `TNS` streamlined
#    10-Mar-2005 (CT) `get_TNS` factored
#    10-Aug-2005 (CT) `set_TNS_name` added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL           import TFL
import _TFL._Meta.Object
import _TFL._TKT

class Mixin (TFL.Meta.Object) :
    """Mixin for TFL.TKT classes

       This mixin supplies two symbolic names for package name spaces:
       - ANS specifies the application specific PNS
       - TNS specifies the toolkit specific PNS

       Descendents should always use these attributes to refer to classes
       instead of using literal names for the package name spaces.
    """

    AC       = None     ### application context
    ANS      = TFL      ### application specific package name space
    TNS_name = None     ### toolkit     specific package name space

    def __init__ (self, AC = None, ** kw) :
        if AC is not None :
            self.AC  = AC
            self.ANS = AC.ANS
            self.TNS = self.get_TNS (AC)
        self.__super.__init__ (AC = AC, ** kw)
    # end def __init__

    @classmethod
    def get_TNS (cls, AC) :
        if cls.TNS_name is not None :
            result = getattr (AC.ANS, "TKT")
            for p in cls.TNS_name.split (".") :
                result = getattr (result, p)
            return result
    # end def get_TNS

    @classmethod
    def set_TNS_name (cls, name, override = None) :
        if (cls.TNS_name is None) or (cls.TNS_name == override) :
            cls.TNS_name = name
    # end def set_TNS_name

# end class Mixin

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Mixin
