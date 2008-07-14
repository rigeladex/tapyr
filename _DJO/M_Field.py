# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    DJO.M_Field
#
# Purpose
#    Subclass Django models/field classes to add useful behavior
#
# Revision Dates
#    14-Jul-2008 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                               import TFL
import _TFL._Meta.M_Class

from   _DJO                               import DJO

from   django.db                          import models as DM
from   django.utils.translation           import gettext_lazy as _

import datetime

class M_Field (TFL.Meta.M_Class, DM.Field.__class__) :
    """Meta class for model fields with support for `.__super` and
       `_real_name`.
    """
# end class M_Field

class _DJO_Field_ (DM.Field) :

    __metaclass__ = M_Field
    _real_name    = "Field"

    output_format = "%s"
    Widget        = None

    def __init__ (self, * args, ** kw) :
        if "output_format" in kw :
            self.output_format = kw.pop ("output_format")
        if "Widget" in kw :
            self.Widget        = kw.pop ("Widget")
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def as_string (self, value) :
        if value is not None :
            return self.output_format % (s, )
        return ""
    # end def as_string

    def formfield (self, ** kw) :
        defaults = dict ()
        if self.Widget :
            defaults.update (widget = self.Widget)
        defaults.update (kw)
        return self.__super.formfield (** defaults)
    # end def formfield

    def from_string (self, s) :
        if s is not None :
            return self._from_string (s)
    # end def from_string

    def _from_string (self, s) :
        return s
    # end def _from_string

Field = _DJO_Field_ # end class

class Auto (Field, DM.AutoField) :

    def _from_string (self, s) :
        return int (s)
    # end def _from_string

# end class Auto

class Boolean (Field, DM.BooleanField) :

    def _from_string (self, s) :
        return s == "True"
    # end def _from_string

# end class Boolean

class Char (Field, DM.CharField) :
    pass
# end class Char

class _Date_ (Field) :

    input_formats  = ("%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y")
    _output_format = None
    _tuple_off     = 0

    def __init__ (self, * args, ** kw) :
        if "input_formats" in kw :
            self.input_formats  = kw.pop ("input_formats")
        if "output_format" in kw :
            self._output_format = kw.pop ("output_format")
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    @property
    def output_format (self) :
        return self._output_format or self.input_formats [0]
    # end def output_format

    def as_string (self, value) :
        try :
            value.strftime
        except AttributeError :
            result = value
        else :
            result = value.strftime (self.output_format)
        return result
    # end def as_string

    def _from_string (self, s) :
        for f in self.input_formats :
            try :
                result = time.strptime (s, f)
            except ValueError :
                pass
            else :
                break
        else :
            raise ValueError, s
        return self._DT_Type (* result [self._tuple_off:self._tuple_len])
    # end def _from_string

    def formfield (self, ** kw) :
        defaults = dict \
            ( format        = self.output_format ### XXX ???
            , input_formats = self.input_formats
            )
        defaults.update (kw)
        return self.__super.formfield (** defaults)
    # end def formfield

# end class _Date_

class Date (_Date_, DM.DateField) :

    _tuple_len     = 3
    _DT_Type       = datetime.date

# end class Date

class Decimal (Field, DM.DecimalField) :

    def as_string (self, value) :
        if value is not None :
            return u"%.*f" % (self.decimal_places, value)
        return ""
    # end def as_string

    def _from_string (self, s) :
        from decimal import Decimal
        return Decimal (s)
    # end def _from_string

# end class Decimal

class Email (Field, DM.EmailField) :
    pass
# end class Email

class File (Field, DM.FileField) :
    pass
# end class File

class File_Path (Field, DM.FilePathField) :
    pass
# end class File_Path

class Float (Field, DM.FieldField) :

    output_format = "%.2f"

    def _from_string (self, s) :
        return float (s)
    # end def _from_string

# end class Float

class Image (Field, DM.ImageField) :
    pass
# end class Image

class Integer (Field, DM.IntegerField) :

    def _from_string (self, s) :
        return int (s)
    # end def _from_string

# end class Integer

class IP_Address (Field, DM.IPAddressField) :
    pass
# end class IP_Address

class Null_Boolean (Boolean, DM.NullBooleanField) :
    pass
# end class Null_Boolean

class  Positive_Integer (Integer, DM.PositiveIntegerField) :
    pass
# end class  Positive_Integer

class Slug (Field, DM.SlugField) :
    pass
# end class Slug

class Small_Integer (Integer, DM.SmallIntegerField) :
    pass
# end class Small_Integer

class Text (Field, DM.TextField) :
    pass
# end class Text

class Time (_Date_, DM.TimeField) :

    input_formats  = ("%H:%M:%S", "%H:%M")
    _tuple_len     = 6
    _tuple_off     = 3
    _DT_Type       = datetime.time

# end class Time

class URL (Field, DM.URLField) :
    pass
# end class URL

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ DJO.M_Field
