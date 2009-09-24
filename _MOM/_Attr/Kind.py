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
#    MOM.Attr.Kind
#
# Purpose
#    Provide descriptor classes for various attribute kinds of MOM
#
# Revision Dates
#    24-Sep-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _MOM                  import MOM

import _TFL._Meta.Property

import _MOM._Attr
import _MOM._Prop.Kind

class Kind (MOM.Prop.Kind) :
    """Root class of attribute kinds to be used as properties for essential
       attributes of the MOM meta object model.
    """

    attr                  = None
    prop                  = TFL.Meta.Alias_Property ("attr")
    sync                  = None
    Table                 = dict ()

    def __init__ (self, attr_type) :
        attr = attr_type      (self)
        self.__super.__init__ (attr)
        self._check_sanity    (attr_type)
        self.record_changes = self.attr.record_changes and self.record_changes
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
        self.set_cooked (obj, value)
    # end def __set__

    def get_value (self, obj) :
        raise NotImplementedError ("must be defined by descendent")
    # end def get_value

    def inc_changes (self, man, obj, value) :
        ### don't redefine this (redefine `_inc_changes` instead)
        ### (this allows applications to extend `inc_changes` without having
        ### to know all classes redefining `_inc_changes`) !!!
        self._inc_changes (man, obj, value)
    # end def inc_changes

    def reset (self, obj) :
        self.set_raw (obj, self.attr.default, dont_raise = True)
    # end def reset

    def set_cooked (self, obj, value) :
        self.attr.check_invariant (obj, value)
        if self.record_changes and self.get_value (obj) != value :
            obj.home_scope.record_change \
                ( TOM.SCM.Entity_Change_Attr
                , obj, {self.name : self.get_raw (obj)}
                )
        self._set_cooked (obj, value)
    # end def set_cooked

    def set_raw (self, obj, raw_value, glob_dict = None, dont_raise = False) :
        if glob_dict is None :
            glob_dict = obj.globals ()
        value = None
        if raw_value :
            try :
                value = self.attr.from_string (obj, raw_value, glob_dict)
                self.attr.check_invariant     (obj, value)
            except KeyboardInterrupt :
                raise
            except StandardError, exc :
                if dont_raise :
                    if __debug__ :
                        print exc
                else :
                    raise
        self._set_raw (obj, raw_value, value)
    # end def set_raw

    def sync_cooked (self, obj, raw_value) :
        if __debug__ :
            print ( "Trying to sync pending attribute %s of %s to `%s`"
                  ) % (self.name, obj.name, raw_value)
        self.set_raw (obj, raw_value)
    # end def sync_cooked

    def _check_sanity (self, attr_type) :
        if __debug__ :
            default = getattr (attr_type, "default", None)
            if (   default is not None
               and not isinstance (default, (str, unicode))
               ) :
                d = attr_type.as_string (default)
                if d == "" and default is not None :
                    d = "%s" % default
                raise ValueError, \
                    ( """>>> %s.%s: got `%s` instead of "%s" as default"""
                    % (attr_type, self.name, default, d)
                    )
    # end def _check_sanity

    def _get_computed (self, obj) :
        computed = self.attr.computed
        if TFL.callable (computed) :
            try :
                val = computed (obj)
            except KeyboardInterrupt :
                raise
            except StandardError :
                raise
            if val is not None :
                return self.attr.cooked (val)
    # end def _get_computed

    def _inc_changes (self, man, obj, value) :
        man.inc_changes ()
    # end def _inc_changes

    def set_cooked (self, obj, value) :
        self.attr.check_invariant (obj, value)
        if self.record_changes and self.get_value (obj) != value :
            obj.home_scope.record_change \
                ( TOM.SCM.Entity_Change_Attr
                , obj, {self.name : self.get_raw (obj)}
                )
        self._set_cooked (obj, value)
    # end def set_cooked

    def set_raw (self, obj, raw_value, glob_dict = None, dont_raise = False) :
        if glob_dict is None :
            glob_dict = obj.globals ()
        value = None
        if raw_value :
            try :
                value = self.attr.from_string (obj, raw_value, glob_dict)
                self.attr.check_invariant     (obj, value)
            except KeyboardInterrupt :
                raise
            except StandardError, exc :
                if dont_raise :
                    if __debug__ :
                        print exc
                else :
                    raise
        self._set_raw (obj, raw_value, value)
    # end def set_raw

    def _set_cooked (self, obj, value) :
        self._set_cooked_inner (obj, value)
    # end def _set_cooked

    def _set_cooked_inner (self, obj, value) :
        if value is not None :
            try :
                value = self.attr.cooked (value)
            except KeyboardInterrupt :
                raise
            except StandardError, exc :
                print "%s: %s.%s, value `%s`" % (exc, obj, self.name, value)
                raise
        self._set_cooked_value (obj, value)
    # end def _set_cooked_inner

    def _set_cooked_value (self, obj, value, changed = 42) :
        man = obj._attr_man
        if changed == 42 :
            ### if the caller didn't pass a (boolean) value, evaluate it here
            changed = \
                man.attr_values [self.attr_dict_name].get (self.name) != value
        if changed :
            self.inc_changes (man, obj, value)
            self._set_cooked_value_inner (obj, value)
    # end def _set_cooked_value

    def _set_cooked_value_inner (self, obj, value) :
        raise NotImplementedError ("must be defined by descendent")
    # end def _set_cooked_value_inner

    def _set_raw (self, obj, raw_value, value) :
        self._set_cooked_inner (obj, value)
    # end def _set_raw

    def _set_raw_inner (self, obj, raw_value, value) :
        pass
    # end def _set_raw_inner

    def __cmp__ (self, other) :
        return cmp  (self.attr, getattr (other, "attr", other)
    # end def __cmp__

    def __hash__ (self) :
        return hash (self.attr)
    # end def __hash__

    def __repr__ (self) :
        return "%s `%s`" % (self.attr.typ, self.name)
    # end def __repr__

# end class Kind

class _DB_Attr_ :
    """Attributes stored in DB."""

    save_to_db     = True
    record_changes = True

    def to_save (self, obj) :
        raw_val = self.get_raw (obj)
        result  = bool (raw_val)
        if result and not self.store_default :
            result = raw_val != self.default
        return result
    # end def to_save

# end class _DB_Attr_

class _Volatile_ :
    """Attributes not stored in DB."""

    save_to_db     = False
    record_changes = False

    def to_save (self, obj) :
        return False
    # end def to_save

# end class _Volatile_

class _User_ (_DB_Attr_, Kind) :
    """Attributes set by user."""

    electric       = False

    def get_raw (self, obj) :
        raise NotImplementedError ("must be defined by descendent")
    # end def get_raw

    def get_value (self, obj) :
        if obj._attr_man.needs_sync.get (self.name) :
            self._sync (obj)
        return self.__super.get_value (obj)
    # end def get_value

    def _set_cooked (self, obj, value) :
        self.__super._set_cooked (obj, value)
        self._set_raw_inner      (obj, self.attr.as_string (value), value)
    # end def _set_cooked

    def _set_raw (self, obj, raw_value, value) :
        if raw_value != self.get_raw (obj) :
            self.inc_changes  (obj._attr_man, obj, value)
        self.__super._set_raw (obj, raw_value, value)
        self._set_raw_inner   (obj, raw_value, value)
    # end def _set_raw

    def _set_raw_inner (self, obj, raw_value, value) :
        raise NotImplementedError ("must be defined by descendent")
    # end def _set_raw_inner

    def _sync (self, obj) :
        raw_value = self.get_raw (obj)
        value     = None
        if raw_value :
            try :
                value = self.attr.from_string (obj, raw_value, obj.globals ())
            except KeyboardInterrupt :
                raise
            except StandardError, exc :
                if __debug__ :
                    print exc
        self._set_cooked_inner (obj, value)
        obj._attr_man.needs_sync [self.name] = False
    # end def _sync

# end class _User_

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Kind
