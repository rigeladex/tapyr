# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
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
#    Message
#
# Purpose
#    Model a mail message
#
# Revision Dates
#     3-Sep-2004 (CT) Creation
#     4-Sep-2004 (CT) Creation continued
#     6-Sep-2004 (CT) `Ascii.sanitized_filename` used in `_filename`
#    12-Sep-2004 (CT) s/ignore/replace/ in `decode` calls
#    12-Sep-2004 (CT) `_decoded_header` simplified and made more robust by
#                     passing `replace` to `decode`
#    12-Sep-2004 (CT) Exception handler added to `Message.summary` to avoid
#                     spam mails to raise `LookupError` on `decode`
#    12-Sep-2004 (CT) Exception handler added to `Message._time`
#                     (Man, do I hate spammers)
#    15-Sep-2004 (CT) Creation continued....
#    17-Nov-2004 (CT) `main` added
#    26-Nov-2004 (CT) `_formatted_body` changed to apply `.rstrip ("\r")` to
#                     each line yielded
#    26-Nov-2004 (CT) `message_from_file` factored
#    30-Nov-2004 (CT) `Message._get_header` robustified
#     3-Jan-2005 (CT) `_Message_._setup_body` robustified
#     4-Jan-2005 (CT) `Msg_Status` used
#     6-Jan-2005 (CT) `all_parts` added
#     6-Jan-2005 (CT) `formatted` changed to only `show_sep` if there is more
#                     than one part
#     6-Jan-2005 (CT) Argument `show_sep` added to `_formatted_part`
#     6-Jan-2005 (CT) `_setup_body` changed to handle `message/rfc822`
#                     correctly
#     6-Jan-2005 (CT) `Message.__init__` changed to pass `name` instead of
#                     `""` to `__super.__init__`
#     6-Jan-2005 (CT) `Message.__repr__` robustified
#    28-Mar-2005 (CT) `_formatted_body` changed to handle `text/x-*`
#                     mime-types better
#    28-Mar-2005 (CT) Redundant definition of `all_parts` removed from
#                     `Message`
#    28-Mar-2005 (CT) `_Msg_Part_` factored and `part_iter` added
#    29-Mar-2005 (CT) `formatted` changed to use `part_iter`
#    31-Mar-2005 (CT) `__str__` and `__repr__` factored up into `_Msg_Part_`
#    31-Mar-2005 (CT) `Body_Part` changed to use a `name` passed by caller
#                     and map `type` to `content_type` as supplied by `email`
#    31-Mar-2005 (CT) `Header_Part` changed to use `X-PMA-Headers` as `type`
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _PMA.Mailcap
import _PMA.Msg_Status
import _TFL.Ascii
import _TFL.Filename
import _TFL._Meta.M_Class
import _TFL._Meta.Property

from   _TFL.predicate          import dict_from_list
from   _TFL.Regexp             import *

import sos
import time

_ws_pat = Regexp    (r"\s+")
now     = time.time ()

class _Msg_Part_ (object) :

    __metaclass__    = TFL.Meta.M_Class_SWRP

    __properties     = \
        ( TFL.Meta.Lazy_Property ("charset",  lambda s : s._charset  ())
        , TFL.Meta.Lazy_Property
            ("content_type", lambda s : s.email.get_content_type ())
        , TFL.Meta.Lazy_Property ("filename", lambda s : s._filename ())
        )

    label_width      = 8
    summary_format   = "%(name)-10s %(type)-20s %(filename)s"

    def __init__ (self, email, name) :
        self.email = email
        self.name  = name
        self.path  = None
        self.body  = None
        self.parts = []
        self._setup_body (email)
    # end def __init__

    def _charset (self) :
        email = self.email
        if email :
            result = email.get_charset ()
            if result is None :
                result = email.get_param ("charset", "us-ascii")
            return result
    # end def _charset

    def _decoded_header (self, header) :
        result = []
        if header :
            for p, c in Lib.decode_header (header) :
                result.append (p.decode (c or "us-ascii", "replace"))
        result = u" ".join (result)
        return result
    # end def _decoded_header

    def _filename (self) :
        email  = self.email
        if email :
            result = email.get_param \
                ("filename", header = "Content-Disposition")
            if not result :
                result = email.get_param ("name")
            if isinstance (result, tuple) :
                result = unicode (result [2], result [0] or "us-ascii")
            return TFL.Ascii.sanitized_filename (self._decoded_header (result))
    # end def _filename

    def _formatted_headers (self, headers = None) :
        email = self.email
        for n in (headers or self.headers_to_show) :
            n, h = self._get_header (email, n)
            if h :
                yield "%-*s: %s" % \
                    (self.label_width, n, self._decoded_header (h))
    # end def _formatted_headers

    def _get_header (self, email, name) :
        if isinstance (name, tuple) :
            for n in name :
                result = email [n]
                if result is not None :
                    name = n
                    break
            else :
                name = ""
        else :
            result = email [name]
        return name.capitalize (), result
    # end def _get_header

    def _temp_body (self) :
        result = TFL.Filename \
            ( sos.tempfile_name ()
            , (self.filename or "").encode ("us-ascii", "ignore")
            ).name
        f = open (result, "w")
        try :
            f.write (self.body)
        finally :
            f.close ()
        return result
    # end def _temp_body

    def __str__ (self) :
        return self.summary_format % dict \
            (name = self.name, type = self.type, filename = self.filename)
    # end def __str__

    def __repr__ (self) :
        return "%s %s : %s" % \
            (self.__class__.__name__, self.name, self.type)
    # end def __repr__

# end class _Msg_Part_

class _Pseudo_Part_ (_Msg_Part_) :

    type          = "text/plain"

    def part_iter (self) :
        for p in self.parts :
            yield p
    # end def part_iter

# end class _Pseudo_Part_

class Body_Part (_Pseudo_Part_) :
    """Model the body of an email as pseudo-part"""

    __properties  = \
        ( TFL.Meta.Lazy_Property ("type", lambda s : s.content_type)
        ,
        )

    def __init__ (self, email, name, needs_sep, headers_to_show) :
        self.needs_sep       = needs_sep
        self.headers_to_show = headers_to_show
        self.__super.__init__ (email, name)
    # end def __init__

    def body_lines (self, sep_length = 79) :
        lines = None
        if self.body :
            type = self.content_type
            if type == "text/plain" or type.startswith ("text/x-") :
                lines = self.body.split ("\n")
            else :
                cap = PMA.Mailcap [type]
                if cap :
                    lines = cap.as_text (self._temp_body ())
        if lines is not None :
            charset = self.charset
            for l in lines :
                yield l.decode (charset, "replace").rstrip ("\r")
        else :
            hp = Header_Part (self.email, self.headers_to_show)
            for l in hp.formatted (sep_length) :
                yield l
    # end def body_lines

    formatted = _formatted = body_lines

    def _separators (self, sep_length) :
        if self.needs_sep :
            for s in ("", "-" * sep_length, "") :
                yield s
    # end def _separators

    def _setup_body (self, email) :
        payload = email.get_payload (decode = True)
        if payload :
            self.body = payload.strip ()
            ### XXX put full-quotes-at-end into `self.parts [0]`
    # end def _setup_body

# end class Body_Part

class Header_Part (_Pseudo_Part_) :
    """Model the headers of an email as pseudo-part"""

    type          = "X-PMA-Headers"

    def __init__ (self, email, headers_to_show, is_leaf = False, name = None) :
        self.headers_to_show = headers_to_show
        self.is_leaf         = is_leaf
        self.__super.__init__ (email, name or "Headers")
    # end def __init__

    def body_lines (self, sep_length = 79) :
        return self._fh
    # end def body_lines

    formatted = _formatted = body_lines

    def _separators (self, sep_length) :
        return ()
    # end def _separators

    def _setup_body (self, email) :
        self._fh  = list (self._formatted_headers (self.headers_to_show))
        self.body = "\n".join (self._fh)
        if not self.is_leaf :
            hts        = dict_from_list (self.headers_to_show)
            hth        = [k for k in email.keys () if k not in hts]
            self.parts = [Header_Part (email, hth, True, "More headers")]
    # end def _setup_body

# end class Header_Part

class _Message_ (_Msg_Part_) :

    __properties  = \
        ( TFL.Meta.Lazy_Property ("type", lambda s : s.content_type)
        ,
        )

    def all_parts (self) :
        for p in self.parts :
            yield p
            for sp in p.all_parts () :
                yield sp
    # end def all_parts

    def body_lines (self, sep_length = 79) :
        return ()
    # end def body_lines

    def formatted (self, sep_length = 79) :
        for p in self.part_iter () :
            for l in p.formatted (sep_length) :
                yield l
    # end def formatted

    def part_iter (self) :
        email  = self.email
        is_msg = isinstance (self, Message)
        if is_msg :
            yield Header_Part (email, self.headers_to_show)
        if not email.is_multipart () :
            yield Body_Part \
                (email, self.name or "Body", is_msg, self.headers_to_show)
        else :
            if self.type == "multipart/alternative" :
                parts = self.parts [0:1] ### XXX return a MP_Alt_Part object
            else :
                parts = self.parts
            for p in parts :
                yield p
    # end def part_iter

    _formatted = formatted

    def _separators (self, sep_length) :
        yield ""
        yield ( "%s part %s %s" % ("-" * 4, self.name, "-" * sep_length)
              ) [:sep_length]
    # end def _separators

    def _setup_body (self, email) :
        name       = self.name
        self.parts = parts = []
        self.body  = None
        if email.is_multipart () :
            payload = email.get_payload ()
            if email.get_content_type () == "message/rfc822" :
                p, = payload
                parts.append (Message (p, name = name))
            else :
                i = 1
                for p in payload :
                    p_name = ".".join (filter (None, (name, str (i))))
                    parts.append (Message_Part (p, name = p_name))
                    i += 1
        else :
            payload = email.get_payload (decode = True)
            if payload :
                self.body = payload.strip ()
    # end def _setup_body

# end class _Message_

class Message_Part (_Message_) :
    """Model a part of a multi-part MIME message"""

    headers_to_show  = ("content-type", "content-disposition")

# end class Message_Part

class Message (_Message_) :
    """Model a mail message"""

    headers_to_show  = \
        ( ("date", "delivery-date")
        , ("from", "reply-to", "return-path")
        , ("to", "envelope-to")
        , "cc"
        , "subject"
        )
    summary_format   = unicode \
        ( "%(number)4s %(date)-12.12s %(sender)-20.20s %(subject)-25.25s "
          "[%(body)-50.50s"
        )

    date             = property (lambda s : s._date    ())
    sender           = property (lambda s : s._sender  ())
    time             = property (lambda s : s._time    ())

    def __init__ (self, email, name = None, mailbox = None, status = None, number = None) :
        if status is None :
            status = PMA.Msg_Status ()
        self.__super.__init__ (email, name)
        self.mailbox = mailbox
        self.status  = status
        self.number  = number
    # end def __init__

    def formatted (self, sep_length = 79) :
        self.status.set_read   ()
        for p in self.part_iter () :
            for s in p._separators (sep_length) :
                yield s
            for l in p._formatted  (sep_length) :
                yield l
    # end def formatted

    def part_iter (self) :
        email = self._reparsed ()
        for p in self.__super.part_iter () :
            yield p
    # end def part_iter

    def summary (self, format = None) :
        email = self.email
        if format is None :
            format = self.summary_format
        number     = self.number
        if number is None :
            number = u""
        date       = self.date or u""
        sender     = self._sender () or u""
        subject    = self._decoded_header (email ["subject"])
        _pl        = email
        while _pl.is_multipart () :
            _pl = _pl.get_payload (0)
        body = _pl.get_payload (decode = True) or u""
        if isinstance (body, str) :
            try :
                body = body.decode (self.charset, "replace")
                   ### XXX some emails trigger
                   ### `UnicodeDecodeError: 'ascii' codec can't decode
                   ### byte 0xe4` without `replace` argument
            except LookupError :
                body = body.decode ("us-ascii", "replace")
        body = _ws_pat.sub (u" ", body.strip ()) or u"<empty>"
        return format % locals ()
    # end def summary

    def _date (self, treshold = 86400 * 270) :
        t = self.time
        if t :
            if now - t > treshold :
                format = "%d-%b  %Y"
            else :
                format = "%d-%b %H:%M"
            return time.strftime (format, time.localtime (t))
    # end def _date

    def _reparsed (self) :
        result = self.email
        if self.path and not result._pma_parsed_body :
            if self.mailbox :
                parser = self.mailbox.parser.parse
            else :
                parser = Lib.message_from_file
            fp = open (self.path, "r")
            try :
                result = self.email = parser (fp)
            finally :
                fp.close ()
            result._pma_dir         = getattr (self.email, "_pma_dir",  None)
            result._pma_path        = getattr (self.email, "_pma_path", None)
            result._pma_parsed_body = True
            self._setup_body (result)
        return result
    # end def _reparsed

    def _sender (self) :
        email  = self.email
        sender = \
            (  email ["from"]
            or email ["reply-to"]
            or email ["return-path"]
            or email.get_unixfrom ()
            )
        if sender :
            sender = \
                (  filter (None, Lib.getaddresses ((sender, )) [0])
                or (None, )
                ) [0]
            return self._decoded_header (sender)
    # end def _sender

    def _time (self) :
        email = self.email
        for date in email ["date"], email ["delivery-date"] :
            if date :
                parsed = Lib.parsedate_tz (date)
                if parsed is not None :
                    try :
                        return Lib.mktime_tz (parsed)
                    except (OverflowError, ValueError) :
                        pass
    # end def _time

    def __str__ (self) :
        return self.summary ()
    # end def __str__

    def __repr__ (self) :
        if self.mailbox :
            result = "%s %s:%s" % \
                (self.__class__.__name__, self.mailbox.path, self.name)
        else :
            result = "%s %s" % (self.__class__.__name__, self.name)
        return result
    # end def __repr__

# end class Message

def message_from_file (filename, parser = None) :
    if parser is None :
        parser = Lib.Parser ()
    fp = open (filename)
    try :
        email = parser.parse (fp)
    finally :
        fp.close ()
    return Message (email, sos.path.split (filename) [-1])
# end def message_from_file

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line
    return Command_Line \
        ( arg_spec    = ("message:S?Message to print")
        , option_spec =
            (
            )
        , description = "Print mail messages"
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    parser = Lib.Parser ()
    for m in cmd.argv :
        msg = message_from_file (m, parser)
        print u"\n".join (msg.formatted ()).encode ("iso-8859-15", "replace")
# end def main

"""
from   _PMA                    import PMA
import _PMA.Mailbox
mb=PMA.MH_Mailbox ("/swing/private/tanzer/MH/inbox")
print mb.summary ().encode ("iso-8859-1", "replace")
m = mb.messages [-1]
m._reparsed ()
for p in m.all_parts () :
  print type (p), p.name

"""

if __name__ != "__main__" :
    PMA._Export ("*")
else :
    main (command_spec ())
### __END__ PMA.Message
