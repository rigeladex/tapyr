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
#    22-Feb-2010 (CT) `langs` and `lang_flag` added
#    ««revision-date»»···
#--

from   _JNJ               import JNJ
from   _TFL               import TFL

from   _GTW               import HTML

import _JNJ.Environment

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Accessor
from   _TFL.I18N          import _, _T, _Tn

class GTW (TFL.Meta.Object) :
    """Provide additional global functions for Jinja templates."""

    from jinja2.runtime import Undefined

    _lang_map = dict \
        ( en  = "us"
        )

    def __init__ (self, env) :
        self.env = env
    # end def __init__

    def call_macro (self, macro_name, * _args, ** _kw) :
        """Call macro named by `macro_name` passing `* _args, ** _kw`."""
        templ_name = _kw.pop   ("templ_name", None)
        try :
            macro  = self.get_macro (macro_name, templ_name)
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

    def get_macro (self, macro_name, templ_name = None) :
        """Return macro `macro_name` from template `templ_name`."""
        if not isinstance (macro_name, basestring) :
            macro_name = str (macro_name)
        if templ_name is None :
            templ_name, macro_name = \
                (p.strip () for p in macro_name.split (",", 1))
        template = self.env.get_template (templ_name)
        return getattr (template.module, macro_name)
    # end def get_macro

    Getter     = TFL.Getter

    def lang_flag (self, lang) :
        if isinstance (lang, basestring) :
            lang = (lang, )
        map = self._lang_map
        for l in lang :
            k      = map.get (l, l).lower ()
            flag   = "/media/GTW/icons/flags/%s.png" % (k, )
            exists = True # XXX # GTW.static_map.exists (flag)
            if exists :
                return flag
    # end def lang_flag

    @Once_Property
    def langs (self) :
        return tuple (l for l in TFL.I18N.Config.Languages if l)
    # end def langs

    def now (self, format = "%Y/%m/%d") :
        from datetime import datetime
        result = datetime.now ()
        return result.strftime (format)
    # end def now

    obfuscated = staticmethod (HTML.obfuscated)

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

    _T   = staticmethod (_T)
    _Tn  = staticmethod (_Tn)

# end class GTW

if __name__ != "__main__" :
    JNJ._Export ("GTW")
### __END__ JNJ.GTW
