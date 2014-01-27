# -*- coding: utf-8 -*-
# Copyright (C) 2011-2014 Mag. Christian Tanzer All rights reserved
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
#    24-Jan-2012 (CT) Redefine `Field.__call__`
#                     and `Field_Composite.__call__` to pass `f_kw` to `__super`
#    24-Jan-2012 (CT) Change `Field_Entity.__call__` to pass `f_kw` to `__super`
#    25-Jan-2012 (CT) Redefine `Field_Entity._call_iter` to consider `prefilled`
#    25-Jan-2012 (CT) Use `_child_kw`
#    26-Jan-2012 (CT) Factor `_MOM_Entity_MI_`,
#                     move code from its `_value` to newly redefined `__call__`
#    26-Jan-2012 (CT) Redefine `_MOM_Entity_._instance_kw` to add `allow_new`
#    26-Jan-2012 (CT) Add support for `form_kw`; add `show_defaults`
#     1-Feb-2012 (CT) Factor `Form.as_pickle_cargo` and `.from_pickle_cargo` to
#                     separate module `Form_Cache`
#    15-Feb-2012 (CT) Redefine `Entity_List.__call__` and ._child_kw` to pass
#                     `form_kw` and extract `max_links`
#    29-Feb-2012 (CT) Set `Field_Role_Hidden.rank` to `Entity_Link.rank - 1`
#    29-Feb-2012 (CT) Redefine `Field_Role_Hidden._anchor_self`
#     1-Mar-2012 (CT) Add `results` to `apply`, `applyf`, and their callees
#     1-Mar-2012 (CT) Change `Field_Role_Hidden.apply` and `.applyf` to return
#                     `results [value.anchor_id]`, if possible
#     2-Mar-2012 (CT) Move `_value_sig_t` from `_MOM_Entity_MI_` to
#                     `_MOM_Entity_`
#     5-Mar-2012 (CT) Redefine `Field_Entity._child_kw` to extract `allow_new`
#     5-Mar-2012 (CT) Change `apply` to ignore `old_pid`
#     8-Mar-2012 (CT) Change `Field_Entity._call_iter` to consider `allow_new`
#                     (do not include `children` unless `allow_new`)
#     9-Mar-2012 (CT) Redefine `Field_Entity.apply` to consider `allow_new
#    19-Mar-2012 (CT) Change `Field_Entity.apply` to consider `prefilled`, too
#    12-Apr-2012 (CT) Change `Field_Entity.__call__` to set `readonly`
#                     according to `changeable` (and factor `_MOM_Field_MI_`)
#    12-Apr-2012 (CT) Add `on_error` to `apply` and its callees
#    13-Apr-2012 (CT) Add guards for `value.edit` to `Field.applyf`
#    13-Apr-2012 (CT) Redefine `Field_Entity._apply_create` to call newly
#                     factored `_apply_get` if there wasn't any attribute
#                     change
#    15-Apr-2012 (CT) Adapted to changes of `MOM.Error`
#    23-Apr-2012 (CT) Change `_MOM_Entity_MI_._create_instance` to use
#                     `query_s` and `ETM ()` instead of `ETM.instance_or_new`
#                     (to protect against ambiguous input)
#    22-May-2012 (CT) Remove `Form.cache_rank` (belongs to `Form_Cache`)
#    19-Aug-2012 (MG) Quick fix for type conversion for `last_cid`
#    10-Oct-2012 (CT) Add `logging.exception` to `_create_instance`
#     6-Nov-2012 (CT) Change `Element._changed_children` to check `c.changed`
#                     for previously existing `entity`
#     6-Nov-2012 (CT) Change `Field.applyf` to return `value.edit` for
#                     previously existing `entity` only if value was changed
#    11-Dec-2012 (CT) Change `Field_Composite.applyf` to not return `{}`
#    12-Dec-2012 (CT) Factor `_child_changed_p`, redefine for `Field_Composite`
#    12-Dec-2012 (CT) Change `Field.applyf` to return `value.edit` if there
#                     is no conflict (needed for composite attributes)
#    17-Dec-2012 (CT) Fix `allow_new` in `Field_Entity.__call__`
#    28-Mar-2013 (CT) Add `polymorphic_epk` to `Field_Entity.__call__`
#    11-Jun-2013 (CT) Improve message logged by `_create_instance`
#    13-Aug-2013 (CT) Change `_create_instance` to check `Required_Missing`
#    14-Jan-2014 (CT) Add `ui_description` to `Field._instance_kw`
#    27-Jan-2014 (CT) Use `ETM.query`, not `.query_s`, in `_create_instance`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW        import GTW
from   _MOM        import MOM
from   _TFL        import TFL

from   _GTW._AFS   import Element as AE

import _GTW._AFS._MOM
import _MOM.Error

import logging

class _MOM_Element_ (AE._Element_) :

    _real_name    = "Element"

    def _changed_children \
            ( self, value, results, scope, entity
            , on_error        = None
            , child_changed_p = None
            , ** kw
            ) :
        if child_changed_p is None :
            child_changed_p = self._child_changed_p
        result = {}
        for c in value.children :
            if entity is None or child_changed_p (c) :
                if c.entity :
                    v = c.entity
                else :
                    v = c.elem.applyf \
                        (c, results, scope, entity, on_error = None, ** kw)
                    value.conflicts += c.conflicts
                if v is not None :
                    result [c.elem.name] = v
        return result
    # end def _changed_children

    def _child_changed_p (self, c) :
        return (c.changes and not c.prefilled)
    # end def _child_changed_p

Element = _MOM_Element_ # end class

class _MOM_Entity_MI_ (_MOM_Element_, AE.Entity) :

    init       = {}

    def __call__ (self, ETM, entity, ** kw) :
        assert ETM.type_name == self.type_name, \
             "%s <-> %s" % (ETM.type_name, self.type_name)
        if entity is None and "init" in kw ["form_kw"] :
            entity = kw ["form_kw"] ["init"]
        if entity is not None :
            assert isinstance (entity, ETM.E_Type), \
                "%s <-> %r" % (ETM, entity)
        result = self.__super.__call__ (ETM, entity, ** kw)
        return result
    # end def __call__

    def apply (self, value, results, scope, ** kw) :
        pid = value.edit.get ("pid")
        if pid is not None :
            result = self._apply_change (pid, value, results, scope, ** kw)
        else :
            result = self._apply_create (value, results, scope, ** kw)
        return result
    # end def apply

    def check_sid (self, value, ** kw) :
        v_sid = self.form_hash (value, ** kw)
        if v_sid != value.sid :
            raise GTW.AFS.Error.Corrupted ()
    # end def check_sid

    def _apply_change (self, pid, value, results, scope, on_error = None, ** kw) :
        entity = scope.pid_query (pid)
        akw    = self._changed_children \
            (value, results, scope, entity, on_error = on_error, ** kw)
        if akw and not value.conflicts :
            ### XXX error handling
            entity.set_raw (on_error = on_error, ** akw)
        return entity
    # end def _apply_change

    def _apply_create (self, value, results, scope, on_error = None, ** kw) :
        akw = self._changed_children \
            (value, results, scope, None, on_error = on_error, ** kw)
        if akw and not value.conflicts :
            ETM = scope [self.type_name]
            return self._create_instance (ETM, akw, on_error)
    # end def _apply_create

    def _create_instance (self, ETM, akw, on_error) :
        error = None
        try :
            try :
                rqas      = ETM.raw_query_attrs (akw, akw)
                matches   = ETM.query (* rqas)
            except Exception as exc :
                logging.exception \
                    ( "Exception from "
                      "`ETM.query (* ETM.raw_query_attrs (akw, akw))` "
                      "for akw = %s"
                    % (sorted (akw.iteritems ()), )
                    )
                raise
            else :
                count     = matches.count ()
            if not count :
                result    = ETM (raw = 1, on_error = on_error, ** akw)
            else :
                error     = None
                try :
                    epks  = ETM.E_Type.epkified (** akw)
                except MOM.Error.Required_Missing as exc :
                    error = exc
                except Exception :
                    pass
                if error is None :
                    if count == 1 :
                        result = matches.one ()
                    else :
                        error = MOM.Error.Ambiguous_Epk \
                            ( ETM.E_Type, (), akw, count
                            , * matches.limit (3).all ()
                            )
                    if error is not None and on_error is not None :
                        on_error (error)
        except MOM.Error.Invariants as exc :
            if not exc.any_required_empty :
                raise
        else :
            if error is not None :
                raise error
            return result
    # end def _create_instance

    def _instance_kw (self, ETM, entity, ** kw) :
        result = self.__super._instance_kw (ETM, entity, ** kw)
        if entity is not None :
            result.update \
                ( _display = entity.ui_display
                , entity   = entity
                )
        prefilled = self.prefilled or result.get ("prefilled")
        if prefilled :
            result.update \
                ( collapsed = True
                , prefilled = prefilled
                )
        return result
    # end def _instance_kw

    def _value (self, ETM, entity, ** kw) :
        result = self.__super._value  (ETM, entity, ** kw)
        key    = "edit" if kw.get ("prefilled") else "init"
        result [key] = self._value_cp (ETM, entity, ** kw)
        return result
    # end def _value

    def _value_cp (self, ETM, entity, ** kw) :
        result = {}
        if entity and not kw.get ("copy", False) :
            result = dict \
                ( cid = int (entity.last_cid)
                , pid = int (entity.pid)
                )
        return result
    # end def _value_cp

# end class _MOM_Entity_MI_

class _MOM_Entity_ (_MOM_Entity_MI_) :
    """Model a MOM-specific sub-form for a single entity."""

    _real_name = "Entity"

    def _instance_kw (self, ETM, entity, ** kw) :
        result = self.__super._instance_kw (ETM, entity, ** kw)
        if "allow_new" not in kw :
            kw ["allow_new"] = entity is None
        return result
    # end def _instance_kw

    def _value_sig_t (self, instance) :
        init = instance.init
        return tuple \
            ( (k, init.get (k)) for k in ("pid", "cid")
            ) + (str (instance.id), str (self.type_name))
    # end def _value_sig_t

Entity = _MOM_Entity_ # end class

class _MOM_Entity_Link_ (AE.Entity_Link, _MOM_Entity_MI_) :
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
                kw.update (role_entity = entity)
            else :
                kw.update (role_entity = kw.get ("outer_entity"))
        return self.__super.__call__ (assoc, link, ** kw)
    # end def __call__

    def instance_call (self, assoc, link, ** kw) :
        kw.pop ("role_entity", None)
        return self.__super.__call__ \
            ( assoc, link
            , role_entity = getattr (link, self.role_name, None)
            , ** kw
            )
    # end def instance_call

    def _create_instance (self, ETM, akw, on_error) :
        return ETM (raw = 1, on_error = on_error, ** akw)
    # end def _create_instance

Entity_Link = _MOM_Entity_Link_ # end class

class _MOM_Entity_List_  (AE.Entity_List) :
    """Model a MOM-specific sub-form for a list of entities."""

    _real_name = "Entity_List"

    def __call__ (self, ETM, entity, ** kw) :
        f_kw = self._child_kw (kw)
        return self.__super.__call__ (ETM, entity, ** f_kw)
    # end def __call__

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

    def _child_kw (self, kw) :
        result = self.__super._child_kw (kw)
        if "max_links" in result ["form_kw"] :
            result ["max_links"] = result ["form_kw"].pop ("max_links")
        return result
    # end def _child_kw

Entity_List = _MOM_Entity_List_ # end class

class _MOM_Field_MI_ (_MOM_Element_, AE._Field_) :

    changeable = True

# end class _MOM_Field_MI_

class _MOM_Field_ (_MOM_Field_MI_, AE.Field) :
    """Model a MOM-specific field of an AJAX-enhanced form."""

    _real_name = "Field"

    def __call__ (self, ETM, entity, ** kw) :
        f_kw = dict (kw, ** kw.pop (self.name, {}))
        return self.__super.__call__ (ETM, entity, ** f_kw)
    # end def __call__

    def applyf (self, value, results, scope, entity, on_error = None, ** kw) :
        ### only called if ::
        ### * this field has changed
        ### * or entity is None
        ### * or another field of the same composite has changed and this field
        ###   is needed too
        result = None
        if entity is not None :
            dbv = entity.raw_attr (self.name)
            if value.init != dbv:
                value.conflicts += 1
                value.asyn       = result = dbv
        if result is None :
            if value.edit or value.init :
                result = value.edit
        return result
    # end def applyf

    def _instance_kw (self, ETM, entity, ** kw) :
        result = self.__super._instance_kw (ETM, entity, ** kw)
        attr   = ETM.attributes [self.name]
        value  = result ["value"]
        init   = value.get ("init", "")
        result ["cooked"]   = cooked = \
            attr.from_string (init) if init else None
        result ["_display"] = init
        if not kw.get ("copy", False) :
            if (not self.changeable) and cooked != attr.default :
                result ["readonly"] = True
        for k in "max_length", "max_value", "min_value", "ui_description" :
            v = getattr (attr, k, None)
            if v is not None :
                result [k] = v
        return result
    # end def _instance_kw

    def _value (self, ETM, entity, ** kw) :
        result = self.__super._value (ETM, entity, ** kw)
        attr   = ETM.attributes [self.name]
        if kw.get ("show_defaults", True) :
            key    = \
                (    "edit"
                if   result.get ("prefilled") or kw.get ("copy", False)
                else "init"
                )
            if "init" in kw ["form_kw"] :
                result [key] = kw ["form_kw"] ["init"]
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

    def __call__ (self, ETM, entity, ** kw) :
        f_kw = self._child_kw (kw)
        return self.__super.__call__ (ETM, entity, ** f_kw)
    # end def __call__

    def applyf (self, value, results, scope, entity, on_error = None, ** kw) :
        if entity is not None :
            entity = getattr (entity, self.name)
        result = self._changed_children \
            (value, results, scope, entity, on_error = on_error, ** kw)
        return result or None
    # end def applyf

    def _call_iter (self, ETM, entity, ** kw) :
        name     = self.name
        attr     = ETM.E_Type.attributes [name]
        c_type   = attr.P_Type
        c_entity = getattr (entity, name, None)
        for c in self.children :
            yield c (c_type, c_entity, ** kw)
    # end def _call_iter

    def _child_changed_p (self, c) :
        ### only called if at least one child changed
        ### --> must include all children, otherwise unchanged values are lost
        return True
    # end def _child_changed_p

Field_Composite = _MOM_Field_Composite_ # end class

class _MOM_Field_Entity_ (_MOM_Field_MI_, _MOM_Entity_MI_, AE.Field_Entity) :
    """Model a MOM-specific entity-holding field of an AJAX-enhanced form.

       A Field_Entity models an attribute that refers to another entity.

       If `allow_new` is false, the form doesn't allow the creation of new
       entities for this field, only existing entities can be selected. In
       this case, no change of attribute values is allowed.

       If `allow_new` is true, the form allows the creation of new entities
       for this field. In this case, changes of epk-attributes will force
       a copy of an existing object (instead of renaming it) -- otherwise the
       danger of confusion are too big.
    """

    _real_name = "Field_Entity"

    def __init__ (self, allow_new = False, ** kw) :
        self.__super.__init__ (allow_new = allow_new, ** kw)
    # end def __init__

    def __call__ (self, ETM, entity, ** kw) :
        f_kw            = self._child_kw (kw)
        allow_new       = \
            (   f_kw.get ("allow_new", True)
            and self.allow_new
            and not f_kw.get ("prefilled")
            )
        if self.type_name == ETM.type_name :
            ### this clause is taken when a part of the form is called
            ### directly like `Form [id].instantiated (...)`
            pepk = ETM.polymorphic_epk
            allow_new = allow_new and not pepk
            f_kw ["allow_new"] = allow_new
            if not (self.changeable or entity is None) :
                f_kw ["readonly"] = True
            result = self.__super.__call__ (ETM, entity, ** f_kw)
        else :
            ### this clause is taken when the whole form is processed
            ### starting with `Form (...)`
            attr         = ETM.E_Type.attributes [self.name]
            a_etm        = attr.etype_manager (ETM)
            a_entity     = getattr (entity, self.name, None)
            if a_entity is None and attr.raw_default :
                a_entity = a_etm.instance (attr.raw_default, raw = True)
            pepk         = a_etm.polymorphic_epk
            allow_new    = allow_new and not pepk
            readonly     = not (self.changeable or a_entity is None)
            f_kw         = dict \
                ( f_kw
                , allow_new      = allow_new
                , collapsed      =
                    (   f_kw.get    ("collapsed", True)
                    and self.kw.get ("collapsed", True)
                    and not (a_entity is None and attr.is_required)
                    ) or readonly or not allow_new
                , outer_entity   = entity
                , role_entity    = None
                , show_defaults  = a_entity is not None or allow_new
                    ### No entity, no `allow_new`
                    ### * only existing entities can be selected
                    ### * default values interfere with auto-completion
                    ### --> don't show them in form
                )
            if readonly :
                f_kw ["readonly"] = readonly
            if pepk :
                f_kw ["polymorphic_epk"] = pepk
            result = self.__super.__call__ (a_etm, a_entity, ** f_kw)
        return result
    # end def __call__

    def apply (self, value, results, scope, on_error = None, ** kw) :
        if getattr (value, "allow_new") and not getattr (value, "prefilled") :
            applier = self._apply_create
        else :
            applier = self._apply_get
        return applier (value, results, scope, on_error = on_error, ** kw)
    # end def apply

    def applyf (self, value, results, scope, entity, on_error = None, ** kw) :
        return value.entity
    # end def applyf

    def _apply_create (self, value, results, scope, on_error = None, ** kw) :
        result = self.__super._apply_create \
            (value, results, scope, on_error = on_error, ** kw)
        if result is None :
            result = self._apply_get \
                (value, results, scope, on_error = on_error, ** kw)
        return result
    # end def _apply_create

    def _apply_get (self, value, results, scope, on_error = None, ** kw) :
        pid = value.edit.get ("pid")
        if pid is not None :
            return scope.pid_query (pid)
    # end def _apply_get

    def _call_iter (self, ETM, entity, ** kw) :
        readonly = \
            ( self.prefilled
            or kw ["form_kw"].get ("prefilled")
            or kw.get ("readonly")
            )
        if kw.get ("allow_new") and not readonly :
            return self.__super._call_iter (ETM, entity, ** kw)
        return ()
    # end def _call_iter

    def _child_kw (self, kw) :
        result = self.__super._child_kw (kw)
        f_kw   = result ["form_kw"]
        if "allow_new" in f_kw :
            result ["allow_new"] = f_kw.pop ("allow_new")
        return result
    # end def _child_kw

Field_Entity = _MOM_Field_Entity_ # end class

class Field_Role_Hidden (Field_Entity) :
    """Hidden field description a hidden role of an Entity_Link."""

    rank           = Entity_Link.rank - 1
    _pop_allow_new = True

    def __init__ (self, ** kw) :
        kw.pop ("completer", None)
        self.__super.__init__ (** kw)
    # end def __init__

    def apply (self, value, results, scope, on_error = None, ** kw) :
        try :
            return results [value.anchor_id]
        except KeyError :
            pid = value.edit.get ("pid")
            if pid is not None :
                return scope.pid_query (pid)
    # end def apply

    def applyf (self, value, results, scope, entity, on_error = None, ** kw) :
        return self.apply (value, results, scope, on_error = on_error, ** kw)
    # end def applyf

    def display (self, instance) :
        return None
    # end def display

    def _anchor_self (self, anchor) :
        if anchor is not None :
            self.__super._anchor_self (anchor)
            ### need to fix `.anchor_id` and `.anchor`: should point to the
            ### anchor of anchor (which is a link to anchor.anchor)
            anchor = self.anchor
            if anchor and anchor.anchor :
                self.anchor_id = anchor.anchor.id
    # end def _anchor_self

# end class Field_Role_Hidden

Fieldset = AE.Fieldset

class _MOM_Form_ (AE.Form) :
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

Group = AE.Group

if __name__ != "__main__" :
    GTW.AFS.MOM._Export_Module ()
### __END__ GTW.AFS.MOM.Element
