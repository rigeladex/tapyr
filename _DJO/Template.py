# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Template
#
# Purpose
#    Model django templates
#
# Revision Dates
#    13-Jul-2009 (CT) Creation
#    14-Jul-2009 (CT) `parent` and `uses` added to `Template`
#    ««revision-date»»···
#--

from   _TFL                               import TFL
from   _DJO                               import DJO

import _TFL._Meta.Object

class M_Template (TFL.Meta.M_Class) :
    """Meta class for `Template`"""

    Table = {}

    def __call__ (cls, name, * args, ** kw) :
        if name in cls.Table :
            result = cls.Table [name]
        else :
            result = cls.Table [name] = cls.__m_super.__call__ \
                (name, * args, ** kw)
        return result
    # end def __call__

    def Copy (cls, proto) :
        return cls.__m_super.__call__ (proto.name)
    # end def Copy

    def __getattr__ (cls, name) :
        try :
            return cls.Table [name]
        except KeyError :
            raise AttributeError, name
    # end def __getattr__

    def __getitem__ (cls, key) :
        return cls.Table [key]
    # end def __getitem__

# end class M_Template

class Template (TFL.Meta.Object) :
    """Model a django template.

       >>> t1 = Template ("field_group_horizontal.html")
       >>> t2 = Template ("field_group_horizontal.html")
       >>> t1 is t2
       True
       >>> print t1
       field_group_horizontal.html
       >>> print Template ["field_group_horizontal.html"]
       field_group_horizontal.html
       >>> Template ["field_group_horizontal.html"] is t2
       True
    """

    __metaclass__  = M_Template

    def __init__ (self, name, Media = None, parent = None, uses = ()) :
        import _DJO.Media
        medias      = tuple \
            (   m
            for m in
              ( (getattr (parent, "Media", None), Media)
              + tuple (u.Media for u in uses)
              )
            if  m is not None
            )
        if medias :
            Media   = DJO.Media (children = medias)
        self.name   = name
        self.Media  = Media
        self.parent = parent
        self.uses   = uses
    # end def __init__

    def copy (self, Media) :
        result        = self.__class__.Copy (self)
        result.parent = self
        result.Media  = DJO.Media (children = (self.Media, Media))
        return result
    # end def copy

    def __repr__ (self) :
        return self.name
    # end def __repr____

    def __str__ (self) :
        return self.name
    # end def __str__

    def __unicode__ (self) :
        return unicode (self.name)
    # end def __unicode__

# end class Template

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.Template
