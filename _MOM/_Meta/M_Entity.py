# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2011 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Meta.M_Entity
#
# Purpose
#    Meta class for essential entity
#
# Revision Dates
#    23-Sep-2009 (CT) Creation started (factored from `MOM.Meta.M_Entity`)
#    22-Oct-2009 (CT) Creation finished
#    27-Oct-2009 (CT) s/Scope_Proxy/E_Type_Manager/
#    28-Oct-2009 (CT) I18N
#    18-Nov-2009 (CT) Major surgery (removed generic e-types [i.e., those for
#                     non-derived app_types])
#    19-Nov-2009 (CT) `M_E_Type.sort_key` added
#    19-Nov-2009 (CT) `app_type.DBW.etype_decorator` called
#    23-Nov-2009 (CT) `Manager` for `M_Id_Entity.M_E_Type` corrected
#    24-Nov-2009 (CT) `_m_auto__init__` changed to set `i_bases` of `__init__`
#    25-Nov-2009 (CT) `_m_setup_attributes` changed to use `P._attr_map`
#                     instead of `attr.invariant` (because `attr` can be shared
#                     between superclass and subclasses, but `P` isn't shared)
#    26-Nov-2009 (CT) `M_Id_Entity.__init__` added to disallow redefinition
#                     of `__init__`
#    26-Nov-2009 (CT) `_m_auto__init__` changed to chain up directly to
#                     `self._MOM_Entity__init__`
#    26-Nov-2009 (CT) `M_Entity`: `add_attribute` and `add_predicate` added
#    27-Nov-2009 (CT) `_m_setup_prop_names` factored and called from
#                     `m_setup_etypes`, too
#    27-Nov-2009 (CT) `M_E_Type_Id.sort_key` fixed by introducing `__sort_key`
#    28-Nov-2009 (CT) `_m_init_prop_specs` changed to assign `is_partial` to
#                     `False` unless it is contained in `dct`
#    30-Nov-2009 (CT) `_m_create_e_types` changed to call
#                     `app_type.DBW.update_etype` after all etypes were created
#     3-Dec-2009 (CT) `_m_setup_sorted_by` added and called
#    14-Dec-2009 (CT) `g_rank`, `i_rank`, and `m_sorted_by` added
#    16-Dec-2009 (MG) `_m_create_e_types` call `DBW.prepare` before the
#                     e-types will be created
#    22-Dec-2009 (CT) `_m_new_e_type_dict` changed to include `epk_sig`
#    30-Dec-2009 (CT) s/Package_NS/PNS/, `PNS_s` added
#     5-Jan-2010 (CT) Use `TFL._Meta.M_Auto_Combine` as base class
#    14-Jan-2010 (CT) `PNS_s` removed
#    21-Jan-2010 (CT) `M_Id_Entity` changed to auto-generate `epkified_ckd`
#                     and `epkified_raw` instead of `__init__`
#    27-Jan-2010 (MG) Add `app_type` parameter when calling `update_etype`
#     4-Feb-2010 (CT) `M_E_Type_An` added
#     7-Feb-2010 (MG) `M_E_Type_An.__call__` added to support creation of
#                     scopeless `An_Entity's`
#     9-Feb-2010 (CT) `M_E_Type_An._m_setup_attributes` redefined to set
#                     `hash_sig`
#    12-Feb-2010 (CT) `M_Entity._m_init_prop_specs` changed to create a new
#                     `ui_display` attribute for each class (with the proper
#                     `ui_name`)
#    18-Feb-2010 (CT) `M_E_Type_An._m_setup_sorted_by` redefined
#    25-Feb-2010 (CT) `M_E_Type._m_setup_attributes` changed to handle
#                     `check_always`
#     1-Mar-2010 (CT) `M_E_Type.m_recordable_attrs` added
#     1-Mar-2010 (CT) `M_E_Type_An._m_setup_attributes` changed to guard
#                     against `primary`
#     5-Mar-2010 (CT) `_m_setup_attributes` changed to set `.Class` of
#                     `_A_Object_` attributes to app_type specific e-type
#    11-Mar-2010 (CT) `M_Id_Entity` changed t use `epk_def_set_ckd` and
#                     `epk_def_set_raw`
#    11-Mar-2010 (CT) `check_always` removed (was a Bad Idea (tm))
#    12-Mar-2010 (CT) `link_map` moved in here (from `M_Object`)
#    24-Mar-2010 (CT) `_set_type_names` changed to take `ui_name` from
#                     `cls.__dict__` if there
#    27-Mar-2010 (MG) `polymorphic_epk` added
#     8-Apr-2010 (CT) `_m_create_e_types` to percolate `polymorphic_epk` up to
#                     base classes
#     9-Apr-2010 (CT) `M_Id_Entity._m_new_e_type_dict` changed to  filter
#                     attributes set to `None`
#    21-Apr-2010 (CT) `M_Id_Entity._m_new_e_type_dict` changed to use `_d_rank`
#     3-May-2010 (CT) `Type_Name_Type` added and used for `type_name`
#    22-Jun-2010 (CT) `_m_setup_attributes` changed to set `is_mandatory` and
#                     to put `a` instead of `a.attr` into `P._syntax_checks`
#    24-Jun-2010 (CT) `db_sig` added
#     5-Aug-2010 (CT) Property `M_E_Type.Class` added
#     9-Aug-2010 (CT) `M_E_Type_Id._m_setup_sorted_by` changed to handle
#                     `_A_Composite_` attributes properly
#     3-Sep-2010 (CT) `M_E_Type_An._m_setup_attributes` changed to set
#                     `cls.hash_sig` to `.user_attr` instead of `.required`
#     4-Sep-2010 (CT) `M_E_Type.__init__` changed to set `Class` and `C_Type`
#                     to `cls` (property `M_E_Type.Class` removed)
#    13-Oct-2010 (CT) `default_child` added
#    17-Nov-2010 (CT) `_m_setup_sorted_by` changed to honor `sort_rank`
#     8-Feb-2011 (CT) s/Mandatory/Required/
#    10-Feb-2011 (CT) `_nested_classes_to_combine` defined as class attribute
#    10-Feb-2011 (CT) `_m_combine_nested_class` factored to `TFL.Meta.M_Base`
#    24-Feb-2011 (CT) s/A_Object/A_Entity/
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _TFL._Meta.M_Auto_Combine
import _TFL._Meta.Once_Property
import _TFL.Decorator
import _TFL.Sorted_By

from   _TFL.predicate        import any_true
from   _TFL.object_globals   import class_globals
from   _TFL.I18N             import _, _T, _Tn

import _MOM._Meta
import _MOM.Scope
import _MOM.E_Type_Manager

import sys

class Type_Name_Type (str) :
    """Type used for `type_name`."""

    pass

# end class Type_Name_Type

class M_E_Mixin (TFL.Meta.M_Auto_Combine) :
    """Meta mixin for M_Entity and M_E_Type."""

    _Class_Kind    = "Bare Essence"

    _S_Extension   = []     ### List of E_Spec
    _BET_map       = {}     ### Dict of bare essential types (type_name -> BET)

    m_sorted_by    = TFL.Sorted_By ("rank", "i_rank")

    Type_Name_Type = Type_Name_Type

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__      (name, bases, dict)
        cls._m_init_name_attributes ()
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        raise TypeError \
            ( _T ("Can't instantiate %s %r, use <scope>.%s %r instead")
            % (cls.type_name, args, cls.type_name, args)
            )
    # end def __call__

    @property
    def default_child (cls) :
        if cls.is_partial :
            return cls._default_child
    # end def default_child

    @default_child.setter
    def default_child (cls, child) :
        if not cls.is_partial :
            raise TypeError, \
                ( "Cannot set default_child of non-partial class %s to %s"
                % (cls, child)
                )
        elif cls._default_child is not None :
            raise TypeError, \
                ( "Cannot change default_child of class %s from %s to %s"
                % (cls, cls._default_child, child)
                )
        else :
            if isinstance (child, M_E_Mixin) :
                child = child.type_name
            cls._default_child = child
    # end def default_child

    def m_setup_etypes (cls, app_type) :
        """Setup EMS- and DBW -specific essential types for all classes in
           `cls._S_Extension`.
        """
        assert not app_type.etypes
        if not cls._BET_map :
            cls.m_init_etypes ()
            ### Call `_m_setup_prop_names` again to make sure automatically
            ### created properties are included in subclasses, too
            for s in cls._S_Extension :
                s._m_setup_prop_names ()
        cls._m_create_e_types (app_type, cls._S_Extension)
        for t in reversed (app_type._T_Extension) :
            t._m_setup_relevant_roots ()
    # end def m_setup_etypes

    def pns_qualified (cls, name) :
        """Returns the `name` qualified with `Package_Namespace` of `cls`
           (i.e., includes the name of the Package_Namespace `cls` lives in,
           if any).
        """
        pkg_ns = getattr (cls, "PNS", None)
        if pkg_ns :
            result = ".".join ((pkg_ns._Package_Namespace__qname, name))
        else :
            result = name
        return result
    # end def pns_qualified

    def set_default_child (cls, child) :
        cls.default_child = child
        return child
    # end def set_default_child

    def set_ui_name (cls, ui_name) :
        """Sets `ui_name` of `cls`"""
        if not cls.show_package_prefix :
            cls.ui_name = ui_name
        else :
            cls.ui_name = cls.pns_qualified (ui_name)
    # end def set_alias

    def _m_init_name_attributes (cls) :
        cls._set_type_names (cls.__name__)
    # end def _m_init_name_attributes

    def _m_create_e_types (cls, app_type, SX) :
        etypes   = app_type.etypes
        e_deco   = app_type.DBW.etype_decorator
        e_update = app_type.DBW.update_etype
        app_type.DBW.prepare ()
        for s in SX :
            app_type.add_type (e_deco (s._m_new_e_type (app_type, etypes)))
        for t in reversed (app_type._T_Extension) :
            if getattr (t, "polymorphic_epk", None) :
                for b in t.__bases__ :
                    if getattr (b, "polymorphic_epk", None) is False :
                        b.polymorphic_epk = True
        for t in app_type._T_Extension :
            t._m_setup_sorted_by ()
            ### `DBW.update_etype` can use features like `children` or
            ### `link_map` that are only available after *all* etypes have
            ### already been created
            e_update (t, app_type)
    # end def _m_create_e_types

    def _m_new_e_type (cls, app_type, etypes) :
        bases  = cls._m_new_e_type_bases (app_type, etypes)
        dct    = cls._m_new_e_type_dict  (app_type, etypes, bases)
        result = cls.M_E_Type            (dct.pop ("__name__"), bases, dct)
        return result
    # end def _m_new_e_type

    def _m_new_e_type_bases (cls, app_type, etypes) :
        return tuple (cls._m_new_e_type_bases_iter (app_type, etypes))
    # end def _m_new_e_type_bases

    def _m_new_e_type_bases_iter (cls, app_type, etypes) :
        yield cls.Essence
        for b in cls.__bases__ :
            tn = getattr (b, "type_name", None)
            if tn in etypes :
                b = etypes [tn]
            if b is not cls.Essence :
                yield b
    # end def _m_new_e_type_bases_iter

    def _m_new_e_type_dict (cls, app_type, etypes, bases, ** kw) :
        if "epk_sig" not in kw :
            kw ["epk_sig"] = ()
        return dict  \
            ( cls.__dict__
            , app_type      = app_type
            , children      = {}
            , M_E_Type      = cls.M_E_Type
            , __metaclass__ = None ### avoid `Metatype conflict among bases`
            , __name__      = cls.__dict__ ["__real_name"] ### M_Autorename
            , _real_name    = cls.type_base_name           ### M_Autorename
            , ** kw
            )
    # end def _m_new_e_type_dict

    def _m_setup_prop_names (cls) :
        for P in cls._Attributes, cls._Predicates :
            P.m_setup_names ()
    # end def _m_setup_prop_names

    def _set_type_names (cls, base_name) :
        cls.type_base_name = base_name
        cls.type_name      = cls.Type_Name_Type (cls.pns_qualified (base_name))
        cls.set_ui_name (cls.__dict__.get ("ui_name", base_name))
    # end def _set_type_names

    def __repr__ (cls) :
        app_type = getattr (cls, "app_type", None)
        if app_type :
            kind = app_type.name
        else :
            kind = getattr (cls, "_Class_Kind", "unknown")
        return "<class %r [%s]>" % (cls.type_name, kind)
    # end def __repr__

# end class M_E_Mixin

class M_Entity (M_E_Mixin) :
    """Meta class for essential entity of MOM meta object model."""

    _nested_classes_to_combine = ("_Attributes", "_Predicates")

    def __new__ (mcls, name, bases, dct) :
        dct ["_default_child"] = dct.pop ("default_child", None)
        result = super (M_Entity, mcls).__new__ (mcls, name, bases, dct)
        return result
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__  (name, bases, dict)
        cls._m_init_prop_specs  (name, bases, dict)
        cls._S_Extension.append (cls)
        cls.i_rank = len (cls._S_Extension) - 1
        cls.g_rank = 1 + max \
            ([getattr (b, "g_rank", -1) for b in bases] + [-1])
    # end def __init__

    def add_attribute (cls, attr, verbose = True, override = False) :
        """Add `attr` to `cls`"""
        cls._m_add_prop (attr, cls._Attributes, verbose, override)
    # end def add_attribute

    def add_predicate (cls, pred, verbose = True, override = False) :
        """Add `pred` to `cls`"""
        cls._m_add_prop (pred, cls._Predicates, verbose, override)
    # end def add_predicate

    def m_init_etypes (cls) :
        """Initialize bare essential types for all classes in `cls._S_Extension`."""
        if not cls._BET_map :
            SX = cls._S_Extension
            cls._m_create_base_e_types (SX)
            cls._m_setup_auto_props    (SX)
    # end def m_setup_etypes

    def _m_add_prop (cls, prop, _Properties, verbose, override = False) :
        name = prop.__name__
        if (not override) and name in _Properties._names :
            if __debug__ :
                if verbose :
                    p = _Properties._names.get (name)
                    print "Property %s.%s already defined as %s [%s]" %\
                        ( cls.type_name, name
                        , getattr (p,    "kind")
                        , getattr (prop, "kind")
                        )
        else :
            _Properties._m_add_prop (cls, name, prop)
    # end def _m_add_prop

    def _m_create_base_e_types (cls, SX) :
        BX = cls._BET_map
        for s in SX :
            tbn = s.type_base_name
            bet = M_E_Mixin \
                ( "_BET_%s_" % s.type_base_name
                , tuple (getattr (b, "__BET", b) for b in s.__bases__)
                , dict
                    ( app_type            = None
                    , E_Spec              = s
                    , is_partial          = s.is_partial
                    , PNS                 = s.PNS
                    , show_package_prefix = s.show_package_prefix
                    , _real_name          = tbn
                    , __module__          = s.__module__
                    )
                )
            bet.Essence = s.Essence = BX [tbn] = bet
            setattr   (bet,                        "__BET", bet)
            setattr   (s,                          "__BET", bet)
            setattr   (s.PNS,                      tbn,     bet)
            setattr   (sys.modules [s.__module__], tbn,     bet)
    # end def _m_create_base_e_types

    def _m_init_prop_specs (cls, name, bases, dct) :
        if "is_partial" not in dct :
            setattr (cls, "is_partial", False)
        for psn in cls._nested_classes_to_combine :
            cls._m_combine_nested_class (psn, bases, dct)
        if "ui_display" not in cls._Attributes.__dict__ :
            base = cls._Attributes.ui_display
            cls._Attributes.ui_display = base.__class__ \
                ("ui_display", (base, ), dict (ui_name = cls.ui_name))
    # end def _m_init_prop_specs

    def _m_setup_auto_props (cls, SX) :
        for c in SX :
            c._m_setup_etype_auto_props ()
    # end def _m_setup_auto_props

    def _m_setup_etype_auto_props (cls) :
        cls._m_setup_prop_names ()
    # end def _m_setup_etype_auto_props

# end class M_Entity

class M_An_Entity (M_Entity) :
    """Meta class for MOM.An_Entity"""

# end class M_An_Entity

class M_Id_Entity (M_Entity) :
    """Meta class for MOM.Id_Entity"""

    _epkified_sep  = "\n    "
    _epkified_head = """def epkified_%(suffix)s (cls, %(args)s) :"""
    _epkified_tail = """return (%(epk)s), kw\n"""

    def __init__ (cls, name, bases, dict) :
        assert "__init__" not in dict, \
          "%s: please redefine `_finish__init__`, not __init__" % cls
        cls.__m_super.__init__  (name, bases, dict)
    # end def __init__

    def _m_auto_epkified (cls, epk_sig, args, code, suffix) :
        form    = cls._epkified_sep.join \
            (x for x in (cls._epkified_head, code, cls._epkified_tail) if x)
        globals = class_globals (cls)
        scope   = dict          ()
        code    = form % dict \
            ( epk    = ", ".join (epk_sig) + ("," if len (epk_sig) == 1 else "")
            , args   = ", ".join (x for x in (args, "** kw") if x)
            , suffix = suffix
            )
        exec code in globals, scope
        result             = scope ["epkified_%s" % suffix]
        result.epk_sig     = epk_sig
        result.args        = args
        result.source_code = code
        return classmethod (result)
    # end def _m_auto_epkified

    def _m_new_e_type_dict (cls, app_type, etypes, bases, ** kw) :
        pkas      = sorted \
            ( (  a for a in cls._Attributes._names.itervalues ()
              if a is not None and a.kind.is_primary
              )
            , key = TFL.Sorted_By ("kind._k_rank", "_t_rank", "rank", "_d_rank")
            )
        epk_sig   = tuple (a.name for a in pkas)
        rel_bases = (b for b in bases if getattr (b, "is_relevant", False))
        pol_epk   = any_true \
            ( (  getattr (rb, "polymorphic_epk", False)
              or rb.epk_sig != epk_sig
              )
            for rb in rel_bases
            )
        a_ckd     = ", ".join (a.as_arg_ckd () for a in pkas)
        a_raw     = ", ".join (a.as_arg_raw () for a in pkas)
        d_ckd     = cls._epkified_sep.join \
            (x for x in (a.epk_def_set_ckd () for a in pkas) if x)
        d_raw     = cls._epkified_sep.join \
            (x for x in (a.epk_def_set_raw () for a in pkas) if x)
        result    = cls.__m_super._m_new_e_type_dict \
            ( app_type, etypes, bases
            , epk_sig         = epk_sig
            , epkified_ckd    = cls._m_auto_epkified
                (epk_sig, a_ckd, d_ckd, "ckd")
            , epkified_raw    = cls._m_auto_epkified
                (epk_sig, a_raw, d_raw, "raw")
            , is_relevant     = cls.is_relevant or (not cls.is_partial)
            , polymorphic_epk = pol_epk
            , _all_link_map   = None
            , _own_link_map   = TFL.defaultdict (set)
            , ** kw
            )
        return result
    # end def _m_new_e_type_dict

# end class M_Id_Entity

@TFL.Add_To_Class ("M_E_Type", M_Entity)
class M_E_Type (M_E_Mixin) :
    """Meta class for for essence of MOM.Entity."""

    app_type    = None

    _Class_Kind = "Essence"

    @TFL.Meta.Once_Property
    def db_sig (cls) :
        return (cls.type_name, tuple (a.db_sig for a in cls.db_attr))
    # end def db_sig

    @TFL.Meta.Once_Property
    def m_recordable_attrs (cls) :
        """Set of attributes that need recording by change management and DBW"""
        return set \
            (a for a in cls.attributes.itervalues () if a.record_changes)
    # end def m_recordable_attrs

    def __init__ (cls, name, bases, dct) :
        cls.Class = cls.C_Type = cls
        cls.__m_super.__init__  (name, bases, dct)
        cls._m_setup_children   (bases, dct)
        cls._m_setup_attributes (bases, dct)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        if "scope" not in kw :
            raise MOM.Error.No_Scope
        return cls._m_call (* args, ** kw)
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
        etype = cls.app_type.entity_type
        for c in cls.children :
            et = etype (c)
            if et :
                yield et
    # end def children_iter

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

    def _m_call (cls, * args, ** kw) :
        result = cls.__new__ (cls, * args, ** kw)
        result.__init__      (* args, ** kw)
        cls.after_creation   (result)
        return result
    # end def _m_call

    def _m_entity_type (cls, scope = None) :
        scope = cls._m_scope (scope)
        if scope is not None :
            return scope.entity_type (cls)
    # end def _m_entity_type

    def _m_get_attribute (cls, etype, name) :
        return getattr (etype, name)
    # end def _m_get_attribute

    def _m_scope (cls, scope = None, ** kw) :
        if scope is None :
            scope = MOM.Scope.active
            if scope.is_universe :
                scope = None
        return scope
    # end def _m_scope

    def _m_setup_attributes (cls, bases, dct) :
        cls._Attributes = A = cls._Attributes (cls)
        cls._Predicates = P = cls._Predicates (cls)
        attr_dict       = A._attr_dict
        app_type        = cls.app_type
        for ak in attr_dict.itervalues () :
            at = ak.attr
            if isinstance (at, MOM.Attr._A_Entity_) and at.Class :
                ats = app_type.entity_type (at.Class)
                if ats :
                    at.Class = ats
        for pv in P._pred_kind.get ("object", []) :
            pn = pv.name
            for an in pv.attributes + pv.attr_none :
                if an in attr_dict :
                    attr = attr_dict [an]
                    if attr :
                        if attr.electric :
                            if not isinstance (attr, MOM.Attr.Once_Cached) :
                                print \
                                    ( "%s: %s attribute `%s` of `%s` cannot "
                                      "be referred to by object "
                                      "invariant `%s`"
                                    ) % (cls, attr.kind, an, cls.type_name, pn)
                        else :
                            P._attr_map [attr.attr].append (pn)
                            if attr.is_required :
                                pv.pred.is_required = True
        P._syntax_checks = \
            [  a for a in attr_dict.itervalues ()
            if (not a.electric) and TFL.callable (a.attr.check_syntax)
            ]
    # end def _m_setup_attributes

    def _m_setup_children (cls, bases, dct) :
        cls.children = {}
        for b in bases :
            if isinstance (b, M_E_Type) :
                b.children [cls.type_name] = cls
    # end def _m_setup_children

    def _m_setup_relevant_roots (cls) :
        pass
    # end def _m_setup_relevant_roots

    def _m_setup_sorted_by (cls) :
        pass
    # end def _m_setup_sorted_by

    def __getattr__ (cls, name) :
        ### just to ease up-chaining in descendents
        raise AttributeError ("%s.%s" % (cls.type_name, name))
    # end def __getattr__

# end class M_E_Type

@TFL.Add_To_Class ("M_E_Type", M_An_Entity)
class M_E_Type_An (M_E_Type) :
    """Meta class for essence of MOM.An_Entity."""

    Manager     = MOM.E_Type_Manager.An_Entity

    def __call__ (cls, * args, ** kw) :
        if "scope" not in kw :
            kw ["scope"] = MOM.Scope.active
        return cls._m_call (* args, ** kw)
    # end def __call__

    def _m_setup_attributes (cls, bases, dct) :
        cls.__m_super._m_setup_attributes (bases, dct)
        cls.hash_sig = cls.user_attr
        assert not cls.primary, \
            "An_Entity `%s` cannot have primary attributes" % (cls.type_name, )
    # end def _m_setup_attributes

    def _m_setup_sorted_by (cls) :
        cls.sorted_by = TFL.Sorted_By (* tuple (a.name for a in cls.hash_sig))
    # end def _m_setup_sorted_by

# end class M_E_Type_An

@TFL.Add_To_Class ("M_E_Type", M_Id_Entity)
class M_E_Type_Id (M_E_Type) :
    """Meta class for essence of MOM.Id_Entity."""

    Manager     = MOM.E_Type_Manager.Id_Entity

    @property
    def link_map (cls) :
        result = cls._all_link_map
        if result is None :
            result = cls._all_link_map = TFL.defaultdict (set)
            refuse = cls.refuse_links
            for b in cls.__bases__ :
                for k, v in getattr (b, "link_map", {}).iteritems () :
                    if k not in refuse :
                        result [k].update (v)
            for k, v in cls._own_link_map.iteritems () :
                result [k].update (v)
        return result
    # end def link_map

    def sort_key (cls, sort_key = None) :
        ###
        ### Using `cls.sorted_by` here fails in Python 3.x for sorting
        ### lists with different link types
        ###
        ###     Because each link type redefines `sorted_by` differently,
        ###     `cls.sorted_by` of their common ancestor doesn't do
        ###     the right thing (TM)
        ###
        ### `__sort_key` re-evaluates `sorted_by` for each `entity` to be
        ### sorted and thus avoids this problem
        ###
        ### `epk_sig` needs to be included to support subclasses of a
        ### specific `relevant_root` to extend `epk`
        ###
        return TFL.Sorted_By \
            ("relevant_root.type_name", "epk_sig", sort_key or cls.__sort_key)
    # end def sort_key

    def __sort_key (cls, entity) :
        return entity.sorted_by (entity)
    # end def __sort_key

    def _m_setup_attributes (cls, bases, dct) :
        cls.__m_super._m_setup_attributes (bases, dct)
        cls.is_editable = (not cls.electric.default) and cls.user_attr
        cls.show_in_ui  = \
            (cls.record_changes and cls.generate_doc and not cls.is_partial)
    # end def _m_setup_attributes

    def _m_setup_children (cls, bases, dct) :
        cls.__m_super._m_setup_children (bases, dct)
        if cls.is_relevant :
            if not any (getattr (b, "is_relevant", False) for b in bases) :
                cls.relevant_root = cls
        else :
            cls.relevant_roots = {}
    # end def _m_setup_children

    def _m_setup_sorted_by (cls) :
        sbs = []
        if cls.epk_sig :
            for pka in sorted (cls.primary, key = TFL.Getter.sort_rank) :
                if isinstance (pka.attr, MOM.Attr._A_Entity_) :
                    et = pka.Class
                    if et :
                        sbs.extend \
                            ("%s.%s" % (pka.name, x) for x in et.sorted_by_epk)
                    else :
                        ### Class is to abstract: need to use `cls.sort_key`
                        sbs = [cls.sort_key]
                        break
                elif isinstance (pka.attr, MOM.Attr._A_Composite_) :
                    sbs.extend \
                        ("%s.%s" % (pka.name, x) for x in pka.Class.sorted_by)
                else :
                    sbs.append (pka.name)
        sb = TFL.Sorted_By (* (sbs or [cls.sort_key]))
        cls.sorted_by_epk = sb
    # end def _m_setup_sorted_by

    def _m_setup_relevant_roots (cls) :
        if not cls.relevant_root :
            rr = cls.relevant_roots
            for c in cls.children.itervalues () :
                if c.relevant_root is c :
                    rr [c.type_name] = c
                else :
                    rr.update (c.relevant_roots)
    # end def _m_setup_relevant_roots

# end class M_E_Type_Id

__doc__ = """
Class `MOM.Meta.M_Entity`
=========================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: M_Entity

    `MOM.Meta.M_Entity` provides the meta machinery for defining the
    characteristics of essential object and link types of the MOM meta object
    model. It is the common base class for
    :class:`MOM.Meta.M_Object<_MOM._Meta.M_Object.M_Object>` and
    :class:`MOM.Meta.M_Link<_MOM._Meta.M_Link.M_Link>`.

XXX

.. class:: M_E_Type

    `MOM.Meta.M_E_Type` provides the meta machinery for defining app-type
    specific essential object and link types (aka, e_types).

    Each instance of `M_E_Type` is a class that is defined using information
    of an essential class, i.e., a descendent of :class:`~_MOM.Entity.Entity`.

    For each instance of `M_E_Type`, it:

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
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Entity
