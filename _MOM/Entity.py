# -*- coding: iso-8859-15 -*-
# Copyright (C) 1999-2013 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Entity
#
# Purpose
#    Root class for object- and link-types of MOM meta object model
#
# Revision Dates
#    17-Sep-2009 (CT) Creation (factored from `TOM.Entity`)
#    23-Sep-2009 (CT) Journal-related methods removed
#     1-Oct-2009 (CT) `Entity_Essentials` removed
#     7-Oct-2009 (CT) `filters` removed
#     8-Oct-2009 (CT) `An_Entity` and `Id_Entity` factored from `Entity`
#     9-Oct-2009 (CT) Cooked instead of raw values assigned to
#                     attribute `default`s
#    12-Oct-2009 (CT) `Entity.__init__` changed to set attributes from `kw`
#    12-Oct-2009 (CT) `Id_Entity._init_epk` added and used
#    13-Oct-2009 (CT) `Id_Entity`: redefined `set` and `set_raw`
#    13-Oct-2009 (CT) `Id_Entity`: added `_extract_primary*`,
#                     `_rename`, and `_reset_epk`
#    13-Oct-2009 (CT) `__init__` and `__new__` refactored
#    15-Oct-2009 (CT) `is_relevant` and `relevant_root` added
#    20-Oct-2009 (CT) Moved call of `init_epk` from `__new__` to `__init__`
#    20-Oct-2009 (NN) `epk_as_dict` added
#    21-Oct-2009 (CT) `is_locked` changed to use `.default` if called
#                     as class method
#    21-Oct-2009 (CT) `Class_Uses_Default_Mixin` removed
#    21-Oct-2009 (CT) `_finish__init__` factored
#    21-Oct-2009 (CT) Predicate `primary_key_defined` removed
#    25-Oct-2009 (MG) `__getattr__` Use %s instead of %r to avoid recursive
#                     calls of `__getattr__`
#     4-Nov-2009 (CT) `refuse_links` changed from dict to set
#    23-Nov-2009 (CT) `epk_as_code` added and used in `_repr` and `__str__`
#    25-Nov-2009 (CT) `set` and `set_raw` of `Id_Entity` corrected
#    25-Nov-2009 (CT) `as_code`, `attr_as_code` and `errors` added
#    26-Nov-2009 (CT) `_extract_primary` changed to allow `role_name`, too
#    26-Nov-2009 (CT) `set` and `set_raw` of `Id_Entity` changed to include
#                     `len (pkas_ckd)` in `result`
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    26-Nov-2009 (CT) s/_finish__init__/_main__init__/
#    27-Nov-2009 (CT) `update_dependency_names` removed
#    28-Nov-2009 (CT) `is_partial = True` added to all classes
#     3-Dec-2009 (CT) `set_raw` changed to use `on_error`
#     3-Dec-2009 (CT) `on_error` changed to use `scope._attr_errors` and print
#                     warning
#     3-Dec-2009 (CT) `sorted_by` changed to be `Alias_Property` for
#                     `sorted_by_epk`
#    14-Dec-2009 (CT) `user_attr_iter` factored
#    14-Dec-2009 (CT) `copy` changed to handle `scope`
#    14-Dec-2009 (CT) `Id_Entity._main__init__` changed to not call `scope.add`
#    15-Dec-2009 (MG) `_reset_epk`: guard added to make sure `epk` is only
#                     deleted if it is present in the instance dict
#    16-Dec-2009 (CT) `_reset_epk` un-DRY-ed
#    16-Dec-2009 (CT) `_set_ckd` and `_set_raw` factored and used
#    16-Dec-2009 (CT) `copy` rewritten to use `nested_change_recorder`
#    17-Dec-2009 (CT) `_record_context` factored from `set` and `set_raw` and
#                     guard for `electric` added
#    17-Dec-2009 (CT) `epk_raw` added
#    17-Dec-2009 (CT) `changes` and `async_changes` added
#    17-Dec-2009 (CT) `user_diff` and `user_equal` added
#    18-Dec-2009 (CT) Initialization of `dependencies` moved to
#                     `_init_meta_attrs`
#    21-Dec-2009 (CT) `as_pickle_cargo` and `from_pickle_cargo` added
#    21-Dec-2009 (CT) Signature of `_finish__init__` changed to `(self)`
#    30-Dec-2009 (CT) s/Package_NS/PNS/
#    20-Jan-2010 (CT) `ETM` and `lid` added to `Id_Entity`
#    21-Jan-2010 (CT) `copy` changed to only copy attributes `to_save`
#    21-Jan-2010 (CT) `epkified` added, `epkified_ckd` and `epkified_raw` used
#     2-Feb-2010 (CT) Support for `updates_pending` of attributes added
#     4-Feb-2010 (CT) `An_Entity.as_string` added
#     4-Feb-2010 (CT) Optional argument `kind` added to `is_correct`
#     4-Feb-2010 (CT) `An_Entity.copy` added and `._init_attributes` redefined
#     5-Feb-2010 (CT) Change management for `set` and `set_raw` moved from
#                     `Id_Entity` to `Entity`
#     5-Feb-2010 (CT) Exception handler added `epkified` to improve error
#                     message
#     8-Feb-2010 (CT) `An_Entity.__init__` added to disable `* args`
#     8-Feb-2010 (CT) `snapshot` and `has_changed` removed
#     9-Feb-2010 (CT) `epk_hash` added
#     9-Feb-2010 (CT) `An_Entity.set` and `.set_raw` redefined
#    10-Feb-2010 (CT) `FO` and `ui_display` added
#    12-Feb-2010 (CT) `FO` turned into a Auto_Cached attribute
#    13-Feb-2010 (MG) `_record_iter` changed to allow recognition of specific
#                     role names (e.g.: rodent, trap, person, ...)
#    16-Feb-2010 (MG) `copy` fixed (use the correct etypes from the passed
#                     scope argument)
#    16-Feb-2010 (CT) `copy` changed to use `scope.entity_type` instead of
#                     home-grown code
#    19-Feb-2010 (MG) `Entity.__repr__` changed
#    22-Feb-2010 (CT) `cooked_attrs` added
#    25-Feb-2010 (CT) `mandatory_defined` added
#    25-Feb-2010 (CT) `Id_Entity._main__init__` changed to pass both `epk` and
#                     `kw` in a single call to `setter`
#     1-Mar-2010 (CT) `set_pickle_cargo` factored from `from_pickle_cargo`
#     1-Mar-2010 (CT) `_record_iter_attrs` replaced by `recordable_attrs`
#    11-Mar-2010 (CT) `mandatory_defined` removed (was a Bad Idea (tm))
#    11-Mar-2010 (CT) `_kw_check_mandatory` added
#    11-Mar-2010 (CT) `raw_attr_dict` factored
#    11-Mar-2010 (CT) `An_Entity.set` and `.set_raw` changed to handle changes
#                     of primary composite attributes properly (rename!)
#    15-Mar-2010 (CT) Exception handler added to `epk_as_code`
#    22-Mar-2010 (CT) `last_changed` added
#     8-Apr-2010 (CT) `last_changed.computed` guarded against `first` returning
#                     `None`
#    26-Apr-2010 (CT) Guard against `raw` added to `Entity.set` and
#                     `Entity.set_raw`
#     3-May-2010 (CT) `epk` and `epk_raw` changed to append `type_name`
#    12-May-2010 (CT) `lid` removed
#    17-May-2010 (CT) `copy` changed to not handle other `scope` instances
#    19-May-2010 (CT) `user_diff` and `user_equal` rewritten to compare
#                     `as_pickle_cargo` (otherwise, attributes pointing to
#                     other entities make trouble)
#    27-May-2010 (CT) `cooked_attrs` changed to `from_string` instead `cooked`
#    27-May-2010 (CT) `on_error` added to `cooked_attrs`
#    17-Jun-2010 (CT) Use `TFL.I18N.encode_o` instead of home-grown code
#    17-Jun-2010 (CT) `__unicode__` introduced
#    18-Jun-2010 (CT) s/""/u""/
#    22-Jun-2010 (CT) `_kw_check_mandatory` changed to set
#                     `_pred_man.missing_mandatory`
#    22-Jun-2010 (CT) `_main__init__` changed to raise `mandatory_errors`, if
#                     any (otherwise, `on_error` can lead to object creation
#                     with missing `epk`)
#    24-Jun-2010 (CT) `relevant_root = None` moved from `Id_Entity` to `Entity`
#    29-Jun-2010 (CT) s/from_pickle_cargo/from_attr_pickle_cargo/
#                     s/as_pickle_cargo/as_attr_pickle_cargo/
#    29-Jun-2010 (CT) New `as_pickle_cargo` added
#    30-Jun-2010 (CT) Reference to `home_scope._locked` removed
#     1-Jul-2010 (CT) `Id_Entity.as_pickle_cargo` changed to put `pid` last
#    11-Aug-2010 (CT) `last_cid` added
#    11-Aug-2010 (CT) Optional argument `ignore` added to `user_diff`
#    18-Aug-2010 (CT) `owner_attr` added to `An_Entity`
#    19-Aug-2010 (CT) `An_Entity.__nonzero__` added
#    19-Aug-2010 (CT) `Id_Entity.ui_display_format` changed to use
#                     `has_substance` to check attributes
#     3-Sep-2010 (CT) `epk_hash` removed
#     8-Sep-2010 (CT) `record_attr_change` implemented
#    13-Sep-2010 (CT) `_FO_.__getattr__` changed to return `FO` of `Entity`
#                     instances
#    14-Sep-2010 (CT) `unicode_literals` added
#    28-Sep-2010 (CT) `epk_raw` changed to use `get_raw_epk` instead of
#                     `get_raw`
#    14-Oct-2010 (CT) `init_finished` added
#    14-Oct-2010 (CT) `Init_Only_Mixin` added to `electric`
#    22-Dec-2010 (CT) `is_relevant` moved from `Id_Entity` to `Entity`
#     8-Feb-2011 (CT) s/Required/Necessary/, s/Mandatory/Required/
#    27-May-2011 (CT) Guard for unchanged `epk` added to `_set_raw`
#     9-Sep-2011 (CT) `Id_Entity.__eq__` (& `__hash__`) redefined to cheaply
#                     support queries against integers (interpreted as `pid`)
#    15-Nov-2011 (CT) Add defaults for `polymorphic_epk` and `polymorphic_epks`
#    20-Dec-2011 (CT) Remove `sorted` from `attr_as_code`
#    19-Jan-2012 (CT) Add `_init_pending`, make `_home_scope` optional
#    19-Jan-2012 (CT) Call `_finish__init__` only if `_home_scope`
#    24-Jan-2012 (CT) Remove `generate_doc`, `auto_display`, and `save_to_db`
#    24-Jan-2012 (CT) Add `show_in_ui`
#    31-Jan-2012 (CT) Change defaults for `polymorphic_epk` & `polymorphic_epks`
#                     from `None` to `False`
#    29-Mar-2012 (CT) Factor `all_links` up from `MOM.Object`
#    11-Apr-2012 (CT) Delay call of `_finish__init__` (called by `Scope.add`)
#    11-Apr-2012 (CT) Change `__eq__` (and `__hash__`) to use `pid` (and `guid`)
#    12-Apr-2012 (CT) Raise `Required_Missing`, not `TypeError`, in `epkified`
#    12-Apr-2012 (CT) Adapt `_kw_check_required` to change of `Required_Missing`
#    15-Apr-2012 (CT) Adapted to changes of `MOM.Error`
#    16-Apr-2012 (CT) Factor `FO.__call__`, add optional argument `value`
#    16-Apr-2012 (CT) Change `epkified` to `raise TypeError` if `not missing`
#    19-Apr-2012 (CT) Use translated `.ui_name` instead of `.type_name` for
#                     exceptions
#    20-Apr-2012 (CT) Change `Id_Entity._main__init__` to wrap
#                     `MOM.Error.Required_Missing` in `MOM.Error.Invariants`
#                     after checking predicates
#    20-Apr-2012 (CT) Factor `_kw_raw_check_predicates`
#    20-Apr-2012 (CT) Change `_set_ckd` and `_set_raw` to not set attributes in
#                     case of predicate errors
#    20-Apr-2012 (CT) Change `errors` to return `iter (self._pred_man)` instead
#                     of home-grown code (that lacked `missing_required`)
#    22-Apr-2012 (CT) Rename argument `kind` of `is_correct` and
#                     `_kw_check_required` to `_kind` to avoid possible name
#                     clash with an attribute with name `kind`
#     6-Jun-2012 (CT) Add `tn_pid`
#     6-Jun-2012 (CT) Set `_A_Id_Entity_.P_Type = Id_Entity`
#    13-Jun-2012 (CT) Add `reload_from_pickle_cargo`
#    18-Jun-2012 (CT) Add `_Id_Entity_Reload_Mixin_`
#     4-Jul-2012 (CT) `Id_Entity.__eq__` (& `__hash__`) redefined to cheaply
#                     support queries against strings (interpreted as `pid`)
#    30-Jul-2012 (CT) Change `_Id_Entity_Reload_Mixin_` to delegate `__repr__`
#     1-Aug-2012 (CT) Change `destroy_dependency` to consider
#                     `attr.is_required` and `attr.is_primary`, record changes
#     1-Aug-2012 (CT) Add `_Id_Entity_Destroyed_Mixin_`
#     3-Aug-2012 (CT) Add `all_referrers`, rewrite `all_links` to use it
#     4-Aug-2012 (CT) Add `Id_Entity.restore`
#     5-Aug-2012 (CT) Add `epk_raw_pid`
#     5-Aug-2012 (MG) Change `set` to use `get_raw_pid`
#     5-Aug-2012 (CT) Change `_record_iter_raw` to include `raw_pid`
#     7-Aug-2012 (CT) Use `Add_To_Class` instead of home-grown code
#     8-Aug-2012 (CT) Use `logging` instead of `print`
#     9-Sep-2012 (CT) Add `creation_date`
#    10-Sep-2012 (CT) Fix `creation_date.computed`
#    24-Sep-2012 (CT) Don't wrap `Error.Attribute_Value`
#    27-Sep-2012 (CT) Remove `rank` (never used in MOM)
#    12-Oct-2012 (CT) Use `signified` in `An_Entity._main__init__` to (allow
#                     `* args`), remove `.__init__` (which disallowed `* args`)
#    12-Oct-2012 (CT) Call `An_Entity.attr_as_code`, not `_formatted_user_attr`,
#                     in `An_Entity._repr` and `.__unicode__`
#    16-Oct-2012 (CT) Factor `attr_tuple_to_save` from `An_Entity.attr_as_code`
#     6-Dec-2012 (CT) Factor `creation_change` and `last_change`,
#                     add `created_by` and `last_changed_by`
#    10-Dec-2012 (CT) Add support for nested attributes to `FO`
#    11-Dec-2012 (CT) Move `_Class_Kind` from `Entity` to `M_Entity`
#    11-Jan-2013 (CT) Check `primary_ais` in `_main__init__`
#    16-Jan-2013 (CT) Use `.E_Type.primary_ais`, not `.primary_ais`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr.Kind
import _MOM._Attr.Manager
import _MOM._Attr.Spec
import _MOM._Attr.Type

import _MOM._Meta.M_Entity

import _MOM._Pred.Kind
import _MOM._Pred.Manager
import _MOM._Pred.Spec
import _MOM._Pred.Type

import _MOM._SCM.Change

from   _MOM._Attr.Type import *
from   _MOM._Attr      import Attr
from   _MOM._Pred      import Pred

import _TFL._Meta.Once_Property
import _TFL.Decorator
import _TFL.defaultdict
import _TFL.Sorted_By

from   _TFL.I18N             import _, _T, _Tn
from   _TFL.object_globals   import object_globals
from   _TFL.predicate        import paired

import itertools
import logging
import traceback

class Entity (TFL.Meta.Object) :
    """Internal root class for MOM entities with and without identity."""

    __metaclass__         = MOM.Meta.M_Entity

    PNS                   = MOM

    deprecated_attr_names = {}
    electric              = False
    init_finished         = False
    is_partial            = True
    is_relevant           = False
    is_used               = True
    polymorphic_epk       = False  ### Set by meta machinery
    polymorphic_epks      = False  ### Set by meta machinery
    relevant_root         = None   ### Set by meta machinery
    show_in_ui            = True   ### Modified by meta machinery
    show_package_prefix   = False  ### Include `PNS` in `ui_name` ???
    ui_display_sep        = ", "
    x_locked              = False

    _app_globals          = {}
    _dicts_to_combine     = ("deprecated_attr_names", )
    _home_scope           = None

    class _Attributes (MOM.Attr.Spec) :

        class FO (A_Blob) :
            """`FO.foo` gives the `ui_display` of attribute `foo`, if defined,
               or the raw value of `foo`, otherwise.
            """

            kind               = Attr.Auto_Cached

            def computed (self, obj) :
                return obj._FO_ (obj)
            # end def computed

        # end class FO

        class ui_display (A_String) :
            """Display in user interface"""

            kind               = Attr.Computed

            def computed (self, obj) :
                return obj.ui_display_format % obj.FO
            # end def computed

        # end class ui_display

    # end class _Attributes

    class _Predicates (MOM.Pred.Spec) :
        pass
    # end class _Predicates

    class _FO_ (TFL.Meta.Object) :
        """Formatter for attributes of object."""

        undefined = object ()

        def __init__ (self, obj) :
            self.__obj = obj
        # end def __init__

        def __call__ (self, name, value = undefined) :
            getter   = getattr (TFL.Getter, name)
            obj      = self.__obj
            try :
                if "." in name :
                    obj, attr = self._get_nested_attr (obj, name)
                else :
                    attr = getattr (obj.__class__, name)
            except AttributeError :
                result = repr (getter (obj))
            else :
                if isinstance (attr, MOM.Attr.Kind) :
                    if value is self.undefined :
                        value   = attr.get_value (obj)
                        get_raw = lambda : attr.get_raw  (obj)
                    else :
                        def get_raw () :
                            result = attr.attr.as_string (value)
                            if isinstance (value, basestring) :
                                result = repr (result)
                                if result.startswith (("u'", 'u"')) :
                                    result = result [1:]
                            elif result == "" :
                                result = "None"
                            return result
                    if isinstance (value, Entity) :
                        return value.FO
                    else :
                        uid = getattr (value, "ui_display", None)
                        if uid :
                            result = uid
                        else :
                            result = get_raw ()
                else :
                    if value is self.undefined :
                        ### Nested attributes need `self.__obj` here
                        result = repr (getter (self.__obj))
                    else :
                        result = value
            return result
        # end def __call__

        def _get_nested_attr (self, obj, name) :
            names = name.split (".")
            p     = names [0]
            attr  = getattr (obj.__class__, p)
            for n in names [1:] :
                obj  = getattr (obj, p)
                cls  = obj.__class__
                attr = getattr (cls, n)
                p    = n
            return obj, attr
        # end def _get_nested_attr

        def __getattr__ (self, name) :
            result = self (name)
            if "." not in name :
                setattr (self, name, result)
            return result
        # end def __getattr__

        def __getitem__ (self, key) :
            try :
                return self.__getattr__ (key)
            except AttributeError :
                raise KeyError (key)
        # end def __getitem__

        def __str__ (self) :
            return TFL.I18N.encode_o (unicode (self))
        # end def __str__

        def __unicode__ (self) :
            return self.__obj.ui_display
        # end def __unicode__

    # end class _FO_

    @property
    def home_scope (self) :
        return self._home_scope or MOM.Scope.active
    # end def home_scope

    @home_scope.setter
    def home_scope (self, value) :
        self._home_scope = value
    # end def home_scope

    @property
    def raw_attr_dict (self) :
        return dict \
            (  (a.name, a.get_raw (self))
            for a in self.user_attr if a.has_substance (self)
            )
    # end def raw_attr_dict

    @property
    def recordable_attrs (self) :
        return self.__class__.m_recordable_attrs
    # end def recordable_attrs

    def __new__ (cls, * args, ** kw) :
        if cls.is_partial :
            raise MOM.Error.Partial_Type (_T (cls.ui_name))
        result = super (Entity, cls).__new__ (cls)
        result._home_scope = kw.get ("scope")
        result._init_meta_attrs ()
        return result
    # end def __new__

    def __init__ (self, * args, ** kw) :
        self._init_attributes ()
        kw.pop                ("scope", None)
        self._main__init__    (* args, ** kw)
    # end def __init__

    @classmethod
    def from_attr_pickle_cargo (cls, scope, cargo) :
        result = cls.__new__    (cls, scope = scope)
        result._init_attributes ()
        result.set_pickle_cargo (cargo)
        return result
    # end def from_attr_pickle_cargo

    ### provide read-only access to this class' __init__
    _MOM_Entity__init__ = property (lambda self, __init__ = __init__ : __init__)

    def after_init (self) :
        pass
    # end def after_init

    def as_attr_pickle_cargo (self) :
        return dict \
            (   (a.name, a.get_pickle_cargo  (self))
            for a in self.attributes.itervalues () if a.to_save (self)
            )
    # end def as_attr_pickle_cargo

    def as_code (self) :
        return "%s (%s)" % (self.type_name, self.attr_as_code ())
    # end def as_code

    def attr_as_code (self) :
        uai = self.user_attr_iter ()
        return ", ".join ("%s = %s" % (a.name, a.as_code (v)) for (a, v) in uai)
    # end def attr_as_code

    def attr_value_maybe (self, name) :
        attr = self.attributes.get (name)
        if attr :
            return attr.get_value (self)
    # end def attr_value_maybe

    def compute_defaults_internal (self) :
        """Compute default values for optional/internal/cached parameters."""
        pass
    # end def compute_defaults_internal

    @classmethod
    def compute_type_defaults_internal (cls) :
        pass
    # end def compute_type_defaults_internal

    @TFL.Meta.Class_and_Instance_Method
    def cooked_attrs (soc, kw, on_error = None) :
        attributes = soc.attributes
        result     = {}
        if on_error is None :
            on_error = soc._raise_attr_error
        for name, value in kw.iteritems () :
            attr = attributes.get (name)
            if attr :
                try :
                    try :
                        result [name] = attr.from_string (value)
                    except MOM.Error.Attribute_Value as exc :
                        raise
                    except (TypeError, ValueError) as exc :
                        raise MOM.Error.Attribute_Value \
                            (soc, name, value, attr.kind, exc)
                except Exception as exc :
                    on_error (exc)
        return result
    # end def cooked_attrs

    def globals (self) :
        return self.__class__._app_globals or object_globals (self)
    # end def globals

    def has_substance (self) :
        """TRUE if there is at least one attribute with a non-default value."""
        return any (a.has_substance (self) for a in self.user_attr)
    # end def has_substance

    def is_correct (self, attr_dict = {}, _kind = "object")  :
        ews = self._pred_man.check_kind (_kind, self, attr_dict)
        return not ews
    # end def is_correct

    def raw_attr (self, name) :
        """Returns the raw value of attribute `name`, i.e., the value entered
           by the user into the object editor.
        """
        attr = self.attributes.get (name)
        if attr :
            return attr.get_raw (self) or u""
    # end def raw_attr

    def record_attr_change (self, kw) :
        if kw and self._home_scope and not self.electric :
            self.home_scope.record_change (self.SCM_Change_Attr, self, kw)
    # end def record_attr_change

    def reload_from_pickle_cargo (self, cargo) :
        self.init_finished  = False
        self._init_pending  = []
        self._init_attributes ()
        self.set_pickle_cargo (cargo)
        self._finish__init__  ()
    # end def reload_from_pickle_cargo

    def reset_syncable (self) :
        self._attr_man.reset_syncable ()
    # end def reset_syncable

    def set (self, on_error = None, ** kw) :
        """Set attributes specified in `kw` from cooked values"""
        assert "raw" not in kw
        gen = \
            (   (name, attr.get_raw_pid (self))
            for attr, name, value in self._record_iter (kw)
            if  attr.get_value (self) != value
            )
        with self._record_context (gen, self.SCM_Change_Attr) :
            return self._set_ckd (on_error, ** kw)
    # end def set

    def set_attr_iter (self, attr_dict, on_error = None) :
        attributes = self.attributes
        if on_error is None :
            on_error = self._raise_attr_error
        for name, val in attr_dict.iteritems () :
            cnam = self.deprecated_attr_names.get (name, name)
            attr = attributes.get (cnam)
            if attr :
                if not attr.is_settable :
                    on_error \
                        (MOM.Error.Attribute_Set (self, name, val, attr.kind))
                else :
                    yield (cnam, val, attr)
            elif name != "raw" :
                on_error (MOM.Error.Attribute_Unknown (self, name, val))
    # end def set_attr_iter

    def set_pickle_cargo (self, cargo) :
        attr_get = self.attributes.get
        for k, v in cargo.iteritems () :
            attr = attr_get (k)
            ### XXX Add legacy lifting
            if attr :
                attr.set_pickle_cargo  (self, v)
    # end def set_pickle_cargo

    def set_raw (self, on_error = None, ** kw) :
        """Set attributes specified in `kw` from raw values"""
        assert "raw" not in kw
        gen = \
            (   (name, raw_pid)
            for attr, name, value, raw, raw_pid in self._record_iter_raw (kw)
            if  raw != value
            )
        with self._record_context (gen, self.SCM_Change_Attr) :
            return self._set_raw (on_error, ** kw)
    # end def set_raw

    def sync_attributes (self) :
        """Synchronizes all user attributes with the values from
           _raw_attr and all sync-cached attributes.
        """
        self._attr_man.sync_attributes (self)
    # end def sync_attributes

    def user_attr_iter (self) :
        user_attr = self.user_attr
        return ((a, a.get_value (self)) for a in user_attr if a.to_save (self))
    # end def user_attr_iter

    def _finish__init__ (self) :
        """Redefine this to perform additional initialization."""
        assert not self.init_finished
        self.init_finished = True
        for ip in self._init_pending :
            ip ()
        try :
            del self._init_pending
        except AttributeError :
            pass
    # end def _finish__init__

    def _init_attributes (self) :
        self._attr_man.reset_attributes (self)
    # end def _init_attributes_

    def _init_meta_attrs (self) :
        self._init_pending = []
        self._attr_man     = MOM.Attr.Manager (self._Attributes)
        self._pred_man     = MOM.Pred.Manager (self._Predicates)
    # end def _init_meta_attrs

    def _kw_check_required (self, * args, ** kw) :
        needed  = tuple (m.name for m in self.required)
        missing = tuple (k for k in needed if k not in kw)
        if missing :
            on_error   = kw.pop ("on_error", self._raise_attr_error)
            all_needed = tuple (m.name for m in self.primary_required) + needed
            error = MOM.Error.Required_Missing \
                (self.__class__, all_needed, missing, args, kw)
            on_error (error)
            raise error
    # end def _kw_check_required

    def _kw_check_predicates (self, _kind = "object", on_error = None, ** kw) :
        result = self.is_correct (kw, _kind)
        if not result :
            errors = self._pred_man.errors [_kind]
            if on_error is None :
                on_error = self._raise_attr_error
            on_error (MOM.Error.Invariants (errors))
        return result
    # end def _kw_check_predicates

    def _kw_raw_check_predicates (self, on_error = None, ** kw) :
        ckd_kw = {}
        to_do  = []
        if on_error is None :
            on_error = self._raise_attr_error
        for name, val, attr in self.set_attr_iter (kw, on_error) :
            if val is not None :
                try :
                    ckd_kw [name] = ckd_val = attr.from_string (val, self)
                except MOM.Error.Attribute_Value as exc :
                    on_error (exc)
                    to_do.append ((attr, u"", None))
                except (TypeError, ValueError) as exc :
                    on_error \
                        ( MOM.Error.Attribute_Value
                            (self, name, val, attr.kind, exc)
                        )
                    if __debug__ :
                        logging.exception  \
                            ( "\n    %s %s, attribute conversion error "
                              "%s: %s [%s]"
                            , self.type_name, self, name, val, type (val)
                            )
                    to_do.append ((attr, u"", None))
                except StandardError as exc :
                    if 0:
                        logging.exception \
                        ( "\n    %s %s, attribute conversion error %s: %s [%s]"
                        , self.type_name, self, name, val, type (val)
                        )
                else :
                    to_do.append ((attr, val, ckd_val))
            else :
                to_do.append ((attr, u"", None))
        result = self._kw_check_predicates (on_error = on_error, ** ckd_kw)
        return result, to_do
    # end def _kw_raw_check_predicates

    def _print_attr_err (self, exc) :
        if debug:
            logging.exception (repr (self))
        print (self, exc)
    # end def _print_attr_err

    @TFL.Meta.Class_and_Instance_Method
    def _raise_attr_error (soc, exc) :
        raise exc
    # end def _raise_attr_error

    @TFL.Contextmanager
    def _record_context (self, gen, Change) :
        if not self._home_scope :
            yield
        else :
            rvr = dict (gen)
            yield rvr
            if rvr :
                self.home_scope.record_change (Change, self, rvr)
    # end def _record_context

    def _record_iter (self, kw) :
        e_type     = self.__class__
        recordable = self.recordable_attrs
        for name, value in kw.iteritems () :
            attr = getattr (e_type, name, None)
            if attr in recordable :
                yield attr, attr.name, value
    # end def _record_iter

    def _record_iter_raw (self, kw) :
        for a, name, value in self._record_iter (kw) :
            yield a, name, value, a.get_raw (self), a.get_raw_pid (self)
    # end def _record_iter_raw

    def _set_ckd (self, on_error = None, ** kw) :
        man = self._attr_man
        tc  = man.total_changes
        man.reset_pending ()
        if kw :
            if self._kw_check_predicates (on_error = on_error, ** kw) :
                for name, val, attr in self.set_attr_iter (kw, on_error) :
                    attr._set_cooked (self, val)
        if man.updates_pending :
            try :
                man.do_updates_pending (self)
            except Exception :
                pass
        return man.total_changes - tc
    # end def _set_ckd

    def _set_raw (self, on_error = None, ** kw) :
        man = self._attr_man
        tc  = man.total_changes
        if kw :
            is_correct, to_do = self._kw_raw_check_predicates \
                (on_error = on_error, ** kw)
            man.reset_pending ()
            if is_correct :
                for attr, raw_val, val in to_do :
                    attr._set_raw (self, raw_val, val)
        if man.updates_pending :
            man.do_updates_pending (self)
        return man.total_changes - tc
    # end def _set_raw

    def _store_attr_error (self, exc) :
        logging.exception ("Setting attribute failed with exception")
        if self._home_scope :
            self.home_scope._attr_errors.append (exc)
    # end def _store_attr_error

    def __getattr__ (self, name) :
        ### just to ease up-chaining in descendents
        raise AttributeError ("%r <%s>" % (name, self.type_name))
    # end def __getattr__

    def __ne__ (self, rhs) :
        return not (self == rhs)
    # end def __ne__

    def __repr__ (self) :
        try :
            return TFL.I18N.encode_o (self._repr (self.type_name))
        except AttributeError :
            return "<%s Incomplete>" % (_T (self.ui_name), )
    # end def __repr__

    def __str__ (self) :
        return TFL.I18N.encode_o (unicode (self))
    # end def __str__

# end class Entity

class An_Entity (Entity) :
    """Root class for anonymous entities without identity."""

    __metaclass__         = MOM.Meta.M_An_Entity

    is_partial            = True
    is_primary            = False
    owner                 = None
    attr_name             = None

    @property
    def ui_display_format (self) :
        return self.ui_display_sep.join \
            ( "%%(%s)s" % a.name for a in self.sig_attr
            if a.has_substance (self)
            )
    # end def ui_display_format

    @property
    def hash_key (self) :
        return tuple (a.get_hash (self) for a in self.hash_sig)
    # end def hash_key

    @property
    def SCM_Change_Attr (self) :
        return MOM.SCM.Change.Attr_Composite
    # end def SCM_Change_Attr

    def as_pickle_cargo (self) :
        return (str (self.type_name), self.as_attr_pickle_cargo ())
    # end def as_pickle_cargo

    def as_string (self) :
        return tuple (sorted (self.raw_attr_dict.iteritems ()))
    # end def as_string

    def attr_as_code (self) :
        attrs  = self.attr_tuple_to_save ()
        values = tuple (a.as_code (a.get_value (self)) for a in attrs)
        if len (values) == 1 :
            ### trailing comma for single element tuple
            values += ("", )
        result = ", ".join ("%s" % (v, ) for v in values)
        return result
    # end def attr_as_code

    def attr_tuple_to_save (self) :
        result  = self.user_attr
        save_p  = tuple (a.to_save (self) for a in result) [::-1]
        to_drop = tuple (itertools.takewhile ((lambda x : not x), save_p))
        if to_drop :
            ### drop trailing attributes that don't need to be saved
            result = result [: -len (to_drop)]
        return result
    # end def attr_tuple_to_save

    def copy (self, ** kw) :
        scope  = kw.pop  ("scope", self.home_scope)
        etype  = scope.entity_type (self.type_name)
        result = etype             (scope = scope, ** kw)
        raw_kw = dict \
            (  (a.name, a.get_raw (self))
            for a in self.user_attr if a.name not in kw
            )
        if raw_kw :
            result.set_raw (** raw_kw)
        return result
    # end def copy

    @classmethod
    def example_attrs (cls, full = False) :
        attrs = cls.user_attr if full else cls.required
        return dict ((a.name, a.example) for a in attrs)
    # end def example_attrs

    @property
    def owner_attr (self) :
        """Return the attribute (kind property) of the `owner` object that
           holds `self`.
        """
        if self.owner and self.attr_name :
            return getattr (self.owner.__class__, self.attr_name, None)
    # end def owner_attr

    def set (self, on_error = None, ** kw) :
        owner_attr = self.owner_attr
        if owner_attr is None or self.electric or not owner_attr.record_changes :
            return self._set_ckd (on_error, ** kw)
        elif owner_attr and owner_attr.is_primary :
            ### Change in primary attribute might be a `rename`
            return self.owner.set (** {self.attr_name : self.copy (** kw)})
        else :
            return self.__super.set (on_error, ** kw)
    # end def set

    def set_raw (self, on_error = None, ** kw) :
        owner_attr = self.owner_attr
        if owner_attr is None or self.electric or not owner_attr.record_changes :
            return self._set_raw (on_error, ** kw)
        elif owner_attr and owner_attr.is_primary :
            ### Change in primary attribute might be a `rename`
            return self.owner.set \
                (** {self.attr_name : self.copy (raw = True, ** kw)})
        else :
            return self.__super.set_raw (on_error, ** kw)
    # end def set_raw

    def _init_attributes (self) :
        self.owner = None
        self.__super._init_attributes ()
    # end def _init_attributes_

    def _main__init__ (self, * args, ** kw) :
        skw = self.signified (* args, ** kw)
        raw = bool (skw.pop ("raw", False))
        self._kw_check_required (* args, ** skw)
        if skw :
            set = self._set_raw if raw else self._set_ckd
            set (** skw)
    # end def _main__init__

    def _repr (self, type_name) :
        return u"%s (%s)" % (type_name, self.attr_as_code ().rstrip (", "))
    # end def _repr

    def __eq__ (self, rhs) :
        rhs = getattr (rhs, "hash_key", rhs)
        return self.hash_key == rhs
    # end def __eq__

    def __hash__ (self) :
        return hash (self.hash_key)
    # end def __hash__

    def __nonzero__ (self) :
        return self.has_substance ()
    # end def __nonzero__

    def __unicode__ (self) :
        return u"(%s)" % (self.attr_as_code ())
    # end def __unicode__

# end class An_Entity

@TFL.Add_To_Class ("P_Type", _A_Id_Entity_)
class Id_Entity (Entity) :
    """Internal root class for MOM entities with identity, i.e.,
       objects and links.
    """

    __metaclass__         = MOM.Meta.M_Id_Entity

    is_partial            = True
    max_count             = 0
    pid                   = None  ### set by `scope.ems.add`
    record_changes        = True
    refuse_links          = set ()
    sorted_by             = TFL.Meta.Alias_Property ("sorted_by_epk")
    tutorial              = None

    _sets_to_combine      = ("refuse_links", )

    class _Attributes (Entity._Attributes) :

        class created_by (A_Id_Entity) :
            """User that created the entity"""

            kind               = Attr.Computed
            P_Type             = "MOM.Id_Entity"

            def computed (self, obj) :
                cc = obj.creation_change
                if cc is not None :
                    try :
                        return obj.home_scope.pid_query (cc.c_user)
                    except Exception :
                        pass
            # end def computed

        # end class created_by

        class creation_change (A_Blob) :
            """Last change of the object"""

            kind               = Attr.Computed

            def computed (self, obj) :
                try :
                    return obj.changes ().order_by \
                        (TFL.Sorted_By ("cid")).first ()
                except IndexError :
                    pass
            # end def computed

        # end class creation_change

        class creation_date (A_Date_Time) :
            """Date/time of creation."""

            kind               = Attr.Computed

            def computed (self, obj) :
                cc = obj.creation_change
                if cc is not None :
                    return cc.c_time
            # end def computed

        # end class creation_date

        class electric (A_Boolean) :
            """Indicates if object/link was created automatically or not."""

            kind          = Attr.Internal
            Kind_Mixins   = (Attr.Init_Only_Mixin, )
            default       = False
            hidden        = True

        # end class electric

        class is_used (A_Int) :
            """Specifies whether entity is used by another entity."""

            kind          = Attr.Cached
            default       = 1

        # end class is_used

        class last_change (A_Blob) :
            """Last change of the object"""

            kind               = Attr.Computed

            def computed (self, obj) :
                try :
                    return obj.changes ().order_by \
                        (TFL.Sorted_By ("-cid")).first ()
                except IndexError :
                    pass
            # end def computed

        # end class last_change

        class last_changed (A_Date_Time) :
            """Date/time of last change."""

            kind               = Attr.Computed

            def computed (self, obj) :
                lc = obj.last_change
                if lc is not None :
                    return lc.time
            # end def computed

        # end class last_changed

        class last_changed_by (A_Id_Entity) :
            """User that applied the last change."""

            kind               = Attr.Computed
            P_Type             = "MOM.Id_Entity"

            def computed (self, obj) :
                lc = obj.last_change
                if lc is not None :
                    try :
                        return obj.home_scope.pid_query (lc.user)
                    except Exception :
                        pass
            # end def computed

        # end class last_changed_by

        class last_cid (A_Int) :
            """Change id of last change for this entity."""

            kind               = Attr.Internal
            default            = 0
            record_changes     = False

        # end class last_cid

        class x_locked (A_Boolean) :
            """Specifies if object can be changed by user"""

            kind          = Attr.Internal
            default       = False
            hidden        = True

        # end class x_locked

    # end class _Attributes

    class _Predicates (Entity._Predicates) :

        class completely_defined (Pred.Condition) :
            """All necessary attributes must be defined."""

            kind          = Pred.System
            guard         = "is_used"
            guard_attr    = ("is_used", )

            def eval_condition (self, obj, glob_dict, val_dict) :
                result = []
                add    = result.append
                for a in obj.necessary :
                    if not a.has_substance (obj) :
                        m = _T ("Necessary attribute %s is not defined") % (a, )
                        add (m)
                self._error_info.extend (result)
                return not result
            # end def eval_condition

        # end class completely_defined

        class object_correct (Pred.Condition) :
            """All object invariants must be satisfied."""

            kind          = Pred.System

            def eval_condition (self, obj, glob_dict, val_dict) :
                result = []
                add    = result.append
                for p in obj._pred_man.errors ["object"] :
                    add (str (p))
                self._error_info.extend (result)
                return not result
            # end def eval_condition

        # end class object_correct

    # end class _Predicates

    @TFL.Meta.Once_Property
    def ETM (self) :
        return self.home_scope [self.type_name]
    # end def ETM

    @TFL.Meta.Once_Property
    def epk (self) :
        """Essential primary key"""
        return tuple \
            (a.get_value (self) for a in self.primary) + (self.type_name,)
    # end def epk

    @property
    def epk_as_code (self) :
        def _conv (tup) :
            if len (tup) == 1 :
                tup += ("", )
            for t in tup :
                if isinstance (t, tuple) :
                    if len (t) == 1 :
                        t += ("", )
                    t = "(%s)" % (", ".join (_conv (t)))
                yield t
        def _gen () :
            for a in self.primary :
                r = a.as_code (a.get_value (self))
                if isinstance (r, tuple) :
                    r = "(%s)" % (", ".join (_conv (r)))
                yield r
        try :
            result = tuple (_gen ())
        except Exception :
            result = "..."
        return result
    # end def epk_as_code

    @TFL.Meta.Once_Property
    def epk_as_dict (self) :
        return dict (zip (self.epk_sig, self.epk))
    # end def epk_as_dict

    @property
    def epk_raw (self) :
        """Essential primary key as raw values"""
        return \
            ( tuple (a.get_raw_epk (self) for a in self.primary)
            + (self.type_name, )
            )
    # end def epk_raw

    @property
    def epk_raw_pid (self) :
        """Essential primary key as raw values (pids for Id_Entity attributes)."""
        return \
            ( tuple (a.get_raw_pid (self) for a in self.primary)
            + (self.type_name, )
            )
    # end def epk_raw

    @property
    def errors (self) :
        return iter (self._pred_man)
    # end def errors

    @property
    def has_errors (self) :
        return self._pred_man.has_errors
    # end def has_errors

    @property
    def has_warnings (self) :
        return self._pred_man.has_warnings
    # end def has_warnings

    @property
    def SCM_Change_Attr (self) :
        return MOM.SCM.Change.Attr
    # end def SCM_Change_Attr

    @property
    def tn_pid (self) :
        return (self.type_name, self.pid)
    # end def tn_pid

    @property
    def ui_display_format (self) :
        return self.ui_display_sep.join \
            ( "%%(%s)s" % a.name for (a, v) in zip (self.primary, self.epk)
              if a.has_substance (self)
            )
    # end def ui_display_format

    def all_links (self) :
        return sorted \
            ( self.all_referrers ()
            , key = self.home_scope.MOM.Id_Entity.sort_key_pm ()
            )
    # end def all_links

    def all_referrers (self) :
        """Return query set of all entities that refer to `self`."""
        scope = self.home_scope
        def _gen (self, ref_map, scope) :
            pid = self.pid
            for ET, attrs in ref_map.iteritems () :
                qfs = tuple ((getattr (Q, a) == pid) for a in attrs)
                ETM = scope [ET.type_name]
                yield ETM.query (Q.OR (* qfs)).distinct ()
        return scope.ems.Q_Result_Composite \
            ( tuple (_gen (self, self.__class__.Ref_Req_Map, scope))
            + tuple (_gen (self, self.__class__.Ref_Opt_Map, scope))
            )
    # end def all_referrers

    def async_changes (self, * filter, ** kw) :
        result = self.home_scope.async_changes (pid = self.pid)
        if filters or kw :
            result = result.filter (* filters, ** kw)
        return result
    # end def async_changes

    def as_pickle_cargo (self) :
        return (str (self.type_name), self.as_attr_pickle_cargo (), self.pid)
    # end def as_pickle_cargo

    def attr_as_code (self) :
        result = ", ".join (self.epk_as_code + (self.__super.attr_as_code (), ))
        if "," not in result :
            result += ","
        return result
    # end def attr_as_code

    def changes (self, * filters, ** kw) :
        """Return change objects related to `self`."""
        result = self.home_scope.query_changes (pid = self.pid)
        if filters or kw :
            result = result.filter (* filters, ** kw)
        return result
    # end def changes

    def check_all (self) :
        """Checks all predicates"""
        return self._pred_man.check_all (self)
    # end def check_all

    def copy (self, * new_epk, ** kw) :
        """Make copy with primary key `new_epk`."""
        scope  = self.home_scope
        etype  = self.__class__
        result = etype (* new_epk, scope = scope, ** kw)
        with scope.nested_change_recorder \
                 (MOM.SCM.Change.Copy, result) as change :
            scope.add (result)
            change.pid = result.pid
            raw_kw     = dict \
                (  (a.name, a.get_raw (self))
                for a in self.user_attr if a.name not in kw and a.to_save (self)
                )
            if raw_kw :
                result.set_raw (** raw_kw)
        return result
    # end def copy

    def correct_unknown_attr (self, error) :
        """Try to correct an unknown attribute error."""
        pass
    # end def correct_unknown_attr

    def destroy (self) :
        """Remove entity from `home_scope`."""
        if self._home_scope :
            if self is self.home_scope.root :
                self.home_scope.destroy ()
            else :
                self.home_scope.remove (self)
    # end def destroy

    def destroy_dependency (self, other) :
        for attr in self.object_referring_attributes.pop (other, ()) :
            if attr.is_required :
                self.destroy ()
            elif attr.is_primary :
                ### resetting a primary attribute means a rename operation
                self.set (** {attr.name : None})
            else :
                old = attr.get_value   (self)
                raw = attr.get_raw_pid (self)
                attr.reset (self)
                if old != attr.get_value (self) :
                    self.record_attr_change ({attr.name : raw})
        if self and other in self.dependencies :
            del self.dependencies [other]
    # end def destroy_dependency

    @classmethod
    def example_attrs (cls, full = False) :
        attrs = itertools.chain \
            (cls.primary, cls.user_attr if full else cls.required)
        return dict ((a.name, a.example) for a in attrs)
    # end def example_attrs

    @classmethod
    def epkified (cls, * epk, ** kw) :
        if epk and isinstance (epk [-1], cls.Type_Name_Type) :
            epk  = epk [:-1]
        raw      = bool (kw.get ("raw", False))
        epkifier = (cls.epkified_ckd, cls.epkified_raw) [raw]
            ### `epkified_ckd` and `epkified_raw` are created by meta machinery
        try :
            return epkifier (* epk, ** kw)
        except TypeError, exc :
            on_error = kw.pop ("on_error", cls._raise_attr_error)
            needed   = tuple (m.name for m in cls.primary_required)
            missing  = tuple (p for p in needed [len (epk):] if p not in kw)
            if missing :
                error = MOM.Error.Required_Missing \
                    (cls, needed, missing, epk, kw, "primary")
                on_error (error)
                raise error
            else :
                raise TypeError \
                    ( _T ("%s needs the arguments %s, got %s instead")
                    % (_T (cls.ui_name), needed, epk)
                    )
    # end def epkified

    def is_defined (self)  :
        return \
            (  (not self.is_used)
            or all (a.has_substance (self) for a in self.necessary)
            )
    # end def is_defined

    def is_g_correct (self)  :
        ews = self._pred_man.check_kind ("system", self)
        return not ews
    # end def is_g_correct

    @TFL.Meta.Class_and_Instance_Method
    def is_locked (soc) :
        if isinstance (soc, Entity) :
            return soc.x_locked or soc.electric
        else :
            return soc.x_locked.default or soc.electric.default
    # end def is_locked

    def notify_dependencies_destroy (self) :
        """Notify all entities registered in `self.dependencies` and
           `self.object_referring_attributes` about the destruction of `self`.
        """
        ### Use `list` because dictionaries are changed inside loop
        for d in list (self.dependencies) :
            d.destroy_dependency (self)
        for o in list (self.object_referring_attributes) :
            o.destroy_dependency (self)
    # end def notify_dependencies_destroy

    def register_dependency (self, other) :
        """Register that `other` depends on `self`"""
        self.dependencies [other] += 1
    # end def register_dependency

    def restore (self, * epk, ** kw) :
        """Restore an object that was destroyed before but not committed."""
        if not (self.pid and self.home_scope) :
            raise TypeError \
                ("%r: pid %r, scope %r" % (self, self.pid, self.home_scope))
        self.init_finished  = False
        self._init_pending  = []
        self.__init__         (* epk, ** kw)
        self.home_scope.add   (self, pid = self.pid)
        return self
    # end def restore

    def unregister_dependency (self, other) :
        """Unregister dependency of `other` on `self`"""
        deps = self.dependencies
        deps [other] -= 1
        if deps [other] <= 0 :
            del deps [other]
    # end def unregister_dependency

    def user_diff (self, other, ignore = ()) :
        """Return differences in user attributes between `self` and `other`."""
        result = {}
        undef  = object ()
        if ignore :
            ignore = set (ignore)
        if self.type_name != other.type_name :
            result ["type_name"] = (self.type_name, other.type_name)
        pc_s = self.as_attr_pickle_cargo  ()
        pc_o = other.as_attr_pickle_cargo ()
        for k in set (pc_s).union (pc_o) :
            if k in ignore :
                continue
            p = pc_s.get (k, undef)
            q = pc_o.get (k, undef)
            if p != q :
                result [k] = \
                    ( p if p is not undef else "<Missing>"
                    , q if q is not undef else "<Missing>"
                    )
        return result
    # end def user_diff

    def user_equal (self, other) :
        """Compare `self` and `other` concerning user attributes."""
        return \
            (   self.type_name               == other.type_name
            and self.as_attr_pickle_cargo () == other.as_attr_pickle_cargo ()
            )
    # end def user_equal

    def _destroy (self) :
        self.notify_dependencies_destroy ()
    # end def _destroy

    def _extract_primary (self, kw) :
        result = {}
        for pka in self.primary :
            name      = pka.name
            role_name = getattr (pka, "role_name", None)
            if name in kw :
                result [name] = kw.pop (name)
            elif role_name and role_name in kw :
                result [name] = kw.pop (role_name)
        return result
    # end def _extract_primary

    def _extract_primary_ckd (self, kw) :
        new_epk  = []
        pkas_ckd = self._extract_primary (kw)
        pkas_raw = {}
        for pka in self.primary :
            name = pka.name
            if name in pkas_ckd :
                v = pkas_ckd [name]
                pkas_raw [name] = pka.as_string (v)
            else :
                v = getattr (self, name)
            new_epk.append (v)
        return new_epk, pkas_raw, pkas_ckd
    # end def _extract_primary_ckd

    def _extract_primary_raw (self, kw) :
        new_epk  = []
        pkas_ckd = {}
        pkas_raw = self._extract_primary (kw)
        for pka in self.primary :
            name = pka.name
            if name in pkas_raw :
                pkas_ckd [name] = v = pka.from_string (pkas_raw [name], self)
            else :
                v = getattr (self, name)
            new_epk.append (v)
        return new_epk, pkas_raw, pkas_ckd
    # end def _extract_primary_raw

    def _init_epk (self, epk) :
        return ((a.name, pka) for a, pka in zip (self.primary, epk))
    # end def _init_epk

    def _init_meta_attrs (self) :
        self.__super._init_meta_attrs ()
        self.dependencies                = TFL.defaultdict (int)
        self.object_referring_attributes = TFL.defaultdict (list)
    # end def _init_meta_attrs

    def _main__init__ (self, * epk, ** kw) :
        self.implicit = kw.pop ("implicit", False)
        raw           = bool (kw.pop ("raw", False))
        setter        = self.__super._set_raw if raw else self.__super._set_ckd
            ### Need to use `__super.` methods here because it's not a `rename`
        try :
            epk, kw = self.epkified (* epk, ** kw)
            self._kw_check_required (* epk, ** kw)
        except MOM.Error.Required_Missing as exc :
            self._pred_man.missing_required = exc
            kw.update (self._init_epk (epk))
            checker = \
                (  self._kw_raw_check_predicates
                if raw else self._kw_check_predicates
                )
            checker (** kw)
            raise MOM.Error.Invariants (self._pred_man)
        if self.E_Type.primary_ais :
            if epk [-1] is not None :
                raise TypeError \
                    ( "Cannot pass value for attribute `%s` of %s, got `%s`"
                    % (self.E_Type.primary_ais.name, self.type_name, epk [-1])
                    )
        kw.update (self._init_epk (epk))
        setter (** kw)
        required_errors = self._pred_man.required_errors
        if required_errors :
            raise MOM.Error.Invariants (self._pred_man)
    # end def _main__init__

    def _rename (self, new_epk, pkas_raw, pkas_ckd) :
        diffs = sum ((n != o) for n, o in paired (new_epk, self.epk [:-1]))
        if diffs :
            def _renamer () :
                attributes = self.attributes
                for k, v in pkas_ckd.iteritems () :
                    attr = attributes [k]
                    attr._set_cooked_inner (self, v)
                    attr._set_raw_inner    (self, pkas_raw [k], v)
                self._reset_epk ()
            self._kw_check_predicates (on_error = None, ** pkas_ckd)
            self.home_scope.rename    (self, tuple (new_epk), _renamer)
        return diffs
    # end def _rename

    def _repr (self, type_name) :
        return "%s (%s)" % (type_name, ", ".join (self.epk_as_code))
    # end def _repr

    def _reset_epk (self) :
        sd = self.__dict__
        for a in ("epk", "epk_as_dict") :
            if a in sd :
                delattr (self, a)
    # end def _reset_epk

    def _set_ckd (self, on_error = None, ** kw) :
        result = 0
        if kw :
            new_epk, pkas_raw, pkas_ckd = self._extract_primary_ckd (kw)
            if pkas_ckd :
                result += self._rename (new_epk, pkas_raw, pkas_ckd)
            result += self.__super._set_ckd (on_error, ** kw)
        return result
    # end def _set_ckd

    def _set_raw (self, on_error = None, ** kw) :
        result = 0
        if kw :
            new_epk, pkas_raw, pkas_ckd = self._extract_primary_raw (kw)
            if pkas_ckd :
                result += self._rename (new_epk, pkas_raw, pkas_ckd)
            result += self.__super._set_raw (on_error, ** kw)
        return result
    # end def _set_raw

    def __eq__ (self, rhs) :
        if isinstance (rhs, int) :
            return self.pid == rhs
        elif isinstance (rhs, basestring) :
            try :
                pid = int (rhs)
            except (ValueError, TypeError) :
                return False
            else :
                return self.pid == pid
        else :
            try :
                rhs = (rhs.pid, rhs.home_scope.guid)
            except AttributeError :
                pass
            return (self.pid, self.home_scope.guid) == rhs
    # end def __eq__

    def __hash__ (self) :
        return hash ((self.pid, self.home_scope.guid))
    # end def __hash__

    def __unicode__ (self) :
        epk = self.epk
        if len (epk) == 1 :
            format = u"%s"
        else :
            format = u"(%s)"
        return format % (", ".join (self.epk_as_code))
    # end def __unicode__

# end class Id_Entity

class _Id_Entity_Reload_Mixin_ (object) :
    """Mixin triggering a reload from the database on any attribute access."""

    def __getattribute__ (self, name) :
        if name in ("__class__", ) :
            return object.__getattribute__ (self, name)
        else :
            cls    = object.__getattribute__ (self, "__class__")
            reload = cls._RELOAD_INSTANCE
            e_type = cls._RESTORE_CLASS (self)
            reload (self, e_type)
            return getattr (self, name)
    # end def __getattribute__

    @classmethod
    def _RELOAD_INSTANCE (cls, self, e_type) :
        raise TypeError \
            ( "%s needs to implement _RELOAD_INSTANCE"
            % self.__class__.__bases__ [0]
            )
    # end def _RELOAD_INSTANCE

    @classmethod
    def _RESTORE_CLASS (cls, self) :
        result = self.__class__ = cls.__bases__ [2]
        return result
    # end def _RESTORE_CLASS

    @classmethod
    def define_e_type (cls, e_type, mixin) :
        e_type._RELOAD_E_TYPE = e_type.New \
            ( "_Reload"
            , head_mixins = (mixin, cls)
            )
    # end def define_e_type

# end class _Id_Entity_Reload_Mixin_

class _Id_Entity_Destroyed_Mixin_ (object) :
    """Mixin indicating an entity that was already destroyed."""

    def __getattribute__ (self, name) :
        if name in \
                ( "E_Type", "pid", "type_name"
                , "__class__", "__nonzero__", "__repr__"
                ) :
            return object.__getattribute__ (self, name)
        else :
            raise MOM.Error.Destroyed_Entity \
                ( "%r: access to attribute %r not allowed"
                % (self, name)
                )
    # end def __getattribute__

    @classmethod
    def define_e_type (cls, e_type) :
        e_type._DESTROYED_E_TYPE = type (cls) \
            (str (e_type.type_base_name + "_Destroyed"), (cls, e_type), {})
    # end def define_e_type

    def __nonzero__ (self) :
        return False
    # end def __nonzero__

    def __repr__ (self) :
        ### Need to reset `self.__class__` temporarily to get proper `__repr__`
        try :
            cls = self.__class__
            self.__class__ = cls.__bases__ [1]
            result = "<Destroyed entity %s>" % (self.__repr__ (), )
        finally :
            self.__class__ = cls
        return result
    # end def __repr__

# end class _Id_Entity_Destroyed_Mixin_

__doc__  = """
Class `MOM.Id_Entity`
=====================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Id_Entity

    `MOM.Id_Entity` provides the framework for defining essential classes and
    associations. Each essential class or association is characterized by

    - `essential attributes`_

    - `essential predicates`_

    - `class attributes`_

    - `methods`_

    Each instance of `Id_Entity` has a attribute :attr:`home_scope` that
    refers to the :class:`~_MOM.Scope.Scope` in which the instance lives.

    `Id_Entity` is normally not directly used as a base class. Instead,
    `Id_Entity`'s subclasses :class:`~_MOM.Object.Object` and
    :class:`~_MOM.Link.Link` serve as root classes for the hierarchies
    of essential classes and associations, respectively.

    .. _`essential attributes`:

    **Essential Attributes**

    Essential attributes are defined inside the class `_Attributes`
    that is nested in `Id_Entity` (or one of its derived classes).

    Any essential class derived (directly or indirectly) from `Id_Entity`
    needs to define a `_Attributes` class that's derived from its
    ancestors `_Attributes`. The top-most `_Attributes` class is
    derived from :class:`MOM.Attr.Spec<_MOM._Attr.Spec.Spec>`.

    Each essential attribute is defined by a class derived from one of
    the attribute types in :mod:`MOM.Attr.Type<_MOM._Attr.Type>`.

    `MOM.Id_Entity` defines a number of attributes that can be overriden by
    descendant classes:

    - electric

    - x_locked

    - is_used

    .. _`essential predicates`:

    **Essential Predicates**

    Essential predicates are defined inside the class `_Predicates` that
    is nested in `Id_Entity` (or one of its derived classes).

    Any essential class derived (directly or indirectly) from `Id_Entity`
    needs to define a `_Predicates` class that's derived from its
    ancestors `_Predicates`. The top-most `_Predicates` class is
    derived from :class:`MOM.Pred.Spec<_MOM._Pred.Spec.Spec>`.

    Each essential predicate is defined by a class derived from one of
    the predicate types in :mod:`MOM.Pred.Type<_MOM._Pred.Type>`.

    `MOM.Id_Entity` defines two predicates that should not be overriden by
    descendant classes:

    - completely_defined

    - object_correct

    Please note that these two predicates are *not* to be used as examples
    of how predicates should be defined. Normally, predicates define
    `assertion`, not `eval_condition`! This is explained in more detail in
    :mod:`MOM.Pred.Type<_MOM._Pred.Type>`.

    .. _`class attributes`:

    **Class Attributes**

    `MOM.Id_Entity` provides a number of class attributes that control various
    aspects of the use of an essential class by the framework.

    .. attribute:: default_child

      Specifies which child of a partial class should be used by the UI by
      default. The value of this attribute is set for the partial class by
      one specific derived class.

    .. attribute:: deprecated_attr_names

      This is a dictionary that maps deprecated names
      of attributes to the currently preferred names (this is used to
      allow the reading of older databases without loss of information).

    .. attribute:: home_scope

      The scope to which the entity belongs.

    .. attribute:: is_partial

      Specifies if objects/links can be created for the essential
      class in question.

      `is_partial` must be explicitly set to `True` for each essential
      class that doesn't allow the creation of objects or links. If
      `is_partial` isn't defined for a class, `False` is assumed.

    .. attribute:: max_count

      Restricts the number of instances that can be created.

    .. attribute:: PNS

      The package namespace in which this class is defined.

      Ideally, each package namespace defining essential classes defines a
      common root for these, e.g., `SPN.Entity`, that defines
      `PNS`, e.g., ::

          class _SPN_Entity_ (MOM.Id_Entity) :

              _real_name = "Entity"

              PNS = SPN
              ...

    .. attribute:: recordable_attrs

      Set of attributes stored in the database for the entity.

    .. attribute:: record_changes

      Changes of the entity will only be recorded if `record_changes` is True.

    .. attribute:: refuse_links

      This is a set of (names of) classes that must not be linked
      to instances of the essential class in question. This can be used if
      objects of a derived class should not participate in associations of
      a base class.

    .. attribute:: show_in_ui

      Class is shown in the UI only if `show_in_ui` is True.

      `show_in_ui` is not inherited --- it must be set to `False` for every single
      class that shouldn't be shown in the UI.

      The meta machinery modifies `show_in_ui` by combining it with
      `record_changes` and `not is_partial`.

    .. attribute:: show_package_prefix

      Specifies whether the class name should be prefixed by the name of
      the package namespace in the UI.

    .. attribute:: tutorial

      Describes why and how to define instances of the essential class and
      is used in step-by-step tutorials.

    .. _`methods`:

    **Methods**

    Descendents of `MOM.Id_Entity` can redefine a number of methods to
    influence how instances of the class are handled by the framework. If
    you redefine one of these methods, you'll normally need to call the
    `super` method somewhere in the redefinition.

    .. method:: after_init

      Is called by the GUI after an instance of the class was
      (successfully) created. `after_init` can create additional objects
      automatically to ease the life of the interactive user of the
      application.

    .. automethod:: all_referrers

    .. automethod:: changes

    .. method:: compute_defaults_internal

      Is called whenever object attributes
      needs to synchronized and can be used to set attributes to computed
      default values. Please note that it is better to use
      `compute_default` defined for a specific attribute than to compute that
      value in `compute_defaults_internal`.

      `compute_defaults_internal` should only be used when the default
      values for several different attributes need to be computed together.

    .. method:: compute_type_defaults_internal

      Is a class method that is called to
      compute a default value of an attribute that is based on all
      instances of the class. The value of such an attribute must be
      stored as a class attribute (or in the root object of the scope).

    .. automethod:: copy

    .. automethod:: destroy

    .. automethod:: set

    .. automethod:: set_raw

"""

if __name__ != "__main__" :
    MOM._Export ("*", "_Id_Entity_Reload_Mixin_", "_Id_Entity_Destroyed_Mixin_")
### __END__ MOM.Entity
