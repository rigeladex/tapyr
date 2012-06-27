# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.__test__.Entity_Reload
#
# Purpose
#    Test entity reloading after a scope.commit and changes in a different
#    process
#
# Revision Dates
#    15-Jun-2012 (MG) Creation
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM

    >>> opti  = SRM.Boat_Class (name = "Optimist", max_crew = 1)
    >>> laser = SRM.Boat_Class (name = "Laser", max_crew = 1)
    >>> b1    = SRM.Boat (u'Optimist', u"AUT", u"1107", raw = True) ### 1
    >>> b2    = SRM.Boat (u"Laser", None, "42", "OE", raw = True)

    >>> laser.max_crew ### before commit
    1
    >>> scope.commit  ()
    >>> modify_scope (%(p1)s, %(n1)s)

    >>> laser.max_crew ### after change
    2
    >>> b3 = scope.SRM.Boat.query (nation = u"AUT").one ()
    >>> b3 is b1
    True
    >>> b1.name
    u'My Boat'
    >>> scope.destroy ()

"""

from _GTW.__test__.model import *
from multiprocessing     import Process
_Ancestor_Essence = GTW.OMP.SRM.Boat

Scaffold.Backend_Parameters ["SQL"] = "'sqlite:///test.sqlite'"

def _modify_scope (* args) :
    scope          = Scaffold.scope (* args, create = False, verbose = False)
    laser          = scope.SRM.Boat_Class.query (name = u"laser").one ()
    laser.max_crew = 2
    boat           = scope.SRM.Boat.query (nation = u"AUT").one ()
    boat.name      = "My Boat"
    ### print (laser.max_crew, boat.name)
    scope.commit  ()
    scope.destroy ()
# end def _modify_scope

def modify_scope (* args) :
    if 1 :
        p = Process   (target = _modify_scope, args = args)
        p.start       ()
        p.join        ()
    else :
        import pdb; pdb.set_trace ()
        _modify_scope (* args)
# end def modify_scope

__test__ = Scaffold.create_test_dict (_test_code, ignore = "HPS")

### __END__ GTW.__test__.Entity_Reload
