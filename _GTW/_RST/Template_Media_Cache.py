# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
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
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.Template_Media_Cache
#
# Purpose
#    Cache media fragments for templates
#
# Revision Dates
#    24-Jul-2012 (CT) Creation (ported from GTW.NAV)
#    ��revision-date�����
#--

from   _GTW                   import GTW
from   _TFL                   import TFL

import _GTW._RST

from   _TFL                   import sos

import _TFL._Meta.Object
import _TFL.predicate

import  hashlib
import  base64
from    posixpath import join as pp_join

class Template_Media_Cache (TFL.Meta.Object) :

    cache_rank = 1000

    def __init__ (self, media_dir, prefix, clear_dir = False) :
        if not prefix.startswith ("/") :
            prefix     = "/%s" % (prefix, )
        self.media_dir = media_dir
        self.prefix    = prefix
        self.clear_dir = clear_dir
    # end def __init__

    def as_pickle_cargo (self, root) :
        if self.clear_dir :
            self._clear_dir ()
        css_map = {}
        js_map  = {}
        TEST    = root.TEST
        TT      = root.Templateer.Template_Type
        for t in TFL.uniq (root.template_iter ()) :
            css_href = self._add_to_map (t, "CSS", css_map)
            js_href  = None if TEST else self._add_to_map (t, "js", js_map)
            TT.Media_Map [t.name] = t.get_cached_media (css_href, js_href)
        self._create_cache ("CSS", css_map, None if TEST else GTW.minified_css)
        if not TEST :
            self._create_cache ("js", js_map, GTW.minified_js)
        return dict (css_href_map = TT.css_href_map, Media_Map = TT.Media_Map)
    # end def as_pickle_cargo

    def from_pickle_cargo (self, root, cargo) :
        TT              = root.Templateer.Template_Type
        TT.css_href_map = cargo.get ("css_href_map", {})
        TT.Media_Map    = cargo.get ("Media_Map",    {})
    # end def from_pickle_cargo

    def _add_to_map (self, t, name, map) :
        try :
            attr = getattr (t, name)
        except Exception as exc :
            print name, "exception for template", t.path
            print "   ", exc
            if __debug__ :
                import traceback
                traceback.print_exc ()
        else :
            if attr :
                attr = attr.encode      (t.env.encoding)
                h    = hashlib.sha1     (attr).digest ()
                k    = base64.b64encode (h, "_-").rstrip ("=")
                if k not in map :
                    cn      = ".".join      ((k, name.lower ()))
                    href    = pp_join       (self.prefix,    cn)
                    fn      = sos.path.join (self.media_dir, cn)
                    map [k] = (href, fn, attr)
                else :
                    href = map [k] [0]
                return href
    # end def _add_to_map

    def _clear_dir (self) :
        for fod in sos.listdir_full (self.media_dir) :
            if sos.path.isdir (fod) :
                sos.rmdir  (fod, True)
            else :
                sos.unlink (fod)
    # end def _clear_dir

    def _create_cache (self, name, map, minifier = None) :
        media_dir = self.media_dir
        if not sos.path.isdir (media_dir) :
            sos.mkdir_p (media_dir)
        for k, (href, fn, attr) in map.iteritems () :
            with open (fn, "wb") as file :
                if minifier is not None :
                    attr = minifier (attr)
                file.write (attr)
    # end def _create_cache

    def __str__ (self) :
        return "Template_Media_Cache (%r, %r)" % (self.media_dir, self.prefix)
    # end def __str__

# end class Template_Media_Cache

if __name__ != "__main__" :
    GTW.RST._Export ("*")
### __END__ GTW.RST.Template_Media_Cache