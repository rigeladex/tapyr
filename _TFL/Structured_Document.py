# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Structured_Document
#
# Purpose
#    Classes for generation of structured documents
#
# Revision Dates
#    15-Nov-1999 (CT) Creation
#    16-Nov-1999 (CT) Creation continued
#     9-Dec-1999 (CT) `_init_children' renamed to `_reset_children'
#     9-Dec-1999 (CT) `add' renamed to `insert'
#     9-Dec-1999 (CT) `add' added
#    15-Dec-1999 (CT) `Init_Arg_Dict' factored into `D_Dict'
#    10-Mar-2000 (CT) Use `NO_List' for `children'
#    15-Mar-2000 (CT) `Doc_Node_Formatter_Guarded_' added
#    20-Mar-2000 (MG) `Structured_Document.add' : Unnesting if children added
#    21-Mar-2000 (MG) `add' and `_insert' changed to allow passing None as
#                     child
#    21-Mar-2000 (MG) `has_child' added
#    23-Mar-2000 (MG) `get_child', `replace_child', and `replace_child' added
#    12-May-2000 (CT) `__getitem__' added
#    27-Oct-2000 (MG) `un_nested' of children added to `__init__' of
#                     `Doc_Node'
#    26-Sep-2001 (MG) Moved into package `TFL`
#    29-Jan-2002 (MG) `get_childrens` added
#    28-Feb-2002 (CT) Use `TFL.d_dict` instead of `D_Dict`
#    12-Apr-2002 (CT) Use `StandardError` instead of `Exception`
#    11-Jun-2003 (CT) s/== None/is None/
#    14-Apr-2005 (CT) Use `isinstance` instead of `type` comparison
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   Formatted_Stream import *
from   _TFL             import TFL
from   NO_List          import NO_List
from   types            import MethodType, FunctionType

import _TFL.predicate
import re
import string

import _TFL.d_dict

class Invalid_Node (StandardError) : pass

class Doc_Node_Formatter_ :
    """Doc_Node_Formatter_ encapsulates a triple of functions necessary to
       format an instance of `Doc_Node'.
    """

    def __init__ (self, head = None, body = None, tail = None, body_sep = None) :
        self._head     = self._function_name (head)
        self._body     = self._function_name (body)
        self._tail     = self._function_name (tail)
        self._body_sep = body_sep
    # end def __init__

    def _function_name (self, fct) :
        if not fct :
            return None
        if isinstance (fct, (MethodType, FunctionType)) :
            fct = fct.__name__
        return fct
    # end def _function_name

    def __call__ (self, * args, ** kw) :
        """`args [0]' must be the instance of `Doc_Node' to be formatted."""
        return ( apply (self.head, args, kw)
               + apply (self.body, args, kw)
               + apply (self.tail, args, kw)
               )
    # end def __call__

    def head (self, this, * args, ** kw) :
        if self._head :
            return apply (getattr (this, self._head), args, kw) or ""
        return ""
    # end def head

    def body (self, this, * args, ** kw) :
        if self._body :
            list = map ( lambda c, b = self._body, args = args, kw = kw
                       : apply (getattr (c, b), args, kw)
                       , this.children
                       )
            return string.join ( filter (None, list)
                               , self._body_sep or this.children_separator
                               )
        return ""
    # end def body

    def tail (self, this, * args, ** kw) :
        if self._tail :
            return apply (getattr (this, self._tail), args, kw) or ""
        return ""
    # end def tail

# end class Doc_Node_Formatter_

class Doc_Node_Formatter_Guarded_ :
    """Guarded Doc_Node_Formatter_: format only if `guard' function approves."""

    def __init__ (self, guard, formatter) :
        self._guard     = guard
        self._formatter = formatter
    # end def __init__

    def __call__ (self, * args, ** kw) :
        if self._guard () :
            ### print "\n***** TRUE  guard", self._guard, str (args [0])
            return apply (self._formatter.__call__, args, kw)
        else :
            ### print "\n***** FALSE guard", self._guard, str (args [0])
            pass
    # end def __call__

    def __getattr__ (self, name) :
        return getattr (self._formatter, name)
    # end def __getattr__

# end class Doc_Node_Formatter_Guarded_

Init_Arg_Dict = TFL.d_dict

class Doc_Node :
    """Node of a structured document"""

    _init_arg_dict = Init_Arg_Dict (name = "")

    __id           = 0

    def _new_id (self) :
        Doc_Node.__id = Doc_Node.__id + 1
        return Doc_Node.__id
    # end def _new_id

    def __init__ (self, * children, ** kw) :
        self.id     = self._new_id ()
        self.parent = None
        self._init_kw        (kw)
        if not self.name :
            self.name = "__%s_%d" % (self.__class__.__name__, self.id)
        self._reset_children ()
        map                  (self.insert, TFL.un_nested (children))
    # end def __init__

    def _init_kw (self, kw) :
        kw = kw.copy ()
        map ( lambda (k, v), s = self :
                  hasattr (s, k) or s._set_attr_value (k, v)
            , self._init_arg_dict.items ()
            )
        for k, v in kw.items () :
            if self._init_arg_dict.has_key (k) :
                self._set_attr_value (k, v)
                del kw [k]
        if kw :
            print self.__class__, self._init_arg_dict
            raise TypeError, "unexpected keyword arguments: %s" % kw
    # end def _init_kw

    def _set_attr_value (self, name, value) :
        setattr (self, name, value)
    # end def _set_attr_value

    def _reset_children (self) :
        self.children = NO_List ()
    # end def _reset_children

    def insert (self, child, index = None, delta = 0) :
        """Insert `child' to `self.children' at position `index'
           (None means append).
        """
        self._insert (child, index, self.children, delta)
    # end def insert

    def add (self, * children) :
        """Append all `children' to `self.children'"""
        children = TFL.un_nested (children)
        if children :
            map (self.insert, children)
    # end def add

    def _insert (self, child, index, children, delta = 0) :
        if not child :
            return
        if index is None :
            index = len (children)
        child.parent = self
        children.insert (index, child, delta)
    # end def _insert

    def _dont_insert (self, child, index = None, delta = 0) :
        raise Invalid_Node, (self, child)
    # end def _dont_insert

    def _child_name (self, child_name) :
        if isinstance (child_name, Doc_Node) :
            child_name = child_name.name
        return child_name
    # end def _child_name

    def _transitive_child_search (self, children, fct, * args) :
        """Calls the memberfunction `fct' for all childrens in `children'
           with the parameter `name' and returns a list of all result which
           are `TRUE'.
        """
        childs = map ( lambda c, p = args, fct = fct : getattr (c, fct) (* p)
                     , children
                     )
        return filter (None, childs)
    # end def _transitive_child_search

    def has_child (self, child_name, transitive = 1) :
        """Checks if this node or one of this childs has a node named
           `child_name'.
        """
        child_name = self._child_name (child_name)
        if self.children.has_key (child_name) :
            return 1
        elif transitive :
            return len (self._transitive_child_search ( self.children
                                                      , "has_child"
                                                      , child_name
                                                      )
                       )
    # end def has_child

    def get_child (self, child_name, transitive = 1) :
        """Returns the child named `child_name' or `None' if no child with
           the specifed name exists.
        """
        child_name = self._child_name (child_name)
        if self.children.has_key (child_name) :
            child  = self.children [child_name]
        else :
            child  = None
        if not child and transitive :
            childs = self._transitive_child_search ( self.children
                                                   , "get_child"
                                                   , child_name
                                                   )
            if len (childs) : child = childs  [0]
            else            : child = None
        return child
    # end def get_child

    def get_childrens (self, child_name, type = None, match = 0, transitive = 1) :
        """XXX"""
        child_name  = self._child_name (child_name)
        if type :
            if match :
                fct =  ( lambda c, n = child_name, type = type
                       : (c.name == n) and (c.__class__ == type)
                       )
            else :
                fct =  ( lambda c, n = child_name, type = type
                       : (c.name == n) and isinstance (c, type)
                       )
        else :
            fct     = ( lambda c, n = child_name : c.name == n)
        children    = filter (fct, self.children)
        if transitive :
            children.extend \
                ( self._transitive_child_search
                      ( self.children, "get_childrens", child_name
                      , type, match, transitive
                      )
                )
        return TFL.un_nested (children)
    # end def get_childrens

    def __getitem__ (self, index) :
        return self.children [index]
    # end def __getitem__

    def replace_child (self, index, new_child) :
        """Replaces the child at postion `index' in `self.children' by
           `new_child' and returns the removed child.
        """
        child = self.get_child (index, transitive = 0)
        if child :
            self.children [child.name] = new_child
            return child
        else :
            return None
    # end def replace_child

    def remove_child (self, child_name) :
        """Checks if this node or one of this childs has a node named
           `child_name' and removes it.
        """
        child_name = self._child_name (child_name)

        if self.children.has_key (child_name) :
            child = self.children [child_name]
            child.destroy ()
            del self.children [child]
            return 1
    # end def remove_child

    def destroy (self) :
        for c in self.children :
            c.destroy        ()
        self._reset_children ()
        self.parent = None
    # end def destroy

    def write_to_stream (self, ostream) :
        """Write `self' and all elements in `self.children' to `ostream'.
        """
        assert (isinstance (ostream, Formatted_Stream))
        return self._stream_formatter (self, ostream)
    # end def write_to_stream

    def _write_to_stream_head (self, ostream) :
        """Redefine in descendents"""
        ### print "kieselack >", self.__class__
        ostream.indent   ()
    # end def _write_to_stream_head

    def _write_to_stream_tail (self, ostream) :
        """Redefine in descendents"""
        ostream.deindent ()
        ### print "kieselack <", self.__class__
    # end def _write_to_stream_tail

    children_separator = "\n"

    _stream_formatter  = Doc_Node_Formatter_ ( head     = _write_to_stream_head
                                             , body     = write_to_stream
                                             , tail     = _write_to_stream_tail
                                             )

    def __repr__ (self) :
        return self._repr_formatter (self)
    # end def __repr__

    def _arg_repr (self) :
        result = []
        map ( lambda (k, d), s = self, r = result
              : (getattr (s, k) == d)
              or r.append ("%s = %s" % (k, repr (getattr (s, k))))
            , self._init_arg_dict.items ()
            )
        return result
    # end def _arg_repr

    def _repr_head (self) :
        args = self._arg_repr ()
        args.append ("children = (")
        return ("%s (%s" % (self.__class__.__name__, string.join (args, ", ")))
    # end def _repr_head

    def _repr_tail (self) :
        return ("))")
    # end def _repr_head

    _repr_formatter   = Doc_Node_Formatter_ ( head     = _repr_head
                                            , body     = __repr__
                                            , tail     = _repr_tail
                                            , body_sep = ", "
                                            )

# end class Doc_Node

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Structured_Document
