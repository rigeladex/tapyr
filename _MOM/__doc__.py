# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
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
#    MOM.__doc__
#
# Purpose
#    Documentation and test for MOM meta object model
#
# Revision Dates
#    18-Oct-2009 (CT) Creation
#     4-Nov-2009 (CT) Creation continued
#     4-Nov-2009 (MG) `Beaver` and `Otter` added
#    23-Nov-2009 (CT) Creation continued..
#    24-Nov-2009 (CT) Creation continued...
#    25-Nov-2009 (CT) Creation continued....
#    27-Nov-2009 (CT) Creation continued.....
#    27-Nov-2009 (MG) Order of test cases changed, use `list` operator in
#                     some tests
#     4-Dec-2009 (MG) Tests adopted to use real database back end
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#    18-Jan-2010 (MG) Tests fixed (`Invalid_Attribute` now has a different
#                     error message)
#    21-Jan-2010 (CT) `Primary_Optional` added
#    ««revision-date»»···
#--

dt_form = \
"""
How to define and use essential object models
==============================================

Using `MOM`, an essential object model is specified by deriving
classes from :class:`MOM.Object<_MOM.Object.Object>`,
:class:`MOM.Named_Object<_MOM.Object.Named_Object>`, or from one of
the descendants of :class:`MOM.Link<_MOM.Link.Link>`.

Each essential class must be defined inside a
:class:`TFL.Package_Namespace<_TFL.Package_Namespace.Package_Namespace>`
and the class definition must contain an explicit or inherited
reference :attr:`PNS<_MOM.Entity.PNS>` to that package
namespace.

Normally, each essential class is defined in a module of its own. In
some cases, a single module might define more than one essential
class.

The module `_MOM.import_MOM` provides all classes necessary to define
essential object or link types and is meant to be imported like::

    >>> from _MOM.import_MOM import *

An essential class as defined by its module isn't usable before an
app-type is created.

    >>> BMT.Person
    <class 'BMT.Person' [Spec Essence]>
    >>> BMT.Rodent
    <class 'BMT.Rodent' [Spec Essence]>
    >>> BMT.Beaver
    <class 'BMT.Beaver' [Spec Essence]>
    >>> BMT.Person_owns_Trap
    <class 'BMT.Person_owns_Trap' [Spec Essence]>
    >>> BMT.Person.last_name
    Traceback (most recent call last):
        ...
    AttributeError: type object 'Person' has no attribute 'last_name'


Application type
----------------

Before an essential object model can be used, the
:class:`application type<_MOM.App_Type.App_Type>` and at least one
:class:`derived application type<_MOM.App_Type._App_Type_D_>` must be
defined:

    >>> %(import_EMS)s as EMS
    >>> %(import_DBW)s as DBW
    >>> apt = MOM.App_Type (u"BMT", BMT).Derived (EMS, DBW)

Creating a derived app-type replaces the specification of the
essential classes with bare essential classes:

    >>> BMT.Person
    <class 'BMT.Person' [Bare Essence]>
    >>> BMT.Rodent
    <class 'BMT.Rodent' [Bare Essence]>
    >>> BMT.Beaver
    <class 'BMT.Beaver' [Bare Essence]>
    >>> BMT.Person_owns_Trap
    <class 'BMT.Person_owns_Trap' [Bare Essence]>

and derives an app-type specific entity-type for each of the essential
classes:

    >>> ET_Id_Entity = apt.entity_type (u"MOM.Id_Entity")
    >>> ET_Named_Obj = apt.entity_type (u"MOM.Named_Object")
    >>> ET_Person    = apt.entity_type (u"BMT.Person")
    >>> ET_Mouse     = apt [u"BMT.Mouse"]
    >>> ET_Rat       = apt [u"BMT.Rat"]
    >>> ET_Rodent    = apt [u"BMT.Rodent"]
    >>> ET_Trap      = apt [u"BMT.Trap"]
    >>> ET_Supertrap = apt [u"BMT.Supertrap"]

For each `entity_type` with a unique :attr:`epk_sig`, the meta
machinery automatically creates methods `epkified_ckd` and
`epkified_raw` matching the `epk_sig`. These auto-generated methods
are used by `__init__` to ensure that the required parameters are
passed for the :ref:`essential primary keys<essential-primary-keys>`.

    >>> for et in apt._T_Extension :
    ...   if et.epk_sig and u"epkified_ckd" in et.__dict__ :
    ...     print u"***", et.type_name, u"***", et.epk_sig
    ...     print et.epkified_ckd.source_code.rstrip ()
    ...     print et.epkified_raw.source_code.rstrip ()
    ...
    *** MOM.Link *** ('left', 'right')
    def epkified_ckd (cls, left, right, ** kw) :
        return (left, right), kw
    def epkified_raw (cls, left, right, ** kw) :
        return (left, right), kw
    *** MOM.Link2 *** ('left', 'right')
    def epkified_ckd (cls, left, right, ** kw) :
        return (left, right), kw
    def epkified_raw (cls, left, right, ** kw) :
        return (left, right), kw
    *** MOM.Link2_Ordered *** ('left', 'right', 'seq_no')
    def epkified_ckd (cls, left, right, seq_no, ** kw) :
        return (left, right, seq_no), kw
    def epkified_raw (cls, left, right, seq_no, ** kw) :
        return (left, right, seq_no), kw
    *** MOM.Link3 *** ('left', 'middle', 'right')
    def epkified_ckd (cls, left, middle, right, ** kw) :
        return (left, middle, right), kw
    def epkified_raw (cls, left, middle, right, ** kw) :
        return (left, middle, right), kw
    *** MOM.Named_Object *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Location *** ('lon', 'lat')
    def epkified_ckd (cls, lon, lat, ** kw) :
        return (lon, lat), kw
    def epkified_raw (cls, lon, lat, ** kw) :
        return (lon, lat), kw
    *** BMT.Person *** ('last_name', 'first_name', 'middle_name')
    def epkified_ckd (cls, last_name, first_name, middle_name = '', ** kw) :
        return (last_name, first_name, middle_name), kw
    def epkified_raw (cls, last_name, first_name, middle_name = u'', ** kw) :
        return (last_name, first_name, middle_name), kw
    *** BMT.Rodent *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Mouse *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Rat *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Beaver *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Otter *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Trap *** ('name', 'serial_no')
    def epkified_ckd (cls, name, serial_no, ** kw) :
        return (name, serial_no), kw
    def epkified_raw (cls, name, serial_no, ** kw) :
        return (name, serial_no), kw
    *** BMT.Supertrap *** ('name', 'serial_no')
    def epkified_ckd (cls, name, serial_no, ** kw) :
        return (name, serial_no), kw
    def epkified_raw (cls, name, serial_no, ** kw) :
        return (name, serial_no), kw
    *** BMT.Rodent_in_Trap *** ('left', 'right')
    def epkified_ckd (cls, left, right, ** kw) :
        return (left, right), kw
    def epkified_raw (cls, left, right, ** kw) :
        return (left, right), kw
    *** BMT.Person_owns_Trap *** ('left', 'right')
    def epkified_ckd (cls, left, right, ** kw) :
        return (left, right), kw
    def epkified_raw (cls, left, right, ** kw) :
        return (left, right), kw
    *** BMT.Person_sets_Trap_at_Location *** ('left', 'middle', 'right')
    def epkified_ckd (cls, left, middle, right, ** kw) :
        return (left, middle, right), kw
    def epkified_raw (cls, left, middle, right, ** kw) :
        return (left, middle, right), kw

The app-type specific entity-types are ready to be used by
:class:`scopes<_MOM.Scope.Scope>` and their
:mod:`etype managers<_MOM.E_Type_Manager>`:

    >>> ET_Person
    <class 'BMT.Person' [BMT__Hash__HPS]>
    >>> ET_Person.Essence
    <class 'BMT.Person' [Bare Essence]>
    >>> ET_Person.E_Spec
    <class 'BMT.Person' [Spec Essence]>
    >>> ET_Person.primary
    [String `last_name`, String `first_name`, String `middle_name`]
    >>> [attr.__class__.__name__ for attr in ET_Person.primary]
    ['Primary', 'Primary', 'Primary_Optional']
    >>> ET_Person.required
    []
    >>> ET_Person.optional
    []

    >>> ET_Mouse.primary
    [Name `name`]
    >>> ET_Mouse.required
    [Float `weight`]
    >>> ET_Mouse.optional
    [String `color`]
    >>> sorted (ET_Mouse.attributes.itervalues (), key = TFL.Getter.name)
    [Cached_Role `catcher`, String `color`, Boolean `electric`, Int `is_used`, Name `name`, Float `weight`, Boolean `x_locked`]

    >>> ET_Person.last_name.name, ET_Person.last_name.ui_name
    ('last_name', 'Last name')
    >>> sorted (ET_Person._Attributes._own_names)
    ['first_name', 'last_name', 'middle_name', 'traps']
    >>> ET_Mouse.color.name, ET_Mouse.color.ui_name
    ('color', 'color')

    >>> sorted (ET_Trap._Attributes._own_names)
    ['catch', 'location', 'max_weight', 'owner', 'serial_no', 'setter']
    >>> sorted (ET_Supertrap._Attributes._own_names)
    []
    >>> sorted (ET_Trap._Attributes._names)
    ['catch', 'electric', 'is_used', 'location', 'max_weight', 'name', 'owner', 'serial_no', 'setter', 'x_locked']
    >>> sorted (ET_Supertrap._Attributes._names)
    ['catch', 'electric', 'is_used', 'location', 'max_weight', 'name', 'owner', 'serial_no', 'setter', 'x_locked']
    >>> sorted (ET_Trap.attributes.itervalues (), key = TFL.Getter.name)
    [Cached_Role `catch`, Boolean `electric`, Int `is_used`, Cached_Role `location`, Float `max_weight`, Name `name`, Cached_Role `owner`, Int `serial_no`, Cached_Role `setter`, Boolean `x_locked`]
    >>> sorted (ET_Supertrap.attributes.itervalues (), key = TFL.Getter.name)
    [Cached_Role `catch`, Boolean `electric`, Int `is_used`, Cached_Role `location`, Float `max_weight`, Name `name`, Cached_Role `owner`, Int `serial_no`, Cached_Role `setter`, Boolean `x_locked`]

    >>> sorted (ET_Id_Entity.relevant_roots)
    ['BMT.Location', 'BMT.Person', 'BMT.Person_owns_Trap',\
 'BMT.Person_sets_Trap_at_Location', 'BMT.Rodent', 'BMT.Rodent_in_Trap',\
 'BMT.Trap']
    >>> ET_Person.relevant_root
    <class 'BMT.Person' [BMT__Hash__HPS]>
    >>> ET_Rodent.relevant_root
    <class 'BMT.Rodent' [BMT__Hash__HPS]>
    >>> ET_Mouse.relevant_root
    <class 'BMT.Rodent' [BMT__Hash__HPS]>

    >>> sorted (ET_Person.children)
    []
    >>> sorted (ET_Rodent.children)
    ['BMT.Mouse', 'BMT.Rat']
    >>> sorted (ET_Rodent.children.itervalues (), key = TFL.Getter.type_name)
    [<class 'BMT.Mouse' [BMT__Hash__HPS]>,\
 <class 'BMT.Rat' [BMT__Hash__HPS]>]
    >>> sorted (ET_Rat.children)
    []

    >>> sorted (apt.etypes)
    ['BMT.Beaver', 'BMT.Location', 'BMT.Mouse', 'BMT.Otter', 'BMT.Person', 'BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rat', 'BMT.Rodent', 'BMT.Rodent_in_Trap', 'BMT.Supertrap', 'BMT.Trap', 'MOM.An_Entity', 'MOM.Entity', 'MOM.Id_Entity', 'MOM.Link', 'MOM.Link2', 'MOM.Link2_Ordered', 'MOM.Link3', 'MOM.Named_Object', 'MOM.Object']
    >>> [t.type_name for t in apt._T_Extension]
    ['MOM.Entity', 'MOM.An_Entity', 'MOM.Id_Entity', 'MOM.Link', 'MOM.Link2', 'MOM.Link2_Ordered', 'MOM.Link3', 'MOM.Object', 'MOM.Named_Object', 'BMT.Location', 'BMT.Person', 'BMT.Rodent', 'BMT.Mouse', 'BMT.Rat', 'BMT.Beaver', 'BMT.Otter', 'BMT.Trap', 'BMT.Supertrap', 'BMT.Rodent_in_Trap', 'BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location']
    >>> for t in apt._T_Extension [2:] :
    ...     print u"%%-35s %%s" %% (t.type_name, t.epk_sig)
    MOM.Id_Entity                       ()
    MOM.Link                            ('left', 'right')
    MOM.Link2                           ('left', 'right')
    MOM.Link2_Ordered                   ('left', 'right', 'seq_no')
    MOM.Link3                           ('left', 'middle', 'right')
    MOM.Object                          ()
    MOM.Named_Object                    ('name',)
    BMT.Location                        ('lon', 'lat')
    BMT.Person                          ('last_name', 'first_name', 'middle_name')
    BMT.Rodent                          ('name',)
    BMT.Mouse                           ('name',)
    BMT.Rat                             ('name',)
    BMT.Beaver                          ('name',)
    BMT.Otter                           ('name',)
    BMT.Trap                            ('name', 'serial_no')
    BMT.Supertrap                       ('name', 'serial_no')
    BMT.Rodent_in_Trap                  ('left', 'right')
    BMT.Person_owns_Trap                ('left', 'right')
    BMT.Person_sets_Trap_at_Location    ('left', 'middle', 'right')
    >>> for t in apt._T_Extension [2:] :
    ...     print u"%%s%%s    %%s" %% (t.type_name, NL, t.sorted_by.criteria)
    MOM.Id_Entity
        (<bound method M_E_Type_Id.sort_key of <class 'MOM.Id_Entity' [BMT__Hash__HPS]>>,)
    MOM.Link
        (<bound method M_E_Type_Link.sort_key of <class 'MOM.Link' [BMT__Hash__HPS]>>,)
    MOM.Link2
        (<bound method M_E_Type_Link2.sort_key of <class 'MOM.Link2' [BMT__Hash__HPS]>>,)
    MOM.Link2_Ordered
        (<bound method M_E_Type_Link2.sort_key of <class 'MOM.Link2_Ordered' [BMT__Hash__HPS]>>,)
    MOM.Link3
        (<bound method M_E_Type_Link3.sort_key of <class 'MOM.Link3' [BMT__Hash__HPS]>>,)
    MOM.Object
        (<bound method M_E_Type_Object.sort_key of <class 'MOM.Object' [BMT__Hash__HPS]>>,)
    MOM.Named_Object
        ('name',)
    BMT.Location
        ('lon', 'lat')
    BMT.Person
        ('last_name', 'first_name', 'middle_name')
    BMT.Rodent
        ('name',)
    BMT.Mouse
        ('name',)
    BMT.Rat
        ('name',)
    BMT.Beaver
        ('name',)
    BMT.Otter
        ('name',)
    BMT.Trap
        ('name', 'serial_no')
    BMT.Supertrap
        ('name', 'serial_no')
    BMT.Rodent_in_Trap
        ('left.name', 'right.name', 'right.serial_no')
    BMT.Person_owns_Trap
        ('left.last_name', 'left.first_name', 'left.middle_name', 'right.name', 'right.serial_no')
    BMT.Person_sets_Trap_at_Location
        ('left.last_name', 'left.first_name', 'left.middle_name', 'middle.name', 'middle.serial_no', 'right.lon', 'right.lat')

    >>> sorted (ET_Person.link_map, key = TFL.Getter.type_name)
    [<class 'BMT.Person_owns_Trap' [BMT__Hash__HPS]>,\
 <class 'BMT.Person_sets_Trap_at_Location' [BMT__Hash__HPS]>]
    >>> sorted (ET_Trap.link_map.iteritems (), key = TFL.Getter [0].type_name)
    [(<class 'BMT.Person_owns_Trap' [BMT__Hash__HPS]>, set([Trap `right`])),\
 (<class 'BMT.Person_sets_Trap_at_Location' [BMT__Hash__HPS]>,\
 set([Trap `middle`])), (<class 'BMT.Rodent_in_Trap' [BMT__Hash__HPS]>,\
 set([Trap `right`]))]

    .. ### DBW-specific finish

Scope
-----

A :class:`scope<_MOM.Scope.Scope>` manages the instances of essential
object and link types.

Specifying `None` as `db_uri` will create an in memory database::

    >>> scope = MOM.Scope.new (apt, None)

For each :attr:`~_MOM.Entity.PNS` defining essential
classes, the `scope` provides an object holding
:class:`object managers<_MOM.E_Type_Manager.Object>` and
:class:`link managers<_MOM.E_Type_Manager.Link>`
that support instance creation and queries:

    .. ### DBW-specific start

    >>> scope.MOM.Id_Entity
    <E_Type_Manager for MOM.Id_Entity of scope BMT__Hash__HPS>
    >>> scope.BMT.Person
    <E_Type_Manager for BMT.Person of scope BMT__Hash__HPS>
    >>> scope.BMT.Person_owns_Trap
    <E_Type_Manager for BMT.Person_owns_Trap of scope BMT__Hash__HPS>

    .. ### DBW-specific finish

.. _`essential-primary-keys`:

Identity
--------

Essential objects and links have identity, i.e., each object or link
can be uniquely identified. This identity is specified by a set of (so
called `primary`) attributes that together define the
`essential primary key`, short `epk`, for the entity in question. If
there is more than one primary attribute, the sequence of the
attributes is defined by their :attr:`rank` and :attr:`name`.

Essential objects identified by a simple, unstructured `name` are
defined by classes derived from
:class:`MOM.Named_Object<_MOM.Object.Named_Object>`. All other
essential objects are defined by classes derived from
:class:`MOM.Object<_MOM.Object.Object>` that specify one or more
essential attributes of kind :class:`~_MOM._Attr.Kind.Primary`.

Essential links are identified by the associated objects (the link's
roles) and any other, if any, primary attributes defined for the link
in question:

- Binary links are derived from :class:`MOM.Link2<_MOM.Link.Link2>`
  and identified by the link roles :attr:`left<_MOM.Link.Link2.left>`
  and :attr:`right<_MOM.Link.Link2.right>` plus any other primary
  attributes.

- Binary ordered links are derived from
  :class:`MOM.Link2_Ordered<_MOM.Link.Link2_Ordered>`
  and identified by the link roles
  :attr:`left<_MOM.Link.Link2_Ordered.left>`,
  :attr:`right<_MOM.Link.Link2_Ordered.right>`, and
  :attr:`seq_no<_MOM.Link.Link2_Ordered.seq_no>` plus any other primary
  attributes.

- Ternary links are derived from :class:`MOM.Link3<_MOM.Link.Link3>`
  and identified by the link roles :attr:`left<_MOM.Link.Link3.left>`,
  :attr:`middle<_MOM.Link.Link3.middle>`,
  and :attr:`right<_MOM.Link.Link3.right>` plus any other primary
  attributes.

Object and link creation
-------------------------

One creates objects or links by calling the etype manager of the
appropriate class:

    >>> scope.MOM.Named_Object (u"foo")
    Traceback (most recent call last):
      ...
    Partial_Type: MOM.Named_Object

    >>> p     = scope.BMT.Person     ("Luke", "Lucky")
    >>> p
    BMT.Person (u'Luke', u'Lucky', u'')
    >>> q     = scope.BMT.Person     (u"Dog",  u"Snoopy")
    >>> l1    = scope.BMT.Location   (-16.268799, 48.189956)
    >>> l2    = scope.BMT.Location   (-16.740770, 48.463313)
    >>> m     = scope.BMT.Mouse      (u"Mighty_Mouse")
    >>> b     = scope.BMT.Beaver     (u"Toothy_Beaver")
    >>> r     = scope.BMT.Rat        (u"Rutty_Rat")
    >>> axel  = scope.BMT.Rat        (u"Axel")
    >>> t1    = scope.BMT.Trap       ("X", 1)
    >>> t2    = scope.BMT.Trap       (u"X", 2)
    >>> t3    = scope.BMT.Trap       (u"Y", 1)
    >>> t4    = scope.BMT.Trap       (u"Y", 2)
    >>> t5    = scope.BMT.Trap       (u"Z", 3)

    >>> RiT   = scope.BMT.Rodent_in_Trap
    >>> PoT   = scope.BMT.Person_owns_Trap
    >>> PTL   = scope.BMT.Person_sets_Trap_at_Location

    >>> RiT (p, t4)
    Traceback (most recent call last):
      ...
    ValueError: BMT.Person (u'Luke', u'Lucky', u'') not eligible for attribute left,
        must be instance of BMT.Rodent
    >>> RiT (m, t1)
    BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1))
    >>> RiT (m, t2)
    Traceback (most recent call last):
      ...
    Multiplicity_Errors: BMT.Rodent_in_Trap, [Maximum number of links for u'Mighty_Mouse' is 1 ((BMT.Mouse (u'Mighty_Mouse'), BMT.Trap (u'X', 2)), [BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1))])]
    >>> RiT (r, t3)
    BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1))
    >>> RiT (axel, t2)
    BMT.Rodent_in_Trap ((u'Axel'), (u'X', 2))

    >>> PoT (p, t1)
    BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1))
    >>> PoT (p, t2)
    BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2))
    >>> PoT (q, t3)
    BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1))
    >>> PoT ((u"Tin", "Tin"), t4)
    BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2))

Creating a link will automatically set `auto_cached` attributes of the objects
participating of the link, like `Trap.setter` and `Trap.location`::

    >>> t1.setter, t1.location
    (None, None)
    >>> PTL (p, t1, l1)
    BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956))
    >>> t1.setter, t1.location
    (BMT.Person (u'Luke', u'Lucky', u''), BMT.Location (-16.268799, 48.189956))
    >>> t2.setter, t2.location
    (None, None)
    >>> PTL (p, t2, l2)
    BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313))
    >>> t2.setter, t2.location
    (BMT.Person (u'Luke', u'Lucky', u''), BMT.Location (-16.74077, 48.463313))
    >>> t3.setter, t3.location
    (None, None)
    >>> PTL (p, t3, l2)
    BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))
    >>> t3.setter, t3.location
    (BMT.Person (u'Luke', u'Lucky', u''), BMT.Location (-16.74077, 48.463313))

Queries
-------

One queries the object model by calling query methods of the
appropriate etype manager. Strict queries return only instances
of the essential class in question,
but not instances of derived classes. Non-strict queries are
transitive, i.e., they return instances of the essential class in
question and all its descendants. For partial types, strict queries
return nothing. By default, queries are non-strict (transitive).
Passing `strict = True` to a query makes it strict.

The query :meth:`instance<_MOM.E_Type_Manager.E_Type_Manager.instance>` can
only be applied to `E_Type_Managers` for essential types that are, or
inherit, a `relevant_root`:

    >>> scope.MOM.Object.instance (u"Mighty_Mouse")
    Traceback (most recent call last):
      ...
    TypeError: epkified_ckd() takes exactly 1 argument (2 given)
    >>> scope.MOM.Named_Object.instance ("Mighty_Mouse")
    Traceback (most recent call last):
      ...
    TypeError: Cannot query `instance` of non-root type `MOM.Named_Object`.
    Use one of the types BMT.Rodent, BMT.Trap instead.

    >>> scope.BMT.Rodent.instance (u"Mighty_Mouse")
    BMT.Mouse (u'Mighty_Mouse')
    >>> print scope.BMT.Rat.instance ("Mighty_Mouse")
    None

    >>> PoT.query_s ().all ()
    [BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2))]
    >>> PoT.instance ((u'Dog', u'Snoopy'), (u'Y', 1))
    BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1))
    >>> PoT.instance ((u'Dog', u'Snoopy', u''), (u'X', 2))
    >>> print PoT.instance (("Man", u"Tin"), t4)
    None

The query :meth:`exists<_MOM.E_Type_Manager.E_Type_Manager.exists>`
returns a list of all `E_Type_Managers` for which an object or link
with the specified `epk` exists:

    >>> scope.MOM.Named_Object.exists (u"Mighty_Mouse")
    [<E_Type_Manager for BMT.Mouse of scope BMT__Hash__HPS>]
    >>> scope.BMT.Mouse.exists ("Mighty_Mouse")
    [<E_Type_Manager for BMT.Mouse of scope BMT__Hash__HPS>]
    >>> scope.BMT.Rat.exists (u"Mighty_Mouse")
    []

    >>> PoT.exists ((u'Dog', u'Snoopy'), (u'Y', 1))
    [<E_Type_Manager for BMT.Person_owns_Trap of scope BMT__Hash__HPS>]
    >>> PoT.exists (("Man", u"Tin"), t4)
    []

The queries :attr:`~_MOM.E_Type_Manager.E_Type_Manager.count`,
:attr:`~_MOM.E_Type_Manager.E_Type_Manager.count_transitive`,
:meth:`~_MOM.E_Type_Manager.E_Type_Manager.query`, and
:meth:`~_MOM.E_Type_Manager.E_Type_Manager.r_query` return the
number, or list, of instances of the specified
etype:

    >>> scope.BMT.Mouse.count
    1
    >>> list (scope.BMT.Mouse.query_s (strict = True))
    [BMT.Mouse (u'Mighty_Mouse')]
    >>> scope.BMT.Mouse.count_transitive
    2
    >>> list (scope.BMT.Mouse.query_s ())
    [BMT.Mouse (u'Mighty_Mouse'), BMT.Beaver (u'Toothy_Beaver')]

    >>> scope.BMT.Rat.count
    2
    >>> list (scope.BMT.Rat.query_s (strict = True))
    [BMT.Rat (u'Axel'), BMT.Rat (u'Rutty_Rat')]
    >>> scope.BMT.Rat.count_transitive
    2
    >>> list (scope.BMT.Rat.query_s ())
    [BMT.Rat (u'Axel'), BMT.Rat (u'Rutty_Rat')]

    >>> scope.BMT.Rodent.count
    0
    >>> list (scope.BMT.Rodent.query_s (strict = True))
    []
    >>> scope.BMT.Rodent.count_transitive
    4
    >>> list (scope.BMT.Rodent.query_s ())
    [BMT.Rat (u'Axel'), BMT.Mouse (u'Mighty_Mouse'), BMT.Rat (u'Rutty_Rat'), BMT.Beaver (u'Toothy_Beaver')]

    >>> scope.MOM.Named_Object.count_transitive
    9
    >>> list (scope.MOM.Named_Object.query_s ())
    [BMT.Rat (u'Axel'), BMT.Mouse (u'Mighty_Mouse'), BMT.Rat (u'Rutty_Rat'), BMT.Beaver (u'Toothy_Beaver'), BMT.Trap (u'X', 1), BMT.Trap (u'X', 2), BMT.Trap (u'Y', 1), BMT.Trap (u'Y', 2), BMT.Trap (u'Z', 3)]
    >>> scope.MOM.Object.count_transitive
    14
    >>> list (scope.MOM.Object.query_s ())
    [BMT.Location (-16.74077, 48.463313), BMT.Location (-16.268799, 48.189956), BMT.Person (u'Dog', u'Snoopy', u''), BMT.Person (u'Luke', u'Lucky', u''), BMT.Person (u'Tin', u'Tin', u''), BMT.Rat (u'Axel'), BMT.Mouse (u'Mighty_Mouse'), BMT.Rat (u'Rutty_Rat'), BMT.Beaver (u'Toothy_Beaver'), BMT.Trap (u'X', 1), BMT.Trap (u'X', 2), BMT.Trap (u'Y', 1), BMT.Trap (u'Y', 2), BMT.Trap (u'Z', 3)]

    >>> list (scope.MOM.Id_Entity.query_s ())
    [BMT.Location (-16.74077, 48.463313), BMT.Location (-16.268799, 48.189956), BMT.Person (u'Dog', u'Snoopy', u''), BMT.Person (u'Luke', u'Lucky', u''), BMT.Person (u'Tin', u'Tin', u''), BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313)), BMT.Rat (u'Axel'), BMT.Mouse (u'Mighty_Mouse'), BMT.Rat (u'Rutty_Rat'), BMT.Beaver (u'Toothy_Beaver'), BMT.Rodent_in_Trap ((u'Axel'), (u'X', 2)), BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1)), BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1)), BMT.Trap (u'X', 1), BMT.Trap (u'X', 2), BMT.Trap (u'Y', 1), BMT.Trap (u'Y', 2), BMT.Trap (u'Z', 3)]
    >>> scope.MOM.Id_Entity.count_transitive
    24

    >>> scope.MOM.Link.count_transitive
    10
    >>> list (scope.MOM.Link.query_s ())
    [BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'Axel'), (u'X', 2)), BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1)), BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1))]
    >>> scope.MOM.Link2.count_transitive
    7
    >>> list (scope.MOM.Link2.query_s ())
    [BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2)), BMT.Rodent_in_Trap ((u'Axel'), (u'X', 2)), BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1)), BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1))]
    >>> scope.MOM.Link3.count_transitive
    3
    >>> list (scope.MOM.Link3.query_s ())
    [BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))]

    >>> sk_right_left = TFL.Sorted_By (RiT.right.sort_key, RiT.left.sort_key)
    >>> RiT.count_transitive
    3
    >>> show (RiT.query_s ())
    [((u'Axel'), (u'X', 2)), ((u'Mighty_Mouse'), (u'X', 1)), ((u'Rutty_Rat'), (u'Y', 1))]
    >>> show (RiT.query_s (sort_key = sk_right_left))
    [((u'Mighty_Mouse'), (u'X', 1)), ((u'Axel'), (u'X', 2)), ((u'Rutty_Rat'), (u'Y', 1))]

    >>> show (RiT.r_query_s (right = t1, strict = True))
    [((u'Mighty_Mouse'), (u'X', 1))]
    >>> show (RiT.r_query_s (trap = (u"X", 2)))
    [((u'Axel'), (u'X', 2))]
    >>> show (RiT.r_query_s (trap = (u"Y", "1"), strict = True))
    [((u'Rutty_Rat'), (u'Y', 1))]
    >>> show (RiT.r_query_s (right = m))
    []
    >>> show (RiT.r_query_s (left = "Foxy_Fox", strict = True))
    []

    >>> show (RiT.r_query_s (left = m))
    [((u'Mighty_Mouse'), (u'X', 1))]
    >>> show (RiT.r_query_s (rodent = u"Rutty_Rat"))
    [((u'Rutty_Rat'), (u'Y', 1))]
    >>> show (RiT.r_query_s (left = (u"Axel", ), strict = True))
    [((u'Axel'), (u'X', 2))]
    >>> show (RiT.r_query_s (left = "Jimmy", strict = True))
    []

    >>> PoT.count_transitive
    4
    >>> show (PoT.r_query_s (left = p))
    [((u'Luke', u'Lucky', u''), (u'X', 1)), ((u'Luke', u'Lucky', u''), (u'X', 2))]
    >>> show (PoT.r_query_s (person = (u"Dog",  u"Snoopy")))
    [((u'Dog', u'Snoopy', u''), (u'Y', 1))]

    >>> PTL.count_transitive
    3
    >>> show (PTL.r_query_s (left = p, trap = t1))
    [((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956))]
    >>> show (PTL.r_query_s (person = p, middle = (u"X", 2)))
    [((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (person = ("Luke", u"Lucky"), trap = t3, strict = True))
    [((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (left = q, middle = t1))
    []

    >>> show (PTL.r_query_s (left = p))
    [((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (location = (-16.74077, 48.463313)))
    [((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (trap = (u"Y", "1")))
    [((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (person = ("Tan", "Tan")))
    []

    >>> show (PTL.r_query_s (left = p))
    [((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (middle = (u'X', 2)))
    [((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (right = l1))
    [((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956))]
    >>> show (PTL.r_query_s (trap = t2, location = l2))
    [((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (middle = (u'Y', 1), right = l1))
    []
    >>> show (PTL.r_query_s (left = p, middle = (u'X', 2), right = l2))
    [((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (person = p, trap = (u'X', 2), location = l1))
    []
    >>> show (PTL.r_query_s (person = p, trap = ('X', 1), location = l1))
    [((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956))]
    >>> show (PTL.r_query_s (left = ("Tan", "Tan")))
    []

    >>> show (PTL.links_of (p))
    [((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))]

    >>> t1
    BMT.Trap (u'X', 1)
    >>> t1.all_links ()
    [BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1))]

    >>> list (scope)
    [BMT.Location (-16.268799, 48.189956), BMT.Location (-16.74077, 48.463313), BMT.Person (u'Luke', u'Lucky', u''), BMT.Person (u'Dog', u'Snoopy', u''), BMT.Person (u'Tin', u'Tin', u''), BMT.Mouse (u'Mighty_Mouse'), BMT.Beaver (u'Toothy_Beaver'), BMT.Rat (u'Rutty_Rat'), BMT.Rat (u'Axel'), BMT.Trap (u'X', 1), BMT.Trap (u'X', 2), BMT.Trap (u'Y', 1), BMT.Trap (u'Y', 2), BMT.Trap (u'Z', 3), BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1)), BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1)), BMT.Rodent_in_Trap ((u'Axel'), (u'X', 2)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2)), BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313))]

    >>> len (list (scope))
    24

Changing objects and links
---------------------------

    >>> old_id = axel.pid
    >>> axel.all_links ()
    [BMT.Rodent_in_Trap ((u'Axel'), (u'X', 2))]
    >>> axel.name = u"betty"
    Traceback (most recent call last):
      ...
    AttributeError: Primary attribute `BMT.Rat.name` cannot be assigned.
    Use `set` or `set_raw` to change it.
    >>> axel.set (name = "betty")
    1
    >>> axel
    BMT.Rat (u'betty')
    >>> axel.pid == old_id
    True
    >>> axel.all_links ()
    [BMT.Rodent_in_Trap ((u'betty'), (u'X', 2))]

    >>> m
    BMT.Mouse (u'Mighty_Mouse')
    >>> m.color, m.weight
    (None, None)
    >>> print m.as_code ()
    BMT.Mouse (u'Mighty_Mouse', )
    >>> m.color = "white"
    >>> print m.as_code ()
    BMT.Mouse (u'Mighty_Mouse', color = u'white')
    >>> m.weight = 0
    Traceback (most recent call last):
      ...
    Invariant_Error: Condition `AC_check_weight_0` :  (weight > 0)
        weight = 0.0
    >>> m.set (weight = -5.0)
    Traceback (most recent call last):
      ...
    Invariant_Errors: Condition `AC_check_weight_0` :  (weight > 0)
        weight = -5.0
    >>> m.weight = 10
    >>> print m.as_code ()
    BMT.Mouse (u'Mighty_Mouse', color = u'white', weight = 10.0)
    >>> m.set (color = "black", weight = 25.0)
    2
    >>> print m.as_code ()
    BMT.Mouse (u'Mighty_Mouse', color = u'black', weight = 25.0)
    >>> m.set (weight = "one ton")
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for float(): one ton
    >>> m.set_raw (weight = "one ton")
    Traceback (most recent call last):
      ...
    Invalid_Attribute: Can't set required attribute <u'Mighty_Mouse'>.weight to `one ton`
        `unexpected EOF while parsing (<string>, line 1)` for : `weight`
         expected type  : `Float`
         got      value : `one ton -> one ton`
         of       type  : `<type 'str'>`
    >>> m.set_raw (color = "yellow", weight = "42")
    3
    >>> m.color, m.weight
    (u'yellow', 42.0)
    >>> print m.as_code ()
    BMT.Mouse (u'Mighty_Mouse', color = u'yellow', weight = 42.0)

    >>> csk = TFL.Sorted_By (Q.parent != None, Q.cid)
    >>> for c in m.changes ().order_by (csk).all () :
    ...     print c
    <Create BMT.Mouse (u'Mighty_Mouse',)>
    <Modify BMT.Mouse (u'Mighty_Mouse',), old-values = {'color' : ''}, new-values = {'color' : u'white'}>
    <Modify BMT.Mouse (u'Mighty_Mouse',), old-values = {'weight' : u''}, new-values = {'weight' : u'10'}>
    <Modify BMT.Mouse (u'Mighty_Mouse',), old-values = {'color' : u'white', 'weight' : u'10'}, new-values = {'color' : u'black', 'weight' : u'25.0'}>
    <Modify BMT.Mouse (u'Mighty_Mouse',), old-values = {'color' : u'black', 'weight' : u'25.0'}, new-values = {'color' : u'yellow', 'weight' : '42'}>

    >>> mm = m.copy ("Magic_Mouse")
    >>> for c in mm.changes ().order_by (csk).all () :
    ...     print c
    <Copy BMT.Mouse (u'Magic_Mouse',)>
        <Create BMT.Mouse (u'Magic_Mouse',)>
        <Modify BMT.Mouse (u'Magic_Mouse',), old-values = {'color' : '', 'weight' : u''}, new-values = {'color' : u'yellow', 'weight' : '42'}>
    <Create BMT.Mouse (u'Magic_Mouse',)>
    <Modify BMT.Mouse (u'Magic_Mouse',), old-values = {'color' : '', 'weight' : u''}, new-values = {'color' : u'yellow', 'weight' : '42'}>

    >>> print l1.as_code ()
    BMT.Location (-16.268799, 48.189956, )
    >>> l1.set (lat =  91.5)
    Traceback (most recent call last):
      ...
    Invariant_Errors: Condition `AC_check_lat_1` :  (-90.0 <= lat <= 90.0)
        lat = 91.5
    >>> l1.set (lon = 270.0)
    Traceback (most recent call last):
      ...
    Invariant_Errors: Condition `AC_check_lon_1` :  (-180.0 <= lon <= 180.0)
        lon = 270.0
    >>> print l1.as_code ()
    BMT.Location (-16.268799, 48.189956, )

    >>> rit = RiT.instance (m, t1)
    >>> print rit.as_code ()
    BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1), )
    >>> print rit.rodent.as_code ()
    BMT.Mouse (u'Mighty_Mouse', color = u'yellow', weight = 42.0)
    >>> print rit.trap.as_code ()
    BMT.Trap (u'X', 1, )
    >>> print rit.is_g_correct ()
    True
    >>> rit.trap.max_weight = 20
    >>> print rit.is_g_correct ()
    False
    >>> for err in rit.errors :
    ...     print err
    Condition `valid_weight` : Weight of `rodent` must not exceed `max_weight` of `trap`. (rodent.weight <= trap.max_weight)
        rodent = u'Mighty_Mouse'
        trap = (u'X', 1)
        rodent.weight = 42.0
        trap.max_weight = 20.0

    >>> pot = PoT.instance (p, t1)
    >>> pot.price = decimal.Decimal ("1.20")
    >>> print pot.as_code ()
    BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1), price = 1.20)

Attribute queries
------------------

    >>> scope.BMT.Person.query_s (Q.last_name == Q.first_name).all ()
    [BMT.Person (u'Tin', u'Tin', u'')]
    >>> scope.BMT.Rodent.query_s (Q.weight != None).all ()
    [BMT.Mouse (u'Magic_Mouse'), BMT.Mouse (u'Mighty_Mouse')]
    >>> scope.BMT.Rodent.query_s (Q.weight == None).all ()
    [BMT.Rat (u'Rutty_Rat'), BMT.Beaver (u'Toothy_Beaver'), BMT.Rat (u'betty')]
    >>> scope.BMT.Rodent.query_s (Q.weight > 0).all ()
    [BMT.Mouse (u'Magic_Mouse'), BMT.Mouse (u'Mighty_Mouse')]
    >>> scope.BMT.Trap.query_s (Q.serial_no > 1).all ()
    [BMT.Trap (u'X', 2), BMT.Trap (u'Y', 2), BMT.Trap (u'Z', 3)]
    >>> scope.BMT.Trap.query_s (Q.serial_no < 2).all ()
    [BMT.Trap (u'X', 1), BMT.Trap (u'Y', 1)]
    >>> scope.BMT.Trap.query_s (Q.serial_no %% 2).all ()
    [BMT.Trap (u'X', 1), BMT.Trap (u'Y', 1), BMT.Trap (u'Z', 3)]
    >>> scope.BMT.Trap.query_s (Q.serial_no %% 2 == 0).all ()
    [BMT.Trap (u'X', 2), BMT.Trap (u'Y', 2)]

Renaming objects and links
--------------------------

    >>> b.all_links ()
    []
    >>> rit.set (left = b)
    1
    >>> print rit.as_code ()
    BMT.Rodent_in_Trap ((u'Toothy_Beaver'), (u'X', 1), )
    >>> b.all_links ()
    [BMT.Rodent_in_Trap ((u'Toothy_Beaver'), (u'X', 1))]
    >>> rit.rodent, rit.right
    (BMT.Beaver (u'Toothy_Beaver'), BMT.Trap (u'X', 1))

    .. ### DBW-specific start

    >>> rit.__class__.rodent, rit.__class__.right
    (Rodent `left`, Trap `right`)

    .. ### DBW-specific finish

    >>> rit.set (rodent = m)
    1
    >>> print rit.as_code ()
    BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1), )

Deleting objects and links
--------------------------

    >>> scope.MOM.Link.query_s ().all ()
    [BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'Mighty_Mouse'), (u'X', 1)), BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1)), BMT.Rodent_in_Trap ((u'betty'), (u'X', 2))]

    .. ### DBW-specific start

    >>> m.object_referring_attributes
    defaultdict(<type 'list'>, {})
    >>> sorted (d.type_name for d in m.dependencies)
    ['BMT.Rodent_in_Trap']
    >>> sorted (d.type_name for d in t1.dependencies)
    ['BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rodent_in_Trap']

    >>> m_id  = m.pid
    >>> t1_id = t1.pid
    >>> t2_id = t2.pid
    >>> show (scope.ems.all_links (m_id))
    [((u'Mighty_Mouse'), (u'X', 1))]
    >>> show (scope.ems.all_links (t1_id))
    [((u'Luke', u'Lucky', u''), (u'X', 1)), ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), ((u'Mighty_Mouse'), (u'X', 1))]

    .. ### DBW-specific finish

    >>> t1.catch
    BMT.Mouse (u'Mighty_Mouse')
    >>> m.destroy ()
    >>> t1.catch

    .. ### DBW-specific start

    >>> show (scope.ems.all_links (m_id))
    []

    >>> sorted (d.type_name for d in t1.dependencies)
    ['BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location']

    .. ### DBW-specific finish

    >>> scope.MOM.Link.query_s ().count ()
    9
    >>> scope.MOM.Link.r_query_s ().all ()
    [BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 1), (-16.268799, 48.189956)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1)), BMT.Rodent_in_Trap ((u'betty'), (u'X', 2))]

    >>> t1.destroy ()

    .. ### DBW-specific start

    >>> show (scope.ems.all_links (t1_id))
    []
    >>> show (scope.ems.all_links (t2_id))
    [((u'Luke', u'Lucky', u''), (u'X', 2)), ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), ((u'betty'), (u'X', 2))]

    .. ### DBW-specific finish

    >>> scope.MOM.Link.query_s ().all ()
    [BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Luke', u'Lucky', u''), (u'X', 2)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'X', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1)), BMT.Rodent_in_Trap ((u'betty'), (u'X', 2))]

    >>> t2.destroy ()
    >>> scope.MOM.Link.query_s ().all ()
    [BMT.Person_owns_Trap ((u'Dog', u'Snoopy', u''), (u'Y', 1)), BMT.Person_owns_Trap ((u'Tin', u'Tin', u''), (u'Y', 2)), BMT.Person_sets_Trap_at_Location ((u'Luke', u'Lucky', u''), (u'Y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'Rutty_Rat'), (u'Y', 1))]

    .. ### DBW-specific start

    >>> show (scope.ems.all_links (t2_id))
    []

    .. ### DBW-specific finish

Scope queries
--------------

    >>> for e in scope.i_incorrect () :
    ...     print list (e.errors)

    >>> for e in scope.g_incorrect () :
    ...     print list (str (x).replace (NL, " ") for x in e.errors)
    ['Condition `completely_defined` : All required attributes must be defined.      Required attribute Float `weight` is not defined']
    ['Condition `completely_defined` : All required attributes must be defined.      Required attribute Float `weight` is not defined']
    ['Condition `completely_defined` : All required attributes must be defined.      Required attribute Float `weight` is not defined']

    >>> len (scope.ems.uncommitted_changes)
    36
    >>> for c in scope.ems.uncommitted_changes :
    ...     print c
    <Create BMT.Person (u'Luke', u'Lucky', '')>
    <Create BMT.Person (u'Dog', u'Snoopy', '')>
    <Create BMT.Location (u'-16.268799', u'48.189956')>
    <Create BMT.Location (u'-16.74077', u'48.463313')>
    <Create BMT.Mouse (u'Mighty_Mouse',)>
    <Create BMT.Beaver (u'Toothy_Beaver',)>
    <Create BMT.Rat (u'Rutty_Rat',)>
    <Create BMT.Rat (u'Axel',)>
    <Create BMT.Trap (u'X', u'1')>
    <Create BMT.Trap (u'X', u'2')>
    <Create BMT.Trap (u'Y', u'1')>
    <Create BMT.Trap (u'Y', u'2')>
    <Create BMT.Trap (u'Z', u'3')>
    <Create BMT.Rodent_in_Trap (u"(u'Mighty_Mouse',)", u"(u'X', u'1')")>
    <Create BMT.Rodent_in_Trap (u"(u'Rutty_Rat',)", u"(u'Y', u'1')")>
    <Create BMT.Rodent_in_Trap (u"(u'Axel',)", u"(u'X', u'2')")>
    <Create BMT.Person_owns_Trap (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')")>
    <Create BMT.Person_owns_Trap (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'2')")>
    <Create BMT.Person_owns_Trap (u"(u'Dog', u'Snoopy', u'')", u"(u'Y', u'1')")>
    <Create BMT.Person (u'Tin', u'Tin', '')>
    <Create BMT.Person_owns_Trap (u"(u'Tin', u'Tin', u'')", u"(u'Y', u'2')")>
    <Create BMT.Person_sets_Trap_at_Location (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')", u"(u'-16.268799', u'48.189956')")>
    <Create BMT.Person_sets_Trap_at_Location (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'2')", u"(u'-16.74077', u'48.463313')")>
    <Create BMT.Person_sets_Trap_at_Location (u"(u'Luke', u'Lucky', u'')", u"(u'Y', u'1')", u"(u'-16.74077', u'48.463313')")>
    <Modify BMT.Rat (u'betty',), old-values = {'name' : u'Axel'}, new-values = {'name' : u'betty'}>
    <Modify BMT.Mouse (u'Mighty_Mouse',), old-values = {'color' : ''}, new-values = {'color' : u'white'}>
    <Modify BMT.Mouse (u'Mighty_Mouse',), old-values = {'weight' : u''}, new-values = {'weight' : u'10'}>
    <Modify BMT.Mouse (u'Mighty_Mouse',), old-values = {'color' : u'white', 'weight' : u'10'}, new-values = {'color' : u'black', 'weight' : u'25.0'}>
    <Modify BMT.Mouse (u'Mighty_Mouse',), old-values = {'color' : u'black', 'weight' : u'25.0'}, new-values = {'color' : u'yellow', 'weight' : '42'}>
    <Copy BMT.Mouse (u'Magic_Mouse',)>
        <Create BMT.Mouse (u'Magic_Mouse',)>
        <Modify BMT.Mouse (u'Magic_Mouse',), old-values = {'color' : '', 'weight' : u''}, new-values = {'color' : u'yellow', 'weight' : '42'}>
    <Modify BMT.Trap (u'X', u'1'), old-values = {'max_weight' : u''}, new-values = {'max_weight' : u'20'}>
    <Modify BMT.Person_owns_Trap (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')"), old-values = {'price' : u'42.0'}, new-values = {'price' : u'1.20'}>
    <Modify BMT.Rodent_in_Trap (u"(u'Toothy_Beaver',)", u"(u'X', u'1')"), old-values = {'left' : u"(u'Mighty_Mouse',)"}, new-values = {'left' : u"(u'Toothy_Beaver',)"}>
    <Destroy BMT.Mouse (u'Mighty_Mouse',), old-values = {'color' : u'yellow', 'weight' : '42'}>
        <Destroy BMT.Rodent_in_Trap (u"(u'Mighty_Mouse',)", u"(u'X', u'1')")>
    <Destroy BMT.Trap (u'X', u'1'), old-values = {'max_weight' : u'20'}>
        <Destroy BMT.Person_owns_Trap (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')"), old-values = {'price' : u'1.20'}>
        <Destroy BMT.Person_sets_Trap_at_Location (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')", u"(u'-16.268799', u'48.189956')")>
    <Destroy BMT.Trap (u'X', u'2')>
        <Destroy BMT.Person_owns_Trap (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'2')")>
        <Destroy BMT.Person_sets_Trap_at_Location (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'2')", u"(u'-16.74077', u'48.463313')")>
        <Destroy BMT.Rodent_in_Trap (u"(u'betty',)", u"(u'X', u'2')")>
    >>> c = scope.ems.uncommitted_changes [-2]
    >>> pckl = c.as_pickle (True)
    >>> cc = c.from_pickle (pckl)
    >>> cc
    <Destroy BMT.Trap (u'X', u'1'), old-values = {'max_weight' : u'20'}>
        <Destroy BMT.Person_owns_Trap (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')"), old-values = {'price' : u'1.20'}>
        <Destroy BMT.Person_sets_Trap_at_Location (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')", u"(u'-16.268799', u'48.189956')")>
    >>> cc.children
    [<Destroy BMT.Person_owns_Trap (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')"), old-values = {'price' : u'1.20'}>, <Destroy BMT.Person_sets_Trap_at_Location (u"(u'Luke', u'Lucky', u'')", u"(u'X', u'1')", u"(u'-16.268799', u'48.189956')")>]
    >>> cc.children [0].parent is cc
    True
    >>> pckl = c.as_pickle ()
    >>> cc = c.from_pickle (pckl)
    >>> cc
    <Destroy BMT.Trap (u'X', u'1'), old-values = {'max_weight' : u'20'}>
    >>> cc.children
    []
    >>> scope.commit ()
    >>> len (scope.ems.uncommitted_changes)
    0

Replaying changes
-----------------

    >>> scop2 = MOM.Scope.new (apt, None)
    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope, scop2))
    (16, 0)
    >>> for c in scope.query_changes (Q.parent == None).order_by (Q.cid) :
    ...     c.redo (scop2)
    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope, scop2))
    (16, 16)
    >>> sorted (scope.user_diff (scop2).iteritems ())
    []
    >>> scope.user_equal (scop2)
    True

    >>> t3.max_weight = 25
    >>> sorted (scope.user_diff (scop2).iteritems ())
    [(('BMT.Trap', (u'Y', u'1')), {'max_weight': (25.0, None)})]
    >>> scop2.BMT.Trap.instance (* t3.epk_raw, raw = True).set (max_weight = 42)
    1
    >>> sorted (scope.user_diff (scop2).iteritems ())
    [(('BMT.Trap', (u'Y', u'1')), {'max_weight': (25.0, 42.0)})]
    >>> t3.destroy ()
    >>> for diff in sorted (scop2.user_diff (scope).iteritems ()) :
    ...     print diff
    (('BMT.Person_owns_Trap', (u"(u'Dog', u'Snoopy', u'')", u"(u'Y', u'1')")), 'Present in Scope <None>, missing in Scope <None>')
    (('BMT.Person_sets_Trap_at_Location', (u"(u'Luke', u'Lucky', u'')", u"(u'Y', u'1')", u"(u'-16.74077', u'48.463313')")), 'Present in Scope <None>, missing in Scope <None>')
    (('BMT.Rodent_in_Trap', (u"(u'Rutty_Rat',)", u"(u'Y', u'1')")), 'Present in Scope <None>, missing in Scope <None>')
    (('BMT.Trap', (u'Y', u'1')), 'Present in Scope <None>, missing in Scope <None>')
    >>> scope.user_equal (scop2)
    False

Saving and re-loading changes from a database
----------------------------------------------

    >>> db_path   = %(db_path)s
    >>> db_uri    = %(db_uri)s
    >>> db_path_x = db_path + ".X"
    >>> if sos.path.exists (db_path) :
    ...     sos.remove (db_path)
    >>> if sos.path.exists (db_path_x) :
    ...     sos.rmdir (db_path_x, deletefiles = True)

    >>> scope.MOM.Id_Entity.count_transitive
    12
    >>> scop3 = scope.copy (apt, db_uri)
    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope, scop3))
    (12, 12)
    >>> sorted (scop3.user_diff (scope).iteritems ())
    []
    >>> scop3.destroy ()

    >>> scop4 = MOM.Scope.load (apt, db_uri)
    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope, scop4))
    (12, 12)
    >>> sorted (scope.user_diff (scop4).iteritems ())
    []
    >>> scop4.destroy ()

    >>> if sos.path.exists (db_path) :
    ...     sos.remove (db_path)

Primary key attributes
-----------------------

    >>> scope.BMT.Trap ("", None)
    Traceback (most recent call last):
    ...
    Invariant_Errors: Condition `AC_check_serial_no_0` :  (serial_no is not None and serial_no != '')
        serial_no = None, Condition `AC_check_name_0` :  (name is not None and name != '')
        name =
    >>> scope.BMT.Trap ("ha", None)
    Traceback (most recent call last):
    ...
    Invariant_Errors: Condition `AC_check_serial_no_0` :  (serial_no is not None and serial_no != '')
        serial_no = None
    >>> scope.BMT.Trap ("", 0)
    Traceback (most recent call last):
    ...
    Invariant_Errors: Condition `AC_check_name_0` :  (name is not None and name != '')
        name =
    >>> scope.BMT.Trap (None, 0)
    Traceback (most recent call last):
    ...
    Invariant_Errors: Condition `AC_check_name_0` :  (name is not None and name != '')
        name = None
    >>> scope.BMT.Trap ("ha", "", raw = True)
    Traceback (most recent call last):
    ...
    Invariant_Errors: Condition `AC_check_serial_no_0` :  (serial_no is not None and serial_no != '')
        serial_no = None
    >>> scope.BMT.Trap ("", "7", raw = True)
    Traceback (most recent call last):
    ...
    Invariant_Errors: Condition `AC_check_name_0` :  (name is not None and name != '')
        name =


"""

db_uri = "'/tmp/bmt_test.bmt'"

__doc__ = doctest = dt_form % dict \
    ( import_DBW = "from _MOM._DBW._HPS.Manager import Manager"
    , import_EMS = "from _MOM._EMS.Hash         import Manager"
    , db_path    = db_uri
    , db_uri     = db_uri
    )

from   _MOM.import_MOM        import *
from   _MOM.Product_Version   import Product_Version, IV_Number
from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _TFL                   import sos

BMT = Derived_Package_Namespace (parent = MOM, name = "_BMT")

Version = Product_Version \
    ( productid           = u"Better Mouse Trap"
    , productnick         = u"BMT"
    , productdesc         = u"Example application for MOM meta object model"
    , date                = "18-Dec-2009"
    , major               = 0
    , minor               = 5
    , patchlevel          = 42
    , author              = u"Christian Tanzer, Martin Glück"
    , copyright_start     = 2009
    , db_version          = IV_Number
        ( "db_version"
        , ("Better Mouse Trap", )
        , ("Better Mouse Trap", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".bmt"
        )
    , script_api_version  = IV_Number
        ( "script_api_version"
        , ("Better Mouse Trap", )
        , ("Example Client 1", "Example Client 2")
        , program_version = 1
        , comp_min        = 0
        )
    )

_Ancestor_Essence = MOM.Object

class Location (_Ancestor_Essence) :
    """Model a location of the Better Mouse Trap application."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        class lon (A_Float) :
            """Longitude """

            kind       = Attr.Primary
            rank       = 1
            min_value  = -180.0
            max_value  = +180.0
            ui_name    = "Longitude"

        # end class lon

        class lat (A_Float) :
            """Latitude"""

            kind       = Attr.Primary
            rank       = 2
            min_value  = -90.0
            max_value  = +90.0
            ui_name    = "Latitude"

        # end class lat

    # end class _Attributes

# end class Location

_Ancestor_Essence = MOM.Object

class Person (_Ancestor_Essence) :
    """Model a person of the Better Mouse Trap application."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        class last_name (A_String) :
            """Last name of person"""

            kind     = Attr.Primary
            rank     = 1
            ui_name  = "Last name"

        # end class last_name

        class first_name (A_String) :
            """First name of person"""

            kind     = Attr.Primary
            rank     = 2
            ui_name  = "First name"

        # end class first_name

        class middle_name (A_String) :
            """Middle name of person"""

            kind     = Attr.Primary_Optional
            default  = ""
            rank     = 1
            ui_name  = "Middle name"

        # end class middle_name

    # end class _Attributes

# end class Person

_Ancestor_Essence = MOM.Named_Object

class Rodent (_Ancestor_Essence) :
    """Model a rodent of the Better Mouse Trap application."""

    PNS    = BMT

    is_partial    = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        class color (A_String) :
            """Color of the rodent"""

            kind     = Attr.Optional

        # end class color

        class weight (A_Float) :
            """Weight of the rodent"""

            kind     = Attr.Required
            check    = ("value > 0", )

        # end class weight

    # end class _Attributes

# end class Rodent

_Ancestor_Essence = Rodent

class Mouse (_Ancestor_Essence) :
    """Model a mouse of the Better Mouse Trap application."""

# end class Mouse

_Ancestor_Essence = Rodent

class Rat (_Ancestor_Essence) :
    """Model a rat of the Better Mouse Trap application."""

# end class Rat

_Ancestor_Essence = Mouse

class Beaver (_Ancestor_Essence) :
    """Model a beaver of the Better Mouse Trap application."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        class region (A_String) :
            """In which are lives the beaver"""

            kind     = Attr.Optional

        # end class region

    # end class _Attributes

# end class Beaver

_Ancestor_Essence = Beaver

class Otter (_Ancestor_Essence) :

    class _Attributes (_Ancestor_Essence._Attributes) :

        class river (A_String) :

            kind       = Attr.Optional
            max_length = 20

        # end class river

    # end class _Attributes

# end class Otter

_Ancestor_Essence = MOM.Named_Object

class Trap (_Ancestor_Essence) :
    """Model a trap of the Better Mouse Trap application."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        class serial_no (A_Int) :
            """Serial number of the trap"""

            kind     = Attr.Primary
            ui_name  = "Serial number"

        # end class serial_no

        class max_weight (A_Float) :
            """Maximum weight of rodent the trap can hold"""

            kind     = Attr.Optional
            check    = ("value > 0", )
            ui_name  = "Maximum weight"

        # end class max_weight

    # end class _Attributes

# end class Trap

_Ancestor_Essence = Trap

class Supertrap (_Ancestor_Essence) :
    """An enormously improved Trap."""
# end class Supertrap

_Ancestor_Essence = MOM.Link2

class Rodent_in_Trap (_Ancestor_Essence) :
    """Model a rodent caught in a trap."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Rodent caught in Trap."""

            role_type     = Rodent
            max_links     = 1
            auto_cache    = "catch"

        # end class left

        class right (_Ancestor.right) :
            """Trap that caught a rodent."""

            role_type     = Trap
            max_links     = 1
            auto_cache    = "catcher"

        # end class right

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        class valid_weight (Pred.Condition) :
            """Weight of `rodent` must not exceed `max_weight` of `trap`."""

            kind          = Pred.System
            assertion     = "rodent.weight <= trap.max_weight"
            attributes    = ("rodent.weight", "trap.max_weight")

        # end class valid_weight

    # end class _Predicates


# end class Rodent_in_Trap

_Ancestor_Essence = MOM.Link2

class Person_owns_Trap (_Ancestor_Essence) :

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Person owning the Trap."""

            role_name     = "owner"
            role_type     = Person
            auto_cache    = True

        # end class left

        class right (_Ancestor.right) :
            """Trap owned by person."""

            role_type     = Trap
            max_links     = 1
            auto_cache    = True

        # end class right

        class price (A_Decimal) :
            kind          = Attr.Optional
            default       = 42.0
        # end class price

    # end class _Attributes

# end class Person_owns_Trap

_Ancestor_Essence = MOM.Link3

class Person_sets_Trap_at_Location (_Ancestor_Essence) :

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Person setting a trap."""

            role_type     = Person
            auto_cache    = MOM.Role_Cacher \
                ( attr_name       = "setter"
                , other_role_name = "middle"
                )

        # end class left

        class middle (_Ancestor.middle) :

            role_type     = Trap
            max_links     = 1

        # end class middle

        class right (_Ancestor.right) :
            """Location where a trap is set."""

            role_type     = Location
            auto_cache    = MOM.Role_Cacher (other_role_name = "middle")

        # end class right

    # end class _Attributes

# end class Person_sets_Trap_at_Location

def show (e) :
    if isinstance (e, (list, TFL._Q_Result_)) :
        print "[%s]" % (", ".join (str (x) for x in e), )
    else :
        print str (e)
# end def show

### All classes defining `__getslice__` have been changed to be
### compatible to Python 3.x by changing `__getitem__` to deal with
### slices
###
### Unfortunately, in Python 2.x `__getslice__` is still necessary and
### code like::
###
###     self.kill_callback [:]
###
### triggers the warning::
###
### DeprecationWarning: in 3.x, __getslice__ has been removed; use __getitem__
###
import warnings
warnings.filterwarnings \
    ( "ignore", "in 3.x, __getslice__ has been removed; use __getitem__")
if 0 :
    warnings.filterwarnings \
        ( "error",  "comparing unequal types not supported in 3.x")

### Because the example classes are all defined here and not in their
### own package namespace, we'll fake it
BMT._Export ("*", "Version")

NL = chr (10)

### __END__ MOM.__doc__
