# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Meta.M_E_Type
#
# Purpose
#    Meta classes for app-type specific entity types of the MOM meta object
#    model
#
# Revision Dates
#    23-Sep-2009 (CT) Creation started (factored from TOM.Meta.M_E_Type)
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL
from   _TFL.object_globals import object_globals

import _TFL._Meta.M_Class
import _MOM._Meta
import _MOM.Scope

class M_E_Type (TFL.Meta.M_Class) :
    """Meta class for app_type specific entity types of the MOM meta object
       model.
    """

    app_type = None

    def __new__ (meta, name, bases, dict) :
        dict ["associated_by"] = {}
        result = super (M_E_Type, meta).__new__ (meta, name, bases, dict)
        return result
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        if cls.app_type is None :
            cls._m_init_name_attributes ()
            cls._m_setup_children       (bases)
            cls._m_setup_attributes     ()
        else :
            cls._m_setup_attributes_dbw ()
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        scope = kw.get ("scope", MOM.Scope.active)
        if scope :
            return cls._m_call (scope, * args, ** kw)
    # end def __call__

    def add_attribute (cls, attr, verbose = True, parent = None, transitive = True, override = False) :
        """Add `attr` to `cls`"""
        result = cls._m_add_prop \
            (attr, cls._Attributes, verbose, parent, override)
        if result is not None :
            if result.check :
                cls._Predicates._setup_attr_checker (cls, result)
            if transitive :
                for c in cls.children_iter () :
                    c.add_attribute \
                        ( attr
                        , verbose   = False
                        , parent    = parent or cls
                        , override = override
                        )
        return result
    # end def add_attribute

    def add_predicate (cls, pred, verbose = True, parent = None, transitive = True, override = False) :
        """Add `pred` to `cls`"""
        result = cls._m_add_prop \
            (pred, cls._Predicates, verbose, parent, override)
        if transitive and result is not None :
            for c in cls.children_iter () :
                c.add_predicate \
                    ( pred
                    , verbose   = False
                    , parent    = parent or cls
                    , override = override
                    )
        return result
    # end def add_predicate

    def after_creation (cls, instance) :
        """Called after the creation of `instance`. Descendent meta classes
           can override `after_creation` to modify certain instances
           automatically when they are created.
        """
        pass
    # end def after_creation

    def children_iter (cls) :
        """Generates the etypes of all children of `cls`."""
        if cls.app_type :
            etype = cls.app_type.etype
        else :
            etype = lambda c : c
        if __debug__ :
            cls.Essence.children_frozen = True
        for c in cls.children :
            et = etype (c)
            if et :
                yield et
    # end def children_iter

    def pns_qualified (cls, name) :
        """Returns the `name` qualified with `Package_Namespace` of `cls`
           (i.e., includes the name of the Package_Namespace `cls` lives in,
           if any).
        """
        pkg_ns = getattr (cls, "Package_NS", None)
        if pkg_ns :
            result = "%s.%s" % (pkg_ns._Package_Namespace__qname, name)
        else :
            result = name
        return result
    # end def pns_qualified

    def set_ui_name (cls, ui_name) :
        """Sets `ui_name` of `cls`"""
        if not cls.show_package_prefix :
            cls.ui_name = ui_name
        else :
            cls.ui_name = cls.pns_qualified (ui_name)
    # end def set_alias

    def _m_add_prop (cls, prop, _Properties, verbose, parent = None, override = False) :
        name = prop.__name__
        if (not override) and name in _Properties._prop_dict :
            if __debug__ :
                if verbose :
                    p = _Properties._prop_dict.get (name)
                    print "Property %s.%s already defined for %s as %s [%s]" %\
                        ( cls.type_name, name, cls.app_type.name
                        , getattr (p,    "kind")
                        , getattr (prop, "kind")
                        )
        else :
            result = _Properties._add_prop (cls, name, prop)
            if result is not None and name not in _Properties._names :
                ### needed for descendents of `cls.Essence` yet to be imported
                _Properties._names [name] = prop
            return result
    # end def _m_add_prop

    def _m__call__ (cls, * args, ** kw) :
        result = cls.__new__ (cls, * args, ** kw)
        result.__init__      (* args, ** kw)
        cls.after_creation   (result)
        return result
    # end def _m__call__

    def _m_entity_type (cls, scope = None) :
        scope = cls._m_scope (scope)
        if scope is not None :
            return scope.entity_type (cls)
    # end def _m_entity_type

    def _m_get_attribute (cls, etype, name) :
        return getattr (etype, name)
    # end def _m_get_attribute

    def _m_init_name_attributes (cls) :
        cls.Essence = cls
        if "name" not in cls.__dict__ :
            cls.name = cls.__name__
        cls._set_type_names (cls.__name__)
    # end def _m_init_name_attributes

    def _m_scope (cls, scope = None, ** kw) :
        if scope is None :
            scope = MOM.Scope.active
            if scope.is_universe :
                scope = None
        return scope
    # end def _m_scope

    def _m_setup_attributes (cls) :
        pass ### XXX implement
    # end def _m_setup_attributes

    def _m_setup_attributes_dbw (cls) :
        cls._Attributes = A = cls.Essence._Attributes (cls)
        cls._Predicates = P = cls.Essence._Predicates (cls)
        attr_dict       = A._attr_dict
        cls.is_editable = (not cls.electric) and cls.user_attr
        cls.show_in_ui  = \
            (cls.record_changes and cls.generate_doc and not cls.is_partial)
        for pv in P._pred_kind.get ("object", []) :
            pn = pv.name
            for an in pv.attributes + pv.attr_none :
                if an in attr_dict :
                    attr = attr_dict [an]
                    if attr :
                        if attr.electric :
                            print ( "%s: %s attribute `%s` of `%s` cannot "
                                    "be referred to by object "
                                    "invariant `%s`"
                                  ) % (cls, attr.kind, an, cls.name, pn)
                        else :
                            attr.invariant.append (pn)
        P._syntax_checks = \
            [  a.attr for a in attr_dict.itervalues ()
            if (not a.electric) and TFL.callable (a.attr.check_syntax)
            ]
    # end def _m_setup_attributes_dbw

    def _m_setup_children (cls, bases) :
        cls.children = {}
        for b in bases :
            b.children [cls.type_name] = cls
            if __debug__ :
                if hasattr (b, "children_frozen") :
                    print \
                        ( "adding %s too late to `children` dict of %s"
                        % (cls.type_name, b.type_name)
                        )
    # end def _m_setup_children

    def _set_type_names (cls, base_name) :
        cls.type_base_name = base_name
        cls.type_name      = cls.pns_qualified (base_name)
        cls.set_ui_name (base_name)
    # end def _set_type_names

    def __getattr__ (cls, name) :
        ### delegate to scope specific class, if any
        if not (name.startswith ("__") and name.endswith ("__")) :
            etype = cls._m_entity_type ()
            if etype :
                return cls._m_get_attribute (etype, name)
        raise AttributeError, name
    # end def __getattr__

# end class M_E_Type

__doc__ = """
Class `MOM.Meta.M_E_Type`
================================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: M_E_Type

    `MOM.Meta.M_E_Type` provides the meta machinery for defining app-type
    specific essential object and link types (aka, e_types).

    Each instance of `M_E_Type` is a class that is defined using information
    of an essential class, i.e., a descendent of :class:`~_MOM.Entity.Entity`.

    For each instance of `M_E_Type`, it:

    ### XXX

    * Setups the attributes and predicates by instantiating
      `Essence._Attributes` and `Essence._Predicates` (and assigning it to
      class variables `_Attributes` and `_Predicates`, respectively, of the
      `etype`).

    * Assigns the class variables `is_editable` and `show_in_ui` according
      the settings of essential and app-type specific settings.

    * Checks that object predicates don't depend on electric attributes.

    * Adds all object predicates to the `invariant` lists of the attributes
      the predicates depend on.

    * Adds `_syntax_checks` entries to `_Predicates` for all non-electric
      attributes with a callable `check_syntax`.

    * Adds the `etype` to the `children` dictionary of all its base classes.

    `M_E_Type` provides the attribute:

    .. attribute:: default_child

      For partial classes, `default_child` can be set to refer to the
      non-partial descendent class that should be used by default (for
      instance, to create a new object in an object editor).

    `M_E_Type` provides the methods:

    .. automethod:: add_attribute
    .. automethod:: add_predicate

    .. method:: add_to_app_type(app_type)

      Adds the newly created `etype` to the `app_type`.

    .. automethod:: after_creation
    .. automethod:: children_iter


"""

if __name__ != "__main__" :
    MOM.Meta._Export ("M_Entity")
### __END__ MOM.Meta.M_E_Type
