# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Attr.Kind
#
# Purpose
#    Provide descriptor classes for various attribute kinds of MOM
#
# Revision Dates
#    24-Sep-2009 (CT) Creation (factored from TOM.Attr.Kind)
#    28-Sep-2009 (CT) Creation continued
#    29-Sep-2009 (CT) Creation continued..
#     6-Oct-2009 (CT) Creation continued...: `Primary`: method redefinitions
#     7-Oct-2009 (CT) Creation continued....: `set_cooked` folded into `__set__`
#     9-Oct-2009 (CT) `_symbolic_default` and `raw_default` added
#     9-Oct-2009 (CT) `Primary.__set__` changed to raise unconditionally
#     9-Oct-2009 (CT) `Sticky_Mixin` changed to use `reset` instead of
#                     homegrown code
#    12-Oct-2009 (CT) `is_primary` and `is_settable` added
#    19-Oct-2009 (CT) `changed = 42` added to various `set`-specific methods
#                     to avoid change checks during `reset`
#    20-Oct-2009 (MH) `s/TOM/MOM/g`
#    21-Oct-2009 (CT) `Class_Uses_Default_Mixin` removed
#    22-Oct-2009 (CT) Use `M_Attr_Kind` as meta
#    22-Oct-2009 (CT) s/default/raw_default/ where necessary
#    22-Oct-2009 (CT) `_Raw_Value_Mixin_` factored
#    28-Oct-2009 (CT) I18N
#    29-Oct-2009 (CT) `rank` added
#     3-Nov-2009 (CT) `Link_Role.get_role` added
#    19-Nov-2009 (CT) `Link_Role.sort_key` added
#    20-Nov-2009 (CT) Documentation added
#    20-Nov-2009 (CT) `__all__` computed explicitly
#    23-Nov-2009 (CT) `__cmp__` and `__hash__` removed (breaks hashing of
#                     Link_Role attributes)
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    26-Nov-2009 (CT) `_Object_Reference_Mixin_` and `Object_Reference_Mixin`
#                     added
#    28-Nov-2009 (CT) `_Object_Reference_Mixin_._update_raw` removed
#    16-Dec-2009 (CT) `record_changes` set to False for all kinds but `_User_`
#    16-Dec-2009 (CT) Defaults for `electric`, `record_changes`, and
#                     `save_to_db` moved to `Kind`
#    17-Dec-2009 (CT) Don't `record_changes` for electric objects
#    18-Dec-2009 (CT) Use `unicode` instead of `str`
#    21-Dec-2009 (CT) `get_pickle_cargo` and `set_pickle_cargo` (and
#                     `_EPK_Mixin_`) added
#    29-Dec-2009 (CT) `get_raw` and `get_value` changed to allow `None` for
#                     `obj`
#    30-Dec-2009 (CT) `_EPK_Mixin_._set_cooked_inner` to guard for differing
#                     `home_scope`
#    30-Dec-2009 (CT) `__set__` changed to really record changes
#     5-Jan-2010 (CT) `_checkers` added to `Kind` and `Primary`
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _MOM                  import MOM

import _TFL._Meta.Property

import _MOM._Attr
import _MOM._Meta.M_Attr_Kind
import _MOM._Prop.Kind

from   _TFL.I18N             import _, _T, _Tn

class Kind (MOM.Prop.Kind) :
    """Root class of attribute kinds to be used as properties for essential
       attributes of the MOM meta object model.
    """

    __metaclass__         = MOM.Meta.M_Attr_Kind

    attr                  = None
    electric              = True
    is_primary            = False
    is_settable           = True
    needs_raw_value       = False
    prop                  = TFL.Meta.Alias_Property ("attr")
    record_changes        = False
    save_to_db            = False
    sync                  = None
    Table                 = dict ()

    def __init__ (self, Attr_Type) :
        attr = Attr_Type      (self)
        self.__super.__init__ (attr)
        self._check_sanity    (attr)
        self.rank           = (attr._t_rank, attr.rank)
        self.record_changes = attr.record_changes and self.record_changes
    # end def __init__

    def __delete__ (self, obj) :
        self.reset (obj)
    # end def __delete__

    def __get__ (self, obj, cls) :
        if obj is None :
            return self
        return self.get_value (obj)
    # end def __get__

    def __set__ (self, obj, value) :
        old_value = self.get_value (obj)
        old_raw   = self.get_raw   (obj)
        self.attr.check_invariant  (obj, value)
        self._set_cooked           (obj, value)
        if  ( self.record_changes and (not obj.electric)
            and old_value != value
            ) :
            obj.home_scope.record_change \
                (MOM.SCM.Change.Attr, obj, {self.name : old_raw})
    # end def __set__

    def get_pickle_cargo (self, obj) :
        return (self.get_value (obj), )
    # end def get_pickle_cargo

    def get_raw (self, obj) :
        if obj is not None :
            val = self.get_value (obj)
            if val is not None :
                return self.attr.as_string (val) or ""
            else :
                return ""
        else :
            return self.attr.raw_default
    # end def get_raw

    def get_value (self, obj) :
        if obj is not None :
            return getattr (obj, self.attr.ckd_name, None)
        else :
            return self.attr.default or self.attr.raw_default
    # end def get_value

    def inc_changes (self, man, obj, value) :
        ### don't redefine this (redefine `_inc_changes` instead)
        ### (this allows applications to extend `inc_changes` without having
        ### to know all classes redefining `_inc_changes`) !!!
        return self._inc_changes (man, obj, value)
    # end def inc_changes

    def reset (self, obj) :
        if self.attr._symbolic_default :
            return self.set_raw \
                (obj, self.attr.raw_default, dont_raise = True, changed = True)
        else :
            if self.attr.raw_default and self.attr.default is None :
                self.attr.default = self.attr.from_string \
                    (self.attr.raw_default, obj, obj.globals ())
            return self._set_raw \
                (obj, self.attr.raw_default, self.attr.default, changed = True)
    # end def reset

    def set_pickle_cargo (self, obj, cargo) :
        self._set_cooked_value (obj, cargo [0], changed = True)
    # end def set_pickle_cargo

    def set_raw (self, obj, raw_value, glob_dict = None, dont_raise = False, changed = 42) :
        if glob_dict is None :
            glob_dict = obj.globals ()
        value = None
        if raw_value :
            try :
                value = self.attr.from_string (raw_value, obj, glob_dict)
                self.attr.check_invariant     (obj, value)
            except StandardError as exc :
                if dont_raise :
                    if __debug__ :
                        print exc
                else :
                    raise
        return self._set_raw (obj, raw_value, value, changed)
    # end def set_raw

    def sync_cooked (self, obj, raw_value) :
        if __debug__ :
            print _T \
                ( "Trying to sync pending attribute %s of %s to `%s`"
                ) % (self.name, obj.name, raw_value)
        self.set_raw (obj, raw_value)
    # end def sync_cooked

    def to_save (self, obj) :
        return False
    # end def to_save

    def _checkers (self) :
        for c in self.attr._checkers () :
            yield c
    # end def _checkers

    def _check_sanity (self, attr_type) :
        if __debug__ :
            default = getattr (attr_type, "raw_default", None)
            if (   default is not None
               and not isinstance (default, basestring)
               ) :
                d = attr_type.as_string (default)
                if d == "" and default is not None :
                    d = "%s" % default
                raise ValueError \
                    ( u""">>> %s.%s: got `%s` instead of "%s" as `raw_default`"""
                    % (attr_type, self.name, default, d)
                    )
    # end def _check_sanity

    def _get_computed (self, obj) :
        computed = self.attr.computed
        if TFL.callable (computed) :
            val = computed (obj)
            if val is not None :
                return self.attr.cooked (val)
    # end def _get_computed

    def _inc_changes (self, man, obj, value) :
        man.inc_changes ()
    # end def _inc_changes

    def _set_cooked (self, obj, value, changed = 42) :
        return self._set_cooked_inner (obj, value, changed)
    # end def _set_cooked

    def _set_cooked_inner (self, obj, value, changed = 42) :
        if value is not None :
            try :
                value = self.attr.cooked (value)
            except StandardError as exc :
                ### print "%s: %s.%s, value `%s`" % (exc, obj, self.name, value)
                raise
        return self._set_cooked_value (obj, value, changed)
    # end def _set_cooked_inner

    def _set_cooked_value (self, obj, value, changed = 42) :
        attr = self.attr
        if changed == 42 :
            ### if the caller didn't pass a (boolean) value, evaluate it here
            changed = self.get_value (obj) != value
        if changed :
            setattr          (obj, attr.ckd_name, value)
            self.inc_changes (obj._attr_man, obj, value)
            return True
    # end def _set_cooked_value

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        return self._set_cooked_inner (obj, value, changed)
    # end def _set_raw

    def _set_raw_inner (self, obj, raw_value, value, changed = 42) :
        pass
    # end def _set_raw_inner

    def __repr__ (self) :
        return "%s `%s`" % (self.attr.typ, self.name)
    # end def __repr__

# end class Kind

class _EPK_Mixin_ (Kind) :
    """Mixin for attributes referring to entities with `epk`."""

    def get_pickle_cargo (self, obj) :
        ref = self.get_value (obj)
        if ref is not None :
            return (ref.epk, )
    # end def get_pickle_cargo

    def set_pickle_cargo (self, obj, cargo) :
        ref = self.attr._get_object (obj, cargo [0], raw = False)
        self._set_cooked_value (obj, ref, changed = True)
    # end def set_pickle_cargo

    def _set_cooked_inner (self, obj, value, changed = 42) :
        scope = obj.home_scope
        if value is not None and scope != value.home_scope :
            etm = scope [value.type_name]
            val = etm.instance (* value.epk_raw, raw = True)
            if val is None :
                raise MOM.Error.Link_Scope_Mix_Error \
                    (scope, value.home_scope, scope)
            else :
                value = val
        return self._set_cooked_value (obj, value, changed)
    # end def _set_cooked_inner

# end class _EPK_Mixin_

class _Raw_Value_Mixin_ (Kind) :
    """Mixin for keeping raw values of user-specified attributes."""

    needs_raw_value = True

    def get_pickle_cargo (self, obj) :
        return self.get_value (obj), self.get_raw (obj)
    # end def get_pickle_cargo

    def get_raw (self, obj) :
        if obj is not None :
            return getattr (obj, self.attr.raw_name, "")
        else :
            return self.attr.raw_default
    # end def get_raw

    def get_value (self, obj) :
        if obj is not None and obj._attr_man.needs_sync.get (self.name) :
            self._sync (obj)
        return self.__super.get_value (obj)
    # end def get_value

    def has_substance (self, obj) :
        return self.get_raw (obj) not in ("", self.raw_default)
    # end def has_substance

    def set_pickle_cargo (self, obj, cargo) :
        ckd = cargo [0]
        if len (cargo) > 1 :
            raw = cargo [1]
            self._set_cooked_value (obj,      ckd, changed = True)
            self._set_raw_inner    (obj, raw, ckd, changed = True)
        else :
            self._set_cooked       (obj,      ckd, changed = True)
    # end def set_pickle_cargo

    def _set_cooked (self, obj, value, changed = 42) :
        self._set_cooked_inner (obj, value, changed)
        self._set_raw_inner (obj, self.attr.as_string (value), value, changed)
    # end def _set_cooked

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        if changed == 42 :
            ### if the caller didn't pass a (boolean) value, evaluate it here
            changed = raw_value != self.get_raw (obj)
        if changed :
            self.inc_changes  (obj._attr_man, obj, value)
        self.__super._set_raw (obj, raw_value, value, changed)
        self._set_raw_inner   (obj, raw_value, value, changed)
    # end def _set_raw

    def _set_raw_inner (self, obj, raw_value, value, changed = 42) :
        setattr (obj, self.attr.raw_name, raw_value)
    # end def _set_raw_inner

    def _sync (self, obj) :
        raw_value = self.get_raw (obj)
        value     = None
        if raw_value :
            try :
                value = self.attr.from_string (raw_value, obj, obj.globals ())
            except StandardError as exc :
                if __debug__ :
                    print exc
        self._set_cooked_inner (obj, value)
        obj._attr_man.needs_sync [self.name] = False
    # end def _sync

# end class _Raw_Value_Mixin_

class _DB_Attr_ (Kind) :
    """Attributes stored in DB."""

    save_to_db     = True

    def to_save (self, obj) :
        raw_val = self.get_raw (obj)
        result  = bool (raw_val)
        if result and not self.store_default :
            result = raw_val != self.raw_default
        return result
    # end def to_save

# end class _DB_Attr_

class _User_ (_DB_Attr_, Kind) :
    """Attributes set by user."""

    electric       = False
    record_changes = True

    def has_substance (self, obj) :
        return self.get_value (obj) not in (None, self.default)
    # end def has_substance

# end class _User_

class _System_ (Kind) :
    """Attributes set by system."""

# end class _System_

class _DB_System_ (_DB_Attr_, _System_) :
    pass
# end class _DB_System_

class _Volatile_ (Kind) :
    """Attributes not stored in DB."""

# end class _Volatile_

class _Cached_ (_Volatile_, _System_) :

    is_settable = False
    kind        = "cached"

    def _inc_changes (self, man, obj, value) :
        pass
    # end def _inc_changes

# end class _Cached_

class Primary (_User_) :
    """Primary attribute: must be defined at all times, used as part of the
       `essential primary key`.
    """

    is_primary  = True
    kind        = "primary"

    def __set__ (self, obj, value) :
        raise AttributeError \
            ( "\n".join
                ( ( _T ( "Primary attribute `%s.%s` cannot be assigned.")
                  , _T ("Use `set` or `set_raw` to change it.")
                  )
                )
            % (obj.type_name, self.name)
            )
    # end def __set__

    def __delete__ (self, obj, value) :
        raise AttributeError \
            ( _T ("Primary attribute `%s.%s` cannot be deleted")
            % (obj.type_name, self.name)
            )
    # end def __delete__

    def to_save (self, obj) :
        return True
    # end def to_save

    def _checkers (self) :
        yield "value is not None and value != ''", (self.name, )
        for c in self.__super._checkers () :
            yield c
    # end def _checkers

# end class Primary

class Link_Role (_EPK_Mixin_, Primary) :
    """Link-role attribute must be defined at all times, used for (essential)
       primary key.
    """

    get_role               = TFL.Meta.Alias_Property ("get_value")

    def sort_key (self, l) :
        r = self.get_role (l)
        return r.__class__.sort_key () (r)
    # end def sort_key

# end class Link_Role

class Required (_User_) :
    """Required attribute: must be defined by the tool user."""

    kind        = "required"

    def to_save (self, obj) :
        return self.has_substance (obj)
    # end def to_save

# end class Required

class Optional (_User_) :
    """Optional attribute: if undefined, the `default` value is used, if any."""

    kind = "optional"

# end class Optional

class Internal (_DB_System_) :
    """Internal attribute: value is defined by some component of the tool."""

    kind = "internal"

# end class Internal

class Const (_Cached_) :
    """Constant attribute (has static default value that cannot be changed)."""

    kind        = "constant"

    def __set__ (self, obj, value) :
        raise AttributeError \
            ( _T ("Constant attribute `%s.%s` cannot be changed")
            % (obj.type_name, self.name)
            )
    # end def __set__

# end class Const

class Cached (_Cached_) :
    """Cached attribute: value is defined by some component of the tool, but
       not saved to DB.
    """

# end class Cached

class Sync_Cached (_Cached_) :
    """Cached attribute computed automatically when syncing. This kind can be
       used for attributes dependending on attributes of different objects,
       as long those don't change significantly between syncing --- use
       :class:`Computed` otherwise.
    """

    def sync (self, obj) :
        self._set_cooked (obj, self._get_computed (obj))
        obj._attr_man.needs_sync [self.name] = False
    # end def sync

    def get_raw (self, obj) :
        if obj is not None and obj._attr_man.needs_sync [self.name] :
            self.sync (obj)
        return self.__super.get_raw (obj)
    # end def get_raw

    def get_value (self, obj) :
        if obj is not None and obj._attr_man.needs_sync [self.name] :
            self.sync (obj)
        return self.__super.get_value (obj)
    # end def get_value

    def reset (self, obj) :
        self.__super.reset (obj)
        obj._attr_man.needs_sync [self.name] = True
    # end def reset

# end class Sync_Cached

class Auto_Cached (_Cached_) :
    """Cached attribute that is recomputed whenever it is accessed after one
       or more of the other attributes changed since the last recomputation.

       This kind must **not** be used if the value of the attribute depends
       on other objects (use :class:`Sync_Cached` or :class:`Computed` if
       that's the case).
    """

    def get_value (self, obj) :
        if obj is not None :
            man = obj._attr_man
            if ((man.total_changes != man.update_at_changes.get (self.name, -1))
               or self.attr.ckd_name not in obj.__dict__
               ) :
                val = self._get_computed (obj)
                if val is None :
                    return
                self._set_cooked (obj, val)
                man.update_at_changes [self.name] = man.total_changes
        return self.__super.get_value (obj)
    # end def get_value

    def reset (self, obj) :
        obj._attr_man.update_at_changes [self.name] = -1
    # end def reset

# end class Auto_Cached

class Once_Cached (_Cached_) :
    """Cached attribute computed just once (a.k.a. computed constant).
       This kind can be used if the `constant` value that is computed depends
       on attributes of different objects, as longs as those don't change
       during the lifetime of this attribute's object.
    """

    def reset (self, obj) :
        val = self.get_value (obj)
        if val is None :
            val = self._get_computed (obj)
            self._set_cooked_inner   (obj, val, changed = True)
    # end def reset

# end class Once_Cached

class Cached_Role (_Cached_) :
    """Cached attribute automagically updated by association."""

    def reset (self, obj) :
        pass
    # end def reset

# end class Cached_Role

class Cached_Role_DFC (Cached_Role) :
    """Cached attribute normally updated by association but asking
       association for DFC_Link.
    """

    def get_value (self, obj) :
        result = self.__super.get_value (obj)
        if obj is not None and result is None :
            ### XXX
            assoc = getattr (obj.home_scope, self.attr.assoc)
            links = getattr (assoc, self.attr.name) (obj)
            if links :
                assert len (links) == 1
                result = getattr (links [0], self.attr.name)
        return result
    # end def get_value

# end class Cached_Role_DFC

class Computed (_Cached_) :
    """Computed attribute: the value is computed for each and every attribute
       access. This is quite inefficient and should only be used if
       :class:`Auto_Cached` or :class:`Sync_Cached` don't work.
    """

    kind        = "computed"

    def reset (self, obj) :
        pass
    # end def reset

    def _check_sanity (self, attr_type) :
        self.__super._check_sanity (attr_type)
        default = self.attr.raw_default
        if default :
            raise TypeError \
                ( "%s is computed but has default %r "
                  "(i.e., `computed` will never be called)"
                % (attr_type, default)
                )
    # end def _check_sanity

# end class Computed

class Computed_Mixin (Kind) :
    """Mixin to compute attribute value if empty, i.e., if no value was
       specified by the tool user.
    """

    def get_value (self, obj) :
        result = self.__super.get_value (obj)
        if obj is not None and result is None :
            result = self._get_computed (obj)
        return result
    # end def get_value

    def _check_sanity (self, attr_type) :
        self.__super._check_sanity (attr_type)
        default = self.attr.raw_default
        if default :
            raise TypeError \
                ( "%s is _Computed_ but has default %r "
                  "(i.e., `computed` will never be called)"
                % (attr_type, default)
                )
    # end def _check_sanity

# end class Computed_Mixin

class Sticky_Mixin (Kind) :
    """Mixin to reset the attribute to the default value whenever the tool
       user enters an empty value.
    """

    def _check_sanity (self, attr_type) :
        self.__super._check_sanity (attr_type)
        if not self.attr.raw_default :
            raise TypeError \
                ("%s is sticky but lacks `default`" % (attr_type, ))
    # end def _check_sanity

    def _set_cooked (self, obj, value, changed = 42) :
        if value is None :
            self.reset (obj)
        else :
            self.__super._set_cooked (obj, value, changed)
    # end def _set_cooked

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        if raw_value in ("", None) :
            self.reset (obj)
        else :
            self.__super._set_raw (obj, raw_value, value, changed)
    # end def _set_raw

# end class Sticky_Mixin

class _Object_Reference_Mixin_ (_EPK_Mixin_) :

    def __delete__ (self, obj) :
        ### We need to manually set the value to None first in order to
        ### get the dependencies updated
        self._set_cooked_value  (obj, None)
        self.__super.__delete__ (obj)
    # end def __delete__

    def _register (self, obj, value) :
        if value is not obj :
            value.register_dependency (obj)
            obj.object_referring_attributes [value].append (self)
    # end def _register

    def _unregister (self, obj, old_value) :
        old_value.unregister_dependency (obj)
        try :
            del obj.object_referring_attributes [old_value]
        except KeyError :
            pass
    # end def _unregister

# end class _Object_Reference_Mixin_

class Object_Reference_Mixin (_Object_Reference_Mixin_) :
    """Kind mixin for handling object references correctly."""

    def _set_cooked_value (self, obj, value, changed = 42) :
        old_value = self.get_value (obj)
        changed   = old_value is not value
        if changed :
            if old_value :
                self._unregister (obj, old_value)
            self.__super._set_cooked_value (obj, value, changed)
            if value and not isinstance (value, basestring) :
                self._register (obj, value)
    # end def _set_cooked_value

# end class Object_Reference_Mixin

### XXX Object-Reference- and Link-related kinds

__doc__ = """
Class `MOM.Attr.Kind`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Kind

    `MOM.Attr.Kind` is the root class of a hierarchy of classes defining the
    various kinds of attributes of essential classes. The attribute kind
    controls how the value of an attribute is accessed and how (and if) it
    can be modified. Technically, `Kind` and its subclasses define Python
    `data descriptors` that implement `property` semantics.

    The kind of a concrete attribute is specified as one the properties of
    the :class:`attribute's type<_MOM._Attr.Type.A_Attr_Type>`. The kind
    class gets instantiated by :class:`~_MOM._Attr.Spec.Spec` which passes
    the `type` to the kind's `__init__`.

    Some kinds of attributes are stored into the database, e.g.,
    :class:`Primary`, :class:`Required`, :class:`Optional` (and its
    descendents), and :class:`Internal`, others are not, e.g., the various
    kinds of cached and computed attributes.

    There are some mixins that can modify the semantics of :class:`Optional`
    attributes.

.. autoclass:: Primary
.. autoclass:: Required
.. autoclass:: Optional

.. autoclass:: Internal
.. autoclass:: Cached
.. autoclass:: Computed
.. autoclass:: Auto_Cached
.. autoclass:: Sync_Cached
.. autoclass:: Once_Cached
.. autoclass:: Const

.. autoclass:: Computed_Mixin
.. autoclass:: Sticky_Mixin

"""

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Kind)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Kind
