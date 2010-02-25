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
#    GTW.Notification
#
# Purpose
#    A framework for user notification in a web application
#
# Revision Dates
#    20-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--
"""
Short test for the notification framework
    >>> from _GTW.File_Session import File_Session
    >>> time1   = datetime.datetime (2010, 2, 20, 11, 42, 00)
    >>> time2   = datetime.datetime (2010, 2, 20, 11, 42, 42)
    >>> session = File_Session ()
    >>> sid     = session.sid

    >>> nc = Notification_Collection (session)
    >>> nc.append (Notification ("Password reset mail has been sent", time2))
    >>> nc.append (Notification ("User has been logged out",          time1))
    >>> nc
    [Notification ('Password reset mail has been sent', datetime.datetime(2010, 2, 20, 11, 42, 42)), Notification ('User has been logged out', datetime.datetime(2010, 2, 20, 11, 42))]
    >>> session.save                 ()

    >>> session2 = File_Session (sid)
    >>> session != session2
    True
    >>> session2.notifications
    [Notification ('Password reset mail has been sent', datetime.datetime(2010, 2, 20, 11, 42, 42)), Notification ('User has been logged out', datetime.datetime(2010, 2, 20, 11, 42))]
    >>> print session2.notifications.discarge ()
    User has been logged out
    Password reset mail has been sent
    >>> print session2.notifications.discarge ()
    <BLANKLINE>
    >>> session.remove ()
"""

from   _TFL                import TFL
import _TFL._Meta.Object

from   _GTW                import GTW

import  datetime

class M_Notification_Collection (list.__class__) :
    """Meta class implementing a singleton pattern"""

    session_key = "notifications"

    def __call__ (cls, session, * args) :
        if cls.session_key not in session :
            session [cls.session_key] = super \
                (M_Notification_Collection, cls).__call__ (* args)
        return session [cls.session_key]
    # end def __call__

# end class M_Notification_Collection

class Notification_Collection (list) :
    """Collection of all notifications for a session."""

    __metaclass__ = M_Notification_Collection

    def discarge (self, head = "", joiner = "\n", tail = "") :
        result = [head]
        result.append \
            ( joiner.join
                (unicode (s) for s in sorted (self, key = lambda n : n.time))
            )
        result.append (tail)
        self [:] = []
        return "".join (result)
    # end def discarge

# end class Notification_Collection

class Notification (TFL.Meta.Object) :
    """A notification based on plain text."""

    def __init__ (self, message, time = None) :
        self.message = message
        self.time    = time or datetime.datetime.now ()
    # end def __init__

    def __str__ (self) :
        return self.message
    # end def __str__

    def __unicode__ (self) :
        return self.message
    # end def __unicode__

    def __repr__ (self) :
        return \
           "%s (%r, %r)" % (self.__class__.__name__, self.message, self.time)
    # end def __repr__

# end class Notification

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Notification
