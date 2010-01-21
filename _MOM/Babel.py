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
#    ««revision-date»»···
#--
from   _TFL           import TFL
from   _TFL.Babel     import Translations
from   _MOM           import MOM
import _MOM.App_Type

from    babel.util    import parse_encoding
import  os

def Add_Translations (encoding, options, app_type) :
    trans = Translations.load_files \
        (TFL.I18N.save_eval (options.get ("message_catalogs"), encoding))
    translations = []
    for et in app_type.etypes.itervalues () :
        msg = et.ui_name
        if not (trans and trans.exists (msg)) :
            translations.append ((0, None, msg, []))
        for prop_spec in et._Attributes, et._Predicates:
            for pn in prop_spec._own_names :
                prop = prop_spec._prop_dict [pn]
                msg  = getattr (prop, "ui_name", prop.name)
                if not (trans and trans.exists (msg)) :
                    translations.append ((0, None, msg, []))
    return translations
# end def Add_Translations

def extract_mom (fobj, keywords, comment_tags, options) :
    d        = {}
    encoding = parse_encoding (fobj) or options.get ("encoding", "iso-8859-1")
    execfile (fobj.name, globals (), d)
    return d ["main"] (encoding, options)
# end def extract_mom

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.Babel
