# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
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
#    GTW.Form.Javascript
#
# Purpose
#    Handle the javascriot code generation for forms
#
# Revision Dates
#    25-Feb-2010 (MG) Creation
#    27-Feb-2010 (MG) Cleanup
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL._Meta.M_Unique_If_Named

from   _GTW               import GTW
import _GTW._Form
import  random
import  json

class Form (TFL.Meta.Object) :
    """Handle the Form code generation for a form."""

    def __init__ (self, form) :
        self.form       = form
        self.inlines    = []
        self.completers = []
    # end def __init__

    @property
    def js_on_ready (self) :
        form           = self.form
        id             = getattr \
            (form, "form_name", str (random.randrange (1, 10000000)))
        form.css_class = " ".join ((getattr (self.form, "css_class", ""), id))
        result     = ["/* setup form `%s` */\n" % (id, )]
        completers = []
        for c, f in self.completers :
            completers.extend (c.js_on_ready (f))
        result.append ('$(".%s").GTW_Form\n' % (id, ))
        init    = dict \
            ( inlines    = [i.js_on_ready ()  for i      in self.inlines]
            , completers = completers
            )
        result.append ('  ( %s\n  );\n'% json.dumps (init))
        return result
    # end def js_on_ready

# end class Form´

class _Inline_ (TFL.Meta.Object) :
    """Base class for the different kind of inline forms"""

    allow_copy = False

    def __init__ (self, form, description) :
        self.form        = form
        self.description = description
        form.Form.javascript.inlines.append (self)
    # end def __init__

    def js_on_ready (self) :
        form   = self.form
        result = dict \
            ( prefix         = form.form_path_css
            , allow_copy     = self.allow_copy
            , instance_class = "inline-instance"
            )
        return result
    # end def js_on_ready

# end class _Inline_

class Attribute_Inline (_Inline_) :
    """A inline form for attributes"""

# end class Attribute_Inline

class Link_Inline (_Inline_) :
    """A inline form which models a link."""

    allow_copy = True

# end class Link_Inline

class _Completer_ (TFL.Meta.Object) :
    """Base class for autocompletion of form/parts of forms."""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    def attach (self, form) :
        form.Form.javascript.completers.append ((self, form))
    # end def attach

# end class _Completer_

if __name__ != "__main__" :
    GTW.Form._Export_Module ()
### __END__ GTW.Form.Javascript
