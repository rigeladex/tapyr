# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.CSS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.CSS.Style_Sheet
#
# Purpose
#    Model a CSS style sheet
#
# Revision Dates
#    29-Dec-2010 (CT) Creation
#     1-Jan-2011 (CT) `Eval` added
#     2-Jan-2011 (CT) `_Eval` factored
#     3-Jan-2011 (CT) `rank` added
#    14-Jan-2011 (CT) `Parameter_Scope` changed to `import_CSS.__dict__` as
#                     object
#    14-Jan-2011 (CT) `Parameter_Scope` moved to `GTW.Parameters.Scope`
#    14-Jan-2011 (CT) `Eval` and `Read` removed (done by JNJ.Templateer now)
#    13-Sep-2011 (CT) `Style_File` added
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._CSS.Media

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.Filename

class M_Style_Sheet (TFL.Meta.Object.__class__) :
    """Meta class for `Style_Sheet`"""

# end class M_Style_Sheet

class _Style_Sheet_ (TFL.Meta.Object) :

    __metaclass__ = M_Style_Sheet

    name          = None
    rank          = 0

    def __init__ (self, media = None, ** kw) :
        self.media = media or GTW.CSS.Media.Type ("all")
        self.__dict__.update (kw)
    # end def __init__

# end class _Style_Sheet_

class Style_Sheet (_Style_Sheet_) :
    """Model a CSS style sheet"""

    _CSS_globs    = {}

    def __init__ (self, * rules, ** attrs) :
        self.__super.__init__ \
            ( attrs   = attrs
            , imports = list (attrs.pop ("imports", []))
            , media   = attrs.pop ("media", None)
            , name    = attrs.pop ("name",  None)
            , rank    = attrs.pop ("rank",  0)
            , rules   = list (rules)
            )
    # end def __init__

    def add_import (self, * imports) :
        self.imports.extend (imports)
    # end def add_import

    def add_rule (self, * rules) :
        self.rules.extend (rules)
    # end def add_rule

    def __iter__ (self) :
        for i in self.imports :
            for r in i :
                yield r
        for r in self.rules :
            for x in r :
                yield x
    # end def __iter__

    def __str__ (self) :
        return "\n\n".join (str (r) for r in self)
    # end def __str__

# end class Style_Sheet

class Style_File (_Style_Sheet_) :
    """Model a style file containing plain old CSS."""

    def __init__ (self, file_name, ** kw) :
        self.__super.__init__ \
            ( file_name = file_name
            , name      = kw.pop ("name", None) or TFL.Filename (file_name).base
            , ** kw
            )
    # end def __init__

    @TFL.Meta.Once_Property
    def body (self) :
        with open (self.file_name, "rb") as f :
            return f.read ().strip ()
    # end def body

    def __str__ (self) :
        return self.body
    # end def __str__

# end class Style_File

S = Style_Sheet

__all__ = tuple \
    ( k for (k, v) in globals ().iteritems () if isinstance (v, M_Style_Sheet)
    )

if __name__ != "__main__" :
    GTW.CSS._Export (* __all__)
### __END__ GTW.CSS.Style_Sheet
