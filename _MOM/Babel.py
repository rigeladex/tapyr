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
#    ««revision-date»»···
#--
from   _TFL.Babel     import Translations
from   _MOM           import MOM
import _MOM.App_Type

from    babel.util    import parse_encoding
import  os

def extract_mom (fobj, keywords, comment_tags, options) :
    d = {}
    execfile (fobj.name, globals (), d)
    app_type = d.get ("app_type")
    if app_type :
        encoding = \
            parse_encoding (fobj) or options.get ("encoding", "iso-8859-1")
        trans = Translations.load_files \
            (options.get ("message_catalogs"), encoding)
        for et in app_type.etypes.itervalues () :
            msg = et.ui_name
            if not (trans and trans.exists (msg)) :
                yield 0, None, msg, []
            msg = et.__doc__.strip ()
            if not (trans and trans.exists (msg)) :
                yield 0, None, msg, []
            for spec, dn in ( (et._Attributes, "_attr_dict")
                            , (et._Predicates, "_pred_dict")
                            ) :
                d = getattr (spec, dn)
                for pn in spec._own_names :
                    prop = d [pn]
                    msg  = getattr (prop, "ui_name", prop.name)
                    if not (trans and trans.exists (msg)) :
                        yield 0, None, msg, []
                    msg = (prop.__doc__ or "").strip ()
                    if msg and not (trans and trans.exists (msg)) :
                        yield 0, None, msg, []
            ### XXX add special role names like address, phone, person, ...
# end def extract_mom

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Babel
