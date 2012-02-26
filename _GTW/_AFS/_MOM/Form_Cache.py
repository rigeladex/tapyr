# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.MOM.Form_Cache
#
# Purpose
#    Handling of AFS form caching
#
# Revision Dates
#     1-Feb-2012 (CT) Creation (factored from GTW.AFS.MOM.Element.Form)
#     1-Feb-2012 (CT) Add `Extra`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _TFL                   import TFL

from   _GTW._AFS._MOM.Element import Form

import _TFL._Meta.Object

class Extra (TFL.Meta.Object) :
    """Specification for an extra, i.e., non-automatically generated, AFS
       form.
    """

    def __init__ (self, fid, * entities) :
        assert entities, "Need at least one entity for Extra"
        self.fid      = fid
        self.entities = entities
    # end def __init__

    def __call__ (self, app_type) :
        return Form (self.fid, children = list (self._gen_children (app_type)))
    # end def __call__

    def _gen_children (self, app_type) :
        for e in self.entities :
            if isinstance (e, basestring) :
                name = e
                spec = None
                kw   = {}
            elif isinstance (e, dict) :
                name = e ["name"]
                spec = e.get ("spec")
                kw   = e.get ("kw", {})
            else :
                name = e.name
                spec = getattr (e, "spec")
                kw   = getattr (e, "kw", {})
            T = app_type [name]
            S = spec or T.GTW.afs_spec
            yield S (T, ** kw)
    # end def _gen_children

# end class Extra

class _Form_Cache_ (TFL.Meta.Object) :
    """Handle cache for AFS forms"""

    cache_rank = -500

    def __init__ (self) :
        self._extras = []
    # end def __init__

    def add (self, * extras) :
        self._extras.extend (extras)
    # end def add

    def as_pickle_cargo (self, nav_root) :
        if not Form.Table :
            ### mustn't do this more than once
            app_type = nav_root.App_Type
            self._create_auto_forms  (app_type)
            self._create_extra_forms (app_type)
        return dict (AFS_Form_Table = Form.Table)
    # end def as_pickle_cargo

    def from_pickle_cargo (self, nav_root, cargo) :
        table = cargo.get ("AFS_Form_Table", {})
        table.update      (Form.Table)
        ### We want to set `Table` for `GTW.AFS.Element.Form`, not for a
        ### possible descedent class
        GTW.AFS.Element.Form.Table = table
    # end def from_pickle_cargo

    def _create_auto_forms (self, app_type) :
        for T in app_type._T_Extension :
            if T.GTW.afs_id is not None and T.GTW.afs_spec is not None :
                Form (T.GTW.afs_id, children = [T.GTW.afs_spec (T)])
    # end def _create_auto_forms

    def _create_extra_forms (self, app_type) :
        for e in self._extras :
            e (app_type)
    # end def _create_extra_forms

# end class _Form_Cache_

Form_Cache = _Form_Cache_ ()

if __name__ != "__main__" :
    GTW.AFS.MOM._Export ("*")
### __END__ GTW.AFS.MOM.Form_Cache
