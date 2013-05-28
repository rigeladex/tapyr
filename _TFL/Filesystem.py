# -*- coding: iso-8859-15 -*-
# Copyright (C) 2001-2013 Mag. Christian Tanzer. All rights reserved
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
#    Filesystem
#
# Purpose
#    Model filesystems, directories, and files
#
# Revision Dates
#    29-Apr-2001 (CT) Creation
#     3-May-2001 (CT) Doc-test framework added at end
#     7-May-2001 (CT) `Filter' renamed to `Regexp_Filter' (and re.escape
#                     removed)
#     7-May-2001 (CT) `Glob_Filter' added
#    28-Sep-2004 (CT) Use `isinstance` instead of type comparison
#    24-Mar-2005 (CT) Use `TFL.sos` instead of `sos`
#    ««revision-date»»···
#--

from   _TFL      import TFL

import _TFL.sos
import dircache
import fnmatch
import re
import stat

class File :
    """Model a file

       Attributes:

       - name            base name of file
       - parent          pointer to directory containing file
       - full_name       file name containing full path
       - permissions     permission bits of file

       and all file attributes returned by `stat'.
    """

    _stat_map = \
        { "atime" : stat.ST_ATIME
        , "ctime" : stat.ST_CTIME
        , "dev"   : stat.ST_DEV
        , "gid"   : stat.ST_GID
        , "ino"   : stat.ST_INO
        , "mode"  : stat.ST_MODE
        , "mtime" : stat.ST_MTIME
        , "nlink" : stat.ST_NLINK
        , "size"  : stat.ST_SIZE
        , "uid"   : stat.ST_UID
        }

    def __init__ (self, name, parent = None, ** kw) :
        p, self.name = TFL.sos.path.split (name)
        assert not (p and parent)
        if p :
            if p != "/" : ### XXX support other OSes than Unix, too
                self.parent = self.__class__ (p, ** kw)
            else :
                self.parent = Root ()
        else :
            self.parent = parent
        self.__dict__.update (kw)
        if TFL.sos.path.isdir (self.full_name) :
            self.__class__ = Directory
    # end def __init__

    def __getattr__ (self, name) :
        if name == "full_name" :
            if self.parent :
                result = TFL.sos.path.join (self.parent.full_name, self.name)
            else :
                result = self.name
            self.full_name = result
            return result
        elif name in self._stat_map:
            stat_info = TFL.sos.stat (self.full_name)
            for k, v in self._stat_map.items () :
                setattr (self, k, stat_info [v])
            return getattr (self, name)
        elif name == "permissions" :
            result = self.permissions = stat.S_IMODE (self.mode)
            return result
        raise AttributeError, name
    # end def __getattr__

    def isdir (self) :
        """Returns true if `self' is a directory"""
        try :
            return stat.S_ISDIR (self.mode)
        except OSError :
            return 0
    # end def isdir

    def isfile (self) :
        """Returns true if `self' is a regular file"""
        try :
            return stat.S_ISREG (self.mode)
        except OSError :
            return 0
    # end def isfile

    def islink (self) :
        """Returns true if `self' is a symbolic link"""
        try :
            return stat.S_ISLNK (self.mode)
        except OSError :
            return 0
    # end def islink

    is_dir  = isdir
    is_file = isfile
    is_link = islink

    def __str__ (self) :
        return self.full_name
    # end def __str__

    def __repr__ (self) :
        return """%s ("%s")""" % (self.__class__.__name__, self.full_name)
    # end def __repr__

# end class File

class Directory (File) :
    """Model a directory"""

    _all_children = []
    _files        = []
    _subdirs      = []
    filter        = None

    File          = File

    def files (self) :
        """Return all files in `self' matching `self.filter'"""
        all = dircache.listdir (self.full_name)
        if all != self._all_children or not self._files :
            self._all_children = all
            if callable (self.filter) :
                F = self.filter
            else :
                F = TFL.sos.path.isfile
            result      = filter (F, all)
            self._files = [ self.File (f, parent = self, filter = F)
                            for f in result
                          ]
        return self._files
    # end def files

    def subdirectories (self) :
        """Return all subdirectories of `self'"""
        all = dircache.listdir (self.full_name)
        if all != self._all_children or not self._subdirs :
            self._all_children = all
            self._subdirs = [ self.File (d, parent = self, filter = self.filter)
                              for d in all
                            ]
            self._subdirs = [ d for d in self._subdirs
                                if isinstance (d, Directory)
                            ]
        return self._subdirs
    # end def subdirectories

    def __setattr__ (self, name, value) :
        if name == "filter" and value != self.filter :
            ### invalidate cached directory listing
            self._all_children = []
        self.__dict__ [name] = value
    # end def __setattr__

# end class Directory

### XXX support other OSes than Unix, too
class Root (Directory) :
    """Model root of filesystem"""

    parent = None

    def __init__ (self) :
        self.full_name = self.name = "/"
    # end def __init__

# end class Root

class Regexp_Filter :
    """Filter using regular expressions"""

    def __init__ (self, pattern) :
        if isinstance (pattern, (str, unicode)) :
            pattern = re.compile (pattern)
        self.pattern = pattern
    # end def __init__

    def __call__ (self, name) :
        return self.pattern.search (name)
    # end def __call__

    def __str__ (self) :
        return self.pattern.pattern
    # end def __str__

    def __repr__ (self) :
        return "%s (%r)" % \
               (self.__class__.__name__, self.pattern.pattern)
    # end def __repr__

# end class Regexp_Filter

class Glob_Filter (Regexp_Filter) :
    """Filter using glob-style patterns"""

    Ancestor = __Ancestor = Regexp_Filter

    def __init__ (self, pattern) :
        self.__Ancestor.__init__ (self, fnmatch.translate (pattern))
    # end def __init__

# end class Glob_Filter

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Filesystem
