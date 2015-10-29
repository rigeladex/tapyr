# -*- coding: utf-8 -*-
# Copyright (C) 2005-2015 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    17-Mar-2014 (CT) Add `addressee` to `forward_format`, `resend_format`
#     2-Apr-2015 (CT) Use `bcc_addr`, not `email_address`, for `Bcc`
#    29-Oct-2015 (CT) Improve Python 3 compatibility
#    ««revision-date»»···
#--

from   _PMA                    import PMA
import _PMA.Composer
import _PMA.Matcher
import _PMA.Mime
import _PMA.Office
import _PMA.Sender

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
      , """Bcc:         %(bcc_addr)s"""
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
      , """To:          %(addressee)s"""
      , """Subject:     FW: %(subject)s"""
      , """Bcc:         %(bcc_addr)s"""
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
      , """Bcc:         %(bcc_addr)s"""
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
      , """To:          %(addressee)s"""
      , """««mail-cc»»"""
      , """««mail-bcc»»"""
      )
    )

PMA.Mime.default_type         = "application/octet-stream"
PMA.Mime.unencoded_mime_types = ("text/plain", "message/rfc822")
PMA.Mime.add_extensions         ("text/plain", None, ".sh", ".sty")

PMA.Office.top_name           = "PMA"

### __END__ PMA.Config_LSE
