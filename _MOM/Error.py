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
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _TFL                     import TFL
from   _MOM                     import MOM

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import *
from   _TFL.Record              import Record

import _TFL.Caller
import _TFL.Accessor
import _TFL.I18N

import itertools

class Exception_Handled (BaseException) :
    """Raised after an exception was already handled to bail out from an
       arbitrary position in a call-tree. Should be ignored further up.
    """
# end class Exception_Handled

class Error (Exception) :
    """Root class of MOM exceptions"""

    arg_sep     = ", "
    is_required = False

    @Once_Property
    def as_str (self) :
        return TFL.I18N.encode_o (unicode (self))
    # end def as_str

    @Once_Property
    def as_unicode (self) :
        return self.arg_sep.join (self.str_arg (self.args))
    # end def as_unicode

    def str_arg (self, args) :
        return (unicode (a) for a in args if a)
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

    def __init__ (self, obj) :
        self.obj            = obj
        self.violators      = ()
        self.violators_attr = ()
        self.attributes     = ()
        self.extra_links    = ()
    # end def __init__

    ### redefine in descendents
    def name            (self)                  : return _T ("Invariant error")
    def description     (self, indent = "")     : return ""
    def explanation     (self, indent = "")     : return ""
    def assertion       (self, indent = "")     : return ""

    ### just for compatibility with Quant
    def violator_values (self, indent = "    ") : return ()

    def _clean_this (self, s) :
        s = s.replace ("this.", "")
        s = s.replace (".name", "")
        return s
    # end def _clean_this

# end class _Invariant_

class Attribute (Error) :

    def __init__ (self, entity, name, val, kind = "unknown", exc = None) :
        msg = \
            ( _T ("Can't set %s attribute %s.%s to `%r`")
            % (kind, entity.type_base_name, name, val)
            )
        if exc :
            msg = "%s\n    %s" % (msg, exc)
        self.args      = (msg, )
        self.entity    = entity
        self.kind      = kind
        self.attribute = name
        self.value     = val
    # end def __init__

    def correct (self) :
        pass
    # end def correct

# end class Attribute

class Attribute_Set (Attribute, AttributeError) :
    """Attribute can't be set."""

# end class Attribute_Set

class Attribute_Syntax (_Invariant_, ValueError) :
    """Raised for syntax errors in attributes of MOM objects/links."""

    def __init__ (self, obj, attr, val, exc_str = "") :
        _Invariant_.__init__ (self, obj)
        self.args         = (obj, attr, val, exc_str)
        self.obj          = obj
        self.attributes   = (attr, )
        self.attr         = attr
        self.is_required  = attr.is_required
        self.val          = val
        self.exc_str      = exc_str
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        result = \
            ( _T ( "`%s` for : `%r`"
                   "\n     expected type  : `%s`"
                   "\n     got      value : `%s`"
                   "\n     of       type  : `%s`"
                 )
            % ( self.exc_str or _T ("Syntax error")
              , self.attr, self.attr.typ, self.val, type (self.val)
              )
            )
        if self.attr.syntax :
            result = "\n".join ((result, self.attr.syntax))
        return result
    # end def as_unicode

    def assertion (self) :
        result = \
            ( _T ("Syntax error: \n  expected type `%s`\n  got value `%s`")
            % (self.attr.typ, self.val)
            )
        if self.attr.syntax :
            result = "%s\n    %s: %s" % \
                (result, _T ("Syntax"), self.attr.syntax)
        if self.exc_str :
            result = "%s\n    %s: %s" % \
                (result, _T ("Exception"), self.exc_str)
        return result
    # end def assertion

    def name (self) :
        return "Invalid Attribute `%s'" % (self.attr.name, )
    # end def name

    def description (self, indent = "") :
        return self.assertion ()
    # end def description

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

    def __init__ (self, obj, inv, violators = (), violators_attr = ()) :
        _Invariant_.__init__ (self, obj)
        self.args           = (obj, inv, violators, violators_attr)
        self.inv            = inv
        self.is_required    = inv.is_required
        self.attributes     = inv.attributes + inv.attr_none
        self.extra_links    = list (inv.extra_links ())
        self.val_dict       = dict (inv.val_dict)
        self.val_desc       = dict (inv.val_desc)
        self.violators      = violators
        self.violators_attr = violators_attr
        description         = inv.description
        try :
            self.inv_desc   = description % TFL.Caller.Object_Scope (obj)
        except TypeError :
            self.inv_desc   = description
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        return self._as_string \
            ( "%s `%s` " % (_T ("Condition"), _T (self.inv.name))
            + ": %s %s%s"
            , "    "
            )
    # end def as_unicode

    def assertion (self, indent = "    ") :
        return self._as_string ("%s\n" + indent + "%s%s", indent)
    # end def assertion

    def attribute_values (self, head = None) :
        return self._attribute_values (self.val_dict, head)
    # end def attribute_values

    def description (self, indent = "") :
        result = self._tail (indent)
        inv    = self.inv
        if inv.description and inv.assertion :
            result = ("\n" + indent).join \
                (["`%s`" % inv.assertion, "", result])
        return self._clean_this (result)
    # end def description

    def explanation (self, indent = "") :
        return self.inv.explanation
    # end def explanation

    def name (self) :
        return self.inv_desc or self.inv.assertion
    # end def name

    def parameter_values (self, head = None) :
        return self._attribute_values (self.val_desc, head)
    # end def parameter_values

    def _as_string (self, format, indent = "    ") :
        inv = self.inv
        ass = inv.assertion
        if ass :
            ass = "(%s)" % (ass, )
        return self._clean_this \
            (format % (self.inv_desc, ass, self._tail (indent)))
    # end def _as_string

    def _attribute_values (self, dict, head = None) :
        tail = head or []
        for attr, val in sorted (dict.items ()) :
            if attr != "this" :
                tail.append ("%s = %r" % (attr, val))
        return tail
    # end def _attribute_values

    def _tail (self, indent = "    ") :
        result = self.parameter_values (self.attribute_values ())
        more   = self.inv.error_info   ()
        if more :
            if isinstance (more, (str, unicode)) :
                result.append (more)
            else :
                result.extend (more)
        if result :
            result.insert (0, "")
        return ("\n" + indent).join (result)
    # end def _tail

# end class Invariant

class Invariants (Error) :

    arg_sep = "\n  "

    def __init__ (self, errors) :
        errors = self.errors = sorted (errors, key = TFL.Getter.inv.name)
        Error.__init__ (self, errors)
    # end def __init__

    @property
    def any_required_empty (self) :
        return any (isinstance (e, Required_Empty) for e in self.errors)
    # end def any_required_empty

    def str_arg (self, args) :
        result = []
        add    = result.append
        for a in args [0] :
            try :
                add (unicode (a))
            except StandardError as exc :
                add ("%s --> %s" % (repr (a), exc))
        return result
    # end def str_arg

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
        self.args = \
            ( _T ("Maximum number of links for %s is %d %s")
            % (etype, max_links, args)
            ,
            )
    # end def __init__

# end class Multiplicity

class Multiplicity_Errors (Error) :
    pass
# end class Multiplicity_Errors

class Name_Clash (Error) :
    """Raised when one name is used for more than one object."""

    arg_sep = " "

    def __init__ (self, new, old) :
        otn = old.type_name if old else ""
        self.args = \
            ( _T ("new definition of %s %s clashes with existing %s %s")
            % (new.type_name, new, otn, old or _T ("object"))
            ,
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

    Ancestor = __Ancestor = Invariant

    def violator_values (self, indent = "    ", sep = ", ") :
        inv  = self.inv
        result = []
        bvars  = inv.bvar [1:-1].split (",")
        for v, d in paired (self.violators, self.violators_attr) :
            if len (bvars) > 1 and isinstance (v, (list, tuple)) :
                result.append \
                    (sep.join (map (self._violator_value, paired (bvars, v))))
            elif isinstance (v, (list, tuple)) :
                result.append \
                    ("%s : [%s]" % (inv.bvar, ", ".join (map (unicode, v))))
            elif type (v) != type (self) : ### v is not a class instance
                result.append ("%s : %s" % (inv.bvar, v))
            else :
                result.append \
                    ("%s = `%s'" % (inv.bvar, getattr (v, "name", v)))
            if d :
                try :
                    items = d.items ()
                except AttributeError :
                    result.append (d)
                else :
                    result.append \
                        ( indent
                        + sep.join
                              (   "%s = %s" % (a, val)
                              for (a, val) in sorted (d.iteritems ())
                              )
                        )
        return result
    # end def violator_values

    def _tail (self, indent = "    ") :
        result = self.__Ancestor._tail (self, indent)
        tail   = self.violator_values  ()
        if tail :
            tail.insert (0, "")
        return "%s%s" % (result, ("\n" + indent).join (tail))
    # end def _tail

    def _violator_value (self, x) :
        n, o = x
        if isinstance (o, Record) :
            v = o
        else :
            v = getattr (o, "name", o)
        return "%s : `%s'" % (n, v)
    # end def _violator_value

# end class Quant

class Readonly_DB (DB) :
    """Database is set to readonly."""
# end class Readonly_DB

class Required_Empty (Invariant) :
    """Primary attribute must not be empty."""

# end class Required_Empty

class Required_Missing (Error) :
    """Raised when required attributes are missing."""

    arg_sep        = " "
    extra_links    = []
    inv_desc       = _ ("All required attributes must be supplied")
    is_required    = True
    val_dict       = {}
    val_desc       = {}
    violators      = ()
    violators_attr = ()

    class inv :
        name       = "required_not_missing"

    def __init__ (self, e_type, needed, missing, epk, kw) :
        self.e_type     = e_type
        self.attributes = self.needed = needed
        self.missing    = missing
        self.epk        = epk
        self.kw         = kw
        self.args       = \
            ( _T  ("%s needs the required attributes: %s")
            % (e_type.type_name, needed)
            , _T ("Instead it got: (%s)")
            % (", ".join
                  ( itertools.chain
                      ( (repr (x) for x in epk)
                      , ("%s = %r" % (k, v) for k, v in kw.iteritems ())
                      )
                  )
              )
            )
    # end def __init__

# end class Required_Missing

class Too_Many_Objects (Error) :
    """Raised when too many objects are created."""

    def __init__ (self, obj, max_count) :
        self.args = \
            ( _T ("Cannot create more than %d objects of %s")
            % (max_count, obj.type_name)
            ,
            )
    # end def __init__

# end class Too_Many_Objects

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.Error
