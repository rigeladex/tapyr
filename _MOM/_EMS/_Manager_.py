# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
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
#    MOM.EMS._Manager_
#
# Purpose
#    Base class for entity manager strategies
#
# Revision Dates
#     2-Dec-2009 (CT) Creation
#     3-Dec-2009 (CT) `count` simplified
#     4-Dec-2009 (MG) `__init__` changed to support database related
#                     parameter and to create the `session`
#    10-Dec-2009 (CT) Class methods `connect` and `new` added,
#                     `__init__` revamped
#    10-Dec-2009 (CT) Empty methods `load_scope` and `register_scope` added
#    14-Dec-2009 (CT) `__iter__` (and relevant_roots) added
#    16-Dec-2009 (MG) Add `scope` parameter to `DWB.create_database` and
#                     `DBW.connect_database`
#    16-Dec-2009 (CT) `pid_query` added
#    16-Dec-2009 (CT) `commit`, `register_change`, and `uncommitted_changes`
#                     added
#    17-Dec-2009 (CT) `async_changes` added
#    17-Dec-2009 (CT) `pid_query` fixed (needs to call `one`)
#    21-Dec-2009 (CT) s/load_scope/load_root/
#    21-Dec-2009 (CT) `relevant_roots` factored to `MOM.Scope`
#    21-Dec-2009 (CT) `commit` changed to update `scope.db_cid`
#    21-Dec-2009 (CT) `close` added
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.Q_Result

from   _TFL.I18N             import _, _T, _Tn

import itertools

class _Manager_ (TFL.Meta.Object) :
    """Base class for entity managers."""

    type_name          = "XXX"

    Q_Result           = TFL.Q_Result
    Q_Result_Composite = TFL.Q_Result_Composite

    @classmethod
    def connect (cls, scope, db_uri) :
        self         = cls (scope, db_uri)
        self.session = self.DBW.connect_database (db_uri, scope)
        return self
    # end def connect

    @classmethod
    def new (cls, scope, db_uri) :
        self         = cls (scope, db_uri)
        self.session = self.DBW.create_database (db_uri, scope)
        return self
    # end def new

    def __init__ (self, scope, db_uri) :
        self.scope               = scope
        self.db_uri              = db_uri
        self.DBW                 = scope.app_type.DBW
        self.uncommitted_changes = []
    # end def __init__

    def async_changes (self, * filters, ** kw) :
        from _MOM.import_MOM import Q
        result = self.changes (Q.cid > self.scope.db_cid)
        if filters or kw :
            result = result.filter (* filters, ** kw)
        return result
    # end def changes

    def close (self) :
        if self.uncommitted_changes :
            self.commit ()
        self.session.close ()
    # end def close

    def commit (self) :
        self.scope.db_cid = self.max_cid
        self.session.commit ()
        self.uncommitted_changes = []
    # end def commit

    def count (self, Type, strict) :
        return self.query (Type, strict = strict).count ()
    # end def count

    def exists (self, Type, epk) :
        epk_dict = dict (zip (Type.epk_sig, epk))
        entities = self.query (Type).filter (** epk_dict)
        scope    = self.scope
        result   = list (getattr (scope, e.type_name) for e in entities)
        return result
    # end def exists

    def instance (self, Type, epk) :
        root = Type.relevant_root
        if root :
            epk_dict = dict (zip (Type.epk_sig, epk))
            try :
                result = self.query (Type).filter (** epk_dict).one ()
            except IndexError :
                result = None
            else :
                if not isinstance (result, Type.Essence) :
                    result = None
            return result
        raise TypeError \
            ( "\n".join
                ( ( _T ("Cannot query `instance` of non-root type `%s`.")
                  , _T ("Use one of the types %s instead.")
                  )
                )
            % (Type.type_name, ", ".join (sorted (Type.relevant_roots)))
            )
    # end def instance

    def load_root (self) :
        """Redefine to load `guid`, `pid`, and `root` of scope from database."""
        raise NotImplementedError
    # end def load_root

    def pid_query (self, pid, Type) :
        """Redefine if optimization is possible for a specific EMS/DBW."""
        return self.query (Type, pid = pid).one ()
    # end def pid_query

    def query (self, Type, * filters, ** kw) :
        root   = Type.relevant_root
        strict = kw.pop ("strict", False)
        if root :
            result = self._query_single_root (Type, root)
        else :
            result = self._query_multi_root (Type)
        if filters or kw :
            result = result.filter (* filters, ** kw)
        if strict :
            result = result.filter (type_name = Type.type_name)
        return result
    # end def query

    def r_query (self, Type, rkw, * filters, ** kw) :
        return self.query (Type, * filters, ** dict (rkw, ** kw))
    # end def r_query

    def register_change (self, change) :
        if change.parent is None :
            self.uncommitted_changes.append (change)
        if change.user is None :
            change.user = self.scope.user
    # end def register_change

    def register_scope (self) :
        """Redefine to store `guid` and `root`-info of scope in database."""
        pass
    # end def register_scope

    def _query_multi_root (self, Type) :
        raise NotImplementedError \
            ("%s needs to define %s" % (self.__class__, "_query_multi_root"))
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        raise NotImplementedError \
            ("%s needs to define %s" % (self.__class__, "_query_single_root"))
    # end def _query_single_root

    def __iter__ (self) :
        sk = TFL.Sorted_By ("pid")
        return itertools.chain \
            (* (   self._query_single_root (r, r).order_by (sk)
               for r in self.scope.relevant_roots
               )
            )
    # end def __iter__

# end class _Manager_

if __name__ != "__main__" :
    MOM.EMS._Export ("_Manager_")
### __END__ MOM.EMS._Manager_
