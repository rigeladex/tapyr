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
#    02-Mar-2010 (MG) `Multi_Completer` moved in here
#     3-May-2010 (MG) New form handling implemented
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
        if self.completers or self.inlines :
            form           = self.form
            et_man         = getattr (form, "et_man", None)
            if et_man :
                id         = et_man.type_name.replace (".", "_")
            else :
                id         = str (random.randrange (1, 10000000))
            form.css_class = " ".join \
                ((getattr (self.form, "css_class", ""), id))
            result     = ["/* setup form `%s` */\n" % (id, )]
            completers = []
            for c, f, rn in self.completers :
                completers.extend (c.js_on_ready (f, rn))
            result.append ('$(".%s").GTW_Form\n' % (id, ))
            init    = dict \
                ( inlines    = [i.js_on_ready ()  for i      in self.inlines]
                , completers = completers
                )
            result.append ('  ( %s\n  );\n'% json.dumps (init))
            return result
        return ()
    # end def js_on_ready

# end class Form

class _Inline_ (TFL.Meta.Object) :
    """Base class for the different kind of inline forms"""

    buttons          = ("rename", "delete", "clear")
    initial_disabled = True

    def __init__ (self, form, description, ** kw) :
        self.form        = form
        self.description = description
        form.javascript.inlines.append (self)
        self.__dict__.update (kw)
    # end def __init__

    def js_on_ready (self) :
        form   = self.form
        result = dict \
            ( prefix           = form.form_name
            , buttons          = self.buttons
            , instance_class   = "inline-instance"
            , initial_disabled = self.initial_disabled
            )
        return result
    # end def js_on_ready

# end class _Inline_

class Attribute_Inline (_Inline_) :
    """A inline form for attributes"""

# end class Attribute_Inline

class Link_Inline (_Inline_) :
    """A inline form which models a link."""

    buttons = ("rename", "delete", "clear", "copy")

# end class Link_Inline

class _Completer_ (TFL.Meta.Object) :
    """Base class for autocompletion of form/parts of forms."""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    def attach (self, form, role_name = None, multi_completer = None) :
        form.javascript.completers.append ((self, form, role_name))
        if multi_completer :
            multi_completer._completers [self.trigger] = self
    # end def attach

# end class _Completer_

class Multi_Completer (_Completer_) :
    """Multiple completers for one inline form"""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    def __init__ (self, root = None, ** completers) :
        self.root        = root
        self.name        = completers.pop ("name", None)
        self._completers = completers
    # end def __init__

    def complete (self, * args, ** kw) :
        return self.root.complete (* args, ** kw)
    # end def complete

    def js_on_ready (self, form, rn) :
        result = []
        if self.root :
            result.extend (self.root.js_on_ready (form, rn))
        for c in self._completers.itervalues () :
            result.extend (c.js_on_ready (form, rn))
        return result
    # end def js_on_ready

    def suggestions (self, * args, ** kw) :
        return self.root.suggestions (* args, ** kw)
    # end def suggestions

    def __getattr__ (self, name) :
        try :
            return self._completers [name]
        except IndexError :
            raise AttributeError (name)
    # end def __getattr__

# end class Multi_Completer

if __name__ != "__main__" :
    GTW.Form._Export_Module ()
### __END__ GTW.Form.Javascript
