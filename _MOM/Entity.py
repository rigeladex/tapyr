# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2009 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

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
import _TFL.defaultdict
import _TFL.Sorted_By

from   _TFL.object_globals   import object_globals

import traceback

class Entity (TFL.Meta.Object) :
    """Internal root class for MOM entities with and without identity."""

    __metaclass__         = MOM.Meta.M_Entity

    Package_NS            = MOM

    deprecated_attr_names = {}
    electric              = False
    generate_doc          = True
    home_scope            = None
    is_partial            = True
    is_used               = True
    show_package_prefix   = False
    x_locked              = False

    _dicts_to_combine     = ("deprecated_attr_names", )

    _Class_Kind           = "Spec Essence"

    class _Attributes (MOM.Attr.Spec) :
        pass
    # end class _Attributes

    class _Predicates (MOM.Pred.Spec) :
        pass
    # end class _Predicates

    def __new__ (cls, * args, ** kw) :
        if cls.is_partial :
            raise MOM.Error.Partial_Type (cls.type_name)
        result = super (Entity, cls).__new__ (cls)
        if not result.home_scope :
            result.home_scope = kw.get ("scope", MOM.Scope.active)
        result._init_meta_attrs ()
        return result
    # end def __new__

    def __init__ (self, * args, ** kw) :
        self.dependencies = TFL.defaultdict  (int)
        self._init_attributes ()
        self._finish__init__  (* args, ** kw)
    # end def __init__

    def after_init (self) :
        pass
    # end def after_init

    def attr_value_maybe (self, name) :
        attr = self.attributes.get (name)
        if attr :
            return attr.get_value (self)
    # end def attr_value_maybe

    def globals (self) :
        return self.__class__._app_globals or object_globals (self)
    # end def globals

    def has_changed (self) :
        return self._attr_man.has_changed (self)
    # end def has_changed

    def has_substance (self) :
        """TRUE if there is at least one attribute with a non-default value."""
        return any (a.has_substance (self) for a in self.user_attr)
    # end def has_substance

    def is_correct (self, attr_dict = {})  :
        ews = self._pred_man.check_kind ("object", self, attr_dict)
        return not ews
    # end def is_correct

    def raw_attr (self, name) :
        """Returns the raw value of attribute `name`, i.e., the value entered
           by the user into the object editor.
        """
        attr = self.attributes.get (name)
        if attr :
            return attr.get_raw (self) or ""
    # end def raw_attr

    def reset_syncable (self) :
        self._attr_man.reset_syncable ()
    # end def reset_syncable

    def set (self, on_error = None, ** kw) :
        """Set attributes specified in `kw` from cooked values"""
        if not kw :
            return 0
        self._kw_satisfies_i_invariants (kw, on_error)
        self._set_record (kw)
        tc = self._attr_man.total_changes
        for name, val, attr in self.set_attr_iter (kw, on_error) :
            attr._set_cooked (self, val)
        return self._attr_man.total_changes - tc
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
                        ( MOM.Error.Invalid_Attribute
                            (self, name, val, attr.kind)
                        )
                else :
                    yield (cnam, val, attr)
            elif name != "raw" :
                on_error (MOM.Error.Unknown_Attribute (self, name, val))
    # end def set_attr_iter

    def set_raw (self, on_error = None, ** kw) :
        """Set attributes specified in `kw` from raw values"""
        if not kw :
            return 0
        tc = self._attr_man.total_changes
        if kw :
            cooked_kw = {}
            to_do     = []
            for name, val, attr in self.set_attr_iter (kw, on_error) :
                if val :
                    try :
                        cooked_kw [name] = cooked_val = \
                            attr.from_string (val, self)
                    except (ValueError, MOM.Error.Attribute_Syntax_Error), err:
                        print ("Warning: Error when setting attribute %s "
                               "of %r to %s\nClearing attribute"
                              ) % (attr.name, self, val)
                        self.home_scope._db_errors.append \
                            ( MOM.Error.Invalid_Attribute
                                (self, name, val, attr.kind)
                            )
                        if __debug__ :
                            print err
                        to_do.append ((attr, "", None))
                    except StandardError, exc :
                        print exc, \
                          ( "; object %s, attribute %s: %s [%s]"
                          % (self, name, val, type (val))
                          )
                        traceback.print_exc ()
                    else :
                        to_do.append ((attr, val, cooked_val))
                else :
                    to_do.append ((attr, "", None))
            self._kw_satisfies_i_invariants (cooked_kw, on_error)
            self._set_record (cooked_kw)
            self._attr_man.reset_pending ()
            for attr, raw_val, val in to_do :
                attr._set_raw (self, raw_val, val)
        return self._attr_man.total_changes - tc
    # end def set_raw

    def sync_attributes (self) :
        """Synchronizes all user attributes with the values from
           _raw_attr and all sync-cached attributes.
        """
        self._attr_man.sync_attributes (self)
    # end def sync_attributes

    def _finish__init__ (self, * args, ** kw) :
        self.implicit = kw.pop ("implicit", False)
        if kw :
            set = (self.set, self.set_raw) [bool (kw.pop ("raw", False))]
            set (** kw)
    # end def _finish__init__

    def _init_attributes (self) :
        self._attr_man.reset_attributes (self)
    # end def _init_attributes_

    def _init_meta_attrs (self) :
        self._attr_man  = MOM.Attr.Manager (self._Attributes)
        self._pred_man  = MOM.Pred.Manager (self._Predicates)
    # end def _init_meta_attrs

    def _kw_satisfies_i_invariants (self, attr_dict, on_error) :
        result = not self.is_correct (attr_dict)
        if result :
            errors = self._pred_man.errors ["object"]
            if on_error is None :
                on_error = self._raise_attr_error
            on_error (MOM.Error.Invariant_Errors (errors))
        return result
    # end def _kw_satisfies_i_invariants

    def _print_attr_err (self, exc) :
        print self, exc
    # end def _print_attr_err

    def _raise_attr_error (self, exc) :
        raise exc
    # end def _raise_attr_error

    def _set_record (self, kw) :
        pass
    # end def _set_record

    def _store_attr_error (self, exc) :
        self.home_scope._db_errors.append (exc)
    # end def _store_attr_error

    def __getattr__ (self, name) :
        ### just to ease up-chaining in descendents
        raise AttributeError ("%r <%s>" % (name, self.type_name))
    # end def __getattr__

    def __repr__ (self) :
        return self._repr (self.type_name)
    # end def __repr__

# end class Entity

class An_Entity (Entity) :
    """Root class for anonymous entities without identity."""

    __metaclass__         = MOM.Meta.M_An_Entity

    def _formatted_user_attr (self) :
        return ", ".join \
            ("%s = %s" % (a.name, a.get_raw (self)) for a in self.user_attr)
    # end def _formatted_user_attr

    def _repr (self, type_name) :
        return "%s (%s)" % (type_name, self._formatted_user_attr ())
    # end def _repr

    def __str__ (self) :
        return "(%s)" % (self._formatted_user_attr ())
    # end def __str__

# end class An_Entity

class Id_Entity (Entity) :
    """Internal root class for MOM entities with identity, i.e.,
       objects and links.
    """

    __metaclass__         = MOM.Meta.M_Id_Entity

    auto_display          = ()
    is_relevant           = False
    max_count             = 0
    rank                  = 0
    record_changes        = True
    refuse_links          = set ()
    relevant_root         = None   ### Set by meta machinery
    save_to_db            = True
    sorted_by             = TFL.Sorted_By ("epk")
    tutorial              = None

    _app_globals          = {}
    _lists_to_combine     = ("auto_display", )
    _sets_to_combine      = ("refuse_links", )

    class _Attributes (Entity._Attributes) :

        class electric (A_Boolean) :
            """Indicates if object/link was created automatically or not."""

            kind          = Attr.Internal
            default       = False
            hidden        = True

        # end class electric

        class x_locked (A_Boolean) :
            """Specifies if object can be changed by user"""

            kind          = Attr.Internal
            default       = False
            hidden        = True

        # end class x_locked

        class is_used (A_Int) :
            """Specifies whether entity is used by another entity."""

            kind          = Attr.Cached
            default       = 1

        # end class is_used

    # end class _Attributes

    class _Predicates (Entity._Predicates) :

        class completely_defined (Pred.Condition) :
            """All required attributes must be defined."""

            kind          = Pred.System
            guard         = "is_used"
            guard_attr    = ("is_used", )

            def eval_condition (self, obj, glob_dict, val_dict) :
                result = []
                add    = result.append
                for a in obj.required :
                    if not a.has_substance (obj) :
                        add ("Required attribute %s is not defined" % (a, ))
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
    def epk (self) :
        """Essential primary key"""
        return tuple (a.get_value (self) for a in self.primary)
    # end def epk

    @property
    def epk_as_code (self) :
        def _gen () :
            for a in self.primary :
                r = a.as_code (a.get_value (self))
                if isinstance (r, tuple) :
                    r = "(%s)" % (", ".join (r))
                yield r
        return tuple (_gen ())
    # end def epk_as_code

    @TFL.Meta.Once_Property
    def epk_as_dict (self) :
        return dict (zip (self.epk_sig, self.epk))
    # end def epk_as_dict

    @property
    def has_errors (self) :
        return self._pred_man.has_errors
    # end def has_errors

    @property
    def has_warnings (self) :
        return self._pred_man.has_warnings
    # end def has_warnings

    def check_all (self) :
        """Checks all predicates"""
        return self._pred_man.check_all (self)
    # end def check_all

    def compute_defaults_internal (self) :
        """Compute default values for optional/internal/cached parameters."""
        pass
    # end def compute_defaults_internal

    @classmethod
    def compute_type_defaults_internal (cls) :
        pass
    # end def compute_type_defaults_internal

    def copy (self, * new_epk, ** kw) :
        """Make copy with primary key `new_epk`."""
        new_obj = self.__class__ (* new_epk, ** kw)
        raw_kw  = dict \
            (  (a.name, a.get_raw (self))
            for a in self.user_attr if a.name not in kw
            )
        if raw_kw :
            new_obj.set_raw (** raw_kw)
        return new_obj
    # end def copy

    def correct_unknown_attr (self, error) :
        """Try to correct an unknown attribute error."""
        pass
    # end def correct_unknown_attr

    def destroy (self) :
        """Remove entity from `home_scope`."""
        if self is self.home_scope.root :
            self.home_scope.destroy ()
        else :
            assert (not self.home_scope._locked)
            self.home_scope.remove (self)
    # end def destroy

    def destroy_dependency (self, other) :
        for attr in self.object_referring_attributes.pop (other, ()) :
            attr.reset (self)
        if other in self.dependencies :
            del self.dependencies [other]
    # end def destroy_dependency

    def is_defined (self)  :
        return \
            (  (not self.is_used)
            or all (a.has_substance (self) for a in self.required)
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

    def make_snapshot (self) :
        self._attr_man.make_snapshot (self)
    # end def make_snapshot

    def notify_dependencies_destroy (self) :
        """Notify all entities registered in `self.dependencies` and
           `self.object_referring_attributes` about the destruction of `self`.
        """
        ### dicts are modified by the loops
        for d in self.dependencies.keys () :
            d.destroy_dependency (self)
        for o in self.object_referring_attributes.keys () :
            o.destroy_dependency (self)
    # end def notify_dependencies_destroy

    def register_dependency (self, other) :
        """Register that `other` depends on `self`"""
        self.dependencies [other] += 1
    # end def register_dependency

    def set (self, on_error = None, ** kw) :
        """Set attributes specified in `kw` from cooked values"""
        with self.home_scope.historian.nested_recorder (MOM.SCM.Change) :
            new_epk, pkas_raw, pkas_ckd = self._extract_primary_ckd (kw)
            if pkas_ckd :
                self._rename (new_epk, pkas_raw, pkas_ckd)
            result = self.__super.set (on_error, ** kw)
        return result
    # end def set

    def set_raw (self, on_error = None, ** kw) :
        """Set attributes specified in `kw` from raw values"""
        with self.home_scope.historian.nested_recorder (MOM.SCM.Change) :
            new_epk, pkas_raw, pkas_ckd = self._extract_primary_raw (kw)
            if pkas_ckd :
                self._rename (new_epk, pkas_raw, pkas_ckd)
            result = self.__super.set_raw (on_error, ** kw)
        return result
    # end def set_raw

    def unregister_dependency (self, other) :
        """Unregister dependency of `other` on `self`"""
        deps = self.dependencies
        deps [other] -= 1
        if deps [other] <= 0 :
            del deps [other]
    # end def unregister_dependency

    def update_dependency_names (self, other, old_name) :
        for attr in self.object_referring_attributes.get (other, []) :
            attr._update_raw (self, other, old_name)
    # end def update_dependency_names

    def _destroy (self) :
        self.notify_dependencies_destroy ()
    # end def _destroy

    def _extract_primary (self, kw) :
        result = {}
        for pka in self.primary :
            name = pka.name
            if name in kw :
                result [name] = kw.pop (name)
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

    def _finish__init__ (self, * epk, ** kw) :
        ### Need to use `__super.` methods here because it's not a `rename`
        setter = (self.__super.set, self.__super.set_raw) \
            [bool (kw.get ("raw", False))]
        self._init_epk       (setter, * epk)
        kw.pop               ("scope", None)
        self.home_scope.add  (self)
        try :
            self.__super._finish__init__  (* epk, ** kw)
        except StandardError, exc :
            self.home_scope.remove (self)
            raise
    # end def _finish__init__

    def _init_epk (self, setter, * epk) :
        assert len (epk) == len (self.primary)
        pkas = {}
        for a, pka in zip (self.primary, epk) :
            pkas [a.name] = pka
        setter (** pkas)
    # end def _init_epk

    def _init_meta_attrs (self) :
        self.__super._init_meta_attrs ()
        self.object_referring_attributes = {}
    # end def _init_meta_attrs

    def _rename (self, new_epk, pkas_raw, pkas_ckd) :
        def _renamer () :
            attributes = self.attributes
            for k, v in pkas_ckd.iteritems () :
                attr = attributes [k]
                attr._set_cooked_inner (self, v)
                attr._set_raw_inner    (self, pkas_raw [k], v)
            self._reset_epk ()
        self._kw_satisfies_i_invariants (pkas_ckd, None)
        self._set_record                (pkas_ckd)
        self.home_scope.rename          (self, tuple (new_epk), _renamer)
    # end def _rename

    def _repr (self, type_name) :
        return "%s (%s)" % \
            (type_name, ", ".join (self.epk_as_code))
    # end def _repr

    def _reset_epk (self) :
        del self.epk
        if "epk_as_dict" in self.__dict__ :
            del self.epk_as_dict
    # end def _reset_epk

    def _set_record (self, kw) :
        rvr = self._attr_man.raw_values_record (self, kw)
        if rvr :
            self.home_scope.record_change \
                (MOM.SCM.Entity_Change_Attr, self, rvr)
    # end def _set_record

    def __str__ (self) :
        epk = self.epk
        if len (epk) == 1 :
            format = "%s"
        else :
            format = "(%s)"
        return format % (", ".join (self.epk_as_code))
    # end def __str__

# end class Id_Entity

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

Essential Attributes
--------------------

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

Essential Predicates
--------------------

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

Class Attributes
----------------

`MOM.Id_Entity` provides a number of class attributes that control various
aspects of the use of an essential class by the framework.

.. attribute:: auto_display

  Lists (names of) the attributes that should be displayed by the UI.

.. attribute:: default_child

  Specifies which child of a partial class should be used by the UI by
  default. The value of this attribute is set for the partial class by
  one specific derived class.

.. attribute:: deprecated_attr_names

  This is a dictionary that maps deprecated names
  of attributes to the currently preferred names (this is used to
  allow the reading of older databases without loss of information).

.. attribute:: is_partial

  Specifies if objects/links can be created for the essential
  class in question.

.. attribute:: max_count

  Restricts the number of instances that can be created.

.. attribute:: Package_NS

  The package namespace in which this class is defined.

  Ideally, each package namespace defining essential classes defines a
  common root for these, e.g., `SPN.Entity`, that defines
  `Package_NS`, e.g., ::

      class _SPN_Entity_ (MOM.Id_Entity) :

          _real_name = "Entity"

          Package_NS = SPN
          ...

.. attribute:: rank

  Defines a relative order between essential classes and associations.
  Entities of lower rank are stored and retrieved from the database
  before entities of higher rank. If instances of a specific type
  depend on the existance of instances of another type, the dependent
  type should have higher rank.

.. attribute:: record_changes

  Changes of the entity will only be recorded if `record_changes` is True.

.. attribute:: refuse_links

  This is a set of (names of) classes that must not be linked
  to instances of the essential class in question. This can be used if
  objects of a derived class should not participate in associations of
  a base class.

.. attribute:: save_to_db

  Entity will be saved to database only if `save_to_db` is True.

.. attribute:: show_package_prefix

  Specifies whether the class name should be prefixed by the name of
  the package namespace in the UI.

.. attribute:: tutorial

  Describes why and how to define instances of the essential class and
  is used in step-by-step tutorials.

Methods
-------

Descendents of `MOM.Id_Entity` can redefine a number of methods to
influence how instances of the class are handled by the framework. If
you redefine one of these methods, you'll normally need to call the
`super` method somewhere in the redefinition.

.. method:: after_init

  Is called by the GUI after an instance of the class was
  (successfully) created. `after_init` can create additional objects
  automatically to ease the life of the interactive user of the
  application.

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


"""

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Entity
