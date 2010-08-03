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
#    and managing their databases
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#    19-May-2010 (CT) `app_type_and_uri` factored
#    20-May-2010 (CT) `scope` corrected (guard for `if` modifying `create`)
#    24-Jun-2010 (CT) Use `MOM.EMS.Backends` and `DBS.Url`
#    25-Jun-2010 (CT) Command handlers added
#    29-Jun-2010 (CT) `-copyright_start` added
#     1-Jul-2010 (CT) `-overwrite` added to `cmd__migrate__opts`
#    12-Jul-2010 (CT) `do_migrate` changed to use `DB_Man`
#     2-Aug-2010 (CT) `cmd__buns` added
#     3-Aug-2010 (MG) Sub-command `shell` added
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *

from   _TFL                   import sos

import _MOM.DB_Man
import _MOM._EMS.Backends

import _TFL.CAO
import _TFL.Filename
import _TFL._Meta.M_Auto_Combine
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.Environment

import sys

class SA_WE_Opt (TFL.CAO.Bool) :
    """Turn SA warnings into errors"""

    def __init__ (self, ** kw) :
        assert "name" not in kw
        kw ["name"] = self.__class__.__name__
        if "description" not in kw :
            kw ["description"] = self.__class__.__doc__
        self.__super.__init__ (** kw)
    # end def __init__

    def cook (self, value, cao = None) :
        result = self.__super.cook (value, cao)
        if result :
            import warnings
            from sqlalchemy import exc as sa_exc
            warnings.filterwarnings \
                (action = "error", category = sa_exc.SAWarning)
        return result
    # end def cook

# end class SA_WE_Opt

class _M_Scaffold_ (TFL.Meta.M_Auto_Combine) :
    """Meta class for `Scaffold`"""

    @TFL.Meta.Once_Property
    def cmd (cls) :
        """Command for database management."""
        return TFL.CAO.Cmd \
            ( args        =
                ( TFL.CAO.Cmd_Choice ("command", * cls.__sub_commands ())
                ,
                )
            , opts        = cls.cmd__base__opts
            , buns        = cls.cmd__buns
            )
    # end def cmd

    @TFL.Meta.Once_Property
    def cmd__create (cls) :
        """Sub-command for database creation."""
        return TFL.CAO.Cmd \
            ( name        = "create"
            , description = "Create database specified by `-db_url`."
            , handler     = cls.__do_create
            , opts        = cls.cmd__create__opts
            )
    # end def cmd__create

    @TFL.Meta.Once_Property
    def cmd__load (cls) :
        """Sub-command for database loading."""
        return TFL.CAO.Cmd \
            ( name        = "load"
            , description = "Load database specified by `-db_url`."
            , handler     = cls.__do_load
            , opts        = cls.cmd__load__opts
            )
    # end def cmd__load

    @TFL.Meta.Once_Property
    def cmd__migrate (cls) :
        """Sub-command for database migration."""
        return TFL.CAO.Cmd \
            ( name        = "migrate"
            , description =
                "Migrate database specified by `-db_url` to `-target_db_url`"
            , handler     = cls.__do_migrate
            , opts        = cls.cmd__migrate__opts
            )
    # end def cmd__migrate

    @TFL.Meta.Once_Property
    def cmd__shell (cls) :
        """Sub-command for an interactive interpreter shell."""
        return TFL.CAO.Cmd \
            ( name        = "shell"
            , description = "Open interactive python shell."
            , handler     = cls.__do_shell
            , opts        = cls.cmd__shell__opts
            )
    # end def cmd__load

    @TFL.Meta.Once_Property
    def cmd__base__opts (cls) :
        return \
            [ "-copyright_start:I=%s" % cls.cmd__copyright_start
            , TFL.CAO.Abs_Path
                ( name        = "db_name"
                , default     = cls.cmd__default_db_name
                , description = "Default name of database"
                , max_number  = 1
                )
            , "-db_url:S=hps://"
                "?Database url "
                "(form: `dialect://user:password@host:port/db_name`)"
            , SA_WE_Opt ()
            ] + cls.cmd__base__opts_x
    # end def cmd__base__opts

    def __do_create (cls, cmd) :
        """Handler for sub-command `create`."""
        return cls.do_create (cmd)
    # end def __do_create

    def __do_load (cls, cmd) :
        """Handler for sub-command `load`."""
        return cls.do_load (cmd)
    # end def __do_load

    def __do_migrate (cls, cmd) :
        """Handler for sub-command `migrate`."""
        return cls.do_migrate (cmd)
    # end def __do_migrate

    def __do_shell (cls, cmd) :
        """Handler for sub-command `shell`."""
        return cls.do_shell (cmd)
    # end def __do_shell

    def __sub_commands (cls) :
        return tuple \
            (getattr (cls, sc) for sc in cls.cmd__sub_commands)
    # end def __sub_commands

# end class _M_Scaffold_

class _MOM_Scaffold_ (TFL.Meta.Object) :
    """Scaffold for creating instances of MOM.App_Type and MOM.Scope and
       managering their databases.
    """

    __metaclass__         = _M_Scaffold_
    _lists_to_combine     = \
        ( "cmd__base__opts_x"
        , "cmd__buns"
        , "cmd__create__opts"
        , "cmd__load__opts"
        , "cmd__migrate__opts"
        , "cmd__shell__opts"
        , "cmd__sub_commands"
        )
    _real_name            = "Scaffold"

    ANS                   = None
    cmd__copyright_start  = 2010
    DB_Man                = MOM.DB_Man
    default_db_name       = ""
    nick                  = "NN"
    PNS_Aliases           = {}
    Scope                 = MOM.Scope

    @classmethod
    def cmd__default_db_name (cls) :
        return sos.path.join \
            ( sos.path.dirname (sys.modules [cls.__module__].__file__)
            , cls.default_db_name or cls.ANS.__name__.lower ()
            )
    # end def cmd__default_db_name

    cmd__base__opts_x     = ()
    cmd__buns             = \
        ( TFL.CAO.Bundle
            ( "mig1"
            , "Migrate from `db_url` to `target_db_url`"
            , command       = "migrate"
            , target_db_url = "hps:///migration"
            )
        , TFL.CAO.Bundle
            ( "mig2"
            , "Migrate from `target_db_url` to `db_url`"
            , command       = "migrate"
            , db_url        = "hps:///migration"
            )
        ### Application needs to define `db_url = target_db_url = XXX` for
        ### the bundles `mig1` and `mig2` to work conventiently
        )
    cmd__create__opts     = ()
    cmd__load__opts       = ()
    cmd__migrate__opts    = \
        ( "chunk_size:I=10000?Number of entities in one chunk"
        , "overwrite:B?Overwrite `target_db_url` if necessary"
        , "target_db_url:S?Database url for target database"
        )
    cmd__shell__opts      = ()
    cmd__sub_commands     = \
        ("cmd__create", "cmd__load", "cmd__migrate", "cmd__shell")

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
    def do_copy (cls, cmd) :
        src_scope = cls.do_load          (cmd)
        apt, url  = cls.app_type_and_url (cmd.target_db_url, cmd.db_name)
        if cmd.overwrite :
            apt.delete_database          (url)
        trg_scope = src_scope.copy       (apt, url)
        trg_scope.destroy ()
    # end def do_copy

    @classmethod
    def do_create (cls, cmd) :
        scope = cls.scope (cmd.db_url, cmd.db_name, create = True)
        scope.destroy ()
    # end def do_create

    @classmethod
    def do_load (cls, cmd) :
        return cls.scope (cmd.db_url, cmd.db_name, create = False)
    # end def do_load

    @classmethod
    def do_migrate (cls, cmd) :
        apt_s, url_s = cls.app_type_and_url (cmd.db_url, cmd.db_name)
        apt_t, url_t = cls.app_type_and_url (cmd.target_db_url, cmd.db_name)
        print "Migrating scope", apt_s, url_s, "to", apt_t, url_t
        db_man_s     = cls.DB_Man.connect   (apt_s, url_s)
        if cmd.overwrite :
            apt_t.delete_database (url_t)
        db_man_t = cls.DB_Man.create (apt_t, url_t, db_man_s, cmd.chunk_size)
        db_man_s.destroy ()
        db_man_t.destroy ()
    # end def do_migrate

    @classmethod
    def do_shell (cls, cmd) :
        scope = cls.do_load      (cmd)
        TFL.Environment.py_shell ()
    # end def do_shell

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
