# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
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
#    DJO.expand_CSS
#
# Purpose
#    Expand a CSS template via the Python `%s` operator
#
# Revision Dates
#    14-Dec-2007 (CT) Creation
#    15-Dec-2007 (MG) `eval_paremeters` factored to support inclueded files
#    15-Dec-2007 (MG) Fix single `%` to avoid having `%%` in the templates
#    15-Dec-2007 (MG) `watch_directories` added
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TFL.Filename          import Filename
from   _TFL.Caller            import Scope
import _TFL.sos               as     os
import _TFL.Record
import  re

try :
    import pyinotify
except ImportError :
    pyinotify = None

def eval_paremeters (filename, pd) :
    pn = pd ["_PARENT_"] = Filename \
        (".parameters", filename, pd.get ("_PARENT_", ""))
    execfile \
        ( pn.name
        , dict ( R        = TFL.Record
               , include  = lambda fn : eval_paremeters (fn, pd)
               )
        , pd
        )
# end def eval_paremeters

template_extension = ".css_template"
fix_percent_pat    = re.compile ("%([^(])")
def create_css_file (filename, overrides) :
    filename     = Filename (filename, template_extension)
    out_filename = Filename (".css", filename).name
    pd           = {}
    eval_paremeters (filename, pd)
    ct    = open         (filename.name).read ()
    ct, _ = fix_percent_pat.subn (lambda m : "%%%s" % (m.group (0), ), ct)
    outf  = open  (out_filename, "wb")
    outf.write    (ct % Scope (globs = pd, locls = overrides))
    outf.close    ()
    print "CSS file created `%s`" % (out_filename, )
    return filename.directory
# end def create_css_file

def watch_directories (overrides, * directories) :
    watch  = pyinotify.WatchManager ()
    events = \
        pyinotify.EventsCodes.IN_MODIFY | pyinotify.EventsCodes.IN_CREATE

    class Event_Prcoessor (pyinotify.ProcessEvent) :

        def process_IN_MODIFY (self, event) :
            self.create_file (event)
        # end def process_IN_MODIFY

        def process_IN_CREATE (self, event) :
            self.create_file (event)
        # end def process_IN_MODIFY

        def create_file (self, event) :
            fn = Filename (os.path.join (event.path, event.name))
            ##import pdb; pdb.set_trace ()
            if (   (fn.ext == template_extension)
               and not (fn.base.startswith ("."))
               ) :
                create_css_file (fn, overrides)
        # end def create_file

    # end class Event_Prcoessor

    notifier = pyinotify.Notifier (watch, Event_Prcoessor ())
    for d in directories :
        watch.add_watch (d, events, rec = False)

    while True:  # loop forever
        try:
            # process the queue of events as explained above
            notifier.process_events ()
            if notifier.check_events ():
                # read notified events and enqeue them
                notifier.read_events ()
            # you can do some tasks here...
        except KeyboardInterrupt :
            # destroy the inotify's instance on this interrupt (stop monitoring)
            notifier.stop ()
            break
# end def watch_directories

def command_spec (arg_array = None) :
    from   _TFL.Command_Line import Command_Line
    return Command_Line \
        ( arg_spec         =
            ( "template:S"
            ,
            )
        , option_spec      = \
              ( "watch_files:B?Use libinotify events for an automatic update"
              ,
              )
        , min_args         = 1
        , process_keywords = True
        , arg_array        = arg_array
        )
# end def command_spec

def main (cmd) :
    keywords    = cmd.keywords
    directories = set ()
    for f in cmd.argv :
        directories.add (create_css_file (f, keywords))
    if cmd.watch_files :
        if not pyinotify :
            print "No python bindings for libinotify"
            raise SystemExit, 42
        watch_directories (keywords, * directories)
# end def main

if __name__ == "__main__":
    main (command_spec ())
### __END__ expand_CSS
