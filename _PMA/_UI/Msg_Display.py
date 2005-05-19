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
#    19-May-2005 (CT) Creation continued...
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Message
import _PMA.Mailcap

import _PMA._UI
import _PMA._UI.HTD
import _PMA._UI.Mixin

from   _TFL.Regexp             import *

import _TGL._UI.HTD
from   _TGL._UI.Styled         import Styled

import itertools

class _Node_Mixin_ (PMA.UI.Mixin) :

    _level_inc = 0

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

class _MD_Node_B3_ (_Node_Mixin_, TGL.UI.HTD.Node_B3) :
    pass
# end class _MD_Node_B3_

class _MD_Node_B8_ (_Node_Mixin_, TGL.UI.HTD.Node_B8) :
    pass
# end class _MD_Node_B8_

class _Node_C_ (_Node_Mixin_, TGL.UI.HTD.Node_C) :
    _level_inc = 1
# end class _Node_C_

class _Generic_Node_ (_MD_Node_B2_) :

    def __init__ (self, msg, parent, ** kw) :
        summary = "%s %s %s" % (msg.name, msg.type, msg.filename)
        self.__super.__init__ \
            ( msg
            , parent   = parent
            , contents =
                ( (summary, )
                , (lambda : u"\n".join (msg.body_lines ()) or summary, )
                )
            , ** kw
            )
    # end def __init__

# end class _Generic_Node_

class _Header_Node_ (_MD_Node_B3_) :

    def __init__ (self, msg, parent, ** kw) :
        S    = _Root_.Style
        n    = 78 - (parent.level * 3)
        summ = S.T (msg.summary_line [: n] ,             S.headers)
        head = S.T (u"\n".join (msg.body_lines      ()), S.headers)
        more = S.T (u"\n".join (msg.more_body_lines ()), S.more_headers)
        self.__super.__init__ \
            ( msg
            , parent   = parent
            , contents =
                ( ( summ, )
                , ( head, )
                , ( head, "\n", more)
                )
            , ** kw
            )
    # end def __init__

# end class _Header_Node_

class _Message_Node_ (_MD_Node_B2_) :

    summary_format      = unicode \
        ( "%(name)s %(date).12s %(sender).20s %(subject)s "
        )

    def __init__ (self, msg, parent, ** kw) :
        email = msg.parts [0]
        n     = 78 - (parent.level * 3)
        self.__super.__init__ \
            ( msg
            , parent   = parent
            , contents =
                ( (email.summary (self.summary_format) [: n], )
                , ("%s %s %s" % (msg.name, msg.type, msg.filename), )
                )
            , ** kw
            )
        self.inc_state ()
    # end def __init__

# end class _Message_Node_

class _MPA_Node_ (_MD_Node_B8_) :

    no_of_states        = property (lambda s : s._no_of_states)
    type                = "multipart/alternative"

    def __init__ (self, msg, parent, ** kw) :
        self._no_of_states = len (msg.altp) + 1
        self.__super.__init__ \
            ( msg
            , parent   = parent
            , contents =
                [ (u"\n".join (msg.parts [0].body_lines ()), )
                ] + [   (lambda : u"\n".join (p.body_lines ()), )
                    for p in msg.altp
                    ]
            , ** kw
            )
    # end def __init__

# end class _MPA_Node_

class _Part_Header_Node_ (_MD_Node_B2_) :

    def __init__ (self, msg, parent, ** kw) :
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
            , ** kw
            )
    # end def __init__

# end class _Part_Header_Node_

class _Text_Node_ (_MD_Node_B2_) :

    def __init__ (self, msg, parent, ** kw) :
        if msg.body :
            body = self._body
            head = "%s %s %s" % (msg.name, msg.type, msg.filename)
        else :
            body = ""
            head = "%s %s %s" % (msg.name, msg.type, "<empty body>")
        self.__super.__init__ \
            ( msg
            , parent   = parent
            , contents = ((head, ), (body, ))
            , ** kw
            )
        if msg.body and msg.type == "text/plain" :
            self.inc_state ()
    # end def __init__

    def _body (self) :
        return u"\n".join (self.msg.body_lines ())
    # end def _body

# end class _Text_Node_

class _Plain_Text_Node (_Text_Node_) :

    _block_patterns = \
        ( ( Regexp ( r"(^--[-\s]*$)|(^(?: - \s)+ \s*$)", re.VERBOSE), "sig1")
        , ( Regexp ( r"(^_+\s*$)",                       re.VERBOSE), "sig2")
        )

    _line_patterns  = \
        ( ( Regexp ( r"^\+", re.VERBOSE), "diff_new")
        , ( Regexp ( r"^\-", re.VERBOSE), "diff_old")
        , ( Regexp ( r"^\s* [A-Za-z]* \s* (?P<q> >(?: [\s>]*))", re.VERBOSE)
          , lambda p : "quote%s" % (min (p.q.count (">"), 5), )
          )
        )

    def _body (self) :
        for block, style in self._style_block (self.msg.body_lines ()) :
            block.append ("")
            yield Styled ("\n".join (block), style)
    # end def _body

    def _match_style (self, l, patterns) :
        for p, s in patterns :
            if p.match (l) :
                if callable (s) :
                    s = s (p)
                return getattr (_Root_.Style, s)
    # end def _match_style

    def _style_block (self, lines) :
        Style      = _Root_.Style
        block      = []
        in_block   = False
        last_line  = None
        last_style = None
        for l in lines :
            if not in_block :
                style = self._match_style (l, self._line_patterns)
            if last_line == "" :
                s = self._match_style (l, self._block_patterns)
                if s is not None :
                    in_block = True
                    style    = s
            if block and style != last_style :
                yield block, last_style
                block = []
            block.append (l)
            last_line  = l.strip ()
            last_style = style
        if block :
            yield block, last_style
    # end def _style_block

# end class _Plain_Text_Node

### http://www.faqs.org/rfcs/rfc2046.html
### http://www.iana.org/assignments/media-types/
_mime_map = \
    { "application"              : _Generic_Node_
    , "audio"                    : _Generic_Node_
    , "image"                    : _Generic_Node_
    , "message"                  : _Generic_Node_
    , "message/external-body"    : _Generic_Node_ ### XXX
    , "message/partial"          : _Generic_Node_ ### XXX
    , "message/rfc822"           : _Message_Node_
    , "multipart"                : _Generic_Node_
    , "multipart/alternative"    : _Generic_Node_
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
    , "text/plain"               : _Plain_Text_Node
    , "video"                    : _Generic_Node_
    , "x-pma/headers"            : _Header_Node_
    , "x-pma/mpa"                : _MPA_Node_
    , "x-pma/part-headers"       : _Part_Header_Node_
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
        self._add_parts \
            ( self, msg
            , itertools.cycle ((self.Style.bg_even, self.Style.bg_odd))
            )
    # end def display

    def _add_parts (self, disp, msg, cycle) :
        for p in msg.part_iter () :
            body = p.body_lines ()
            if p.type.startswith ("multipart/") :
                d = disp
            else :
                d = self._mime_node (p) (p, disp, style = cycle.next ())
            if p.type != "x-pma/mpa" :
                self._add_parts (d, p, cycle)
    # end def _add_parts

    def _mime_node (self, msg) :
        type = msg.type
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
        add ("bg_even",   background = "lightyellow1")
        add ("bg_odd",    background = "lightyellow2")
        add ("diff_new",  foreground = "red")
        add ("diff_old",  foreground = "blue")
        add ("quote1",    foreground = "DeepPink3")
        add ("quote2",    foreground = "DeepPink2")
        add ("quote3",    foreground = "DeepPink1")
        add ("quote4",    foreground = "HotPink3")
        add ("quote5",    foreground = "HotPink2")
        add ("sig1",      foreground = "magenta2")
        add ("sig2",      foreground = "cornflower blue")
    # end def _setup_styles

# end class MD_Root

class MO_Root (_Root_) :
    """Root node of message outline"""

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
            m = c.msg
            o = Node \
                ( msg        = m
                , controlled = c
                , parent     = disp
                , contents   =
                    "%-10s %-20.20s" % (m.name, getattr (c, "type", m.type))
                , style      = c.u_style
                )
            self._add_parts (o, c)
    # end def _add_parts

# end class MO_Root

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ Msg_Display
