# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.EMS.SA
#
# Purpose
#    Entity manager strategy using SQLAlchemy session as storeage
#
# Revision Dates
#    16-Oct-2009 (MG) Creation
#    25-Oct-2009 (MG) Updated to support inheritance
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS._Manager_
import _MOM.Entity
import _MOM._DBW._SA.Sorted_By
import _TFL._Meta.Object

import _TFL.defaultdict

import itertools

from   sqlalchemy import exc as SA_Exception

class Manager (MOM.EMS._Manager_) :
    """Entity manager using hash tables to hold entities."""

    type_name = "SA"

    @TFL.Meta.Once_Property
    def session (self) :
        return self.scope.dbw.session
    # end def session

    def add (self, entity) :
        ses = self.session
        ses.flush () ### add all pending operations to the database transaction
        max_c = entity.max_count
        if max_c and max_c <= self.s_count (entity.Essence) :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        try :
            ses.add   (entity)
            ses.flush ()
        except SA_Exception.IntegrityError as exc :
            ses.rollback ()
            raise MOM.Error.Name_Clash \
                (entity, self.instance (entity.__class__, entity.epk))
        ### XXX how to handle Roles ???
        ### if entity.Roles :
        ###     r_map = self._r_map
        ###     for r in entity.Roles :
        ###         r_map [r] [r.get_role (entity).id].add (entity)
    # end def add

#    def exists (self, Type, epk) :
#        if not isinstance (epk, (tuple, list)) :
#            epk = (epk, )
#        scope     = self.scope
#        Type      = getattr (Type, "_etype", Type)
#        ses       = self.session
#        if Type.relevant_root :
#            queries = (Type, )
#        else :
#            queries = Type.relevant_roots.itervalues ()
#        result = []
#        for Type in queries :
#            result.extend \
#                (     getattr (scope, e.type_name)
#                for e in ses.query (Type)
#                            .filter_by (** dict (zip (Type.epk_sig, epk)))
#                )
#        return result
#
#    def instance (self, Type, epk) :
#        if isinstance (Type, basestring) :
#            Type = getattr (self.scope, Type)
#        Type = getattr (Type, "_etype", Type)
#        root = Type.relevant_root
#        if root :
#            epk_dict = dict (zip (Type.epk_sig, epk))
#            return self.session.query (Type).filter_by (** epk_dict).first ()
#        raise TypeError \
#            ( "Cannot query `instance` of non-root type `%s`."
#              "\n"
#              "Use one of the types %s instead."
#            % (Type.type_name, ", ".join (sorted (Type.relevant_roots)))
#            )
#    # end def instance

    def remove (self, entity) :
        self.session.delete (entity)
        self.session.flush  ()
        ### if entity.Roles :
        ###     r_map = self._r_map
        ###     for r in entity.Roles :
        ###         r_map [r] [r.get_role (entity).id].remove (entity)
    # end def remove

    def rename (self, entity, new_epk, renamer) :
        old_entity = self.instance (entity.__class__, new_epk)
        if old_entity :
            raise MOM.Error.Name_Clash (entity, old_entity)
        renamer     ()
    # end def rename

    def s_count (self, Type) :
        root = Type.relevant_root
        if root :
            query = self.session.query (root)
            if Type._sa_inheritance :
                query = query.filter_by (Type_Name = Type.type_name)
            return query.count ()
        return 0
    # end def s_count

    def s_extension (self, Type, sort_key = False) :
        root   = Type.relevant_root
        if root :
            query = self.session.query (root)
            if Type._sa_inheritance :
                query = query.filter_by (Type_Name = Type.type_name)
            if sort_key is not None :
                return sorted (query,  key = Type.sort_key (sort_key))
            return query
        return ()
    # end def s_extension

    ### XXX don't know how roles will be handled
    def s_role (self, role, obj, sort_key = False) :
        if not isinstance (obj, role.role_type.Essence) :
            return [] ### XXX
        return self.session.query \
            (role.assoc).filter_by (** {role.name : obj}).all ()
    # end def s_role

    def t_count (self, Type, seen = None) :
        root = Type.relevant_root
        if root :
            return self.session.query (Type).count ()
        return sum \
            (self.t_count (rr) for rr in Type.relevant_roots.itervalues ())
    # end def t_count

    def t_extension (self, Type , sort_key = None) :
        root   = Type.relevant_root
        ses    = self.session
        if root :
            result = ses.query (getattr (Type, "_type", Type))
        else :
            result = []
            for rr in Type.relevant_roots.itervalues () :
                result.extend (ses.query (rr).all ())
        if sort_key is not None :
            result = sorted (result, key = Type.sort_key (sort_key))
        return result
    # end def t_extension

    ### XXX don't know how roles will be handled
    def t_role (self, role, obj, sort_key = False) :
        return self.s_role (role, obj, sort_key)
    # end def t_role

    def _query_multi_root (self, Type) :
        QR      = self.Q_Result
        session = self.session
        return list (QR (session.query (t)) for t in Type.relevant_roots)
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        result = self.session.query (root)
        if Type._sa_inheritance :
            ### XXX wrong filter condition ???
            ### cf. EMS.Hash._query_single_root::
            ### result = itertools.ifilter \
            ###     (lambda x : isinstance (x, Type), result)
            result = result.filter_by (Type_Name = Type.type_name)
        return result
    # end def _query_single_root

    def __iter__ (self) :
        relevant_roots = self.scope.MOM.Id_Entity.relevant_roots.itervalues ()
        return itertools.chain \
            (* (self.t_extension (rr).all () for rr in relevant_roots))
    # end def __iter__

# end class Manager

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.SA
