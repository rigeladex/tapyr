# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.DBW.SAS.__doc__
#
# Purpose
#    Test for MOM meta object model using SQLAlchemy as database backend
#
# Revision Dates
#    12-Feb-2010 (MG) Creation
#    16-Feb-2010 (MG) Test for database migration added
#    ««revision-date»»···
#--

from _MOM.__doc__ import dt_form, MOM, BMT, show, NL, sos
from   _TFL.Regexp import Dict_Replacer, re

filter_dbw_pat = re.compile \
    (  "\#\#\#\sDBW-specific\sstart.+?\#\#\#\sDBW-specific\sfinish"
    , re.DOTALL | re.X | re.MULTILINE
    )

fixer = Dict_Replacer ({"__Hash" : "__SAS", "__HPS": "__SAS", "hps://" : "sqlite://"})

doc__ = fixer \
    ( filter_dbw_pat.sub ("", dt_form)
    % dict
        ( import_DBW = "from _MOM._DBW._SAS.Manager import Manager"
        , import_EMS = "from _MOM._EMS.SAS          import Manager"
        , db_path    = "'test.sqlite'"
        , db_scheme  = "'sqlite://'"
        )
    )
__doc__ = doc__

_db_mig_test = """
>>> from _MOM._DBW._HPS.Manager import Manager as DBW_HPS
>>> from _MOM._EMS.Hash         import Manager as EMS_HPS
>>> from _MOM._DBW._SAS.Manager import Manager as DBW_SAS
>>> from _MOM._EMS.SAS          import Manager as EMS_SAS

>>> DBW_SAS.Reset_Metadata    ()
>>> apt_gen = MOM.App_Type    (u"BMT_DBM", BMT)
>>> apt_sas = apt_gen.Derived (EMS_SAS, DBW_SAS)
>>> apt_hps = apt_gen.Derived (EMS_HPS, DBW_HPS)
>>> apt_sas is apt_hps
False
>>> apt_sas.parent is apt_hps.parent
True
>>> db_path_old  = "scope_old.sqlite"
>>> db_path_new  = "scope_new.sqlite"
>>> hps_filename = "scope_hps"
>>> hps_path     = "%s.bmt" % (hps_filename, )
>>> hps_url      = "hps:///%s" % (hps_path, )
>>> remove (db_path_old)
>>> remove (db_path_new)
>>> remove (hps_path)
>>> remove (hps_path + ".X", True)
>>> scope_1 = MOM.Scope.new          (apt_sas, "sqlite:///%s" % (db_path_old, ))
>>> m1 = scope_1.BMT.Mouse           ("Mouse_1")
>>> m2 = scope_1.BMT.Mouse           ("Mouse_2")
>>> m3 = scope_1.BMT.Mouse           ("Mouse_3")
>>> r1 = scope_1.BMT.Rat             ("Rat_1")
>>> t1 = scope_1.BMT.Trap            ("Brand", 1)
>>> t2 = scope_1.BMT.Trap            ("Brand", 2)
>>> t3 = scope_1.BMT.Trap            ("Brand", 3)
>>> t4 = scope_1.BMT.Trap            ("Brand", 4)
>>> rit = scope_1.BMT.Rodent_in_Trap (m1, t1)
>>> rit = scope_1.BMT.Rodent_in_Trap (m2, t2)
>>> rit = scope_1.BMT.Rodent_in_Trap (m3, t3)
>>> rit = scope_1.BMT.Rodent_in_Trap (r1, t4)
>>> scope_1.commit                   ()
>>> scope_1.destroy                  ()

Now, we load the `old` database and save it as a HPS
>>> scope_1 = MOM.Scope.load         (apt_sas, "sqlite:///%s" % (db_path_old, ))
>>> scope_2 = scope_1.copy           (apt_hps, hps_url)
>>> scope_1.destroy                  ()
>>> scope_2.destroy                  ()

Here is the point where we upgrade the object model and load the HPS database
again to perform the migration
>>> scope_2 = MOM.Scope.load         (apt_hps, hps_url)
>>> scope_3 = scope_2.copy           (apt_sas, "sqlite:///%s" % (db_path_new, ))
>>> scope_2.destroy                  ()
>>> scope_3.destroy                  ()

Now we load the load and the new SAS based scopes and compare them
>>> scope_1 = MOM.Scope.load         (apt_sas, "sqlite:///%s" % (db_path_old, ))
>>> scope_3 = MOM.Scope.load         (apt_sas, "sqlite:///%s" % (db_path_new, ))
>>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope_1, scope_3))
(12, 12)
>>> sorted (scope_1.user_diff (scope_3, ignore = ["last_cid"]).iteritems ())
[]
>>> scope_1.destroy ()
>>> scope_3.destroy ()
>>> remove          (db_path_old)
>>> remove          (db_path_new)
>>> remove          (hps_filename + ".bak")
>>> remove          (hps_path)
>>> remove          (hps_path + ".X", True)
"""
__test__ = dict (db_migration = _db_mig_test)

def remove (file, is_dir = False) :
    if sos.path.exists (file) :
        if is_dir :
            sos.rmdir  (file, deletefiles = True)
        else :
            sos.unlink (file)
# end def remove

### __END__ MOM.DBW.SAS.__doc__
