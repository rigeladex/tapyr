# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2009 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Error
#
# Purpose
#    Provide exception classes for MOM
#
# Revision Dates
#    18-Sep-2009 (CT) Creation (factored from TOM.Error)
#    12-Oct-2009 (CT) `Invalid_Primary_Key` added
#    ««revision-date»»···
#--

from   _TFL           import TFL
from   _MOM           import MOM

from   _TFL.predicate import *
from   _TFL.Record    import Record

import _TFL.Caller

class Exception_Handled (Exception) :
    """Raised after an exception was already handled to bail out from an
       arbitrary position in a call-tree. Should be ignored further up.
    """
# end class Exception_Handled

class Error (StandardError) :
    """Root class of MOM exceptions"""

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
# end class Undefined_Cross_Ref

class Unknown_Assoc (Error) :
    """Raised when a cross-referenced link refers to an unknown association."""
# end class Unknown_Assoc

class Name_Clash (Error) :
    """Raised when one name is used for more than one object."""

    arg_sep = " "

    def __init__ (self, new, old) :
        self.args = ("new definition of", new, "clashes with existing", old)
    # end def __init__

# end class Name_Clash

class Invalid_Name (Error) :
    """Raised when an invalid name is given for an object to be created."""
# end class Invalid_Name

class Invalid_Primary_Key (Error) :
    """Raised when an invalid primary key is given for an identified entity to be created."""
# end class Invalid_Name

class Invalid_Seq_Nr (Error) :
    """Raised when an invalid sequence number is given for an ordered link to be created."""
# end class Invalid_Seq_Nr

class Partial_Type (Error) :
    """Raised when creation of an object of a partial type is tried."""
# end class Partial_Type

class No_Such_Directory (Error) :
    """Raised for a file specification containing a non-existent directory."""
# end class No_Such_Directory

class No_Such_File (Error) :
    """Raised for a file specification of a non-existing file."""
# end class No_Such_File

class No_Such_Link (Error) :
    """Raised if names/objects are passed to association which aren't linked."""
# end class No_Such_Link

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
# end class Duplicate_Link

class Duplicate_Seq_Nr (Error) :
    """Raised when a sequence number is added to an ordered association more than once."""
# end class Duplicate_Seq_Nr

class Assoc_Link_Error (Error) :
    """Raised when a link of wrong type is added to an association."""
# end class Assoc_Link_Error

class Empty_Link_Error (Error) :
    """Raised when an empty link is added to an association."""
# end class Empty_Link_Error

class Link_Type_Error (Error) :
    """Raised when a link is created with wrong object types."""
# end class Link_Type_Error

class Link_Scope_Mix_Error (Error) :
    """Raised when objects with different home scopes are put into a link."""
# end class Link_Scope_Mix_Error

class Circular_Link (Error) :
    """Raised when a link is added to an association which results directly or indirectly in a circular link."""
# end class Circular_Link

class Incomplete_Assoc_Error (Error) :
    """Raised when an association without link type is defined."""
# end class Incomplete_Assoc_Error

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
# end class Multiplicity_Errors

class Inconsistent_Attribute (Error) :
    pass
# end class Inconsistent_Attribute

class Locked_Attribute (Error) :
    pass
# end class Locked_Attribute

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
        self.val_dict       = dict (inv.val_dict)
        self.val_desc       = dict (inv.val_desc)
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
    """Raised when a quantifier invariant of a MOM object/link is violated."""

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
    """Raised for syntax errors in attributes of MOM objects/links."""

    def __init__ (self, obj, attr, val, exc_str = "") :
        ### XXX ### _Invariant_Error_.__init__ (self, obj)
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
            except StandardError, exc :
                add ("%s --> %s" % (repr (a), exc))
        return result
    # end def str_arg

# end class Invariant_Errors

class Invalid_Attribute (Error, AttributeError) :

    def __init__ (self, entity, name, val, kind = "unknown") :
        self.args = \
            ( ( "Can't set %s attribute <%s>.%s to `%s`"
              % (kind, entity, name, val)
              )
            ,
            )
        self.entity    = entity
        self.kind      = kind
        self.attribute = name
        self.value     = val
    # end def __init__

    def correct (self) :
        pass
    # end def correct

# end class Invalid_Attribute

class Unknown_Attribute (Invalid_Attribute) :

    def correct (self) :
        """Try to correct this error."""
        self.entity.correct_unknown_attr (self)
    # end def correct

# end class Unknown_Attribute

class Invalid_Attribute_Type (Error) :
    pass
# end class Invalid_Attribute_Type

class Already_Editing (Error) :
    pass
# end class Already_Editing

class Type_Not_In_Scope (Error) :
    pass
# end class Type_Not_In_Scope

class Cannot_Rename_Root_Object (Error) :
    pass
# end class Cannot_Rename_Root_Object

class DB_Error (StandardError) :
    pass
# end class DB_Error

class Incompatible_DB_Version (DB_Error) :
    pass
# end class Incompatible_DB_Version

class Empty_DB (DB_Error) :
    pass
# end class Empty_DB

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.Error
