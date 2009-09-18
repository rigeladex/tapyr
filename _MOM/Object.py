# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2009 Mag. Christian Tanzer. All rights reserved
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
#    TOM.Object
#
# Purpose
#    Root class for object-types of Tanzer's Object Model
#
# Revision Dates
#     2-Aug-1999 (CT) Creation
#     4-Aug-1999 (CT) `O_Root' used instead of `"TOM_Object"' by
#                     `define_stmt', `journal_stmt', and `__repr__'
#     4-Aug-1999 (CT) `name_pattern' added and checked
#     5-Aug-1999 (CT) Allow obsolete classes in `instance'
#     2-Dec-1999 (CT) `__cmp__' allows strings for `other'
#     9-Feb-2000 (CT) `rank' and `rank_cmp' added
#     6-Mar-2000 (CT) Redefinition of `globals' removed
#     9-Mar-2000 (CT) `TOM_System_Object' and `customize' added
#    28-Mar-2000 (CT) `rank_cmp' changed to compare `id' for objects of
#                     equal rank
#    13-Apr-2000 (CT) `Ancestor' replaced by `__Ancestor'
#                     (can use `self.__Ancestor' instead of `<class>.Ancestor')
#    23-Jun-2000 (CT) `entity_type' and `entity_kind' statically defined in
#                     `TOM_Object' instead of set dynamically by `index_class'
#    23-Jun-2000 (CT) `repr' uses literal "instance" instead of
#                     `_name_of_define_stmt'
#    13-Jul-2000 (CT) `TOM_System_Object': added
#                         `attributes__ = Ancestor.attributes___'
#                     to avoid writing of internal attributes
#    19-Jul-2000 (CT) Hash-table `extension' renamed to `_extension'
#    19-Jul-2000 (CT) Argument `of_class' of function `extension' made
#                     optional
#    19-Jul-2000 (CT) Class functions `exists' and `extension' added
#    19-Jul-2000 (CT) `_destroy_links' factored
#    19-Jul-2000 (CT) `destroy' redefined in `TOM_System_Object'
#     3-Aug-2000 (CT) `active_scope' and `home_scope' added
#     4-Aug-2000 (CT) `active_scope' and `home_scope' moved to `TOM_Entity'
#    28-Aug-2000 (CT) `_name_of_customize_stmt' added
#    28-Aug-2000 (CT) Argument `implicit = None' removed from `customize'
#    31-Oct-2000 (CT) `TOM_Entity_Type' used
#     2-Nov-2000 (CT) `_destroy' factored
#     2-Nov-2000 (CT) `link' changed from list to dictionary
#     2-Nov-2000 (CT) `_name_of_customize_stmt' removed
#     2-Nov-2000 (CT) `TOM_System_Object.destroy' removed
#     2-Nov-2000 (CT) Parts of `rename' factored to `TOM_Scope'
#    14-Nov-2000 (CT) `_names' added
#     1-Feb-2001 (CT) `is_partial' checked in `TOM_Entity.__init__' instead
#                     of in `TOM_Object.__init__'
#     5-Feb-2001 (CT) `TOM_Entity.active_scope' replaced by
#                     `TOM_Scope.active'
#     5-Feb-2001 (CT) Get `O_Root' from `self.etype' instead of from `self'
#     5-Feb-2001 (CT) `Class_Proxy' added
#     9-Feb-2001 (CT) `__getstate__' and `__setstate__' replaced by
#                     `TOM_Object_Pickle'
#     9-Feb-2001 (CT) `TOM_System_Object' removed
#     9-Feb-2001 (CT) `instance' and `customize' also provided as class
#                     functions
#    19-Feb-2001 (CT) Last remnants of `_extension' removed (is managed by
#                     TOM_Scope)
#    19-Feb-2001 (CT) Increment `etype.count' in `TOM_Object.__init__'
#    22-Feb-2001 (CT) `TOM_Class_Proxy' renamed to `TOM_Object_Class_Proxy'
#    27-Mar-2001 (CT) `Class_Proxy' renamed to `Class_Proxy_Type' and
#                     `Class_Proxy' set to actual class-proxy instance
#    30-Mar-2001 (CT) Import `*' from `TOM_Object_Class_Proxy' (instead of
#                     just `TOM_Object_Class_Proxy')
#    26-Jun-2001 (CT) Functor for `TOM_Object.define' added
#    20-Jul-2001 (CT) `Entity_Type_S` added
#    20-Jul-2001 (CT) s/TOM_Entity_Type/TOM_Object_Type/g
#    27-Jul-2001 (CT) Migrated into package `TOM`
#    31-Jul-2001 (CT) Calls to `string` module replaced by string methods
#    17-Aug-2001 (CT) Adapted to `etype` revamping
#     3-Sep-2001 (CT) Class attribute `entity_type` removed, `entity_kind`
#                     and `O_Root` moved from `_e_type_template` into class
#     4-Sep-2001 (CT) `_destroy_links` removed from `remove`
#     4-Oct-2001 (MG) `Object.__init__`: moved call of `__Ancestor.__init__`
#    12-Oct-2001 (CT) Argument `scope` added to `instance`
#    12-Oct-2001 (CT) `instance` uses `scope.entity_type` to get the correct
#                     class to instantiate new object (also needed to
#                     s/isinstance_cp/TOM.isinstance/)
#    23-Oct-2001 (MG) `instance`: Second check for obsolete classes added
#    23-Nov-2001 (CT) Use `Function` instead of `Functor`
#    23-Nov-2001 (CT) `define_stmt` factored into `Entity`
#    23-Nov-2001 (CT) `_define_stmt_name_arg` added
#    23-Apr-2002 (CT) Optional argument `sep` added to `_define_stmt`
#    17-Jun-2002 (CT) `_use_defaults` added
#    15-Oct-2002 (CT) `rage_cmp` added
#    19-Dec-2002 (CT) `Cannot_Rename_Root_Object` raised
#    15-Jan-2003 (CT) Major revamping started
#                     - use new Attr_Type/Attr_Kind
#                     - use meta class
#    17-Jan-2003 (CT) `M_` prefixes added
#    22-Jan-2003 (CT) `_ATS_Types` with `_template*` added
#    29-Jan-2003 (CT) Definition of `Object.Proxy_Type` moved to `Proxy`
#    19-Feb-2003 (CT) s/register_link/register_dependency/g
#    19-Feb-2003 (CT) s/link/dependencies/g
#    27-Mar-2003 (MG) Setting of `Meta_E_Type` moved from `M_E_Type` into
#                     `ATS_Type._template` to support different `M_E_Type`
#                     for different ATS_Types (reuse)
#    27-Mar-2003 (MG) Setting of `_M_SS_E_Type` moved from `M_E_Type`
#     3-Apr-2003 (CT) s/compute_defaults/compute_defaults_internal/
#     4-Apr-2003 (CT) Changed semantics of `_auto_mixin` to dictionary
#    15-Apr-2003 (CT) `_define_stmt`, `journal_stmt`, and `__repr__` changed
#                     to just use `type_name` instead of `O_Root`
#    15-Apr-2003 (CT) `_define_stmt` moved to `Entity`
#    16-Apr-2003 (CT) Call of `_destroy` moved from `destroy` to `Scope`
#    17-Apr-2003 (CT) `old_name` added to `update_dependency_names`
#     8-May-2003 (CT) Parts of `__new__` factored into `Entity`
#    12-May-2003 (MG) Setting of `self.name` moved from `Object.__init__` to
#                     `Object.__new__`
#     9-Oct-2003 (CT) `** kw` added to `__init__`
#    10-Jan-2004 (CED) `_template_R` removed
#    17-Dec-2004 (CED) `_name_of_remove_stmt`, `_remove_stmt_name_arg` added
#    12-Jun-2006 (CT)  Use `.Essence.type_name` instead of `.type_name`
#    12-Jun-2006 (CT)  `_repr` added (and `__repr__` inherited from `Entity`)
#     2-Aug-2006 (CT)  Stale `O_Root` removed
#    29-Sep-2006 (CED) `Singleton_Object` added
#    16-Nov-2006 (PGO) Users of Export_Module'd modules fixed
#     2-Apr-2007 (PGO) Calculation of `id` moved to ancestor
#    23-Jul-2007 (CED) Activated absolute_import
#    12-Sep-2007 (CED) Fixed `rename`
#    29-Aug-2008 (CT)  s/super(...)/__super/
#    11-Feb-2009 (CT)  Documentation added
#    17-Apr-2009 (CT)  `_remove_stmt_name_arg` fixed (CED, oh, CED)
#    ««revision-date»»···
#--

from __future__ import absolute_import

from   _TFL      import TFL
from   _TOM      import TOM

import _TOM.Entity
import _TOM._Meta.M_Object
import _TOM._Meta.M_E_Type
import _TOM.Pickle

from   _TOM._Attr.Type import *
from   _TOM._Attr      import Attr

class Singleton_Object (TOM.Meta.Object) :

    def _destroy (self) :
        self.__class__.singleton = None
        self.__super._destroy ()
    # end def _destroy

# end class Singleton_Object

_Ancestor_Essence = TOM.Entity

class Object (_Ancestor_Essence) :
    """Root class for object-types of Tanzer's Object Model."""

    __metaclass__ = TOM.Meta.M_Object

    ### redefine in descendents if object name must match a certain pattern
    name_pattern          = None

    entity_kind           = "object"

    Pickle                = TOM.Object_Pickle
    _name_of_define_stmt  = "define"
    _name_of_remove_stmt  = "destroy"

    def __new__ (cls, name, ** kw) :
        result       = super (Object, cls).__new__ (cls)
        result.name  = name
        return result
    # end def __new__

    def __init__ (self, name, ** kw) :
        if not name :
            raise TOM.Error.Invalid_Name ("<empty>")
        if self.name_pattern and not self.name_pattern.match (name) :
            raise TOM.Error.Invalid_Name (name)
        self.implicit = None
        self.home_scope.add (self)
        ### Call the __init__ of the Ancestor as late as possible.
        self.__super.__init__ ()
        if kw :
            self.set (** kw)
    # end def __init__

    def destroy (self) :
        """Remove object from `extension'."""
        if self is self.home_scope.root :
            self.home_scope.destroy ()
        else :
            assert (not self.home_scope._locked)
            self.home_scope.remove (self.name)
    # end def destroy

    def rename (self, new_name) :
        """Rename object to `new_name'."""
        if self.home_scope._roots.get (self.Essence.type_base_name) is self :
            raise TOM.Error.Cannot_Rename_Root_Object (self, new_name)
        if self.name_pattern and not self.name_pattern.match (new_name) :
            raise TOM.Error.Invalid_Name (new_name)
        old_name  = self.name
        self.home_scope.rename (self, new_name)
        self.name = new_name
        for d in self.dependencies.keys () :
            try :
                d.update_dependency_names (self, old_name)
            except :
                print self.__class__, old_name, new_name, d
                raise
    # end def rename

    def _names (self) :
        return (self.name, )
    # end def _names

    def _define_stmt_name_arg (self) :
        return '"%s"' % self.name
    # end def _define_stmt_name_arg

    def _remove_stmt_name_arg (self) :
        return "%s.instance (%r)" % (self.type_name, self.name)
    # end def _remove_stmt_name_arg

    def journal_stmt (self, result_dict) :
        args = self._journal_items \
             (result_dict, [self._define_stmt_name_arg ()])
        if len (args) > 1 :
            return """%s.%s (%s, raw=1)\n""" % \
                (self.type_name, self._name_of_define_stmt, ", ".join (args))
        else :
            return ""
    # end def journal_stmt

    def _repr (self, type_name) :
        return """%s.instance ("%s")""" % (type_name, self.name)
    # end def _repr

    def __str__ (self) :
        return self.type_name + " `" + self.name + "'"
    # end def __str__

    def __hash__ (self) :
        return self.id
    # end def __hash__

    def __cmp__  (self, other) :
        if isinstance (other, Object) :
            return cmp (self.name, other.name)
        return cmp (self.name, other)
    # end def __cmp__

    def rank_cmp (self, other) :
        if isinstance (other, Object) :
            return cmp ((self.rank,  self.id), (other.rank, other.id))
        return cmp (self.rank, other)
    # end def rank_cmp

    def rage_cmp (self, other) :
        """Compare `self` and `other` regarding relative age"""
        try :
            return cmp (self.id, other.id)
        except AttributeError :
            return cmp (self.id, other)
    # end def rage_cmp

    def _use_defaults (self, other) :
        if self.rank_cmp (other) > 0 :
            other.compute_defaults_internal ()
    # end def _use_defaults

# end class Object

_Essence = Object

class _ATS_Types (_Ancestor_Essence._ATS_Types) :

    _Ancestor = _Ancestor_Essence._ATS_Types

    class _template (_Ancestor._template) :

        rank         = 0
        """`rank` is used for sorting the objects before iteration."""

        Meta_E_Type            = TOM.Meta._.M_E_Type.M_E_Type_Object
        Meta_E_Type_Singleton  = TOM.Meta._.M_E_Type.M_E_Type_Singleton
        _M_SS_E_Type           = TOM.Meta._.M_E_Type._M_SS_E_Type_Object_
        _M_SS_E_Type_Singleton = TOM.Meta._.M_E_Type._M_SS_E_Type_Singleton_
        _Singleton_Mixin       = Singleton_Object
    # end class _template

    class _template_I (_template, _Ancestor._template_I) :
        pass
    # end class _template_I

    _auto_mixin = TFL.d_dict \
      ( d       = _template
      , i       = _template_I
      )

# end class _ATS_Types

__doc__ = """
Class `TOM.Object`
==================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Object

   `TOM.Object` provides the framework for defining essential classes. It is
   based on :class:`~_TOM.Entity.Entity`. In addition to the
   properties defined by `Entity`, each instance of `Object` is characterized
   by a unique name that must be specified when the instance is created.

Object Queries
--------------

For each essential class `E`, a number of queries is defined:

- `E.count` gives the number of strict instances of `E` (i.e., excluding
  instances of descendent classes). For partial classes, `count` always
  returns zero.

- `E.exists(name)` returns True if an instance of `E` (or one of its
  descendent classes) with the specific `name` exists.

- `E.extension()` returns all instances of `E` and its descendent classes.

- `E.extension_strict()` returns all instances of `E` but none of its
  descendent classes.

- `E.instance(name)` returns the instance of `E` (or one of its descendent
  classes) with the specific `name`.

    .. note::
      For historical reasons, `instance` tries to create an instance with
      `name` if none exists.

- `E.root` gives the root object of `E` in the current scope, if any.

All these queries can be applied to all classes derived from `Object` and to
`Object` itself.

"""

if __name__ != "__main__" :
    TOM._Export ("Object")
### __END__ TOM.Object
