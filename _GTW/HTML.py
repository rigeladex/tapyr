# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.HTML
#
# Purpose
#    Provide HTML related functions for GTW
#
# Revision Dates
#    17-Feb-2010 (CT) Creation
#    17-Mar-2010 (CT) `Cleaner` added
#     3-Aug-2010 (CT) `obfuscator` completely revamped (letting jQuery
#                     rewrite the obfuscated `<a...</a>` elements)
#     1-Dec-2011 (CT) Add `Styler`
#     5-Dec-2011 (CT) Add `Entity_Map` and use in `Styler`
#    23-Dec-2011 (CT) Factor `Styler_Safe` and `Entity_Map_Safe`
#    22-Feb-2012 (CT) Add `Video`, `Vimeo` and `Youtube`
#    22-Feb-2012 (CT) Change `_obfuscator_format` so it's valid html5
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import *
from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object
import _TFL.Caller

from   random                   import randrange

import urllib

_obfuscator_format = """\
<a class="nospam" title="%(need)s">%(text)s</a>\
<b class="nospam" title="%(js_args)s"></b>\
"""

scheme_map = dict \
    ( mailto = _("email address")
    , tel    = _("phone number")
    )

def obfuscated (text) :
    """Return `text` as (slightly) obfuscated Javascript array."""
    result = ",".join \
        ( "%s%+d" % (s, c - s)
        for (c, s) in ((ord (c), randrange (1, 256)) for c in text)
        )
    return result
# end def obfuscated

def _obfuscator (scheme = "mailto") :
    def _rep (match) :
        return _obfuscator_format % dict \
            ( js_args  = obfuscated  (match.group (0))
            , need     =
                ( _T ("Need Javascript for displaying %s")
                % _T (scheme_map.get (scheme, scheme))
                )
            , text     = match.group (2)
            )
    return Re_Replacer \
        ( r"(?:"
            r"<a"
            r"("
              r"(?:\s+\w+=" r'"[^"]*"' r")*"
              r"\s+href=" r'"' r"mailto:[^>]+>"
            r")"
          r")"
          r"([^<]*)"
          r"(</a>)"
        , _rep, re.MULTILINE
        )
# end def _obfuscator

obfuscator = dict ((s, _obfuscator (s)) for s in scheme_map)

class Cleaner (TFL.Meta.Object) :
    """Clean up HTML using BeautifulSoup."""

    def __init__ (self, input) :
        self.input = input
    # end def __init__

    def remove_comments (self) :
        from BeautifulSoup import Comment
        matcher = lambda t : isinstance (t, Comment)
        return [str (c) for c in self._remove (text = matcher)]
    # end def remove_comments

    def remove_tags (self, * tags) :
        return set (t.name for t in self._remove (tags))
    # end def remove_tags

    @Once_Property
    def soup (self) :
        from BeautifulSoup import BeautifulSoup
        return BeautifulSoup (self.input)
    # end def soup

    def _remove (self, * args, ** kw) :
        result = []
        for c in self.soup.findAll (* args, ** kw) :
            result.append (c)
            c.extract ()
        return result
    # end def _remove

    def __str__ (self) :
        return str (self.soup)
    # end def __str__

    def __unicode__ (self) :
        return unicode (self.soup)
    # end def __unicode__

# end class Cleaner

Entity_Map = \
    { r"---"          : r"&#0032;&mdash;&#0032;"
    , r"..."          : r"&#8230;"
    , r"(c)"          : r"&#0032;&copy;&#0032;"
    , r"!="           : r"&ne;"
    , r"=="           : r"&equiv;"
    , r">="           : r"&ge;"
    , r"<="           : r"&le;"
    , r"+/-"          : r"&plusmn;"
    , r"+-"           : r"&plusmn;"
    }
Entity_Map_Safe = \
    { r">"            : r"&gt;"
    , r"<"            : r"&lt;"
    , r"&"            : r"&amp;"
    }
Entity_Map_Safe.update (Entity_Map)

_dash_replacers = \
    ( Re_Replacer   (r"(?<!<!)--(?!>)", r"&#0032;&ndash;&#0032;")
    , Re_Replacer   (r"\%2d\%2d",       r"--")
    )

Styler = Multi_Re_Replacer (Dict_Replacer (Entity_Map), * _dash_replacers)

Styler_Safe = Multi_Re_Replacer \
    (Dict_Replacer (Entity_Map_Safe), * _dash_replacers)

class Video (TFL.Meta.Object) :
    """Generate html-element to embedd a video."""

    css_class          = "video"
    format             = """
        <div class="%(css_class)s" style="width:%(width + 10)spx">
          <iframe
            src="%(player_url)s%(video_id)s%(query)s"
            width="%(width)s" height="%(height)s"
          ></iframe>
        </div>
        <p class="video-desc">
          <a href="%(watcher_url)s%(video_id)s">
            %(desc)s
          </a>
        </p>
        """.strip ()
    q_parameters       = dict \
        ( autoplay     = 0   ### play the video automatically on load
        , loop         = 0   ### play the video again when it reaches the end
        ,
        )
    ws_replacer        = Re_Replacer (r"  +", " ")

    def __call__ (self, video_id, ** kw) :
        css_classes = [self.css_class]
        if "css_class" in kw :
            css_classes.append (kw.pop ("css_class"))
        if "align" in kw :
            css_classes.append ("align-%s" % (kw.pop ("align"), ))
        css_class   = " ".join (c for c in css_classes if c)
        height      = kw.pop ("height",      self.height)
        width       = kw.pop ("width",       self.width)
        desc        = kw.pop ("desc",        self.watcher_url + video_id)
        query       = "?" + urllib.urlencode (dict (self.q_parameters, ** kw))
        result      =  self.format % TFL.Caller.Object_Scope (self)
        result      = self.ws_replacer (result)
        return result
    # end def __call__

# end class Video

class Vimeo (Video) :
    """Generate html-element to embedd a Vimeo video.

    >>> print vimeo_video ("34480636", desc = "Seascape 18 Gaea+ Christmas Sailing", align = "right")
    <div class="video align-right" style="width:410px">
     <iframe
     src="http://player/vimeo.com/video/34480636?color=%2300adef&byline=0&title=0&api=1&portrait=0&loop=0&autoplay=0"
     width="400" height="300"
     ></iframe>
     </div>
     <p class="video-desc">
     <a href="http://vimeo.com/34480636">
     Seascape 18 Gaea+ Christmas Sailing
     </a>
     </p>

    """

    ### http://vimeo.com/api/docs/player

    color              = "#00adef"  ### default color for player controls "#"
    height             = 300
    width              = 400
    q_parameters       = dict \
        ( Video.q_parameters
        , api          = 1     ### enable Javascript API
        , byline       = 0     ### show the byline on the video
        , color        = color ### specify the color of the video controls
        , portrait     = 0     ### show the user's portrait on the video
        , title        = 0     ### show the title on the video
        )
    service_name       = "Vimeo"
    service_url        = "http://vimeo.com/"
    player_url         = "http://player/vimeo.com/video/"
    watcher_url        = service_url

# end class Vimeo

class Youtube (Video) :
    """Generate html-element to embedd a youtube video.

    >>> print youtube_video ("EeMJErxbn1I", css_class = "centered")
    <div class="video centered" style="width:435px">
     <iframe
     src="http://www.youtube.com/embed/EeMJErxbn1I?showinfo=0&modestbranding=0&controls=1&enablejsapi=1&theme=light&fs=1&autohide=2&rel=0&loop=0&showsearch=0&hd=0&autoplay=0"
     width="425" height="349"
     ></iframe>
     </div>
     <p class="video-desc">
     <a href="http://www.youtube.com/watch?v=EeMJErxbn1I">
     http://www.youtube.com/watch?v=EeMJErxbn1I
     </a>
     </p>

    """

    ### https://code.google.com/apis/youtube/player_parameters.html

    height             = 349
    width              = 425
    q_parameters       = dict \
        ( Video.q_parameters
        , autohide       = 2   ### video controls will automatically hide
        , controls       = 1   ### display video player controls
        , enablejsapi    = 1   ### enable Javascript API
        , fs             = 1   ### enable the fullscreen button
        , hd             = 0   ### enable HD playback by default
        , modestbranding = 0   ### show a YouTube logo if 1
        , rel            = 0   ### load related videos if 1
        , showinfo       = 0   ### show video title and uploader if 1
        , showsearch     = 0   ### show search box if 1
        , theme          = "light" ### valid values: "dark" and "light"
        )
    service_name       = "YouTube"
    service_url        = "http://www.youtube.com/"
    player_url         = "".join ((service_url, "embed/"))
    watcher_url        = "".join ((service_url, "watch?v="))

# end class Youtube

vimeo_video   = Vimeo   ()
youtube_video = Youtube ()

if __name__ != "__main__" :
    GTW._Export_Module ()
### __END__ GTW.HTML
