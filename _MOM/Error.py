# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2008 Mag. Christian Tanzer. All rights reserved
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
#    TOM.Error
#
# Purpose
#    Provide exception classes for TOM
#
# Revision Dates
#     2-Aug-1999 (CT) Creation (factored from TTA.py)
#     2-Aug-1999 (CT) `Locked_Attribute' added
#     4-Oct-1999 (CT) `Invariant.__init__': take `inv.attr_none' into account
#    17-Nov-1999 (CT) `__cmp__' and `__hash__' added
#    18-Nov-1999 (CT) `Attribute_Syntax_Error.__str__': use string
#                     interpolation instead of string addition
#     3-Dec-1999 (CT) `Invariant_Error_': set `self.attributes'
#    19-Jan-2000 (CT) `assertion': put text of assertion in separate line
#    24-Jan-2000 (CT) `Undefined_Object' added
#    25-Jan-2000 (CT) `Undefined_Object' renamed to `Undefined_Cross_Ref'
#    25-Jan-2000 (CT) `Unknown_Assoc' added
#     3-Feb-2000 (CT) `Invariant_Error._attribute_values' factored
#     3-Feb-2000 (CT) `_clean_this' used
#    21-Jun-2000 (CT) `Quant_Error.violator_values': formatting changed
#    21-Jun-2000 (CT) 2 calls to `_clean_this' added to `Quant_Error'
#    27-Jul-2000 (MY) `Frame_Address_Error' added
#     3-Aug-2000 (MY) `Frame_Address_Error' renamed to `MEDLerror'
#    14-Sep-2000 (CT) `User_RDA_Module_Error' added
#    15-Mar-2001 (CT) `Link_Scope_Mix_Error' added
#     8-Oct-2001 (CT) `Quant_Error._violator_value` factored and made more
#                     robust
#     7-Nov-2001 (CT) Inherit from `StandardError` instead of `Exception`
#     7-Nov-2001 (CT) Specialcased `Record` instance in `_violator_value`
#    12-Nov-2001 (CT) `violator_values` made more robust
#    18-Apr-2002 (MY) Rename MEDLerror to MEDL_Error
#    25-Apr-2002 (MY) Remove MEDL_Error
#     4-Jun-2002 (CT) `No_Such_Link` added
#    18-Jun-2002 (CT) `Quant_Error` made descendent of `Invariant_Error`
#                     - major refactorings in `Invariant_Error` and
#                       `Quant_Error`
#    10-Jul-2002 (CT) `Circular_Link` added
#     6-Aug-2002 (CT) `violator_values` corrected
#    17-Oct-2002 (CT) `_attribute_values` corrected (use `%` instead of
#                     string concatenation of `repr`)
#    19-Dec-2002 (CT) `Cannot_Rename_Root_Object` added
#     6-Feb-2003 (CT) `inv.error_info` added to `Invariant_Error._tail`
#     6-Feb-2003 (CT) s/Invariant_Error_/_Invariant_Error_/g
#    10-Feb-2003 (CT) `extra_links` added
#    17-Feb-2003 (CED) `Kind_Not_Valid_For_App_Type` added
#    10-Apr-2003 (CT)  `Attribute_Syntax_Error` fixed
#     8-May-2003 (CT)  `Attribute_Syntax_Error` fixed, again
#     8-May-2003 (CT)  `Attribute_Syntax_Error` derived from `ValueError`, too
#     7-Oct-2003 (CT)  `Attribute_Syntax_Error.__str__` changed to show
#                      `exc_str`
#    14-Jun-2004 (CT)  `Exception_Handled` added
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#    11-Nov-2004 (CT)  `Invariant_Error.inv_desc` added and used
#    14-Apr-2005 (CT)  Use `isinstance` instead of `type` comparison
#     4-May-2006 (CT)  `Attribute_Syntax_Error.__str__` changed to not
#                      display class, anymore
#     1-Jun-2006 (CT)  Use `type_name` instead of `__class__.__name__`
#     1-Jun-2006 (CT)  Style
#    15-Jun-2006 (CT)  Use `Documenter.description` and
#                      `Documenter.explanation`
#     6-Jul-2006 (CT)  Use `app_type.doc_translation` in `Invariant_Error`
#                      and `Attribute_Syntax_Error` (`name`, `description`)
#     1-Aug-2006 (CT)  `obj` and `doc_translator` added to `_Invariant_Error_`
#     1-Aug-2006 (CT)  `doc_translator` used instead of home-grown code
#     1-Aug-2006 (CT)  `extra_links` run through `doc_translator`
#     2-Aug-2006 (CT)  Yesterday's code corrected to only run strings in
#                      `extra_links` through `doc_translator`
#     9-Aug-2006 (CT)  `__cmp__` and `__hash__` changed to use `str (self)`
#    29-Aug-2006 (MZO) [21185] `__cmp__` fixed
#    04-Jul-2007 (CED) User RDAs removed
#    23-Jul-2007 (CED) Activated absolute_import
#     4-Apr-2008 (CT)  Exceptions factored in here from TOM.DB_File
#    ««revision-date»»···
#--

from __future__ import absolute_import

from   _TFL           import TFL
from   _TOM           import TOM
import _TFL.Caller

from   copy           import copy
from   _TFL.predicate import *
from   _TFL.Record    import Record

class Exception_Handled (Exception) :
    """Raised after an exception was already handled to bail out from an
       arbitrary position in a call-tree. Should be ignored further up.
    """
# end class Exception_Handled

class Error (StandardError) :
    """Root class of TOM exceptions"""

    arg_sep = ", "

    def __str__ (self) :
        return "%s : %s" % \
            ( self.__class__.__name__
            , self.arg_sep.join (self.str_arg (self.args))
            )
    # end def __str__

    def str_arg (self, args) :
        return map (str, args)
    # end def str_arg

    def __cmp__ (self, other) :
        return cmp (str (self), str (other))
    # end def __cmp__

    def __hash__ (self) :
        return hash (str (self))
    # end def __hash__

# end class Error

class Undefined_Cross_Ref (Error) :
    """Raised when a cross-referenced object/link is undefined or the
       cross-referenced attribute of that entity is undefined.
    """
    pass

class Unknown_Assoc (Error) :
    """Raised when a cross-referenced link refers to an unknown association."""
    pass

class Name_Clash (Error) :
    """Raised when one name is used for more than one object."""
    arg_sep = " "

    def __init__ (self, new, old) :
        self.args = ("new definition of", new, "clashes with existing", old)
    # end def __init__

class Invalid_Name (Error) :
    """Raised when an invalid name is given for an object to be created."""
    pass

class Invalid_Seq_Nr (Error) :
    """Raised when an invalid sequence number is given for an ordered link to be created."""
    pass

class Partial_Type (Error) :
    """Raised when creation of an object of a partial type is tried."""
    pass

class No_Such_Directory (Error) :
    """Raised for a file specification containing a non-existent directory."""
    pass

class No_Such_File (Error) :
    """Raised for a file specification of a non-existing file."""
    pass

class No_Such_Link (Error) :
    """Raised if names/objects are passed to association which aren't linked."""
    pass

class Too_Many_Objects (Error) :
    """Raised when too many objects are created."""

    arg_sep = " "

    def __init__ (self, obj, max_count) :
        self.args = \
            "cannot create more than", max_count, "objects of", obj.type_name
    # end def __init__

# end class Too_Many_Objects

class Duplicate_Link (Error) :
    """Raised when a link is added to an association more than once."""
    pass

class Duplicate_Seq_Nr (Error) :
    """Raised when a sequence number is added to an ordered association more than once."""
    pass

class Assoc_Link_Error (Error) :
    """Raised when a link of wrong type is added to an association."""
    pass

class Empty_Link_Error (Error) :
    """Raised when an empty link is added to an association."""
    pass

class Link_Type_Error (Error) :
    """Raised when a link is created with wrong object types."""
    pass

class Link_Scope_Mix_Error (Error) :
    """Raised when objects with different home scopes are put into a link."""
    pass

class Circular_Link (Error) :
    """Raised when a link is added to an association which results directly or indirectly in a circular link."""
    pass

class Incomplete_Assoc_Error (Error) :
    """Raised when an association without link type is defined."""
    pass

class Multiplicity_Error (Error) :
    """Raised when the maximum multiplicity for an association is violated."""

    def __repr__ (self) :
        args = self.args
        return "Maximum number of links for %s is %d %s" % \
            (args [0], args [1], args [2:])
    # end def __repr__

# end class Multiplicity_Error

class Multiplicity_Errors (Error) :
    pass

class Inconsistent_Attribute (Error) :
    pass

class Locked_Attribute (Error) :
    pass

class _Invariant_Error_ (Error) :

    def __init__ (self, obj) :
        self.obj            = obj
        self.doc_translator = obj.app_type.doc_translation
        self.violators      = ()
        self.violators_attr = ()
        self.attributes     = ()
        self.extra_links    = ()
    # end def __init__

    ### redefine in descendents
    def name            (self)                  : return "Invariant error"
    def description     (self, indent = "")     : return ""
    def explanation     (self, indent = "")     : return ""
    def assertion       (self, indent = "")     : return ""

    ### just for compatibility with Quant_Error
    def violator_values (self, indent = "    ") : return ()

    def _clean_this (self, s) :
        s = s.replace ("this.", "")
        s = s.replace (".name", "")
        return s
    # end def _clean_this

# end class _Invariant_Error_

class Invariant_Error (_Invariant_Error_) :

    def __init__ (self, obj, inv, violators = (), violators_attr = ()) :
        _Invariant_Error_.__init__ (self, obj)
        self.args           = (obj, inv, violators, violators_attr)
        self.inv            = inv
        self.attributes     = inv.attributes + inv.attr_none
        dt                  = self.doc_translator
        self.extra_links    = sel = []
        for el in inv.extra_links () :
            if isinstance (el, basestring) :
                el = dt (el)
            sel.append (el)
        self.val_dict       = copy (inv.val_dict)
        self.val_desc       = copy (inv.val_desc)
        self.violators      = violators
        self.violators_attr = violators_attr
        description         = obj.Documenter.description (inv)
        try :
            self.inv_desc   = description % TFL.Caller.Object_Scope (obj)
        except TypeError :
            self.inv_desc   = description
    # end def __init__

    def _as_string (self, format, indent = "    ") :
        inv = self.inv
        ass = inv.assertion
        if ass :
            ass = "(%s)" % (ass, )
        return self._clean_this \
            (format % (self.inv_desc, ass, self._tail (indent)))
    # end def _as_string

    def assertion   (self, indent = "    ") :
        return self._as_string ("%s\n" + indent + "%s%s", indent)
    # end def assertion

    def _attribute_values (self, dict, head = None) :
        tail = head or []
        for attr, val in dict.items () :
            if attr != "this" :
                tail.append ("%s = %s" % (attr, val))
        return tail
    # end def _attribute_values

    def attribute_values (self, head = None) :
        return self._attribute_values (self.val_dict, head)
    # end def attribute_values

    def description (self, indent = "") :
        result = self._tail (indent)
        inv    = self.inv
        if inv.description and inv.assertion :
            result = ("\n" + indent).join \
                (["`%s`" % inv.assertion, "", result])
        return self.doc_translator (self._clean_this (result))
    # end def description

    def explanation (self, indent = "") :
        return self.obj.Documenter.explanation (self.inv)
    # end def explanation

    def name (self) :
        return self.doc_translator (self.inv_desc or self.inv.assertion)
    # end def name

    def parameter_values (self, head = None) :
        return self._attribute_values (self.val_desc, head)
    # end def parameter_values

    def __str__ (self) :
        return self._as_string \
            ( "Condition `%s` " % (self.obj.Documenter.name (self.inv), )
            + ": %s %s%s"
            , "    "
            )
    # end def __str__

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

# end class Invariant_Error

class Quant_Error (Invariant_Error) :
    """Raised when a quantifier invariant of a TOM object/link is violated."""

    Ancestor = __Ancestor = Invariant_Error

    def _tail (self, indent = "    ") :
        result = self.__Ancestor._tail (self, indent)
        tail   = self.violator_values  ()
        if tail :
            tail.insert (0, "")
        return "%s%s" % (result, ("\n" + indent).join (tail))
    # end def _tail

    def _violator_value (self, (n, o)) :
        if isinstance (o, Record) :
            v = o
        else :
            v = getattr (o, "name", o)
        return "%s : `%s'" % (n, v)
    # end def _violator_value

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
                    ("%s : [%s]" % (inv.bvar, ", ".join (map (str, v))))
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

# end class Quant_Error

class Attribute_Syntax_Error (_Invariant_Error_, ValueError) :
    """Raised for syntax errors in attributes of TOM objects/links."""

    def __init__ (self, obj, attr, val, exc_str = "") :
        _Invariant_Error_.__init__ (self, obj)
        self.args       = (obj, attr, val, exc_str)
        self.obj        = obj
        self.attributes = (attr, )
        self.attr       = attr
        self.val        = val
        self.exc_str    = exc_str
    # end def __init__

    def name (self) :
        return "Invalid Attribute `%s'" % (self.attr.name, )
    # end def name

    def description (self, indent = "") :
        return self.doc_translator (self.assertion ())
    # end def description

    def __str__ (self) :
        return ( ("`%s` for : `%s'"
                  "\n     expected type  : `%s'"
                  "\n     got      value : `%s'"
                  "\n     of       type  : `%s`"
                 )
               % ( self.exc_str or "Syntax error"
                 , self.attr, self.attr.typ, self.val, type (self.val)
                 )
               )
    # end def __str__

    def assertion (self) :
        ### XXX Add `attr.syntax`
        result = ( "Syntax error: \n  expected type `%s'\n  got value `%s'"
                 % (self.attr.typ, self.val)
                 )
        if self.attr.syntax :
            result = "%s\n    Syntax: %s" % (result, self.attr.syntax)
        if self.exc_str :
            result = "%s\n    Exception: %s" % (result, self.exc_str)
        return result
    # end def assertion

# end class Attribute_Syntax_Error

class Invariant_Errors (Error) :

    def str_arg (self, args) :
        result = []
        add    = result.append
        for a in args [0] :
            try :
                add (str (a))
            except KeyboardInterrupt :
                raise
            except StandardError, exc :
                add ("%s --> %s" % (repr (a), exc))
        return result
    # end def str_arg

# end class Invariant_Errors

class Invalid_Attribute_Type (Error) :
    pass
# end class Invalid_Attribute_Type

class Already_Editing (Error) :
    pass
# end class Already_Editing

class Type_Not_In_Scope (Error) :
    pass

class Cannot_Rename_Root_Object (Error) :
    pass

class Kind_Not_Valid_For_App_Type (Error) :
    pass

class DB_Error                (StandardError) : pass
class Incompatible_DB_Version (DB_Error)      : pass
class Empty_DB                (DB_Error)      : pass

if __name__ != "__main__" :
    TOM._Export_Module ()
### __END__ TOM.Error
