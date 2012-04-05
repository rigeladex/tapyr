# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW.File_Session
#
# Purpose
#    Session backend which stores the information in a file on the disk
#
# Revision Dates
#    25-Jan-2010 (MG) Creation
#    19-Feb-2010 (MG) Moved from `GTW.Tornado` into `GTW`
#    10-Mar-2011 (CT) Property `_file_name` renamed to `file_name`,
#                     `exists` and `file_name` changed to use factored method
#                     `_file_name` (previously, `exists` and `_file_name`
#                     differed erroneously)
#    11-May-2011 (MG) `file_name` changed from `Once_Property` to `property`
#                     (because `_sid` can changed during the lifetime of the
#                     session object)
#     5-Apr-2012 (CT) Sort alphabetically
#    ««revision-date»»···
#--
from   _TFL._Meta.Once_Property import Once_Property
from   _GTW                     import GTW
import _GTW.Session
import  cPickle
import  os

class File_Session (GTW.Session) :
    """Stores the session data in a file on disk.

    >>> session = File_Session ()
    >>> session.save ()
    >>> session ["name"] = "user1"
    >>> session ["lang"] = "de_AT"
    >>> session.save ()

    >>> session2 = File_Session (session.sid)
    >>> sorted (session._data.items ())
    [('lang', 'de_AT'), ('name', 'user1')]
    >>> sorted (session2._data.items ())
    [('lang', 'de_AT'), ('name', 'user1')]
    >>> session.sid == session2.sid
    True
    >>> session.name
    'user1'
    >>> session.name == session2 ["name"]
    True
    >>> session.lang == session2 ["lang"]
    True
    >>> session.get ("lang")
    'de_AT'
    >>> del session.lang
    >>> print session.get ("lang")
    None
    >>> session.get ("lang") == session2 ["lang"]
    False
    >>> session.remove ()
    >>> session3 = File_Session (session.sid)
    >>> session3.get ("name"), session.name
    (None, 'user1')
    >>> session3.get ("lang"), session.lang
    (None, None)
    """

    base_path       = "/tmp"
    _non_data_attrs = set (("file_name", ))

    @property
    def file_name (self) :
        return self._file_name (self.sid)
    # end def file_name

    def exists (self, sid) :
        return os.path.exists (self._file_name (sid))
    # end def exists

    def remove (self) :
        try :
            os.unlink (self.file_name)
        except EnvironmentError :
            pass
    # end def remove

    def save (self) :
        with open (self.file_name, "wb") as f :
            cPickle.dump (self._data, f)
    # end def save

    def _file_name (self, sid) :
        return os.path.join (self.base_path, "%s.sid" % (sid, ))
    # end def _file_name

    def _load (self) :
        try :
            with open (self.file_name, "rb") as f :
                return cPickle.load (f)
        except :
            return {}
    # end def _load

# end class File_Session

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.File_Session
