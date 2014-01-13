# -*- coding: utf-8 -*-
# Copyright (C) 2008-2014 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Error
#
# Purpose
#    Provide exception classes for MOM
#
# Revision Dates
#    18-Sep-2009 (CT) Creation (factored from TOM.Error)
#    12-Oct-2009 (CT) `Invalid_Primary_Key` added
#    21-Oct-2009 (CT) Creation continued
#    24-Nov-2009 (CT) `No_Such_Object` added
#    24-Nov-2009 (CT) `Error.__str__` changed
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#     3-Dec-2009 (CT) Optional argument `exc` added to `Invalid_Attribute`
#    15-Jan-2010 (MG) `Attribute_Syntax_Error.__unicode__` added
#    12-Feb-2010 (CT) `Invariant_Error._attribute_values` changed to use `%r`
#                     instead of `%s` for val
#    12-Feb-2010 (CT) `Invariant_Errors.__init__` redefined to sort `errors`
#    11-Mar-2010 (CT) `Mandatory_Missing` added
#    16-Jun-2010 (CT) `__str__` changed to `.encode` result of `__unicode__`
#    17-Jun-2010 (CT) Use `TFL.I18N.encode_o` instead of home-grown code
#    22-Jun-2010 (CT) `is_mandatory` added
#    30-Jun-2010 (CT) `Readonly_DB` added
#     8-Feb-2011 (CT) s/Required/Necessary/, s/Mandatory/Required/
#    22-Mar-2011 (MG) `Commit_Conflict` added
#     8-Nov-2011 (CT) Add `Required_Empty` and `any_required_empty`
#    30-Jan-2012 (CT) Change `Name_Clash` to show `.type_name`
#    12-Apr-2012 (CT) Change `Required_Missing` to use `I18N`,
#                     make it compatible to `Invariant_Error`
#    15-Apr-2012 (CT) Complete overhaul: cleanup, renamings, reparentings, I18N
#    16-Apr-2012 (CT) Continue complete overhaul: __super, refactoring, cleanup
#    17-Apr-2012 (CT) Add `as_json_cargo`, factor `Invariant.bindings`, cleanup
#    19-Apr-2012 (CT) Generalize `_formatted_bindings` for use in
#                     `Required_Missing.description`
#    19-Apr-2012 (CT) Use translated `.ui_name` instead of `.type_name`
#    19-Apr-2012 (CT) Change `_formatted_bindings` to remove @*$&@*% `u` prefix
#    20-Apr-2012 (CT) Add `_Invariant_.all_bindings`, put them into
#                     `as_json_cargo` as `bindings`
#    20-Apr-2012 (CT) Factor `Invariants._sort_key` and robustify
#    20-Apr-2012 (CT) Improve output of `Required_Missing`
#    20-Apr-2012 (CT) Add `Required_Missing.missing_t`
#    23-Apr-2012 (CT) Add `Ambiguous_Epk`
#    27-Apr-2012 (CT) Add `ui_display` to json cargo of `extra_links`
#    27-Apr-2012 (CT) Change `_Invariant_.bindings` to apply `unicode` to values
#    27-Apr-2012 (CT) Add and use `Invariants._flattened`
#    30-Apr-2012 (CT) Add `Duplicate_Link.__init__`
#    11-May-2012 (CT) Add message to `assert` in `Ambiguous_Epk.__init__`
#    11-May-2012 (CT) Change `Attribute_Syntax` to use
#                     `self.attribute.name`, not `self.attribute`, for json
#     1-Aug-2012 (CT) Add `Destroyed_Entity`
#     8-Aug-2012 (CT) Derive base class from `StandardError`, not `Exception`
#                     (too many exception clauses still use `StandardError`)
#    10-Aug-2012 (MG) Use `getattr` too access pid `Invariant.__init__`
#    12-Aug-2012 (CT) Add `Not_Unique`
#    10-Sep-2012 (CT) Fix name error in `Not_Unique`
#    11-Sep-2012 (CT) Derive `Not_Unique` from `_Invariant_`
#    12-Dec-2012 (CT) Change `Attribute.bindings` to format `value`
#    29-Jan-2013 (CT) Improve text of `Name_Clash`
#    30-Jan-2013 (CT) Fix `Not_Unique`, remove `Duplicate_Link`
#    26-Feb-2013 (CT) Improve text of `Multiplicity`
#    26-Feb-2013 (CT) Improve text of `Not_Unique`
#     1-Mar-2013 (CT) Use `_real_name` for `Error`
#    18-Apr-2013 (CT) Change `Link_Error` to `Wrong_Type`
#    25-Apr-2013 (CT) Add `Permission`
#     6-May-2013 (CT) Change `Error.as_unicode` to use `__doc__`, unless `.args`
#    11-Jun-2013 (CT) Add guard to `Attribute.bindings`
#    21-Aug-2013 (CT) Guard `is_required` in `Attribute_Syntax.__init__`
#    14-Jan-2014 (CT) Robustify `Attribute.__init__` and `.bindings`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _TFL                     import TFL
from   _MOM                     import MOM

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import *
from   _TFL.Record              import Record

import _TFL._Meta.Object
import _TFL.Caller
import _TFL.Accessor
import _TFL.I18N
import _TFL.Record

import itertools

class Exception_Handled (BaseException) :
    """Raised after an exception was already handled to bail out from an
       arbitrary position in a call-tree. Should be ignored further up.
    """
# end class Exception_Handled

def as_json_cargo (* excs) :
    def _gen (excs) :
        for exc in excs :
            try :
                cargo = exc.as_json_cargo
            except AttributeError :
                cargo = dict \
                    ( description = unicode (exc)
                    , head        = exc.__class__.__name__
                    )
            if isinstance (cargo, (list, tuple)) :
                for c in cargo :
                    yield c
            else :
                yield cargo
    return list (_gen (excs))
# end def as_json_cargo

class _MOM_Error_ (StandardError) :
    """Root class of MOM exceptions"""

    __metaclass__    = TFL.Meta.Object.__class__
    _real_name       = "Error"

    arg_sep          = ", "
    is_required      = False

    _json_attributes = \
        ( "as_unicode"
        , "is_required"
        )

    _json_map        = dict \
        ( as_unicode = "description"
        )

    @Once_Property
    def as_json_cargo (self) :
        json_map = self._json_map
        result   = {}
        for k in self._json_attributes :
            v = getattr (self, k, None)
            if v :
                result [json_map.get (k, k)] = v
        return result
    # end def as_json_cargo

    @Once_Property
    def as_str (self) :
        return TFL.I18N.encode_o (unicode (self))
    # end def as_str

    @Once_Property
    def as_unicode (self) :
        result = self.arg_sep.join (self.str_arg (self.args))
        if not result :
            result = _T (self.__class__.__doc__)
        return result
    # end def as_unicode

    def str_arg (self, args) :
        for a in args :
            try :
                s = unicode (a)
            except Exception as exc :
                s = "%s --> %s" % (repr (a), exc)
            yield s
    # end def str_arg

    def __eq__ (self, other) :
        return self.as_str == str (other)
    # end def __eq__

    def __le__ (self, other) :
        return self.as_str <= str (other)
    # end def __le__

    def __lt__ (self, other) :
        return self.as_str < str (other)
    # end def __lt__

    def __hash__ (self) :
        return hash (self.as_str)
    # end def __hash__

    def __str__ (self) :
        return self.as_str
    # end def __str__

    def __unicode__ (self) :
        return self.as_unicode
    # end def __unicode__

Error = _MOM_Error_ # end class

class _Invariant_ (Error) :

    attributes       = ()
    description      = ""
    description_plus = ""
    explanation      = ""
    extra_links      = ()
    indent           = " " * 4
    val_disp         = {}

    _json_attributes = \
        ( "all_bindings"
        , "attributes"
        , "description"
        , "explanation"
        , "head"
        , "is_required"
        )
    _json_map        = dict \
        ( all_bindings = "bindings"
        )

    def __init__ (self, obj, raw = False) :
        self.obj = obj
        self.raw = raw
    # end def __init__

    @Once_Property
    def all_bindings (self) :
        result = self.bindings
        result.extend \
            ((a, None) for a in self.attributes if a not in self.val_disp)
        return sorted (result)
    # end def all_bindings

    @Once_Property
    def as_json_cargo (self) :
        result = self.__super.as_json_cargo
        xtra   = sorted \
            ( (   (pid, d)
              for pid, d in
                    (   (getattr (x, "pid", None), x.ui_display)
                    for x in self.extra_links
                    )
              if  pid is not None
              )
            , key = TFL.Getter [1]
            )
        if xtra :
            result ["extra_links"] = xtra
        return result
    # end def as_json_cargo

    @Once_Property
    def bindings (self) :
        return sorted ((k, unicode (v)) for k, v in self.val_disp.iteritems ())
    # end def bindings

    @property
    def head (self) :
        return _T ("Invariant error")
    # end def head

    def assertion (self) :
        result = []
        for info in self.head, self.description, self.explanation :
            if info :
                result.append (info)
        return ("\n" + self.indent).join (result)
    # end def assertion

    def _clean_this (self, s) :
        return s.replace ("this.", "").strip ()
    # end def _clean_this

    def _formatted_bindings (self, bindings = None) :
        if bindings is None :
            bindings = self.bindings
        for k, v in bindings :
            if isinstance (v, (list, tuple)) :
                v = ", ".join ("%s" % (x, ) for x in v)
            elif v is None :
                v = _T ("None")
            else :
                v = ("%r" if self.raw else "%s") % (v, )
                if v.startswith (('u"', "u'")) :
                    v = v [1:]
            yield "%s = %s" % (k, v)
    # end def _formatted_bindings

# end class _Invariant_

class Ambiguous_Epk (_Invariant_) :

    arg_sep        = ". "
    raw            = False

    def __init__ (self, e_type, epk, kw, count, * matches) :
        assert 1 < count <= len (matches), \
            "count = %s, matches = %s" % (count, matches)
        self.e_type     = e_type
        self.epk        = tuple (repr (x) for x in epk)
        self.kw         = kw
        self.count      = count
        self.matches    = tuple (m.ui_display for m in matches)
        self.FO         = matches [0].FO
    # end def __init__

    @Once_Property
    def all_bindings (self) :
        result = self.bindings
        given  = dict (result)
        e_type = self.e_type
        result.extend \
            ( (a.name, None)
            for a in itertools.chain (e_type.primary, e_type.required)
            if  a.name not in given
            )
        return sorted (result)
    # end def all_bindings

    @Once_Property
    def args (self) :
        attrs = _T ("Attributes given: (%s)") % \
            ( ", ".join
                ( self._formatted_bindings
                    ((k, v) for k, v in self.bindings if v is not None)
                )
            )
        return (self.head, attrs, self.description)
    # end def args

    @Once_Property
    def bindings (self) :
        FO = self.FO
        return sorted \
            (   (k, (str (FO (k, v)) if v is not None else v))
            for (k, v) in itertools.chain
                ( (zip (self.e_type.epk_sig, self.epk))
                , self.kw.iteritems ()
                )
            )
    # end def bindings

    @Once_Property
    def head (self) :
        return \
            ( _T
              ("The given attributes match %s entities instead of one or none")
            % (self.count, )
            )
    # end def head

    @Once_Property
    def description (self) :
        matches = self.matches
        more    = self.count - len (matches)
        result  = \
            ( _T ("Matching entities: %s%s")
            % ("; ".join (matches), " ..." if more else "")
            )
        return result
    # end def description

# end class Ambiguous_Epk

class Attribute (Error) :

    _json_attributes = \
        ( "as_unicode"
        , "attributes"
        , "bindings"
        , "is_required"
        )

    def __init__ (self, entity, name, val, kind = "unknown", exc = None) :
        if entity :
            msg = \
                ( _T ("Can't set %s attribute %s.%s to `%r`")
                % (_T (kind), entity.type_base_name, name, val)
                )
        else :
            msg = \
                ( _T ("Can't set %s attribute %s to %r")
                % (_T (kind), name, val)
                )
        if exc :
            msg = "%s.\n    %s" % (msg, exc)
        self.args       = (msg, )
        self.entity     = entity
        self.kind       = kind
        self.attribute  = name
        self.attributes = (name, )
        self.value      = val
    # end def __init__

    @Once_Property
    def bindings (self) :
        if self.entity :
            FO    = self.entity.FO
            name  = self.attribute
            try :
                fov   = FO (name, self.value)
            except Exception :
                value = str (self.value)
            else :
                value = str (fov)
            return ((name, value), )
    # end def bindings

    def correct (self) :
        pass
    # end def correct

# end class Attribute

class Attribute_Set (Attribute, AttributeError) :
    """Attribute can't be set."""

# end class Attribute_Set

class Attribute_Syntax (_Invariant_, ValueError) :
    """Raised for syntax errors in attributes of MOM objects/links."""

    class inv :
        name       = "syntax_valid"

    def __init__ (self, obj, attr, val, exc_str = "") :
        self.__super.__init__ (obj)
        self.args         = (obj, attr, val, exc_str)
        self.obj          = obj
        self.attribute    = attr
        self.attributes   = (attr.name, )
        try :
            self.is_required  = attr.is_required
        except AttributeError :
            self.is_required  = getattr (attr.kind, "is_required", False)
        self.value        = val
        self.exc_str      = exc_str
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        attr   = self.attribute
        result = \
            ( _T ( "`%s` for : `%r`"
                   "\n     expected type  : `%s`"
                   "\n     got      value : `%s`"
                 )
            % ( self.exc_str or _T ("Syntax error")
              , attr, attr.typ, self.value
              )
            )
        if attr.syntax :
            result = "\n".join ((result, attr.syntax))
        return result
    # end def as_unicode

    @Once_Property
    def bindings (self) :
        return ((self.attribute.name, self.value), )
    # end def bindings

    @Once_Property
    def head (self) :
        return \
            ( _T ("Syntax error: \n  expected type `%s`\n  got value `%s`")
            % (_T (self.attribute.typ), self.value)
            )
    # end def head

    @Once_Property
    def description (self) :
        if self.attribute.syntax :
            return "%s: %s" % (_T ("Syntax"), _T (self.attribute.syntax))
    # end def description

    @Once_Property
    def explanation (self) :
        if self.exc_str :
            return "%s: %s" % (_T ("Exception"), self.exc_str)
    # end def explanation

# end class Attribute_Syntax

class Attribute_Unknown (Attribute, AttributeError) :
    """An unknown name was used to set an attribute."""

    def correct (self) :
        """Try to correct this error."""
        self.entity.correct_unknown_attr (self)
    # end def correct

# end class Attribute_Unknown

class Attribute_Value (Attribute, ValueError) :
    """Invalid value for attribute."""

# end class Attribute_Value

class Circular_Link (Error) :
    """Raised when a link is added to an association which results directly or indirectly in a circular link."""
# end class Circular_Link

class DB (Error) :
    pass
# end class DB

class Commit_Conflict (DB) :
    """Conflict during commit of database."""
# end class Commit_Conflict

class Destroyed_Entity (Error) :
    """The entity was already destroyed and cannot be used anymore."""
# end class Destroyed_Entity

class Empty_DB (DB) :
    """Database is empty."""
# end class Empty_DB

class Incompatible_DB_Version (DB) :
    """Database version is not compatible to software version."""
# end class Incompatible_DB_Version

class Inconsistent_Attribute (Error) :
    pass
# end class Inconsistent_Attribute

class Inconsistent_Predicate (Error) :
    pass
# end class Inconsistent_Predicate

class Invariant (_Invariant_) :

    def __init__ (self, obj, inv) :
        self.__super.__init__ (obj)
        pid               = getattr (obj, "pid", None)
        self.args         = (obj, inv) if pid else (_T (obj.ui_name), inv)
        self.inv          = inv
        self.is_required  = inv.is_required
        self.attributes   = sorted (inv.attributes + inv.attr_none)
        self.extra_links  = list   (inv.extra_links)
        self.val_disp     = dict   (inv.val_disp)
        description       = inv.description
        try :
            self.inv_desc = description % TFL.Caller.Object_Scope (obj)
        except TypeError :
            self.inv_desc = description
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        return self._as_string \
            (head = "%s `%s` : " % (_T ("Condition"), _T (self.inv.name)))
    # end def as_unicode

    @Once_Property
    def description (self) :
        inv    = self.inv
        more   = inv.error_info
        result = []
        if inv.description and inv.assertion :
            result.append ("(%s)" % (inv.assertion, ))
        if more :
            result.extend (more)
        return "\n".join (result)
    # end def description

    @Once_Property
    def description_plus (self) :
        description = self.description
        result      = self._tail ("")
        if description :
            result = "\n".join ((description, "", result))
        return self._clean_this (result)
    # end def description_plus

    @Once_Property
    def explanation (self) :
        return self.inv.explanation
    # end def explanation

    @Once_Property
    def head (self) :
        return self.inv_desc or self.inv.assertion
    # end def head

    def assertion (self) :
        indent = self.indent
        return self._as_string (sep = "\n" + indent, indent = indent)
    # end def assertion

    def _as_string (self, sep = " ", head = "", indent = None) :
        desc   = self.description
        result = [head]
        if self.head :
            result.extend ((self.head, sep))
        if desc :
            result.append (desc)
        result.append (self._tail (indent))
        return self._clean_this ("".join (result))
    # end def _as_string

    def _tail (self, indent = None) :
        if indent is None :
            indent = self.indent
        result = []
        sep    = "\n" + indent
        if self.bindings :
            result = itertools.chain ([""], self._formatted_bindings ())
        return sep.join (result)
    # end def _tail

# end class Invariant

class Invariants (Error) :

    arg_sep = "\n  "

    def __init__ (self, errors) :
        errors = self.errors = sorted \
            (self._flattened (errors), key = self._sort_key)
        self.__super.__init__ (* errors)
    # end def __init__

    @Once_Property
    def as_json_cargo (self) :
        return list (e.as_json_cargo for e in self.errors)
    # end def as_json_cargo

    @property
    def any_required_empty (self) :
        return any (isinstance (e, Required_Empty) for e in self.errors)
    # end def any_required_empty

    def _flattened (self, errors) :
        for e in errors :
            ee = getattr (e, "errors", None)
            if ee is not None :
                e = tuple (ee)
            if isinstance (e, (list, tuple)) :
                for x in self._flattened (e) :
                    yield x
            else :
                yield e
    # end def _flattened

    def _sort_key (self, err) :
        try :
            return err.inv.name
        except AttributeError :
            return unicode (err)
    # end def _sort_key

# end class Invariants

class Link_Scope_Mix (Error) :
    """Raised when objects with different home scopes are put into a link."""
# end class Link_Scope_Mix

class Multiplicity (Error) :
    """Raised when the maximum multiplicity for an association is violated."""

    def __init__ (self, e_type, role, r_obj, epk, * links) :
        self.e_type       = e_type
        self.role         = role
        self.type_name    = e_type.ui_name
        self.l_ui_display = str  (epk)
        self.r_ui_display = r_obj.ui_repr
        self.extra_links  = tuple \
            ( TFL.Record
                ( pid        = getattr (x, "pid", None)
                , ui_display = x.ui_repr
                , type_name  = _T (x.ui_name)
                )
            for x in links
            )
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        return self.description
    # end def as_unicode

    @Once_Property
    def head (self) :
        return \
            ( _T
              ("The new definition of %s %s would exceed the maximum "
               "number [%s] of links allowed for %s."
              )
            % ( self.type_name, self.l_ui_display
              , self.role.max_links, self.r_ui_display
              )
            )
    # end def head

    @Once_Property
    def description (self) :
        result = [self.head]
        extras = tuple (x.ui_display for x in self.extra_links)
        result.append \
            ( _T ("Already existing:\n    %s") % ("\n    ".join (extras), ))
        return "\n  ".join (result)
    # end def description

# end class Multiplicity

class Multiplicity_Errors (Error) :

    arg_sep = "\n  "

    @Once_Property
    def as_json_cargo (self) :
        return list (a.as_json_cargo for a in self.args)
    # end def as_json_cargo

# end class Multiplicity_Errors

class Name_Clash (Error) :
    """Raised when one name is used for more than one object."""

    arg_sep = " "

    def __init__ (self, new, old) :
        otn = _T (old.ui_name) if old else ""
        otd = ("`%s`" % (old.ui_display, )) if old else _T ("object")
        self.__super.__init__ \
            ( _T ("new definition of %s `%s` clashes with existing %s %s")
            % (_T (new.ui_name), new.ui_display, otn, otd)
            )
    # end def __init__

# end class Name_Clash

class No_Such_Directory (Error) :
    """Raised for a file specification containing a non-existent directory."""
# end class No_Such_Directory

class No_Such_Entity (Error) :
    """Raised if an unknown epk is passed for an object or link-role."""
# end class No_Such_Entity

class No_Such_File (Error) :
    """Raised for a file specification of a non-existing file."""
# end class No_Such_File

class Not_Unique (_Invariant_) :
    """Set of attributes is not unique for each entity."""

    def __init__ (self, obj, inv) :
        self.__super.__init__ (obj)
        self.attributes   = sorted (inv.attributes + inv.attr_none)
        self.count        = len (inv.clashes)
        self.extra_links  = tuple \
            ( TFL.Record
                ( pid        = getattr (x, "pid", None)
                , ui_display = x.ui_repr
                , type_name  = _T (x.ui_name)
                )
            for x in inv.extra_links
            )
        self.inv          = inv
        self.type_name    = _T (obj.ui_name)
        self.ui_display   = obj.ui_repr
        self.args         = (self.type_name, self.ui_display)
        description       = _T (inv.description)
        try :
            self.inv_desc = description % TFL.Caller.Object_Scope (obj)
        except TypeError :
            self.inv_desc = description
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        return self.description
    # end def as_unicode

    @Once_Property
    def head (self) :
        return \
            ( _T
                ( "The new definition of %s %s would clash with %s "
                  "existing entities"
                )
            % (self.type_name, self.ui_display, self.count)
            )
    # end def head

    @Once_Property
    def description (self) :
        result = [self.inv_desc] if self.inv_desc else []
        result.append  (self.head)
        extras = tuple (x.ui_display for x in self.extra_links)
        result.append \
            ( _T ("Already existing:\n    %s") % ("\n    ".join (extras), ))
        return "\n  ".join (result)
    # end def description

# end class Not_Unique

class Partial_Type (Error) :
    """Raised when creation of an object of a partial type is tried."""
# end class Partial_Type

class Permission (_Invariant_, ValueError) :
    """You are not allowed to use that object in this context"""

    class inv :
        name       = "Permission_Error"

    def __init__ (self, obj, attr, val, allowed) :
        self.__super.__init__ (obj)
        self.args         = (obj, attr, val.ui_display)
        self.obj          = obj
        self.attribute    = attr
        self.attributes   = (attr.name, )
        self.is_required  = attr.is_required
        self.value        = val.ui_display
        self.allowed      = tuple (x.ui_display for x in allowed)
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        attr   = self.attribute
        result = \
            ( _T( "Permission error for : `%r`"
                  "\n     allowed  values : (%s)"
                  "\n     got      value  : `%s`"
                )
            % (attr, ", ".join (self.allowed), self.value)
            )
        return result
    # end def as_unicode

    @Once_Property
    def bindings (self) :
        return ((self.attribute.name, self.value), )
    # end def bindings

    @Once_Property
    def head (self) :
        return unicode (self)
    # end def head

# end class Permission

class Quant (Invariant) :
    """Raised when a quantifier invariant of a MOM object/link is violated."""

    def __init__ (self, obj, inv, violators, violators_attr) :
        self.violators      = violators
        self.violators_attr = violators_attr
        self.__super.__init__ (obj, inv)
    # end def __init__

    @Once_Property
    def bindings (self) :
        result = sorted \
            (itertools.chain (self.__super.bindings, self._violator_values ()))
        return result
    # end def bindings

    def _violator_values (self) :
        bvars = inv.bvar [1:-1].split (",")
        for v, d in paired (self.violators, self.violators_attr) :
            if len (bvars) > 1 and isinstance (v, (list, tuple)) :
                for k, v in paired (bvars, v) :
                    yield (str (k), repr (r))
            elif isinstance (v, (list, tuple)) :
                yield \
                    (str (inv.bvar), "[%s]" % (", ".join (map (unicode, v)), ))
            else :
                yield (str (inv.bvar), repr (v))
            if d :
                try :
                    items = d.iteritems ()
                except AttributeError :
                    val = repr (d)
                else :
                    val = sorted \
                        ((str (a), repr (x)) for (a, x) in items)
                yield repr (v), val
    # end def _violator_values

# end class Quant

class Readonly_DB (DB) :
    """Database is set to readonly."""
# end class Readonly_DB

class Required_Empty (Invariant) :
    """Primary attribute must not be empty."""

    is_required    = True

# end class Required_Empty

class Required_Missing (_Invariant_) :
    """Raised when required attributes are missing."""

    arg_sep        = "; "
    is_required    = True

    class inv :
        name       = "required_not_missing"

    def __init__ \
            (self, e_type, needed, missing, epk, kw, kind = _("required")) :
        kw  = dict   (kw)
        raw = kw.pop ("raw", False)
        self.__super.__init__ (e_type, raw)
        self.e_type     = e_type
        self.attributes = self.needed = needed
        self.missing    = missing
        self.epk        = tuple (repr (x) for x in epk)
        self.kw         = kw
        self.kind       = kind
        self.args       = (self.head, self.description)
    # end def __init__

    @Once_Property
    def as_json_cargo (self) :
        result = self.__super.as_json_cargo
        missing_t = self.missing_t
        if missing_t :
            result ["missing_t"] = missing_t
        return result
    # end def as_json_cargo

    @Once_Property
    def head (self) :
        n = len (self.needed)
        return  \
            (  _Tn ( "%s needs the %s attribute: %s"
                   , "%s needs the %s attributes: %s"
                   , n
                   )
            % (_T (self.e_type.ui_name), _T (self.kind), self.needed)
            )
    # end def head

    @Once_Property
    def description (self) :
        return \
            ( _T ("Instead it got: (%s)")
            % (", ".join
                  ( itertools.chain
                      ( self._formatted_bindings
                          (zip (self.e_type.epk_sig, self.epk))
                      , self._formatted_bindings (self.kw.iteritems ())
                      )
                  )
              )
            )
    # end def description

    @Once_Property
    def explanation (self) :
        return _T ("All required attributes must be supplied")
    # end def explanation

    @Once_Property
    def missing_t (self) :
        AQ = self.e_type.AQ
        def _gen (AQ, missing) :
            for m in missing :
                t = list \
                    ( a._attr.name
                    for a in getattr (AQ, m).Attrs
                    if  a._attr.is_required
                    )
                if t :
                    yield m, t
        return dict (_gen (self.e_type.AQ, self.missing))
        return tuple \
            ( itertools.chain
                ( a._full_name
                for m in self.missing
                for a in getattr (AQ, m).Attrs
                if  a._attr.is_required
                )
            )
    # end def missing_t

# end class Required_Missing

class Too_Many_Objects (Error) :
    """Raised when too many objects are created."""

    def __init__ (self, obj, max_count) :
        self.__super.__init__ \
            ( _T ("Cannot create more than %d objects of %s")
            % (max_count, _T (obj.ui_name))
            )
    # end def __init__

# end class Too_Many_Objects

class Wrong_Type (Error) :
    """Raised when an instance of inccorect type is passed to an attribute."""
# end class Wrong_Type

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.Error
