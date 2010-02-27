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
#    27-Feb-2010 (MG) `Field_Completer` added, `_MOM_Completer_` factored
#    ««revision-date»»···
#--
from   _TFL               import TFL
from   _TFL.predicate     import uniq
import _TFL._Meta.Object
import _TFL._Meta.M_Unique_If_Named

from   _GTW                       import GTW
import _GTW._Form.Javascript      as     Javascript
import _GTW._Form._MOM
from   _MOM.import_MOM            import Q

class _MOM_Completer_ (GTW.Form.Javascript._Completer_) :
    """Base class for the MOM Completers"""

    def complete (self, form, handler, lid) :
        et_man   = form.et_man
        try :
            obj  = et_man.pid_query (et_man.pid_from_lid (lid))
        except IndexError, exc :
            error = (_T("%s `%s` existiert nicht!") % (_T(et_man.ui_name), id))
            raise self.top.HTTP.Error_404 (request.path, error)
        return self._send_result (form, handler, obj)
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
                    , label = self.ui_display (c)
                    )
              for c in et_man.query ().filter (* filter).distinct ()
              ]
            )
    # end def suggestions

# end class _MOM_Completer_

class Field_Completer (_MOM_Completer_) :
    """Complete parts of a form."""

    options = dict \
        ( min_chars = 2
        )

    def __init__ ( self, trigger, fields
                 , prefix       = "/Admin"
                 , separator    = ", "
                 , ** kw
                 ) :
        self.trigger     = trigger
        self.prefix    = prefix
        self.separator = separator
        self.options   = dict (self.options, ** kw)
        self.fields    = fields
    # end def __init__

    def _send_result (self, form_cls, handler, obj) :
        attributes = obj.attributes
        result     = dict \
            ((f, attributes [f].get_raw (obj)) for f in self.fields)
        return handler.json (result)
    # end def _send_result

    def js_on_ready (self, form) :
        bname, fname = form.form_path.split ("/", 1)
        url_format   = "%s/%s/%%s/%s/%s" \
            % (self.prefix, bname, fname, self.trigger)
        result = \
            ( dict
                ( field_prefix = form.prefix
                , triggers     =
                    {self.trigger : dict (self.options, fields = self.fields)}
                , type         = self.__class__.__name__
                , suggest_url  = url_format % ("complete", )
                , complete_url = url_format % ("completed", )
                )
            ,
            )
        return result
    # end def js_on_ready

    def ui_display (self, obj) :
        attributes = obj.attributes
        result     = [attributes [f].get_raw (obj) for f in self.fields]
        return self.separator.join (p for p in result if p)
    # end def ui_display

# end class Field_Completer

class Completer (_MOM_Completer_) :
    """Completion for the whole form for an MOM entity."""

    ### Can be overriden by `__init__` arguments
    options   = dict \
        ( fields       = ()
        , min_chars    = 3
        , prefix       = "/Admin"
        )
    _ignore_options = set (("name", "prefix"))

    def __init__ (self, triggers, ** kw) :
        self._triggers = triggers
        self.options   = dict (self.options, ** kw)
    # end def __init__

    def js_on_ready (self, form) :
        bname, fname = form.form_path.split ("/", 1)
        url_format   = "%s/%s/%%s/%s"  % (self.options ["prefix"], bname, fname)
        return \
            ( dict
                ( field_prefix = form.prefix
                , triggers     = self.triggers
                , type         = self.__class__.__name__
                , suggest_url  = url_format % ("complete", )
                , complete_url = url_format % ("completed", )
                )
            ,
            )
    # end def js_on_ready

    def _send_result (self, form_cls, handler, obj) :
        form = form_cls (obj)
        return handler.json \
            (dict ((f.name, form.get_raw (f)) for f in form.fields))
    # end def _send_result

    @property
    def triggers (self) :
        result = {}
        for k, v in self._triggers.iteritems () :
            result [k] = d = v.copy ()
            for k, v in self.options.iteritems () :
                if k not in self._ignore_options :
                    d.setdefault (k, v)
        return result
    # end def triggers

    def ui_display (self, obj) :
        return obj.ui_display
    # end def ui_display

# end class Completer

class Multi_Completer (GTW.Form.Javascript._Completer_) :
    """Multiple completers for one inline form"""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    def __init__ (self, root, ** completers) :
        self.root = root
        self.name = completers.pop ("name", None)
        self._completers = completers
    # end def __init__

    def complete (self, * args, ** kw) :
        return self.root.complete (* args, ** kw)
    # end def complete

    def js_on_ready (self, form) :
        result = list (self.root.js_on_ready (form))
        for c in self._completers.itervalues () :
            result.extend (c.js_on_ready (form))
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
    GTW.Form.MOM._Export_Module ()
### __END__ GTW.Form.MOM.Javascript
