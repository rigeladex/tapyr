# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Graph.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.Graph.Command
#
# Purpose
#    Provide a command to generate renderings of MOM.Graphs
#
# Revision Dates
#    24-Sep-2012 (CT) Creation
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#     2-Sep-2014 (CT) Change `dynamic_defaults` to check `combined`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM                       import MOM
from   _TFL                       import TFL

import _MOM.App_Type

from   _TFL                       import sos
from   _TFL._Meta.Once_Property   import Once_Property

import _TFL.Command
import _TFL.Decorator
import _TFL.Filename

class MOM_Graph_Command (TFL.Command.Root_Command) :
    """Command to generate renderings of MOM.Graphs"""

    _real_name              = "Command"

    min_args = max_args     = 0

    _opts                   = \
        ( "-dir:P?Directory of output file"
        , "-name:P?Name of output file"
        , "-png:B?Render graph as png file (implies `-svg`)"
        , "-svg:B?Render graph as svg file"
        , "-txt:B?Render graph as ascii graphic file"
        , "-verbose:B?Verbose output"
        )

    @Once_Property
    def app_type (self) :
        from _MOM._DBW._HPS.Manager import Manager as DBW
        from _MOM._EMS.Hash         import Manager as EMS
        apt = MOM.App_Type (self.PNS._._bname, self.PNS)
        return apt.Derived (EMS, DBW)
    # end def app_type

    @Once_Property
    def graph (self) :
        from _TFL.object_globals import object_globals
        globals = object_globals (self)
        return globals ["graph"]
    # end def graph

    def dynamic_defaults (self, defaults) :
        result   = self.__super.dynamic_defaults (defaults)
        combined = dict (defaults, ** result)
        if "dir" not in combined :
            result ["dir"] = self._app_dir_default
        if "name" not in combined :
            result ["name"] = self.PNS._._bname
        return result
    # end def dynamic_defaults

    def file_name (self, cmd, ext) :
        fn = TFL.Filename ("." + ext, cmd.name, default_dir = cmd.dir)
        return fn.name
    # end def file_name

    def handler (self, cmd) :
        g = self.graph (self.app_type)
        if cmd.svg or cmd.png :
            from _MOM._Graph.SVG import Renderer as SVG_Renderer
            r = SVG_Renderer (g)
            r.render ()
            with self.open (cmd, "svg") as f :
                r.canvas.write_to_xml_stream (f)
            if cmd.verbose :
                print ("Rendered ", f.name)
        if cmd.png :
            import plumbum
            inkscape = plumbum.local [b"inkscape"]
            png_fn   = self.file_name (cmd, "png")
            svg_fn   = self.file_name (cmd, "svg")
            inkscape ["-y", "1", "-e", png_fn, svg_fn] ()
            if cmd.verbose :
                print ("Rendered ", png_fn)
        if cmd.txt :
            from _MOM._Graph.Ascii import Renderer as Ascii_Renderer
            r = Ascii_Renderer (g)
            with self.open (cmd, "txt") as f :
                print (r.render (), file = f)
            if cmd.verbose :
                print ("Rendered ", f.name)
    # end def handler

    @TFL.Contextmanager
    def open (self, cmd, ext) :
        fn = self.file_name (cmd, ext)
        with open (fn, "wb") as f :
            yield f
    # end def open

    def _app_dir_default (self) :
        return self.app_dir
    # end def _app_dir_default

Command = MOM_Graph_Command # end class

if __name__ != "__main__" :
    MOM.Graph._Export ("Command")
### __END__ MOM.Graph.Command
