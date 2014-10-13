# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.Day_Column
#
# Purpose
#    Colum with a special header widget
#
# Revision Dates
#    18-Dec-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Tree_View_Column

class Day_Column (GTK.Tree_View_Column) :
    """Colum with a special header widget"""

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        #self._label = self.TNS.Label (self.title)
        #self._label.show             ()
        #self.widget = self._label
    # end def __init__

# end class Day_Column

if __name__ != "__main__" :
    GTK._Export ("Day_Column")
### __END__ TGL.TKT.GTK.Day_Column
