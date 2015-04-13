# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.MF3.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.MF3.Completer
#
# Purpose
#    Completers for fields and entities for MOM Forms
#
# Revision Dates
#     7-May-2014 (CT) Creation
#     8-May-2014 (CT) Add support for nested completers
#     9-May-2014 (CT) Add `__call__`, `attr_names`, `field_ids`, `aq_filters`
#    10-May-2014 (CT) Change `__call__` to `choices`, add `_q_[ae]_as_json`
#    13-May-2014 (CT) Add `choose`
#    14-May-2014 (CT) Change `_q_a_as_json` to try single-attribute
#                     completion if multi-attribute completion exceeds `limit`
#    19-Aug-2014 (CT) Factor `ac_ui_display` to `MOM.E_Type_Manager`
#    25-Aug-2014 (CT) Fix `choose` to handle `Id_Entity` instances properly
#    25-Aug-2014 (CT) Change `elems` to use `entity_p_buddy_elems`, either of
#                     `embedder` or `self`
#    25-Aug-2014 (CT) Change `own_elems` to return `buddies`, only
#    25-Aug-2014 (CT) Change `embedded_elems` to `Once_Property`; change
#                     `E_Completer.embedded_elems` to return `embedded_elems`
#                     of all `.elem.elements` with `.completer`
#    26-Aug-2014 (CT) Add `anchor` to `result` of `choose`
#    29-Aug-2014 (CT) Factor `field_values`; add init-values for `readonly`
#                     elements
#    30-Aug-2014 (CT) Sort `matches` in `_q_e_as_json`
#    13-Apr-2015 (CT) Remove special-casing of MOM.Id_Entity from `choose`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                     import GTW
from   _MOM                     import MOM
from   _TFL                     import TFL

from   _MOM.import_MOM          import Q

import _MOM._Attr.Completer

from   _TFL._Meta.M_Class       import BaM
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import uniq
from   _TFL.pyk                 import pyk

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL._Meta.Property

from   itertools                import chain as ichain

@TFL.Add_To_Class ("MF3", MOM.Attr.Completer)
@pyk.adapt__bool__
class _MF3_Completer_ (TFL.Meta.Object) :

    _real_name = "Completer"

    embedder   = None

    def __init__ (self, elem) :
        attr           = elem.attr
        completer      = attr.completer
        parent         = elem.parent
        self.anchor    = elem.Entity
        self.attr      = attr
        self.elem      = elem
        self.entity_p  = completer.entity_p
        self.name      = str (elem.r_name)
        self.treshold  = completer.treshold
        if parent.completer is not None :
            parent.completer.add_inner (self)
    # end def __init__

    @property
    def as_json_cargo (self) :
        result = dict \
            ( entity_p = self.entity_p
            , fields   = list (self.fields)
            , treshold = self.treshold
            )
        return result
    # end def as_json_cargo

    @TFL.Meta.Once_Property
    def attr_names (self) :
        def _gen (self) :
            anchor  = self.anchor
            p_len   = (len (anchor.q_name) + 1) if anchor.q_name else 0
            for e in self.elems :
                yield e.q_name [p_len:]
        return tuple (_gen (self))
    # end def attr_names

    @TFL.Meta.Once_Property
    def elems (self) :
        if self.embedder :
            elems  = ichain ((self.elem, ), self.embedder.entity_p_buddy_elems)
            result = tuple  (uniq (elems))
        else :
            result = self.entity_p_buddy_elems
        return result
    # end def elems

    @TFL.Meta.Once_Property
    def embedded_elems (self) :
        return (self.elem, )
    # end def embedded_elems

    @TFL.Meta.Once_Property
    def entity_p_buddy_elems (self) :
        result = self.own_elems
        if self.entity_p :
            def _gen (self) :
                yield self.own_elems
                for e in self.anchor.elements :
                    c = e.completer
                    if c is not None and c.entity_p :
                        yield c.embedded_elems
            result = tuple (uniq (ichain (* _gen (self))))
        return result
    # end def entity_p_buddy_elems

    @TFL.Meta.Once_Property
    def etn (self) :
        return self.anchor.E_Type.type_name
    # end def etn

    @TFL.Meta.Once_Property
    def field_ids (self) :
        return tuple (e.id for e in self.elems)
    # end def field_ids

    @TFL.Meta.Once_Property
    def field_map (self) :
        return dict (zip (self.field_ids, self.attr_names))
    # end def field_map

    @TFL.Meta.Once_Property
    def fields (self) :
        return tuple (str (id) for id in sorted (self.field_ids))
    # end def fields

    @TFL.Meta.Once_Property
    def id (self) :
        completer_map = self.elem.root.completer_map
        sig           = self.sig
        try :
            result = completer_map [sig]
        except KeyError :
            result = completer_map [sig] = len (completer_map)
        return result
    # end def id

    @TFL.Meta.Once_Property
    def own_elems (self) :
        def _gen (self) :
            ep = self.elem.parent
            yield (self.elem, )
            for n in self.attr.completer.names :
                elem = ep.get (n)
                if elem is not None :
                    if elem.completer is not None :
                        yield elem.completer.embedded_elems
                    else :
                        yield (elem, )
        return tuple (uniq (ichain (* _gen (self))))
    # end def own_elems

    @TFL.Meta.Once_Property
    def sig (self) :
        return (self.fields, self.treshold, self.entity_p)
    # end def sig

    def add_inner (self, inner) :
        pass
    # end def add_inner

    def copy (self, ** kw) :
        cls    = self.__class__
        result = cls.__new__   (cls)
        result.__dict__.update (self.__dict__, ** kw)
        return result
    # end def copy

    def aq_filters (self, ETM, values) :
        def _gen (self, ETM, values) :
            AQ   = ETM.AQ
            fmap = self.field_map
            root = self.elem.root
            for k, v in pyk.iteritems (values) :
                if v != "" :
                    name = fmap.get (k)
                    if name is not None :
                        aq = getattr (AQ, name)
                        yield aq.AC (v)
        return tuple (_gen (self, ETM, values))
    # end def aq_filters

    def choices (self, scope, json, xtra_filter, max_completions = 20) :
        ETM       = scope [self.etn]
        limit     = max_completions + 1
        query     = self.query (ETM, self.field_values (json), xtra_filter)
        q_as_json = self._q_e_as_json if self.entity_p else self._q_a_as_json
        return q_as_json (ETM, query, json, limit)
    # end def choices

    def choose (self, scope, json, xtra_filter, pid_query_request) :
        ETM    = scope [self.etn]
        E_Type = ETM.E_Type
        anchor = self.anchor
        AQ     = ETM.E_Type.AQ
        fs     = tuple (getattr (AQ, n).QR for n in self.attr_names)
        ids    = self.field_ids
        obj    = pid_query_request (json ["pid"], E_Type)
        def _gen_values (obj, fs) :
            for f in fs :
                v = f (obj)
                yield v
            yield dict (display = obj.ui_display, pid = obj.pid)
        result = dict \
            ( completions  = 1
            , fields       = len  (fs)                  + 1
            , field_ids    = list (ids)                 + [anchor.id]
            , values       = list (_gen_values (obj, fs))
            )
        if self.entity_p :
            result ["anchor"] = anchor.id
        return result
    # end def choose

    def field_values (self, json) :
        result = dict (json ["field_values"])
        for e in self.elems :
            if e.id not in result :
                v = e.init
                if e.readonly and v is not None and not TFL.is_undefined (v) :
                    result [e.id] = v
        return result
    # end def field_values

    def query (self, ETM, values, xtra_filter) :
        aq_fs = self.aq_filters (ETM, values)
        if aq_fs or self.treshold == 0 :
            q = ETM.query (* aq_fs)
            if xtra_filter is not None :
                q = q.filter (xtra_filter)
            return q.distinct ()
        return TFL.Q_Result (())
    # end def query

    def _q_a_as_json (self, ETM, query, json, limit, names = None) :
        if names is None :
            names = self.attr_names
        AQ        = ETM.E_Type.AQ
        fs        = tuple (getattr (AQ, n).QR for n in names)
        fs_n      = len (fs)
        ids       = self.field_ids
        matches   = query.attrs (* fs).limit (limit).all ()
        result    = dict (matches = [], partial = False)
        n         = result ["completions"] = len (matches)
        finished  = result ["finished"]    = n == 1
        if n :
            if n < limit :
                result.update \
                    ( fields    = fs_n
                    , field_ids = ids [: fs_n]
                    , matches   = sorted (ETM.ac_ui_display (names, matches))
                    )
            else :
                if fs_n > 1 :
                    s_matches = query.attrs (fs [0]).limit (limit).all ()
                    m = len (s_matches)
                    if m < limit :
                        s_matches = sorted \
                            ( [m [0], "..."] for m in ETM.ac_ui_display
                                (names [:1], s_matches)
                            )
                        result.update \
                            ( fields    = 1
                            , field_ids = ids [: 1]
                            , matches   = sorted (s_matches)
                            , partial   = True
                            )
                    else :
                        ### XXX find fewer partial matches !!!
                        result.update \
                            ( fields    = 0
                            , field_ids = []
                            , feedback  = _T ("More than %s matches" % n)
                            )
        return result
    # end def _q_a_as_json

    def _q_e_as_json (self, ETM, query, json, limit) :
        matches  = query.limit (limit).all ()
        result   = dict (partial = False)
        n        = result ["completions"] = len (matches)
        finished = result ["finished"]    = n == 1
        if n :
            if n < limit :
                result.update \
                    ( fields    = 2
                    , field_ids = []
                    , matches   = list
                        (   (m.ui_display, m.pid)
                        for m in sorted (matches, key = ETM.sort_key)
                        )
                    )
            else :
                names  = self.attr_names [:1]
                result = dict \
                    ( self._q_a_as_json (ETM, query, json, limit, names = names)
                    , partial = True
                    )
        return result
    # end def _q_e_as_json

    def __bool__ (self) :
        return self.id is not None and bool (self.elems)
    # end def __bool__

    def __repr__ (self) :
        return "<%s for %s, treshold = %d, entity_p = %1d>" % \
            (self.__class__.__name__, self.elem, self.treshold, self.entity_p)
    # end def __repr__

Completer = _MF3_Completer_ # end class

class _Nested_Completer_ (Completer) :

    def add_inner (self, inner) :
        if inner.entity_p :
            inner.anchor   = self.anchor
            inner.embedder = self
    # end def add_inner

# end class _Nested_Completer_

@TFL.Add_To_Class ("MF3", MOM.Attr.C_Completer)
class _MF3_C_Completer_ (_Nested_Completer_) :

    _real_name = "C_Completer"

    @TFL.Meta.Once_Property
    def id (self) :
        ### The completer for a composite attribute isn't needed client-side,
        ### it's only used internally
        return None
    # end def id

    @TFL.Meta.Once_Property
    def own_elems (self) :
        return self.elem.field_elements
    # end def own_elems

    @TFL.Meta.Once_Property
    def embedded_elems (self) :
        return self.own_elems
    # end def embedded_elems

C_Completer = _MF3_C_Completer_ # end class

@TFL.Add_To_Class ("MF3", MOM.Attr.E_Completer)
class _MF3_E_Completer_ (_Nested_Completer_) :

    _real_name = "E_Completer"

    @TFL.Meta.Once_Property
    def embedded_elems (self) :
        def _gen (self) :
            for e in self.elem.elements :
                c = e.completer
                if c is not None :
                    yield c.embedded_elems
            yield (self.elem, )
        return tuple (uniq (ichain (* _gen (self))))
    # end def embedded_elems

E_Completer = _MF3_E_Completer_ # end class

if __name__ != "__main__" :
    GTW.MF3._Export ("*")
### __END__ GTW.MF3.Completer
