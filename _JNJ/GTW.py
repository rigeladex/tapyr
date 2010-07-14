# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    JNJ.GTW
#
# Purpose
#    Provide additional global functions for Jinja templates
#
# Revision Dates
#    29-Dec-2009 (CT) Creation
#    13-Jan-2010 (CT) Converted to class; `call_macro` added;
#                     `_T` and `_Tn` added to class `GTW`
#    25-Jan-2010 (MG) `_T` and `_Tn` need to be static methods
#    27-Jan-2010 (CT) `Getter`, `now`, and `sorted` added
#    17-Feb-2010 (CT) `email_uri`, `obfuscated`, `tel_uri`, and `uri` added
#    23-Feb-2010 (CT) `pjoin` added
#    24-Feb-2010 (CT) `log_stdout` added
#    10-Mar-2010 (CT) `zip` added
#     3-May-2010 (MG) `call_macro`: `widget_type` added
#     5-May-2010 (MG) `render_fofi_widget` added
#     5-May-2010 (MG) `default_render_mode` used
#     5-May-2010 (MG) `render_mode` added
#     6-May-2010 (MG) `render_fofi_widget` exception handling improoved
#    ««revision-date»»···
#--

from   _JNJ               import JNJ
from   _TFL               import TFL

from   _GTW               import HTML

import _JNJ.Environment

import _TFL._Meta.Object

import _TFL.Accessor
from   _TFL               import sos
from   _TFL.I18N          import _, _T, _Tn

class GTW (TFL.Meta.Object) :
    """Provide additional global functions for Jinja templates."""

    from jinja2.runtime import Undefined

    def __init__ (self, env) :
        self.env               = env
        self.render_mode_stack = []
    # end def __init__

    def call_macro (self, macro_name, * _args, ** _kw) :
        """Call macro named by `macro_name` passing `* _args, ** _kw`."""
        templ_name  = _kw.pop ("templ_name",  None)
        widget_type = _kw.pop ("widget_type", None)
        try :
            macro  = self.get_macro (macro_name, templ_name, widget_type)
        except ValueError :
            print repr ((macro_name, templ_name, _args, _kw))
            raise
        return macro (* _args, ** _kw)
    # end def call_macro

    def email_uri (self, email, text = None, ** kw) :
        """Returns a telephone URI for `phone_number`.

           http://tools.ietf.org/html/rfc3966
        """
        return self.uri (scheme = "mailto", uri = email, text = text, ** kw)
    # end def email_uri

    def firstof (self, * args) :
        if len (args) == 1 and isinstance (args [0], (tuple, list)) :
            args = args [0]
        for a in args :
            if not (a is None or isinstance (a, self.Undefined)) :
                return a
    # end def firstof

    def get_macro (self, macro_name, templ_name = None, widget_type = None) :
        """Return macro `macro_name` from template `templ_name`."""
        if widget_type :
            macro_name = getattr (macro_name, widget_type)
        if not isinstance (macro_name, basestring) :
            macro_name = str (macro_name)
        if templ_name is None :
            templ_name, macro_name = \
                (p.strip () for p in macro_name.split (",", 1))
        template = self.env.get_template (templ_name)
        return getattr (template.module, macro_name)
    # end def get_macro

    Getter     = TFL.Getter

    def log_stdout (self, text) :
        print text
        return ""
    # end def log_stdout

    def now (self, format = "%Y/%m/%d") :
        from datetime import datetime
        result = datetime.now ()
        return result.strftime (format)
    # end def now

    obfuscated = staticmethod (HTML.obfuscated)
    pjoin      = staticmethod (sos.path.join)

    def render_fofi_widget (self, fofi, widget, * args, ** kw) :
        pushed = False
        obj_render_mode = getattr (fofi, "render_mode", None)
        kw_render_mode  = kw.pop  ("render_mode",       None)
        if obj_render_mode :
            pushed  = True
            self.render_mode_stack.append (obj_render_mode)
        elif kw_render_mode :
            pushed  = True
            self.render_mode_stack.append (kw_render_mode)
        elif not self.render_mode_stack :
            pushed  = True
            self.render_mode_stack.append (fofi.default_render_mode)
        render_mode = self.render_mode_stack [-1]
        try :
            try :
                mode_desc   = fofi.render_mode_description [render_mode]
            except ValueError :
                raise ValueError \
                    ("%r does not support render mode %r" % (fofi, render_mode))
            result      = self.call_macro \
                (getattr (mode_desc, widget), * args, ** kw)
            return result
        finally :
            if pushed :
                self.render_mode_stack.pop ()
    # end def render_fofi_widget

    @TFL.Meta.Once_Property
    def render_mode (self) :
        return self.render_mode_stack and self.render_mode_stack [-1]
    # end def render_mode

    sorted     = staticmethod (sorted)

    def tel_uri (self, phone_number, text = None, ** kw) :
        """Returns a telephone URI for `phone_number`.

           http://tools.ietf.org/html/rfc3966
        """
        return self.uri (scheme = "tel", uri = phone_number, text = text, ** kw)
    # end def tel_uri

    def uri (self, scheme, uri, text = None, ** kw) :
        obfuscate = kw.pop ("obfuscate", False)
        if text is None :
            text = uri
        attrs = ['href="%s:%s"' % (scheme, uri)]
        for k, v in kw.iteritems () :
            attrs.append ('%s="%s"' % (k, v))
        attrs = " ".join (sorted (attrs))
        result = u"""<a %(attrs)s>%(text)s</a>""" % locals ()
        if obfuscate :
            scheme_desc = _Tn (HTML.scheme_map.get (scheme, scheme))
            result = "".join \
                (( self.obfuscated (result)
                 , HTML._obfuscation_format_ns
                   % (_T ("Need Javascript for displaying"), scheme_desc, text)
                ))
        return result
    # end def uri

    zip  = staticmethod (zip)
    _T   = staticmethod (_T)
    _Tn  = staticmethod (_Tn)

# end class GTW

if __name__ != "__main__" :
    JNJ._Export ("GTW")
### __END__ JNJ.GTW
