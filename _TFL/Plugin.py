# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Plugin
#
# Purpose
#    Model a plugin of an application
#
# Revision Dates
#     7-Jun-2004 (CT)  Creation
#    23-Jun-2004 (CED) `__init__` changed to call `_init` function of plugin
#     4-Aug-2004 (MG)  Attribute `directory` added
#     4-Aug-2004 (MG)  Call of `_init` removed
#    21-Sep-2004 (CT)  `Plugin.__init__` changed to Set `plugin_pns._Plugin`
#                      to `self`
#    22-Sep-2004 (CED) `M_Plugin` added and used
#    22-Sep-2004 (CED) `base_pns_base` and `setup` set, bug fixed
#    23-Sep-2004 (CED) Some refactorings
#    23-Sep-2004 (CED) Futher improvements in `setup`
#    23-Sep-2004 (CED) Leading underscore regarded in version string
#    22-Feb-2006 (CED) `directory` set correct for frozen plugin
#     6-Nov-2006 (CED) `frozen` magic delegated to `Plugin_Importer`
#    24-Sep-2007 (PGO) Calling super in the metaclass
#     7-Nov-2007 (CT)  Use `Getter` instead of `lambda`
#    22-Aug-2008 (CT)  Moved from `_TOM` to `_TFL`, code from `TTA.Plugin`
#                      factored in here
#    ««revision-date»»···
#--

from   _TFL                  import TFL

import _TFL._Meta.Object
import _TFL._Meta.M_Class
import _TFL._UI.Command_Mgr
import _TFL.Accessor
import _TFL.Functor
import _TFL.import_module

from   _TFL                  import sos
from   _TFL.Importers        import Plugin_Importer
from   _TFL.Filename         import Filename
from   _TFL.Regexp           import *

import weakref

class M_Plugin (TFL.Meta.M_Class) :

    Table = {}

    def __call__ (cls, name, * args, ** kw) :
        if name in cls.Table :
            raise KeyError, "Duplicate plugin name %s" % (name, )
        result           = super (M_Plugin, cls).__call__ (name, * args, ** kw)
        cls.Table [name] = result
        return result
    # end def __call__

# end class M_Plugin

class _TFL_Plugin_ (TFL.Meta.Object) :
    """Model a plugin of an application."""

    __metaclass__        = M_Plugin
    _real_name           = "Plugin"

    application          = None
    Command              = TFL.UI.Command
    date                 = property (TFL.Getter._version.date)
    description          = property (TFL.Getter._version.productdesc)
    expiration_date      = property (TFL.Getter._version.expiration_date)
    name                 = property (TFL.Getter._version.productname)
    release              = property (TFL.Getter._version.version)
    version              = property (TFL.Getter._version.version)

    def __init__ (self, name, application = None) :
        if application is not None :
            self._set_application (application)
        ( self.directory
        , self.module
        , plain_name
        )                           = Plugin_Importer.new_plugin (name)
        pkg_name                    = "_Plugins._%s" % (plain_name, )
        self.pns_name               = plain_name
        self.plugin_pns = pns       = getattr (self.module, plain_name)
        pns._Plugin                 = weakref.proxy (self)
        self.rank                   = getattr (self.module, "rank", 0)
        self._version               = getattr \
            (TFL.import_module ("%s.Version" % (pkg_name, )), "Version")
        if application is not None :
            application.load_images_from_dir (self.directory)
            self._add_documents ()
    # end def __init__

    def add_command (self, group, cmd, ** kw) :
        if self.application :
            cmd_mgr = self.application.cmd_mgr
            g       = cmd_mgr.group (group)
            g.add_command (cmd, ** kw)
            cmd_mgr.update_state (force = True)
    # end def add_command

    def add_dyn_group (self, group, name, ** kw) :
        if self.application :
            cmd_mgr = self.application.cmd_mgr
            g       = cmd_mgr.group (group)
            g.add_dyn_group (name, ** kw)
            cmd_mgr.update_state (force = True)
    # end def add_dyn_group

    def setup (self) :
        _setup = getattr (self.module, "_setup", None)
        if callable (_setup) :
           _setup (self)
    # end def setup

    def _add_documents (self) :
        for filename in \
            (   f
            for f in sos.listdir (self.directory)
            if  f.endswith (".pdf")
            ) :
                fname = filename.rsplit (".", 2) [0]
                fname = fname.replace ("_", " ")
                fname = fname.replace (".", " ")
                cmd = self.application.ANS.UI.Command \
                    ( fname
                    , TFL.Functor
                        ( self.application._open_manual
                        , sos.path.join (self.directory, filename)
                        )
                    , batchable = False
                    )
                self.add_command \
                    ( "Help"
                    , cmd
                    , if_names = ("mb", )
                    )
    # end def _add_documents

    def __repr__ (self) :
        return "%s (%s)" % (self.__class__.__name__, self.pns_name)
    # end def __repr__

    def __str__ (self) :
        return "Plugin %s, version %s" % (self.name, self.version)
    # end def __str__

    def _set_application (self, application) :
        self.application = application
    # end def _set_application

Plugin = _TFL_Plugin_ # end class

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Plugin
