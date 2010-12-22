# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.
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
#    GTW.NAV.E_Type.Site_Admin
#
# Purpose
#    Model an admin page for a GTW site
#
# Revision Dates
#     8-Jan-2010 (CT) Moved from DJO to GTW
#    18-Jan-2010 (CT) Surgery
#    25-Jan-2010 (CT) `rendered` changed to take `handler` instead of `context`
#     5-Mar-2010 (CT) `_etype_man_entries` corrected
#    15-Mar-2010 (CT) `kind_name` removed
#    23-Jun-2010 (MG) `Site_Admin.__init__` changed to not require a scope
#     5-Aug-2010 (CT) `_filter_etype_entries` added
#     5-Aug-2010 (CT) Work on `man.admin_args.copy ()` instead of
#                     `man.admin_args` (`pop` being as destructive as it is)
#    16-Dec-2010 (CT) Redefine `delegate_view_p` instead of bypassing
#                     `__super.rendered`
#    16-Dec-2010 (CT) s/Admin/Site_Admin/
#    22-Dec-2010 (CT) `top.E_Types` replaced by `ET_Map`
#    22-Dec-2010 (CT) Assignment to `top.Admin` removed
#    22-Dec-2010 (CT) Moved from `GTW.NAV` to `GTW.NAV.E_Type`
#    22-Dec-2010 (CT) `Admin_Group` factored, `Admin_Group._pns_entries` added
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type.Admin

from   _TFL._Meta.Once_Property import Once_Property

from   itertools import chain as ichain, repeat as irepeat

class Admin_Group (GTW.NAV.Dir) :
    """Model a group of E-Type admin pages."""

    delegate_view_p = False
    Page            = GTW.NAV.E_Type.Admin
    template        = "site_admin" ### XXX wrong name

    """
        [   str (T.type_base_name)
        for T in scope.app_type.etypes_by_pns ['GTW.OMP.Auth']
        if T.is_relevant and not T.electric.default)
        ]

    """

    def __init__ (self, src_dir, parent, ** kw) :
        entries = self._filter_etype_entries \
            (kw.pop ("etypes", []), self._pns_entries (* kw.pop ("PNSs", [])))
        self.__super.__init__ (src_dir, parent, ** kw)
        self.add_entries      (entries)
        self._entries.sort    (key = TFL.Getter.short_title)
    # end def __init__

    def _filter_etype_entries (self, * args) :
        seen = set ()
        for d in ichain (* args) :
            try :
                etm = d ["ETM"]
            except KeyError :
                print "No `ETM`\n   ", sorted (d.iteritems ())
            else :
                if etm not in seen :
                    seen.add (etm)
                    yield d
    # end def _filter_etype_entries

    def _pns_entries (self, * pnss) :
        app_type = self.top.scope.app_type
        for pns in pnss :
            for T in app_type.etypes_by_pns [pns] :
                if T.is_relevant and not T.electric.default :
                    if T.admin_args :
                        yield T.admin_args
    # end def _pns_entries

# end class Admin_Group

class Site_Admin (Admin_Group) :
    """Model an admin page for a GTW site."""

    def _etype_man_entries (self) :
        for et in self.top.ET_Map.itervalues () :
            man = et.manager
            if man is not None and et.admin is None :
                m_kw        = man.admin_args.copy ()
                short_title = m_kw.pop ("short_title", man.short_title)
                title       = m_kw.pop \
                    ("title", "%s: %s" % (self.title, man.name))
                ETM         = m_kw.pop ("ETM", man._ETM)
                Type        = m_kw.pop ("Type", self.Page)
                d           = dict \
                    ( name        = man.name
                    , short_title = short_title
                    , title       = title
                    , ETM         = ETM
                    , Type        = Type
                    , ** m_kw
                    )
                yield d
    # end def _etype_man_entries

    def _filter_etype_entries (self, * args) :
        return self.__super._filter_etype_entries \
            (self._etype_man_entries (), * args)
    # end def _filter_etype_entries

# end class Site_Admin

if __name__ != "__main__":
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Site_Admin
