# -*- coding: iso-8859-1 -*-
# Copyright (C) 2001-2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.FDB.Record
#
# Purpose
#    Model a record in a file-based DB
#
# Revision Dates
#    21-Jan-2001 (CT) Creation
#    27-Jan-2001 (CT) `matches' corrected (to handle list-valued fields)
#    27-Jan-2001 (CT) `_test_match' factored
#    22-Apr-2003 (CT) Moved to package `TFL.FDB`
#    22-Apr-2003 (CT) `field_pat` changed to allow for `key` and modifier
#    22-Apr-2003 (CT) `_split` changed to populate `_keys`
#    28-Sep-2004 (CT) Use `isinstance` instead of type comparison
#    ««revision-date»»···
#--

from   _TFL._FDB import FDB
from   Regexp    import *
import string

class Record :
    """Model a record in a file-based DB."""

    field_sep = Regexp ("\n(?!\\s)") ### a new-line followed by non-whitespace
    field_pat = Regexp ( r"(?P<name> "
                           r"    (?P<key>      [A-Za-z][A-Za-z0-9_]*"
                           r"(?: (?P<modifier> [A-Za-z0-9_\\-]+) )?"
                         r")"
                         r"\s* : \s*"
                         r"(?P<value> .*)"
                       , re.VERBOSE | re.DOTALL
                       )

    def __init__ (self, path, folder, name, body) :
        self._path    = path
        self.folder   = folder
        self.name     = name
        self._body    = body
        self._matches = []
    # end def __init__

    def add (self, name, value) :
        """Add field `name' with `value'"""
        fields = self._fields
        if name in fields :
            if isinstance (fields [name], (str, unicode)) :
                fields [name] = [fields [name]]
            fields [name].append (value)
        else :
            fields [name] = value
            self._seq.append (name)
    # end def add

    def keys (self) :
        return self._seq
    # end def keys

    def items (self) :
        return map (lambda n, f = self._fields : (n, f [n]), self._seq)
    # end def items

    def values (self) :
        return map (lambda n, f = self._fields : f [n], self._seq)
    # end def values

    def write (self, path = None) :
        """Write `str (self)' to `path or self._path'"""
        path = path or self._path
        if isinstance (path, str) :
            file = open (path, "w")
            self._write (file)
            file.close  ()
        else :
            self._write (path)
    # end def write

    def _test_match (self, field, value, pattern, result) :
        match = pattern.search (value)
        if match :
            result.append ((field, match))
    # end def _test_match

    def matches (self, * pats, ** field_pats) :
        """Returns list of matches for `pats' and `field_pats'."""
        result = self._matches = []
        test   = self._test_match
        for p in pats :
            test (None, self._body, p, result)
        for f, p in field_pats.items () :
            v = getattr (self, f, "")
            if v :
                if isinstance (v, (list, tuple)) :
                    for w in v :
                        test (f, w, p, result)
                else :
                    test (f, v, p, result)
        if len (result) != (len (pats) + len (field_pats)) :
            self._matches = []
        return self._matches
    # end def matches

    def _write (self, file) :
        file.write (str (self))
        file.write ("\n")
    # end def _write

    def __getattr__ (self, name) :
        if name in ("_fields", "_seq", "_keys") :
            self._split ()
            return getattr (self, name)
        else :
            try :
                return self._fields [name]
            except KeyError :
                pass
        raise AttributeError, name
    # end def __getattr__

    def __getitem__ (self, index) :
        if isinstance (index, str) :
            return self._fields [index]
        else :
            return self._fields [self._seq [index]]
    # end def __getitem__

    def _split (self) :
        fields        = filter (None, self.field_sep.split (self._body))
        pat           = self.field_pat
        self._fields  = {}
        self._keys    = {}
        self._seq     = []
        self._errors  = []
        for f in fields :
            f = string.strip (f)
            if pat.match (f) :
                self.add (pat.name, pat.value)
                if pat.key in self._keys :
                    if pat.name not in self._keys [key] :
                        self._keys [key].append (name)
                else :
                    self._keys [key] = [name]
            else :
                self._errors.append (f)
    # end def _split

    def __str__ (self) :
        result = []
        width  = max (map (lambda k : len (k), self.keys ()) + [0])
        format = "%%-%ds : %%s" % (width, )
        for n, v in self.items () :
            if isinstance (v, (list, tuple)) :
                for w in v :
                    r = self.field_sep.sub ("\n    ", format % (n, w))
                    result.append (r)
            else :
                r = self.field_sep.sub ("\n    ", format % (n, v))
                result.append (r)
        return string.join (result, "\n")
    # end def __str__

# end class Record

if __name__ != "__main__":
    FDB._Export ("Record")
### __END__ TFL.FDB.Record
