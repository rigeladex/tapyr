# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2010 Mag. Christian Tanzer. All rights reserved
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
#    PMA.Sender
#
# Purpose
#    Support sending of emails via SMTP
#
# Revision Dates
#    28-Jul-2005 (CT) Creation (factored from Composer.py)
#    19-Feb-2010 (CT) `TFL.SMTP` factored
#    27-Dec-2010 (CT) `** kw` added to `__init__`
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA

import _TFL._Meta.Object
import _TFL.SMTP

class Sender (TFL.Meta.Object) :
    """Send emails via SMTP"""

    def __init__ (self, mail_host = None, ** kw) :
        self.smtp = TFL.SMTP (mail_host = mail_host, ** kw)
    # end def __init__

    def __call__ (self, email, envelope = None) :
        self.smtp.send_message (email, envelope)
    # end def __call__

    def send (self, from_addr, to_addrs, msg, mail_opts = None, rcpt_opts = None) :
        self.smtp.send (from_addr, to_addrs, msg, mail_opts, rcpt_opts)
    # end def send

# end class Sender

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Sender
