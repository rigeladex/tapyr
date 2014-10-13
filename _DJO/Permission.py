# -*- coding: utf-8 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
        if isinstance (group, basestring) :
            self._group_name = group
        else :
            self._group = group
    # end def __init__

    @Once_Property
    def group (self) :
        from django.contrib.auth.models import Group
        return Group.objects.get (name = self._group_name)
    # end def group

    def predicate (self, user, page, * args, ** kw) :
        return self.group in user.groups.all ()
    # end def predicate

# end class In_Group

class In_Page_Group (_Permission_) :

    def predicate (self, user, page, * args, ** kw) :
        return page.Group in user.groups.all ()
    # end def predicate

# end class In_Page_Group

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
