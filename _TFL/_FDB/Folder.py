# Copyright (C) 2001-2003 Mag. Christian Tanzer. All rights reserved
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
#    TFL.FDB.Folder
#
# Purpose
#    Model a folder in a file-based DB
#
# Revision Dates
#    21-Jan-2001 (CT) Creation
#    22-Apr-2003 (CT) Moved to package `TFL.FDB`
#    ««revision-date»»···
#--

from   _TFL._FDB  import FDB
from   Filename   import *
from   subdirs    import *

import _TFL._FDB.Record

class Folder :
    """Model a folder in a file-based DB."""

    extension = ".fdb"

    def __init__ (self, path, top = "", transitive = 0, parent = None) :
        self.path       = path = Filename ("", default_dir = path)
        self.top        = top  = Filename ("", default_dir = top)
        self.transitive = transitive
        self.qname      = path.directory    [len (top.directory) + 1: ]
        self.name       = sos.path.basename (self.qname)
        self._parent    = parent
        self._get_files ()
        if transitive :
            self._get_folders (transitive)
    # end def __init__

    def matches (self, * pats,  ** field_pats) :
        """Returns list of elements matching `pats' and `field_pats'."""
        result = []
        for f in self.files.values () :
            if apply (f.matches, pats, field_pats) :
                result.append (f)
        return result
    # end def matches

    def __getattr__ (self, name) :
        if name == "folders" :
            self._get_folders (self.transitive)
            return self.folders
        elif name == "fields" :
            self._get_fields ()
            return self.fields
        elif name == "parent" :
            self._get_parent ()
            return self.parent
        raise AttributeError, name
    # end def __getattr__

    def _get_folders (self, transitive) :
        self.folders = {}
        for f in subdirs (self.path.name) :
            folder = self.__class__ ( f
                                    , top        = self.top.directory
                                    , transitive = transitive
                                    , parent     = self
                                    )
            self.folders [folder.qname] = folder
    # end def _get_folders

    def _get_files (self) :
        self.files = {}
        for f in sos.listdir_ext (self.path.name, self.extension) :
            fn   = Filename  (f)
            file = open      (f)
            body = file.read ()
            file.close       ()
            self.files [fn.base] = FDB.Record (f, self.qname, fn.base, body)
    # end def _get_files

    def _get_fields (self) :
        self.fields = []
        try :
            file        = sos.path.join (self.path.directory, ".fields")
            self.fields = filter ( None
                                 , map (string.strip, open (file).readlines ())
                                 )
        except IOError :
            if self.parent :
                self.fields = self.parent.fields
    # end def _get_fields

    def _get_parent (self) :
        if self._parent :
            self.parent = self._parent
        else :
            path = self.path.directory
            if path != self.top.directory :
                self.parent = self.__class__ ( sos.path.dirname (path)
                                             , top        = self.top
                                             , transitive = 0
                                             )
            else :
                self.parent = None
    # end def _get_parent

    def __str__ (self) :
        return self.qname
    # end def __str__

    def __repr__ (self) :
        return "(%s, %s, %s, %s, %s)" % ( self.path.directory
                                        , self.top.directory
                                        , len (self.folders)
                                        , len (self.files)
                                        , self.parent
                                        )
    # end def __repr__

# end class Folder

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line
    return Command_Line \
        ( arg_spec         =
            ( "pattern:S?"
                "Pattern to match anywhere in the file"
            ,
            )
        , option_spec      =
            ( "-extension:S=%s?Extension of files in DB" % Folder.extension
            , "-folder:S?Folder of file DB to match in"
            , "-Full:B?Print matching files fully"
            , "-Regexp:B?Interpret the patterns as regular expressions"
            , "-root:S?Root directory of file DB"
            , "-summary:B?Print names of matching files, only"
            , "-transitive:B?Match in all folders"
            )
        , description      =
            "Print all files of file DB matching the "
            "specified patterns. Specific fields can be "
            "matched by using keyword notation: "
            "`field-name=pattern'."
        , arg_array        = arg_array
        , process_keywords = 1
        )
# end def command_spec

def main (cmd) :
    from Regexp import *
    Folder.extension = cmd.extension
    ff               = Folder (cmd.folder, cmd.root, cmd.transitive)
    quote            = not cmd.Regexp
    pats             = map ( lambda p, q = quote, R = Regexp
                           : R (p, quote = q)
                           , filter (None, cmd.argv.body)
                           )
    field_pats       = {}
    map ( lambda (f, p), q = quote, R = Regexp, field_pats = field_pats
        : field_pats.update ({f : R (p, quote = q)})
        , cmd.keywords.items ()
        )
    matches = apply (ff.matches, pats, field_pats)
    if cmd.summary :
        for fr in matches :
            print fr._path
    elif cmd.Full :
        for fr in matches :
            print "*" * 15, fr._path, "*" * (77 - 15 - len (fr._path))
            print fr
            print
    else :
        for fr in matches :
            print "*" * 15, fr._path, "*" * (77 - 15 - len (fr._path))
            for f, m in fr._matches :
                if f :
                    print "%s : %s" % (f, getattr (fr, f))
# end def main

if __name__ == "__main__":
    main (command_spec ())
else :
    FDB._Export ("Folder")
### __END__ TFL.FDB.Folder
