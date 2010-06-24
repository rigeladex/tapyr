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
#    19-May-2010 (CT) `app_type_and_uri` factored
#    20-May-2010 (CT) `scope` corrected (guard for `if` modifying `create`)
#    24-Jun-2010 (CT) Use `MOM.EMS.Backends` and `DBS.Url`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *

from   _TFL                   import sos

import _MOM._EMS.Backends

import _TFL.Filename
import _TFL._Meta.Object

from    posixpath             import join as pjoin

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
    def app_type_and_url (cls, db_url = "hps://", default_path = None) :
        assert cls.ANS is not None
        EMS, DBW, DBS = MOM.EMS.Backends.get (db_url)
        apt = cls.app_type (EMS, DBW)
        url = DBS.Url (db_url, cls.ANS, default_path)
        return apt, url
    # end def app_type_and_url

    @classmethod
    def scope (cls, db_url = "hps://", default_path = None, create = True) :
        apt, url = cls.app_type_and_url (db_url, default_path)
        create = create or url.create
        if create :
            print "Creating new scope", apt, url.path or "in memory"
            scope = cls._create_scope (apt, url)
        else :
            print "Loading scope", apt, url
            scope = cls._load_scope (apt, url)
        return scope
    # end def scope

    @classmethod
    def _create_scope (cls, apt, url) :
        if url :
            apt.delete_database (url)
        return cls.Scope.new (apt, url)
    # end def _create_scope

    @classmethod
    def _load_scope (cls, apt, url) :
        return cls.Scope.load (apt, url)
    # end def _load_scope

Scaffold = _MOM_Scaffold_ # end class

if __name__ != "__main__" :
    MOM._Export ("Scaffold")
### __END__ MOM.Scaffold
