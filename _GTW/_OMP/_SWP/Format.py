# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SWP.
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
#    GTW.OMP.SWP.Formatter
#
# Purpose
#    Provide formatter objects for different markup types
#
# Revision Dates
#    31-Jan-2010 (CT) Creation
#     2-Feb-2010 (CT) Creation continued
#    ««revision-date»»···
#--

### To-do:
# - markdown

from   _GTW                   import GTW
from   _TFL                   import TFL

from   _MOM.import_MOM        import *

import _GTW._OMP._SWP
import _GTW.ReST

import _TFL._Meta.Object

class M_Format (TFL.Meta.Object.__class__) :
    """Meta class for formatter classes"""

    Table = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "_Format_" :
            cls._m_add (name,     cls.Table)
    # end def __init__

    def _m_add (cls, name, Table) :
        assert name not in Table, "Name clash: `%s` <-> `%s`" % \
            (name, Table [name].__class__)
        Table [name] = cls
    # end def _m_add

# end class M_Format

class _Format_ (TFL.Meta.Object) :

    __metaclass__ = M_Format

# end class _Format_

class HTML (_Format_) :
    """Formatter for text in HTML markup"""

    forbidden = "applet frame frameset head html iframe input object script"

    @classmethod
    def convert (cls, text) :
        ### XXX remove tags listed in `forbidden`
        return text
    # end def convert

# end class HTML

class ReST (_Format_) :
    """Formatter for re-structured text"""

    @classmethod
    def convert (cls, text) :
        return GTW.ReST.to_html (text, encoding = "utf8")
    # end def convert

# end class ReST

class Markdown (_Format_) :
    """Formatter for text in `Markdown` markup"""

    MD = None

    @classmethod
    def convert (cls, text) :
        if cls.MD is None :
            import markdown
            cls.MD = markdown.Markdown ()
        return cls.MD.convert (text)
    # end def convert

# end class Markdown

class A_Format (MOM.Attr._A_Named_Object_) :
    """Format to use for text of a page"""

    typ         = "Format"
    Table       = M_Format.Table

# end class A_Format

if __name__ != "__main__" :
    GTW.OMP.SWP._Export_Module ()
### __END__ GTW.OMP.SWP.Formatter
