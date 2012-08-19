# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.SRM_Graph
#
# Purpose
#    Test SRM.Graph
#
# Revision Dates
#    17-Aug-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> g = graph (scope.app_type)

    >>> for v in sorted (g.map.itervalues (), key = TFL.Getter.index) :
    ...   print "%%-34s %%s" %% (v, v.label)
    <Graph.Link2  SRM.Boat_in_Regatta> _in_
    <Graph.Link1  SRM.Regatta>         SRM.Regatta
    <Graph.Object SRM.Regatta_Event>   SRM.Regatta_Event
    <Graph.Object SRM.Club>            SRM.Club
    <Graph.Link2  SRM.Crew_Member>     SRM.Crew_Member
    <Graph.Link1  SRM.Boat>            SRM.Boat
    <Graph.Object SRM.Boat_Class>      SRM.Boat_Class
    <Graph.Link1  SRM.Sailor>          SRM.Sailor
    <Graph.Object PAP.Person>          PAP.Person
    <Graph.Object PAP.Subject>         PAP.Subject

    >>> for k, v in sorted (g.map.iteritems ()) :
    ...   print "%%-34s %%-34s %%s" %% (v, v.anchor, v.pos)
    <Graph.Object PAP.Person>          <Graph.Link1  SRM.Sailor>          N*3
    <Graph.Object PAP.Subject>         <Graph.Object PAP.Person>          E*2 + N*3
    <Graph.Link1  SRM.Boat>            <Graph.Link2  SRM.Boat_in_Regatta> W
    <Graph.Object SRM.Boat_Class>      <Graph.Link1  SRM.Boat>            W*2
    <Graph.Link2  SRM.Boat_in_Regatta> None                               (0,0)
    <Graph.Object SRM.Club>            <Graph.Object SRM.Regatta_Event>   NE*2
    <Graph.Link2  SRM.Crew_Member>     <Graph.Link2  SRM.Boat_in_Regatta> NE
    <Graph.Link1  SRM.Regatta>         <Graph.Link2  SRM.Boat_in_Regatta> E
    <Graph.Object SRM.Regatta_Event>   <Graph.Link1  SRM.Regatta>         E*2
    <Graph.Link1  SRM.Sailor>          <Graph.Link2  SRM.Boat_in_Regatta> N*2

    >>> for k, v in sorted (g.map.iteritems ()) :
    ...     print v.type_name, v.e_type.Roles
    PAP.Person ()
    PAP.Subject ()
    SRM.Boat (Boat_Class `left`,)
    SRM.Boat_Class ()
    SRM.Boat_in_Regatta (Boat `left`, Regatta `right`)
    SRM.Club ()
    SRM.Crew_Member (Boat_in_Regatta `left`, Sailor `right`)
    SRM.Regatta (Regatta_Event `left`,)
    SRM.Regatta_Event ()
    SRM.Sailor (Person `left`,)

    >>> for v in sorted (g.map.itervalues (), key = TFL.Getter.index) :
    ...     if v.relations :
    ...         for a, l in sorted (v.relations.iteritems ()) :
    ...             print l
    <Graph.Relation.Role SRM.Boat_in_Regatta.left -> SRM.Boat>
    <Graph.Relation.Role SRM.Boat_in_Regatta.right -> SRM.Regatta>
    <Graph.Relation.Attr SRM.Boat_in_Regatta.skipper -> SRM.Sailor>
    <Graph.Relation.Role SRM.Regatta.left -> SRM.Regatta_Event>
    <Graph.Relation.Attr SRM.Regatta_Event.club -> SRM.Club>
    <Graph.Relation.Role SRM.Crew_Member.left -> SRM.Boat_in_Regatta>
    <Graph.Relation.Role SRM.Crew_Member.right -> SRM.Sailor>
    <Graph.Relation.Role SRM.Boat.left -> SRM.Boat_Class>
    <Graph.Relation.Attr SRM.Sailor.club -> SRM.Club>
    <Graph.Relation.Role SRM.Sailor.left -> PAP.Person>
    <Graph.Relation PAP.Person IS A PAP.Subject>

    >>> for v in sorted (g.map.itervalues (), key = TFL.Getter.index) :
    ...     if v.relations :
    ...         for a, l in sorted (v.relations.iteritems ()) :
    ...             print l.kind, l.source, l.target
    Role <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Boat>
    Role <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Regatta>
    Attr <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Sailor>
    Role <Graph.Link1  SRM.Regatta> <Graph.Object SRM.Regatta_Event>
    Attr <Graph.Object SRM.Regatta_Event> <Graph.Object SRM.Club>
    Role <Graph.Link2  SRM.Crew_Member> <Graph.Link2  SRM.Boat_in_Regatta>
    Role <Graph.Link2  SRM.Crew_Member> <Graph.Link1  SRM.Sailor>
    Role <Graph.Link1  SRM.Boat> <Graph.Object SRM.Boat_Class>
    Attr <Graph.Link1  SRM.Sailor> <Graph.Object SRM.Club>
    Role <Graph.Link1  SRM.Sailor> <Graph.Object PAP.Person>
    Is_A <Graph.Object PAP.Person> <Graph.Object PAP.Subject>

"""

from _GTW.__test__.model  import *
from _GTW._OMP._SRM.Graph import graph

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.SRM_Graph
