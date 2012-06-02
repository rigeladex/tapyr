# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
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
#    MOM.Command
#
# Purpose
#    Provide an extendable Command for applications based on MOM
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
#    10-Aug-2010 (CT) Command `description` defined as doc-string of `handler`
#    11-Aug-2010 (CT) `cmd__info` and friends added
#    13-Aug-2010 (CT) `-readonly` added to command `migrate`
#    16-Aug-2010 (CT) `cmd__readonly` and friends added
#    16-Aug-2010 (CT) `-verbose` added
#    16-Aug-2010 (MG) `verbose` handling in `scope` fixed
#    16-Aug-2010 (CT) `cmd__delete` and friends added
#    27-Jan-2012 (CT) `app_path` added
#    24-Apr-2012 (CT) Add call to `db_man_t.ems.compact` to `_do_migration`
#    17-May-2012 (CT) Derive from `TFL.Command`,
#                     rename from `Scaffold` to `Command`
#    22-May-2012 (CT) Remove unused imports
#    22-May-2012 (CT) Factor `app_path` to `TFL.Command.app_dir`
#    22-May-2012 (CT) Factor `TFL.Sub_Command`
#    31-May-2012 (CT) Factor `-config` option to `TFL.Command`
#    31-May-2012 (CT) Call `scope.ems.compact` in `_handle_create`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *

import _MOM.DB_Man
import _MOM._EMS.Backends

from   _TFL                   import sos

import _TFL.CAO
import _TFL.Command
import _TFL.Environment
import _TFL.Filename
import _TFL._Meta.Once_Property

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

class _MOM_Command_ (TFL.Command.Sub_Command) :

    _rn_prefix              = "_MOM"

_Command_ = _MOM_Command_ # end class

class MOM_Command (TFL.Command.Command) :
    "" ### """Extendable Command for applications based on MOM"""

    _rn_prefix              = "MOM"

    ANS                     = None
    DB_Man                  = MOM.DB_Man
    nick                    = "NN"
    PNS_Aliases             = {}
    Scope                   = MOM.Scope

    _buns                   = \
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
    _default_db_name        = "" ### used by `default_db_name`
    _defaults               = dict \
        ( copyright_start   = 2010
        )
    _opts                   = \
        ( "-copyright_start:I?Start of copyright for this application"
        , TFL.CAO.Abs_Path
            ( name        = "db_name"
            , description = "Default name of database"
            , max_number  = 1
            )
        , "-db_url:S=hps://"
            "?Database url (form: `dialect://user:password@host:port/db_name`)"
        , SA_WE_Opt ()
        , "-verbose:B"
        )

    ### Sub-commands defined as class attributes to allow redefinition by
    ### derived classes; meta class puts their names into `_sub_commands`
    class _MOM_Create_ (_Command_) :
        """Create database specified by `-db_url`."""

    _Create_ = _MOM_Create_ # end class

    class _MOM_Delete_ (_Command_) :
        """Delete database specified by `-db_url`."""

    _Delete_ = _MOM_Delete_ # end class

    class _MOM_Info_ (_Command_) :
        """Display info about database specified by `-db_url`."""

    _Info_ = _MOM_Info_ # end class

    class _MOM_Load_ (_Command_) :
        """Load database specified by `-db_url`."""

    _Load_ = _MOM_Load_ # end class

    class _MOM_Migrate_ (_Command_) :
        """Migrate database specified by `-db_url` to `-target_db_url`."""

        _opts                   = \
            ( "chunk_size:I=10000?Number of entities in one chunk"
            , "overwrite:B?Overwrite `target_db_url` if necessary"
            , "readonly:B?Mark database `db_url` as readonly"
            , "target_db_url:S?Database url for target database"
            )

    _Migrate_ = _MOM_Migrate_ # end class

    class _MOM_Readonly_ (_Command_) :
        """Change readonly-state of database."""

        _args                   = \
            ( TFL.CAO.Arg.Key
                ( name          = "state"
                , dct           = dict
                    ( yes       = True
                    , no        = False
                    )
                )
            ,
            )

    _Readonly_ = _MOM_Readonly_ # end class

    class _MOM_Shell_ (_Command_) :
        """Open interactive python shell."""

    _Shell_ = _MOM_Shell_ # end class

    @TFL.Meta.Once_Property
    def default_db_name (self) :
        return sos.path.join \
            ( self.app_dir
            , self._default_db_name or self.ANS.__name__.lower ()
            )
    # end def default_db_name

    def app_type (self, * ems_dbw) :
        """Return app_type named `self.nick` for application namespace
           `self.ANS`.
        """
        assert self.ANS is not None
        result = MOM.App_Type.Table.get (self.nick)
        if result is None :
            result = MOM.App_Type \
                (self.nick, self.ANS, PNS_Aliases = self.PNS_Aliases)
        if ems_dbw :
            result = result.Derived (* ems_dbw)
        return result
    # end def app_type

    def app_type_and_url (self, db_url = "hps://", default_path = None) :
        assert self.ANS is not None
        EMS, DBW, DBS = MOM.EMS.Backends.get (db_url)
        apt = self.app_type (EMS, DBW)
        url = DBS.Url (db_url, self.ANS, default_path)
        return apt, url
    # end def app_type_and_url

    def dynamic_defaults (self, defaults) :
        result = self.__super.dynamic_defaults (defaults)
        if "db_name" not in defaults :
            result ["db_name"] = self.default_db_name
        return result
    # end def dynamic_defaults

    def scope ( self
              , db_url       = "hps://"
              , default_path = None
              , create       = True
              , verbose      = False
              ) :
        apt, url = self.app_type_and_url (db_url, default_path)
        create = create or url.create
        if create :
            if verbose :
                print "Creating new scope", apt, url.path or "in memory"
            scope = self._create_scope (apt, url, verbose)
        else :
            if verbose :
                print "Loading scope", apt, url
            scope = self._load_scope (apt, url)
        return scope
    # end def scope

    def _create_scope (self, apt, url, verbose = False) :
        if url :
            apt.delete_database (url)
        return self.Scope.new (apt, url)
    # end def _create_scope

    @TFL.Contextmanager
    def _cro_context (self, db_man, state) :
        old_state = db_man.db_meta_data.readonly
        db_man.change_readonly (state)
        try :
            yield
        except :
            db_man.change_readonly (old_state)
            raise
    # end def _cro_context

    def _do_migration (self, cmd, apt_s, url_s, apt_t, url_t, db_man_s) :
        if cmd.overwrite :
            apt_t.delete_database (url_t)
        db_man_t = self.DB_Man.create (apt_t, url_t, db_man_s, cmd.chunk_size)
        if cmd.verbose :
            self._print_info  (apt_s, url_s, db_man_s.db_meta_data, "    ")
            self._print_info  (apt_t, url_t, db_man_t.db_meta_data, "    ")
        db_man_t.ems.compact ()
        db_man_t.destroy ()
    # end def _do_migration

    def _handle_create (self, cmd) :
        scope = self.scope \
            (cmd.db_url, cmd.db_name, create = True, verbose = cmd.verbose)
        scope.commit      ()
        scope.ems.compact ()
        scope.destroy     ()
    # end def _handle_create

    def _handle_delete (self, cmd) :
        apt, url = self.app_type_and_url (cmd.db_url, cmd.db_name)
        if cmd.verbose :
            print "Deleting scope", apt, url.path
        apt.delete_database (url)
    # end def _handle_delete

    def _handle_info (self, cmd) :
        apt, url = self.app_type_and_url (cmd.db_url, cmd.db_name)
        db_man   = self.DB_Man.connect   (apt, url)
        self._print_info (apt, url, db_man.db_meta_data)
        db_man.destroy   ()
    # end def _handle_info

    def _handle_load (self, cmd) :
        return self.scope (cmd.db_url, cmd.db_name, create = False)
    # end def _handle_load

    def _handle_migrate (self, cmd) :
        if cmd.verbose :
            print "Migrating scope", cmd.db_url, cmd.db_name, \
                "-->", cmd.target_db_url
        apt_s, url_s = self.app_type_and_url (cmd.db_url, cmd.db_name)
        apt_t, url_t = self.app_type_and_url (cmd.target_db_url, cmd.db_name)
        if cmd.verbose :
            print "   ", apt_s, url_s, "to", apt_t, url_t
        db_man_s = self.DB_Man.connect (apt_s, url_s)
        if cmd.readonly :
            with self._cro_context (db_man_s, True) :
                self._do_migration (cmd, apt_s, url_s, apt_t, url_t, db_man_s)
        else :
            self._do_migration (cmd, apt_s, url_s, apt_t, url_t, db_man_s)
        db_man_s.destroy ()
    # end def _handle_migrate

    def _handle_readonly (self, cmd) :
        apt, url = self.app_type_and_url (cmd.db_url, cmd.db_name)
        db_man   = self.DB_Man.connect   (apt, url)
        db_man.change_readonly (cmd.state)
        if cmd.verbose :
            self._print_info (apt, url, db_man.db_meta_data)
        db_man.destroy ()
    # end def _handle_readonly

    def _handle_shell (self, cmd) :
        scope = self._handle_load (cmd)
        TFL.Environment.py_shell  ()
    # end def _handle_shell

    def _load_scope (self, apt, url) :
        return self.Scope.load (apt, url)
    # end def _load_scope

    def _print_info (self, apt, url, dbmd, indent = "") :
        print "%sInfo for database" % (indent, ), apt, url
        for k in sorted (dbmd) :
            print "%s%-12s : %s" % (indent, k, dbmd [k])
        print "%s%-12s : %s" % (indent, "dbv_hash/apt", apt.db_version_hash)
        print
    # end def _print_info

Command = MOM_Command # end class

if __name__ != "__main__" :
    MOM._Export ("Command", "_Command_")
### __END__ MOM.Command
