# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL._pyk2
#
# Purpose
#    Python2 specific implementation of TFL.pyk
#
# Revision Dates
#    16-Jun-2010 (CT) Creation
#     5-Jan-2011 (CT) `pickle` added
#    18-Apr-2012 (CT) Change `fprint` to encode `sep` and `end`, too
#    23-May-2013 (CT) Add `string_types`, `text_type`, `Classic_Class_Type`
#    23-May-2013 (CT) Add class decorator `adapt__bool__`
#    24-May-2013 (CT) Add `adapt__div__`, `adapt__str__`
#    24-May-2013 (CT) Add `iteritems`, `iterkeys`, `itervalues`, `xrange`
#    24-May-2013 (CT) Add `int_types`
#    25-May-2013 (CT) Add `new_instancemethod`, `izip`, `zip`
#    26-May-2013 (CT) Convert to class/instance to allow lazy imports
#     9-Oct-2013 (CT) Add `izip`
#    ««revision-date»»···
#--

import functools
import itertools
import sys

def lazy_property (fct) :
    name = fct.__name__
    @functools.wraps (fct)
    def _ (self) :
        try :
            result = self.__dict__ [name]
        except KeyError :
            result = self.__dict__ [name] = fct (self)
        return result
    return property (_)
# end def lazy_property

class _Pyk_ (object) :
    """Python2 specific implementation of TFL.pyk.

       Use a class instead of module-level definitions to allow lazy imports.
    """

    @staticmethod
    def adapt__bool__ (cls) :
        dct = cls.__dict__
        if "__bool__" in dct and "__nonzero__" not in dct :
            setattr (cls, "__nonzero__", dct ["__bool__"])
        return cls
    # end def adapt__bool__

    @staticmethod
    def adapt__div__ (cls) :
        dct = cls.__dict__
        if "__truediv__" in dct and "__div__" not in dct :
            cls.__div__ = cls.__truediv__
        if "__itruediv__" in dct and "__idiv__" not in dct :
            cls.__idiv__ = cls.__itruediv__
        if "__rtruediv__" in dct and "__rdiv__" not in dct :
            cls.__rdiv__ = cls.__rtruediv__
        return cls
    # end def adapt__div__

    @staticmethod
    def adapt__str__ (cls) :
        dct = cls.__dict__
        if "__str__" in dct and "__unicode__" not in dct :
            from _TFL import TFL
            cls.__unicode__ = cls.__str__
            cls.__str__     = lambda s : TFL.I18N.encode_o (s.__unicode__ ())
        return cls
    # end def adapt__str__

    @lazy_property
    def Classic_Class_Type (self) :
        import types
        return types.ClassType
    # end def Classic_Class_Type

    @staticmethod
    def fprint (* values, ** kw) :
        """print(value, ..., sep=' ', end='\\n', file=sys.stdout)

           Prints the values to a stream, or to sys.stdout by default.
           Optional keyword arguments:
           file: a file-like object (stream); defaults to the current sys.stdout.
           sep:  string inserted between values, default a space.
           end:  string appended after the last value, default a newline.
        """
        from   _TFL.User_Config import user_config
        def _convert (v, encoding) :
            if not isinstance (v, basestring) :
                v = unicode (v)
            if isinstance (v, unicode) :
                v = v.encode (encoding, "replace")
            return v
        file = kw.pop ("file", None)
        if file is None :
            file = sys.stdout
        enc  = user_config.output_encoding
        sep  = _convert (kw.pop ("sep",  " "),  enc)
        end  = _convert (kw.pop ("end",  "\n"), enc)
        txt  = sep.join (_convert (v, enc) for v in values)
        file.write (txt + end)
    # end def fprint

    int_types = (int, long)
    izip      = itertools.izip

    @staticmethod
    def iteritems (dct) :
        return dct.iteritems ()
    # end def iteritems

    @staticmethod
    def iterkeys (dct) :
        return dct.iterkeys ()
    # end def iterkeys

    @staticmethod
    def itervalues (dct) :
        return dct.itervalues ()
    # end def itervalues

    @lazy_property
    def izip (self) :
        import itertools
        return itertools.izip
    # end def izip

    long_types = (long, )

    @lazy_property
    def new_instancemethod (self) :
        import new
        return new.instancemethod
    # end def new_instancemethod

    @lazy_property
    def pickle (self) :
        import cPickle
        return cPickle
    # end def pickle

    @lazy_property
    def StringIO (self) :
        import cStringIO
        return cStringIO.StringIO
    # end def StringIO

    string_types = (str, unicode)
    text_type    = unicode
    unichr       = unichr
    xrange       = staticmethod (xrange)
    zip          = staticmethod (zip)

# end class _Pyk_

pyk = _Pyk_ ()

### __END__ TFL._pyk2
