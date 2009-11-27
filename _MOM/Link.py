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
#    MOM.Link
#
# Purpose
#    Root class for link-types of MOM meta object model
#
# Revision Dates
#    22-Oct-2009 (CT) Creation (factored from TOM.Link)
#     4-Nov-2009 (CT) `Link2` added
#    20-Nov-2009 (CT) `Link3` and `Link2_Ordered` added
#    20-Nov-2009 (CT) Documentation added
#    26-Nov-2009 (CT) `Role_Cacher` added
#    26-Nov-2009 (CT) `_init_epk` and `destroy` redefined to handle
#                     `auto_cache_roles`
#    27-Nov-2009 (CT) `Role_Cacher.setup` changed to store `other_role`
#                     instead of `other_role_name`
#    ««revision-date»»···
#--

from   _TFL      import TFL
from   _MOM      import MOM

from   _MOM._Attr.Type import *
from   _MOM._Attr      import Attr
from   _MOM._Pred      import Pred

import  _MOM._Meta.M_Link

import _MOM.Entity

class _MOM_Link_ (MOM.Id_Entity) :
    """Root class for link-types of MOM meta object model."""

    __metaclass__         = MOM.Meta.M_Link
    _real_name            = "Link"
    entity_kind           = "link"
    is_synthetic          = False

    @property
    def roles (self) :
        return self.epk [:self.number_of_roles]
    # end def roles

    def _init_epk (self, setter, * epk) :
        self.__super._init_epk (setter, * epk)
        for role_cacher in self.auto_cache_roles :
            role_cacher (self, no_value = False)
    # end def

    def destroy (self) :
        for role_cacher in self.auto_cache_roles :
            role_cacher (self, no_value = True)
        self.__super.destroy ()
    # end def destroy

Link = _MOM_Link_ # end class

class Link2 (Link) :
    """Model an entity-based link of a binary association of the MOM meta
       object model.
    """

    __metaclass__         = MOM.Meta.M_Link2

    class _Attributes (Link._Attributes) :

        class left (_A_Link_Role_Left_, A_Link_Role_EB) :
            """Left role of association. Override to define `role_type`, ..."""

        # end class left

        class right (_A_Link_Role_Right_, A_Link_Role_EB) :
            """Right role of association. Override to define `role_type`, ..."""

        # end class right

    # end class _Attributes

# end class Link2

class Link3 (Link2) :
    """Model a link of a ternary essential association of the MOM meta
       object model.
    """

    __metaclass__         = MOM.Meta.M_Link3

    class _Attributes (Link2._Attributes) :

        class middle (_A_Link_Role_Middle_, A_Link_Role_EB) :
            """Middle role of association. Override to define `role_type`, ..."""

        # end class middle

    # end class _Attributes

# end class Link3

class Link2_Ordered (Link2) :
    """Model a link of a binary ordered essential association of the MOM meta
       object model.
    """

    __metaclass__         = MOM.Meta.M_Link2_Ordered

    class _Attributes (Link2._Attributes) :

        class seq_no (_A_Link_Role_Seq_No_, A_Link_Role_EB) :
            """Sequence-number role of association. Override to define `role_type`, ..."""

        # end class seq_no

    # end class _Attributes

# end class Link2_Ordered

class Role_Cacher (TFL.Meta.Object) :

    def __init__ (self, attr_name = None, other_role_name = None) :
        self.role_name       = None
        self.attr_name       = attr_name
        self.other_role_name = other_role_name
        self.other_role      = None
    # end def __init__

    def __call__ (self, link, no_value = False) :
        assert self.role_name is not None
        o = getattr (link, self.other_role.name)
        if o is not None :
            if no_value :
                value = None
            else :
                value = getattr (link, self.role_name)
            setattr (o, self.attr_name, value)
    # end def __call__

    def setup (self, Link, role) :
        assert self.role_name is None
        self.role_name = role_name = role.role_name
        attr_name      = self.attr_name
        if attr_name is None or attr_name == True :
            self.attr_name = role_name
        assert isinstance (self.attr_name, basestring)
        other_role_name = \
            self.other_role_name or Link.other_role_name (role.name)
        self.other_role = getattr (Link._Attributes, other_role_name)
        del self.other_role_name
    # end def setup

# end class Role_Cacher

__doc__ = """
Class `MOM.Link`
================

.. class:: Link

    `MOM.Link` provides the framework for defining essential
    associations. It is based on :class:`~_MOM.Entity.Id_Entity`.

    An association models the relationship between two or
    more objects of essential classes. An association manages the set
    of links between the objects of the associated classes.
    Conceptually, each link is an independent entity.

    The class `Link` simultaneously models two concepts:

    - The class `Link` itself models the association, i.e., the
      collection of all links.

      The behavior of the association is provided by the methods and
      properties of the link manager
      :class:`MOM.E_Type_Manager<_MOM.E_Type_Manager.E_Type_Manager>`.

    - Each instance of `Link` models one specific link of the association.

    Each essential association is characterized by:

    - `arity`_

    - `roles`_

    - `multiplicity`_

    Each association can be implemented in one of two ways:

    - `entity-based links`_ (derived from a `arity`_-specific descendent
      of :class:`Link_EB`)

    - `attribute-based links`_ (derived from :class:`~_MOM.Link_AB.Link2_AB`)

    From a client's point of view, entity-based links and
    attribute-based links are compatible to each other.

Arity
-----

Arity defines how many objects one link comprises. A binary
association relates pairs of objects to each other, a ternary
association relates triples of objects to each other, and so on.

For each arity, a separate subclass exists, e.g.,
:class:`Link2`, :class:`Link3`, etc. Each arity-specific subclass has
its own arity-specific metaclass, e.g., :class:`M_Link2_Ordered` defines the
behavior of :class:`Link2_Ordered`.

An essential association is modelled by a class that inherits from the
proper arity-specific descendent of :class:`Link_EB` or
:class:`~_MOM.Link_AB.Link_AB`.

.. autoclass:: Link2()
.. autoclass:: Link2_Ordered()
.. autoclass:: Link3()

.. autoclass:: _MOM.Link_AB.Link2_AB()

Roles
-----

Each object participating in a link of an association plays a specific
`role`. A role is characterized by:

* Role type: the type of essential object expected.

* Role name (default `role_type.type_base_name.lower ()`).

  - If an association links objects of the same types in different
    roles to each other, at least one, preferably all of these roles
    need a unique role name that's different from the default role
    name.

* Generic role name (e.g., `left` or `right`).

* Role abbreviation (e.g., `l` or `r`).

* Multiplicity constraint, if any.

* Non-essential properties:

  - `dfc_synthesizer` (see `dfc-synthesis`_)

  - `auto_cache` (see `auto-caching`_)

Each role of a specific association is defined by a link-role attribute named
by the generic role name. For a specific association, the link-role attribute

  * Must define :attr:`role_type` (unless that's already inherited).

  * May define :attr:`role_name`, multiplicity constraints
    (:attr:`max_links`) or any non-essential property of the role.

For instance::

    class Person_works_for_Company (Link2) :

        class _Attributes (Link2._Attributes) :

            class left (Link2._Attributes.left) :
                role_type   = Person
                role_name   = "employee"
                auto_cache  = True
                max_links   = 1 ### Danger, Will Robinson
            # end class left

            class right (Link2._Attributes.right) :
                role_type   = Company
                role_name   = "employer"
            # end class right

        # end class _Attributes

Multiplicity
------------

Multiplicity restricts how many links can exist for a single object
in a specific role. Constraints on multiplicity frequently change over
the lifetime of a software application.

Common multiplicities (of binary associations) are:

- 1 <--> 1

- 1 <--> n

- n <--> m

Associations with at least one role with multiplicity 1 could be
implemented by an attribute of the respective object instead of an
association. Any change of requirements might invalidate that
implementation, though. Therefore, `Link2_AB` should be used instead
to implement such associations (changing `Link2_AB` to `Link2` does
not invalidate clients of the association).

Simple multiplicity constraints are implemented by defining
`max_links` for the appropriate role. In this case, the `Link` class
will enforce the constraint.

Entity-based Links
------------------

Entity-based links are implemented as independent entities, e.g., for
each life link of the association a separate instance of `Link`
exists.

This is the fully general way to implement associations and supports:

- any kind of arity

- link attributes

- link predicates

The downside is increased memory consumption which in turn might mean
increased run-time.

:class:`Link_EB` provides the framework for entity-based links.

Attribute-based Links
---------------------

Attribute-based links are implemented by storing the information about
a specific link in attributes of the linked objects instead of a
independent link instance.

Attribute-based links are applicable only for binary links

- with at least one role restricted to `multiplicity`_ 1

- without link attributes

- without link predicates

The upside is greatly reduced memory consumption which might reduce
run-time.

:class:`~_MOM.Link_AB.Link_AB` provides the framework for
attribute-based links.

Queries to associations implemented with attribute-based links will
return synthetic link instances that live only as long as the client
retains the query result.

DFC-Synthesis
-------------

Some object models allow recursive structures of the form:

- A container-like class `C` inherits from class `X`. `C` thus is
  substitutable for `X` and can participate in all associations
  defined for `X`.

- An association `X_in_C` that defines a container-like association
  with the multiplicity constraint that each instance of `X` is
  restricted to a single link to `C`.

In many such models, the instances of `X` linked to a specific
container `c` should reflect the links `c` itself participates in. To
avoid numerous redundant links, the module :mod:`~_MOM.DFC_Link`
provides classes that allow the automatic synthesis of links derived
from a container association.

DFC-synthesis is specified for the association that needs synthetic
`DFC_Links` by defining the property `dfc_synthesizer` (which must be
an instance of a subclass of :class:`~_MOM.DFC_Link.DFC_Synthesizer`)
for the role related to `X`.

For instance, given `C`, `X`, and `X_in_C` as described above,
DFC-synthesis for an association `X_has_P` would be defined like::

    class X_has_P (Link2) :

        class _Attributes (Link2._Attributes) :

            class left (Link2._Attributes.left) :
                role_type       = X
                dfc_synthesizer = MOM.DFC_Synthesizer_LL (X_in_C)
            # end class left

            class right (Link2._Attributes.right) :
                role_type       = P
            # end class right

        # end class _Attributes


Auto-Caching
------------

By specifying `auto_cache` for one of the `roles` of an entity-based
association, an attribute caching the objects linked via this
association is automagically added to another role of the association.

`auto_cache` can be set to one of the values:

- `True`. This only works for binary associations without any
  non-default properties for auto-caching. As it is the simplest case,
  it should be preferred over the other possibilities, if possible.

- A string specifying the name of the attribute used for caching.

- A tuple of strings specifying the name of the attribute used for
  caching and the name of the other role holding the cache.

- XXX An instance of :class:`_MOM.Link_Role.Role_Cacher<MOM.Link_Role.Role_Cacher>`.

In all cases, an instance of `Role_Cacher` will manage the automatic
cache for the role in question.

"""

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Link
