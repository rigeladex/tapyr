# -*- coding: utf-8 -*-
# Copyright (C) 2005-2020 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
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
#     2-Apr-2015 (CT) Add `Sender_Logger`, `Sender_Tester`
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA

import _TFL._Meta.Object
import _TFL.SMTP

class Sender (TFL.Meta.Object) :
    """Send emails via SMTP"""

    SMTP = TFL.SMTP

    def __init__ (self, mail_host = None, ** kw) :
        self.smtp = self.SMTP (mail_host = mail_host, ** kw)
    # end def __init__

    def __call__ (self, email, envelope = None) :
        self.smtp.send_message (email, envelope)
    # end def __call__

    def send (self, from_addr, to_addrs, msg, mail_opts = None, rcpt_opts = None) :
        self.smtp.send (from_addr, to_addrs, msg, mail_opts, rcpt_opts)
    # end def send

# end class Sender

class Sender_Logger (Sender) :

    SMTP = TFL.SMTP_Logger

# end class Sender_Logger

class Sender_Tester (Sender) :

    SMTP = TFL.SMTP_Tester

# end class Sender_Tester

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Sender
