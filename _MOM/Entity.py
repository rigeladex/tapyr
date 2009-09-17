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

import _MOM.Documenter
import _MOM.Filter

from   _MOM._Attr.Type import *
from   _MOM._Attr      import Attr
from   _MOM._Pred      import Pred

import traceback

def cmp_key_id (ent) :
    return ent.id
# end def cmp_key_id

def cmp_key_name (ent) :
    return ent.name
# end def cmp_key_name

def cmp_key_rank_id (ent) :
    return (ent.rank, ent.id)
# end def cmp_key_rank_id

def cmp_key_rank_name (ent) :
    return (ent.rank, ent.name)
# end def cmp_key_rank_name

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

    __metaclass__ = MOM.Meta.M_Entity
    __id          = 0 ### used to generate a unique id for each entity
    __autowrap    = dict \
      (is_locked  = TFL.Meta.Class_and_Instance_Method)

    doc_description_attributes = ("type_desc", "__doc__")
    doc_explanation_attributes = ("type_expl", )
    doc_name_attributes        = ("ui_name", )

    _appl_globals              = {}
    _db_attr                   = {}

    Documenter                 = MOM.Documenter ()

    rank                = 0

    _lists_to_combine   = ("filters", "auto_display")
    """`_lists_to_combine` names the list-valued attributes to be merged
       from all levels of the inheritance hierarchy
       """
    _dicts_to_combine   = ("deprecated_attr_names", "refuse_links")
    """`_dicts_to_combine` names the dict-valued attributes to be merged
       from all levels of the inheritance hierarchy
    """

    filters             = \
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

    @staticmethod
    def __new_id () :
        Entity.__id += 1
        return Entity.__id
    # end def __new_id

    @classmethod
    def add_filter (cls, * filters) :
        """Add `filters` to `clss`."""
        cls.filters += filters
    # end def add_filter

    def globals (self) :
        return self.__class__._appl_globals or object_globals (self)
    # end def globals

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
            """Number of users."""

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

    def __new__ (cls, * args, ** kw) :
        if cls.is_partial :
            raise MOM.Error.Partial_Type (cls.type_name)
        result = super (Entity, cls).__new__ (cls)
        if not result.home_scope :
            result.home_scope = MOM.Scope.active
        result.id = result.__new_id ()
        return result
    # end def __new__

    def __init__ (self) :
        self._init_meta_attrs ()
        self._init_attributes ()
    # end def __init__

    def after_init (self) :
        pass
    # end def after_init

    def after_init_db (self) :
        pass
    # end def after_init

    def _init_meta_attrs (self) :
        self._attr_man                   = MOM.Attr.Manager (self._Attributes)
        self._pred_man                   = MOM.Pred.Manager (self._Predicates)
        self.dependencies                = TFL.defaultdict  (int)
        self.object_referring_attributes = {}
    # end def _init_meta_attrs

    def _init_attributes (self) :
        self._attr_man.reset_attributes (self)
    # end def _init_attributes_

    def attr_value_maybe (self, name) :
        attr = self.attributes.get (name)
        if attr :
            return attr.get_value (self)
    # end def attr_value_maybe

    cmp_key_id        = cmp_key_id
    cmp_key_name      = cmp_key_name
    cmp_key_rank_id   = cmp_key_rank_id
    cmp_key_rank_name = cmp_key_rank_name

    def raw_attr (self, name) :
        """Returns the raw value of attribute `name`, i.e., the value entered
           by the user into the object editor.
        """
        attr = self.attributes.get (name)
        if attr :
            return attr.get_raw (self) or ""
    # end def raw_attr

    def set_attr_iter (self, attr_dict, raise_err = True) :
        attributes = self.attributes
        for name, val in attr_dict.iteritems () :
            cnam = self.deprecated_attr_names.get (name, name)
            attr = attributes.get (cnam)
            if attr :
                if attr._set is None :
                    if raise_err :
                        raise AttributeError, \
                            ( "Can't set %s attribute <%s>.%s to `%s`"
                            % (attr.kind, self, name, val)
                            )
                    else :
                        self.home_scope._db_errors.append \
                            (MOM.Invalid_Attribute (self, name, val))
                else :
                    yield (cnam, val, attr)
            elif name != "raw" :
                self.home_scope._db_errors.append \
                    (MOM.Unknown_Attribute (self, name, val))
    # end def set_attr_iter

    def _set_internal_attributes (self, raw = 1, ** kw) :
        g = self.globals ()
        for name, raw_val, attr in self.set_attr_iter (kw, raise_err = False) :
            try :
                val = attr.from_code_string (self, raw_val, g)
            except MOM.Error.Attribute_Syntax_Error, exc :
                print exc
            except StandardError, exc :
                if __debug__ :
                    print "_set_internal_attributes:", exc
                    print self, name, raw_val
                    traceback.print_exc ()
            else :
                attr._set_raw (self, raw_val, val)
    # end def _set_internal_attributes

    def _set_pickle_state (self, editable, electric) :
        try :
            if editable :
                self.set (raise_exception = 0, ** editable)
                self._db_attr  = editable
        except StandardError, exc :
            if __debug__ :
                print "Unpickling error %s: editable=%s" % (self, editable)
                print exc
                traceback.print_exc ()
        try :
            if electric :
                self._set_internal_attributes (** electric)
        except StandardError, exc:
            if __debug__ :
                print "Unpickling error %s: electric=%s" % (self, electric)
                print exc
                traceback.print_exc ()
        self.after_init_db ()
    # end def _set_pickle_state

    def is_locked (self) :
        return self.x_locked or self.electric
    # end def is_locked

    def set (self, raise_exception = 1, raw = 0, internals = None, ** kw) :
        """Set attributes specified in parameter list"""
        if raw :
            return self.set_raw    (raise_exception, internals, ** kw)
        else :
            return self.set_cooked (raise_exception, ** kw)
    # end def set

    def _set_record (self, kw) :
        rvr = self._attr_man.raw_values_record (self, kw)
        if rvr :
            self.home_scope.record_change \
                (MOM.SCM.Entity_Change_Attr, self, rvr)
    # end def _set_record

    def set_cooked (self, raise_exception = 1, ** kw) :
        """Set attributes specified in `kw` from cooked values"""
        self._kw_satisfies_i_invariants (kw, raise_exception)
        self._set_record (kw)
        tc = self._attr_man.total_changes
        for name, val, attr in self.set_attr_iter (kw, raise_exception) :
            attr._set_cooked (self, val)
        return self._attr_man.total_changes - tc
    # end def set_cooked

    def set_raw (self, raise_exception = 1, internals = None, ** kw) :
        """Set attributes specified in `kw` from raw values"""
        if not (internals or kw) :
            return 0
        tc = self._attr_man.total_changes
        if kw :
            if not self._db_attr :
                self._db_attr = kw
            cooked_kw = {}
            to_do     = []
            for name, val, attr in self.set_attr_iter (kw, raise_exception) :
                if val :
                    try :
                        cooked_kw [name] = cooked_val = \
                            self._attr_from_string (attr, val)
                    except (ValueError, MOM.Error.Attribute_Syntax_Error), err:
                        print ("Warning: Error when setting attribute %s "
                               "of %s to %s\nClearing attribute"
                              ) % (attr.name, self.name, val)
                        self.home_scope._db_errors.append \
                            (MOM.Invalid_Attribute (self, name, val))
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
            self._kw_satisfies_i_invariants (cooked_kw, raise_exception)
            self._set_record (cooked_kw)
            self._attr_man.reset_pending ()
            for attr, raw_val, val in to_do :
                attr._set_raw (self, raw_val, val)
        if internals :
            ikw = {}
            self._decode_internals (internals, ikw)
            if ikw :
                self._set_internal_attributes (** ikw)
        return self._attr_man.total_changes - tc
    # end def set_raw

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

    def has_changed (self) :
        return self._attr_man.has_changed (self)
    # end def has_changed

    @property
    def has_errors (self) :
        return self._pred_man.has_errors
    # end def has_errors

    @property
    def has_warnings (self) :
        return self._pred_man.has_warnings
    # end def has_warnings

    def make_snapshot (self) :
        self._attr_man.make_snapshot (self)
    # end def make_snapshot

    def is_instance (self, of_class) :
        return isinstance (self, of_class)
    # end def is_instance

    def is_correct (self, attr_dict = {})  :
        ews = self._pred_man.check_kind ("object", self, attr_dict)
        return not ews
    # end def is_correct

    def is_g_correct (self)  :
        ews = self._pred_man.check_kind ("system", self)
        return not ews
    # end def is_g_correct

    def is_defined (self)  :
        return (not self.is_used) or self.is_defined__ ()
    # end def is_defined

    def _kw_satisfies_i_invariants (self, attr_dict, raise_exception) :
        result = not self.is_correct (attr_dict)
        if result :
            errors = self._pred_man.errors ["object"]
            if raise_exception :
                raise MOM.Error.Invariant_Errors (errors)
            else :
                print self, MOM.Error.Invariant_Errors (errors)
        return result
    # end def _kw_satisfies_i_invariants

    def is_defined__ (self)  :
        ### XXX move code into _attr_man and Attr.Kind
        for a in self.required :
            if not a.has_substance (self) :
                return False
        return True
    # end def is_defined__

    def _destroy (self) :
        self.notify_dependencies_destroy ()
        self.__super._destroy ()
    # end def _destroy

    def destroy_dependency (self, other) :
        for attr in self.object_referring_attributes.pop (other, ()) :
            attr.reset (self)
        if other in self.dependencies :
            del self.dependencies [other]
    # end def destroy_dependency

    def notify_dependencies_destroy (self) :
        """Notify all entities registered in `self.dependencies` and
           `self.object_referring_attributes` about the destruction of `self`.
        """
        for d in self.dependencies.keys () :
            d.destroy_dependency (self)
        for o in self.object_referring_attributes.keys () :
            o.destroy_dependency (self)
    # end def notify_dependencies_destroy

    def register_dependency (self, other) :
        """Register that `other` depends on `self`"""
        self.dependencies [other] += 1
    # end def register_dependency

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

    def has_substance (self) :
        """TRUE if there is at least one attribute with a non-default value."""
        return bool \
            (  self.dependencies
            or any (a.has_substance (self) for a in self.user_attr)
            )
    # end def has_substance

    def reset_syncable (self) :
        self._attr_man.reset_syncable ()
    # end def reset_syncable

    def sync_attributes (self) :
        """Synchronizes all user attributes with the values from
           _raw_attr and all sync-cached attributes.
        """
        self._attr_man.sync_attributes (self)
    # end def sync_attributes

    def check_all (self) :
        """Checks all predicates"""
        return self._pred_man.check_all (self)
    # end def check_all

    def _attr_from_string (self, attr, raw_val) :
        try :
            return attr.from_string (self, raw_val)
        except TypeError :
            print self, attr.name, raw_val, type (raw_val)
            raise
    # end def _attr_from_string

    def compute_defaults_internal (self) :
        """Compute default values for optional/internal/cached parameters."""
        pass
    # end def compute_defaults_internal

    @classmethod
    def compute_type_defaults_internal (cls) :
        pass
    # end def compute_type_defaults_internal

    def _save_attr_to_db (self, attr, value) :
        return attr.to_save (self)
    # end def _save_attr_to_db

    def _picklish (self) :
        if not self.save_to_db :
            return
        editable = {"raw" : 1}
        electric = {"raw" : 1}
        for a in self.attributes.values () :
            if not a.save_to_db :
                continue
            if not a.electric :                        ### required or optional
                v = a.get_raw (self)
                if self._save_attr_to_db (a, v) :
                    editable [a.name] = v
            else :                                     ### computed or internal
                v = getattr (self, a.name)
                if self._save_attr_to_db (a, v) :
                    try :
                        electric [a.name] = a.as_code_string (v)
                    except (SystemExit, KeyboardInterrupt), exc :
                        raise
                    except :
                        print self, a.name, a.typ, v
                        raise
        return self.Pickle (self, editable, electric)
    # end def _picklish

    def attributes___ (self, start = None) :
        result = start or []
        for kind in self.required, self.optional :
            for a in kind :
                if a.to_save (self) :
                    result.append \
                        ("%s = %s" % (a.name, a.raw_as_string (self)))
        return result
    # end def attributes___

    def attributes__ (self, start = []) :
        result   = start + self.attributes___ ()
        internal = self._encoded_internals ()
        if internal :
            if isinstance (internal, (str, unicode)) :
                result.append ("internals = " + `internal`)
            else :
                result [len (result):] = internal
        return result
    # end def attributes__

    def customize_stmt (self) :
        return self.define_stmt ("customize")
    # end def customize_stmt

    def define_stmt (self, name_of_def_stmt = None) :
        name = self._define_stmt_name_arg ()
        args = self.attributes__  ([name])
        if self._need_define_stmt (args) :
            return self._define_stmt \
                (args, name_of_def_stmt = name_of_def_stmt)
        else :
            ### print "Ignoring", name
            return ""
    # end def define_stmt

    def remove_stmt (self) :
        return """%s.%s (%s)\n""" % \
               ( self.type_name
               , self._name_of_remove_stmt
               , self._remove_stmt_name_arg ()
               )
    # end def remove_stmt

    def _define_stmt \
        (self, args, sep = ", ", sep2 = " ", name_of_def_stmt = None) :
        if name_of_def_stmt is None :
            name_of_def_stmt = self._name_of_define_stmt
        return """%s.%s (%s, raw=1)\n""" % \
               (self.type_name, name_of_def_stmt, sep.join (args))
    # end def _define_stmt

    def _need_define_stmt (self, args) :
        return 1
    # end def _need_define_stmt

    def _decode_internals (self, internals, kw) :
        pass
    # end def _decode_internals

    def _encoded_internals (self, attr_kinds = ("internal", )) :
        result = []
        for kn in attr_kinds :
            kind = getattr (self, kn)
            for a in kind :
                v = getattr (self, a.name)
                if self._save_attr_to_db (a, v) :
                    result.append (a.name + " = " + a.as_code_string (v))
        return result
    # end def _encoded_internals

    def _journal_items (self, result_dict, result) :
        attributes = self.attributes
        raw_attr_d = self._attr_man.raw_attr_value_dict
        for k, v in dusort (result_dict.iteritems (), TFL.Item [0]) :
            if k in raw_attr_d :
                old = raw_attr_d [k]
                if (old != v) and (v or old):
                    result.append \
                        ( '%s = %s'
                        % (k, attributes [k].raw_as_string (self, v))
                        )
        return result
    # end def _journal_items

    def correct_unknown_attr (self, error) :
        """Try to correct an unknown attribute error."""
        pass
    # end def correct_unknown_attr

    def __repr__ (self) :
        return self._repr (self.type_name)
    # end def __repr__

# end class Entity

_Essence = Entity

__all__ = \
    ( "Entity", "Entity_Essentials"
    , "cmp_key_name", "cmp_key_id", "cmp_key_rank_name", "cmp_key_rank_id"
    )

__doc__ = """
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

       .. note::
         Technically, `home_scope` is a class attribute (of a
         scope-specific class that's automatically created by the
         framework).

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

- default_sort_key

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

- `after_init_db` is called after an instance of the class was read
  from the database. Such methods can be used as legacy lifters after
  a serious change of semantics and are normally injected into the
  essential class in question by the database framework.

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
