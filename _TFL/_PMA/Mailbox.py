# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    Mailbox
#
# Purpose
#    Model a mailbox
#
# Revision Dates
#     3-Sep-2004 (CT) Creation
#     4-Sep-2004 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _TFL._PMA               import Lib
import _TFL._PMA.Message
import _TFL._Meta.Object

from   predicate               import *
from   subdirs                 import subdirs
import sos

class Mailbox (TFL.Meta.Object) :
    """Root class for mailbox classes"""

    messages           = property (lambda s : s._get_messages ())

    def __init__ (self, path) :
        self.path      = path
        self._messages = None
        self.sub_boxes = []
    # end def __init__

    def sort (self, decorator = None) :
        if decorator is None :
            decorator = lambda m : m.time
        self._messages = dusort (self.messages, decorator)
        for i, m in enumerate (self._messages) :
            m.number = i + 1
    # end def sort

    def summary (self, format = "%-99.99s") :
        return "\n".join ([format % m.summary () for m in self.messages])
    # end def summary

    def _get_messages (self) :
        if self._messages is None :
            self._setup_messages ()
            self.sort ()
        return self._messages
    # end def _get_messages

    def _new_email (self, fp) :
        result = Lib.message_from_file (fp)
        result._pma_path = fp.name
        return result
    # end def _new_email

    def _new_message (self, m) :
        return TFL.PMA.Message (email = m, name = m._pma_path, mailbox = self)
    # end def _new_message

    def __str__ (self) :
        return self.summary ()
    # end def __str__

    def __repr__ (self) :
        if self._messages is None :
            return "%s %s: %d sub-boxes" % \
                (self.__class__.__name__, self.path, len (self.sub_boxes))
        else :
            return "%s %s: %d messages, %d sub-boxes" % \
                ( self.__class__.__name__, self.path
                , len (self._messages), len (self.sub_boxes)
                )
    # end def __repr__

# end class Mailbox

class _Mailbox_in_Dir_ (Mailbox) :
    """Model directory-based mailbox"""

    def __init__ (self, path) :
        self.__super.__init__ (path)
        self.sub_boxes = [self.__class__ (s) for s in self._subdirs (path)]
    # end def __init__

    def _setup_messages (self) :
        self._messages = \
            [ self._new_message (m)
              for m in self.MB_Type (self.path, self._new_email)
            ]
    # end def _setup_messages

    def _subdirs (self, path) :
        return subdirs (path)
    # end def _subdirs

# end class _Mailbox_in_Dir_

class _Mailbox_in_File_ (Mailbox) :
    """Model file-based mailbox"""

    def _setup_messages (self) :
        f = open (self.path, "r")
        try :
            self._messages = \
                [ self._new_message (m)
                  for m in self.MB_Type (f, self._new_email)
                ]
        finally :
            f.close ()
    # end def _setup_messages

# end class _Mailbox_in_File_

class Unix_Mailbox (_Mailbox_in_File_) :
    """Model a Unix style mailbox"""

    MB_Type = Lib.mailbox.UnixMailbox

# end class Unix_Mailbox

class MH_Mailbox (_Mailbox_in_Dir_) :
    """Model a MH style mailbox"""

    MB_Type = Lib.mailbox.MHMailbox

# end class MH_Mailbox

class Maildir (_Mailbox_in_Dir_) :
    """Model a Maildir style mailbox"""

    MB_Type = Lib.mailbox.Maildir

    def _subdirs (self, path) :
        try :
            return subdirs (sos.path.join (path, "sub"))
        except OSError :
            return []
    # end def _subdirs

# end class Maildir

"""
from   _TFL                    import TFL
import _TFL._PMA.Mailbox
mb=TFL.PMA.Maildir ("/swing/private/.Tanzer/Maildir")
mb=TFL.PMA.MH_Mailbox ("/swing/private/tanzer/MH/CT")
mb=TFL.PMA.MH_Mailbox ("/swing/private/tanzer/MH/inbox")
print mb.summary ().encode ("iso-8859-1", "ignore")
m = mb.messages [-3]
m = mb.messages [62]
print u"\n".join (m.formatted()).encode ("iso-8859-1", "ignore")
"""

if __name__ != "__main__" :
    TFL.PMA._Export ("*")
### __END__ Mailbox
