# -*- coding: iso-8859-15 -*-
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
#    26-Sep-2011 (MG) Creation (factored from GTW.NAV.Base.load_css, store_css)
#    21-Oct-2011 (MG) `_create_css_cache` creating of directory added
#    21-Oct-2011 (CT) Esthetics
#    22-Nov-2011 (MG) Use `sos.mkdir_p` instead of `sos.mkdir`
#    25-Nov-2011 (CT) Use `nav_root.template_iter` (major surgery)
#    ««revision-date»»···
#--

from   _GTW                   import GTW
import _GTW._NAV

from   _TFL                   import TFL
from   _TFL                   import sos
from   _TFL.predicate         import first

import _TFL._Meta.Object

import  hashlib
import  base64
from    posixpath import join as pjoin

class Template_Media_Cache (TFL.Meta.Object) :

    rank = 1000

    def __init__ (self, css_dir, prefix, clear_dir = False) :
        if not prefix.startswith ("/") :
            prefix     = "/%s" % (prefix, )
        self.css_dir   = css_dir
        self.prefix    = prefix
        self.clear_dir = clear_dir
    # end def __init__

    def as_pickle_cargo (self, nav_root) :
        if self.clear_dir :
            self._clear_dir ()
        css_map_t = TFL.mm_list ()
        css_map_p = {}
        for t in nav_root.template_iter () :
            self._add_to_css_map (t, css_map_t)
        for p, t in self._create_css_cache (css_map_t) :
            css_map_p [t.name] = p
        nav_root.Templateer.Template_Type.css_href_map = css_map_p
        return dict (css_map_p = css_map_p)
    # end def as_pickle_cargo

    def _add_to_css_map (self, t, css_map) :
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
                css_map [k].append   (t)
    # end def _add_to_css_map

    def _clear_dir (self) :
        for fod in sos.listdir_full (self.css_dir) :
            if sos.path.isdir (fod) :
                sos.rmdir  (fod, True)
            else :
                sos.unlink (fod)
    # end def _clear_dir

    def _create_css_cache (self, css_map) :
        if not sos.path.isdir (self.css_dir) :
            sos.mkdir_p (self.css_dir)
        for k, ts in css_map.iteritems () :
            cn = "%s.css" %    (k)
            p  = pjoin         (self.prefix,  cn)
            fn = sos.path.join (self.css_dir, cn)
            t  = ts [0]
            with open (fn, "wb") as file :
                file.write (t.CSS)
            for t in ts :
                yield p, t
    # end def _create_css_cache

    @classmethod
    def Media_Filenames (cls, nav_root, include_templates = True) :
        result = set ()
        def _add (ts) :
            for t in ts :
                if include_templates and t.source_path is not None :
                    result.add (t.source_path)
                if t.media_path is not None :
                    result.add (t.media_path)
        for t in nav_root.template_iter () :
            _add (t.templates)
        return result
    # end def Media_Filenames

    def from_pickle_cargo (self, nav_root, cargo) :
        css_map_p = cargo.get ("css_map_p", {})
        nav_root.Templateer.Template_Type.css_href_map = css_map_p
    # end def from_pickle_cargo

    def __str__ (self) :
        return "Template_Media_Cache (%r, %r)" % (self.css_dir, self.prefix)
    # end def __str__

# end class Template_Media_Cache

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Template_Media_Cache
