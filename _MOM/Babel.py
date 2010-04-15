# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.
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
#    MOM.Babel
#
# Purpose
#    Special extractor which adds attribute names XXX
#
# Revision Dates
#    20-Jan-2010 (MG) Creation
#    21-Jan-2010 (MG) No need to add doc strings because they are found by
#                     the extended python extractor
#    21-Jan-2010 (MG) Use new `TFL.Babel.Existing_Translations`
#    25-Jan-2010 (MG) Add doctrings to translations
#    27-Feb-2010 (MG) Add the filename of the e-type to the translation
#    23-Mar-2010 (MG) Plural added for `ui_name`
#    15-Apr-2010 (MG) Don't create plurals for attributes, hide non-user
#                     attributes and names starings with `_` from the
#                     translation
#    ««revision-date»»···
#--
from   _MOM                import MOM

from   _TFL                import TFL
import _TFL.normalized_indent
from    babel.util         import parse_encoding
from    babel.support      import Translations
import  os

def Add_Translations (encoding, config, method, app_type) :
    trans        = config.get ("loaded_translations", method)
    translations = []

    def _add_object ( obj, default_name, add_doc_string, filename
                    , plural = False
                    ) :
        msg  = getattr (obj, "ui_name", default_name)
        kind = "_T"
        if msg.startswith ("_") :
            ### skip keys which start with an underscore
            return
        if plural :
            ui_plur = "%s%s" % (msg, "s" if msg [-1] != "s" else "es")
            msg     = (msg, ui_plur)
            kind    = "_Tn"
        if msg not in trans :
            translations.append ((0, kind, msg, [], filename))
        doc_string = TFL.normalized_indent (obj.__doc__ or "")
        if add_doc_string and doc_string and doc_string not in trans :
            translations.append ((0, "_T", doc_string, [], filename))
    # end def _add_object

    for et in app_type.etypes.itervalues () :
        filename = et.__module__
        _add_object (et, et.ui_name, False, filename, True)
        for prop_spec, inst_cls in ( (et._Attributes, MOM.Attr._User_)
                                   , (et._Predicates, None)
                                   ) :
            for pn in prop_spec._own_names :
                prop = prop_spec._prop_dict [pn]
                if not inst_cls or isinstance (prop, inst_cls) :
                    _add_object (prop, prop.name, True, filename)
    return translations
# end def Add_Translations


def Extract (fobj, keywords, comment_tags, config, method) :
    d        = {}
    encoding = parse_encoding (fobj) or config.get \
        ("encoding", default = "iso-8859-1")
    exec (fobj.read (), globals (), d)
    return d ["main"] (encoding, config, method)
# end def Extract

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.Babel
