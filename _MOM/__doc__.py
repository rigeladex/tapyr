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
#    MOM.__doc__
#
# Purpose
#    Test for MOM meta object model
#
# Revision Dates
#    18-Oct-2009 (CT) Creation
#     4-Nov-2009 (CT) Creation continued
#     4-Nov-2009 (MG) `Beaver` and `Otter` added
#    23-Nov-2009 (CT) Creation continued..
#    24-Nov-2009 (CT) Creation continued...
#    25-Nov-2009 (CT) Creation continued....
#    ««revision-date»»···
#--

"""
How to define and use essential object models
==============================================

Using `MOM`, an essential object model is specified by deriving
classes from :class:`MOM.Object<_MOM.Object.Object>`,
:class:`MOM.Named_Object<_MOM.Object.Named_Object>`, or from one of
the descendents of :class:`MOM.Link<_MOM.Link.Link>`.

Each essential class must be defined inside a
:class:`TFL.Package_Namespace<_TFL.Package_Namespace.Package_Namespace>`
and the class definition must contain an explicit or inherited
reference :attr:`Package_NS<_MOM.Entity.Package_NS>` to that package
namespace.

    Because the example classes are all defined here and not in their
    own package namespace, we'll fake it:

    >>> BMT._Export ("*")

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

    >>> import _MOM._EMS.Hash
    >>> import _MOM._DBW.Session
    >>> EMS   = MOM.EMS.Hash.Manager
    >>> DBW   = MOM.DBW.Session ### XXX change to a real DBW
    >>> apt   = MOM.App_Type ("BMT", BMT).Derived (EMS, DBW)

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

    >>> ET_Id_Entity = apt.entity_type ("MOM.Id_Entity")
    >>> ET_Named_Obj = apt.entity_type ("MOM.Named_Object")
    >>> ET_Person    = apt.entity_type ("BMT.Person")
    >>> ET_Mouse     = apt ["BMT.Mouse"]
    >>> ET_Rat       = apt ["BMT.Rat"]
    >>> ET_Rodent    = apt ["BMT.Rodent"]
    >>> ET_Trap      = apt ["BMT.Trap"]

    >>> for et in apt._T_Extension :
    ...   if (et.epk_sig and "__init__" in et.__dict__ and
    ...       hasattr (et.__init__, "source_code")) :
    ...     print "***", et.type_name, "***", et.__init__.i_bases
    ...     print et.__init__.source_code
    ...
    *** MOM.Link2 *** (<class 'MOM.Link' [BMT__Hash__XXX]>,)
    def __init__ (self, left, right, * args, ** kw) :
        return super (Link2, self).__init__ (left, right, * args, ** kw)
    <BLANKLINE>
    *** MOM.Link3 *** (<class 'MOM.Link2' [BMT__Hash__XXX]>,)
    def __init__ (self, left, middle, right, * args, ** kw) :
        return super (Link3, self).__init__ (left, middle, right, * args, ** kw)
    <BLANKLINE>
    *** MOM.Link2_Ordered *** (<class 'MOM.Link2' [BMT__Hash__XXX]>,)
    def __init__ (self, left, right, seq_no, * args, ** kw) :
        return super (Link2_Ordered, self).__init__ (left, right, seq_no, * args, ** kw)
    <BLANKLINE>
    *** MOM.Named_Object *** (<class 'MOM.Object' [BMT__Hash__XXX]>,)
    def __init__ (self, name, * args, ** kw) :
        return super (Named_Object, self).__init__ (name, * args, ** kw)
    <BLANKLINE>
    *** BMT.Location *** (<class 'MOM.Object' [BMT__Hash__XXX]>,)
    def __init__ (self, lon, lat, * args, ** kw) :
        return super (Location, self).__init__ (lon, lat, * args, ** kw)
    <BLANKLINE>
    *** BMT.Person *** (<class 'MOM.Object' [BMT__Hash__XXX]>,)
    def __init__ (self, last_name, first_name, * args, ** kw) :
        return super (Person, self).__init__ (last_name, first_name, * args, ** kw)
    <BLANKLINE>
    *** BMT.Trap *** (<class 'MOM.Object' [BMT__Hash__XXX]>,)
    def __init__ (self, cat, serial_no, * args, ** kw) :
        return super (Trap, self).__init__ (cat, serial_no, * args, ** kw)
    <BLANKLINE>

    >>> ET_Person
    <class 'BMT.Person' [BMT__Hash__XXX]>
    >>> ET_Person.Essence
    <class 'BMT.Person' [Bare Essence]>
    >>> ET_Person.E_Spec
    <class 'BMT.Person' [Spec Essence]>
    >>> ET_Person.last_name
    String `last_name`
    >>> ET_Person.last_name.__class__
    <class '_MOM._Attr.Kind.Primary'>
    >>> ET_Person.primary
    [String `last_name`, String `first_name`]
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
    [String `color`, Boolean `electric`, Int `is_used`, Name `name`,\
 Float `weight`, Boolean `x_locked`]

    >>> sorted (ET_Id_Entity.relevant_roots)
    ['BMT.Location', 'BMT.Person', 'BMT.Person_owns_Trap',\
 'BMT.Person_sets_Trap_at_Location', 'BMT.Rodent', 'BMT.Rodent_in_Trap',\
 'BMT.Trap']
    >>> ET_Person.relevant_root
    <class 'BMT.Person' [BMT__Hash__XXX]>
    >>> ET_Rodent.relevant_root
    <class 'BMT.Rodent' [BMT__Hash__XXX]>
    >>> ET_Mouse.relevant_root
    <class 'BMT.Rodent' [BMT__Hash__XXX]>

    >>> sorted (ET_Person.children)
    []
    >>> sorted (ET_Rodent.children)
    ['BMT.Mouse', 'BMT.Rat']
    >>> sorted (ET_Rodent.children.itervalues (), key = TFL.Getter.type_name)
    [<class 'BMT.Mouse' [BMT__Hash__XXX]>,\
 <class 'BMT.Rat' [BMT__Hash__XXX]>]
    >>> sorted (ET_Rat.children)
    []

    >>> sorted (apt.etypes)
    ['BMT.Beaver', 'BMT.Location', 'BMT.Mouse', 'BMT.Otter',\
 'BMT.Person', 'BMT.Person_owns_Trap',\
 'BMT.Person_sets_Trap_at_Location', 'BMT.Rat', 'BMT.Rodent',\
 'BMT.Rodent_in_Trap', 'BMT.Trap', 'MOM.An_Entity', 'MOM.Entity',\
 'MOM.Id_Entity', 'MOM.Link', 'MOM.Link2', 'MOM.Link2_Ordered',\
 'MOM.Link3', 'MOM.Named_Object', 'MOM.Object',\
 'MOM.Sequence_Number']
    >>> [t.type_name for t in apt._T_Extension]
    ['MOM.Entity', 'MOM.An_Entity', 'MOM.Id_Entity',\
 'MOM.Link', 'MOM.Link2', 'MOM.Link3', 'MOM.Link2_Ordered',\
 'MOM.Object', 'MOM.Named_Object', 'MOM.Sequence_Number',\
 'BMT.Location', 'BMT.Person', 'BMT.Rodent', 'BMT.Mouse', 'BMT.Rat',\
 'BMT.Beaver', 'BMT.Otter', 'BMT.Trap', 'BMT.Rodent_in_Trap',\
 'BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location']

    >>> sorted (ET_Person.link_map, key = TFL.Getter.type_name)
    [<class 'BMT.Person_owns_Trap' [BMT__Hash__XXX]>,\
 <class 'BMT.Person_sets_Trap_at_Location' [BMT__Hash__XXX]>]
    >>> sorted (ET_Trap.link_map.iteritems (), key = TFL.Getter [0].type_name)
    [(<class 'BMT.Person_owns_Trap' [BMT__Hash__XXX]>, set([Trap `right`])),\
 (<class 'BMT.Person_sets_Trap_at_Location' [BMT__Hash__XXX]>,\
 set([Trap `middle`])), (<class 'BMT.Rodent_in_Trap' [BMT__Hash__XXX]>,\
 set([Trap `right`]))]

Scope
-----

A :class:`scope<_MOM.Scope.Scope>` manages the instances of essential
object and link types.

    >>> scope = MOM.Scope (apt)

For each :attr:`~_MOM.Entity.Package_NS` defining essential
classes, the `scope` provides an object holding
:class:`object managers<_MOM.E_Type_Manager.Object>` and
:class:`link managers<_MOM.E_Type_Manager.Link2>`
that support instance creation and queries:

    >>> scope.MOM.Id_Entity
    <E_Type_Manager for MOM.Id_Entity of scope BMT__Hash__XXX>
    >>> scope.BMT.Person
    <E_Type_Manager for BMT.Person of scope BMT__Hash__XXX>
    >>> scope.BMT.Person_owns_Trap
    <E_Type_Manager for BMT.Person_owns_Trap of scope BMT__Hash__XXX>

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

    >>> scope.MOM.Named_Object ("foo")
    Traceback (most recent call last):
      ...
    Partial_Type: MOM.Named_Object

    >>> p     = scope.BMT.Person     ("Luke", "Lucky")
    >>> p
    BMT.Person ('Luke', 'Lucky')
    >>> q     = scope.BMT.Person     ("Dog",  "Snoopy")
    >>> l1    = scope.BMT.Location   (-16.268799, 48.189956)
    >>> l2    = scope.BMT.Location   (-16.740770, 48.463313)
    >>> m     = scope.BMT.Mouse      ("Mighty_Mouse")
    >>> b     = scope.BMT.Beaver     ("Toothy_Beaver")
    >>> r     = scope.BMT.Rat        ("Rutty_Rat")
    >>> axel  = scope.BMT.Rat        ("Axel")
    >>> t1    = scope.BMT.Trap       ("X", 1)
    >>> t2    = scope.BMT.Trap       ("X", 2)
    >>> t3    = scope.BMT.Trap       ("Y", 1)
    >>> t4    = scope.BMT.Trap       ("Y", 2)

    >>> RiT   = scope.BMT.Rodent_in_Trap
    >>> PoT   = scope.BMT.Person_owns_Trap
    >>> PTL   = scope.BMT.Person_sets_Trap_at_Location

    >>> RiT (m, t1)
    BMT.Rodent_in_Trap (('Mighty_Mouse'), ('X', 1))
    >>> RiT (m, t2)
    Traceback (most recent call last):
      ...
    Multiplicity_Errors: BMT.Rodent_in_Trap, [Maximum number of links for 'Mighty_Mouse' is 1 ((BMT.Mouse ('Mighty_Mouse'), BMT.Trap ('X', 2)), [BMT.Rodent_in_Trap (('Mighty_Mouse'), ('X', 1))])]
    >>> RiT (r, t3)
    BMT.Rodent_in_Trap (('Rutty_Rat'), ('Y', 1))
    >>> RiT (axel, t2)
    BMT.Rodent_in_Trap (('Axel'), ('X', 2))
    >>> RiT (p, t4)
    Traceback (most recent call last):
      ...
    ValueError: BMT.Person ('Luke', 'Lucky') not eligible for attribute left,
        must be instance of BMT.Rodent

    >>> PoT (p, t1)
    BMT.Person_owns_Trap (('Luke', 'Lucky'), ('X', 1))
    >>> PoT (p, t2)
    BMT.Person_owns_Trap (('Luke', 'Lucky'), ('X', 2))
    >>> PoT (q, t3)
    BMT.Person_owns_Trap (('Dog', 'Snoopy'), ('Y', 1))
    >>> PoT (("Tin", "Tin"), t4)
    BMT.Person_owns_Trap (('Tin', 'Tin'), ('Y', 2))

    >>> PTL (p, t1, l1)
    BMT.Person_sets_Trap_at_Location (('Luke', 'Lucky'), ('X', 1), (-16.268799, 48.189956))
    >>> PTL (p, t2, l2)
    BMT.Person_sets_Trap_at_Location (('Luke', 'Lucky'), ('X', 2), (-16.74077, 48.463313))
    >>> PTL (p, t3, l2)
    BMT.Person_sets_Trap_at_Location (('Luke', 'Lucky'), ('Y', 1), (-16.74077, 48.463313))

Queries
-------

One queries the object model by calling query methods of the
appropriate etype manager. Queries starting with `s_` are strict,
i.e., they return only instances of the essential class in question,
but not instances of derived classes. Queries starting with `t_` are
transitive, i.e., they return instances of the essential class in
question and all its descendents. For partial types, strict queries
return nothing.


The query :meth:`instance<_MOM.E_Type_Manager.E_Type_Manager.instance>` can
only be applied to `E_Type_Managers` for essential types that are or
inherit a `relevant_root`:

    >>> scope.MOM.Object.instance ("Mighty_Mouse")
    Traceback (most recent call last):
      ...
    TypeError: Cannot query `instance` of non-root type `MOM.Object`.
    Use one of the types BMT.Location, BMT.Person, BMT.Rodent, BMT.Trap instead.
    >>> scope.MOM.Named_Object.instance ("Mighty_Mouse")
    Traceback (most recent call last):
      ...
    TypeError: Cannot query `instance` of non-root type `MOM.Named_Object`.
    Use one of the types BMT.Rodent instead.

    >>> scope.BMT.Rodent.instance ("Mighty_Mouse")
    BMT.Mouse ('Mighty_Mouse')
    >>> print scope.BMT.Rat.instance ("Mighty_Mouse")
    None

    >>> PoT.instance (('Dog', 'Snoopy'), ('Y', 1))
    BMT.Person_owns_Trap (('Dog', 'Snoopy'), ('Y', 1))
    >>> PoT.instance (('Dog', 'Snoopy'), ('X', 2))
    >>> print PoT.instance (("Man", "Tin"), t4)
    None

The query :meth:`exists<_MOM.E_Type_Manager.E_Type_Manager.exists>`
returns a list of all `E_Type_Managers` for which an object or link
with the specified `epk` exists:

    >>> scope.MOM.Named_Object.exists ("Mighty_Mouse")
    [<E_Type_Manager for BMT.Mouse of scope BMT__Hash__XXX>]
    >>> scope.BMT.Mouse.exists ("Mighty_Mouse")
    [<E_Type_Manager for BMT.Mouse of scope BMT__Hash__XXX>]
    >>> scope.BMT.Rat.exists ("Mighty_Mouse")
    []

    >>> PoT.exists (('Dog', 'Snoopy'), ('Y', 1))
    [<E_Type_Manager for BMT.Person_owns_Trap of scope BMT__Hash__XXX>]
    >>> PoT.exists (("Man", "Tin"), t4)
    []

The queries :meth:`~_MOM.E_Type_Manager.E_Type_Manager.s_count`,
:meth:`~_MOM.E_Type_Manager.E_Type_Manager.t_count`,
:meth:`~_MOM.E_Type_Manager.E_Type_Manager.s_extension`, and
:meth:`~_MOM.E_Type_Manager.E_Type_Manager.t_extension` return the
number, or list, of strict or transitive instances of the specified
etype:

    >>> scope.BMT.Mouse.s_count
    1
    >>> scope.BMT.Mouse.s_extension ()
    [BMT.Mouse ('Mighty_Mouse')]
    >>> scope.BMT.Mouse.t_count
    2
    >>> scope.BMT.Mouse.t_extension ()
    [BMT.Mouse ('Mighty_Mouse'), BMT.Beaver ('Toothy_Beaver')]

    >>> scope.BMT.Rat.s_count
    2
    >>> scope.BMT.Rat.s_extension ()
    [BMT.Rat ('Axel'), BMT.Rat ('Rutty_Rat')]
    >>> scope.BMT.Rat.t_count
    2
    >>> scope.BMT.Rat.t_extension ()
    [BMT.Rat ('Axel'), BMT.Rat ('Rutty_Rat')]

    >>> scope.BMT.Rodent.s_count
    0
    >>> scope.BMT.Rodent.s_extension ()
    []
    >>> scope.BMT.Rodent.t_count
    4
    >>> scope.BMT.Rodent.t_extension ()
    [BMT.Rat ('Axel'), BMT.Mouse ('Mighty_Mouse'), BMT.Rat ('Rutty_Rat'), BMT.Beaver ('Toothy_Beaver')]

    >>> scope.MOM.Named_Object.t_count
    4
    >>> scope.MOM.Named_Object.t_extension ()
    [BMT.Rat ('Axel'), BMT.Mouse ('Mighty_Mouse'), BMT.Rat ('Rutty_Rat'), BMT.Beaver ('Toothy_Beaver')]
    >>> scope.MOM.Object.t_count
    13
    >>> scope.MOM.Object.t_extension ()
    [BMT.Location (-16.74077, 48.463313), BMT.Location (-16.268799, 48.189956), BMT.Person ('Dog', 'Snoopy'), BMT.Person ('Luke', 'Lucky'), BMT.Person ('Tin', 'Tin'), BMT.Rat ('Axel'), BMT.Mouse ('Mighty_Mouse'), BMT.Rat ('Rutty_Rat'), BMT.Beaver ('Toothy_Beaver'), BMT.Trap ('X', 1), BMT.Trap ('X', 2), BMT.Trap ('Y', 1), BMT.Trap ('Y', 2)]

    >>> scope.MOM.Id_Entity.t_count
    23

    >>> sk_right_left = TFL.Sorted_By (RiT.right.sort_key, RiT.left.sort_key)
    >>> RiT.t_count
    3
    >>> show (RiT.t_extension ())
    [(('Axel'), ('X', 2)), (('Mighty_Mouse'), ('X', 1)), (('Rutty_Rat'), ('Y', 1))]
    >>> show (RiT.t_extension (sk_right_left))
    [(('Mighty_Mouse'), ('X', 1)), (('Axel'), ('X', 2)), (('Rutty_Rat'), ('Y', 1))]

    >>> show (RiT.s_left (t1))
    [(('Mighty_Mouse'), ('X', 1))]
    >>> show (RiT.t_left (("X", 2)))
    [(('Axel'), ('X', 2))]
    >>> show (RiT.s_left (("Y", "1")))
    [(('Rutty_Rat'), ('Y', 1))]
    >>> show (RiT.t_left (m))
    []
    >>> show (RiT.s_left ("Foxy_Fox"))
    []

    >>> show (RiT.s_right (m))
    [(('Mighty_Mouse'), ('X', 1))]
    >>> show (RiT.s_right ("Rutty_Rat"))
    [(('Rutty_Rat'), ('Y', 1))]
    >>> show (RiT.s_right (("Axel", )))
    [(('Axel'), ('X', 2))]
    >>> show (RiT.s_right ("Jimmy", ))
    []

    >>> show (PoT.trap (p))
    [(('Luke', 'Lucky'), ('X', 1)), (('Luke', 'Lucky'), ('X', 2))]
    >>> show (PoT.trap (("Dog",  "Snoopy")))
    [(('Dog', 'Snoopy'), ('Y', 1))]

    >>> show (PTL.s_right (p, t1))
    [(('Luke', 'Lucky'), ('X', 1), (-16.268799, 48.189956))]
    >>> show (PTL.s_right (p, ("X", 2)))
    [(('Luke', 'Lucky'), ('X', 2), (-16.74077, 48.463313))]
    >>> show (PTL.s_right (("Luke", "Lucky"), t3))
    [(('Luke', 'Lucky'), ('Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.s_right (q, t1))
    []

    >>> show (PTL.s_middle_right (p))
    [(('Luke', 'Lucky'), ('X', 1), (-16.268799, 48.189956)), (('Luke', 'Lucky'), ('X', 2), (-16.74077, 48.463313)), (('Luke', 'Lucky'), ('Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.s_left_middle  ((-16.74077, 48.463313)))
    [(('Luke', 'Lucky'), ('X', 2), (-16.74077, 48.463313)), (('Luke', 'Lucky'), ('Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.s_left_right   (("Y", "1")))
    [(('Luke', 'Lucky'), ('Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.s_middle_right (("Tan", "Tan")))
    []

    >>> show (PTL.s_links_of (l = p))
    [(('Luke', 'Lucky'), ('X', 1), (-16.268799, 48.189956)), (('Luke', 'Lucky'), ('X', 2), (-16.74077, 48.463313)), (('Luke', 'Lucky'), ('Y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.s_links_of (m = ('X', 2)))
    [(('Luke', 'Lucky'), ('X', 2), (-16.74077, 48.463313))]
    >>> show (PTL.s_links_of (r = l1))
    [(('Luke', 'Lucky'), ('X', 1), (-16.268799, 48.189956))]
    >>> show (PTL.s_links_of (m = ('X', 2), r = l2))
    [(('Luke', 'Lucky'), ('X', 2), (-16.74077, 48.463313))]
    >>> show (PTL.s_links_of (m = ('Y', 1), r = l1))
    []
    >>> show (PTL.s_links_of (l = p, m = ('X', 2), r = l2))
    [(('Luke', 'Lucky'), ('X', 2), (-16.74077, 48.463313))]
    >>> show (PTL.s_links_of (l = p, m = ('X', 2), r = l1))
    []
    >>> show (PTL.s_links_of (l = p, m = ('X', 1), r = l1))
    [(('Luke', 'Lucky'), ('X', 1), (-16.268799, 48.189956))]
    >>> show (PTL.s_links_of (l = ("Tan", "Tan")))
    []

    >>> t1
    BMT.Trap ('X', 1)
    >>> t1.all_links ()
    [BMT.Person_owns_Trap (('Luke', 'Lucky'), ('X', 1)),\
 BMT.Person_sets_Trap_at_Location\
 (('Luke', 'Lucky'), ('X', 1), (-16.268799, 48.189956)),\
 BMT.Rodent_in_Trap (('Mighty_Mouse'), ('X', 1))]

"""

from   _MOM.import_MOM       import *

BMT = TFL.Package_Namespace ("_BMT")

class Location (MOM.Object) :
    """Model a location of the Better Mouse Trap application."""

    Package_NS = BMT

    is_partial = False

    class _Attributes (MOM.Object._Attributes) :

        class lon (A_Float) :
            """Longitude """

            kind     = Attr.Primary
            rank     = 1

        # end class lon

        class lat (A_Float) :
            """Latitude"""

            kind     = Attr.Primary
            rank     = 2

        # end class lat

    # end class _Attributes

# end class Location

class Person (MOM.Object) :
    """Model a person of the Better Mouse Trap application."""

    Package_NS = BMT

    is_partial = False

    class _Attributes (MOM.Object._Attributes) :

        class last_name (A_String) :
            """Last name of person"""

            kind     = Attr.Primary
            rank     = 1

        # end class last_name

        class first_name (A_String) :
            """First name of person"""

            kind     = Attr.Primary
            rank     = 2

        # end class first_name

    # end class _Attributes

# end class Person

class Rodent (MOM.Named_Object) :
    """Model a rodent of the Better Mouse Trap application."""

    Package_NS = BMT

    class _Attributes (MOM.Named_Object._Attributes) :

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

class Mouse (Rodent) :
    """Model a mouse of the Better Mouse Trap application."""

    is_partial = False

# end class Mouse

class Rat (Rodent) :
    """Model a rat of the Better Mouse Trap application."""

    is_partial = False

# end class Rat

class Beaver (Mouse) :
    """Model a beaver of the Better Mouse Trap application."""

    class _Attributes (Mouse._Attributes) :

        class region (A_String) :
            """In wich are lives the beaver"""

            kind     = Attr.Optional

        # end class region

    # end class _Attributes

# end class Beaver

class Otter (Beaver) :

    class _Attributes (Beaver._Attributes) :

        class river (A_String) :

            kind       = Attr.Optional
            max_length = 20

        # end class river

    # end class _Attributes

# end class Otter

class Trap (MOM.Object) :
    """Model a trap of the Better Mouse Trap application."""

    Package_NS = BMT

    is_partial = False

    class _Attributes (MOM.Object._Attributes) :

        class cat (A_String) :
            """Category of the trap"""

            kind     = Attr.Primary

        # end class cat

        class serial_no (A_Int) :
            """Serial number of the trap"""

            kind     = Attr.Primary

        # end class serial_no

        class max_weight (A_Float) :
            """Maximum weight of rodent the trap can hold"""

            kind     = Attr.Optional
            check    = ("value > 0", )

        # end class max_weight

    # end class _Attributes

# end class Trap

class Rodent_in_Trap (MOM.Link2) :
    """Model a rodent caught in a trap."""

    Package_NS = BMT

    is_partial = False

    class _Attributes (MOM.Link2._Attributes) :

        class left (MOM.Link2._Attributes.left) :
            """Rodent caught in Trap."""

            role_type     = Rodent
            max_links     = 1

        # end class left

        class right (MOM.Link2._Attributes.right) :
            """Trap that caught a rodent."""

            role_type     = Trap
            max_links     = 1

        # end class right

    # end class _Attributes

# end class Rodent_in_Trap

class Person_owns_Trap (MOM.Link2) :

    Package_NS = BMT

    is_partial = False

    class _Attributes (MOM.Link2._Attributes) :

        class left (MOM.Link2._Attributes.left) :
            """Person owning the Trap."""

            role_type     = Person

        # end class left

        class right (MOM.Link2._Attributes.right) :
            """Trap owned by person."""

            role_type     = Trap
            max_links     = 1

        # end class right

    # end class _Attributes

# end class Person_owns_Trap

class Person_sets_Trap_at_Location (MOM.Link3) :

    Package_NS = BMT

    is_partial = False

    class _Attributes (MOM.Link2._Attributes) :

        class left (MOM.Link2._Attributes.left) :

            role_type     = Person

        # end class left

        class middle (MOM.Link2._Attributes.right) :

            role_type     = Trap
            max_links     = 1

        # end class middle

        class right (MOM.Link2._Attributes.right) :

            role_type     = Location

        # end class right

    # end class _Attributes

# end class Person_sets_Trap_at_Location

def show (e) :
    if isinstance (e, list) :
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

### __END__ MOM.__doc__
