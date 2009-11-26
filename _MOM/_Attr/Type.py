# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Attr.Type
#
# Purpose
#    Model attribute types of MOM meta object model
#
# Revision Dates
#    28-Sep-2009 (CT) Creation (factored from TOM.Attr.Type)
#     7-Oct-2009 (CT) Class attribute `syntax` removed (added by `M_Attr_Type`
#                     if necessary)
#     7-Oct-2009 (CT) `_A_Named_Value_` and `A_Boolean` added
#     9-Oct-2009 (CT) `raw_default` and `_symbolic_default` added
#    13-Oct-2009 (CT) Guard for empty string added to `_to_cooked`
#    20-Oct-2009 (MG) `check_ascii` added as it is used for String attributes
#    22-Oct-2009 (CT) `needs_raw_value` added
#    22-Oct-2009 (CT) `max_length` added to `A_String` and its descendents
#    22-Oct-2009 (CT) Signatures of `_from_string_prepare` and
#                     `_from_string_eval` fixed
#    27-Oct-2009 (CT) `_A_Object_` changed to use `epk` instead of `name`
#    28-Oct-2009 (CT) I18N
#    28-Oct-2009 (CT) `A_Link_Role` and descendents added
#    29-Oct-2009 (CT) `_t_rank` added
#     3-Nov-2009 (CT) Fixed `as_string` and `_to_cooked` of `_A_Object_`
#     3-Nov-2009 (CT) `A_Link_Role` derived from `_A_Object_`
#     4-Nov-2009 (CT) `__all__` defined and used
#    19-Nov-2009 (CT) `_A_Object_._get_scope` changed to use
#                     `MOM.Scope.active` as default
#    23-Nov-2009 (CT) `__cmp__` and `__hash__` removed (breaks hashing of
#                     Link_Role attributes)
#    24-Nov-2009 (CT) `_A_Object_.cooked` added to check value agains `Class`
#    25-Nov-2009 (CT) `invariant` removed
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    26-Nov-2009 (CT) `A_Object`, `A_Cached_Role`, and `A_Cached_Role_DFC` added
#    26-Nov-2009 (CT) `_A_Object_.etype_manager` factored and used
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr.Kind
import _MOM._Meta.M_Attr_Type

from   _TFL.I18N             import _, _T, _Tn
from   _TFL.Regexp           import *

import _TFL._Meta.Property

import datetime
import itertools
import time

class A_Attr_Type (object) :
    """Root class for attribute types for the MOM meta object model."""

    __metaclass__     = MOM.Meta.M_Attr_Type

    check             = ()
    check_syntax      = None
    code_format       = "%r"
    computed          = None
    default           = None
    description       = ""
    explanation       = ""
    format            = "%s"
    group             = ""
    hidden            = False
    kind              = None
    Kind_Mixins       = ()
    needs_raw_value   = True
    rank              = 0
    raw_default       = ""
    record_changes    = True
    simple_cooked     = None
    store_default     = False
    symbolic_ref_pat  = Regexp (r"^\s*\$\(.*\)\s*$", re.MULTILINE)
    typ               = None

    _symbolic_default = False
    _t_rank           = 0

    def __init__ (self, kind) :
        self.kind = kind
    # end def __init__

    def as_code (self, value) :
        return self.code_format % (value, )
    # end def as_code

    def as_pickle (self, value) :
        return value
    # end def as_pickle

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return soc.format % (value, )
        return ""
    # end def as_string

    def check_invariant (self, obj, value) :
        errors = obj._pred_man.check_attribute (obj, self, value)
        if len (errors) == 1 :
            raise errors [0]
        elif errors :
            raise MOM.Error.Invariant_Errors (errors)
    # end def check_invariant

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if soc.simple_cooked :
            return soc.simple_cooked (value)
        return value
    # end def cooked

    def from_code (self, s, obj = None, glob = {}, locl = {}) :
        return self._to_cooked (s, self._call_eval, obj, glob, locl)
    # end def from_code

    def from_pickle (self, s, obj = None, glob = {}, locl = {}) :
        return p
    # end def from_pickle

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        return self._to_cooked (s, self._from_string_resolve, obj, glob, locl)
    # end def from_string

    def _call_eval (self, s, glob, locl) :
        return eval (s, glob, locl.copy ())
    # end def _call_eval

    def _from_string (self, s, obj, glob, locl) :
        t = self._from_string_prepare (s, obj)
        try :
            u = self._from_string_eval (t, obj, glob, locl)
        except StandardError as exc :
            raise MOM.Error.Attribute_Syntax_Error \
                (obj, self, "%s -> %s" % (s, t), str (exc))
        try :
            if u is not None :
                return self.cooked (u)
            else :
                pass
        except StandardError as exc :
            raise MOM.Error.Attribute_Syntax_Error \
                (obj, self, "%s -> %s -> %s" % (s, t, u), str (exc))
    # end def _from_string

    def _from_string_eval (self, s, obj, glob, locl) :
        return self._call_eval (s, glob, locl)
    # end def _from_string_eval

    def _from_string_prepare (self, s, obj) :
        try :
            s = s.encode ("ascii")
        except AttributeError as exc :
            if __debug__ :
                print "%s.%s = %s --> %s" % (obj, self, s, exc)
        except UnicodeError :
            raise MOM.Error.Attribute_Syntax_Error \
                ( obj, self, s
                , _T ("Non-ascii values are currently not supported")
                )
        return s
    # end def _from_string_prepare
    check_ascii          = _from_string_prepare ### XXX

    def _from_string_resolve (self, s, obj, glob, locl) :
        if obj is not None and not glob :
            glob = obj.globals ()
        if self.symbolic_ref_pat.match (s) :
            resolver = self._from_symbolic_ref
        else :
            resolver = self._from_string
        return resolver (s, obj, glob, locl)
    # end def _from_string_resolve

    def _from_symbolic_ref (self, s, obj, glob, locl) :
        raise NotImplementedError ("_from_symbolic_ref: XXX")
    # end def _from_symbolic_ref

    def _to_cooked (self, s, cooker, obj, glob, locl) :
        if s :
            if self.simple_cooked :
                try :
                    return self.simple_cooked (s)
                except (ValueError, TypeError) :
                    pass
            return cooker (s, obj, glob or {}, locl or {})
    # end def _to_cooked

    def __repr__ (self) :
       return "%s `%s'" % (self.typ, self.name)
    # end def __repr__

    def __str__ (self) :
        return self.name
    # end def __str__

# end class A_Attr_Type

class _A_Date_ (A_Attr_Type) :
    """Common base class for date-valued attributes of an object."""

    _tuple_off     = 0

    @property
    def output_format (self) :
        return self.input_formats [0]
    # end def output_format

    def as_code (self, value) :
        return self.__super.as_code (self.as_string (value))
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return value.strftime (self.output_format)
        return ""
    # end def as_string

    def from_code (self, s, obj = None, glob = None, locl = None) :
        return self.from_string (self.__super.from_code (s, obj, glob, locl))
    # end def from_code

    def _from_string_eval (self, s, obj, glob, locl) :
        s = s.strip ()
        for f in self.input_formats :
            try :
                result = time.strptime (s, f)
            except ValueError :
                pass
            else :
                break
        else :
            raise ValueError (s)
        return self._DT_Type (* result [self._tuple_off:self._tuple_len])
    # end def _from_string_eval

# end class _A_Date_

class _A_Named_Value_ (A_Attr_Type) :
    """Common base class for attributes holding named values."""

    __metaclass__     = MOM.Meta.M_Attr_Type_Named_Value

    needs_raw_value   = False

    def as_code (self, value) :
        return self.code_format % (self.__class__.Elbat [value], )
    # end def as_code

    def as_pickle (self, value) :
        return self.__class__.Elbat [value]
    # end def as_pickle

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        Elbat = getattr (soc, "Elbat", None)
        if Elbat is None :
            Elbat = getattr (soc.__class__, "Elbat", None)
        return soc.format % (Elbat [value], )
    # end def as_string

    def eligible_raw_values (self, obj = None) :
        return sorted (self.__class__.Table.iterkeys ())
    # end def eligible_raw_values

    def from_code (self, s, obj = None, glob = None, locl = None) :
        return self._from_string_eval (self._call_eval (s, glob, locl))
    # end def from_code

    def from_pickle (self, s, obj = None, glob = None, locl = None) :
        try :
            return self.__class__.Table [s]
        except KeyError :
            pass
    # end def from_pickle

    def _from_string_eval (self, s, obj, glob, locl) :
        try :
            return self.__class__.Table [s]
        except KeyError :
            raise ValueError ("%s not in %s" % (s, self.eligible_raw_values ()))
    # end def _from_string_eval

# end class _A_Named_Value_

class _A_Number_ (A_Attr_Type) :
    """Common base class for number-valued attributes of an object."""

# end class _A_Number_

class _A_Float_ (_A_Number_) :
    """Models a floating-point attribute of an object."""

    typ         = "Float"
    cooked      = float

    def _from_string_prepare (self, s, obj) :
        return s.replace ("/", "*1.0/")
    # end def _from_string_prepare

# end class _A_Float_

class _A_Int_ (_A_Number_) :
    """Models an integer attribute of an object."""

    typ         = "Int"
    cooked      = int

# end class _A_Int_

class _A_Link_Role_Left_ (A_Attr_Type) :
    """Attribute modelling the left role of a link."""

    generic_role_name = "left"
    rank              = 0
    role_abbreviation = "l"
    typ               = "Left"

# end class _A_Link_Role_Left_

class _A_Link_Role_L_Middle_ (A_Attr_Type) :
    """Attribute modelling the left-middle role of a link."""

    generic_role_name = "l_middle"
    rank              = 1
    role_abbreviation = "lm"
    typ               = "L_Middle"

# end class _A_Link_Role_L_Middle_

class _A_Link_Role_Middle_ (A_Attr_Type) :
    """Attribute modelling the middle role of a link."""

    generic_role_name = "middle"
    rank              = 2
    role_abbreviation = "m"
    typ               = "Middle"

# end class _A_Link_Role_Middle_

class _A_Link_Role_R_Middle_ (A_Attr_Type) :
    """Attribute modelling the right-middle role of a link."""

    generic_role_name = "r_middle"
    rank              = 3
    role_abbreviation = "rm"
    typ               = "R_Middle"

# end class _A_Link_Role_R_Middle_

class _A_Link_Role_Right_ (A_Attr_Type) :
    """Attribute modelling the right role of a link."""

    generic_role_name = "right"
    rank              = 4
    role_abbreviation = "r"
    typ               = "Right"

# end class _A_Link_Role_Right_

class _A_Link_Role_Seq_No_ (A_Attr_Type) :
    """Attribute modelling the sequence number role of an ordered link."""

    generic_role_name = "seq_no"
    rank              = 5
    role_abbreviation = "n"
    typ               = "Seq_No"

# end class _A_Link_Role_Seq_No_

class _A_Object_ (A_Attr_Type) :
    """Models an attribute referring to an object."""

    Class             = ""

    needs_raw_value   = False

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return soc.format % \
                ( tuple
                    (a.as_string (a.get_value (value)) for a in value.primary)
                ,
                )
        return ""
    # end def as_string

    def as_code (self, value) :
        return tuple (a.as_code (a.get_value (value)) for a in value.primary)
    # end def as_code

    def as_pickle (self, value) :
        if value is not None :
            return value.epk
    # end def as_pickle

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        et = soc.etype_manager ()
        if et and not isinstance (value, et) :
            raise ValueError \
                ( _T
                    ( "%s %s not eligible for attribute %s,"
                      "\n"
                      "    must be instance of %s"
                    )
                % (value.type_name, str (value), soc, soc.Class.type_name)
                )
        return value
    # end def cooked

    def eligible_objects (self, obj = None) :
        etm = self.etype_manager (obj)
        return (et and et.t_extension ()) or ()
    # end def eligible_objects

    def eligible_raw_values (self, obj = None) :
        return sorted (o.epk for o in self.eligible_objects (obj))
    # end def eligible_raw_values

    @TFL.Meta.Class_and_Instance_Method
    def etype_manager (soc, obj = None) :
        if soc.Class :
            return getattr (soc._get_scope (obj), soc.Class.type_name, None)
    # end def etype_manager

    def from_pickle (self, p, obj = None, glob = None, locl = None) :
        if p is not None :
            return self._to_cooked (p, None, obj, glob, locl)
    # end def from_pickle

    def from_string (self, s, obj = None, glob = None, locl = None) :
        if s :
            return self._to_cooked (s, None, obj, glob, locl)
    # end def from_string

    def _accept_object (self, obj, result) :
        if (      self.__class__.eligible_objects.im_func
           is not _A_Object_.eligible_objects.im_func
           ) :
            eo = self.eligible_objects (obj)
            if eo :
                return result in eo
        return True
    # end def _accept_object

    @TFL.Meta.Class_and_Instance_Method
    def _get_scope (soc, obj) :
        return obj.home_scope if obj else MOM.Scope.active
    # end def _get_scope

    def _to_cooked (self, s, cooker, obj, glob, locl) :
        assert self.Class, "%s needs to define `Class`" % self
        if isinstance (s, tuple) :
            t  = s
        else :
            t  = self._call_eval    (s, {}, {})
        scope  = self._get_scope    (obj)
        et     = self.etype_manager (obj)
        result = et.instance        (* t, raw = True)
        if result is not None :
            if self._accept_object  (obj, result) :
                return self.cooked  (result)
            else :
                raise ValueError \
                    ( _T ("object %s %s not eligible, specify one of: %s")
                    % (self.Class.type_name, t, self.eligible_raw_values (obj))
                    )
        else :
            raise MOM.Error.No_Such_Object, \
                ( _T ("No object %s %s in scope %s")
                % (self.Class.type_name, t, scope.name)
                )
    # end def _to_cooked

# end class _A_Object_

class _A_Unit_ (A_Attr_Type) :
    """Mixin for attributes describing physical quantities with optional
       units.
    """

    __metaclass__ = MOM.Meta.M_Attr_Type_Unit
    _default_unit = None ### set by meta class
    _unit_dict    = {}
    _unit_pattern = Regexp \
        ( r"[])a-zA-Z_0-9] \s+ (?P<unit> [a-zA-Z]+ (?: / [a-zA-Z]+)?) \s*$"
        , re.VERBOSE
        )

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        ### beware: `as_string` can be used as class method, too;
        ### when called for the class, `soc.__super` doesn't
        ### work while `super (_A_Unit_, soc)` does
        if value is not None :
            return "%s %s" % \
               (super (_A_Unit_, soc).as_string (value), soc._default_unit)
        return ""
    # end def as_string

    def eligible_raw_values (self, obj = None) :
        return sorted (self._unit_dict.iterkeys ())
    # end def eligible_raw_values

    def _from_string_eval (self, s, obj, glob, locl) :
        factor = 1
        pat    = self._unit_pattern
        if pat.search (s) :
            unit = pat.unit
            s    = s [: pat.start ("unit")]
            try :
                factor = self._unit_dict [unit]
            except KeyError :
                raise ValueError \
                      ( _T ("Invalid unit %s, specify one of %s")
                      % (unit, self.eligible_raw_values ())
                      )
        return self.__super._from_string_eval (obj, s, glob, locl) * factor
    # end def _from_string_eval

# end class _A_Unit_

class A_Boolean (_A_Named_Value_) :
    """Models a Boolean attribute of an object."""

    typ            = "Boolean"

    Table          = dict \
        ( no       = False
        , yes      = True
        )

# end class A_Boolean

class A_Date (_A_Date_) :
    """Models a date-valued attribute of an object."""

    typ            = "Date"
    input_formats  = \
        ( "%Y/%m/%d", "%Y%m%d", "%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y")
    _tuple_len     = 3
    _DT_Type       = datetime.date

# end class A_Date

class A_Date_Time (_A_Date_) :
    """Models a date-time-valued attribute of an object."""

    typ            = "Date-Time"
    input_formats  = tuple \
        ( itertools.chain
            ( * (  (f + " %H:%M:%S", f + " %H:%M", f)
                for f in A_Date.input_formats
                )
            )
        )
    _tuple_len     = 6
    _DT_Type       = datetime.datetime

# end class A_Date_Time

class A_Float (_A_Float_) :
    code_format   = "%s"
    simple_cooked = float
# end class A_Float

class A_Int (_A_Int_) :
    simple_cooked = int
# end class A_Int

class A_Length (_A_Unit_, _A_Float_) :
    """Models a length attribute with unit information."""

    typ           = "Length"
    _unit_dict    = dict \
        ( { "in"    : 0.0254 }
        , cm        = 1.e-2
        , ft        = 0.3048000
        , km        = 1.e3
        , m         = 1.0
        , mi        = 1609.344
        , mm        = 1.e-3
        , Nm        = 1852.0
        , nm        = 1.e-9
        , um        = 1.e-6
        , yd        = 0.9144000
        )

# end class A_Length

class A_Link_Role (_A_Object_) :
    """Attribute describing a link-role."""

    __metaclass__     = MOM.Meta.M_Attr_Type_Link_Role

    auto_cache        = False
    dfc_synthesizer   = None
    kind              = MOM.Attr.Link_Role
    max_links         = 0
    role_name         = None
    role_type         = None

    _t_rank           = -100

# end class A_Link_Role

class A_Link_Role_AB (A_Link_Role) :
    """Attribute describing a link-role of an attribute-based link."""

    attr_name         = None

# end class A_Link_Role_AB

class A_Link_Role_EB (A_Link_Role) :
    """Attribute describing a link-role of an entity-based link."""

# end class A_Link_Role_EB

class A_Object (_A_Object_) :
    """Models an attribute referring to an object."""

    typ         = "Object"
    Kind_Mixins = (MOM.Attr.Object_Reference_Mixin, )

# end class A_Object

class A_Cached_Role (A_Object) :
    """Models an attribute referring to an object linked via an
       association.
    """

    kind         = MOM.Attr.Cached_Role
    hidden       = True

# end class A_Cached_Role

class A_Cached_Role_DFC (A_Cached_Role) :
    """Models an attribute to an object linked via an association or derived
       from a container.
    """

    kind         = MOM.Attr.Cached_Role_DFC

# end class A_Cached_Role_DFC

class A_String (A_Attr_Type) :
    """Models a string-valued attribute of an object."""

    typ               = "String"

    max_length        = 64
    needs_raw_value   = False

    def _from_string_eval (self, s, obj, glob, locl) :
        return s
    # end def _from_string

    def check_syntax (self, obj, value) :
        if value :
            self.check_ascii (value, obj)
    # end def check_syntax

# end class A_String

class A_Name (A_String) :
    """Models a name-valued attribute of an object."""

    typ                = "Name"

    max_length         = 32
    identifier_pattern = Regexp ("^ [a-zA-Z_] [a-zA-Z0-9_]* $", re.X)
    syntax             = _T \
        ( "A name must start with a letter or underscore and continue with "
          "letters, digits, and underscores."
        )

    def check_syntax (self, obj, value) :
        if value :
            self.__super.check_syntax (obj, value)
            v = value.strip ()
            if not self.identifier_pattern.match (v) :
                raise MOM.Error.Attribute_Syntax_Error (obj, self, value)
    # end def check_syntax

# end class A_Name

class A_Text (A_String) :
    """Models a string-valued attribute of an object which allows text of
       arbitrary length.
    """
    typ         = "Text"

    max_length  = None

# end class A_Text

class A_Time (_A_Date_) :
    """Models a time-valued attribute of an object."""

    typ            = "Time"
    input_formats  = ("%H:%M:%S", "%H:%M")
    _tuple_len     = 6
    _tuple_off     = 3
    _DT_Type       = datetime.time

# end class A_Time

__doc__ = """
Class `MOM.Attr.A_Attr_Type`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: A_Attr_Type

    `MOM.Attr.A_Attr_Type` provides the framework for defining the
    type of essential or non-essential attributes of essential objects
    and links. It is the root class for a hierarchy of classes defining
    abstract attribute types like `A_Int`, `A_String`, `A_Name` and
    many more. All classes specifying abstract attribute types should
    be named following the convention `A_«type-name»` and must define
    a class attribute `typ` that defines the human-readable name of
    the abstract attribute type, e.g., `int`, `string`, or `name`.

    Concrete attribute definitions for essential classes are then
    specified by defining a class derived from the appropriate class
    defining the attribute type, e.g., `A_Int`. The names of classes
    defining concrete attributes **must** not start with `A_` to avoid
    terminal confusion.

    Abstract attribute types are characterized by the properties:

    .. attribute:: name

      Specified by the name of the class.

    .. attribute:: syntax

      Provides information about the syntax required for the
      attribute.

    .. attribute:: typ

      Defines the human-readable name of
      the abstract attribute type, e.g., `int`, `string`, or `name`.

    .. attribute:: needs_raw_value

      Specifies if the raw value needs to be stored for
      this attribute type.

    Concrete attribute types are characterized by the properties:

    .. attribute:: name

      Specified by the name of the class.

    .. attribute:: description

      A short description of the attribute in question.
      This is for example used for displaying a short help text.

      Normally specified via the doc-string of the
      class (but can also be defined by defining a class attribute
      `description`).

    .. attribute:: explanation

      A long description of the attribute in question
      (optional). This is used for the documentation of the attribute
      (together with `description`) and is for example displayed by
      an attribute browser.

    .. attribute:: kind

      Refers to the specific class defining the
      :class:`~_MOM._Attr.Kind.Kind` of the attribute in question.

    .. attribute:: Kind_Mixins

      A number of mixins for the `kind` to be used for this
      attribute. Some of the possible mixins are
      :class:`~_MOM._Attr.Kind.Computed_Mixin`,
      :class:`~_MOM._Attr.Kind.Sticky_Mixin`, and
      :class:`~_MOM._Attr.Kind.Class_Uses_Default_Mixin`.

      This is optional and defaults to `()`.

    .. attribute:: check

      Specifies a tuple of expressions that constrain the possible
      values of the attribute. e.g. '0 <= this <= 100'.

      This is optional and defaults to `()`.

    .. attribute:: default

      Defines the default value to be used for the
      attribute when no explicit value is defined by the tool's user.

      This is optional and defaults to `None`.

      `default` **must** not be specified for
      :class:`~_MOM._Attr.Kind.Primary` and
      :class:`~_MOM._Attr.Kind.Required` attributes.

    .. attribute:: computed

      A method that's used to compute a value if none is
      specified by the tool user for
      :class:`~_MOM._Attr.Kind.Optional` attributes with the
      :class:`~_MOM._Attr.Kind.Computed_Mixin` or
      one of the internal attributes kinds
      :class:`~_MOM._Attr.Kind.Sync_Cached`,
      :class:`~_MOM._Attr.Kind.Auto_Cached`,
      :class:`~_MOM._Attr.Kind.Once_Cached`, or
      :class:`~_MOM._Attr.Kind.Computed`.

    .. attribute:: group

      A string that can be used to group a set of attributes
      together. For instance, editors display attributes sorted
      alphabetically by `(group, name)`.

    .. attribute:: rankis

      Used when sorting attributes of `Primary`.

    .. attribute:: store_default

      Specifies whether the default value should be
      stored in the database (unless explicitly specified, it isn't).

"""

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Type
