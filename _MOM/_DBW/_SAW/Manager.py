# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.
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
#    MOM.DBW.SAW.Manager
#
# Purpose
#    Database wrapper for RDBMS accessed by sqlalchemy wrapped by SAW
#
# Revision Dates
#    19-Jun-2013 (CT) Creation
#    21-Jun-2013 (CT) Add `PNS`, change `Pid_Manager` into property
#     1-Jul-2013 (CT) Redefine `_M_SAW_Manager_.__init__` to set `type_name`
#     1-Jul-2013 (CT) Implement `update_etype`
#     3-Jul-2013 (CT) Change `update_etype` to add `Partial_E_Type_Wrapper`
#     7-Jul-2013 (CT) Set `_SAW` for `Partial_E_Type_Wrapper`, too
#     8-Jul-2013 (CT) Add argument `app_type` to `finalize`
#     8-Jul-2013 (CT) Add `App_Type_Wrapper.finalize` to setup `tn_map`
#     8-Jul-2013 (CT) Use `PNS.SA_Type`, set `ATW.SA_Type`
#    16-Jul-2013 (CT) Fix `_Reload_Mixin_`
#    18-Jul-2013 (CT) Fix various bugs
#    26-Jul-2013 (CT) Put partial E_Types into `tn_map`, too
#    28-Jul-2013 (CT) Change `_saw_table_name` to remove `.`, change to lower
#    30-Jul-2013 (CT) Add `App_Type_Wrapper.seq_map`
#     1-Aug-2013 (CT) Add `App_Type_Wrapper.spk_names`
#     5-Aug-2013 (CT) Set `ems_check` of `P_uniqueness [0]` to `False` if a
#                     `UniqueConstraint` of the database is possible
#     6-Aug-2013 (CT) Don't define `Index` for `UniqueConstraint`
#     7-Aug-2013 (CT) Don't create `Partial_E_Type_Wrapper` unless `parent`
#                     has a `root_table`
#     9-Aug-2013 (CT) Change `update_etype` to fix `children` of partial
#                     descendents of relevant E_Types
#    ««revision-date»»···
#--

from   __future__     import division, print_function
from   __future__     import absolute_import, unicode_literals

from   _MOM           import MOM
from   _TFL           import TFL
from   _TFL.pyk       import pyk

from   _MOM._DBW._SAW import SA

import _MOM._DBW
import _MOM._DBW._Manager_
import _MOM._DBW._SAW
import _MOM._DBW._SAW.DBS
import _MOM._DBW._SAW.Pid_Manager
import _MOM._DBW._SAW.SA_Type
import _MOM._DBW._SAW.Session
import _MOM._SCM.Change

from   _TFL._Meta.Single_Dispatch import Single_Dispatch_Method

import itertools

class _Reload_Mixin_ (object) :
    """Mixin which triggers a reload of an entity from the database on any
       attribute access
    """

    @classmethod
    def _RELOAD_INSTANCE (cls, self, e_type) :
        e_type._SAW.Reloader.reload (self, self.home_scope.ems.session)
    # end def _RELOAD_INSTANCE

# end class _Reload_Mixin_

class App_Type_Wrapper (TFL.Meta.Object) :
    """SAW specific information about a derived App_Type"""

    def __init__ (self, app_type) :
        self.app_type   = app_type
        self.DBW        = DBW = app_type.DBW
        self.PNS        = PNS = DBW.PNS
        self.e_types_t  = []
        self.et_map     = {}
        self.tn_map     = {}
        self.metadata   = SA.schema.MetaData ()
        self.SA_Type    = PNS.SA_Type (self)
        self.sequences  = []
        self.seq_map    = {}
        self.spk_names  = set ()
    # end def __init__

    def add (self, etw) :
        tn = etw.type_name
        if etw.sa_table is not None :
            self.e_types_t.append (etw)
            seq = etw.sequence
            if seq :
                self.sequences.append (seq)
                name         = seq.attr.name
                seq_map      = self.seq_map
                seq_map [tn] = seq
                if name in ("cid", "pid") :
                    assert not name in seq_map
                    seq_map [name] = seq
        self.et_map [tn] = etw
        spk_name = etw.spk_name
        if spk_name :
            self.spk_names.add (spk_name)
    # end def add

    def finalize (self) :
        tn_map = self.tn_map
        names  = itertools.chain ([""], sorted (self.et_map))
        for tid, tn in enumerate (names) :
            tn_map.update (((tid, tn), (tn, tid)))
    # end def finalize

    def __getitem__ (self, key) :
        key = getattr (key, "type_name", key)
        return self.et_map [key]
    # end def __getitem__

# end class App_Type_Wrapper

class _M_SAW_Manager_ (MOM.DBW._Manager_.__class__) :
    """Meta class of MOM.DBW.SAW.Manager"""

    @TFL.Meta.Once_Property
    def db_sig (cls) :
        return tuple \
            (   ( k
                , tuple
                    (  (c.name, str (c.type), c.nullable, c.primary_key)
                    for c in columns
                    )
                )
            for (k, columns) in sorted (cls.meta_table_columns.iteritems ())
            )
    # end def db_sig

    @TFL.Meta.Once_Property
    def meta_table_columns (cls) :
        SA_Type = cls.PNS.SA_Type
        return dict \
            ( scope_metadata     =
                ( SA.schema.Column ("pk", SA_Type.Integer, primary_key = True)
                , SA.schema.Column ("readonly",  SA_Type.Boolean)
                , SA.schema.Column ("meta_data", SA_Type.PickleType)
                ,
                )
            )
    # end def meta_table_columns

    @property
    def Pid_Manager (cls) :
        return cls.PNS.Pid_Manager
    # end def Pid_Manager

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        cls.type_name = cls.PNS.__name__.rsplit (".", 1) [-1]
    # end def __init__

    def connect_database (cls, db_url, scope) :
        dbs     = cls.DBS_map       [db_url.scheme]
        engine  = dbs.create_engine (db_url)
        return cls._create_session  (engine, scope, TFL.Method.load_info)
    # end def connect_database

    def create_database (cls, db_url, scope) :
        ATW    = scope.app_type._SAW
        dbs    = cls.DBS_map        [db_url.scheme]
        dbs.create_database         (db_url, cls)
        engine = dbs.create_engine  (db_url)
        engine.create_tables        (ATW.metadata)
        return cls._create_session  (engine, scope, TFL.Method.create)
    # end def create_database

    def delete_database (cls, db_url) :
        dbs = cls.DBS_map   [db_url.scheme]
        dbs.delete_database (db_url, cls)
    # end def delete_database

    def etype_decorator (cls, e_type) :
        if not hasattr (e_type, "_SAW") :
            e_type._SAW = None
        if (  getattr (e_type, "relevant_root", None)
           or e_type.type_name == "MOM.Id_Entity"
           or not e_type.is_partial ### descendents of An_Entity, ...
           ) :
            etw = e_type._SAW = cls.PNS.E_Type_Wrapper (e_type)
            etw.ATW.add (etw)
        return e_type
    # end def etype_decorator

    def finalize (cls, app_type) :
        app_type._SAW.finalize ()
    # end def finalize

    def prepare (cls, app_type) :
        atw = app_type._SAW = App_Type_Wrapper (app_type)
        cls._create_meta_table (atw, "scope_metadata")
    # end def prepare

    def update_etype (cls, e_type, app_type) :
        ETW = e_type._SAW
        if ETW is not None :
            if ETW.e_type is e_type :
                sa_table = ETW.sa_table
                if sa_table is None :
                    if e_type.is_relevant :
                        if not e_type.is_partial :
                            raise TypeError \
                                ( "Non-partial revelant type %s "
                                  "without a table?"
                                % (e_type.type_name, )
                                )
                        ### partial e_type with relevant_root
                        ### fix children (the children's ETW refer to the first
                        ### ancestor with a sa_table)
                        ETW.children = sorted \
                            ( (c._SAW for c in pyk.itervalues (e_type.children))
                            , key = TFL.Getter.type_name
                            )
                else :
                    unique   = ETW.unique
                    unique_o = ETW.unique_o
                    if (   unique
                       and unique == unique_o
                       and not e_type.polymorphic_relevant_epk
                       ) :
                        sa_table.append_constraint \
                            (SA.schema.UniqueConstraint (* unique))
                        e_type.P_uniqueness [0].ems_check = False
                    if e_type._Reload_Mixin_ is not None :
                        e_type._Reload_Mixin_.define_e_type \
                            (e_type, _Reload_Mixin_)
                    cls._add_check_constraints    (e_type, ETW, sa_table)
                    cls._add_user_defined_indices (e_type, ETW, sa_table)
            elif ETW.root_table is not None :
                etw = e_type._SAW = cls.PNS.Partial_E_Type_Wrapper (e_type, ETW)
                ETW.ATW.add (etw)
    # end def update_etype

    def _add_check_constraints (cls, e_type, ETW, sa_table) :
        own_names = e_type._Predicates._own_names
        QR        = ETW.Q_Result
        for pk in e_type.P_uniqueness :
            if pk.name in own_names :
                pred    = pk.pred
                columns = []
                tables  = set ((sa_table, ))
                for qs in pred.aqs :
                    cols, join = qs._saw_filter (QR, ETW)
                    columns.extend (cols)
                    if join :
                        tables.update (j.table for j in join)
                if len (tables) == 1 :
                    unique = SA.schema.UniqueConstraint \
                        (* columns, name = pk.name)
                    sa_table.append_constraint (unique)
                    pred.ems_check = False
    # end def _add_check_constraints

    def _add_user_defined_indices (cls, e_type, ETW, sa_table) :
        for col_names in e_type.use_indices :
            if not isinstance (col_names, (tuple, list)) :
                col_names = (col_names, )
            col_names     = list (col_names)
            columns       = [getattr (sa_table.c, cn) for cn in col_names]
            ### add the table name to ensure uniqueness of the index name
            col_names.insert (0, sa_table.name)
            SA.schema.Index ("__".join (col_names), * columns)
    # end def _add_user_defined_indices

    def _create_meta_table (cls, atw, t_name) :
        columns = tuple (c.copy () for c in cls.meta_table_columns [t_name])
        result  = SA.schema.Table \
            (t_name, atw.metadata, * columns, ** cls.PNS.DBS.table_kw)
        setattr (atw, t_name, result)
        return result
    # end def _create_meta_table

    def _create_session  (cls, engine, scope, method) :
        result = getattr (cls.PNS, "Session_%s" % scope.ilk) (scope, engine)
        method           (result)
        return result
    # end def _create_session

# end class _M_SAW_Manager_

class _SAW_Manager_ \
          (TFL.Meta.BaM (MOM.DBW._Manager_, metaclass = _M_SAW_Manager_)) :
    """Database wrapper for SAW-wrapped sqlalchemy """

    _real_name    = "Manager"

    PNS           = MOM.DBW.SAW

Manager = _SAW_Manager_ # end class

@TFL.Add_To_Class ("_saw_table_name", MOM.Meta.M_E_Type)
@Single_Dispatch_Method (T = Manager.__class__)
def _saw_table_name (cls, DBW) :
    return cls.type_name.replace (".", "_").lower ()
# end def _saw_table_name

if __name__ != "__main__" :
    MOM.DBW.SAW._Export ("*", "_Reload_Mixin_")

    ### The following modules dispatch on `Manager.__class__` and therefore
    ### need to import `Manager`. Due to the cycle we need to import them
    ### after defining and exporting `Manager`
    import _MOM._DBW._SAW.Attr
    import _MOM._DBW._SAW.E_Type_Wrapper
### __END__ MOM.DBW.SAW.Manager
