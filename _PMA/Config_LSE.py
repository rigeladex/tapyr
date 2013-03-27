# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005-2013 Mag. Christian Tanzer. All rights reserved
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
#    PMA.Config_LSE
#
# Purpose
#    Default config for use of LS-Emacs
#
# Revision Dates
#    17-Aug-2005 (CT) Creation (factored from `~tanzer/PMA/.config.py`)
#    27-Mar-2013 (CT) Add `%(receiver)s`, `%(subject)s`, `formatted_replacers`
#    ««revision-date»»···
#--

from   _PMA                    import PMA
import _PMA.Composer
import _PMA.Mime
import _PMA.Office
import _PMA.Sender
import _PMA._UI.Application

from   _TFL.Regexp             import *

PMA.Composer.editor           = "emacsclient --alternate-editor vi"

PMA.Composer.formatted_replacers.add \
    ( Re_Replacer
        ( u"""^Subject: *$"""
        , u"""Subject:     «text»"""
        , re.IGNORECASE | re.MULTILINE
        )
    , Re_Replacer
        ( u"""^To: *$"""
        , u"""To:          «text»"""
        , re.IGNORECASE | re.MULTILINE
        )
    )

PMA.Composer.compose_format   = "\n".join \
    ( ( """From:        %(email_address)s"""
      , """To:          %(receiver)s"""
      , """Subject:     %(subject)s"""
      , """Bcc:         %(email_address)s"""
      , """Reply-to:    %(email_address)s"""
      , """X-mailer:    PMA %(version)s"""
      , """««mail-cc»»"""
      , """««mail-bcc»»"""
      , """%(body_marker)s"""
      , ""
      , """««text»»"""
      , ""
      )
    )

PMA.Composer.forward_format   = "\n".join \
    ( ( """From:        %(email_address)s"""
      , """To:          %(receiver)s"""
      , """Subject:     FW: %(subject)s"""
      , """Bcc:         %(email_address)s"""
      , """X-mailer:    PMA %(version)s"""
      , """««mail-cc»»"""
      , """««mail-bcc»»"""
      , """%(body_marker)s"""
      , ""
      , """see attached mail"""
      , """««text»»"""
      , ""
      )
    )

PMA.Composer.reply_format     = "\n".join \
    ( ( """From:        %(email_address)s"""
      , """To:          %(reply_address)s"""
      , """Subject:     Re: %(subject)s"""
      , """Bcc:         %(email_address)s"""
      , """X-mailer:    PMA %(version)s"""
      , """««mail-cc»»"""
      , """««mail-bcc»»"""
      , """In-reply-to: Your message of "%(message_date)s" """
      , """             %(message_id)s"""
      , """References:  %(message_id)s"""
      , """Reply-to:    %(email_address)s"""
      , """%(body_marker)s"""
      , """««text»»%(sender_name)s wrote at %(message_date)s:"""
      , ""
      , """««text»»"""
      , ""
      )
    )

PMA.Composer.reply_all_format = "\n".join \
        ( ( """Cc:          %(reply_address_cc)s"""
          , PMA.Composer.reply_format
          )
        )

PMA.Composer.resend_format    = "\n".join \
    ( ( """From:        %(email_address)s"""
      , """To:          %(receiver)s"""
      , """««mail-cc»»"""
      , """««mail-bcc»»"""
      )
    )

PMA.Mime.default_type         = "application/octet-stream"
PMA.Mime.unencoded_mime_types = ("text/plain", "message/rfc822")
PMA.Mime.add_extensions         ("text/plain", None, ".sh", ".sty")

PMA.Office.top_name           = "PMA"

### __END__ PMA.Config_LSE
