# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.MOM.Spec
#
# Purpose
#    Specification of AFS forms for MOM entities
#
# Revision Dates
#    14-Feb-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM                     import MOM
from   _TFL                     import TFL

from   _GTW._AFS._MOM           import Element

import _MOM._Attr.Type

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Decorator
import _TFL.multimap

class _Base_ (TFL.Meta.Object) :
    """Base class for spec classes"""

    defaults = {}
    rank     = 0

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "rank")
        self.kw = dict (self.defaults, ** kw)
    # end def __init__

    def __getattr__ (self, name) :
        try :
            return self.kw [name]
        except KeyError :
            raise AttributeError (name)
    # end def __getattr__

# end class _Base_

class _Entity_Mixin_ (_Base_) :

    attr_spec           = {}
    defaults            = {}
    include_kind_groups = False
    _elems              = None

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "include_kind_groups")
        self.attr_spec = TFL.mm_dict \
            (self.attr_spec, ** kw.pop ("attr_spec", {}))
        self.__super.__init__ (** kw)
    # end def __init__

    def __call__ (self, E_Type, spec = None, seen = None) :
        if seen is None :
            seen = set ()
        kw       = self.kw
        elems    = sorted (self.elements (E_Type), key = TFL.Getter.rank)
        children = (e (E_Type, self, seen) for e in elems)
        kw.setdefault ("name", E_Type.type_name)
        return self.Type \
            ( children  = tuple (c for c in children if c is not None)
            , type_name = E_Type.type_name
            , ** kw
            )
    # end def __call__

    def default_elements (self, E_Type) :
        return \
            ( Field_Group_Primary   ()
            , Field_Group_Required  ()
            , Field_Group_Necessary ()
            , Field_Group_Optional  ()
            )
    # end def default_elements

    def elements (self, E_Type) :
        if self.include_kind_groups :
            for e in self.default_elements (E_Type) :
                yield e
        for e in self._elems :
            yield e
    # end def elements

# end class _Entity_Mixin_

class _Field_ (_Base_) :

    pass

# end class _Field_

@TFL.Add_To_Class ("AFS_Spec", MOM.Attr.A_Attr_Type)
class Field (_Field_) :
    """Specification for a field of a AFS form."""

    Type     = Element.Field

    def __call__ (self, E_Type, spec, seen) :
        return self.Type (** self.kw)
    # end def __call__

# end class Field

@TFL.Add_To_Class ("AFS_Spec", MOM.Attr._A_Composite_)
class Field_Composite (_Entity_Mixin_, _Field_) :
    """Specification for a composite field of a AFS form."""

    Type     = Element.Field_Composite

    def __init__ (self, ** kw) :
        self._elems = kw.pop ("elements", ())
        self.__super.__init__ (** kw)
        self.include_kind_groups = True
    # end def __init__

    def __call__ (self, E_Type, spec, seen) :
        attr = getattr (E_Type, self.name)
        return self.__super.__call__ (attr.C_Type, self, set ())
    # end def __call__

    def default_elements (self, E_Type) :
        fg = Field_Group_K (kind = "user_attr")
        for f in fg.fields (E_Type, self, set ()) :
            yield f
    # end def default_elements

# end class Field_Composite

@TFL.Add_To_Class ("AFS_Spec", MOM.Attr._A_Object_)
class Field_Object (_Field_) :
    """Specification of a object-holding field of a AFS form."""

    Type     = Element.Entity

    def __call__ (self, E_Type, spec, seen) :
        attr = getattr (E_Type, self.name)
        if attr.ui_allow_new :
            return self.Type (** self.kw)
        else :
            print NotImplementedError ("Object-Completer field"), E_Type, attr
            return Element.Field (** self.kw)
    # end def __call__

# end class Field_Object

### XXX sub-structured fields (e.g., date as year/month/date combination)

class  _Field_Group_ (_Base_) :
    """Specification of a Field_Group of a AFS form."""

    defaults = dict (collapsed = True)
    Type     = Element.Fieldset

    def __call__ (self, E_Type, spec, seen) :
        children = tuple \
            (f (E_Type, spec, seen) for f in self.fields (E_Type, spec, seen))
        if children :
            return self.Type (children = children, ** self.kw)
    # end def __call__

    def fields (self, E_Type, spec, seen) :
        attr_spec = spec.attr_spec
        for attr in self.attrs (E_Type, spec, seen) :
            name = attr.name
            if name not in seen :
                seen.add (name)
                kw = dict \
                    ( name        = name
                    , description = attr.description
                    , ui_name     = attr.ui_name
                    , ** attr_spec [name]
                    )
                if attr.explanation :
                    kw ["explanation"] = attr.explanation
                yield attr.AFS_Spec (** kw)
    # end def fields

# end class  _Field_Group_

class Field_Group (_Field_Group_) :
    """Specification of a Field_Group for a specified set of attributes."""

    def __init__ (self, * names, ** kw) :
        self._names = names
        self.__super.__init__ (** kw)
    # end def __init__

    def attrs (self, E_Type, spec, seen) :
        for name in self._names :
            yield getattr (E_Type, name)
    # end def attrs

# end class Field_Group

class Field_Group_K (_Field_Group_) :
    """Specification of a Field_Group for a specific attribute kind of a AFS
       form for an essential MOM entity.
    """

    def __init__ (self, ** kw) :
        self.pop_to_self      (kw, "kind")
        self.__super.__init__ (name = self.kind, ** kw)
    # end def __init__

    def attrs (self, E_Type, spec, seen) :
        return getattr (E_Type, self.kind, ())
    # end def attrs

# end class Field_Group_K

class Field_Group_Necessary (Field_Group_K) :
    """Specification of a field group for necessary  attributes."""

    kind      = "necessary"
    rank      = -200

# end class Field_Group_Necessary

class Field_Group_Optional (Field_Group_K) :
    """Specification of a field group for optional attributes."""

    kind      = "optional"
    rank      = -100

# end class Field_Group_Optional

class Field_Group_Primary (Field_Group_K) :
    """Specification of a field group for primary attributes."""

    defaults  = dict (collapsed = False)
    kind      = "primary"
    rank      = -400

# end class Field_Group_Primary

class Field_Group_Required (Field_Group_K) :
    """Specification of a field group for required attributes."""

    kind      = "required"
    rank      = -300

# end class Field_Group_Required

class Entity (_Entity_Mixin_) :
    """Specification of a AFS form for an essential MOM entity."""

    Type      = Element.Entity

    def __init__ (self, * elements, ** kw) :
        self._elems    = elements
        kw.setdefault ("include_kind_groups", not elements)
        self.__super.__init__ (** kw)
    # end def __init__

# end class Entity

class Entity_Link (Entity) :
    """Specification of a AFS sub-form for a type of link(s) of an essential MOM entity."""

    Type = Element.Entity_Link

    def __init__ (self, name, * elements, ** kw) :
        self.name = name
        self.__super.__init__ (* elements, ** kw)
    # end def __init__

    def __call__ (self, E_Type, spec = None, seen = ()) :
        assoc = self._get_assoc (self.name, E_Type)
        try :
            role_name = self.role_name
        except AttributeError :
            role_name = self.kw ["role_name"] = \
                assoc.Roles [assoc.role_map [E_Type.type_name]].name
        role = getattr (assoc, role_name)
        seen = set ([role.generic_role_name])
        result = self.__super.__call__ (assoc, self, seen)
        if role.max_links != 1 :
            result = Element.Entity_List (proto = result)
        return result
    # end def __call__

    def _get_assoc (self, name, E_Type) :
        cached_role = getattr (E_Type, name, None)
        if cached_role is not None :
            name = cached_role.assoc
        return E_Type.app_type.etypes [name]
    # end def _get_assoc

# end class Entity_Link

if __name__ != "__main__" :
    GTW.AFS.MOM._Export_Module ()
### __END__ GTW.AFS.MOM.Spec
