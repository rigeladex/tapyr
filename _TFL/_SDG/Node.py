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
#    26-Jul-2004 (CT) Creation continued
#    27-Jul-2004 (CT) Call to `_autoconvert` corrected (`self` passed)
#    28-Jul-2004 (CT) `front_args` and `rest_args` added to `__init__`
#    30-Jul-2004 (CT) `base_indent2` added
#     2-Aug-2004 (CT) `_write_to_stream` added
#     2-Aug-2004 (CT) Methods put into alphabetical order
#     3-Aug-2004 (CT) `__repr__` changed to use `as_tree` (to make `as_tree`
#                     work for cases where a node is stored as an attribute
#                     instead of a child)
#     3-Aug-2004 (CT) `__str__` added (using `as_repr`)
#     3-Aug-2004 (CT) s/as_repr/as_str/  and s/repr_format/str_format/
#     3-Aug-2004 (CT) s/as_tree/as_repr/ and s/tree_format/repr_format/
#     3-Aug-2004 (CT) `base_indent` moved from `init_arg_defaults` to class
#                     variable (save memory for spurious instance attribute)
#    12-Aug-2004 (CT) s/recurse_args/recurse_kw/g
#    12-Aug-2004 (MG) `default_cgi` added
#    12-Aug-2004 (MG) `add`: unnest pass childrens (backward compatibility)
#    12-Aug-2004 (CT) `indent_anchor` added
#    13-Aug-2004 (MG) `formatted` Parameter `ht_width` added
#    13-Aug-2004 (CT) `* args, ** kw` added to `_formatted_attrs`
#    13-Aug-2004 (CT) Replaced `TFL.Caller.Scope` by `TFL.Caller.Object_Scope`
#    13-Aug-2004 (CT) `node_type` removed
#    13-Aug-2004 (CT) `base_indent2` removed
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL.Caller
import _TFL._SDG
import _TFL._SDG.M_Node

from   NO_List           import NO_List
from   predicate         import *
import sys

class Invalid_Node (StandardError) :
    pass
# end class Invalid_Node

class Node :
    """Node of a structured document.

       A node has attributes and children. Attributes specify information
       about the node itself, e.g., name, type, children group index.
       Children define lower-level nodes.

       Attributes
       ==========

       Normally, attributes must be passed as keyword arguments to
       `__init__`.

       - `init_arg_defaults` defines which attribute names are allowed
         for a specific node type and specify default values for these
         attributes.

       - `_autoconvert` is a dictionary mapping attribute names to
         conversion functions called automatically during object
         initialization for all attribute values specified by the
         caller.

       - `front_args` defines the names of attributes that can be
         passed as normal arguments at the beginning of the argument
         list.

       - `rest_args` defines the name of a single attributes that
         takes all non-named arguments which aren't `front_args`.

       Children
       ========

       For non-leaf nodes, children can be passed to `__init__` behind
       the `front_args` and keyword arguments if any (if `rest_args`
       is defined, children cannot be passed to `__init__`).

       Children can be split into different groups.

       - Each node type defines a children group index `cgi` to be
         used as default.

         `default_cgi` of the parent will be used to add a node with a
         `cgi` of None.

       - `children_group_names` defines the names of the children
         groups supported by a node type.

         For Node, only the group `Body` is defined.

       - For each children group xxx, a property xxx_children allows
         access to the group's children.

       - `children` iterates over all children of all groups in some
         unspecified sequence.

       Formats
       =======

       Formats define how to format a node and its children for a
       specific purpose.

       - `_list_of_formats` specifies the names of the applicable
         formats.

       - Each format is a string defined as a class variable.

       - The meta class M_Node transforms the format strings into
         lists of formatter objects.

       - Each line of the format string is handled by a separate
         formatter object that controls the indentation and other
         aspects of the formatting process.

       - A line of a format string can contain

         * A leading indentation marker comprising zero or more `>`
           characters. Each `<` corresponds to the number of spaces
           specified by `base_indent`.

           If base_indent is "  " (two spaces), a leading indentation
           marker of `>>>` will result in an leading indentation of
           six spaces for the line in question (relative to the other
           lines of the format).

         * Plain text.

           This is put into the formatted representation of the node
           as is.

         * A format string as required by Python's dictionary
           interpolation. This has the form
           `%(<someexpression>)<format-spec>`.

           `<someexpression>` is evaluated in the context of the node
           object and its `formatted` operation. The result is put in
           to the formatted representation of the node.

           `<format-spec>` is documented in the Python Library
           Reference manual, in the section `String Formatting
           Operations`.

           A simple example is `%(base_indent * 2)s` which will add
           two times `node.base_indent` to the formatted representation.

         * A complex SDG format specification. This has the form
           `%(:<control>:<key-spec>:)<format-spec>` and is described
           in more detail below.

         * A format line containing a complex SDG format specification
           can expand to more than a single line of output in the
           formatted representation of a node.

         * All other lines of a format specification must expand to a
           single line of output (otherwise indentation is messed up).

       Complex SDG format specifications
       =================================

       tdb

       Example
       =======

       `str_format` is used to convert a node to a string when
       `__str__` is called.

           str_format           = '''
               %(__class__.__name__)s %(name)s
               >%(::*children:)s
           '''

       The first line of `str_format` contains two simple format
       specifications which expand to the class-name and name of a
       node. The second line starts with an indentation level marker
       specifying a relative indentation of one `base_indent` followed
       by a complex SDG format specification. `%(::*children:)s`
       expands to a formatted representation of the children of the
       node using the same format specification applied to the node
       itself (in this case, `str_format`):

       >>> class T_Node (Node) :
       ...     init_arg_defaults = dict (hansi = "kieselack")
       ...
       >>> root = T_Node (
       ...       T_Node ( Leaf ( name = "a.1")
       ...              , Leaf ( name = "a.2")
       ...              , name  = "a"
       ...              , hansi = "A"
       ...              )
       ...     , T_Node ( Node ( name = "b.x")
       ...              , Leaf ( name = "b.z")
       ...              , name = "b"
       ...              )
       ...     , name = "R"
       ...     )
       >>> print root
       T_Node R
           T_Node a
               Leaf a.1
               Leaf a.2
           T_Node b
               Node b.x
               Leaf b.z

    """

    __metaclass__        = TFL.SDG.M_Node

    children             = property (lambda s : s._children_iter ())
    children_group_names = (Body, ) = range (1)
    default_cgi          = Body
    body_children        = property (lambda s : s.children_groups [s.Body])

    base_indent          = "    "
    init_arg_defaults    = dict (name = "", cgi = 0)
    _autoconvert         = {}
    front_args           = ()
    rest_args            = None

    _list_of_formats     = ("repr_format", "str_format")
    repr_format          = """
        %(__class__.__name__)s \\
        >%(:front=( ¡sep=, :>*children,>@_formatted_attrs:)s
        >)
    """
    str_format           = """
        %(__class__.__name__)s %(name)s
        >%(::*children:)s
    """

    def __init__ (self, * children, ** kw) :
        self.parent = None
        n = len (children)
        for a in self.front_args :
            if children :
                if a in kw :
                    raise TypeError, \
                        ( "%s() got multiple values for keyword argument %s"
                        % (self.__class__.__name__, a)
                        )
                kw [a]   = children [0]
                children = children [1:]
            elif a not in kw :
                raise TypeError, \
                    ( "%s() takes exactly %s arguments (%s given)"
                    % (self.__class__.__name__, len (self.front_args), n)
                    )
        if self.rest_args and children :
            kw [self.rest_args] = children
            children            = ()
        self._init_kw (kw)
        if not self.name :
            self.name = "__%s_%d" % (self.__class__.__name__, self.id)
        self._reset_children ()
        self.add (* children)
    # end def __init__

    def add (self, * children) :
        """Append all `children' to `self.children'"""
        for c in un_nested (children) :
            self.insert (c)
    # end def add

    def as_repr (self, base_indent = None) :
        return self.formatted ("repr_format", base_indent)
    # end def as_repr

    def as_str (self, base_indent = None) :
        return self.formatted ("str_format", base_indent)
    # end def as_str

    def destroy (self) :
        for c in self.children :
            c.destroy ()
        self._reset_children ()
        self.parent = None
    # end def destroy

    def formatted (self, format_name, base_indent = None, output_width = 79, indent_offset = 0, ht_width = 0, ** kw) :
        if base_indent is None :
            base_indent = self.base_indent
        recurser   = "formatted"
        format     = getattr (self, format_name)
        recurse_kw = dict \
            ( format_name = format_name
            , base_indent = base_indent
            , ** kw
            )
        context = TFL.Caller.Object_Scope (self)
        for f in format :
            indent = f.indent_level * base_indent
            indent_offset += len (indent)
            context.locals ["indent_offset"] = \
                context.locals ["indent_anchor"] = indent_offset
            for l in f (self, context) :
                yield "%s%s" % (indent, l)
            indent_offset -= len (indent)
    # end def formatted

    def has_child (self, child_name, transitive = True) :
        """Checks if this node or one of this childs has a node named
           `child_name'.
        """
        child_name = self._child_name (child_name)
        for children in self.children_groups.itervalues () :
            if child_name in children :
                return True
        if transitive :
            for c in self.children :
                if c.has_child (child_name, transitive = True) :
                    return True
        return False
    # end def has_child

    def insert (self, child, index = None, delta = 0) :
        """Insert `child' to `self.children' at position `index'
           (None means append).
        """
        cgi = child.cgi
        if cgi is None :
            cgi = self.default_cgi
        else :
            self.default_cgi = min (cgi, self.default_cgi)
        self._insert (child, index, self.children_groups [cgi], delta)
    # end def insert

    def _child_name (self, child_name) :
        if isinstance (child_name, Node) :
            child_name = child_name.name
        return child_name
    # end def _child_name

    def _children_iter (self) :
        for group in self.children_groups.itervalues () :
            for c in group :
                yield c
    # end def _children_iter

    def _formatted_attrs (self, format_name, * args, ** kw) :
        for k, v in sorted (self.init_arg_defaults.iteritems ()) :
            a = getattr (self, k)
            if a != v :
                yield "%s = %r" % (k, a)
    # end def _formatted_attrs

    def _init_kw (self, kw) :
        kw_err = {}
        for k, v in self.init_arg_defaults.iteritems () :
            if not hasattr (self, k) :
                setattr (self, k, v)
        for k, v in kw.iteritems () :
            if k in self.init_arg_defaults :
                if k in self._autoconvert :
                    v = self._autoconvert [k] (self, k, v)
                setattr (self, k, v)
            else :
                kw_err [k] = v
        if kw_err :
            print self.__class__, self.init_arg_defaults
            raise TypeError, "unexpected keyword arguments: %s" % kw_err
    # end def _init_kw

    def _insert (self, child, index, children, delta = 0) :
        if child :
            if index is None :
                index = len (children)
            child.parent = self
            children.insert (index, child, delta)
    # end def _insert

    def _reset_children (self) :
        self.children_groups = dict \
            ([(i, NO_List ()) for i in self.children_group_names])
    # end def _reset_children

    def _write_to_stream (self, gen, stream, gauge = None) :
        if stream is None :
            stream = sys.stdout
        for x in gen :
            stream.write  (x)
            stream.write  ("\n")
            if gauge is not None :
                gauge.inc ()
    # end def _write_to_stream

    def __iter__ (self) :
        yield self
        for c in self.children :
            for n in iter (c) :
                yield n
    # end def __iter__

    def __repr__ (self) :
        return "\n".join (self.as_repr ())
    # end def __repr__

    def __str__ (self) :
        return "\n".join (self.as_str ())
    # end def __str__

# end class Node

class Leaf (Node) :
    """Leaf node which doesn't allow children"""

    children_group_names = () ### doesn't allow any children

    def insert (self, child, index = None, delta = 0) :
        raise Invalid_Node, (self, child)
    # end def insert

# end class Leaf

### debugging code to be pasted into an interactive interpreter
"""
from _TFL._SDG.Node import *
class T_Node (Node) :
    init_arg_defaults = dict (hansi = "kieselack")

root = T_Node \
    ( T_Node ( Leaf ( name = "a.1")
             , Leaf ( name = "a.2")
             , name  = "a"
             , hansi = "A"
             )
    , T_Node ( Node ( name = "b.x")
             , T_Node ( Node ( name = "b.y.1")
                      , Node ( name = "b.y.2")
                      , name  = "b.y"
                      , hansi = "B.Y"
                      )
             , Leaf ( name = "b.z")
             , name = "b"
             )
    , name = "R"
    )
print root
print repr (root)

"""

if __name__ != "__main__" :
    TFL.SDG._Export ("*")
### __END__ TFL.SDG.Node
