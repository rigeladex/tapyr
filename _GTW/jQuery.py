# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    jQuery
#
# Purpose
#    Definition of the javascript and CSS file if jQuery and jQuery UI should
#    be used.
#
# Revision Dates
#     1-May-2010 (MG) Creation
#     3-Aug-2010 (CT) `de_obfuscate_a` added
#     4-Aug-2010 (CT) `fix_a_nospam` factored
#    ««revision-date»»···
#--

from   _GTW import GTW
import _GTW.Media

if __debug__ :
    GTW.Script \
        ( src = "/media/GTW/js/jquery-1.4.2.js"
        , sort_key = -100  ## should be loaded first
        , name     = "jQuery"
        )
    GTW.Script (src = "/media/GTW/js/jquery-ui.js", name = "jQuery_UI")
else :
    GTW.Script \
        ( src = "/media/GTW/js/jquery-1.4.2.min.js"
        , sort_key = -100  ## should be loaded first
        , name     = "jQuery"
        )
    GTW.Script (src = "/media/GTW/js/jquery-ui-1.8.min.js", name = "jQuery_UI")
GTW.Script (src = "/media/GTW/js/jquery.gritter.js",    name = "jQuery_Gritter")

GTW.CSS_Link ("/media/GTW/css/jquery-ui-1.8.css", name = "jQuery_UI")
GTW.CSS_Link \
    ( "/media/GTW/css/jquery.gritter.css", "screen"
    , name = "jQuery_Gritter"
    )
GTW.JS_On_Ready \
    ( '$.gritter.Convert_Patagraphs_to_Gitter ("notifications");'
    , name = "jQuery_Gritter"
    )

GTW.Script      (src = "/media/GTW/js/GTW_util.js", name = "de_obfuscate_a")
GTW.JS_On_Ready ("$.GTW.fix_a_nospam ($);",         name = "de_obfuscate_a")

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.jQuery
