# -*- coding: iso-8859-15 -*-
# Copyright (C) 2008-2012 Mag. Christian Tanzer. All rights reserved
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

class Error (Exception) :
    """Root class of MOM exceptions"""

    __metaclass__    = TFL.Meta.Object.__class__

    arg_sep          = ", "
    is_required      = False

    _json_map        = dict \
        ( as_unicode = "description"
        )

    _json_attributes = \
        ( "as_unicode"
        , "is_required"
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
        return self.arg_sep.join (self.str_arg (self.args))
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

# end class Error

class _Invariant_ (Error) :

    attributes       = ()
    description      = ""
    description_plus = ""
    explanation      = ""
    extra_links      = ()
    indent           = " " * 4
    val_disp         = {}

    _json_attributes = \
        ( "attributes"
        , "bindings"
        , "description"
        , "explanation"
        , "head"
        , "is_required"
        )

    def __init__ (self, obj, raw = False) :
        self.obj = obj
        self.raw = raw
    # end def __init__

    @Once_Property
    def as_json_cargo (self) :
        result = self.__super.as_json_cargo
        xtra   = list \
            (   pid
            for pid in (getattr (x, "pid", None) for x in self.extra_links)
            if  pid is not None
            )
        if xtra :
            result ["extra_links"] = xtra
        return result
    # end def as_json_cargo

    @Once_Property
    def bindings (self) :
        return sorted (self.val_disp.iteritems ())
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
            elif v is not None :
                v = ("%r" if self.raw else "%s") % (v, )
                if v.startswith (('u"', "u'")) :
                    v = v [1:]
            yield "%s = %s" % (k, v)
    # end def _formatted_bindings

# end class _Invariant_

class Attribute (Error) :

    _json_attributes = \
        ( "as_unicode"
        , "attributes"
        , "bindings"
        , "is_required"
        )

    def __init__ (self, entity, name, val, kind = "unknown", exc = None) :
        msg = \
            ( _T ("Can't set %s attribute %s.%s to `%r`")
            % (kind, entity.type_base_name, name, val)
            )
        if exc :
            msg = "%s\n    %s" % (msg, exc)
        self.args       = (msg, )
        self.entity     = entity
        self.kind       = kind
        self.attribute  = name
        self.attributes = (name, )
        self.value      = val
    # end def __init__

    @Once_Property
    def bindings (self) :
        return ((self.attribute, self.value), )
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
        self.attributes   = (attr, )
        self.is_required  = attr.is_required
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
        return ((self.attribute, self.value), )
    # end def bindings

    @Once_Property
    def head (self) :
        return \
            ( _T ("Syntax error: \n  expected type `%s`\n  got value `%s`")
            % (self.attribute.typ, self.value)
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

class Duplicate_Link (Error) :
    """Raised when a link is added to an association more than once."""
# end class Duplicate_Link

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
        self.args           = (obj, inv)
        self.inv            = inv
        self.is_required    = inv.is_required
        self.attributes     = sorted (inv.attributes + inv.attr_none)
        self.extra_links    = list   (inv.extra_links)
        self.val_disp       = dict   (inv.val_disp)
        description         = inv.description
        try :
            self.inv_desc   = description % TFL.Caller.Object_Scope (obj)
        except TypeError :
            self.inv_desc   = description
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
        errors = self.errors = sorted (errors, key = TFL.Getter.inv.name)
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

# end class Invariants

class Link_Scope_Mix (Error) :
    """Raised when objects with different home scopes are put into a link."""
# end class Link_Scope_Mix

class Link_Type (Error) :
    """Raised when a link is created with wrong object types."""
# end class Link_Type

class Multiplicity (Error) :
    """Raised when the maximum multiplicity for an association is violated."""

    def __init__ (self, etype, max_links, * args) :
        self.__super.__init__ \
            ( _T ("Maximum number of links for %s is %d %s")
            % (etype, max_links, args)
            )
    # end def __init__

# end class Multiplicity

class Multiplicity_Errors (Error) :

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
        self.__super.__init__ \
            ( _T ("new definition of %s %s clashes with existing %s %s")
            % (_T (new.ui_name), new, otn, old or _T ("object"))
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

class Partial_Type (Error) :
    """Raised when creation of an object of a partial type is tried."""
# end class Partial_Type

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

    def __init__ (self, e_type, needed, missing, epk, kw, raw = False) :
        kw  = dict   (kw)
        raw = kw.pop ("raw", raw)
        self.__super.__init__ (e_type, raw)
        self.e_type     = e_type
        self.attributes = self.needed = needed
        self.missing    = missing
        self.epk        = epk
        self.kw         = kw
        self.args       = (self.head, self.description)
    # end def __init__

    @Once_Property
    def head (self) :
        return  \
            (  _T ("%s needs the required attributes: %s")
            % (_T (self.e_type.ui_name), self.needed)
            )
    # end def head

    @Once_Property
    def description (self) :
        return \
            ( _T ("Instead it got: (%s)")
            % (", ".join
                  ( itertools.chain
                      ( (repr (x) for x in self.epk)
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

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.Error
