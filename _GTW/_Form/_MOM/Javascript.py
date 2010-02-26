# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
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
#    GTW.Form.MOM.Javascript
#
# Purpose
#    MOM specific javascript code generation
#
# Revision Dates
#    26-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW                       import GTW
import _GTW._Form.Javascript      as     Javascript
import _GTW._Form._MOM
from   _MOM.import_MOM            import Q

class Field_Completer (Javascript._Completer_) :
    """Complete parts of a form."""

# end class Field_Completer

class MOM_Completer (Javascript._Completer_) :
    """Completion for the whole form for an MOM entity."""

    def js_on_ready (self, form) :
        bname, fname = form.form_path.split ("/", 1)
        url_format   = "%s/%s/%%s/%s"  % (self.options ["prefix"], bname, fname)
        return dict \
            ( field_prefix = form.prefix
            , triggers     = self.triggers
            , type         = self.__class__.__name__
            , suggest_url  = url_format % ("complete", )
            , complete_url = url_format % ("completed", )
            )
    # end def js_on_ready

    def complete (self, form, handler, lid) :
        et_man   = form.et_man
        try :
            obj  = et_man.pid_query (et_man.pid_from_lid (lid))
        except IndexError, exc :
            error = (_T("%s `%s` existiert nicht!") % (_T(et_man.ui_name), id))
            raise self.top.HTTP.Error_404 (request.path, error)
        form = form (obj)
        return handler.json \
            (dict ((f.name, form.get_raw (f)) for f in form.fields))
    # end def complete

    def suggestions (self, form, handler, args) :
        et_man   = form.et_man
        trigger  = getattr (et_man._etype, args.pop ("TRIGGER_FIELD"))
        filter   = tuple \
            (    getattr (Q, k).STARTSWITH (v)
            for (k, v) in et_man.cooked_attrs (args).iteritems ()
            )
        return handler.json \
            ( [   dict
                    ( lid   = c.lid
                    , value = trigger.get_raw (c)
                    , label = c.ui_display
                    )
              for c in et_man.query ().filter (* filter).distinct ()
              ]
            )
    # end def suggestions

# end class MOM_Completer

if __name__ != "__main__" :
    GTW.Form.MOM._Export_Module ()
### __END__ GTW.Form.MOM.Javascript
