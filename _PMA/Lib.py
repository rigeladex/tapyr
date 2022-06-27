# -*- coding: utf-8 -*-
# Copyright (C) 2004-2020 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    PMA.Lib
#
# Purpose
#    Encapsulate classes/functions from standard Python library for use by PMA
#
# Revision Dates
#    31-Aug-2004 (CT) Creation
#     3-Sep-2004 (CT) Creation continued
#    28-Jul-2005 (CT) `encode_base64` added
#    11-Apr-2008 (CT) Exception handler added to make import version specific
#                     (in Python 2.5.2, the import of old-style names fails
#                     to import `mktime_tz` from `Utils`; arrrg)
#    20-Apr-2008 (CT) Imports changed so that it really works for 2.5.2 and 2.4
#    29-Oct-2015 (CT) Simplify imports
#                     * Python 2.7 *and* 3.5 use lowercase module names
#    29-Oct-2015 (CT) Add `UnixMailbox`, `MHMailbox` aliase for Python 3.x
#     4-Nov-2015 (CT) Add `encode_7or8bit`, remove `message_from_string`
#    25-Mar-2020 (CT) Add `policy`
#    ««revision-date»»···
#--

from   _PMA                    import PMA

from   email                   import message_from_file, policy
from   email.encoders          import encode_base64, encode_7or8bit
from   email.generator         import *
from   email.header            import *
from   email.message           import *
from   email.mime.audio        import MIMEAudio
from   email.mime.base         import MIMEBase
from   email.mime.image        import MIMEImage
from   email.mime.message      import MIMEMessage
from   email.mime.multipart    import MIMEMultipart
from   email.mime.nonmultipart import MIMENonMultipart
from   email.mime.text         import MIMEText
from   email.parser            import *
from   email.utils             import *
from   email.utils             import mktime_tz

import mailbox
import mailcap

try :
    mailbox.UnixMailbox
except AttributeError :
    mailbox.UnixMailbox = mailbox.mbox

try :
    mailbox.MHMailbox
except AttributeError :
    mailbox.MHMailbox = mailbox.MH

if __name__ != "__main__" :
    PMA._Export_Module ()
### __END__ PMA.Lib
