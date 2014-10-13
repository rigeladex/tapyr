# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    PMA.SCM.Mailbox
#
# Purpose
#    Change tracker objects for PMA Mailbox objects
#
# Revision Dates
#    15-Jan-2006 (MG) Creation
#    23-Jan-2006 (MG) `Add_Filter_Subbox` added
#    26-Jan-2006 (MG) `_Messages_.__init__` allow strings and message objects
#    26-Jan-2006 (MG) `Remove_Messages` fixed
#    26-Jan-2006 (MG) `messages_from_box` factored
#    ««revision-date»»···
#--

from   _PMA              import PMA
from   _TFL              import TFL
import _TFL._Meta.Object

import _PMA._SCM

class _Messages_ (TFL.Meta.Object) :
    """Root class for all message based change objects"""

    def __init__ (self, * messages) :
        self.messages = [getattr (m, "name", m) for m in messages]
    # end def __init__

    def messages_from_box (self, mailbox) :
        return (mailbox._msg_dict [n] for n in self.messages)
    # end def messages_from_box

    def __repr__ (self) :
        return "%s (%r)" % (self.__class__.__name__, self.messages)
    # end def __repr__

# end class _Messages_

class _Subbox_ (TFL.Meta.Object) :
    """Root class for subbox based change objects"""

    def __init__ (self, subbox) :
        self.subbox = subbox.qname
    # end def __init__

    def __repr__ (self) :
        return "%s (%r)" % (self.__class__.__name__, self.subbox)
    # end def __repr__

# end class _Subbox_

class Remove_Messages (_Messages_) :
    """Remove a set of messages from a mailbox"""

    def __call__ (self, target, source) :
        target.remove_msg (* self.messages)
    # end def __call__

# end class Remove_Messages

class Add_Messages (_Messages_) :
    """Add a set of messages to a mailbox"""

    def __call__ (self, target, source) :
        result = target.add_messages (* self.messages_from_box (source))
        if target._messages is None :
            target._messages = target._msg_dict.values ()
            target._sort ()
        return result
    # end def __call__

# end class Add_Messages

class Change_Messages (_Messages_) :
    """Messages for which the status has changed."""

# end class Change_Messages

class Add_Subbox (_Subbox_) :
    """This subbox has been added"""

# end class Add_Subbox

class Add_Filter_Subbox (Add_Subbox) :
    """This filter subbox has been added."""

    def __init__ (self, subbox) :
        self.__super.__init__ (subbox)
        ### XXX how to save the matcher ?
        return
        self.condition = subbox._matcher.condition
        self.ckw       = subbox._matcher.ckw
    # end def __init__

# end class Add_Filter_Subbox

class Remove_Subbox (_Subbox_) :
    """This subbox has been removed"""

# end class Remove_Subbox

if __name__ != "__main__" :
    PMA.SCM._Export ("*")
### __END__ PMA.SCM.Mailbox
