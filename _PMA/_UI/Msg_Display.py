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
#    PMA.UI.Msg_Display
#
# Purpose
#    UI for display of PMA.UI.Message
#
# Revision Dates
#    17-May-2005 (CT) Creation
#    18-May-2005 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Message
import _PMA.Mailcap

import _PMA._UI
import _PMA._UI.HTD
import _PMA._UI.Mixin

import _TGL._UI.HTD

class _Node_Mixin_ (PMA.UI.Mixin) :

    def __init__ (self, msg, * args, ** kw) :
        self.msg = msg
        self.__super.__init__ (* args, ** kw)
    # end def __init__

# end class _Node_Mixin_

class _MD_Node_ (_Node_Mixin_, TGL.UI.HTD.Node) :
    pass
# end class _MD_Node_

class _MD_Node_B_ (_Node_Mixin_, TGL.UI.HTD.Node_B) :
    pass
# end class _MD_Node_B_

class _MD_Node_B2_ (_Node_Mixin_, TGL.UI.HTD.Node_B2) :
    pass
# end class _MD_Node_B2_

class _MD_Node_B8_ (_Node_Mixin_, TGL.UI.HTD.Node_B8) :
    pass
# end class _MD_Node_B8_

class _Node_C_ (_Node_Mixin_, TGL.UI.HTD.Node_C) :
    pass
# end class _Node_C_

class _Generic_Node_ (_MD_Node_B2_) :

    def __init__ (self, msg, parent) :
        body = u"\n".join (msg.body_lines ())
        self.__super.__init__ \
            ( msg
            , parent   = parent
            , contents =
                ( ("%s %s %s" % (msg.name, msg.type, msg.filename), )
                , (body, )
                )
            )
    # end def __init__

# end class _Generic_Node_

class _Header_Node_ (_MD_Node_B2_) :

    def __init__ (self, msg, parent) :
        S    = _Root_.Style
        head = S.T (u"\n".join (msg.body_lines      ()), S.headers)
        more = S.T (u"\n".join (msg.more_body_lines ()), S.more_headers)
        self.__super.__init__ \
            ( msg
            , parent   = parent
            , contents =
                ( ( head, )
                , ( head, "\n", more)
                )
            )
    # end def __init__

# end class _Header_Node_

class _Text_Node_ (_MD_Node_B2_) :

    def __init__ (self, msg, parent) :
        body = u"\n".join (msg.body_lines ())
        self.__super.__init__ \
            ( msg
            , parent   = parent
            , contents =
                ( ("%s %s %s" % (msg.name, msg.type, msg.filename), )
                , (body, )
                )
            )
        if msg.type == "text/plain" :
            self.inc_state ()
    # end def __init__

# end class _Text_Node_

### http://www.faqs.org/rfcs/rfc2046.html
### http://www.iana.org/assignments/media-types/
_mime_map = \
    { "application"              : _Generic_Node_
    , "audio"                    : _Generic_Node_
    , "image"                    : _Generic_Node_
    , "message"                  : _Generic_Node_
    , "message/external-body"    : _Generic_Node_ ### XXX
    , "message/partial"          : _Generic_Node_ ### XXX
    , "message/rfc822"           : _Generic_Node_ ### XXX
    , "multipart"                : _Generic_Node_
    , "multipart/alternative"    : _Generic_Node_ ### XXX
    , "multipart/digest"         : _Generic_Node_
    , "multipart/encrypted"      : _Generic_Node_ ### XXX rfc1847
    , "multipart/form-data"      : _Generic_Node_ ### XXX rfc2388
    , "multipart/mixed"          : _Generic_Node_
    , "multipart/parallel"       : _Generic_Node_
    , "multipart/related"        : _Generic_Node_ ### XXX rfc2387
    , "multipart/signed"         : _Generic_Node_ ### XXX rfc1847
    , "text"                     : _Text_Node_
    , "text/calendar"            : _Text_Node_    ### XXX rfc2445
    , "text/directory"           : _Text_Node_    ### XXX rfc2425
    , "text/enriched"            : _Text_Node_    ### XXX rfc1896
    , "text/html"                : _Generic_Node_ ### XXX rfc2854
    , "video"                    : _Generic_Node_
    , "x-pma/headers"            : _Header_Node_
    }

class _Root_ (TGL.UI.HTD.Root) :

    Style               = TGL.UI.Style.__class__ ()
    _style_defaults     = dict \
        ( TGL.UI.HTD.Root._style_defaults
        , courierFontFamily      = "Monospace"
        , titleFontSize          = "medium"
        )

# end class _Root_

class MD_Root (_Root_) :
    """Root node of message display"""

    msg                 = None
    summary_format      = unicode \
        ( "%(number)4s %(name)-10s %(date)-12.12s %(sender)-20.20s "
          "%(subject)-50.50s "
        )

    def display (self, msg) :
        self.clear ()
        self.msg = msg
        if 0 :
            _MD_Node_ \
                ( msg
                , parent   = self
                , contents = msg.summary (self.summary_format)
                , style    = self.Style.title
                    ( background = "gray90"
                    , foreground = "deep sky blue"
                    , wrap       = "none"
                    )
                )
        self._add_parts (self, msg)
    # end def display

    def _add_parts (self, disp, msg) :
        for p in msg.part_iter () :
            body = p.body_lines ()
            if p.type.startswith ("multipart/") :
                d = disp
            else :
                d = self._mime_node (p) (p, disp)
            self._add_parts (d, p)
    # end def _add_parts

    def _mime_node (self, msg) :
        type = msg.type.lower ()
        base = type.split ("/") [0]
        return (_mime_map.get (type, _mime_map.get (base, _Generic_Node_)))
    # end def _mime_node

    def _setup_styles (self, w) :
        self.__super._setup_styles (w)
        Style = self.Style
        add   = Style.add
        add ( "headers"
            , foreground = "red"
            , font_size  = "medium"
            )
        add ( "more_headers"
            , foreground = "gray30"
            , font_size  = "small"
            )
    # end def _setup_styles

# end class MD_Root

class MO_Root (_Root_) :
    """Root node of message outline"""

    summary_format      = unicode ("%(name)-10s %(type)-20.20s")

    _style_defaults     = dict \
        ( _Root_._style_defaults
        , normalFontSize         = "small"
        , titleFontSize          = "small"
        )

    def __init__ (self, controlled, * args, ** kw) :
        self.controlled = controlled
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def display (self) :
        self.clear           ()
        self._add_parts      (self, self.controlled)
        self.controlled.goto ()
    # end def display

    def _add_parts (self, disp, controlled) :
        Node = _Node_C_
        for c in controlled.children :
            o = Node \
                ( msg        = c.msg
                , controlled = c
                , parent     = disp
                , contents   = c.msg.summary (self.summary_format)
                , style      = c.u_style
                )
            self._add_parts (o, c)
    # end def _add_parts

# end class MO_Root

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ Msg_Display
