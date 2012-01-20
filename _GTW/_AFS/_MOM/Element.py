# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011-2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.AFS.MOM.Element
#
# Purpose
#    Model MOM-specific elements of AJAX-enhanced forms
#
# Revision Dates
#    23-Feb-2011 (CT) Creation
#    24-Feb-2011 (CT) Creation continued..
#    25-Feb-2011 (CT) Creation continued...
#    27-Feb-2011 (CT) Creation continued....
#     1-Mar-2011 (CT) Creation continued.....
#     2-Mar-2011 (CT) Creation continued...... (`_value_sig_t`)
#     8-Mar-2011 (CT) `Entity._value` changed to always set `init`
#     8-Mar-2011 (CT) `_value` simplified
#     8-Mar-2011 (CT) `apply` added
#     9-Mar-2011 (CT) `Field_Role_Hidden` added
#    21-Mar-2011 (CT) `Field._instance_kw` added
#    29-Mar-2011 (CT) `Field._instance_kw` changed to set `readonly`, if
#                     necessary
#    30-Mar-2011 (CT) `display` and `_display` added
#     1-Apr-2011 (CT) `Entity_Link.__call__` changed to allow `link` to be
#                     passed in
#     5-Apr-2011 (CT) `Entity_Link.__call__` corrected
#    13-Apr-2011 (CT) `Field_Entity.__call__` changed to allow call for
#                     instance, support `allow_new` and `collapsed`
#    25-May-2011 (CT) `Element._changed_children` changed to consider `c.entity`
#    25-May-2011 (CT) `Field_Role_Hidden.apply` added,
#                     empty `._update_sid` removed
#     8-Jun-2011 (CT) `_create_instance` factored to use `instance_or_new`
#                     for all but implicit links
#    21-Jun-2011 (MG) `from/as_pickle_cargo` added
#    18-Jul-2011 (CT) Use `query_1` instead of home-grown code
#     9-Sep-2011 (CT) Use `.E_Type` instead of `._etype`
#    16-Sep-2011 (CT) Use `AE.` instead of `import *`
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#     7-Oct-2011 (CT) `Entity.apply` changed to look at `old_pid`
#     8-Nov-2011 (CT) Change `_changed_children` and `Field.applyf` to not
#                     check for changes
#     8-Nov-2011 (CT) Change `_apply_create` to check `value.conflicts`
#     8-Nov-2011 (CT) Change `Field_Composite.applyf` to update `entity`
#                     before up-chaining
#     8-Nov-2011 (CT) Change `Field_Entity.__call__` to honor `attr.raw_default`
#     8-Nov-2011 (CT) Change `_create_instance` to pass `exc.any_required_empty`
#     8-Nov-2011 (CT) Change `Field._value` to check `entity` vs. `allow_new`
#    18-Nov-2011 (CT) Apply `str` to `.type_name` (in `_value_sig_t`)
#     2-Dec-2011 (CT) Change `Entity._value_cp` to include `uid`
#    20-Jan-2012 (CT) s/_check_sid/check_sid/ and let client call it
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW        import GTW
from   _MOM        import MOM
from   _TFL        import TFL

from   _GTW._AFS   import Element as AE

import _GTW._AFS._MOM
import _MOM.Error

class _MOM_Element_ (AE._Element_) :

    _real_name    = "Element"

    def _changed_children (self, value, scope, entity, ** kw) :
        result = {}
        for c in value.children :
            v = None
            if c.entity :
                v = c.entity
            else :
                v = c.elem.applyf (c, scope, entity, ** kw)
                value.conflicts += c.conflicts
            if v is not None :
                result [c.elem.name] = v
        return result
    # end def _changed_children

Element = _MOM_Element_ # end class

class _MOM_Entity_ (_MOM_Element_, AE.Entity) :
    """Model a MOM-specific sub-form for a single entity."""

    _real_name = "Entity"
    init       = {}

    def apply (self, value, scope, ** kw) :
        pid = value.edit.get ("pid")
        if pid is not None :
            result = self._apply_change (pid, value, scope, ** kw)
        else :
            old_pid = value.init.get ("pid")
            if old_pid is None :
                result = self._apply_create (value, scope, ** kw)
            else :
                ### Value of entity field is reset to `None`
                result = None
        return result
    # end def apply

    def check_sid (self, value, ** kw) :
        v_sid = self.form_hash (value, ** kw)
        if v_sid != value.sid :
            raise GTW.AFS.Error.Corrupted ()
    # end def check_sid

    def _apply_change (self, pid, value, scope, ** kw) :
        entity = scope.pid_query (pid)
        akw    = self._changed_children (value, scope, entity, ** kw)
        if akw and not value.conflicts :
            ### XXX error handling
            entity.set_raw (** akw)
        return entity
    # end def _apply_change

    def _apply_create (self, value, scope, ** kw) :
        akw = self._changed_children (value, scope, None, ** kw)
        if akw and not value.conflicts :
            ### XXX error handling
            ETM = scope [self.type_name]
            return self._create_instance (ETM, akw)
    # end def _apply_create

    def _create_instance (self, ETM, akw) :
        try :
            return ETM.instance_or_new (raw = 1, ** akw)
        except MOM.Error.Invariant_Errors as exc :
            if not exc.any_required_empty :
                raise
    # end def _create_instance

    def _instance_kw (self, ETM, entity, ** kw) :
        result = self.__super._instance_kw (ETM, entity, ** kw)
        if entity is not None :
            result.update \
                ( _display = entity.ui_display
                , entity   = entity
                )
        return result
    # end def _instance_kw

    def _value (self, ETM, entity, ** kw) :
        assert ETM.type_name == self.type_name, \
             "%s <-> %s" % (ETM.type_name, self.type_name)
        if entity is not None :
            assert isinstance (entity, ETM.E_Type), \
                "%s <-> %r" % (ETM, entity)
        result = self.__super._value  (ETM, entity, ** kw)
        key    = "edit" if result.get ("prefilled") else "init"
        result [key] = self._value_cp (ETM, entity, ** kw)
        return result
    # end def _value

    def _value_cp (self, ETM, entity, ** kw) :
        return {} if kw.get ("copy", False) else dict \
            ( cid = getattr (entity, "last_cid",   None)
            , pid = getattr (entity, "pid",        None)
            , uid = getattr (entity, "ui_display", None)
            )
    # end def _value_cp

    def _value_sig_t (self, instance) :
        init = instance.init
        return tuple \
            ( (k, init.get (k)) for k in ("pid", "cid")
            ) + (str (instance.id), str (self.type_name))
    # end def _value_sig_t

Entity = _MOM_Entity_ # end class

class _MOM_Entity_Link_ (AE.Entity_Link, Entity) :
    """Model a MOM-specific sub-form for a link to entity in containing
       sub-form.
    """

    _real_name = "Entity_Link"

    def __call__ (self, ETM, entity, ** kw) :
        assoc = ETM.home_scope [self.type_name]
        link  = entity
        if entity is not None :
            if not isinstance (entity, assoc.E_Type) :
                n, link = assoc.query_1 (** { self.role_name : entity })
        return self.__super.__call__ (assoc, link, role_entity = entity, ** kw)
    # end def __call__

    def instance_call (self, assoc, link, ** kw) :
        kw.pop ("role_entity", None)
        return self.__super.__call__ \
            ( assoc, link
            , role_entity = getattr (link, self.role_name, None)
            , ** kw
            )
    # end def instance_call

    def _create_instance (self, ETM, akw) :
        return ETM (raw = 1, ** akw)
    # end def _create_instance

Entity_Link = _MOM_Entity_Link_ # end class

class _MOM_Entity_List_  (AE.Entity_List) :
    """Model a MOM-specific sub-form for a list of entities."""

    _real_name = "Entity_List"

    def _call_iter (self, ETM, entity, ** kw) :
        if entity is not None :
            cs     = []
            proto  = self.proto
            assoc  = ETM.home_scope [proto.type_name]
            for i, link in enumerate \
                    (assoc.query_s (** { proto.role_name : entity })) :
                cs.append ((link, self.new_child (i, {})))
            for link, c in cs :
                yield c.instance_call (assoc, link, ** kw)
    # end def _call_iter

Entity_List = _MOM_Entity_List_ # end class

class _MOM_Field_ (AE.Field) :
    """Model a MOM-specific field of an AJAX-enhanced form."""

    _real_name = "Field"

    def applyf (self, value, scope, entity, ** kw) :
        result = None
        if entity is not None :
            dbv = entity.raw_attr (self.name)
            if value.init != dbv:
                value.conflicts += 1
                value.asyn       = result = dbv
            else :
                result = value.edit
        else :
            result = value.edit
        return result
    # end def applyf

    def _instance_kw (self, ETM, entity, ** kw) :
        result = self.__super._instance_kw (ETM, entity, ** kw)
        attr   = ETM.attributes [self.name]
        value  = result ["value"]
        init   = value.get ("init", "")
        result ["cooked"]   = attr.from_string (init) if init else None
        result ["_display"] = init
        if not kw.get ("copy", False) :
            if (not attr.is_changeable) and init != attr.raw_default :
                result ["readonly"] = True
        for k in "max_length", "max_value", "min_value" :
            v = getattr (attr, k, None)
            if v is not None :
                result [k] = v
        return result
    # end def _instance_kw

    def _value (self, ETM, entity, ** kw) :
        result = self.__super._value (ETM, entity, ** kw)
        attr   = ETM.attributes [self.name]
        akw    = kw.get (self.name, {})
        if entity is None and not kw.get ("allow_new") :
            ### No entity, no `allow_new`:
            ### * only existing entities can be selected
            ### * default values interfere with auto-completion
            ### * don't put them in `result`
            return result
        key    = \
            (    "edit"
            if   result.get ("prefilled") or kw.get ("copy", False)
            else "init"
            )
        if "init" in akw :
            result [key] = akw ["init"]
            key = "init"
        init = attr.get_raw (entity)
        if init :
            result [key] = init
        return result
    # end def _value

Field = _MOM_Field_ # end class

class _MOM_Field_Composite_ (_MOM_Element_, AE.Field_Composite) :
    """Model a MOM-specific composite field of a AJAX-enhanced form."""

    _real_name = "Field_Composite"

    def applyf (self, value, scope, entity, ** kw) :
        if entity is not None :
            entity = getattr (entity, self.name)
        return self._changed_children (value, scope, entity, ** kw)
    # end def applyf

    def _call_iter (self, ETM, entity, ** kw) :
        attr     = ETM.E_Type.attributes [self.name]
        c_type   = attr.P_Type
        c_entity = getattr (entity, self.name, None)
        for c in self.children :
            yield c (c_type, c_entity, ** dict (kw, ** kw.get (self.name, {})))
    # end def _call_iter

Field_Composite = _MOM_Field_Composite_ # end class

class _MOM_Field_Entity_ (Entity, AE.Field_Entity) :
    """Model a MOM-specific entity-holding field of an AJAX-enhanced form."""

    _real_name = "Field_Entity"

    def __call__ (self, ETM, entity, ** kw) :
        if self.type_name == ETM.type_name :
            result = self.__super.__call__ (ETM, entity, ** kw)
        else :
            attr     = ETM.E_Type.attributes [self.name]
            a_etm    = attr.etype_manager (ETM)
            a_entity = getattr (entity, self.name, None)
            if a_entity is None and attr.raw_default :
                a_entity = a_etm.instance (attr.raw_default, raw = True)
            a_kw     = dict (kw, ** kw.get (self.name, {}))
            kw       = dict \
                ( a_kw
                , allow_new = attr.ui_allow_new and a_kw.get ("allow_new", True)
                , collapsed =
                    (   a_kw.get    ("collapsed", True)
                    and self.kw.get ("collapsed", True)
                    and not (a_entity is None and attr.is_required)
                    )
                , outer_entity = entity
                , role_entity  = None
                )
            result = self.__super.__call__ (a_etm, a_entity, ** kw)
        return result
    # end def __call__

    def applyf (self, value, scope, entity, ** kw) :
        return value.entity
    # end def applyf

Field_Entity = _MOM_Field_Entity_ # end class

class Field_Role_Hidden (Field_Entity) :
    """Hidden field description a hidden role of an Entity_Link."""

    def __init__ (self, ** kw) :
        kw.pop ("completer", None)
        self.__super.__init__ (** kw)
    # end def __init__

    def apply (self, value, scope, ** kw) :
        pid = value.edit.get ("pid")
        if pid is not None :
            return scope.pid_query (pid)
    # end def apply

    def applyf (self, value, scope, entity, ** kw) :
        pid = value.edit.get ("pid")
        if pid is not None :
            result = scope.pid_query (pid)
        else :
            result = getattr (entity, "self.name", None)
        return result
    # end def applyf

    def display (self, instance) :
        return None
    # end def display

# end class Field_Role_Hidden

Fieldset = AE.Fieldset

class _MOM_Form_ (AE.Form) :
    """Model a MOM-specific AJAX-enhanced form."""

    _real_name = "Form"

    cache_rank = -500

    def _call_iter (self, * args, ** kw) :
        if len (self.children) == 1 and len (args) <= 2 :
            c = self.children [0]
            yield c (* args, ** kw)
        else :
            assert len (args) == len (self.children), repr (self)
            assert not kw, repr (self)
            for a, c in zip (args, self.children) :
                yield c (a.ETM, a.entity, ** a.kw)
    # end def _call_iter

    @classmethod
    def as_pickle_cargo (cls, nav_root) :
        if not cls.Table :
            ### mustn't do this more than once
            for T in nav_root.App_Type._T_Extension :
                if T.GTW.afs_id is not None and T.GTW.afs_spec is not None :
                    Form (T.GTW.afs_id, children = [T.GTW.afs_spec (T)])
        return dict (AFS_Form_Table = cls.Table)
    # end def as_pickle_cargo

    @classmethod
    def from_pickle_cargo (cls, nav_root, cargo) :
        """Update `Table` with `table`."""
        table = cargo.get ("AFS_Form_Table", {})
        table.update      (cls.Table)
        ### We want to set `Table` for `GTW.AFS.Element.Form`, not for a
        ### possible descedent class
        GTW.AFS.Element.Form.Table = table
    # end def from_pickle_cargo

Form = _MOM_Form_ # end class

Group = AE.Group

if __name__ != "__main__" :
    GTW.AFS.MOM._Export_Module ()
### __END__ GTW.AFS.MOM.Element
