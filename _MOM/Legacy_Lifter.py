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
#    25-Jan-2013 (MG) Add filter code for old account passwort storage
#    29-Jan-2013 (MG) Lift `Type_Name` in pickle carge
#    30-Jan-2013 (MG) Add support for `removing` objects during legacy
#                     lifting
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from    _MOM             import MOM
from    _TFL             import TFL
import  _TFL._Meta.Object
import  _TFL.sos         as     os

class Project_Legacy_Lifter (object) :
    """Base class for project specific legacy lifter"""

    __metaclass__      = TFL.Meta.M_Auto_Combine_Dicts

    _dicts_to_combine  = \
        ("Type_Name_Renaming", "Type_Name_Lifter", "E_Type_Lifter")

    Type_Name_Renaming = \
        { "Auth.Account_P" : "Auth.Account"
        }
    Type_Name_Lifter   = \
        { "Auth.Account"   : "_account_lifter"
        }
    E_Type_Lifter      = dict ()

    @classmethod
    def _account_lifter (cls, type_name, pc, pid) :
        if ("salt" in pc) and ("ph_name" not in pc) :
            salt            = pc.pop ("salt") [0]
            pc ["password"] = ["%s::%s" % (salt, pc ["password"] [0])]
            pc ["ph_name"]  = ["sha224"]
        return type_name, pc, pid
    # end def _account_lifter

# end class Project_Legacy_Lifter

class Legacy_Lifter (TFL.Meta.Object) :
    """Database legacy lifter"""

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
            type_name = self.module.Type_Name_Renaming.get \
                (type_name, type_name)
            if "Type_Name" in pc : ### in case we changed the type name
                                   ### through the Type_Name_Renaming we
                                   ### need to change the Type_Name in
                                   ### the pickle cargo as well
                pc ["Type_Name"] = [type_name]
            lifter    = self.module.Type_Name_Lifter.get (type_name)
            if lifter :
                lifter = getattr (self.module, lifter)
                type_name, pc, pid = lifter (type_name, pc, pid)
            if type_name and self.module.E_Type_Lifter :
                pc_et   = db_man.app_type [type_name]
                for let, lifter in self.module.E_Type_Lifter.iteritems () :
                    let = db_man.app_type [let]
                    if issubclass (pc_et, let) :
                        lifter = getattr (self.module, lifter)
                        type_name, pc, pid = lifter (type_name, pc, pid)
            if type_name is not None :
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
