# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.SDG.Node
#
# Purpose
#    Model a node of a structured document
#
# Revision Dates
#    23-Jul-2004 (CT) Creation
#    ««revision-date»»···
#--

"""
from _TFL._SDG.Node import *
root = Node \
    ( Node ( Node ( name = "a.1")
           , Node ( name = "a.2")
           , name = "a"
           )
    , Node ( Node ( name = "b.x")
           , Node ( Node ( name = "b.y.1")
                  , Node ( name = "b.y.2")
                  , name = "b.y"
                  )
           , Node ( name = "b.z")
           , name = "b"
           )
    , name = "R"
    )
print "\n".join (root.as_repr(base_indent = "  "))

"""

from   _TFL              import TFL
import _TFL.Caller
import _TFL._SDG
import _TFL._SDG.M_Node

from   NO_List           import NO_List
from   predicate         import *

class Invalid_Node (StandardError) :
    pass
# end class Invalid_Node

class Node :
    """Node of a structured document"""

    __metaclass__     = TFL.SDG.M_Node

    base_indent       = "    "
    init_arg_defaults = dict (name = "")
    _list_of_formats  = ("repr_format", )
    repr_format       = """
        %(name)-20.20s
        >%(*children*)s
    """

    def __init__ (self, * children, ** kw) :
        self.parent = None
        self._init_kw (kw)
        if not self.name :
            self.name = "__%s_%d" % (self.__class__.__name__, self.id)
        self._reset_children ()
        self.add (* children)
    # end def __init__

    def add (self, * children) :
        """Append all `children' to `self.children'"""
        for c in children :
            self.insert (c)
    # end def add

    def as_repr (self, base_indent = None, gauge = None, head = "") :
        if base_indent is None :
            base_indent = self.base_indent
        recurser = "as_repr"
        recurse_args = dict \
            ( base_indent = base_indent
            , gauge       = gauge
            , head        = head
            )
        context = TFL.Caller.Scope (globs = self.__dict__)
        for f in self.repr_format :
            indent = f.indent_level * base_indent
            for l in f (self, context, head) :
                yield "%s%s" % (indent, l)
    # end def as_repr

    def destroy (self) :
        for c in self.children :
            c.destroy ()
        self._reset_children ()
        self.parent = None
    # end def destroy

    def get_child (self, child_name, transitive = True) :
        """Returns the child named `child_name' or `None' if no child with
           the specifed name exists.
        """
        child_name = self._child_name (child_name)
        if child_name in self.children :
            return self.children [child_name]
        elif transitive :
            for c in self.children :
                r = c.get_child (child_name, transitive = True)
                if r is not None :
                    return r
    # end def get_child

    def has_child (self, child_name, transitive = True) :
        """Checks if this node or one of this childs has a node named
           `child_name'.
        """
        child_name = self._child_name (child_name)
        if child_name in self.children :
            return True
        elif transitive :
            for c in self.children :
                if c.has_child (child_name, transitive = True) :
                    return True
        return False
    # end def has_child

    def insert (self, child, index = None, delta = 0) :
        """Insert `child' to `self.children' at position `index'
           (None means append).
        """
        self._insert (child, index, self.children, delta)
    # end def insert

    def _child_name (self, child_name) :
        if isinstance (child_name, Doc_Node) :
            child_name = child_name.name
        return child_name
    # end def _child_name

    def _init_kw (self, kw) :
        kw_err = {}
        for k, v in self.init_arg_defaults.iteritems () :
            if not hasattr (self, k) :
                setattr (self, k, v)
        for k, v in kw.iteritems () :
            if k in self.init_arg_defaults :
                setattr (self, k, v)
            else :
                kw_err [k] = v
        if kw_err :
            print self.__class__, self.init_arg_defaults
            raise TypeError, "unexpected keyword arguments: %s" % kw_err
    # end def _init_kw

    def _insert (self, child, index, children, delta = 0) :
        if not child :
            return
        if index is None :
            index = len (children)
        child.parent = self
        children.insert (index, child, delta)
    # end def _insert

    def _reset_children (self) :
        self.children = NO_List ()
    # end def _reset_children

    def __getitem__ (self, index) :
        return self.children [index]
    # end def __getitem__

    def __iter__ (self) :
        yield self
        for c in self.children :
            for n in iter (c) :
                yield n
    # end def __iter__

    def __repr__ (self) :
        return "\n".join (self.as_repr ())
    # end def __repr__

# end class Node

class Leaf (Node) :
    """Leaf node which doesn't have children"""

    children = NO_List ()

    def insert (self, child, index = None, delta = 0) :
        raise Invalid_Node, (self, child)
    # end def insert

    def _reset_children (self) :
        pass
    # end def _reset_children

# end class Leaf

if __name__ != "__main__" :
    TFL.SDG._Export ("*")
### __END__ TFL.SDG.Node
