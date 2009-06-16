# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2009 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Model_Field
#
# Purpose
#    Subclass Django models/field classes to add useful behavior
#
# Revision Dates
#    14-Jul-2008 (CT) Creation
#    15-Jul-2008 (CT) Creation continued
#     3-Oct-2008 (CT) s/django.newforms/django.forms/g
#    16-Oct-2008 (CT) `widget_attrs` added
#    20-Oct-2008 (CT) `Auto_Slug` added
#    21-Oct-2008 (CT) `Auto_Slug.field_fmt_kw` added
#    27-Feb-2009 (CT) `Choice_Char`, `Choice_Int` and `Choice_Small` added
#    15-May-2009 (CT) `Positive_Small_Integer` added
#    19-May-2009 (CT) `_Numeric_` added; `_Integer_` factored;
#                     `Positive_Integer` and `Positive_Small_Integer` removed
#    19-May-2009 (CT) `Choice` (and `M_Choice`) added;
#                     `Choice_Char`, `Choice_Int`, and `Choice_Small` removed
#    19-May-2009 (CT) `Foreign_Key`, `Many_to_Many`, and `One_to_One` added
#    28-May-2009 (CT) `Null` added
#    28-May-2009 (CT) `sort_key` added
#    30-May-2009 (CT) `M_Field.__call__` added to save `_creation_kw`
#    30-May-2009 (CT) `opt_proxy_args` added to `Foreign_Key`
#     1-Jun-2009 (CT) Support for `real_name` added
#    11-Jun-2009 (CT) Support for `css_class` added
#    ««revision-date»»···
#--

from   _TFL                               import TFL
import _TFL._Meta.M_Class
from   _TFL.defaultdict                   import defaultdict

from   _DJO                               import DJO

from   django.db                          import models       as DM
from   django.forms                       import widgets
from   django.utils.translation           import gettext_lazy as _

import datetime
import time

class M_Field (TFL.Meta.M_Class, DM.Field.__class__) :
    """Meta class for model fields with support for `.__super` and
       `_real_name`.
    """

    def __call__ (cls, * args, ** kw) :
        ckw    = dict (kw)
        result = cls.__m_super.__call__ (* args, ** kw)
        result._creation_kw = ckw
        if args :
            if "verbose_name" not in ckw :
                ckw ["verbose_name"] = result.verbose_name
        return result
    # end def __call__

# end class M_Field

class M_Choice (M_Field) :
    """Meta class for choice model fields."""

    Table = {}

    def __call__ (cls, Field_Type, * args, ** kw) :
        Type = cls.Table.get (Field_Type)
        if Type is None :
            name = "Choice_%s" % Field_Type.__name__
            dct  = dict \
                ( __module__ = cls.__module__
                , Null       = Field_Type.Null
                )
            Type = cls.Table [Field_Type] = type (Field_Type) \
                (name, (_Choice_, Field_Type), dct)
        return Type (* args, ** kw)
    # end def __call__

# end class M_Choice

class _DJO_Field_ (DM.Field) :

    __metaclass__ = M_Field
    _real_name    = "Field"

    Null          = ""
    output_format = "%s"
    Widget        = None

    def __init__ (self, * args, ** kw) :
        if "output_format" in kw :
            self.output_format = kw.pop ("output_format")
        if "real_name" in kw :
            self.real_name = kw.pop ("real_name")
        if "Widget" in kw :
            self.Widget    = kw.pop ("Widget")
        if self.Null == "" :
            kw.pop ("null", None)
        self.css_class    = kw.pop ("css_class", "")
        self._sort_key    = kw.pop ("sort_key", 0)
        self.widget_attrs = dict \
            ( {"class" : self.css_class}
            , ** (kw.pop ("widget_attrs", {}))
            )
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def as_string (self, value) :
        if value is not None :
            return self.output_format % (value, )
        return ""
    # end def as_string

    def formfield (self, ** kw) :
        defaults = dict ()
        if self.Widget :
            ### XXX ???
            ### - instantiate `Widget`
            ### - pass `self` (cf. `_D_Widget_`)
            defaults.update (widget = self.Widget)
        defaults.update (kw)
        result = self.__super.formfield (** defaults)
        result.widget.attrs.update (self.widget_attrs)
        return result
    # end def formfield

    def from_string (self, s) :
        if s is not None :
            return self._from_string (s)
    # end def from_string

    @property
    def sort_key (self) :
        return (self._sort_key, self.creation_counter)
    # end def sort_key

    def _from_string (self, s) :
        return s
    # end def _from_string

Field = _DJO_Field_ # end class

class _Numeric_ (Field) :
    """Mixin for numeric field types"""

    Null          = None

    def __init__ (self, * args, ** kw) :
        self.min_value = kw.pop ("min_value", None)
        self.max_value = kw.pop ("max_value", None)
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def formfield (self, * args, ** kw) :
        if self.min_value is not None :
            kw ["min_value"] = self.min_value
        if self.max_value is not None :
            kw ["max_value"] = self.max_value
        return self.__super.formfield (* args, ** kw)
    # end def formfield

# end class _Numeric_

class Auto (Field, DM.AutoField) :

    Null          = None

    def _from_string (self, s) :
        return int (s)
    # end def _from_string

# end class Auto

class Boolean (Field, DM.BooleanField) :

    Null          = None

    def _from_string (self, s) :
        return s == "True"
    # end def _from_string

# end class Boolean

class Char (Field, DM.CharField) :
    pass
# end class Char

class _D_Widget_ (widgets.TextInput) :

    def __init__ (self, attrs=None, field=None) :
        super (_D_Widget_, self).__init__ (attrs)
        self.field = field
    # end def __init__

    def render (self, name, value, attrs = None) :
        if self.field :
            value = self.field.as_string (value)
        return super (_D_Widget_, self).render (name, value, attrs)
    # end def render

# end class _D_Widget_

class _Date_ (Field) :

    input_formats  = ("%Y/%m/%d", "%Y%m%d", "%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y")
    Null           = None
    _output_format = None
    _tuple_off     = 0

    Widget         = _D_Widget_

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

    def as_string (self, value, output_format = None) :
        try :
            value.strftime
        except AttributeError :
            result = value or ""
        else :
            result = value.strftime (output_format or self.output_format)
        return result
    # end def as_string

    def _from_string (self, s) :
        s = s.strip ()
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
            ( input_formats = self.input_formats
            , widget        = self.Widget (field = self)
            )
        defaults.update (kw)
        return self.__super.formfield (** defaults)
    # end def formfield

# end class _Date_

class Date (_Date_, DM.DateField) :
    """
       >>> df = Date ()
       >>> df.from_string ("2008/04/30")
       datetime.date(2008, 4, 30)
       >>> df.from_string ("20080430")
       datetime.date(2008, 4, 30)
       >>> df.from_string ("2008-04-30")
       datetime.date(2008, 4, 30)
       >>> df.from_string ("30/4/2008")
       datetime.date(2008, 4, 30)
       >>> df.from_string ("30.4.2008")
       datetime.date(2008, 4, 30)
       >>> d=df.from_string ("20080430")
       >>> df.as_string (d)
       '2008/04/30'
       >>> df.from_string ("2008/04/31")
       ...
       ValueError: 2008/04/31
    """

    _tuple_len     = 3
    _DT_Type       = datetime.date

# end class Date

class Date_Time (_Date_, DM.DateTimeField) :

    input_formats  = \
      ( "%Y/%m/%d %H:%M:%S"
      , "%Y/%m/%d %H:%M"
      , "%Y%m%d %H:%M:%S"
      , "%Y%m%d %H:%M"
      , "%Y-%m-%d %H:%M:%S"
      , "%Y-%m-%d %H:%M"
      , "%d/%m/%Y %H:%M:%S"
      , "%d/%m/%Y %H:%M"
      , "%d.%m.%Y %H:%M:%S"
      , "%d.%m.%Y %H:%M"
      ) + _Date_.input_formats
    _tuple_len     = 6
    _DT_Type       = datetime.datetime

# end class Date_Time

class Decimal (_Numeric_, DM.DecimalField) :

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

class Float (_Numeric_, DM.FloatField) :

    output_format = "%.2f"

    def _from_string (self, s) :
        return float (s)
    # end def _from_string

# end class Float

class Foreign_Key (Field, DM.ForeignKey) :

    Null          = None

    def __init__ (self, * args, ** kw) :
        self.opt_proxy_args = kw.pop ("opt_proxy_args", ())
        self.__super.__init__ (* args, ** kw)
    # end def __init__

# end class Foreign_Key

class Image (Field, DM.ImageField) :
    pass
# end class Image

class _Integer_ (_Numeric_) :

    def _from_string (self, s) :
        return int (s)
    # end def _from_string

# end class _Integer_

class Integer (_Integer_, DM.IntegerField) :
    pass
# end class Integer

class IP_Address (Field, DM.IPAddressField) :
    pass
# end class IP_Address

class Many_to_Many (Field, DM.ManyToManyField) :
    Null          = None
# end class Many_to_Many

class Null_Boolean (Boolean, DM.NullBooleanField) :
    pass
# end class Null_Boolean

class One_to_One (Field, DM.OneToOneField) :
    Null          = None
# end class One_to_One

class Slug (Field, DM.SlugField) :
    pass
# end class Slug

class Auto_Slug (Slug) :

    def __init__ (self, * args, ** kw) :
        from_fields = kw.pop ("from_fields")
        if isinstance (from_fields, basestring) :
            from_fields   = (from_fields, )
        self.from_fields  = from_fields
        self.field_fmt_kw = kw.pop ("field_fmt_kw", defaultdict (dict))
        kw ["unique"]     = True
        self.__super.__init__ (* args, ** kw)
        self.editable = False
    # end def __init__

    def pre_save (self, obj, add) :
        result = self.__super.pre_save (obj, add)
        fmt_kw = self.field_fmt_kw
        if not result :
            from django.template import defaultfilters
            from _DJO._NAV.Model import Field
            base   = defaultfilters.slugify \
                ( u"--".join
                    (   unicode (Field (f, None, obj, fmt_kw [f]))
                    for f in self.from_fields
                    )
                )
            result = self._unique_slug (obj, base)
        return result
    # end def pre_save

    def _unique_slug (self, obj, base) :
        result  = base
        i       = 1
        objects = obj.__class__.objects.all ()
        key     = "%s__exact" % self.attname
        while objects.filter (** { key : result}) :
            i      += 1
            result  = u"%s-%s" % (base, i)
        return result
    # end def _unique_slug

# end class Auto_Slug

class Small_Integer (_Integer_, DM.SmallIntegerField) :
    pass
# end class Small_Integer

class Text (Field, DM.TextField) :
    Widget         = widgets.Textarea
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

class _Choice_ (Field) :

    def __init__ (self, * args, ** kw) :
        choices = kw ["choices"]
        if isinstance (choices, dict) :
            kw ["choices"] = sorted (choices.iteritems ())
        else :
            ### doesn't support collecting available choices into named groups
            choices = dict (choices)
        self._code_to_choice = choices
        self._choice_to_code = dict ((v, k) for (k, v) in choices.iteritems ())
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def choice_to_code (self, value) :
        if value in self._code_to_choice :
            result = value
        else :
            result = self._choice_to_code [value]
        return result
    # end def choice_to_code

    def code_to_choice (self, value) :
        if value in self._choice_to_code :
            result = value
        else :
            result = self._code_to_choice [value]
        return result
    # end def code_to_choice

# end class _Choice_

class Choice (Field) :
    __metaclass__ = M_Choice
# end class Choice

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ DJO.Model_Field
