# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package MOM.
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
#    MOM.Legacy_Lifter
#
# Purpose
#    Database legacy lifting during migration
#
# Revision Dates
#    19-Jan-2013 (MG) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from    _MOM             import MOM
from    _TFL             import TFL
import  _TFL._Meta.Object
import  _TFL.sos         as     os

class Project_Legacy_Lifter (TFL.Meta.Object) :
    """Base class for project specific legacy lifter"""

    Type_Lifter   = dict ()
    E_Type_Lifter = dict ()

# end class for

class Legacy_Lifter (TFL.Meta.Object) :
    """Database legacy lifter"""

    Type_Name_Lifter = \
        { "Auth.Account_P" : "Auth.Account"
        }

    def __init__ (self, module) :
        self.module = Project_Legacy_Lifter
        if module :
            try :
                self.module = __import__ (module).Legacy_Lifter
            except ImportError :
                print ("Could not import zombie lifter `%s`" % (module, ))
    # end def __init__

    def entity_iter (self, db_man, db_iter) :
        for type_name, pc, pid in db_iter :
            type_name = self.Type_Name_Lifter.get (type_name, type_name)
            lifter    = self.module.Type_Lifter.get (type_name)
            if lifter :
                lifter = getattr (self.module, lifter)
                type_name, pc, pid = lifter (type_name, pc, pid)
            if self.module.E_Type_Lifter :
                pc_et   = db_man.app_type [type_name]
                for let, lifter in self.module.E_Type_Lifter.iteritems () :
                    let = db_man.app_type [let]
                    if issubclass (pc_et, let) :
                        lifter = getattr (self.module, lifter)
                        type_name, pc, pid = lifter (type_name, pc, pid)
            yield type_name, pc, pid
    # end def entity_iter

    def change_iter (self, db_man, db_iter) :
        for chg_cls, chg_dct, children_pc in db_iter :
            yield chg_cls, chg_dct, children_pc
    # end def change_iter

# end class Legacy_Lifter

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Legacy_Lifter
