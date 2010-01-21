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
#    ««revision-date»»···
#--
from   _MOM                import MOM

from   _TFL                import TFL
from   _TFL._Babel.Extract import Existing_Translations

from    babel.util         import parse_encoding
from    babel.support      import Translations
import  os

def Add_Translations (encoding, config, app_type) :
    trans        = Existing_Translations (config.get ("ignore_packages"))
    translations = []
    for et in app_type.etypes.itervalues () :
        msg = et.ui_name
        if msg not in trans :
            translations.append ((0, None, msg, []))
        for prop_spec in et._Attributes, et._Predicates:
            for pn in prop_spec._own_names :
                prop = prop_spec._prop_dict [pn]
                msg  = getattr (prop, "ui_name", prop.name)
                if msg not in trans :
                    translations.append ((0, None, msg, []))
    return translations
# end def Add_Translations

def Extract (fobj, keywords, comment_tags, config) :
    d        = {}
    encoding = parse_encoding (fobj) or config.get \
        ("encoding", default = "iso-8859-1")
    execfile (fobj.name, globals (), d)
    return d ["main"] (encoding, config)
# end def Extract

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.Babel
