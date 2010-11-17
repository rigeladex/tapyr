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
#    29-Jan-2010 (CT) `get_template` changed to use `Template_Map`
#    19-Feb-2010 (CT) `error_405` added
#    14-May-2010 (MG) `dynamic_form` added
#    19-May-2010 (MG) `render_string` added
#     2-Aug-2010 (MG) `console` added
#    17-Aug-2010 (CT) `error_503` added
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
          , 405       : "html/error_405.jnj"
          , 500       : "html/error_500.jnj"
          , 503       : "html/error_503.jnj"
          }
        , account_activate             = "html/activate.jnj"
        , account_change_email         = "html/change_email.jnj"
        , account_change_password      = "html/change_password.jnj"
        , account_register             = "html/register.jnj"
        , account_reset_password       = "html/reset_password.jnj"
        , account_verify_new_email     = "email/verifiy_new_email.jnj"
        , account_verify_email         = "email/verifiy_new_email.jnj"
        , calendar                     = "html/calendar.jnj"
        , calendar_qx                  = "html/cal/wr.jnj"
        , calendar_day                 = "html/cal_day.jnj"
        , calendar_day_qx              = "html/cal/day.jnj"
        , calendar_week                = "html/cal_week.jnj"
        , console                      = "html/console.jnj"
        , default                      = "html/error.jnj"
        , dynamic_form                 = "html/dynamic_form.jnj"
        , e_type_admin                 = "html/e_type_admin.jnj"
        , e_type_aggregator            = "html/e_type_aggregator.jnj"
        , e_type_change                = "html/e_type_change.jnj"
        , gallery                      = "html/gallery.jnj"
        , login                        = "html/login.jnj"
        , photo                        = "html/photo.jnj"
        , regatta_registration         = "html/regatta_registration.jnj"
        , regatta_result               = "html/regatta_result.jnj"
        , regatta_result_teamrace      = "html/regatta_result_teamrace.jnj"
        , site_admin                   = "html/site_admin.jnj"
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
        return self.env.get_template (self.Template_Map.get (name, name))
    # end def get_template

    def render (self, template_or_name, context) :
        template = template_or_name
        if isinstance (template_or_name, basestring) :
            template = self.get_template (template_or_name)
        return template.render (context)
    # end def render

    def render_string (self, template_string, context) :
        return self.render (self.env.from_string (template_string), context)
    # end def render_string

# end class Templateer

if __name__ != "__main__" :
    JNJ._Export ("*")
### __END__ JNJ.Templateer
