# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DBW.SAS.
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
#    MOM.DBW.SAS.Query
#
# Purpose
#    A wrapper which provides access to the SQL column objects trough the
#    attribute names of Entities.
#
# Revision Dates
#    12-Feb-2010 (MG) Creation (based on SA.Query)
#    18-Feb-2010 (MG) `MOM_Composite_Query`: comperison operators added
#    24-Mar-2010 (MG) Composite handling fixed
#    27-Apr-2010 (MG) `SAS_EQ_Clause` method added to support named value
#                     attributes
#     3-May-2010 (MG) Support for joins for filter and order_by added
#     4-May-2010 (CT) `_add_q` factored from `MOM_Query.__init__`,
#                     `ckd_name` added
#     5-May-2010 (MG) `Join_Quer.__call__` fixed to support ordering as well
#     7-May-2010 (MG) `MOM_Query.__init__` inherit `_query_fct` dict as well
#    12-May-2010 (MG) New `pid` style
#     5-Aug-2010 (MG) `MOM_Composite_Query.__ne__, __eq__` fixed
#    10-Aug-2010 (MG) Missing `_SA_TABLE` attributes added
#     2-Sep-2010 (CT) Signature of `Pickler.as_cargo` changed
#     2-Sep-2010 (MG) Store the kind in the database column attributes
#     6-Sep-2010 (MG) `Join_Query` specify the join condition
#     6-Sep-2010 (MG) `_MOM_Query_.SAS_EQ_Clause` fixed
#    19-Jul-2011 (MG) Support for raw queries added
#    21-Jul-2011 (MG) `_MOM_Query_.attributes` `pid` added
#    22-Sep-2011 (CT) s/A_Entity/A_Id_Entity/
#    22-Sep-2011 (CT) s/Class/P_Type/ for _A_Id_Entity_ attributes
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#     9-Nov-2011 (MG) `Join_Query.__call__`: handling of new `outerjoin`
#                     element in the `joins` list added
#    16-Dec-2011 (MG) `MOM_Composite_Query`: `MOM_C_Kind` added, accessors
#                     for cooked and raw name added
#    24-Jan-2012 (MG) `Join_Query.__call__` fixed
#    24-Jan-2012 (MG) `Join_Query.__call__` order of joins fixed (sqlite does
#                     not mapper, but other database do)
#    14-May-2012 (CT) Print exception info in `MOM_Composite_Query.__init__`
#    14-May-2012 (MG) `MOM_Composite_Query.__init__` query attribute handling
#                     fixed
#    10-Jun-2012 (MG) `Join_Query` Support for `tn_pid` added
#    29-Jun-2012 (MG) `Query.__init__` map `type_name` to `Type_Name`
#    11-Aug-2012 (MG) Change composite query handling
#    21-Aug-2012 (MG) Add support for `type_name` queries on joined tables
#    24-Aug-2012 (MG) Fix raw attribute queries for composites
#    19-Sep-2012 (MG) Change handling of role names to support redefinition
#                     in descantents
#    23-Jan-2013 (MG) Support query attributes resulting in Id_Entity's
#    26-Jan-2013 (CT) Add `e_type` to error TypeError
#    26-Jan-2013 (MG) Add `Cached_Role_Query`
#    29-Jan-2013 (MG) Support for cached roles enhanced
#    31-Jan-2013 (MG) Move creation of query attributes into the `finalize`
#                     method (required if query attributes of roles of an
#                     association access cached roles)
#    31-Jan-2013 (MG) Add `eq` and `ne` support for `Cached_Role_Query`
#    ««revision-date»»···
#--

from   _TFL                     import TFL
import _TFL._Meta.Object
import _TFL.Sorted_By
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe

from   _MOM                     import MOM
from   _MOM.import_MOM          import Q
import _MOM._DBW._SAS

from    sqlalchemy              import sql
import  operator
import  itertools

class Query (TFL.Meta.Object) :
    """A query object for non MOM objects"""

    def __init__ (self, cls, sa_table, ** attr_map) :
        cls._SAQ              = self
        self._CLASS           = cls
        self._SA_TABLE        = sa_table
        self._ID_ENTITY_ATTRS = dict ()
        columns               = sa_table.columns
        for col in columns :
            setattr (self, col.name, col)
            if col.name == "type_name" :
                self.Type_Name = col
        for syn, attr in attr_map.iteritems () :
            setattr (self, syn, getattr (self, attr))
    # end def __init__

    def SAS_EQ_Clause (self, attr, value) :
        return (), (getattr (self, attr) == value, )
    # end def SAS_EQ_Clause

    def __getattr__ (self, name) :
        return getattr (self._CLASS, name)
    # end def __getattr__

# end class Query

class _MOM_Query_ (TFL.Meta.Object) :
    """Base class for all queries for MOM objects"""

    _query_fct = {}

    @Once_Property
    @getattr_safe
    def attributes (self) :
        return dict (self._E_TYPE [0].attributes, pid = "pid")
    # end def attributes

    def raw_attr (self, key) :
        return self._RAW_ATTRIBUTES.get (key, getattr (self, key))
    # end def raw_attr

    def SAS_EQ_Clause (self, attr, cooked) :
        db = cooked
        if   attr == "type_name" :
            attr = "Type_Name"
        elif isinstance (cooked, MOM.Id_Entity) :
            db   = cooked.pid
        else :
            kind = getattr (self._E_TYPE [0], attr, None)
            if kind and kind.Pickler :
                db = kind.Pickler.as_cargo (kind, kind.attr, cooked)
        return (), (getattr (self, attr) == db, )
    # end def SAS_EQ_Clause

    def __getattr__ (self, name) :
        if name in self._query_fct :
            return self._query_fct [name].query._sa_filter (self)
        raise AttributeError (name)
    # end def __getattr__

# end class class _MOM_Query_

class MOM_Query (_MOM_Query_) :
    """Query for MOM Entities"""

    def __init__ ( self, e_type, sa_table, db_attrs, bases
                 , role_cacher
                 , cached_roles
                 ) :
        e_type._SAQ            = self
        self._CACHE_SPEC       = (role_cacher, cached_roles)
        self._E_TYPE           = e_type, bases
        self._SA_TABLE         = sa_table
        columns                = sa_table.columns
        self.pid               = columns [e_type._sa_pk_name]
        self._ATTRIBUTES       = []
        self._ROLE_ATTRIBUTES  = {}
        self._RAW_ATTRIBUTES   = {}
        self._COMPOSITES       = []
        self._ID_ENTITY_ATTRS  = {}
        self._CACHED_ROLES     = {}
        self._query_fct        = {}
        self.delayed = delayed = []
        #if e_type.type_name in ("PAP.Person_has_Address", "PAP.Person_has_Phone") :
        #    import pdb; pdb.set_trace ()
        if e_type is e_type.relevant_root :
            self.Type_Name    = columns.Type_Name
            self.pid          = columns.pid
            self.pid.MOM_Kind = None
            self._ATTRIBUTES.extend (("Type_Name", "pid"))
        for name, kind in db_attrs.iteritems () :
            attr = kind.attr
            if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                attr_name = "_SAQ_%s" % (name, )
                self._COMPOSITES.append (name)
                qclass = _MOM_Composite_Query_.__class__ \
                    ( "%s_%s_Query_Class" % (e_type.type_name, name)
                    , (kind.SAS_Query_Mixin, _MOM_Composite_Query_)
                    , {}
                    )
                comp_query = qclass (e_type, attr.P_Type, kind, sa_table)
                self._add_q (comp_query, kind, name, attr.ckd_name)
            elif isinstance (kind, MOM.Attr.Query) :
                delayed.append ((name, kind, attr))
            else :
                col        = columns [attr._sa_col_name]
                attr_names = [name]
                self._add_q (col, kind, name, attr.ckd_name)
                if kind.needs_raw_value :
                    rcol             = columns [attr._sa_raw_col_name]
                    rcol.IS_RAW_COL  = True
                    self._RAW_ATTRIBUTES [name] = rcol
                    self._add_q (rcol, kind, attr.raw_name)
                if isinstance (kind, MOM.Attr.Link_Role) :
                    self._ROLE_ATTRIBUTES [name] = col
                    attr_names.append (attr.role_name)
                if isinstance (attr, MOM.Attr._A_Id_Entity_) :
                    join_query = Join_Query (self)
                    for an in attr_names :
                        self._ID_ENTITY_ATTRS [an] = join_query
        for rc, assoc in role_cacher :
            self._add_cached_role (rc.role_name, rc, assoc)
        for name, attr in cached_roles :
            if name not in self._CACHED_ROLES :
                #import pdb; pdb.set_trace ()
                self._add_cached_role \
                    (name, attr.cacher, e_type.app_type [attr.assoc])
        for b_saq in (b._SAQ for b in bases if getattr (b, "_SAQ", None)) :
            self._COMPOSITES.extend (b_saq._COMPOSITES)
            self._ROLE_ATTRIBUTES.update (b_saq._ROLE_ATTRIBUTES)
            self._RAW_ATTRIBUTES = dict \
                (b_saq._RAW_ATTRIBUTES, ** self._RAW_ATTRIBUTES)
            for name in b_saq._ATTRIBUTES :
                setattr (self, name, b_saq [name])
                self._ATTRIBUTES.append (name)
            for an, jf in b_saq._ID_ENTITY_ATTRS.iteritems () :
                if an not in self._ID_ENTITY_ATTRS :
                    self._ID_ENTITY_ATTRS [an] = jf
            for an, attr in b_saq._query_fct.iteritems () :
                if an not in self._query_fct :
                    self._query_fct [an] = attr
            for name, crq in b_saq._CACHED_ROLES.iteritems () :
                if name not in self._CACHED_ROLES :
                    setattr (self, name, crq) ### XXX
                    self._CACHED_ROLES [name] = crq
        for rname, col in self._ROLE_ATTRIBUTES.iteritems () :
            kind = getattr (e_type, rname)
            setattr        (self, kind.role_name, col)
    # end def __init__

    def _add_cached_role (self, name, rc, assoc) :
        e_type = self._E_TYPE [0]
        if isinstance (rc, MOM.Link_Cacher) :
            crq = None
        else :
            crq = Cached_Role_Query \
                (self, assoc, rc.role_name, rc.other_role.name, e_type)
        self._CACHED_ROLES [name] = crq
        setattr (self, name, crq)
    # end def _add_cached_role

    def _add_q (self, q, kind, * names) :
        q.MOM_Kind = kind
        for n in names :
            setattr (self, n, q)
            self._ATTRIBUTES.append (n)
    # end def _add_q

    def finalize (self) :
        for name, kind, attr in self.delayed :
            query_fct = getattr (attr, "query_fct")
            if query_fct :
                self._query_fct [name] = attr
                if isinstance (attr, MOM.Attr._A_Id_Entity_) :
                    raise TypeError \
                       ( "Id Entity query `%s.%s` must be specified as "
                         "`query`, not `query_fct`"
                       % (e_type.type_name, attr.name, )
                       )
            else :
                ###import pdb; pdb.set_trace ()
                query   = attr.query._sa_filter (self)
                column  = jq = query [1] [0]
                if not isinstance (column, Cached_Role_Query) :
                    jq  = None
                ### since we are in the `finalize` function we need to create
                ### this attribute in the etype and all children
                etype   = self._E_TYPE [0]
                for et in itertools.chain \
                    ((etype, ), etype.children.itervalues ()) :
                    kind = getattr (et, attr.name)
                    if kind :
                        saq = et._SAQ
                        saq._add_q (column, kind, name)
                        if isinstance (attr, MOM.Attr._A_Id_Entity_) :
                            if jq is None :
                                jq = Join_Query (saq)
                            saq._ID_ENTITY_ATTRS [attr.name] = jq
    # end def finalize

    def __getitem__ (self, name) :
        return getattr (self, name)
    # end def __getitem__

# end class MOM_Query

class _MOM_Composite_Query_ (_MOM_Query_) :
    """Base class for query attributes of a composite attribute"""

    _Handled_Compare_Operations = set ()

    def __init__ (self, owner_etype, e_type, kind, sa_table) :
        self._E_TYPE      = (e_type, )
        self._SA_TABLE    = sa_table
        prefix            = kind._sa_prefix
        db_attrs, columns = e_type._sa_save_attrs.pop \
            ((owner_etype.type_name, kind.attr.name))
        prefix_len                = len (prefix)
        attr_names                = [c.name [prefix_len:] for c in columns]
        self._ATTRIBUTES          = attr_names
        self._RAW_ATTRIBUTES      = {}
        self._COLUMNS             = []
        self._ID_ENTITY_ATTRS     = {}
        for idx, name in \
            (  (i, an) for (i, an) in enumerate (attr_names)
            if not an.startswith ("__raw_")
            )  :
            col            = columns [idx]
            c_kind         = getattr (e_type, name)
            col.MOM_Kind   = c_kind
            col.MOM_C_Kind = kind
            setattr                (self, name,            col)
            setattr                (self, c_kind.ckd_name, col)
            self._COLUMNS.append   (col)
            if c_kind.needs_raw_value :
                c_kind                      = getattr (e_type, name)
                col                         = columns [idx + 1]
                col.MOM_Kind                = c_kind
                col.MOM_C_Kind              = kind
                col.IS_RAW_COL              = True
                self._RAW_ATTRIBUTES [name] = col
                setattr (self, c_kind.raw_name, col)
        self._query_fct = {}
        for name, c_kind in db_attrs.iteritems () :
            if isinstance (c_kind, MOM.Attr.Query) :
                query_fct = getattr (c_kind.attr, "query_fct")
                if query_fct :
                    self._query_fct [name] = c_kind.attr
                else :
                    col = c_kind.attr.query._sa_filter (self) [1] [0]
                    try :
                        col.MOM_kind   = c_kind
                        col.MOM_C_Kind = kind
                    except Exception as exc :
                        import sys
                        print >> sys.stderr, exc
                        print >> sys.stderr, owner_etype, e_type, name, c_kind, kind
                        raise
                    setattr (self, name, col)
    # end def __init__

    def _handle_operator_ (self, rhs, op, op_desc) :
        if op in self._Handled_Compare_Operations :
            result = []
            op     = getattr (operator, op)
            for an in self._QUERY_ATTRIBUTES :
                result.append \
                    (op (getattr (self, an), getattr (rhs, an, rhs)))
            return sql.and_ (* result)
        raise TypeError \
            ("`%s` is not supported for composites" % (op_desc, ))
    # end def _handle_operator_

    def __eq__ (self, rhs) :
        return self._handle_operator_ (rhs, "eq",  "==")
    # end def __eq__

    def __ne__ (self, rhs) :
        return self._handle_operator_ (rhs, "ne",  "!=")
    # end def __ne__

    def __le__ (self, rhs) :
        return self._handle_operator_ (rhs, "le",  "<=")
    # end def __le__

    def __lt__ (self, rhs) :
        return self._handle_operator_ (rhs, "lt",  "<")
    # end def __lt__

    def __gt__ (self, rhs) :
        return self._handle_operator_ (rhs, "gt",  ">")
    # end def __gt__

    def __ge__ (self, rhs) :
        return self._handle_operator_ (rhs, "ge",  ">=")
    # end def __ge__

    def in_ (self, rhs) :
        return self._handle_operator_ (rhs, "in_", "in")
    # end def in_

# end class _MOM_Composite_Query_

class Join_Query (_MOM_Query_) :
    """A query which requires the joining of two tables."""

    def __init__ (self, source) :
        self.source     = source
    # end def __init__

    def __call__ (self, attr_name, desc = False) :
        base, sub_attr = attr_name.split (".", 1)
        column         = getattr (self.source, base)
        try :
            o_SAQ      = column.mom_kind.P_Type._SAQ
        except AttributeError :
            if sub_attr == "tn_pid" :
                ### special handling of tn_pid queries
                pid_Table = MOM.DBW.SAS.Manager.sa_pid
                joins = ( ( column.table
                          , pid_Table
                          , column == pid_Table.c.pid
                          , False
                          )
                        ,
                        )
                oc    = (pid_Table.c.Type_Name, column)
            elif sub_attr == "type_name" :
                ### special handling of type_name queries
                pid_Table = MOM.DBW.SAS.Manager.sa_pid
                joins = ( ( column.table
                          , pid_Table
                          , column == pid_Table.c.pid
                          , False
                          )
                        ,
                        )
                oc    = (pid_Table.c.Type_Name, )
            else :
                type_name  = column.mom_kind.P_Type.type_name
                raise TypeError \
                    ( "Cannot query attribute `%s` of type `%s`.\n"
                      "If you need this query consider making `%s` relevant."
                    % (sub_attr, type_name, type_name)
                    )
        else :
            sub_sb         = TFL.Sorted_By (getattr (TFL.Getter, sub_attr) (Q))
            joins, oc      = sub_sb._sa_order_by (o_SAQ, desc = desc)
            for b in o_SAQ._E_TYPE [1] :
                j_SAQ = b._SAQ
                joins.append \
                    ( ( j_SAQ._SA_TABLE
                      , o_SAQ._SA_TABLE
                      ,    j_SAQ.pid
                        == o_SAQ._SA_TABLE.columns [o_SAQ._E_TYPE [0]._sa_pk_name]
                      , False
                      )
                    )
            joins.append \
                ( ( self.source._SA_TABLE
                  , o_SAQ.pid.table
                  , column == o_SAQ.pid
                  , not isinstance
                        ( column.mom_kind
                        , (MOM.Attr.Primary, MOM.Attr.Necessary)
                        )
                  )
                )
        return joins, oc
    # end def __call__

# end class Join_Query

class Cached_Role_Query (_MOM_Query_) :
    """A query attribute for cached roles"""

    def __init__ (self, source, assoc, attr_name, oattr_name, orole_et) :
        self.source       = source
        self.assoc        = assoc
        self. attr_name   =  attr_name
        self.oattr_name   = oattr_name
        self.orole_et     = orole_et
    # end def __init__

    @Once_Property
    @getattr_safe
    def joins (self) :
        sa_source      = self.source._SA_TABLE
        ### we have to use the _SAQ.left.table to get the table which defines
        ### the left/right attribute
        sa_assoc       = self.assoc._SAQ.left.table
        role_et        = getattr (self.assoc, self. attr_name).P_Type
        attr_col       = getattr (self.assoc._SAQ, self. attr_name)
        oattr_col      = getattr (self.assoc._SAQ, self.oattr_name)
        role_col       =       role_et._SAQ.pid
        orole_col      = self.orole_et._SAQ.pid
        role_table     = role_et._sa_table
        self.role_et   = role_et
        self.attr_col  = attr_col
        return \
           [ (sa_assoc,  role_table, attr_col  ==  role_col, False)
           , (sa_source, sa_assoc,   oattr_col == orole_col, False)
           ]
    # end def joins

    def _sa_filter (self, * args, ** kw) :
        joins = self.joins
        return joins [1:], (self.attr_col, )
    # end def _sa_filter

    def __call__ (self, attr_name) :
        base, sub_attr = attr_name.split (".", 1)
        return self.joins, (getattr (Q, sub_attr) (self.role_et._SAQ), )
    # end def __call__

    def __getattr__ (self, name) :
        if name.startswith ("__") :
            raise TypeError ("Opeation `%s` not supported" % (name, ))
        return self (".%s" % name)
    # end def __getattr__

    def _operator (self, name, arg) :
        joins, ac = self._sa_filter ()
        return getattr (ac [0], name) (arg)
    # end def _operator

    def contains (self, other) :
        return self._operator ("contains", getattr (other, "pid", other))
    # end def contains

    def in_ (self, others) :
        return self._operator ("in_", [getattr (o, "pid", o) for o in others])
    # end def in_

    def notin_ (self, others) :
        return self._operator \
            ("notin_", [getattr (o, "pid", o) for o in others])
    # end def notin_

    def __eq__ (self, rhs) :
        return self._operator ("__eq__", getattr (rhs, "pid", rhs))
    # end def __eq__

    def __ne__ (self, rhs) :
        return self._operator ("__ne__", getattr (rhs, "pid", rhs))
    # end def __ne__

# end class Cached_Role_Query

@TFL.Add_To_Class ("SAS_Query_Mixin", MOM.Attr._A_Composite_)
class _Default_Comp_Mixin_ (TFL.Meta.Object) :
    """Default implementation of the compare operations for composite
       attributes.
    """

    _Handled_Compare_Operations = set (("eq", "ne"))

    @Once_Property
    @getattr_safe
    def _QUERY_ATTRIBUTES (self) :
        return self._ATTRIBUTES
    # end def _QUERY_ATTRIBUTES

# end class _Default_Comp_Mixin_

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*", "_MOM_Composite_Query_")
### __END__ MOM.DBW.SAS.Query
