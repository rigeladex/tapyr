# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
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
    >>> session._save ()
    >>> session ["name"] = "user1"
    >>> session ["lang"] = "de_AT"
    >>> session._save ()
    >>> session2 = File_Session (session.sid)
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

    base_path = "/tmp"

    def exists (self, sid) :
        return os.path.exists (os.path.join (self.base_path, sid))
    # end def exists

    @Once_Property
    def _file_name (self) :
        return os.path.join (self.base_path, "%s.sid" % (self.sid, ))
    # end def _file_name

    def _load (self) :
        try :
            return cPickle.load (open (self._file_name, "rb"))
        except :
            return {}
    # end def _load

    def save (self) :
        cPickle.dump (self._data, open (self._file_name, "wb"))
    # end def save

    def remove (self) :
        os.unlink (self._file_name)
    # end def remove

# end class File_Session

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.File_Session


