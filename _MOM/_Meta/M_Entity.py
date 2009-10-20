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
#    MOM.Meta.M_Entity
#
# Purpose
#    Meta class for essential entity
#
# Revision Dates
#    23-Sep-2009 (CT) Creation (factored from `MOM.Meta.M_Entity`)
#    13-Oct-2009 (CT) Creation continued
#    14-Oct-2009 (CT) Creation continued..
#    15-Oct-2009 (CT) Creation continued...
#    16-Oct-2009 (CT) Creation continued....
#    18-Oct-2009 (CT) Creation continued.....
#    19-Oct-2009 (CT) Creation continued.....
#    20-Oct-2009 (CT) Creation continued......
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _TFL._Meta.M_Class
import _TFL.Sorted_By

from   _TFL.object_globals import class_globals

import _MOM._Meta

import sys

class M_E_Mixin (TFL.Meta.M_Class) :
    """Meta mixin for M_Entity and M_E_Type."""

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__      (name, bases, dict)
        cls._m_init_name_attributes ()
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        raise TypeError \
            ( "Can't instantiate %s %r, use <scope>.%s %r instead"
            % (cls.type_name, args, cls.type_name, args)
            )
    # end def __call__

    def pns_qualified (cls, name) :
        """Returns the `name` qualified with `Package_Namespace` of `cls`
           (i.e., includes the name of the Package_Namespace `cls` lives in,
           if any).
        """
        pkg_ns = getattr (cls, "Package_NS", None)
        if pkg_ns :
            result = ".".join ((pkg_ns._Package_Namespace__qname, name))
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

    def _m_init_name_attributes (cls) :
        cls._set_type_names (cls.__name__)
    # end def _m_init_name_attributes

    def _m_create_e_types (cls, app_type, SX) :
        etypes = app_type.etypes
        for s in SX :
            app_type.add_type (s._m_new_e_type (app_type, etypes))
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
        return dict  \
            ( cls.__dict__
            , app_type      = app_type
            , children      = {}
            , __metaclass__ = None ### avoid `Metatype conflict among bases`
            , __name__      = cls.__dict__ ["__real_name"] ### M_Autorename
            , _real_name    = cls.type_base_name           ### M_Autorename
            , ** kw
            )
    # end def _m_new_e_type_dict

    def _set_type_names (cls, base_name) :
        cls.type_base_name = base_name
        cls.type_name      = cls.pns_qualified (base_name)
        cls.set_ui_name (base_name)
    # end def _set_type_names

    def __repr__ (cls) :
        if cls.app_type :
            return "<class %r [%s]>" % (cls.type_name, cls.app_type.name)
        return "<class %r [Bare Essence]>" % (cls.type_name, )
    # end def __repr__

# end class M_E_Mixin

class M_Entity (M_E_Mixin) :
    """Meta class for essential entity of MOM meta object model."""

    _S_Extension = []     ### List of E_Spec

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__  (name, bases, dict)
        cls._m_init_prop_specs  (name, bases, dict)
        cls._S_Extension.append (cls)
    # end def __init__

    def m_setup_etypes (cls, app_type) :
        """Setup essential types for all classes in `cls._S_Extension`."""
        import _MOM._Meta.M_E_Type
        assert not app_type.etypes
        SX = cls._S_Extension
        cls._m_create_base_e_types (SX)
        cls._m_setup_auto_props    (app_type, SX)
        cls._m_create_e_types      (app_type, SX)
    # end def m_setup_etypes

    def _m_create_base_e_types (self, SX) :
        for s in SX :
            tbn = s.type_base_name
            bet = M_E_Mixin \
                ( "_BET_%s_" % s.type_base_name
                , tuple (getattr (b, "__BET", b) for b in s.__bases__)
                , dict
                    ( app_type            = None
                    , E_Spec              = s
                    , Package_NS          = s.Package_NS
                    , show_package_prefix = s.show_package_prefix
                    , _real_name          = tbn
                    , __module__          = s.__module__
                    )
                )
            bet.Essence = s.Essence = bet
            setattr (bet,                        "__BET", bet)
            setattr (s,                          "__BET", bet)
            setattr (s.Package_NS,               tbn,     bet)
            setattr (sys.modules [s.__module__], tbn,     bet)
    # end def _m_create_base_e_types

    def _m_init_prop_specs (cls, name, bases, dct) :
        for psn in "_Attributes", "_Predicates" :
            if psn not in dct :
                prop_bases = tuple (getattr (b, psn) for b in bases)
                d          = dict  (__module__ = cls.__module__)
                ### `TFL.Meta.M_M_Class` will choose the right meta class
                ### (i.e., `M_Attr_Spec` or `M_Pred_Spec`)
                setattr (cls, psn, MOM.Meta.M_Prop_Spec (psn, prop_bases, d))
    # end def _m_init_prop_specs

    def _m_setup_auto_props (cls, app_type, SX) :
        for c in SX :
            c._m_setup_etype_auto_props (app_type)
    # end def _m_setup_auto_props

    def _m_setup_etype_auto_props (cls, app_type) :
        for P in cls._Attributes, cls._Predicates :
            P.m_setup_names ()
    # end def _m_setup_etype_auto_props

# end class M_Entity

class M_An_Entity (M_Entity) :
    """Meta class for MOM.An_Entity"""

# end class M_An_Entity

class M_Id_Entity (M_Entity) :
    """Meta class for MOM.Id_Entity"""

    ### `_init_form` needs `* args` to allow additional primary keys in
    ### descendent classes to properly percolate up
    _init_form = """def __init__ (self, %(epk)s, * args, ** kw) :
        return super (%(type)s, self).__init__ (%(epk)s, * args, ** kw)
"""

    def _m_auto__init__ (cls, epk_sig) :
        globals = class_globals (cls)
        scope   = dict          ()
        code    = cls._init_form % dict \
            ( epk  = ", ".join (epk_sig)
            , type = cls.type_base_name
            )
        exec code in globals, scope
        result             = scope ["__init__"]
        result.epk_sig     = epk_sig
        result.source_code = code
        return result
    # end def _m_auto__init__

    def _m_new_e_type_dict (cls, app_type, etypes, bases, ** kw) :
        result = cls.__m_super._m_new_e_type_dict \
            ( app_type, etypes, bases
            , is_relevant = cls.is_relevant or (not cls.is_partial)
            , ** kw
            )
        pkas   = tuple \
            (  a for a in cls._Attributes._names.itervalues ()
            if a.kind.is_primary
            )
        if pkas and "__init__" not in result :
            M_E_Type_Id = MOM.Meta.M_E_Type_Id
            epk_sig = tuple \
                ( a.name
                for a in sorted (pkas, key = TFL.Sorted_By ("rank", "name"))
                )
            i_bases = tuple (b for b in bases if isinstance (b, M_E_Type_Id))
            if not (i_bases and i_bases [0].epk_sig == epk_sig) :
                result ["__init__"] = cls._m_auto__init__ (epk_sig)
        return result
    # end def _m_new_e_type_dict

    ### XXX Should this go into M_Link ???
    def _m_setup_etype_auto_props (cls, app_type) :
        cls.__m_super._m_setup_etype_auto_props (app_type)
        ### XXX Create auto-props for cached roles
    # end def _m_setup_etype_auto_props

# end class M_Id_Entity

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

    For each essential class, `M_Entity`:

    - Creates `_Attributes` and `_Predicates`, if they weren't already
      defined by the class definition.

    - Defines the class attributes

      .. attribute:: Essence

          Always points to the class defining the essence (even in the
          automatically generated ats-specific children of that class).

      .. attribute:: name

          Refers to the essential name of the class.

      .. attribute:: type_base_name

          Refers to the essential name of the class.

      .. attribute:: type_name

          Refers to the essential name of the class qualified by the
          name of defining :attr:`package namespace<_MOM.Entity.Package_NS>`.

      .. attribute:: ui_name

          Refers to the name of the class to be displayed by the user
          interface(s). Depending on the class variable
          :attr:`~_MOM.Entity.show_package_prefix`, `ui_name` might or
          might not be qualified by the name of defining
          :attr:`package namespace<_MOM.Entity.Package_NS>`.

    ### XXX ???
    `M_Entity` delegates two operations to the scope-specific type
    of the class:

    - object creation,

    - attribute access (for attributes not defined by the essential
      class itself).

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Entity
