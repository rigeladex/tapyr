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
#    ««revision-date»»···
#--

from   _GTW._AFS.Element import *
import _GTW._AFS._MOM

class _MOM_Entity_ (Entity) :
    """Model a MOM-specific sub-form for a single entity."""

    _real_name = "Entity"
    init       = {}

    def apply (self, value, scope, ** kw) :
        self._check_sid (value, ** kw)
        pid = value.edit.get ("pid")
        if pid is not None :
            result = self._apply_change (pid, value, scope, ** kw)
        else :
            result = self._apply_create (value, scope, ** kw)
        return result
    # end def apply

    def _apply_change (self, pid, value, scope, ** kw) :
        entity = scope.pid_query (pid)
        akw    = self._changed_children (value, entity, ** kw)
        if akw and not value.conflicts :
            ### XXX error handling
            entity.set_raw (** akw)
        return entity
    # end def _apply_change

    def _apply_create (self, value, scope, ** kw) :
        akw = self._changed_children (value, None, ** kw)
        if akw :
            ETM = scope [self.type_name]
            ### XXX error handling
            return ETM (raw = 1, ** akw)
    # end def _apply_create

    def _changed_children (self, value, entity, ** kw) :
        if value.changes :
            result = {}
            for c in value.children :
                v = c.elem.applyf (c, entity, ** kw)
                value.conflicts += c.conflicts
                if v is not None :
                    result [c.elem.name] = v
            return result
    # end def _changed_children

    def _check_sid (self, value, ** kw) :
        v_sid = self.form_hash (value, ** kw)
        if v_sid != value.sid :
            raise GTW.AFS.Error.Corrupted ()
    # end def _check_sid

    def _instance_kw (self, ETM, entity, ** kw) :
        result = self.__super._instance_kw (ETM, entity, ** kw)
        if entity is not None :
            result ["_display"] = entity.ui_display
        return result
    # end def _instance_kw

    def _value (self, ETM, entity, ** kw) :
        assert ETM.type_name == self.type_name, \
             "%s <-> %s" % (ETM.type_name, self.type_name)
        if entity is not None :
            assert isinstance (entity, ETM._etype), \
                "%s <-> %r" % (ETM, entity)
        result = self.__super._value (ETM, entity, ** kw)
        result.update \
            ( init = {} if kw.get ("copy", False) else dict
                ( cid = getattr (entity, "last_cid", None)
                , pid = getattr (entity, "pid",      None)
                )
            )
        return result
    # end def _value

    def _value_sig_t (self, instance) :
        init = instance.init
        return tuple \
            ( (k, init.get (k)) for k in ("pid", "cid")
            ) + (str (instance.id), self.type_name)
    # end def _value_sig_t

Entity = _MOM_Entity_ # end class

class _MOM_Entity_Link_ (Entity_Link, Entity) :
    """Model a MOM-specific sub-form for a link to entity in containing
       sub-form.
    """

    _real_name = "Entity_Link"

    def __call__ (self, ETM, entity, ** kw) :
        assoc = ETM.home_scope [self.type_name]
        link  = entity
        if entity is not None :
            if not isinstance (entity, assoc) :
                try :
                    link = assoc.query (** { self.role_name : entity }).one ()
                except IndexError :
                    pass
        return self.__super.__call__ (assoc, link, ** kw)
    # end def __call__

    def instance_call (self, assoc, link, ** kw) :
        return self.__super.__call__ (assoc, link, ** kw)
    # end def instance_call

Entity_Link = _MOM_Entity_Link_ # end class

class _MOM_Entity_List_  (Entity_List) :
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

class _MOM_Field_ (Field) :
    """Model a MOM-specific field of an AJAX-enhanced form."""

    _real_name = "Field"

    def applyf (self, value, entity, ** kw) :
        if entity is not None :
            dbv = entity.raw_attr (self.name)
            if value.init != dbv:
                value.conflicts += 1
                value.asyn       = dbv
                return dbv
            if value.init != value.edit :
                return value.edit
        else :
            return value.edit
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
        if "init" in akw :
            init = akw ["init"]
        else :
            init = attr.get_raw (entity)
        if init :
            result.update (init = init)
        return result
    # end def _value

Field = _MOM_Field_ # end class

class _MOM_Field_Composite_ (Field_Composite) :
    """Model a MOM-specific composite field of a AJAX-enhanced form."""

    _real_name = "Field_Composite"

    def applyf (self, value, entity, ** kw) :
        return self._changed_children (value, entity, ** kw)
    # end def applyf

    def _call_iter (self, ETM, entity, ** kw) :
        attr     = ETM._etype.attributes [self.name]
        c_type   = attr.C_Type
        c_entity = getattr (entity, self.name, None)
        for c in self.children :
            yield c (c_type, c_entity, ** dict (kw, ** kw.get (self.name, {})))
    # end def _call_iter

Field_Composite = _MOM_Field_Composite_ # end class

class _MOM_Field_Entity_ (Entity, Field_Entity) :
    """Model a MOM-specific entity-holding field of an AJAX-enhanced form."""

    _real_name = "Field_Entity"

    def __call__ (self, ETM, entity, ** kw) :
        attr     = ETM._etype.attributes [self.name]
        a_type   = attr.etype_manager (ETM)
        a_entity = getattr (entity, self.name, None)
        a_kw     = dict (kw, ** kw.get (self.name, {}))
        kw       = dict \
            ( a_kw
            , allow_new = attr.ui_allow_new and a_kw.get ("allow_new", True)
            # XXX completer
            )
        return self.__super.__call__ (a_type, a_entity, ** kw)
    # end def __call__

    def applyf (self, value, entity, ** kw) :
        return value.entity
    # end def applyf

Field_Entity = _MOM_Field_Entity_ # end class

class Field_Role_Hidden (Field_Entity) :
    """Hidden field description a hidden role of an Entity_Link."""

    def display (self, instance) :
        return None
    # end def display

    def _update_sid (self, result, ** kw) :
        pass
    # end def _update_sid

    def _value (self, ETM, entity, ** kw) :
        result = self.__super._value (ETM, entity, ** kw)
        if kw.get ("copy", False) :
            result.pop ("init", None)
        return result
    # end def _value

# end class Field_Role_Hidden

class _MOM_Form_ (Form) :
    """Model a MOM-specific AJAX-enhanced form."""

    _real_name = "Form"

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

Form = _MOM_Form_ # end class

if __name__ != "__main__" :
    GTW.AFS.MOM._Export_Module ()
### __END__ GTW.AFS.MOM.Element
