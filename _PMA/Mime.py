# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    PMA.Mime
#
# Purpose
#    Support creation of mime parts
#
# Revision Dates
#    28-Jul-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _TFL.Filename
import _TFL.sos

from   _TFL.Regexp             import *

import mimetypes

default_type         = "application/octet-stream"
unencoded_mime_types = ("text/plain", "message/rfc822")

_sep                 = TFL.sos.sep
mh_pat               = Regexp (r"%sMH%s.*%s\d+$" % (_sep, _sep, _sep))

extension_map        = {}

def _add_extensions (typ, enc, * extensions) :
    for ext in extensions :
        extension_map [ext] = (typ, enc)
# end def _add_extensions

_add_extensions \
    ("text/plain", None, ".pl", ".c", ".cc", ".h", ".el", ".lse", ".txt")
_add_extensions \
    ("text/x-python", None, ".py")
_add_extensions \
    ("application/gzip", "base64", ".gz", ".tgz")

class _M_Type_ (TFL.Meta.Object) :

    mode = "rb"

    def __init__ (self, MIME) :
        self.MIME = MIME
    # end def __init__

    def __call__ (self, mt, st, filename) :
        f = open   (filename, self.mode)
        b = f.read ()
        f.close    ()
        return self._new (mt, st, b)
    # end def __call__

    def _new (self, mt, st, b) :
        return self.MIME (b, _subtype = st)
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
        return self.MIME (Lib.message_from_string (b), _subtype = st)
    # end def _new

# end class _M_Type_Msg_

class _M_Type_Text_ (_M_Type_) :

    mode    = "r"
    charset = "iso-8859-1"

    def _new (self, mt, st, b) :
        return self.MIME (b, _subtype = st, _charset = self.charset)
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
