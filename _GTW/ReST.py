# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    GTW.ReST
#
# Purpose
#    Conversion of re-structured text markup to HTML
#
# Revision Dates
#    25-Jan-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW               import GTW
from   _TFL               import TFL

def to_html (text, encoding = "utf8", language = "en") :
    """Convert `text` from re-structured text markup to HTML."""
    from docutils.core import publish_parts
    import _ReST.Roles
    settings = dict \
        ( base_section                  = "0"
        , input_encoding                = "unicode"
        , output_encoding               = encoding
        , output_encoding_error_handler = "xmlcharrefreplace"
        , language_code                 = language
        , cloak_email_addresses         = False
        )
    parts    = publish_parts \
        ( source             = unicode (text)
        , writer_name        = "html4css1"
        , settings_overrides = settings
        )
    return parts ["fragment"]
# end def to_html

if __name__ != "__main__" :
    GTW._Export_Module ()
### __END__ GTW.ReST
