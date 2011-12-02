# -*- coding: iso-8859-15 -*-
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
#    24-Feb-2011 (CT) s/Field_Object/Field_Entity/,
#                     `Field_Entity` dervied from `_Entity_Mixin_`
#     8-Mar-2011 (CT) `_Field_Group_.fields` changed to put `label` instead
#                     of `ui_name` into `kw` for `attr.AFS_Spec`
#     9-Mar-2011 (CT) `** kw` added to `__call__`
#     9-Mar-2011 (CT) `_Entity_Mixin_.__call__` changed to set `name` to
#                     `E_Type.ui_name` instead of `.type_name`
#     9-Mar-2011 (CT) `Field_Role_Hidden` and `_Hidden_Role_` added,
#                     `Entity_Link` changed to support `_Hidden_Role_`
#    14-Mar-2011 (CT) `_Field_._field_kw` factored from `_Field_Group_.fields`
#                     (and changed to add `kind` and `required`)
#    14-Mar-2011 (CT) `_Entity_Mixin_.__init__` changed to honor `include_links`
#    15-Mar-2011 (CT) `setup_defaults` added
#    18-Mar-2011 (CT) `_Field_._field_kw`: `css_class`, `choices`, and
#                     `input_widget` added
#    28-Mar-2011 (CT) `Entity_Link._get_role_name` factored, improved
#    29-Mar-2011 (CT) `_Field_._field_kw` changed to set `changeable`
#    30-Mar-2011 (CT) `include_elems` added
#    30-Mar-2011 (CT) `Entity_Link.__call__` changed to set `name` and `ui_name`
#    10-Jun-2011 (MG) `_Entity_Mixin_.__init__` `entity_links_group` and
#                     `Entity_Links_Group` added
#     6-Jul-2011 (CT) Use `MOM.Attr.Selector` instead of homegrown code
#     6-Jul-2011 (CT) `f_completer` added
#    17-Jul-2011 (CT) s/f_completer/completer/
#    15-Sep-2011 (CT) Move instantiation of `attr.completer` to `MOM.Attr.Spec`
#    20-Sep-2011 (CT) `_Field_._field_kw` changed to use `attr.completer` as is
#                     (instead of `as_json_cargo`)
#    22-Sep-2011 (CT) s/A_Entity/A_Id_Entity/
#     4-Nov-2011 (CT) Set `css_class` for attribute kinds
#     4-Nov-2011 (CT) Improve handling of `css_class`
#     4-Nov-2011 (CT) Change `_Entity_Mixin_.__call__` to add `description`
#     4-Nov-2011 (CT) Add support for `_A_Named_Object_`
#     7-Nov-2011 (CT) Change `Entity_Link._get_role_name` to use
#                     `other_role_name` to find `result`
#     9-Nov-2011 (CT) Add `css_align` for attribute types
#     2-Dec-2011 (CT) Add `MAT._A_Id_Entity_.input_widget`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _MOM                     import MOM
from   _TFL                     import TFL

from   _GTW._AFS._MOM           import Element
from   _GTW._Form.Widget_Spec   import Widget_Spec as WS
import _GTW._Form._MOM.Field ### XXX remove after migration of `css_class`

import _MOM._Attr.Selector
import _MOM._Attr.Type

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Decorator
import _TFL.multimap

MAT                                  = MOM.Attr
MAT.A_Attr_Type.input_widget         = WS ("html/AFS/input.jnj,  string")
MAT.A_Boolean.input_widget           = WS ("html/AFS/input.jnj,  boolean")
MAT.A_Date.input_widget              = WS ("html/AFS/input.jnj,  date")
MAT.A_Date_Time.input_widget         = WS ("html/AFS/input.jnj,  datetime")
MAT.A_Email.input_widget             = WS ("html/AFS/input.jnj,  email")
MAT.A_Text.input_widget              = WS ("html/AFS/input.jnj,  text")
MAT._A_Id_Entity_.input_widget       = WS ("html/AFS/input.jnj,  id_entity")
MAT._A_Named_Object_.input_widget    = WS ("html/AFS/input.jnj,  named_object")
MAT._A_Named_Value_.input_widget     = WS ("html/AFS/input.jnj,  named_value")
MAT._A_Number_.input_widget          = WS ("html/AFS/input.jnj,  number")

MAT.Kind.css_class                   = ""
MAT.A_Attr_Type.css_class            = ""

MAT.A_Attr_Type.css_align            = ""
MAT._A_Number_.css_align             = "right"
MAT.A_Date.css_align                 = "right"
MAT.A_Numeric_String.css_align       = "right"
MAT.A_Time.css_align                 = "right"

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
    _elems              = ()

    def __init__ (self, ** kw) :
        self.attr_spec = TFL.mm_dict \
            (self.attr_spec, ** kw.pop ("attr_spec", {}))
        include_elems = kw.pop ("include_elems", ())
        include_links = tuple \
            (   (Entity_Link (l) if isinstance (l, basestring) else l)
            for l in kw.pop ("include_links", ())
            )
        etl_group = kw.pop ("entity_links_group", None)
        if  etl_group :
            include_links = \
                (getattr (GTW.AFS.MOM.Spec, etl_group) (include_links), )
        for include in include_elems, include_links :
            self._elems += include
        if "include_kind_groups" in kw :
            self.pop_to_self (kw, "include_kind_groups")
        else :
            self.include_kind_groups = not any \
                (   not isinstance (e, (Entity_Link, Entity_Links_Group))
                for e in self._elems
                )
        self.__super.__init__ (** kw)
    # end def __init__

    def __call__ (self, E_Type, spec = None, seen = None, ** kw) :
        if seen is None :
            seen = set ()
        ekw      = dict (E_Type.GTW.afs_kw or {}, ** self.kw)
        elems    = sorted (self.elements (E_Type), key = TFL.Getter.rank)
        children = (e (E_Type, self, seen) for e in elems)
        ekw.update     (kw)
        ekw.setdefault ("name",        E_Type.ui_name)
        ekw.setdefault ("ui_name",     E_Type.ui_name)
        ekw.setdefault ("description", E_Type.__doc__)
        return self.Type \
            ( children  = tuple (c for c in children if c is not None)
            , type_name = E_Type.type_name
            , ** ekw
            )
    # end def __call__

    def default_elements (self, E_Type) :
        return default_elements
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

    def _field_kw (self, attr, E_Type, ** kw) :
        at      = attr.attr
        ui_name = attr.ui_name or attr.name
        result  = dict \
            ( changeable  = attr.is_changeable
            , description = attr.description or ""
            , kind        = attr.kind
            , label       = ui_name
            , required    = attr.is_required
            , ui_name     = ui_name
            )
        if isinstance (at, MOM.Attr._A_Named_Object_) :
            result ["choices"] = sorted \
                ( ((k, str (v)) for k, v in at.Table.iteritems ())
                , key = TFL.Getter [1]
                )
        elif isinstance (at, MOM.Attr._A_Named_Value_) :
            result ["choices"] = sorted (at.Table)
        cssc = " ".join (c for c in self._css_classes (attr) if c)
        if cssc :
            result ["css_class"] = cssc
        if attr.input_widget :
            result ["input_widget"] = attr.input_widget
        if attr.explanation :
            result ["explanation"] = attr.explanation
        if attr.completer :
            result ["completer"] = attr.completer
        result.update (self.kw)
        result.update (kw)
        return result
    # end def _field_kw

    def _css_classes (self, attr) :
        return (attr.css_class, attr.attr.css_class, )
    # end def _css_classes

# end class _Field_

class _Field_Entity_Mixin_ (_Entity_Mixin_, _Field_) :

    def __call__ (self, E_Type, spec, seen, ** kw) :
        attr = getattr (E_Type, self.name)
        return self.__super.__call__ \
            (attr.P_Type, self, set (), ** self._field_kw (attr, E_Type, ** kw))
    # end def __call__

# end class _Field_Entity_Mixin_

class Entity (_Entity_Mixin_) :
    """Specification of a AFS form for an essential MOM entity."""

    Type      = Element.Entity

    def __init__ (self, * elements, ** kw) :
        self._elems = elements
        self.__super.__init__ (** kw)
    # end def __init__

# end class Entity

class Entity_Link (Entity) :
    """Specification of a AFS sub-form for a type of link(s) of an essential MOM entity."""

    defaults  = dict (collapsed = True)
    Type      = Element.Entity_Link

    def __init__ (self, name, * elements, ** kw) :
        self.name = name
        self.__super.__init__ \
            ( _Hidden_Role_ (), * elements
            , include_kind_groups = kw.pop ("include_kind_groups", True)
            , ** kw
            )
    # end def __init__

    def __call__ (self, E_Type, spec = None, seen = (), ** kw) :
        assoc      = self._get_assoc     (self.name, E_Type)
        role_name  = self._get_role_name (assoc,     E_Type)
        role       = getattr (assoc, role_name)
        r_name     = role.generic_role_name
        seen       = set ([r_name])
        with self.LET (hidden_role_name = r_name) :
            result = self.__super.__call__ (assoc, self, seen, ** kw)
        if role.max_links != 1 :
            elkw = dict (kw)
            elkw.setdefault ("name",      result.ui_name)
            elkw.setdefault ("ui_name",   result.ui_name)
            elkw.setdefault ("type_name", assoc.type_name)
            if role.max_links > 0 :
                elkw.setdefault (max_links = role.max_links)
            result = Element.Entity_List (proto = result, ** elkw)
        return result
    # end def __call__

    def _get_assoc (self, name, E_Type) :
        cached_role = getattr (E_Type, name, None)
        if cached_role is not None :
            name = cached_role.assoc
        return E_Type.app_type.etypes [name]
    # end def _get_assoc

    def _get_role_name (self, assoc, E_Type) :
        try :
            result = self.role_name
        except AttributeError :
            r_map = assoc.role_map
            try :
               result = assoc.Roles [r_map [E_Type.type_name]].name
            except KeyError :
                if len (assoc.Roles) == 1 :
                    result = assoc.Roles [0].name
                else :
                    n = self.name
                    if n in r_map :
                        role = assoc.Roles [r_map [n]]
                    elif n.endswith ("s") and n [:-1] in r_map :
                        role = assoc.Roles [r_map [n [:-1]]]
                    else :
                        raise TypeError ("No role-name defined for %s" % n)
                    if role.generic_role_name in assoc.other_role_name :
                        rn = assoc.other_role_name [role.generic_role_name]
                        result = assoc.Roles [r_map [rn]].name
                    else :
                        raise TypeError ("No role-name defined for %s" % n)
            self.kw ["role_name"] = result
        return result
    # end def _get_role_name

# end class Entity_Link

@TFL.Add_To_Class ("AFS_Spec", MOM.Attr.A_Attr_Type)
class Field (_Field_) :
    """Specification for a field of a AFS form."""

    Type     = Element.Field

    def __call__ (self, E_Type, spec, seen, ** kw) :
        attr = getattr (E_Type, self.name)
        return self.Type (** self._field_kw (attr, E_Type, ** kw))
    # end def __call__

    def _css_classes (self, attr) :
        return self.__super._css_classes (attr) + (attr.css_class_len, )
    # end def _css_classes

# end class Field

@TFL.Add_To_Class ("AFS_Spec", MOM.Attr._A_Composite_)
class Field_Composite (_Field_Entity_Mixin_) :
    """Specification for a composite field of a AFS form."""

    defaults  = dict (collapsed = True)
    Type      = Element.Field_Composite

    def __init__ (self, ** kw) :
        self._elems = kw.pop  ("elements", ())
        self.__super.__init__ (** kw)
        self.include_kind_groups = True
    # end def __init__

    def default_elements (self, E_Type) :
        fg = Field_Group (attr_selector = MOM.Attr.Selector.user)
        for f in fg.fields (E_Type, self, set ()) :
            yield f
    # end def default_elements

# end class Field_Composite

@TFL.Add_To_Class ("AFS_Spec", MOM.Attr._A_Id_Entity_)
class Field_Entity (_Field_Entity_Mixin_) :
    """Specification of an entity-holding field of a AFS form."""

    defaults  = dict (collapsed = True)
    Type      = Element.Field_Entity

    def default_elements (self, E_Type) :
        for f in FGP.fields (E_Type, self, set ()) :
            yield f
    # end def default_elements

# end class Field_Entity

class Field_Role_Hidden (_Field_Entity_Mixin_) :

    Type     = Element.Field_Role_Hidden

# end class Field_Role_Hidden

### XXX sub-structured fields (e.g., date as year/month/date combination)

class Field_Group (_Base_) :
    """Specification of a Field_Group of a AFS form."""

    defaults = dict (collapsed = True)
    Type     = Element.Fieldset

    def __init__ (self, attr_selector, ** kw) :
        self.attr_selector = attr_selector
        self.__super.__init__ (** kw)
    # end def __init__

    def __call__ (self, E_Type, spec, seen, ** kw) :
        children = tuple \
            (   f (E_Type, spec, seen, ** kw)
            for f in self.fields (E_Type, spec, seen)
            )
        if children :
            return self.Type (children = children, ** dict (self.kw, ** kw))
    # end def __call__

    def attrs (self, E_Type, spec, seen) :
        return iter (self.attr_selector (E_Type))
    # end def attrs

    def fields (self, E_Type, spec, seen) :
        attr_spec = spec.attr_spec
        for attr in self.attrs (E_Type, spec, seen) :
            name = attr.name
            if name not in seen :
                seen.add   (name)
                akw = dict (attr_spec [name], name = name)
                yield attr.AFS_Spec (** akw)
    # end def fields

# end class Field_Group

class Field_Group_K (Field_Group) :
    """Specification of a Field_Group for a specific attribute kind of a AFS
       form for an essential MOM entity.
    """

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "kind")
        self.__super.__init__ \
            (getattr (MOM.Attr.Selector, self.kind), name = self.kind, ** kw)
    # end def __init__

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

FGP = Field_Group_Primary   ()
FGR = Field_Group_Required  ()
FGN = Field_Group_Necessary ()
FGO = Field_Group_Optional  ()

default_elements = (FGP, FGR, FGN, FGO)

class Entity_Links_Group (_Base_) :
    """A container holding all entity links for an entity."""

    Type = Element.Group

    def __init__ (self, entity_links) :
        self.__super.__init__ ()
        self.entity_links = entity_links
    # end def __init__

    def __call__ (self, E_Type, spec, seen, ** kw) :
        return self.Type \
            ( children =
                (etl (E_Type, spec, seen, ** kw) for etl in self.entity_links)
            )
    # end def __call__

# end class Entity_Links_Group

class _Hidden_Role_ (_Base_) :
    """Specification of a hidden field describing the hidden role of an
       Entity_Link.
    """

    rank = - (1 << 16)

    def __call__ (self, E_Type, spec, seen, ** kw) :
        fe = Field_Role_Hidden \
            ( allow_new           = False
            , hidden              = True
            , include_kind_groups = False
            , name                = spec.hidden_role_name
            )
        result = fe (E_Type, spec, seen, ** kw)
        return result
    # end def __call__

# end class _Hidden_Role_

def setup_defaults (default_spec = None, id_prefix = "AF") :
    import _MOM.Entity
    if default_spec is None :
        default_spec = Entity ()
    for T in MOM.Entity._S_Extension [::-1] :
        if T.GTW.afs_id is None :
            T.GTW.afs_id   = "%s%s" % (id_prefix, T.i_rank)
        if T.GTW.afs_kw is None :
            T.GTW.afs_kw   = {}
        if T.GTW.afs_spec is None and not T.is_partial :
            T.GTW.afs_spec = default_spec
# end def setup_defaults

if __name__ != "__main__" :
    GTW.AFS.MOM._Export_Module ()
### __END__ GTW.AFS.MOM.Spec
