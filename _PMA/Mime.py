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
#    PMA.Mime
#
# Purpose
#    Support creation of mime parts
#
# Revision Dates
#    28-Jul-2005 (CT) Creation
#     9-Aug-2005 (CT) s/default_charset/default_encoding/g
#    29-Oct-2015 (CT) Improve Python 3 compatibility
#     4-Nov-2015 (CT) Use `pyk.email_message_from_bytes`,
#                     not `Lib.message_from_string` because Python 3
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _TFL.Filename
import _TFL.sos

from   _TFL.pyk                import pyk
from   _TFL.Regexp             import *

import mimetypes

default_type         = "application/octet-stream"
unencoded_mime_types = ("text/plain", "message/rfc822")

_sep                 = TFL.sos.sep
mh_pat               = Regexp (r"%sMH%s.*%s\d+$" % (_sep, _sep, _sep))

extension_map        = {}

def add_extensions (typ, enc, * extensions) :
    for ext in extensions :
        extension_map [ext] = (typ, enc)
# end def add_extensions

add_extensions \
    ("text/plain", None, ".pl", ".c", ".cc", ".h", ".el", ".lse", ".txt")
add_extensions \
    ("text/x-python", None, ".py")
add_extensions \
    ("application/gzip", "base64", ".gz", ".tgz")

class _M_Type_ (TFL.Meta.Object) :

    mode = "rb"

    def __init__ (self, MIME) :
        self.MIME = MIME
    # end def __init__

    def __call__ (self, mt, st, filename) :
        with open (filename, self.mode) as f :
            b = f.read ()
        return self._new (mt, st, b)
    # end def __call__

    def _new (self, mt, st, b) :
        return self.MIME (pyk.as_str (b, "latin-1"), _subtype = st)
    # end def _new

# end class _M_Type_

class _M_Type_B_ (_M_Type_) :

    def _new (self, mt, st, b) :
        result = self.MIME (mt, st)
        result.set_payload (b)
        Lib.encode_base64  (result)
        return result
    # end def _new

# end class _M_Type_B_

class _M_Type_Msg_ (_M_Type_) :

    def _new (self, mt, st, b) :
        msg = pyk.email_message_from_bytes (pyk.encoded (b, "latin-1"))
        return self.MIME (msg, _subtype = st)
    # end def _new

# end class _M_Type_Msg_

class _M_Type_Text_ (_M_Type_) :

    mode    = "r"

    def _new (self, mt, st, b) :
        return self.MIME \
            ( pyk.as_str (b, "latin-1")
            , _subtype = st, _charset = PMA.default_encoding
            )
    # end def _new

# end class _M_Type_Text_

MIME_Map = dict \
    ( application = _M_Type_B_     (Lib.MIMEBase)
    , audio       = _M_Type_       (Lib.MIMEAudio)
    , image       = _M_Type_       (Lib.MIMEImage)
    , message     = _M_Type_Msg_   (Lib.MIMEMessage)
    , text        = _M_Type_Text_  (Lib.MIMEText)
    )

def guess_type (name) :
    fname = TFL.Filename (name)
    try :
        typ, enc = extension_map [fname.ext]
    except KeyError :
        typ, enc = mimetypes.guess_type (name)
        if not typ :
            if mh_pat.search (name) :
                typ = "message/rfc822"
            else :
                typ = default_type
    if typ not in unencoded_mime_types :
        enc = "base64"
    return typ, enc
# end def guess_type

def Part (filename, additional_headers) :
    """Returns a MIME object with the contents of the file named `filename`.

       The result can be attached to a `email.Message` object.
    """
    typ, enc = guess_type (filename)
    if additional_headers :
        t = additional_headers.get ("Content-Type", None)
        if t :
            typ = t
        e = additional_headers.get ("Content-Transfer-Encoding", None)
        if e :
            enc = e
    mt, st   = (x.lower () for x in typ.split ("/", 1))
    result   = MIME_Map.get (mt, MIME_Map ["application"]) (mt, st, filename)
    if additional_headers :
        for k in additional_headers.keys () :
            for h in additional_headers.get_all (k, []) :
                if h :
                    del result [k]
                    result [k] = h
    if "Content-Disposition" not in result :
        result ["Content-Disposition"] = \
            ( """attachement; filename="%s" """
            % TFL.Filename (filename).base_ext
            )
    return result
# end def Part

if __name__ != "__main__" :
    PMA._Export_Module ()
### __END__ PMA.Mime
