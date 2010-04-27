# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.
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
#    MOM.Scaffold
#
# Purpose
#    Provide a scaffold for creating instances of MOM.App_Type and MOM.Scope
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *

from   _TFL                   import sos

import _TFL.Filename
import _TFL._Meta.Object

class _MOM_Scaffold_ (TFL.Meta.Object) :
    """Scaffold for creating instances of MOM.App_Type and MOM.Scope."""

    _real_name      = "Scaffold"

    ANS             = None
    nick            = "NN"
    PNS_Aliases     = {}
    Scope           = MOM.Scope

    @classmethod
    def app_type (cls, * ems_dbw) :
        """Return app_type named `cls.nick` for application namespace
           `cls.ANS`.
        """
        assert cls.ANS is not None
        result = MOM.App_Type.Table.get (cls.nick)
        if result is None :
            result = MOM.App_Type \
                (cls.nick, cls.ANS, PNS_Aliases = cls.PNS_Aliases)
        if ems_dbw :
            result = result.Derived (* ems_dbw)
        return result
    # end def app_type

    @classmethod
    def app_type_hps (cls) :
        from _MOM._EMS.Hash         import Manager as EMS
        from _MOM._DBW._HPS.Manager import Manager as DBW
        return cls.app_type (EMS, DBW)
    # end def app_type_hps

    @classmethod
    def app_type_sas (cls) :
        from _MOM._EMS.SAS          import Manager as EMS
        from _MOM._DBW._SAS.Manager import Manager as DBW
        return cls.app_type (EMS, DBW)
    # end def app_type_sas

    @classmethod
    def scope (cls, db_prefix = None, db_name = None, create = True) :
        assert cls.ANS is not None
        uri = None
        if db_prefix :
            apt = cls.app_type_sas ()
            if db_prefix.startswith ("sqlite:////") :
                ### SQLite database with absolute path
                uri = "".join ((db_prefix, db_name))
            elif db_name :
                uri = sos.path.join \
                    (db_prefix, TFL.Filename (db_name).base_ext)
        else :
            apt = cls.app_type_hps ()
            if db_name :
                uri = ".".join (db_name, cls.ANS.db_version.db_extension)
            if not uri or not sos.path.exists (uri) :
                create = True
        if create :
            print "Creating new scope", apt, uri or "in memory"
            scope = cls._create_scope (apt, uri)
        else :
            print "Loading scope", apt, uri
            scope = cls._load_scope (apt, uri)
        return scope
    # end def scope

    @classmethod
    def _create_scope (cls, apt, uri) :
        if uri :
            apt.delete_database (uri)
        return cls.Scope.new (apt, uri)
    # end def _create_scope

    @classmethod
    def _load_scope (cls, apt, uri) :
        return cls.Scope.load (apt, uri)
    # end def _load_scope

Scaffold = _MOM_Scaffold_ # end class

if __name__ != "__main__" :
    MOM._Export ("Scaffold")
### __END__ MOM.Scaffold
