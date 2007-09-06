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
#    26-Jul-2005 (CT) `save_status` changed to call `save_status` of each
#                     mailbox
#    26-Jul-2005 (CT) `load_status` factored and handling of `Off_Status` added
#    29-Jul-2005 (CT) `storage_path` removed (dead code)
#    29-Jul-2005 (CT) Ignore directories starting with `.`
#    30-Jul-2005 (MG) `commit` added
#     7-Aug-2005 (CT) `extra_delivery_boxes` added and import of
#                     `Pop3_Mailbox` removed (let ~/PMA/.config.py do that)
#     2-Jan-2006 (CT) `dbx_matchers` added
#     5-Jan-2006 (CT) `_new_delivery_box` factored and changed to load
#                     mailbox-specific config file, if any
#    24-Jan-2006 (MG) `virtual_mailbox_path` added
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _TGL                    import TGL
from   _PMA                    import PMA
from   _PMA                    import Lib
import _PMA.Mailbox
import _PMA.Off_Status
import _TFL.Environment
import _TFL._Meta.Object
import _TFL.sos                as     sos
import _TGL.load_config_file

from   _TFL.subdirs            import subdirs

class Office (TFL.Meta.Object) :
    """Personal post office"""

    top_name             = "PMA"
    delivery_area_name   = "Delivery"
    virtual_root         = ".virtual"

    dbx_matchers         = ()
    extra_delivery_boxes = []

    def __init__ (self, root = None) :
        self.path           = path = self.default_path  (root)
        self.delivery_area  = da   = self.delivery_path (path)
        self.load_status                                (path)
        self.delivery_boxes = self._delivery_boxes      (da)
        self.storage_boxes  = self._storage_boxes       (path, da)
    # end def __init__

    def commit (self) :
        for kind in self.delivery_boxes, self.storage_boxes :
            for box in kind :
                box.commit_all (transitive = True)
    # end def commit

    def load_status (self, path) :
        self.status         = stat = PMA.Off_Status (self)
        self.status_fn      = stfn = sos.path.join  (path, ".status")
        self.msg_status_fn  = msfn = sos.path.join  (path, ".msg.status")
        stat.load           (stfn)
        PMA.Msg_Status.load (msfn)
    # end def load_status

    def msg_boxes (self, transitive = False) :
        for b in self.delivery_boxes + self.storage_boxes :
            yield b
            if transitive :
                for sb in self.sub_boxes (b, transitive) :
                    yield sb
    # end def msg_boxes

    def save_status (self) :
        self.status.save    (self.status_fn)
        PMA.Msg_Status.save (self.msg_status_fn)
        for b in self.msg_boxes (transitive = True) :
            b.save_status ()
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
        dirs   = \
            [ d for d in subdirs (da)
                if  not sos.path.split (d) [-1].startswith (".")
            ]
        if not dirs :
            inbox = self._path (da, "inbox")
            for d in "cur", "new", "tmp" :
                self._path (inbox, d)
            dirs.append (inbox)
        return \
            ( self.extra_delivery_boxes
            + [self._new_delivery_box (d, prefix) for d in dirs]
            )
    # end def _delivery_boxes

    def _new_delivery_box (self, d, prefix) :
        config = TGL.load_config_file \
            ( sos.path.join (d, ".config.py")
            , dict
                ( Maildir_Type = PMA.Maildir
                , Maildir_kw   = {}
                , PMA          = PMA
                )
            )
        result = config ["Maildir_Type"] \
            (d, prefix = prefix, ** config ["Maildir_kw"])
        result.config = config
        return result
    # end def _new_delivery_box

    def _storage_boxes (self, path, da) :
        return \
            [   PMA.Mailbox (sa)
            for sa in subdirs (path) if sa != da
            if  not sos.path.split (sa) [-1].startswith (".")
            ]
    # end def _storage_boxes

    @classmethod
    def default_path (cls, root = None) :
        if root is None :
            root = TFL.Environment.home_dir
        return cls._path (root, cls.top_name)
    # end def default_path

    @classmethod
    def delivery_path (cls, root) :
        return cls._path (root, cls.delivery_area_name)
    # end def delivery_path

    @classmethod
    def virtual_mailbox_path (cls) :
        return cls._path (cls.default_path (), cls.virtual_root)
    # end def virtual_mailbox_path

    @classmethod
    def _path (cls, root, stem) :
        result = sos.path.join (root, stem)
        if not sos.path.isdir (result) :
            sos.mkdir (result)
        return result
    # end def _path

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
