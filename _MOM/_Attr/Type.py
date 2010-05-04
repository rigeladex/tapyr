# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Attr.Type
#
# Purpose
#    Model attribute types of MOM meta object model
#
# Revision Dates
#    28-Sep-2009 (CT) Creation (factored from TOM.Attr.Type)
#     7-Oct-2009 (CT) Class attribute `syntax` removed (added by `M_Attr_Type`
#                     if necessary)
#     7-Oct-2009 (CT) `_A_Named_Value_` and `A_Boolean` added
#     9-Oct-2009 (CT) `raw_default` and `_symbolic_default` added
#    13-Oct-2009 (CT) Guard for empty string added to `_to_cooked`
#    20-Oct-2009 (MG) `check_ascii` added as it is used for String attributes
#    22-Oct-2009 (CT) `needs_raw_value` added
#    22-Oct-2009 (CT) `max_length` added to `A_String` and its descendents
#    22-Oct-2009 (CT) Signatures of `_from_string_prepare` and
#                     `_from_string_eval` fixed
#    27-Oct-2009 (CT) `_A_Object_` changed to use `epk` instead of `name`
#    28-Oct-2009 (CT) I18N
#    28-Oct-2009 (CT) `A_Link_Role` and descendents added
#    29-Oct-2009 (CT) `_t_rank` added
#     3-Nov-2009 (CT) Fixed `as_string` and `_to_cooked` of `_A_Object_`
#     3-Nov-2009 (CT) `A_Link_Role` derived from `_A_Object_`
#     4-Nov-2009 (CT) `__all__` defined and used
#    19-Nov-2009 (CT) `_A_Object_._get_scope` changed to use
#                     `MOM.Scope.active` as default
#    23-Nov-2009 (CT) `__cmp__` and `__hash__` removed (breaks hashing of
#                     Link_Role attributes)
#    24-Nov-2009 (CT) `_A_Object_.cooked` added to check value agains `Class`
#    25-Nov-2009 (CT) `invariant` removed
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    26-Nov-2009 (CT) `A_Object`, `A_Cached_Role`, and `A_Cached_Role_DFC` added
#    26-Nov-2009 (CT) `_A_Object_.etype_manager` factored and used
#    18-Dec-2009 (CT) Use `unicode` instead of `str`
#    21-Dec-2009 (CT) `_A_Object_._get_object` factored
#    22-Dec-2009 (CT) `_A_Link_Role_Seq_No_` removed
#    30-Dec-2009 (CT) `A_Decimal` added
#     5-Jan-2010 (CT) `_Number_.min_value` and `_Number_.max_value` added
#     5-Jan-2010 (CT) `_checkers` added to `A_Attr_Type` and `_Number_`
#    14-Jan-2010 (CT) `ui_name` added
#    18-Jan-2010 (CT) `_A_Typed_Collection_`, `_A_Typed_List_`,
#                     `_A_Typed_Set_`, and `_A_Object_Set_` added
#    18-Jan-2010 (CT) `A_Cached_Role_Set` added
#    18-Jan-2010 (CT) `_A_Object_._check_type` factored
#    18-Jan-2010 (CT) `A_Link_Role`: redefined `cooked` (performance) and
#                     `_check_type` (to check `refuse_links`)
#    19-Jan-2010 (CT) `_A_String_` factored
#    19-Jan-2010 (CT) `A_Char` added
#    21-Jan-2010 (CT) `as_arg_ckd` and `as_arg_raw` added
#    21-Jan-2010 (CT) `cooked` and `_to_cooked` redefined for `_A_String_`
#    31-Jan-2010 (CT) `computed_default` added
#    31-Jan-2010 (CT) `A_Date_Slug` added
#     2-Feb-2010 (CT) `Pickler = None` added to `_A_Attr_Type_`
#     2-Feb-2010 (CT) `_A_Named_Object_` added
#     2-Feb-2010 (CT) `auto_up_depends` added
#     3-Feb-2010 (CT) `A_Email` added
#     4-Feb-2010 (CT) `_A_String_.default` added (`""`)
#     4-Feb-2010 (CT) `_A_Composite_` added
#     4-Feb-2010 (CT) Argument `e_type` added to `_checkers`
#                     `_A_Composite_._checkers` added
#     5-Feb-2010 (CT) `_A_Composite_.cooked` added
#     6-Feb-2010 (MG) `_A_Date_.as_string` typo fixed
#     9-Feb-2010 (CT) `now` added to `A_Date`, `A_Date_Time`, and `A_Time`
#    10-Feb-2010 (CT) `_A_Date_.needs_raw_value = False` added
#    12-Feb-2010 (CT) `A_Blob` added
#    22-Feb-2010 (CT) `A_Attr_Type.cooked` changed to guard agains `None`
#    22-Feb-2010 (CT) `_A_String_.cooked` removed, `._from_string_eval` and
#                     `._to_cooked` changed to call `simple_cooked`
#    22-Feb-2010 (CT) `_A_String_.__metaclass__` set to `M_Attr_Type_String`
#    24-Feb-2010 (CT) `ui_length` added
#    28-Feb-2010 (CT) `_A_String_Base_` factored, `A_Numeric_String` added
#     3-Mar-2010 (CT) `_checkers` changed to take additional argument `kind`
#     3-Mar-2010 (CT) `_A_Composite_._checkers` changed to honor `kind.electric`
#     4-Mar-2010 (CT) `_A_String_Base_._checkers` redefined to add a check
#                     for `max_length`, if any
#     4-Mar-2010 (CT) `max_length = 0` added to `_A_String_Base_`
#    10-Mar-2010 (CT) `A_Int_List` and `A_Date_List` added
#    11-Mar-2010 (CT) `epk_def_set_ckd` and `epk_def_set_raw` added
#    11-Mar-2010 (CT) `_A_Typed_Set_` corrected
#    12-Mar-2010 (CT) `_A_Composite_.from_string` corrected
#                     (s/s/t/ after assignment)
#    12-Mar-2010 (CT) Interface of `Pickler` changed
#    13-Mar-2010 (CT) `_A_Typed_Collection_.needs_raw_value = False`
#    13-Mar-2010 (CT) `_A_Binary_String_` added
#    15-Mar-2010 (CT) Interface of `attr.Pickler` changed again (`attr_type`)
#    22-Mar-2010 (CT) `A_Dirname` and `A_Filename` added (+ `_A_Filename_`)
#     9-Apr-2010 (CT) `A_Url` added
#    20-Apr-2010 (CT) Default `Type` added to `_A_Named_Object_.Pickler`
#    26-Apr-2010 (CT) `_A_Object_._to_cooked` changed to accept a single value
#                     as plain string instead of as a 1-tuple
#    26-Apr-2010 (CT) `_A_Typed_Collection_.from_string` redefined
#    26-Apr-2010 (CT) `_fix_C_Type` added
#    26-Apr-2010 (CT) `_A_Typed_Collection_._checkers` redefined to call
#                     `_fix_C_Type`
#    27-Apr-2010 (CT) Default for `glob` and `locl` changed from `None` to `{}`
#    27-Apr-2010 (CT) Default for `needs_raw_value` changed to `False`
#    28-Apr-2010 (CT) `_A_Collection_` factored from `_A_Typed_Collection_`
#    28-Apr-2010 (CT) `_A_Composite_Collection_` added
#    30-Apr-2010 (CT) `_A_Object_._get_object` changed to improve the message
#                     passed to `MOM.Error.No_Such_Object`
#    30-Apr-2010 (CT) `_A_Composite_.from_string` changed to set `raw = True`
#    30-Apr-2010 (CT) `A_Date.cooked` and `A_Date_Time.cooked` added to
#                     enforce the right type
#     4-May-2010 (CT) `ac_query` and `Q` added
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr.Kind
import _MOM._Meta.M_Attr_Type

from   _TFL.I18N             import _, _T, _Tn
from   _TFL.Regexp           import *
from   _TFL                  import sos

import _TFL._Meta.Once_Property
import _TFL._Meta.Property
import _TFL.Filter

import binascii
import datetime
import decimal
import itertools
import time

Q = TFL.Attr_Query ()

class _AC_Query_ (TFL.Meta.Object) :

    def __init__ (self, q, cooker = None) :
        self.q      = q
        self.cooker = cooker
    # end def __init__

    def __call__ (self, value) :
        cooker = self.cooker
        if cooker is not None :
            try :
                value = cooker (value)
            except (ValueError, TypeError) :
                return None
        return self.q (value)
    # end def __call__

# end class _AC_Query_

class A_Attr_Type (object) :
    """Root class for attribute types for the MOM meta object model."""

    __metaclass__       = MOM.Meta.M_Attr_Type
    _sets_to_combine    = ("check", )
    _lists_to_combine   = ("Kind_Mixins", )

    auto_up_depends     = ()
    check               = set ()
    check_syntax        = None
    code_format         = u"%r"
    computed            = None
    computed_default    = None
    default             = None
    description         = u""
    explanation         = u""
    format              = u"%s"
    group               = u""
    hidden              = False
    kind                = None
    Kind_Mixins         = ()
    needs_raw_value     = False
    Pickler             = None
    query               = None
    query_fct           = None
    rank                = 0
    raw_default         = u""
    record_changes      = True
    simple_cooked       = None
    store_default       = False
    symbolic_ref_pat    = Regexp (r"^\s*\$\(.*\)\s*$", re.MULTILINE)
    typ                 = None
    ui_name             = TFL.Meta.Once_Property \
        (lambda s : s.name.capitalize ().replace ("_", " "))
    ui_length           = 20

    _symbolic_default   = False
    _t_rank             = 0

    @TFL.Meta.Once_Property
    def ac_query (self) :
        if self.needs_raw_value :
            result = _AC_Query_ \
                (getattr (Q, self.raw_name).STARTSWITH, unicode)
        else :
            result = _AC_Query_ \
                (getattr (Q, self.ckd_name).__eq__, self.cooked)
        return result
    # end def ac_query

    def __init__ (self, kind) :
        self.kind = kind
    # end def __init__

    @classmethod
    def as_arg_ckd (cls) :
        if cls.kind :
            return cls.kind.as_arg_ckd (cls)
    # end def as_arg_ckd

    @classmethod
    def as_arg_raw (cls) :
        if cls.kind :
            return cls.kind.as_arg_raw (cls)
    # end def as_arg_raw

    def as_code (self, value) :
        return self.code_format % (value, )
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return soc.format % (value, )
        return u""
    # end def as_string

    def check_invariant (self, obj, value) :
        errors = obj._pred_man.check_attribute (obj, self, value)
        if len (errors) == 1 :
            raise errors [0]
        elif errors :
            raise MOM.Error.Invariant_Errors (errors)
    # end def check_invariant

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if value is not None and soc.simple_cooked :
            return soc.simple_cooked (value)
        return value
    # end def cooked

    @classmethod
    def epk_def_set_ckd (cls) :
        pass
    # end def epk_def_set_ckd

    @classmethod
    def epk_def_set_raw (cls) :
        pass
    # end def epk_def_set_raw

    def from_code (self, s, obj = None, glob = {}, locl = {}) :
        return self._to_cooked (s, self._call_eval, obj, glob, locl)
    # end def from_code

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        return self._to_cooked (s, self._from_string_resolve, obj, glob, locl)
    # end def from_string

    def _call_eval (self, s, glob, locl) :
        return eval (s, glob, locl.copy ())
    # end def _call_eval

    def _checkers (self, e_type, kind) :
        for c in sorted (self.check) :
            yield c, ()
    # end def _checkers

    def _fix_C_Type (self, e_type) :
        pass
    # end def _fix_C_Type

    def _from_string (self, s, obj, glob, locl) :
        t = self._from_string_prepare (s, obj)
        try :
            u = self._from_string_eval (t, obj, glob, locl)
        except StandardError as exc :
            raise MOM.Error.Attribute_Syntax_Error \
                (obj, self, "%s -> %s" % (s, t), str (exc))
        try :
            if u is not None :
                return self.cooked (u)
            else :
                pass
        except StandardError as exc :
            raise MOM.Error.Attribute_Syntax_Error \
                (obj, self, "%s -> %s -> %s" % (s, t, u), str (exc))
    # end def _from_string

    def _from_string_eval (self, s, obj, glob, locl) :
        return self._call_eval (s, glob, locl)
    # end def _from_string_eval

    def _from_string_prepare (self, s, obj) :
        try :
            s = unicode (s)
        except UnicodeError :
            raise MOM.Error.Attribute_Syntax_Error \
                ( obj, self, s
                , _T ("Non-ascii values in 8-bit strings are not supported")
                )
        return s
    # end def _from_string_prepare

    def _from_string_resolve (self, s, obj, glob, locl) :
        if obj is not None and not glob :
            glob = obj.globals ()
        if self.symbolic_ref_pat.match (s) :
            resolver = self._from_symbolic_ref
        else :
            resolver = self._from_string
        return resolver (s, obj, glob, locl)
    # end def _from_string_resolve

    def _from_symbolic_ref (self, s, obj, glob, locl) :
        raise NotImplementedError ("_from_symbolic_ref: XXX")
    # end def _from_symbolic_ref

    def _to_cooked (self, s, cooker, obj, glob, locl) :
        if s :
            if self.simple_cooked :
                try :
                    return self.simple_cooked (s)
                except (ValueError, TypeError) :
                    pass
            return cooker (s, obj, glob or {}, locl or {})
    # end def _to_cooked

    def __repr__ (self) :
       return "%s `%s`" % (self.typ, self.name)
    # end def __repr__

    def __str__ (self) :
        return self.name
    # end def __str__

# end class A_Attr_Type

class _A_Binary_String_ (A_Attr_Type) :
    """Base type for attributes written to database as binary string."""

    hidden              = True
    max_length          = None

    def as_code (self, value) :
        code = binascii.b2a_base64 (value)
        return self.__super.as_code_string (code)
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        return value or ""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        return value or ""
    # end def cooked

    def from_code (self, s, obj = None, glob = {}, locl = {}) :
        code = self.__super.from_code (s, obj, glob, locl)
        try :
            result = binascii.a2b_base64 (code)
        except (binascii.Error, TypeError) :
            result = ""
        return result
    # end def from_code

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        if s :
            return s
    # end def from_string

# end class _A_Binary_String_

class _A_Collection_ (A_Attr_Type) :
    """Base class for attributes that hold a collection of values."""

    C_Type          = None ### Type of entities held by collection
    C_sep           = ","
    R_Type          = None ### Type of collection

    needs_raw_value = False

    def __init__ (self, kind) :
        self.__super.__init__     (kind)
        self.C_Type = self.C_Type (kind)
    # end def __init__

    def as_code (self, value) :
        if value is not None :
            return self.__super.as_code \
              (self.C_sep.join (self._C_as_code (value)))
        return u""
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, val) :
        return soc.R_Type (soc.C_Type.cooked (v) for v in val)
    # end def cooked

    def from_code (self, s, obj = None, glob = {}, locl = {}) :
        comps = self._C_split (s.strip ())
        return self.R_Type (self._C_from_code (obj, comps, glob, locl))
    # end def from_code

    def _C_as_code (self, value) :
        return (self.C_Type.as_code (v) for v in value)
    # end def _C_as_code

    def _C_from_code (self, obj, comps, glob, locl) :
        return (self.C_Type.from_code (obj, c, glob, locl) for c in comps)
    # end def _C_from_code

    def _C_split (self, s) :
        if s in ("[]", "") :
            return []
        if s.startswith ("[") and s.endswith ("]") :
            s = s [1:-1]
        elif s.startswith ("(") and s.endswith (")") :
            s = s [1:-1]
        return (x for x in (r.strip () for r in s.split (self.C_sep)) if x)
    # end def _C_split

    def _from_symbolic_ref (self, s, obj, glob, locl) :
        raise TypeError \
            ( "Symbolic cross references not supported for attributes "
              "of type %s: `%s`"
            % (self.typ, s)
            )
    # end def _from_symbolic_ref

# end class _A_Collection_

class _A_Composite_ (A_Attr_Type) :
    """Common base class for composite attributes of an object."""

    ### Type of composite attribute (derived from MOM.An_Entity)
    C_Type            = None

    Kind_Mixins       = (MOM.Attr._Composite_Mixin_, )
    needs_raw_value   = False

    def as_code (self, value) :
        if value is not None :
            return "dict (%s)" % \
                ( ", ".join
                    (   "%s = %s" % (a.name, a.as_code (a.get_value (value)))
                    for a in value.user_attr if a.has_substance (value)
                    )
                ,
                )
        return u""
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return value.as_string ()
        return u""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, tuple) :
            value = dict (value)
        if isinstance (value, dict) :
            value = soc.C_Type (** value)
        if value is not None and not isinstance (value, soc.C_Type) :
            raise ValueError \
                (_T ("Value `%r` is not of type %s") % (value, soc.C_Type))
        return value
    # end def cooked

    @classmethod
    def epk_def_set_ckd (cls) :
        if cls.kind :
            form = "if %(name)s is None : %(name)s = cls.%(name)s.C_Type ()"
            return cls.kind.epk_def_set (form % dict (name = cls.name))
    # end def epk_def_set_ckd

    def from_code (self, s, obj = None, glob = {}, locl = {}) :
        return self.C_Type (** self.__super.from_code (s, obj, glob, locl))
    # end def from_code_string

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        t = s or {}
        if isinstance (t, basestring) :
            t = self._call_eval (t, {}, {})
        if isinstance (t, tuple) :
            t = dict (t)
        t.setdefault ("raw", True)
        return self.C_Type (** t)
    # end def from_string

    def _checkers (self, e_type, kind) :
        self._fix_C_Type (e_type)
        for c in self.__super._checkers (e_type, kind) :
            yield c
        name = self.name
        for k, ps in self.C_Type._Predicates._pred_kind.iteritems () :
            if kind.electric :
                k = kind.kind
                p_kind = MOM.Pred.System
            else :
                p_kind = MOM.Pred.Kind.Table [k]
            if ps :
                p_name = "AC_check_%s_%s" % (name, k)
                check  = MOM.Pred.Condition.__class__ \
                    ( p_name, (MOM.Pred.Condition, )
                    , dict
                        ( assertion  = "%s.is_correct (kind = %r)" % (name, k)
                        , attributes = (name, )
                        , kind       = p_kind
                        , name       = p_name
                        , __doc__    = " "
                          ### Space necessary to avoid inheritance of `__doc__`
                        )
                    )
                yield check, ()
    # end def _checkers

    def _fix_C_Type (self, e_type) :
        C_Type = self.C_Type
        if not hasattr (C_Type, "app_type") :
            if not isinstance (C_Type, basestring) :
                C_Type = C_Type.type_name
            self.C_Type = C_Type = e_type.app_type.etypes [C_Type]
    # end def _fix_C_Type

# end class _A_Composite_

class _A_Composite_Collection_ (_A_Collection_) :
    """Base class for attributes that hold a collection of composite values."""

    Kind_Mixins       = (MOM.Attr._Composite_Collection_Mixin_, )
    R_Type            = list

    class Pickler (TFL.Meta.Object) :

        __metaclass__ = MOM.Meta.M_Attr_Type__Pickler

        @classmethod
        def as_cargo (cls, obj, attr_kind, attr_type, value) :
            if value is not None :
                R_Type = attr_type.R_Type
                return tuple (v.as_pickle_cargo () for v in value)
        # end def as_cargo

        @classmethod
        def from_cargo (cls, obj, attr_kind, attr_type, cargo) :
            if cargo is not None :
                R_Type = attr_type.R_Type
                fpc    = attr_type.C_Type.C_Type.from_pickle_cargo
                return R_Type (fpc (obj.home_scope, c) for c in cargo)
        # end def from_cargo

    # end class Pickler

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return tuple (v.as_string () for v in value)
        return u""
    # end def as_string

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        t = s or ()
        if isinstance (t, basestring) :
            t = self._call_eval (t, {}, {})
        if t :
            C_fs = self.C_Type.from_string
            return self.R_Type (C_fs (c, obj, glob, locl) for c in t)
    # end def from_string

    def _checkers (self, e_type, kind) :
        C_Type = self.C_Type
        if C_Type :
            C_C_Type = getattr (C_Type, "C_Type", None)
            if C_C_Type :
                C_Type._fix_C_Type (e_type)
            ### XXX Predicate checking each component for `C_Type._checkers`
        return ()
    # end def _checkers

# end class _A_Composite_Collection_

class _A_Date_ (A_Attr_Type) :
    """Common base class for date-valued attributes of an object."""

    needs_raw_value    = False
    _tuple_off         = 0

    @property
    def output_format (self) :
        return self.input_formats [0]
    # end def output_format

    def as_code (self, value) :
        return self.__super.as_code (self.as_string (value))
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return value.strftime (soc.output_format)
        return u""
    # end def as_string

    def from_code (self, s, obj = None, glob = {}, locl = {}) :
        return self.from_string (self.__super.from_code (s, obj, glob, locl))
    # end def from_code

    def _from_string_eval (self, s, obj, glob, locl) :
        s = s.strip ()
        for f in self.input_formats :
            try :
                result = time.strptime (s, f)
            except ValueError :
                pass
            else :
                break
        else :
            raise ValueError (s)
        return self._DT_Type (* result [self._tuple_off:self._tuple_len])
    # end def _from_string_eval

# end class _A_Date_

class _A_Named_Value_ (A_Attr_Type) :
    """Common base class for attributes holding named values."""

    __metaclass__     = MOM.Meta.M_Attr_Type_Named_Value

    C_Type            = None ### Type of cooked values

    needs_raw_value   = False

    def as_code (self, value) :
        return self.code_format % (self.__class__.Elbat [value], )
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        Elbat = getattr (soc, "Elbat", None)
        if Elbat is None :
            Elbat = getattr (soc.__class__, "Elbat", None)
        return soc.format % (Elbat [value], )
    # end def as_string

    def eligible_raw_values (self, obj = None) :
        return sorted (self.__class__.Table.iterkeys ())
    # end def eligible_raw_values

    def from_code (self, s, obj = None, glob = {}, locl = {}) :
        return self._from_string_eval (self._call_eval (s, glob, locl))
    # end def from_code

    def _from_string_eval (self, s, obj, glob, locl) :
        try :
            return self.__class__.Table [s]
        except KeyError :
            raise ValueError \
                (u"%s not in %s" % (s, self.eligible_raw_values ()))
    # end def _from_string_eval

# end class _A_Named_Value_

class _A_Number_ (A_Attr_Type) :
    """Common base class for number-valued attributes of an object."""

    min_value         = None
    max_value         = None

    @TFL.Meta.Once_Property
    def ui_length (self) :
        if self.max_value :
            import math
            return int (math.ceil (math.log10 (self.max_value) + 1))
        else :
            return 12
    # end def ui_length

    def _checkers (self, e_type, kind) :
        if self.min_value is not None :
            if self.max_value is not None :
                yield "%s <= value <= %s" % (self.min_value, self.max_value), ()
            else :
                yield "%s <= value" % (self.min_value, ), ()
        elif self.max_value :
            yield "value <= %s" % (self.max_value, ), ()
        for c in self.__super._checkers (e_type, kind) :
            yield c
    # end def _checkers

# end class _A_Number_

class _A_Float_ (_A_Number_) :
    """Models a floating-point attribute of an object."""

    typ         = "Float"
    cooked      = float

    def _from_string_prepare (self, s, obj) :
        return s.replace ("/", "*1.0/")
    # end def _from_string_prepare

# end class _A_Float_

class _A_Int_ (_A_Number_) :
    """Models an integer attribute of an object."""

    typ         = "Int"
    cooked      = int

# end class _A_Int_

class _A_Link_Role_Left_ (A_Attr_Type) :
    """Attribute modelling the left role of a link."""

    generic_role_name = "left"
    rank              = 0
    role_abbreviation = "l"
    typ               = "Left"

# end class _A_Link_Role_Left_

class _A_Link_Role_L_Middle_ (A_Attr_Type) :
    """Attribute modelling the left-middle role of a link."""

    generic_role_name = "l_middle"
    rank              = 1
    role_abbreviation = "lm"
    typ               = "L_Middle"

# end class _A_Link_Role_L_Middle_

class _A_Link_Role_Middle_ (A_Attr_Type) :
    """Attribute modelling the middle role of a link."""

    generic_role_name = "middle"
    rank              = 2
    role_abbreviation = "m"
    typ               = "Middle"

# end class _A_Link_Role_Middle_

class _A_Link_Role_R_Middle_ (A_Attr_Type) :
    """Attribute modelling the right-middle role of a link."""

    generic_role_name = "r_middle"
    rank              = 3
    role_abbreviation = "rm"
    typ               = "R_Middle"

# end class _A_Link_Role_R_Middle_

class _A_Link_Role_Right_ (A_Attr_Type) :
    """Attribute modelling the right role of a link."""

    generic_role_name = "right"
    rank              = 4
    role_abbreviation = "r"
    typ               = "Right"

# end class _A_Link_Role_Right_

class _A_Object_ (A_Attr_Type) :
    """Models an attribute referring to an object."""

    Class             = ""

    needs_raw_value   = False

    def as_code (self, value) :
        return tuple (a.as_code (a.get_value (value)) for a in value.primary)
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return soc.format % \
                ( tuple
                    (a.as_string (a.get_value (value)) for a in value.primary)
                ,
                )
        return ""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        etm = soc.etype_manager ()
        if etm :
            soc._check_type (etm._etype, value)
        return value
    # end def cooked

    def eligible_objects (self, obj = None) :
        etm = self.etype_manager (obj)
        return (et and et.t_extension ()) or ()
    # end def eligible_objects

    def eligible_raw_values (self, obj = None) :
        return sorted (o.epk for o in self.eligible_objects (obj))
    # end def eligible_raw_values

    @TFL.Meta.Class_and_Instance_Method
    def etype_manager (soc, obj = None) :
        if soc.Class :
            return getattr (soc._get_scope (obj), soc.Class.type_name, None)
    # end def etype_manager

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        if s :
            return self._to_cooked (s, None, obj, glob, locl)
    # end def from_string

    def _accept_object (self, obj, result) :
        if (      self.__class__.eligible_objects.im_func
           is not _A_Object_.eligible_objects.im_func
           ) :
            eo = self.eligible_objects (obj)
            if eo :
                return result in eo
        return True
    # end def _accept_object

    @TFL.Meta.Class_and_Instance_Method
    def _check_type (soc, etype, value) :
        if not isinstance (value, etype) :
            raise ValueError \
                ( _T
                    ( u"%s %s not eligible for attribute %s,"
                      u"\n"
                      u"    must be instance of %s"
                    )
                % ( value.type_name, unicode (value), soc.name
                  , soc.Class.type_name
                  )
                )
    # end def _check_type

    def _get_object (self, obj, epk, raw = False) :
        scope  = self._get_scope (obj)
        tn     = self.Class.type_name
        etm    = scope [tn]
        result = etm.instance (* epk, raw = raw)
        if result is not None :
            if self._accept_object  (obj, result) :
                return self.cooked  (result)
            else :
                raise ValueError \
                    ( _T (u"object %s %s not eligible, specify one of: %s")
                    % (tn, epk, self.eligible_raw_values (obj))
                    )
        else :
            raise MOM.Error.No_Such_Object, \
                (  _T (u"No object of type %s with epk %s in scope %s")
                % (tn, epk, scope.name)
                )
    # end def _get_object

    @TFL.Meta.Class_and_Instance_Method
    def _get_scope (soc, obj) :
        return obj.home_scope if obj else MOM.Scope.active
    # end def _get_scope

    def _to_cooked (self, s, cooker, obj, glob, locl) :
        assert self.Class, "%s needs to define `Class`" % self
        if isinstance (s, tuple) :
            t  = s
        else :
            try :
                t  = self._call_eval (s, {}, {})
            except (NameError, SyntaxError) :
                t = (s, )
        return self._get_object  (obj, t, raw = True)
    # end def _to_cooked

# end class _A_Object_

class _A_String_Base_ (A_Attr_Type) :
    """Base class for string-valued attributes of an object."""

    default           = ""
    max_length        = 0
    ui_length         = TFL.Meta.Once_Property \
        (lambda s : s.max_length or 120)

    @TFL.Meta.Once_Property
    def ac_query (self) :
        return _AC_Query_ \
            (getattr (Q, self.ckd_name).STARTSWITH, self.simple_cooked)
    # end def ac_query

    def _checkers (self, e_type, kind) :
        for c in self.__super._checkers (e_type, kind) :
            yield c
        if self.max_length :
            name   = self.name
            p_kind = [MOM.Pred.Object, MOM.Pred.System] [kind.electric]
            p_name = "AC_check_%s_length" % (name, )
            check = MOM.Pred.Condition.__class__ \
                ( p_name, (MOM.Pred.Condition, )
                , dict
                    ( assertion  = "length <= %s" % (self.max_length, )
                    , attributes = (name, )
                    , bindings   = dict
                        ( length = "len (%s)" % (name, )
                        )
                    , kind       = p_kind
                    , name       = p_name
                    , __doc__    = "Value for %s must not be longer than %s"
                      % (name, self.max_length)
                    )
                )
            yield check, ()
    # end def _checkers

    def _from_string_eval (self, s, obj, glob, locl) :
        return self.simple_cooked (s)
    # end def _from_string

    def _to_cooked (self, s, cooker, obj, glob, locl) :
        if s is not None :
            return self.simple_cooked (s)
        return s
    # end def _to_cooked

# end class _A_String_Base_

class _A_Filename_ (_A_String_Base_) :
    """Base class for attributes holding filenames."""

    needs_raw_value   = False

    open_mode         = "w"
    """`open_mode' defines the mode to use for opening the file specified
       by the attribute's value.
       """

    do_check         = True
    """`do_check' specifies whether the existence of a file as specified by
       the attribute's value is checked by `from_string'.
       """

    @TFL.Meta.Class_and_Instance_Method
    def simple_cooked (soc, s) :
        if s :
            return s.encode ("ascii")
    # end def simple_cooked

    def _check_dir (self, d) :
        if not sos.path.isdir (d) :
            raise MOM.Error.No_Such_Directory, d
    # end def _check_dir

    def _check_read (self, s) :
        if "r" in self.open_mode and not sos.path.isfile (s):
            raise MOM.Error.No_Such_File, s
    # end def _check_read

    def _check_open (self, s, mode) :
        if "w" in self.open_mode or "a" in self.open_mode :
            exists = sos.path.isfile (s)
            file   = open (s, mode)
            file.close ()
            if not exists :
                sos.remove (s)
    # end def _check_open

    def _check_write (self, s) :
        if self.do_check :
            self._check_open (s, self.open_mode)
    # end def _check_write

# end class _A_Filename_

class _A_String_ (_A_String_Base_) :
    """Base class for string-valued attributes of an object."""

    __metaclass__     = MOM.Meta.M_Attr_Type_String

    ignore_case       = False
    needs_raw_value   = False
    simple_cooked     = unicode

# end class _A_String_

class _A_Named_Object_ (_A_Named_Value_) :
    """Common base class for attributes holding named objects (that can't be
       directly put into a database).
    """

    __metaclass__     = MOM.Meta.M_Attr_Type_Named_Object

    class Pickler (TFL.Meta.Object) :

        Type = _A_String_

        @classmethod
        def as_cargo (cls, obj, attr_kind, attr_type, value) :
            return attr_type.__class__.Elbat [value]
        # end def as_cargo

        @classmethod
        def from_cargo (cls, obj, attr_kind, attr_type, cargo) :
            Table = attr_type.__class__.Table
            try :
                return Table [cargo]
            except KeyError :
                raise ValueError (u"%s not in %s" % (cargo, sorted (Table)))
        # end def from_cargo

    # end class Pickler

# end class _A_Named_Object_

class _A_Typed_Collection_ (_A_Collection_) :
    """Base class for attributes that hold a collection of strictly typed
       values.
    """

    __metaclass__   = MOM.Meta.M_Attr_Type_Typed_Collection

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        ### when called for the class, `soc.__super` doesn't
        ### work while `super (_A_Typed_Collection_, soc)` does
        if value is not None :
            return super (_A_Typed_Collection_, soc).as_string \
                (soc.C_sep.join (soc._C_as_string (value)))
        return u""
    # end def as_string

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        result = None
        t      = s or []
        if isinstance (t, basestring) :
            result = self._from_string_eval (s, obj, glob, locl)
        elif t :
            C_fs = self.C_Type.from_string
            result = self.R_Type (C_fs (c, obj, glob, locl) for c in t)
        return result
    # end def from_string

    def _checkers (self, e_type, kind) :
        C_Type = self.C_Type
        if C_Type :
            if __debug__ :
                if isinstance (C_Type, _A_Composite_) :
                    raise TypeError \
                        ( "For composite collections, you need to derive "
                          "%s from `_A_Composite_Collection_`"
                        % self
                        )
            pass ### XXX Predicate checking each component for `C_Type._checkers`
        return ()
    # end def _checkers

    @TFL.Meta.Class_and_Instance_Method
    def _C_as_string (soc, value) :
        return (soc.C_Type.as_string (v) for v in value)
    # end def _C_as_string

    def _from_string_eval (self, s, obj, glob, locl) :
        comps = self._C_split (s.strip ())
        C_fse = self.C_Type._from_string_eval
        return self.R_Type (C_fse (c, obj, glob, locl) for c in comps)
    # end def _from_string

# end class _A_Typed_Collection_

class _A_Typed_List_ (_A_Typed_Collection_) :
    """Base class for list-valued attributes with strict type."""

    R_Type         = list

# end class _A_Typed_List_

class _A_Typed_Set_ (_A_Typed_Collection_) :
    """Base class for set-valued attributes with strict type."""

    R_Type         = set

# end class _A_Typed_Set_

class _A_Object_Set_ (_A_Typed_Set_) :

    C_Type         = _A_Object_

    def _C_as_code (self, value) :
        sk = MOM.Scope.active.MOM.Id_Entity.sort_key ()
        return self.__super._C_as_code (sorted (value, key = sk))
    # end def _C_as_code

    def _C_as_string (self, value) :
        sk = MOM.Scope.active.MOM.Id_Entity.sort_key ()
        return self.__super._C_as_string (sorted (value, key = sk))
    # end def _C_as_string

# end class _A_Object_Set_

class _A_Unit_ (A_Attr_Type) :
    """Mixin for attributes describing physical quantities with optional
       units.
    """

    __metaclass__  = MOM.Meta.M_Attr_Type_Unit
    _default_unit  = None ### set by meta class
    _unit_dict     = {}
    _unit_pattern  = Regexp \
        ( ur"[])a-zA-Z_0-9] \s+ (?P<unit> [a-zA-Z]+ (?: / [a-zA-Z]+)?) \s*$"
        , re.VERBOSE
        )

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        ### beware: `as_string` can be used as class method, too;
        ### when called for the class, `soc.__super` doesn't
        ### work while `super (_A_Unit_, soc)` does
        if value is not None :
            return "%s %s" % \
               (super (_A_Unit_, soc).as_string (value), soc._default_unit)
        return ""
    # end def as_string

    def eligible_raw_values (self, obj = None) :
        return sorted (self._unit_dict.iterkeys ())
    # end def eligible_raw_values

    def _from_string_eval (self, s, obj, glob, locl) :
        factor = 1
        pat    = self._unit_pattern
        if pat.search (s) :
            unit = pat.unit
            s    = s [: pat.start ("unit")]
            try :
                factor = self._unit_dict [unit]
            except KeyError :
                raise ValueError \
                      ( _T (u"Invalid unit %s, specify one of %s")
                      % (unit, self.eligible_raw_values ())
                      )
        return self.__super._from_string_eval (obj, s, glob, locl) * factor
    # end def _from_string_eval

# end class _A_Unit_

class A_Blob (A_Attr_Type) :
    """Generic type for binary attributes that aren't set by the user."""

    typ                 = "Blob"
    kind                = MOM.Attr._Cached_
    hidden              = True

# end class A_Blob

class A_Boolean (_A_Named_Value_) :
    """Models a Boolean attribute of an object."""

    typ            = "Boolean"
    ui_length      = 5

    Table          = dict \
        ( no       = False
        , yes      = True
        )

# end class A_Boolean

class A_Cached_Role (_A_Object_) :
    """Models an attribute referring to an object linked via an
       association.
    """

    kind           = MOM.Attr.Cached_Role
    typ            = "Cached_Role"
    hidden         = True

# end class A_Cached_Role

class A_Cached_Role_DFC (A_Cached_Role) :
    """Models an attribute to an object linked via an association or derived
       from a container.
    """

    kind           = MOM.Attr.Cached_Role_DFC

# end class A_Cached_Role_DFC

class A_Cached_Role_Set (_A_Object_Set_) :
    """Models an attribute referring to a set of objects linked via an
       association.
    """

    kind           = MOM.Attr.Cached_Role_Set
    typ            = "Cached_Role_Set"
    hidden         = True

# end class A_Cached_Role_Set

class A_Char (_A_String_) :
    """Models an attribute holding a single character."""

    typ            = "Character"
    max_length     = 1

# end class A_Char

class A_Date (_A_Date_) :
    """Models a date-valued attribute of an object."""

    typ            = "Date"
    ui_length      = 12
    input_formats  = \
        ( "%Y/%m/%d", "%Y%m%d", "%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y")
    _tuple_len     = 3
    _DT_Type       = datetime.date

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, datetime.datetime) :
            value = value.date ()
        elif not isinstance (value, datetime.date) :
            raise TypeError ("Date expected, got %r" % (value, ))
        return value
    # end def cooked

    @classmethod
    def now (cls) :
        return datetime.datetime.now ().date ()
    # end def now

# end class A_Date

class A_Date_List (_A_Typed_List_) :
    """Models a list-valued attribute comprising date elements."""

    typ            = "Date_List"
    C_Type         = A_Date

# end class A_Date_List

class A_Date_Slug (_A_String_) :
    """Models an atribute that stores a unique value based on the date/time
       of entity creation.
    """

    typ            = "Date-Slug"
    ui_length      = 22

    def computed_default (self) :
        now    = datetime.datetime.now ()
        result = "%s_%06d_%s" % \
            ( now.strftime ("%Y%m%d_%H%M%S")
            , now.microsecond
            , sos.getpid ()
            )
        return result
    # end def computed_default

# end class A_Date_Slug

class A_Date_Time (_A_Date_) :
    """Models a date-time-valued attribute of an object."""

    typ            = "Date-Time"
    ui_length      = 18
    input_formats  = tuple \
        ( itertools.chain
            ( * (  (f + " %H:%M:%S", f + " %H:%M", f)
                for f in A_Date.input_formats
                )
            )
        )
    _tuple_len     = 6
    _DT_Type       = datetime.datetime

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, datetime.date) :
            value = datetime.datetime (value.year, value.month, value.day)
        elif not isinstance (value, datetime.datetime) :
            raise TypeError ("Date expected, got %r" % (value, ))
        return value
    # end def cooked

    @classmethod
    def now (cls) :
        return datetime.datetime.now ()
    # end def now

# end class A_Date_Time

class A_Decimal (_A_Number_) :
    """Models a decimal-number valued attribute of an object."""

    __metaclass__  = MOM.Meta.M_Attr_Type_Decimal
    typ            = "Decimal"
    code_format    = "%s"

    decimal_places = 2
    max_digits     = 12
    rounding       = decimal.ROUND_HALF_UP
    ui_length      = TFL.Meta.Once_Property (lambda s : s.max_digits + 2)

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        D = decimal.Decimal
        if not isinstance (value, D) :
            if isinstance (value, float) :
                value = str (value)
            value = D (value, soc.D_Context)
        return value.quantize (soc.D_Quant)
    # end def cooked

# end class A_Decimal

class A_Dirname (_A_Filename_) :
    """Models an attribute of an object specifying a directory."""

    typ         = "Directory"

    def _from_string_eval (self, s, obj, glob, locl) :
        s = self.__super._from_string_eval (s, obj, glob, locl)
        if s :
            if sos.altsep :
                s = s.replace (sos.altsep, sos.sep)
            if not s.endswith (sos.sep) :
                s += sos.sep
            if self.do_check :
                self._check_dir   (s)
                self._check_write (s + ".ignore")
        return sos.path.normpath (s)
    # end def _from_string

# end class A_Dirname

class A_Email (_A_String_) :
    """An email address"""

    typ                = "Email"
    max_length         = 80

    ### XXX check_syntax

# end class A_Email

class A_Filename (_A_Filename_) :
    """Models an attribute of an object specifying a filename."""

    typ         = "Filename"

    def _from_string_eval (self, s, obj, glob, locl) :
        s = self.__super._from_string_eval (s, obj, glob, locl)
        if s and self.do_check :
            self._check_dir   (sos.path.dirname (s))
            self._check_read  (s)
            self._check_write (s)
        return sos.path.normpath (s)
    # end def _from_string

# end class A_Filename

class A_Float (_A_Float_) :
    code_format    = "%s"
    simple_cooked  = float
# end class A_Float

class A_Int (_A_Int_) :
    simple_cooked  = int
# end class A_Int

class A_Int_List (_A_Typed_List_) :
    """Models a list-valued attribute comprising integer elements."""

    typ            = "Int_List"
    C_Type         = A_Int

# end class A_Int_List

class A_Length (_A_Unit_, _A_Float_) :
    """Models a length attribute with unit information."""

    typ            = "Length"
    _unit_dict     = dict \
        ( { "in"   : 0.0254 }
        , cm       = 1.e-2
        , ft       = 0.3048000
        , km       = 1.e3
        , m        = 1.0
        , mi       = 1609.344
        , mm       = 1.e-3
        , Nm       = 1852.0
        , nm       = 1.e-9
        , um       = 1.e-6
        , yd       = 0.9144000
        )

# end class A_Length

class A_Link_Role (_A_Object_) :
    """Attribute describing a link-role."""

    __metaclass__     = MOM.Meta.M_Attr_Type_Link_Role

    auto_cache        = False
    dfc_synthesizer   = None
    kind              = MOM.Attr.Link_Role
    max_links         = 0
    role_name         = None
    role_type         = None
    ui_name           = TFL.Meta.Once_Property \
        (lambda s : s.role_name.capitalize ().replace ("_", " "))

    _t_rank           = -100

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        soc._check_type (soc.role_type, value)
        return value
    # end def cooked

    @TFL.Meta.Class_and_Instance_Method
    def _check_type (soc, etype, value) :
        soc.__super._check_type (etype, value)
        tn = soc.assoc.type_name
        if tn in value.refuse_links :
            raise MOM.Error.Link_Type_Error \
                ( tn
                , soc.role_type
                , soc.role_type.type_name
                , value
                , type (value)
                )
    # end def _check_type

# end class A_Link_Role

class A_Link_Role_AB (A_Link_Role) :
    """Attribute describing a link-role of an attribute-based link."""

    attr_name         = None

# end class A_Link_Role_AB

class A_Link_Role_EB (A_Link_Role) :
    """Attribute describing a link-role of an entity-based link."""

# end class A_Link_Role_EB

class A_Name (_A_String_) :
    """Models a name-valued attribute of an object."""

    typ                = "Name"
    max_length         = 32
    identifier_pattern = Regexp (u"^ [a-zA-Z_] [a-zA-Z0-9_]* $", re.X)
    syntax             = _T \
        ( u"A name must start with a letter or underscore and continue with "
          u"letters, digits, and underscores."
        )

    def check_syntax (self, obj, value) :
        if value :
            super = self.__super.check_syntax
            if super is not None :
                super (obj, value)
            v = value.strip ()
            if not self.identifier_pattern.match (v) :
                raise MOM.Error.Attribute_Syntax_Error (obj, self, value)
    # end def check_syntax

# end class A_Name

class A_Numeric_String (_A_String_Base_) :
    """Models an string-valued attribute that holds a numeric value (as
       string).
    """

    typ               = "Numeric_String"

    as_number         = int

    @TFL.Meta.Class_and_Instance_Method
    def simple_cooked (soc, value) :
        if isinstance (value, basestring) :
            value = value.replace (" ", "").lstrip ("+-")
        if value :
            value = soc.as_number (value)
        return unicode (value)
    # end def simple_cooked

# end class A_Numeric_String

class A_Object (_A_Object_) :
    """Models an attribute referring to an object."""

    typ            = "Object"
    Kind_Mixins    = (MOM.Attr.Object_Reference_Mixin, )

# end class A_Object

class A_String (_A_String_) :
    """Models a string-valued attribute of an object."""

    typ            = "String"
    max_length     = 64

# end class A_String

class A_Text (_A_String_) :
    """Models a string-valued attribute of an object which allows text of
       arbitrary length.
    """

    typ            = "Text"
    max_length     = None

# end class A_Text

class A_Time (_A_Date_) :
    """Models a time-valued attribute of an object."""

    typ            = "Time"
    ui_length      = 8
    input_formats  = ("%H:%M:%S", "%H:%M")
    _tuple_len     = 6
    _tuple_off     = 3
    _DT_Type       = datetime.time

    @classmethod
    def now (cls) :
        return datetime.datetime.now ().time ()
    # end def now

# end class A_Time

class A_Url (_A_String_) :
    """Models an url-valued attribute of an object."""

    typ            = "Url"
    max_length     = 96
    check          = ("""value.startswith (("/", "http://", "https://"))""", )

# end class A_Url

__doc__ = """
Class `MOM.Attr.A_Attr_Type`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: A_Attr_Type

    `MOM.Attr.A_Attr_Type` provides the framework for defining the
    type of essential or non-essential attributes of essential objects
    and links. It is the root class for a hierarchy of classes defining
    abstract attribute types like `A_Int`, `A_String`, `A_Name` and
    many more. All classes specifying abstract attribute types should
    be named following the convention `A_«type-name»` and must define
    a class attribute `typ` that defines the human-readable name of
    the abstract attribute type, e.g., `int`, `string`, or `name`.

    Concrete attribute definitions for essential classes are then
    specified by defining a class derived from the appropriate class
    defining the attribute type, e.g., `A_Int`. The names of classes
    defining concrete attributes **must** not start with `A_` to avoid
    terminal confusion.

    Abstract attribute types are characterized by the properties:

    .. attribute:: name

      Specified by the name of the class.

    .. attribute:: syntax

      Provides information about the syntax required for the
      attribute.

    .. attribute:: typ

      Defines the human-readable name of
      the abstract attribute type, e.g., `int`, `string`, or `name`.

    .. attribute:: needs_raw_value

      Specifies if the raw value needs to be stored for
      this attribute type.

    Concrete attribute types are characterized by the properties:

    .. attribute:: name

      Specified by the name of the class.

    .. attribute:: description

      A short description of the attribute in question.
      This is for example used for displaying a short help text.

      Normally specified via the doc-string of the
      class (but can also be defined by defining a class attribute
      `description`).

    .. attribute:: explanation

      A long description of the attribute in question
      (optional). This is used for the documentation of the attribute
      (together with `description`) and is for example displayed by
      an attribute browser.

    .. attribute:: kind

      Refers to the specific class defining the
      :class:`~_MOM._Attr.Kind.Kind` of the attribute in question.

    .. attribute:: Kind_Mixins

      A number of mixins for the `kind` to be used for this
      attribute. Some of the possible mixins are
      :class:`~_MOM._Attr.Kind.Computed_Mixin`,
      :class:`~_MOM._Attr.Kind.Sticky_Mixin`, and
      :class:`~_MOM._Attr.Kind.Class_Uses_Default_Mixin`.

      This is optional and defaults to `()`.

    .. attribute:: check

      Specifies a tuple of expressions that constrain the possible
      values of the attribute. e.g. '0 <= this <= 100'.

      This is optional and defaults to `()`.

    .. attribute:: default

      Defines the default value to be used for the
      attribute when no explicit value is defined by the tool's user.

      This is optional and defaults to `None`.

      `default` **must** not be specified for
      :class:`~_MOM._Attr.Kind.Primary` and
      :class:`~_MOM._Attr.Kind.Required` attributes.

    .. attribute:: computed

      A method that's used to compute a value if none is
      specified by the tool user for
      :class:`~_MOM._Attr.Kind.Optional` attributes with the
      :class:`~_MOM._Attr.Kind.Computed_Mixin` or
      one of the internal attributes kinds
      :class:`~_MOM._Attr.Kind.Sync_Cached`,
      :class:`~_MOM._Attr.Kind.Auto_Cached`,
      :class:`~_MOM._Attr.Kind.Once_Cached`, or
      :class:`~_MOM._Attr.Kind.Computed`.

    .. attribute:: group

      A string that can be used to group a set of attributes
      together. For instance, editors display attributes sorted
      alphabetically by `(group, name)`.

    .. attribute:: rank

      Used when sorting attributes.

    .. attribute:: store_default

      Specifies whether the default value should be
      stored in the database (unless explicitly specified, it isn't).

"""

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    ) + ("decimal", "Q")

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
    MOM._Export      ("Q")
### __END__ MOM.Attr.Type
