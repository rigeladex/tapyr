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
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _MOM                  import MOM
from   _TFL.object_globals   import object_globals
from   _TFL.Regexp           import *

import _TFL.defaultdict

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

import _MOM.Filter

from   _MOM._Attr.Type import *
from   _MOM._Attr      import Attr
from   _MOM._Pred      import Pred

import itertools
import traceback

class _Entity_Essentials_ (TFL.Meta.Object) :
    """Define essential attributes of MOM entities (as needed by editors, ...)
    """

    Class                 = None
    home_scope            = None
    is_partial            = True  ### all complete descendents of this class
                                  ### must redefine `is_partial' to None
    show_package_prefix   = False
    ui_name               = None

    Package_NS            = MOM
    """`Package_Namespace` the class belongs to. Set to `None` if not
       defined inside a package.
       """

    class _Attributes (MOM.Attr.Spec) :
        pass
    # end class _Attributes

    class _Predicates (MOM.Pred.Spec) :
        pass
    # end class _Predicates

    def after_init    (self) : pass
    def after_init_db (self) : pass
    def has_substance (self) : pass

    def _repr (self, type_name) :
        return "%s (%s)" % (type_name, self.name)
    # end def _repr

    def __str__ (self) :
        return self.name
    # end def __str__

    def __repr__ (self) :
        try :
            tn = self.type_name
        except AttributeError :
            tn = self.__class__
        return self._repr (tn)
    # end def __repr__

    def __getattr__ (self, name) :
        ### just to ease up-chaining in descendents
        raise AttributeError, "%s.%s" % (self, name)
    # end def __getattr__

# end class _Entity_Essentials_

class Entity_Essentials (_Entity_Essentials_) :
    """Define essential attributes of thingies masquerading as MOM entities
       (as needed by editors, ...)
    """

    default_child         = None
    x_locked              = False
    electric              = False

    auto_display          = ()    ### object/link editor will display all
                                  ### attributes listed in `auto_display' for
                                  ### the selected object/link in the status
                                  ### window
    filters               = ()    ### filters for object editors
    generate_doc          = True  ### `generate_doc == False` inhibits
                                  ### generation of documentation
    max_count             = 0     ### restriction on number of instances
    record_changes        = True  ### `record_changes == False' inhibits
                                  ### recording of changes for an object or
                                  ### class
    save_to_db            = True  ### `save_to_db == False' inhibits saving of
                                  ### the object/link to the database
    tutorial              = None  ### text for step-to-step tutorial
    type_desc             = None  ### short description of object/link type

    deprecated_attr_names = {}
    refuse_links          = {}    ### subclasses can put associations here
                                  ### they don't want to participate in

    children              = {}
    """`children' enumerates the (direct) descendent classes of this class --
       it maps class names to class objects.
       """

# end class Entity_Essentials

class Entity (_Entity_Essentials_) :
    """Internal root class for MOM objects and links."""

    __metaclass__         = MOM.Meta.M_Entity
    __id                  = 0 ### used to generate a unique id for each entity
    __autowrap            = dict \
      (is_locked          = TFL.Meta.Class_and_Instance_Method)

    _appl_globals         = {}

    rank                  = 0

    _lists_to_combine     = ("filters", "auto_display")
    """`_lists_to_combine` names the list-valued attributes to be merged
       from all levels of the inheritance hierarchy
       """
    _dicts_to_combine     = ("deprecated_attr_names", "refuse_links")
    """`_dicts_to_combine` names the dict-valued attributes to be merged
       from all levels of the inheritance hierarchy
    """

    filters               = \
        ( MOM.Filter
            ( predicate   = "not object.is_defined ()"
            , name        = "underdefined"
            , description = "All objects with undefined required attributes"
            , bvar        = "object"
            )
        , MOM.Filter
            ( predicate   = "object.is_correct ()"
            , name        = "is internally correct"
            , description = "All internally correct objects"
            , bvar        = "object"
            , invert      = 1
            )
        , MOM.Filter
            ( predicate   = "object.is_g_correct ()"
            , name        = "is globally correct"
            , description = "All globally correct objects"
            , bvar        = "object"
            , invert      = 1
            )
        , MOM.Filter
            ( predicate   = "not object.is_locked ()"
            , name        = "editable"
            , description = "All objects with some editable attributes"
            , bvar        = "object"
            )
        )

    class _Attributes (_Entity_Essentials_._Attributes) :

        class default_sort_key (A_Blob) :
            """Defines the sort key to be used when sorting this entity."""

            kind          = Attr.Once_Cached ### Change in descendants

            def computed (self, obj) :
                return obj.id,
            # end def computed

        # end class default_sort_key

        class electric (A_Boolean) :
            """Indicates if object/link was created automatically or not."""

            kind          = Attr.Internal
            Kind_Mixins   = (Attr.Class_Uses_Default_Mixin, )
            default       = "no"
            hidden        = True

        # end class electric

        class x_locked (A_Boolean) :
            """Specifies if object can be changed by user"""

            kind          = Attr.Internal
            Kind_Mixins   = (Attr.Class_Uses_Default_Mixin, )
            default       = "no"
            hidden        = True

        # end class x_locked

        class is_used (A_Int) :
            """Specifies whether entity is used by another entity."""

            kind          = Attr.Cached
            default       = "1"

        # end class is_used

    # end class _Attributes

    class _Predicates (_Entity_Essentials_._Predicates) :

        class completely_defined (Pred.Condition) :
            """All required attributes must be defined."""

            kind          = Pred.System
            guard         = "is_used"
            guard_attr    = ("is_used", )

            def eval_condition (self, obj, glob_dict, val_dict) :
                info = self._error_info
                add  = info.append
                for a in obj.required :
                    if not a.has_substance (obj) :
                        add ("Required attribute %s is not defined" % (a, ))
                return not info
            # end def eval_condition

        # end class completely_defined

        class object_correct (Pred.Condition) :
            """All object invariants must be satisfied."""

            kind          = Pred.System

            def eval_condition (self, obj, glob_dict, val_dict) :
                info = self._error_info
                add  = info.append
                for p in obj._pred_man.errors ["object"] :
                    add (str (p))
                return not info
            # end def eval_condition

        # end class object_correct

    # end class _Predicates

    @property
    def has_errors (self) :
        return self._pred_man.has_errors
    # end def has_errors

    @property
    def has_warnings (self) :
        return self._pred_man.has_warnings
    # end def has_warnings

    def __new__ (cls, * args, ** kw) :
        if cls.is_partial :
            raise MOM.Error.Partial_Type (cls.type_name)
        result = super (Entity, cls).__new__ (cls)
        if not result.home_scope :
            result.home_scope = kw.get ("scope", MOM.Scope.active)
        result.id = result.__new_id ()
        return result
    # end def __new__

    def __init__ (self) :
        self._init_meta_attrs ()
        self._init_attributes ()
    # end def __init__

    @classmethod
    def add_filter (cls, * filters) :
        """Add `filters` to `clss`."""
        cls.filters += filters
    # end def add_filter

    def after_init (self) :
        pass
    # end def after_init

    def attr_value_maybe (self, name) :
        attr = self.attributes.get (name)
        if attr :
            return attr.get_value (self)
    # end def attr_value_maybe

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

    ### XXX needs to change
    def copy (self, * new_n, ** kw) :
        """Make copy with name(s) `new_n`."""
        new_obj = self.__class__ (* new_n)
        raw_kw  = self._attr_man.raw_attr_value_dict
        if raw_kw :
            new_obj.set_raw (** raw_kw)
        if kw :
            new_obj.set     (** kw)
        return new_obj
    # end def copy

    def correct_unknown_attr (self, error) :
        """Try to correct an unknown attribute error."""
        pass
    # end def correct_unknown_attr

    def globals (self) :
        return self.__class__._appl_globals or object_globals (self)
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

    def is_locked (self) :
        return self.x_locked or self.electric
    # end def is_locked

    def make_snapshot (self) :
        self._attr_man.make_snapshot (self)
    # end def make_snapshot

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
                if attr._set is None :
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
                            attr.from_string (self, val)
                    except (ValueError, MOM.Error.Attribute_Syntax_Error), err:
                        print ("Warning: Error when setting attribute %s "
                               "of %s to %s\nClearing attribute"
                              ) % (attr.name, self.name, val)
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

    def _init_meta_attrs (self) :
        self._attr_man  = MOM.Attr.Manager (self._Attributes)
        self._pred_man  = MOM.Pred.Manager (self._Predicates)
        self.object_referring_attributes = {}
    # end def _init_meta_attrs

    def _init_attributes (self) :
        self._attr_man.reset_attributes (self)
    # end def _init_attributes_

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
        rvr = self._attr_man.raw_values_record (self, kw)
        if rvr :
            self.home_scope.record_change \
                (MOM.SCM.Entity_Change_Attr, self, rvr)
    # end def _set_record

    def _store_attr_error (self, exc) :
        self.home_scope._db_errors.append (exc)
    # end def _store_attr_error

    @staticmethod
    def __new_id () :
        Entity.__id += 1
        return Entity.__id
    # end def __new_id

    def __repr__ (self) :
        return self._repr (self.type_name)
    # end def __repr__

# end class Entity

_Essence = Entity

__all__  = ("Entity", "Entity_Essentials")

__doc__  = """
Class `MOM.Entity`
==================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Entity

   `MOM.Entity` provides the framework for defining essential classes and
   associations. Each essential class or association is characterized by

   - `essential attributes`_

   - `essential predicates`_

   - `class attributes`_

   - `methods`_

   Each instance of `Entity` has a a couple of attributes:

   - `id` is a unique identifier that isn't changed after the instance
     is created -- even when the entity is renamed.

   - `home_scope` refers to the :class:`~_MOM.Scope.Scope` in
     which the instance lives.

   `Entity` is normally not directly used as a base class. Instead,
   `Entity`'s subclasses :class:`~_MOM.Object.Object` and
   :class:`~_MOM.Link.Link` serve as root classes for the hierarchies
   of essential classes and associations, respectively.

Essential Attributes
--------------------

Essential attributes are defined inside the class `_Attributes`
that is nested in `Entity` (or one of its derived classes).

Any essential class derived (directly or indirectly) from `Entity`
needs to define a `_Attributes` class that's derived from its
ancestors `_Attributes`. The top-most `_Attributes` class is
derived from :class:`MOM.Attr.Spec<_MOM._Attr.Spec.Spec>`.

Each essential attribute is defined by a class derived from one of
the attribute types in :mod:`MOM.Attr.Type<_MOM._Attr.Type>`.

`MOM.Entity` defines a number of attributes that can be overriden by
descendant classes:

- electric

- x_locked

- is_used

Essential Predicates
--------------------

Essential predicates are defined inside the class `_Predicates` that
is nested in `Entity` (or one of its derived classes).

Any essential class derived (directly or indirectly) from `Entity`
needs to define a `_Predicates` class that's derived from its
ancestors `_Predicates`. The top-most `_Predicates` class is
derived from :class:`MOM.Pred.Spec<_MOM._Pred.Spec.Spec>`.

Each essential predicate is defined by a class derived from one of
the predicate types in :mod:`MOM.Pred.Type<_MOM._Pred.Type>`.

`MOM.Entity` defines two predicates that should not be overriden by
descendant classes:

- completely_defined

- object_correct

Please note that these two predicates are *not* to be used as examples
of how predicates should be defined. Normally, predicates define
`assertion`, not `eval_condition`! This is explained in more detail in
:mod:`MOM.Pred.Type<_MOM._Pred.Type>`.

Class Attributes
----------------

`MOM.Entity` provides a number of class attributes that control various
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

.. attribute:: filters

  This is a sequence of filter objects (see :class:`~_MOM.Filter`)
  that can be used in the UI to reduce the number of objects displayed
  to those satisfying the filter condition.

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

      class _SPN_Entity_ (MOM.Entity) :

          _real_name = "Entity"

          Package_NS = SPN
          ...

.. attribute:: rank

  Defines a relative order between essential classes and associations.
  Entities of lower rank are stored and retrieved from the database
  before entities of higher rank. If instances of a specific type
  depend on the existance of instances of another type, the dependent
  type should have higher rank.

.. attribute:: refuse_links

  This is a dictionary of (names of) classes that must not be linked
  to instances of the essential class in question. This can be used if
  objects of a derived class should not participate in associations of
  a base class.

.. attribute:: show_package_prefix

  Specifies whether the class name should be prefixed by the name of
  the package namespace in the UI.

.. attribute:: tutorial

  Describes why and how to define instances of the essential class and
  is used in step-by-step tutorials.

Methods
-------

Descendents of `MOM.Entity` can redefine a number of methods to
influence how instances of the class are handled by the framework. If
you redefine one of these methods, you'll normally need to call the
`super` method somewhere in the redefinition.

- `after_init` is called by the GUI after an instance of the class was
  (successfully) created. `after_init` can create additional objects
  automatically to ease the life of the interactive user of the
  application.

- `compute_defaults_internal` is called whenever object attributes
  needs to synchronized and can be used to set attributes to computed
  default values. Please note that it is better to use
  `compute_default` defined for a specific attribute than to compute that
  value in `compute_defaults_internal`.

  `compute_defaults_internal` should only be used when the default
  values for several different attributes need to be computed together.

- `compute_type_defaults_internal` is a class method that is called to
  compute a default value of an attribute that is based on all
  instances of the class. The value of such an attribute must be
  stored as a class attribute (or in the root object of the scope).


"""

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Entity
