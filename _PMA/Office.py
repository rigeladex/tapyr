# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    PMA.Office
#
# Purpose
#    Model a personal post office which contains a delivery and a storage
#    area
#
# Revision Dates
#     3-Jan-2005 (CT) Creation
#    25-Jul-2005 (CT) `_storage_boxes` factored and changed to look at all
#                     toplevel directories except for the `delivery_area`
#    25-Jul-2005 (CT) s/save_msg_status/save_status/
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib
import _PMA.Mailbox
import _TFL._Meta.Object

import Environment
import sos
from   subdirs                 import subdirs

class Office (TFL.Meta.Object) :
    """Personal post office"""

    def __init__ (self, root = None) :
        self.path           = path = self.default_path  (root)
        self.delivery_area  = da   = self.delivery_path (path)
        self.msg_status_fn  = msfn = sos.path.join      (path, ".msg.status")
        PMA.Msg_Status.load                             (msfn)
        self.delivery_boxes = self._delivery_boxes      (da)
        self.storage_boxes  = self._storage_boxes       (path, da)
    # end def __init__

    def msg_boxes (self, transitive = False) :
        for b in self.delivery_boxes + self.storage_boxes :
            yield b
            if transitive :
                for sb in self.sub_boxes (b, transitive) :
                    yield sb
    # end def msg_boxes

    def save_status (self) :
        PMA.Msg_Status.save (self.msg_status_fn)
    # end def save_status

    def sub_boxes (self, box, transitive = False) :
        for sb in box.sub_boxes :
            yield sb
            if transitive :
                for ssb in self.sub_boxes (sb, transitive) :
                    yield ssb
    # end def sub_boxes

    def _delivery_boxes (self, da) :
        prefix = sos.path.split (da) [-1]
        dirs   = subdirs (da)
        if not dirs :
            inbox = self._path (da, "inbox")
            for d in "cur", "new", "tmp" :
                self._path (inbox, d)
            dirs.append (inbox)
        return [PMA.Maildir (d, prefix = prefix) for d in dirs]
    # end def _delivery_boxes

    def _storage_boxes (self, path, da) :
        return [PMA.Mailbox (sa) for sa in subdirs (path) if sa != da]
    # end def _storage_boxes

    ### class methods
    def default_path (cls, root = None) :
        if root is None :
            root = Environment.home_dir
        return cls._path (root, "PMA")
    default_path = classmethod (default_path)

    def delivery_path (cls, root) :
        return cls._path (root, "D")
    delivery_path = classmethod (delivery_path)

    def storage_path (cls, root) :
        return cls._path (root, "S")
    storage_path = classmethod (storage_path)

    def _path (cls, root, stem) :
        result = sos.path.join (root, stem)
        if not sos.path.isdir (result) :
            sos.mkdir (result)
        return result
    _path = classmethod (_path)

# end class Office

"""
from   _PMA                    import PMA
from   _PMA.Office             import *
import _PMA.Mailbox
o  = Office ()
mb = PMA.MH_Mailbox ("/swing/private/tanzer/MH/Firma")
o.storage_boxes [0].add_subbox (mb, transitive = True)

"""
if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Office
