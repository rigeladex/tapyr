# -*- coding: utf-8 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Text_Translation_Cacher
#
# Purpose
#    Provide caching for text translations
#
# Revision Dates
#    14-Jun-2006 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL import TFL
import _TFL._Meta.Object

class Text_Translation_Cacher (TFL.Meta.Object) :
    """Provide caching for text translations.

       >>> ttc = Text_Translation_Cacher (
       ...     dict (foo = "bar", bar = "baz", qux = "hu?").get)
       >>> sorted (ttc._cache.items ())
       []
       >>> ttc ("wibble")
       'wibble'
       >>> sorted (ttc._cache.items ())
       [('wibble', 'wibble')]
       >>> ttc ("foo")
       'bar'
       >>> sorted (ttc._cache.items ())
       [('foo', 'bar'), ('wibble', 'wibble')]
       >>> ttc ("bar")
       'baz'
       >>> sorted (ttc._cache.items ())
       [('bar', 'baz'), ('foo', 'bar'), ('wibble', 'wibble')]
       >>> ttc ("42")
       '42'
       >>> sorted (ttc._cache.items ())
       [('42', '42'), ('bar', 'baz'), ('foo', 'bar'), ('wibble', 'wibble')]
    """

    def __init__ (self, translator = None) :
        if translator is not None :
            self.translator = translator
        self._cache = {}
    # end def __init__

    def __call__ (self, text) :
        cache  = self._cache
        result = cache.get (text)
        if result is None :
            t = self.translator (text)
            if t is None :
                t = text
            result = cache [text] = t
        return result
    # end def __call__

# end class Text_Translation_Cacher

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Text_Translation_Cacher
