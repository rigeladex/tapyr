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
#    PMA.Message
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
#    18-May-2005 (CT) s/Header_Part/Message_Header/
#    18-May-2005 (CT) s/Body_Part/Message_Body/
#    18-May-2005 (CT) `_setup_body` changed to but `Message_Body` into `parts`
#    18-May-2005 (CT) `_formatted_headers` changed to yield `name` and
#                     formatted header line
#    18-May-2005 (CT) `more_body_lines` added to `Message_Header` and
#                     separate `Message_Header` instance for `more headers`
#                     removed
#    18-May-2005 (CT) `email_summary` (and `_date`, `_sender`, and `_time`)
#                     factored up
#    18-May-2005 (CT) `Part_Header` factored
#    19-May-2005 (CT) s/_charset/_get_charset/
#    19-May-2005 (CT) `_get_content_type` added and redefined for
#                     `Message_Body` to deal with broken `content-type`
#    19-May-2005 (CT) `part_iter` refactored (got rid of `if isinstance` and
#                     `_Pseudo_Part_`)
#    19-May-2005 (CT) Result of `_temp_body` cached
#    19-May-2005 (CT) `Message_MPA` added and `_Message_._setup_body` changed
#                     to call it for "multipart/alternative"
#    19-May-2005 (CT) `all_parts` removed
#    19-May-2005 (CT) Property for `subject` added
#    20-May-2005 (MG) Property `subject` fixed
#    22-May-2005 (CT) `save` (and `_save`) added
#    22-May-2005 (CT) `_reparsed` changed to use `PMA.Sb` if available
#    22-May-2005 (CT) s/_get_header/_get_headers/ (and changed to return all
#                     headers)
#    22-May-2005 (CT) `pending` and `_Pending_Action_` added
#    23-May-2005 (CT) `_Pending_Action_` changed to treat `move` as another
#                     `copy` if there is more than one `_targets` already
#                     (instead of forbidding that)
#    25-May-2005 (CT) Bug fix `self.status` initialization
#    26-Jul-2005 (CT) `Msg_Scope` added and used
#    27-Jul-2005 (CT) `Msg_Scope.__getitem__` improved
#    29-Jul-2005 (CT) `main` and `command_spec` renamed to `_main` and
#                     `_command_spec` to avoid name clashes in PMA namespace
#    29-Jul-2005 (CT) `_Message_._decoded_header` moved to module-level
#                     `decoded_header`
#    29-Jul-2005 (CT) `Msg_Scope` changed to use `decoded_header`
#    29-Jul-2005 (MG) `_Pending_Action_.__nonzero__` fixed (must return bool,
#                     not dict)
#    30-Jul-2005 (MG) `_Pending_Action_`: Properties `copyied`, "deleted",
#                     and `moved` added
#    30-Jul-2005 (MG) `_Pending_Action_.commit`: retur all mailboxes which
#                     have been changed
#    30-Jul-2005 (MG) s/_reset/reset/g
#    30-Jul-2005 (MG) `_Pending_Action_.__len__` added
#     1-Aug-2005 (MG) `message_from_string` added
#     9-Aug-2005 (CT) Use of `PMA.default_charset` increased
#     9-Aug-2005 (CT) Use `PMA.file_system_encoding` instead of `us-ascii`
#     9-Aug-2005 (CT) s/default_charset/default_encoding/g
#    16-Aug-2005 (CT) `Msg_Scope._get_header_` factored
#    16-Aug-2005 (CT) `Msg_Scope._get_sender_name` added
#    31-Aug-2005 (CT) `body_lines` changed back to using `self.charset`
#                     instead of `PMA.default_encoding` for `decode`
#    13-Sep-2005 (CT) `Msg_Scope._get_body` factored from
#                     `_Msg_Part_.email_summary`
#    14-Sep-2005 (CT) `kw` added to `Msg_Scope.__init__`
#    14-Sep-2005 (CT) Always pass `Msg_Scope` to `%` applied to
#                     `summary_format` and `short_summary_format`
#    14-Sep-2005 (CT) `Message.sender` and `_Msg_Part_._sender` removed (use
#                     `Msg_Scope ["sender"]` instead)
#    14-Sep-2005 (CT) `Message.date` and _Msg_Part_._date removed (use
#                     `Msg_Scope ["date"]` instead)
#    14-Sep-2005 (CT) `_get_header_` moved back to `_Msg_Part_`
#    15-Sep-2005 (CT) `Msg_Scope._get_attr_` factored and
#                     `Msg_Scope.__getattr__` added
#    15-Sep-2005 (MG) `Msg_Scope.__init__`: only assign `u""` to number if
#                     `msg.number` is None (and not `0`)
#    16-Sep-2005 (CT) `Msg_Scope._get_attr_` changed to delegate to `msg`
#                     (and caching of `msg` attributes removed from `__init__`)
#    16-Sep-2005 (CT) `_Msg_Part_.scope` added as `Lazy_Property`
#    17-Sep-2005 (CT) `% Msg_Scope (self)` replaced by `% self.scope`
#    28-Dec-2005 (MG) `Msg_Scope._get_attr_` catch `KeyError` as well
#    29-Dec-2005 (CT) `Msg_Scope._get_sender_` factored
#    29-Dec-2005 (CT) `Msg_Scope._get_sender_addr` added
#    29-Dec-2005 (CT) `list_id`, `sb_vote`, `spam_flag` added to `_header_map`
#    29-Dec-2005 (CT) `Msg_Scope._get_sb_score`, `._get_is_spam`, and
#                     `._get_maybe_spam` added
#     2-Jan-2006 (CT) `_get_sender_` and `_get_sender_name` fixed
#     2-Jan-2006 (CT) `_reparsed` changed to use `mailbox.reparsed`
#     2-Jan-2006 (CT) `SB.filter` removed from `_reparsed` (let that be done
#                     by POP3_Mailbox, procmail, etc.)
#     3-Jan-2006 (CT) `body_start` implemented
#     3-Jan-2006 (CT) `_Pending_Action_` changed to support errors during
#                     `commit` of a `delete` gracefully
#     4-Jan-2006 (CT) `reset` re-refactored
#     4-Jan-2006 (CT) `_Msg_Part_._save` refactored to module-level function
#                     `save`
#     5-Jan-2006 (CT) SB-related commands added
#    25-Jan-2006 (CT) `body_lines` changed (again!) to using `self.charset`
#                     *or* `PMA.default_encoding` for `decode`
#     9-Jul-2007 (CT) `body_lines` changed to use `textwrap.Wrapper` to split
#                     overlong lines
#     7-Nov-2007 (CT) Use `Getter` instead of `lambda`
#    24-Feb-2009 (CT) `Message_Body.body_lines` changed to not gobble empty
#                     lines (`textwrap.TextWrapper` is broken in that regard)
#    19-Mar-2009 (CT) Use `with open_tempfile` instead of `sos.tempfile_name`
#    31-Mar-2009 (CT) `_get_sender_name` robustified
#    16-Apr-2009 (CT) `_get_charset` guarded against unknown `charset`
#     8-Jun-2009 (CT) Use `with` instead of `try..finally` for opening files
#    28-Mar-2013 (CT) Add `defaults` to `Msg_Scope`,
#                     allow `msg=None` in `Msg_Scope`
#    16-Jun-2013 (CT) Use `TFL.CAO`, not `TFL.Command_Line`
#     8-Sep-2013 (CT) Change `decoded_header` to allow `unknown`
#                     (shame on: Oracle Communications Messaging Server)
#    18-Dec-2013 (CT) Add options `-msg_base_dirs` and `-Print`
#    21-Dec-2013 (CT) Fix assignment of `encoding`
#    21-Dec-2013 (CT) Add option `-body_only`
#    23-Dec-2013 (CT) Factor `messages_from_args` and `formatted`
#    23-Jan-2014 (CT) Set `PMA.default_encoding` in all cases in `_main`
#    17-Mar-2014 (CT) Fix error message `tail` in `messages_from_args`
#    22-Apr-2014 (CT) Change `_main` to pass `encoding` to `formatted`
#     5-Jun-2014 (CT) Use `Once_Property`, not `Lazy_Property`; use
#                     `M_Class`, not `M_Class_SWRP`, as metaclass
#     8-Oct-2015 (CT) Change `__getattr__` to *not* handle `__XXX__`
#    29-Oct-2015 (CT) Improve Python 3 compatibility
#     4-Nov-2015 (CT) Use mode "rb" for message files
#     4-Nov-2015 (CT) Remove `message_from_string` because broken Python 3
#     9-Nov-2015 (CT) Change `body_lines` to call `pyk.decoded` before `.split`
#    23-Feb-2016 (CT) Change `_main` to encode `subject` after `%`, not before
#    27-Dec-2016 (CT) Change `body_lines` to pass `encoding` to `as_text`
#    17-Jul-2018 (CT) Fix Python 3 encoding issues
#                     + Open files in text, not binary mode
#                     + Use `pyk.fprint`, not `print`, for `text`, not `bytes`
#    19-Aug-2019 (CT) Make `_Msg_Part_._temp_body` Python 3 compatible
#                     + Don't `encode` argument to `Filename`
#                     + Open temp-file as binary, not text
#    19-Aug-2019 (CT) Add `main_type`, `sub_type`
#    19-Aug-2019 (CT) Add `PMA.msg_base_dirs`
#    12-Dec-2019 (CT) Use mode `wb` for `open_tempfile` (Py3 compatibility)
#    13-Dec-2019 (CT) Use `LNX.text_to_postscript._header_encode_rep`
#                     * `a2ps` coughs on Unicode
#     2-Jun-2020 (CT) Use `TFL.text_to_pdf`, not `LNX.text_to_postscript`
#                     + Add `Msg_Scope.full_date`
#    24-Jun-2020 (CT) Add `-Cutable` to options for `text_to_pdf`
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _PMA.Mailcap
import _PMA.Msg_Status
import _PMA.SB

from   _TFL.predicate          import callable, filtered_join, first, split_hst
from   _TFL.pyk                import pyk
from   _TFL.Regexp             import *
from   _TFL                    import sos

import _TFL.Accessor
import _TFL.Ascii
import _TFL.Caller
import _TFL.CAO
import _TFL.FCM
import _TFL.Filename
import _TFL._Meta.M_Class
import _TFL._Meta.Property

import sys
import textwrap
import time
import weakref

_ws_pat = Regexp    (r"\s+")
now     = time.time ()

def decoded_header (header) :
    result = []
    if header :
        for p, c in Lib.decode_header (header) :
            enc = c or PMA.default_encoding
            if enc == "unknown" :
                enc = PMA.default_encoding
            result.append (pyk.decoded (p, enc))
    result = " ".join (result)
    return result
# end def decoded_header

def save (filename, body) :
    if body :
        with open (filename, "wb") as f :
            f.write (pyk.encoded (body, PMA.default_encoding))
# end def save

class Msg_Scope (TFL.Caller.Scope) :
    """Provide access to the caller's locals and to the message object passed
       in.
    """

    class Lookup_Error (Exception) : pass

    _defaults = None

    def __init__ (self, msg, locls = None, defaults = None, ** kw) :
        self.msg = msg
        if defaults :
            self._defaults = TFL.Caller.Scope (0, defaults, {})
        self.__super.__init__ (depth = 1, locls = locls, ** kw)
    # end def __init__

    def _get_attr_ (self, name) :
        try :
            return self.__super.__getitem__ (name)
        except (NameError, KeyError) :
            if self.msg is not None :
                key    = name.lower ()
                getter = getattr (self.__class__, "_get_%s" % key, None)
                if callable (getter) :
                    return getter (self)
                else :
                    result = self.msg._get_header_ (key, name)
                    if result is not None :
                        return decoded_header (result)
                result = getattr (self.msg, name, None)
                if result is not None :
                    return result
            if self._defaults :
                try :
                    return self._defaults [name]
                except (NameError, KeyError) :
                    pass
            raise self.Lookup_Error (name)
    # end def _get_attr_

    def _get_body (self) :
        _pl = self.msg.email
        while _pl.is_multipart () :
            _pl = _pl.get_payload (0)
        result  = _pl.get_payload (decode = True) or ""
        result  = pyk.decoded (result, self.msg.charset)
        result  = _ws_pat.sub (" ", result.strip ()) or "<empty>"
        return result
    # end def _get_body

    def _get_date (self, treshold = 86400 * 270) :
        t = self.msg._time ()
        if t :
            if now - t > treshold :
                format = "%d-%b  %Y"
            else :
                format = "%d-%b %H:%M"
            return time.strftime (format, time.localtime (t))
    # end def _get_date

    def _get_full_date (self) :
        t = self.msg._time ()
        if t :
            return time.strftime ("%Y-%m-%d %H:%M", time.localtime (t))
    # end def _get_full_date

    def _get_is_spam (self) :
        msg    = self.msg
        result = ""
        flag   = msg._get_header_ ("spam_flag", "")
        if flag and flag.lower () == "yes" :
            result = "yes"
        else :
            sb_score = self._get_sb_score ()
            if sb_score and float (sb_score) > 0.75 :
                result = "yes"
        return result
    # end def _get_is_spam

    def _get_maybe_spam (self) :
        msg    = self.msg
        result = ""
        flag   = msg._get_header_ ("spam_flag", "")
        if flag and flag.lower () not in ("no", "yes") :
            result = "yes"
        else :
            sb_score = self._get_sb_score ()
            if sb_score and 0.20 < float (sb_score) <= 0.75 :
                result = "yes"
        return result
    # end def _get_maybe_spam

    def _get_reply_address_cc (self) :
        email  = self.msg.email
        result = []
        for key in "to", "cc" :
            result.extend (decoded_header (r) for r in email.get_all (key, []))
        return ", \n             ".join (r for r in result if r)
    # end def _get_reply_address_cc

    def _get_sb_score (self) :
        sb_vote = self.msg._get_header_ ("sb_vote", "")
        if sb_vote :
            i, w = [x.strip () for x in sb_vote.split (";")]
            return w
        return ""
    # end def _get_sb_score

    def _get_sender_ (self) :
        msg    = self.msg
        result = (None, None)
        sender = msg._get_header_ ("sender", "Sender")
        if sender is None :
            sender = msg.email.get_unixfrom ()
        if sender is not None :
            result = Lib.getaddresses ((sender, )) [0] or result
        return result
    # end def _get_sender_

    def _get_sender_addr (self) :
        result = self._get_sender_ () [1]
        if result is not None :
            return result
        return ""
    # end def _get_sender_addr

    def _get_sender_name (self) :
        try :
            result = first (s for s in self._get_sender_ () if s)
        except IndexError :
            result = None
        if result is not None :
            return decoded_header (result)
        return ""
    # end def _get_sender_name

    def __getattr__ (self, name) :
        if name.startswith ("__") and name.endswith ("__") :
            ### Placate inspect.unwrap of Python 3.5,
            ### which accesses `__wrapped__` and eventually throws `ValueError`
            return getattr (self.__super, name)
        try :
            return self._get_attr_ (name)
        except self.Lookup_Error :
            raise AttributeError (name)
    # end def __getattr__

    def __getitem__ (self, index) :
        try :
            return self._get_attr_ (index)
        except self.Lookup_Error :
            return ""
    # end def __getitem__

# end class Msg_Scope

class _Msg_Part_ (TFL.Meta.Object) :

    label_width         = 8
    number              = None
    summary_format      = "%(name)-10s %(type)-20s %(filename)s"
    _charset            = None
    _tfn                = None

    _header_map         = dict \
        ( delivery_date = ("Delivery-date")
        , in_reply_to   = ("In-reply-to", )
        , list_id       = ("List-id", )
        , message_date  = ("Date", "Delivery-date")
        , message_id    = ("Message-id", "References")
        , receiver      = ("to", "envelope-to")
        , reply_address =
            ( "Mail-followup-to"
            , "X-mailing-list"
            , "Reply-To"
            , "From"
            , "Sender"
            , "Return-path"
            )
        , sender        = ("From", "Reply-To", "Sender", "Return-path")
        , sb_vote       = ("X-spambayes-classification", )
        , spam_flag     = ("X-spam-flag", )
        )

    def __init__ (self, email, name) :
        self.email = email
        self.name  = name
        self.path  = None
        self.body  = None
        self.parts = []
        self._setup_body (email)
    # end def __init__

    @TFL.Meta.Once_Property
    def charset (self) :
        result = self._charset
        if result is None :
            email = self.email
            if email :
                result = email.get_charset ()
                if result is None :
                    result = email.get_param ("charset", "us-ascii")
        try :
            "".encode (result, "replace")
        except LookupError :
            ### Guard against broken messages like::
            ###   Content-Type: text/plain; charset=unknown-8bit
            result = "us-ascii"
        return result
    # end def charset

    @TFL.Meta.Once_Property
    def content_type (self) :
        return self.email.get_content_type ().lower ()
    # end def content_type

    @TFL.Meta.Once_Property
    def filename (self) :
        email  = self.email
        if email :
            result = email.get_param \
                ("filename", header = "Content-Disposition")
            if not result :
                result = email.get_param ("name")
            if isinstance (result, tuple) :
                result = pyk.decoded (result [2], result [0] or "us-ascii")
            return TFL.Ascii.sanitized_filename (decoded_header (result))
    # end def filename

    @TFL.Meta.Once_Property
    def main_type (self) :
        return self.email.get_content_maintype ().lower ()
    # end def main_type

    @TFL.Meta.Once_Property
    def scope (self) :
        return Msg_Scope (self)
    # end def scope

    @TFL.Meta.Once_Property
    def subject (self) :
        return decoded_header (self.email ["subject"])
    # end def subject

    @TFL.Meta.Once_Property
    def sub_type (self) :
        return self.email.get_content_subtype ().lower ()
    # end def sub_type

    @TFL.Meta.Once_Property
    def type (self) :
        return self.content_type
    # end def type

    def email_summary (self, email, format = None) :
        if format is None :
            format = self.summary_format
        return format % self.scope
    # end def email_summary

    def part_iter (self) :
        yield from self.parts
    # end def part_iter

    def summary (self, summary_format = None) :
        if summary_format is None :
            summary_format = self.summary_format
        return summary_format % self.scope
    # end def summary

    def _formatted_headers (self, headers = None) :
        email = self.email
        for n in (headers or self.headers_to_show) :
            for n, h in self._get_headers (email, n) :
                yield n, "%-*s: %s" % \
                    (self.label_width, n, decoded_header (h))
    # end def _formatted_headers

    def _get_header_ (self, key, index) :
        email = self.email
        for n in self._header_map.get (key, (index, )) :
            try :
                result = email [n]
                if result is not None :
                    return result
            except KeyError :
                pass
    # end def _get_header_

    def _get_headers (self, email, name) :
        if isinstance (name, tuple) :
            for n in name :
                result = email.get_all (n, ())
                if result :
                    name = n
                    break
            else :
                name = ""
        else :
            result = email.get_all (name, ())
        name = name.capitalize ()
        for r in result :
            yield name, r
    # end def _get_headers

    def _separators (self, sep_length) :
        yield ""
        yield ( "%s part %s %s" % ("-" * 4, self.name, "-" * sep_length)
              ) [:sep_length]
    # end def _separators

    def _temp_body (self) :
        if self._tfn is None or not sos.path.isfile (self._tfn) :
            dir = TFL.Filename (self.filename or "").directory
            with TFL.open_tempfile ("wb", dir = dir, auto_remove = False) as \
                     (f, result) :
                f.write (self.body)
                self._tfn = result
        return self._tfn
    # end def _temp_body

    def _time (self) :
        date = self._get_header_ ("date", "Date")
        if date :
            parsed = Lib.parsedate_tz (date)
            if parsed is not None :
                try :
                    return Lib.mktime_tz (parsed)
                except (OverflowError, ValueError) :
                    pass
    # end def _time

    def __str__ (self) :
        return self.summary_format % self.scope
    # end def __str__

    def __repr__ (self) :
        return "%s %s : %s" % (self.__class__.__name__, self.name, self.type)
    # end def __repr__

# end class _Msg_Part_

class Message_Body (_Msg_Part_) :
    """Model the body of a (non multi-part) message or message-part"""

    _file_result_pattern = Regexp \
        ( r"[^:]+ \s* : \s* (?P<type> [^;]+) "
          r"(?: \s* ; \s* charset=(?P<charset> [-A-Za-z0-9]+))?"
        , re.VERBOSE
        )

    def __init__ (self, email, name, headers_to_show) :
        assert not email.is_multipart ()
        self.headers_to_show = headers_to_show
        self.lines           = None
        self.__super.__init__ (email, name)
    # end def __init__

    @TFL.Meta.Once_Property
    def content_type (self) :
        result = self.__super.content_type
        if result == "application/octet-stream" :
            pipe = sos.popen     ("file -i %s" % (self._temp_body (), ), "r")
            f_result = pipe.read ()
            pipe.close           ()
            pat = self._file_result_pattern
            if pat.match (f_result) :
                result = pat.type
                if pat.charset :
                    self._charset = pat.charset
        elif result == "application/python" :
            if self.filename.endswith (".py") :
                result = "text/x-python"
        return result
    # end def content_type

    def body_lines (self, sep_length = 79) :
        lines = self.lines
        if lines is None :
            if self.body :
                charset = self.charset or PMA.default_encoding
                type    = self.content_type
                if type == "text/plain" or type.startswith ("text/x-") :
                    lines = pyk.decoded (self.body, charset).split ("\n")
                    ### XXX put full-quotes-at-end into `self.parts [0]`
                else :
                    cap = PMA.Mailcap [type]
                    if cap :
                        lines = cap.as_text \
                            (self._temp_body (), encoding = charset)
                    if lines is None and type.startswith ("text/") :
                        lines = pyk.decoded (self.body, charset).split ("\n")
                if lines is not None :
                    self.lines = lines
        if lines is not None :
            wrapper = textwrap.TextWrapper \
                (width = PMA.text_output_width, break_long_words = False)
            for line in lines :
                line = line.rstrip ("\r")
                if line :
                    yield from wrapper.wrap (line or "")
                else :
                    ### `wrapper` returns an empty list for an empty string
                    yield line
        else :
            hp = Part_Header (self.email, self.headers_to_show)
            self.lines = lines = list (hp.formatted (sep_length))
            yield from lines
    # end def body_lines

    formatted = _formatted = body_lines

    def save (self, filename) :
        """Save message/part body to file with `filename`"""
        save (filename, self.body)
    # end def save

    def _separators (self, sep_length) :
        if self.name == "Body" :
            seps = ("", "-" * sep_length, "")
        else :
            seps = self.__super._separators (sep_length)
        yield from seps
    # end def _separators

    def _setup_body (self, email) :
        payload = email.get_payload (decode = True)
        if payload :
            self.body = payload.strip ()
    # end def _setup_body

# end class Message_Body

class Part_Header (_Msg_Part_) :
    """Model the headers of a message part as pseudo-part"""

    def __init__ (self, email, headers_to_show) :
        self.headers_to_show = headers_to_show
        self.__super.__init__ (email, "Headers")
    # end def __init__

    @TFL.Meta.Once_Property
    def type (self) :
        return "x-pma/part-headers"
    # end def type

    def body_lines (self, sep_length = 79) :
        return self._fh
    # end def body_lines

    formatted = _formatted = body_lines

    def more_body_lines (self, sep_length = 79) :
        return self._mh
    # end def more_body_lines

    def save (self, filename) :
        """Save message/part headers to file with `filename`"""
        save (filename, "\n".join ("\n".join (self._fh), "\n".join (self._mh)))
    # end def save

    def _separators (self, sep_length) :
        return ()
    # end def _separators

    def _setup_body (self, email) :
        self._fh  = _fh = []
        add       = _fh.append
        _hn       = {}
        for n, h in self._formatted_headers (self.headers_to_show) :
            add (h)
            _hn [n] = h
        self.body = "\n".join (_fh)
        mhn       = sorted (set (k for k in email.keys () if k not in _hn))
        self._mh  = []
        add       = self._mh.append
        seen      = {}
        for n, h in self._formatted_headers (mhn) :
            if h not in seen :
                add  (h)
                seen [h] = True
    # end def _setup_body

# end class Part_Header

class Message_Header (Part_Header) :
    """Model the headers of an email as pseudo-part"""

    def __init__ (self, email, headers_to_show, summary) :
        self.summary_line = summary
        self.__super.__init__ (email, headers_to_show)
    # end def __init__

    @TFL.Meta.Once_Property
    def type (self) :
        return "x-pma/headers"
    # end def type

# end class Message_Header

class _Message_ (_Msg_Part_) :

    def body_lines (self, sep_length = 79) :
        return ()
    # end def body_lines

    def formatted (self, sep_length = 79) :
        for p in self.part_iter () :
            yield from p.formatted (sep_length)
    # end def formatted

    def save (self, filename) :
        """Save message to file with `filename`"""
        save (filename, self.email.as_string ())
    # end def save

    _formatted = formatted

    def _new_part (self, name, p, i) :
        p_name = filtered_join (".", (name, str (i)))
        if p.is_multipart () :
            result = Message_Part (p, p_name)
        else :
            result = Message_Body (p, p_name, Message_Part.headers_to_show)
        return result
    # end def _new_part

    def _setup_body (self, email) :
        name       = b_name = self.name
        self.parts = parts  = []
        self.body  = None
        if isinstance (self, Message) or not b_name :
            b_name = "Body"
        if email.is_multipart () :
            payload = email.get_payload ()
            type    = email.get_content_type ()
            if type == "message/rfc822" :
                p, = payload
                parts.append (Message (p, name))
            elif type == "multipart/alternative" and len (payload) > 1 :
                parts.append (Message_MPA (email, b_name, * payload))
            else :
                parts.extend \
                    ([   self._new_part (name, p, i+1)
                     for (i, p) in enumerate (payload)
                     ]
                    )
        else :
            b = Message_Body (email, b_name, self.headers_to_show)
            parts.append     (b)
    # end def _setup_body

# end class _Message_

class Message_MPA (_Message_) :
    """Model the parts of a multipart/alternative MIME message"""

    def __init__ (self, email, name, head, * rest) :
        self.head = head
        self.rest = rest
        self.__super.__init__ (email, name)
    # end def __init__

    @TFL.Meta.Once_Property
    def type (self) :
        return "x-pma/mpa"
    # end def type

    def _setup_body (self, email) :
        name       = self.name
        self.parts = [self._new_part (name, self.head, 1)]
        self.altp  = \
            [self._new_part (name, p, i+2) for (i, p) in enumerate (self.rest)]
    # end def _setup_body

# end class Message_MPA

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
        , "X-spambayes-classification"
        )
    short_summary_format = \
        ( "%(name)s %(date).12s %(sender_name).20s %(subject).45s "
        )
    summary_format   = \
        ( "%(number)4s %(date)-12.12s %(sender_name)-20.20s %(subject)-25.25s "
          "[%(body)-50.50s"
        )

    body_start       = property (lambda s : s.scope.eval ("body") [:50])
    time             = property (TFL.Method._time)

    def __init__ (self, email, name = None, mailbox = None, number = None) :
        self.__super.__init__ (email, name)
        self.mailbox = mailbox
        self.number  = number
        self.status  = None
        if mailbox :
            self.pending = _Pending_Action_ (self)
            if mailbox.supports_status :
                mdn = mailbox.md_name (self)
                self.status = PMA.Msg_Status.new (mdn)
        if self.status is None :
            self.status = PMA.Msg_Status ()
    # end def __init__

    def formatted (self, sep_length = 79) :
        self.status.set_read ()
        for p in self.part_iter () :
            yield from p._separators (sep_length)
            yield from p._formatted  (sep_length)
    # end def formatted

    def part_iter (self) :
        email = self._reparsed ()
        yield Message_Header \
            ( email
            , self.headers_to_show
            , self.summary (self.short_summary_format)
            )
        yield from self.__super.part_iter ()
    # end def part_iter

    def summary (self, format = None) :
        return self.email_summary (self.email, format)
    # end def summary

    def _reparsed (self) :
        result = self.email
        if self.path and not result._pma_parsed_body :
            if self.mailbox :
                result = self.mailbox.reparsed (self)
            else :
                with open (self.path, "r") as fp :
                    result = Lib.message_from_file (fp)
            result._pma_dir  = getattr (self.email, "_pma_dir",  None)
            result._pma_path = getattr (self.email, "_pma_path", None)
            result._pma_parsed_body = True
            self.email = result
            self._setup_body (result)
        return result
    # end def _reparsed

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

class _Pending_Action_ (TFL.Meta.Object) :

    msg     = property (TFL.Getter._msg)
    copied  = property (lambda s : bool (    s._targets and not s._delete))
    deleted = property (lambda s : bool (not s._targets and     s._delete))
    moved   = property (lambda s : bool (    s._targets and     s._delete))

    def __init__ (self, msg) :
        self._msg = weakref.proxy (msg)
        self.reset ()
    # end def __init__

    def commit (self) :
        """Commit all pending actions of message."""
        affected_boxes = set ()
        msg = self._msg
        for t in self._targets :
            t.add_messages     (msg)
            affected_boxes.add (t)
        self._targets = set ()
        source = self._delete
        if hasattr (source, "delete") :
            try :
                source.delete (msg)
            except Exception as exc :
                print \
                    ( "Couldn't delete `%s (%s)` due to exception `%s`"
                    % (msg.number, msg.name, exc)
                    )
            else :
                self._delete = None
                affected_boxes.add (source)
        return affected_boxes
    # end def commit

    def copy (self, target) :
        """Copy message into mailbox `target` (cancels `delete` if `target`
           is the `mailbox` currently marked for `delete`).
        """
        if target is self._delete :
            self._delete = None
        else :
            if not self._targets :
                self._delete = None
            self._targets.add (target)
    # end def copy

    def delete (self) :
        """Delete message from mailbox"""
        self._delete  = self._msg.mailbox
        self._targets = set ()
    # end def delete

    def move (self, target) :
        """Move message into mailbox `target`"""
        if len (self._targets) == 1 :
            self._targets = set ()
        self._delete = self._msg.mailbox
        self._targets.add (target)
    # end def move

    def reset (self) :
        self._delete  = None
        self._targets = set ()
    # end def reset

    def train_ham (self) :
        """Train message as ham."""
        PMA.SB.train_ham (self._msg)
    # end def train_ham

    def train_spam (self) :
        """Train message as spam."""
        PMA.SB.train_spam (self._msg)
    # end def train_spam

    def untrain_ham (self) :
        """Un-Train message as ham."""
        PMA.SB.untrain_ham (self._msg)
    # end def untrain_ham

    def untrain_spam (self) :
        """Un-Train message as spam."""
        PMA.SB.untrain_spam (self._msg)
    # end def untrain_spam

    def __len__ (self) :
        return self.__bool__ ()
    # end def __len__

    def __bool__ (self) :
        return bool (self._delete or self._targets)
    # end def __bool__

    def __str__ (self) :
        result = ["%s" % self._msg.name]
        if self :
            if self._delete :
                result.append ("delete from %s" % self._delete.path)
            result.extend ("copy to %s" % t.path for t in self._targets)
        else :
            result.append ("no actions pending")
        return ":".join (result)
    # end def __str__

# end class _Pending_Action_

def message_from_file (filename, parser = None) :
    if parser is None :
        parser = Lib.Parser ()
    with open (filename, "r") as fp :
        email = parser.parse (fp)
        email._pma_parsed_body = True
    result = PMA.Message (email, sos.path.split (filename) [-1])
    result.path = filename
    return result
# end def message_from_file

def messages_from_args (args, base_dirs) :
    parser = Lib.Parser ()
    for arg in args :
        matches = tuple \
            ( TFL.CAO.Rel_Path.resolved_paths
                (base_dirs, arg, single_match = False, skip_missing = True)
            )
        if not matches and sos.path.exists (arg) :
            matches = [arg]
        if len (matches) == 1 :
            yield PMA.message_from_file (matches [0], parser)
        elif matches :
            print \
                ( "Multiple matches for %r: choose one of\n    %s"
                % (arg, "\n    ".join (matches))
                )
        else :
            tail = ("in\n    %s" % "\n    ".join (base_dirs)) \
                if base_dirs else ""
            print ("No match found for %r%s" % (arg, tail))
# end def messages_from_args

def formatted (msg, encoding = "utf-8", body_only = False) :
    fmt_msg = "\n".join (msg.formatted ())
    if body_only :
        h, _, t = split_hst (fmt_msg, "\n\n")   ### split off headers
        b, _, s = split_hst (t,       "\n--\n") ### split off signature
        fmt_msg = "\n" + b.lstrip ("-").strip () + "\n"
    if encoding :
        fmt_msg = fmt_msg.encode (encoding, "replace")
    return fmt_msg
# end def formatted

_text_to_pdf_options = \
    [ "-columns=2"
    , "-Cutable"
    , "-Font_Family=Dejavu"
    , "-font_size=6.8"
    , "-footer='$p#||$c'"
    , "-Footer_size_factor=1.0"
    , "-header='$t|$s'"
    , "-Header_size_factor=1.2"
    , "-landscape"
    , "-Print"
    , "-purge"
    , "STDIN"
    ]

def _main (cmd) :
    from _TFL.formatted_repr import formatted_repr
    import subprocess
    encoding        = PMA.default_encoding = pyk.user_config.output_encoding
    msg_base_dirs   = cmd.msg_base_dirs or PMA.msg_base_dirs
    printer_name    = cmd.printer_name
    for msg in messages_from_args (cmd.argv, msg_base_dirs) :
        txt         = formatted (msg, encoding = None)
        if cmd.Print :
            scope   = msg.scope
            date    = scope.full_date
            sender  = scope.sender_name or msg.sender_addr
            subject = scope.subject
            p_cmd   = \
                [ sys.executable, "-m", "_TFL.text_to_pdf"
                , "-printer_name='%s'"    % (printer_name, )
                , "-Subject='%s'"         % sender
                , "-Title='%s'"           % subject
                ] + _text_to_pdf_options
            if cmd.verbose :
                print (formatted_repr (p_cmd))
            subprocess.run \
                ( p_cmd
                , encoding = encoding
                , env      = dict (sos.environ)
                , input    = txt
                )
        else :
            print (txt)
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "message:S?Message(s) to print"
        ,
        )
    , opts          =
        ( "-body_only:B?Restrict output to body of message"
        , "-msg_base_dirs:Q:?Base directories for searching `message`"
        , "-Print:B?Print the message(s)"
        , "-printer_name:S=lp?Name of printer to print to"
        , "-verbose:B"
        , TFL.CAO.Opt.Output_Encoding ()
        )
    , description   = "Format mail messages for viewing and printing"
    )

if __name__ != "__main__" :
    PMA._Export ("*")
else :
    import _PMA.Message
    PMA.load_user_config  ()
    _PMA.Message._Command ()
### __END__ PMA.Message
