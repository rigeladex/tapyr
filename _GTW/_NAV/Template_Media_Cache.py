# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.NAV.
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
#    GTW.NAV.Template_Media_Cache
#
# Purpose
#    Handling of the caching of media fragments for templates
#
# Revision Dates
#    26-Sep-2011 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW                   import GTW
import _GTW._NAV

from   _TFL                   import TFL
from   _TFL                   import sos as os
import _TFL._Meta.Object
from    _TFL.predicate        import first
from   _JNJ                   import JNJ

import  hashlib
import  base64
from    posixpath import join as pjoin

class Template_Media_Cache (TFL.Meta.Object) :

    rank = 1000

    def __init__ (self, css_dir, prefix, clear_dir = False) :
        if not prefix [0] == "/" :
            prefix     = "/%s" % (prefix, )
        self.css_dir   = css_dir
        self.prefix    = prefix
        self.clear_dir = clear_dir
    # end def __init__

    def as_pickle_cargo (self, nav_root) :
        if self.clear_dir :
            self._clear_dir ()
        T            = nav_root.Templateer
        css_map_t    = TFL.mm_list ()
        css_map_i    = TFL.mm_list ()
        css_map_p    = TFL.mm_list ()
        it_media_map = TFL.mm_list ()
        for tn in nav_root.template_names :
            t = T.get_template (tn)
            self._add_to_css_map (t, css_map_t)
        for nav in nav_root.children_transitive :
            t = JNJ.Injected_Templates (T.env, nav.injected_templates)
            if t is not None :
                self._add_to_css_map (t, css_map_i, nav)
        for p, t, _   in self._create_css_cache ("t", css_map_t) :
            css_map_p [p].append (t.path)
        for p, t, nav in self._create_css_cache ("i", css_map_i) :
            it_media_map [p].append (nav.injected_media_href)
        return dict (css_map_t = css_map_p, css_map_i = it_media_map)
    # end def as_pickle_cargo

    def _add_to_css_map (self, t, css_map, obj = None) :
        try :
            css = t.CSS
        except Exception as exc :
            print "CSS exception for template", t.path
            print "   ", exc
            if __debug__ :
                import traceback
                traceback.print_exc ()
        else :
            if css :
                h = hashlib.sha1     (css).digest ()
                k = base64.b64encode (h, "_-").rstrip ("=")
                css_map [k].append   ((t, obj))
    # end def _add_to_css_map

    def _clear_dir (self) :
        for fod in os.listdir_full (self.css_dir) :
            if os.path.isdir (fod) :
                os.rmdir  (fod, True)
            else :
                os.unlink (fod)
    # end def _clear_dir

    def _create_css_cache (self, suffix, css_map) :
        for k, ts_and_obj in css_map.iteritems () :
            cn = "%s-%s.css" % (suffix, k)
            p  = pjoin        (self.prefix,  cn)
            fn = os.path.join (self.css_dir, cn)
            t  = first        (ts_and_obj) [0]
            with open (fn, "wb") as file :
                file.write (t.CSS)
            for t, obj in ts_and_obj :
                t.css_href = p
                yield p, t, obj
    # end def _create_css_cache

    @classmethod
    def Media_Filenames (cls, nav_root, include_templates = True) :
        T      = nav_root.Templateer
        result = set ()
        def _add (t) :
            if include_templates and t.source_path is not None :
                result.add (t.source_path)
            if t.media_path is not None :
                result.add (t.media_path)
        # end def _add

        for tn in nav_root.template_names :
            t = T.get_template (tn)
            if t.source_path :
                _add (t)
                for st in t.templates :
                    _add (st)
        for nav in nav_root.children_transitive :
            for t in nav.injected_templates :
                _add (t)
                for st in t.templates :
                    _add (st)
        return result
    # end def Media_Filenames

    def from_pickle_cargo (self, nav_root, cargo) :
        T            = nav_root.Templateer
        for p, tns in cargo.get ("css_map_p", {}).iteritems () :
            for tn in tns :
                T.get_template (tn).css_href = p
    # end def from_pickle_cargo

    def __str__ (self) :
        return "Template_Media_Cache (%r, %r)" % (self.css_dir, self.prefix)
    # end def __str__

# end class Template_Media_Cache

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Template_Media_Cache
