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
#    29-Dec-2010 (CT) `Template` added and used
#    ««revision-date»»···
#--

from   _JNJ               import JNJ
from   _TFL               import TFL

import _JNJ.Environment

import _TFL._Meta.Object

class Template (TFL.Meta.Object) :
    """Describe a Jinja template."""

    Map           = {}

    _css_fragment = None
    _css_path     = None

    def __init__ (self, name, path, css_fragment_name = None) :
        assert name not in self.Map, name
        self.name              = name
        self.path              = path
        self.css_fragment_name = css_fragment_name
        self.Map [name]        = self
    # end def __init__

    def css_fragment (self, env) :
        if self._css_fragment is None :
            self._load_css (env)
        return self._css_fragment
    # end def css_fragment

    def css_path (self, env) :
        if self._css_path is None :
            self._load_css (env)
        return self._css_path
    # end def css_path

    def _load_css (self, env) :
        from jinja2.exceptions import TemplateNotFound
        f_path = self.css_fragment_name
        if f_path is None :
            f_path = "%s.css" % (self.path, )
        try :
            source, path, _ = env.loader.get_source (env, f_path)
        except TemplateNotFound :
            pass
        else :
            self._css_fragment = source
            self._css_path     = path
    # end def _load_css

# end class Template

Template (401,                            "html/error_401.jnj")
Template (403,                            "html/error_403.jnj")
Template (404,                            "html/error_404.jnj")
Template (405,                            "html/error_405.jnj")
Template (500,                            "html/error_500.jnj")
Template (503,                            "html/error_503.jnj")
Template ("account_activate",             "html/activate.jnj")
Template ("account_change_email",         "html/change_email.jnj")
Template ("account_change_password",      "html/change_password.jnj")
Template ("account_register",             "html/register.jnj")
Template ("account_reset_password",       "html/reset_password.jnj")
Template ("account_reset_password_email", "email/reset_password.jnj")
Template ("account_verify_new_email",     "email/verify_new_email.jnj")
Template ("account_verify_email",         "email/verify_new_email.jnj")
Template ("calendar",                     "html/calendar.jnj")
Template ("calendar_qx",                  "html/cal/wr.jnj")
Template ("calendar_day",                 "html/cal_day.jnj")
Template ("calendar_day_qx",              "html/cal/day.jnj")
Template ("calendar_week",                "html/cal_week.jnj")
Template ("console",                      "html/console.jnj")
Template ("default",                      "html/error.jnj")
Template ("dynamic_form",                 "html/dynamic_form.jnj")
Template ("e_type_admin",                 "html/e_type_admin.jnj")
Template ("e_type_aggregator",            "html/e_type_aggregator.jnj")
Template ("e_type_change",                "html/e_type_change.jnj")
Template ("gallery",                      "html/gallery.jnj")
Template ("login",                        "html/login.jnj")
Template ("photo",                        "html/photo.jnj")
Template ("regatta_calendar",             "html/regatta_calendar.jnj")
Template ("regatta_registration",         "html/regatta_registration.jnj")
Template ("regatta_result",               "html/regatta_result.jnj")
Template ("regatta_result_teamrace",      "html/regatta_result_teamrace.jnj")
Template ("site_admin",                   "html/site_admin.jnj")

class Templateer (TFL.Meta.Object) :
    """Encapsulate Jinja template handling"""

    Context         = dict
    Template_Map    = Template.Map

    def __init__ (self, * args, ** kw) :
        self.env = JNJ.Environment.HTML (* args, ** kw)
    # end def __init__

    def get_std_template (self, name) :
        if name in self.Template_Map :
            template = self.Template_Map [name]
        else :
            template = self.Template_Map ["default"]
        return self.env.get_template (template.path)
    # end def get_std_template

    def get_template (self, name) :
        if name in self.Template_Map :
            path = self.Template_Map [name].path
        else :
            path = name
        return self.env.get_template (path)
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
