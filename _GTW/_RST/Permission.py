# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.RST.
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
#    GTW.RST.Permission
#
# Purpose
#    Classes modelling permissions for accessing RESTful resources
#
# Revision Dates
#    16-Jan-2010 (CT) Creation
#    18-Jan-2010 (CT) `In_Page_Group` removed
#    26-Feb-2010 (CT) `Is_Superuser` added
#     8-Jun-2012 (CT) Add `Login_Required`, add guards for `user`
#    11-Jun-2012 (CT) Add `rank`
#    20-Jun-2012 (CT) Remove dependency on `GTW.NAV.Root.top`
#     5-Jul-2012 (CT) Move from `GTW.NAV` to `GTW.RST`
#    10-Aug-2012 (CT) Rename `rank` to `_rank`
#    14-Dec-2012 (CT) Remove `Login_Required`
#                     (use `login_required` argument to GTW.Resource instead)
#    14-Dec-2012 (CT) Adapt `Is_Creator` to changes of `MOM.Entity`
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _GTW                     import GTW

import _GTW._RST

import _TFL.Filter

class _Permission_ (TFL._.Filter._Filter_S_) :

    _rank = 0

# end class _Permission_

class In_Group (_Permission_) :
    """Permission if user is member of group"""

    def __init__ (self, name) :
        self.name = name
    # end def __init__

    def group (self, page) :
        scope = page.top.scope
        Group = scope ["Auth.Group"]
        return Group.instance (self.name)
    # end def group

    def predicate (self, user, page, * args, ** kw) :
        if user :
            group = self.group (page)
            return group in user.groups
    # end def predicate

# end class In_Group

class Is_Creator (_Permission_) :
    """Permission if user is the creator of the object associated with the resource"""

    def __init__ (self, attr_name = "created_by") :
        self.attr_name = attr_name
    # end def __init__

    def predicate (self, user, page, * args, ** kw) :
        obj = getattr (page, "obj", None)
        return user and obj and user == getattr (obj, self.attr_name, None)
    # end def predicate

# end class Is_Creator

class Is_Superuser (_Permission_) :

    def predicate (self, user, page, * args, ** kw) :
        return user and user.superuser
    # end def predicate

# end class Is_Superuser

if __name__ != "__main__":
    GTW.RST._Export ("*", "_Permission_")
### __END__ GTW.RST.Permission
