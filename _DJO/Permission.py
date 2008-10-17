# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Permission
#
# Purpose
#    Classes modelling permissions for accessing Navigation objects
#
# Revision Dates
#    17-Oct-2008 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _DJO                     import DJO

from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Filter

class _Permission_ (TFL._.Filter._Filter_S_) :

    pass

# end class _Permission_

class Has_Permission (_Permission_) :

    def __init__ (self, * perms) :
        self.perms = perms
    # end def __init__

    def predicate (self, user, page, * args, ** kw) :
        return user.has_perms (self.perms)
    # end def predicate

# end class Has_Permission

class In_Group (_Permission_) :
    """Permission if user is member of group"""

    _group_name = None
    _group      = None

    def __init__ (self, group) :
        self.__super.__init__ ()
        if isinstance (group, basestring) :
            self._group_name = group
        else :
            self._group = group
    # end def __init__

    @Once_Property
    def group (self) :
        result = self._group
        if not result :
            from django.contrib.auth.models import Group
            self._group = result = Group.objects.get (name = self._group_name)
        return result
    # end def group

    def predicate (self, user, page, * args, ** kw) :
        return self.group in user.groups
    # end def predicate

# end class In_Group

class Is_Creator (_Permission_) :

    def __init__ (self, attr_name = "creator") :
        self.attr_name = attr_name
    # end def __init__

    def predicate (self, user, page, * args, ** kw) :
        return user == getattr (page.obj, self.attr_name, None)
    # end def predicate

# end class Is_Creator

class Is_Staff (_Permission_) :
    """Permission if user is staff"""

    def predicate (self, user, page, * args, ** kw) :
        return user.is_staff
    # end def predicate

# end class Is_Staff

class Is_Superuser (_Permission_) :
    """Permission if user is superuser"""

    def predicate (self, user, page, * args, ** kw) :
        return user.is_superuser
    # end def predicate

# end class Is_Superuser

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.Permission
