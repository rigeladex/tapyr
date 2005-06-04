# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TGL.Threading
#
# Purpose
#    Simple threading classes.
#
# Revision Dates
#     4-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                import TGL
from   _TFL                import TFL
import _TFL._Meta.Object
import  threading

class _Thread_ (TFL.Meta.Object, threading.Thread) :
    """Simple thread class"""

    real_name = "Thread"

    def __init__ (self, command, * args, ** kw) :
        if "name" in kw :
            name = kw ["name"]
            del kw ["name"]
        else :
            name = None
        self.__super.__init__ \
            ( group  = None
            , target = command
            , name   = name
            , args   = args
            , kwargs = kw
            )
        self.finished = False
    # end def __init__

    def run (self) :
        result        = self.__super.run ()
        self.finished = True
        return result
    # end def run

Thread = _Thread_ # end class Thread

if __name__ != "__main__" :
    TGL._Export ("Thread")
else :
    import _TFL.sos as os
    import time
    def Send_Mail (mail) :
        os.system ("emacsclient %d" % (mail, ))
        print "And now send the mail using PMA..."
    # end def Send_Mail

    t = Thread (Send_Mail, 1)
    t.start    ()
    c = 0
    while not t.finished :
        print "Wait for sending the mail %2d" % (c, )
        c += 1
        time.sleep (2)
### __END__ TGL.Threading
