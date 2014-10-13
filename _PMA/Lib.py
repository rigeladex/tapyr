# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    ««revision-date»»···
#--

from   _PMA                    import PMA

from   email.Utils             import *
from   email                   import message_from_string, message_from_file
try :
    mktime_tz
except NameError :
    from   email.encoders          import encode_base64
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
else : ### email 3.0 module names
    from   email.Encoders          import encode_base64
    from   email.Generator         import *
    from   email.Header            import *
    from   email.Message           import *
    from   email.MIMEAudio         import MIMEAudio
    from   email.MIMEBase          import MIMEBase
    from   email.MIMEImage         import MIMEImage
    from   email.MIMEMessage       import MIMEMessage
    from   email.MIMEMultipart     import MIMEMultipart
    from   email.MIMENonMultipart  import MIMENonMultipart
    from   email.MIMEText          import MIMEText
    from   email.Parser            import *
    from   email.Utils             import *

import mailbox
import mailcap

if __name__ != "__main__" :
    PMA._Export_Module ()
### __END__ PMA.Lib
