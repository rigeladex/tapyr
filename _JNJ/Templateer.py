# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package JNJ.
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
#    JNJ.Templateer
#
# Purpose
#    Encapsulate Jinja template handling
#
# Revision Dates
#    14-Jan-2010 (CT) Creation
#    15-Jan-2010 (CT) `Error_Templates` added
#    18-Jan-2010 (CT) `get_std_template` added; s/Error_Templates/Template_Map/
#    ««revision-date»»···
#--

from   _JNJ               import JNJ
from   _TFL               import TFL

import _JNJ.Environment

import _TFL._Meta.Object

class Templateer (TFL.Meta.Object) :
    """Encapsulate Jinja template handling"""

    Context         = dict
    Template_Map    = dict \
        ( { 401       : "html/error_401.jnj"
          , 403       : "html/error_403.jnj"
          , 404       : "html/error_404.jnj"
          , 500       : "html/error_500.jnj"
          }
        , default       = "html/error.jnj"
        , e_type_admin  = "html/e_type_admin.jnj"
        , e_type_change = "html/e_type_change.jnj"
        , site_admin    = "html/site_admin.jnj"
        )

    def __init__ (self, * args, ** kw) :
        self.env = JNJ.Environment.HTML (* args, ** kw)
    # end def __init__

    def get_std_template (self, name) :
        if name in self.Template_Map :
            name = self.Template_Map [name]
        else :
            name = self.Template_Map ["default"]
        return self.env.get_template (name)
    # end def get_std_template

    def get_template (self, name) :
        return self.env.get_template (name)
    # end def get_template

    def render (self, template_or_name, context) :
        template = template_or_name
        if isinstance (template_or_name, basestring) :
            template = self.get_template (template_or_name)
        return template.render (context)
    # end def render

# end class Templateer

if __name__ != "__main__" :
    JNJ._Export ("*")
### __END__ JNJ.Templateer
