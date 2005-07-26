# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    PMA.Box_Status
#
# Purpose
#    Encapsulate status of mailbox
#
# Revision Dates
#    26-Jul-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _TFL._Meta.Property     import prop
from   _PMA                    import PMA
import _PMA._Status_

import cPickle                 as     pickle

class Box_Status (PMA._Status_) :
    """Status of mailbox"""

    def __init__ (self, box, * attr) :
        self.__dict__ ["box"] = box
        self.__super.__init__ (* attr)
    # end def __init__

    @prop
    def current_message () :
        def get (self) :
            result = None
            cmn    = self._attr.get ("current_message")
            if cmn is not None :
                result = self.box.msg_dict.get (cmn)
            return result
        def set (self, cm) :
            self._set_attr (current_message = cm and cm.name)
        return get, set
    # end def current_message

    def load (self, filename) :
        try :
            f = open (filename)
        except IOError :
            pass
        else :
            try :
                try :
                    attrs = pickle.load (f)
                except EOFError :
                    pass
                else :
                    if attrs :
                        print self.box.qname, attrs
                    self._set_attr (** attrs)
            finally :
                f.close ()
    # end def load

    def save (self, filename) :
        f = open    (filename, "wb")
        pickle.dump (self._attr, f, pickle.HIGHEST_PROTOCOL)
        f.close     ()
    # end def save

# end class Box_Status

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Box_Status
