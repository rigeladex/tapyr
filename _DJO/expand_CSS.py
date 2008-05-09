# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2008 Mag. Christian Tanzer. All rights reserved
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
#    16-Dec-2007 (MG) Exception handling added
#    19-Apr-2008 (MG) Template handling moved into a class to support
#                     dependency tracking and automatic css file recreation
#                     based on changes of a parameter file
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL.Filename
from   _TFL.Caller            import Scope
import _TFL._Meta.Object
import _TFL.defaultdict
import _TFL.sos               as     os
import _TFL.Record
import  re
import  traceback

class CSS_Template (TFL.Meta.Object) :
    """Models a css template and teh dependencies to parameter files."""


    parameter_files = TFL.defaultdict (set)
    templates       = {}
    fix_percent_pat = re.compile ("%([^(])")

    def __init__ (self, template, parameter_file = None, css_file = None) :
        self.count    = 0
        self.template = TFL.Filename \
            (template, "filename.css_template", absolute = True)
        self.css_file = TFL.Filename (css_file or ".css", self.template)
        self.pdict    = {}
        if not os.path.isfile (self.template.name) :
            raise ValueError ("`%s` does not exist" % (self.template.name, ))
        self.templates [self.template.name] = self
        self.parameter_file = TFL.Filename \
            (parameter_file or ".parameters", self.template)
        if os.path.isfile (self.parameter_file.name) :
            self._update_dependencies    ()
        else :
            print "*** no parameter file for", self.template.name
            self.parameter_file = None
    # end def __init__

    def create_css_file (self, overrides = {}) :
        try :
            self.pdict = {} ### lets clear it again before we read everything
            self._update_dependencies ()
            ct    = open         (self.template.name).read ()
            ct, _ = self.fix_percent_pat.subn \
                (lambda m : "%%%s" % (m.group (0), ), ct)
            outf  = open  (self.css_file.name, "wb")
            outf.write    (ct % Scope (globs = self.pdict, locls = overrides))
            outf.close    ()
            print "[%04d] CSS file created `%s`" \
                % (self.count, self.css_file.name, )
            self.count += 1
        except :
            traceback.print_exc ()
    # end def create_css_file

    @classmethod
    def find_templates (cls, directory, recursive = False) :
        for file in os.listdir_full (directory) :
            if os.path.isdir (file) :
                if recursive :
                    cls.find_templates (file, recursive = True)
            if file.endswith (".css_template") and not "#" in file :
                cls (file)
    # end def find_templates

    def _update_dependencies (self, filename = None) :
        if filename is None :
            filename = self.parameter_file.name
        self.parameter_files [os.path.abspath (filename)].add (self)
        new_dir = TFL.Filename (filename).directory
        if new_dir :
            old_dir = os.getcwd ()
            os.chdir (new_dir)
        execfile \
             ( filename
             , dict
                 ( R       = TFL.Record
                 , include = self._update_dependencies
                 )
             , self.pdict
             )
        if new_dir :
            os.chdir (old_dir)
    # end def _update_dependencies

# end class CSS_Template

def watch_directories (overrides, * directories) :
    import pyinotify
    watch  = pyinotify.WatchManager ()
    events = \
        pyinotify.EventsCodes.IN_MODIFY | pyinotify.EventsCodes.IN_CREATE

    class Event_Prcoessor (pyinotify.ProcessEvent) :

        def process_IN_MODIFY (self, event) :
            self.update_changed_files (event)
        # end def process_IN_MODIFY

        def process_IN_CREATE (self, event) :
            self.update_changed_files (event)
        # end def process_IN_MODIFY

        def update_changed_files (self, event) :
            fn = TFL.Filename (os.path.join (event.path, event.name))
            if not fn.base.startswith (".#") :
                fn = os.path.abspath (fn.name)
                # we ignore temp files created by emacs
                if fn in CSS_Template.templates :
                    self.changed_files.add (CSS_Template.templates [fn])
                elif fn in CSS_Template.parameter_files :
                    self.changed_files.update \
                        (CSS_Template.parameter_files [fn])
        # end def update_changed_files

    # end class Event_Prcoessor

    event_processor               = Event_Prcoessor ()
    event_processor.changed_files = set ()
    notifier                      = pyinotify.Notifier (watch, event_processor)
    for d in directories :
        watch.add_watch (d, events, rec = False)

    while True:  # loop forever
        try:
            # process the queue of events as explained above
            notifier.process_events ()
            for fn in event_processor.changed_files :
                fn.create_css_file (overrides)
            event_processor.changed_files = set ()
            if notifier.check_events ():
                # read notified events and enqeue them
                notifier.read_events ()
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
              ( "watch_directories:P,?List of directories to watch for changes"
              ,
              )
        , min_args         = 0
        , process_keywords = True
        , arg_array        = arg_array
        )
# end def command_spec

def main (cmd) :
    keywords    = cmd.keywords
    directories = set ()
    if cmd.template :
        for f in cmd.argv :
            CSS_Template (f).create_css_file (keywords)
    if cmd.watch_directories :
        for d in cmd.watch_directories :
            CSS_Template.find_templates (d, False)
        for t in CSS_Template.templates.itervalues () :
            t.create_css_file (keywords)
        watch_directories (keywords, * cmd.watch_directories)
# end def main

if __name__ == "__main__":
    main (command_spec ())
### __END__ expand_CSS
