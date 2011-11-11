# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Attr.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.Attr.Filter
#
# Purpose
#    Model query filters for MOM attributes
#
# Revision Dates
#    11-Nov-2011 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr

import _TFL._Meta.Object

from   _TFL.Regexp           import Regexp, re

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL._Meta.Property
import _TFL.Filter

Q = TFL.Attr_Query ()

class _M_Filter_ (TFL.Meta.Object.__class__) :
    """Meta class for Filter classes."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if not name.startswith ("_") :
            cls.op_nam = name.lower ().replace ("_", "-")
            if cls.op_sym is None :
                cls.op_sym = cls.op_nam
    # end def __init__

    def __str__ (cls) :
        return "<Attr.Filter %s [%s]>" % (cls.op_fct, cls.op_sym)
    # end def __str__

# end class _M_Filter_

class _Filter_ (TFL.Meta.Object) :
    """Base class for attribute filters."""

    __metaclass__ = _M_Filter_

    op_fct        = None ### Must be redefined for subclasses or instances
    op_sym        = None ### Must be redefined for subclasses

    def __init__ (self, attr, cooker = None, name = None) :
        self.attr      = attr
        self.attr_name = name or self.attr.name
        self.cooker    = cooker
    # end def __init__

    def __call__ (self, value, prefix = None) :
        cooker = self.cooker
        if cooker is not None :
            try :
                value = cooker (value)
            except (ValueError, TypeError) :
                return None
        return self.query (value, prefix)
    # end def __call__

    def a_query (self, prefix = None) :
        name = self.attr_name
        if prefix :
            name = ".".join ((prefix, name))
        return getattr (Q, name)
    # end def a_query

    def query (self, value, prefix = None) :
        aq = self.a_query (prefix)
        q  = getattr (aq, self.op_fct)
        return q (value)
    # end def query

    def __str__ (self) :
        return "<Attr.%s %s.%s [%s]>" % \
            (self.__class__.__name__, self.attr_name, self.op_fct, self.op_sym)
    # end def __str__

# end class _Filter_

class _Composite_ (_Filter_) :
    """Base class for composite-attribute filters."""

    def __call__ (self, value, prefix = None) :
        name   = self.attr.name
        P_Type = self.attr.P_Type
        pf     = ".".join ((prefix, name)) if prefix else name
        def _gen () :
            for k, v in value.iteritems () :
                attr = getattr (P_Type, k)
                q    = getattr (attr.Q, self.op_fct)
                r    = q (v, pf)
                if r is not None :
                    yield r
        qs = tuple (_gen ())
        if qs :
            return Q.AND (* qs)
    # end def __call__

# end class _Composite_

class _Date_ (_Filter_) :
    """Base class for date-attribute filters."""

    pat = Regexp \
        ( r"^"
            r"(?P<year> [0-9]{4})"
            r"(?: [-/]"
              r"(?P<month> [0-9]{2})"
            r")?"
          r"[-/]?"
          r"$"
        , re.VERBOSE
        )

    def __call__ (self, value, prefix = None) :
        pat = self.pat
        if pat.match (value) :
            q    = self.a_query (prefix)
            args = (int (pat.year), )
            if pat.month :
                args = (int (pat.month, 10), ) + args
                q    = q.D.MONTH
            else :
                q    = q.D.YEAR
            return q (* args)
        else :
            return self.__super.__call__ (value, prefix)
    # end def __call__

# end class _Date_

class _Id_Entity_ (_Composite_) :
    """Base class for entity-attribute filters."""

    def __call__ (self, value, prefix = None) :
        if isinstance (value, dict) :
            return self.__super.__call__ (value, prefix)
        else :
            return self.query (value, prefix)
    # end def __call__

# end class _Id_Entity_

class _String_ (_Filter_) :
    """Base class for string-attribute filters."""

    def query (self, value, prefix = None) :
        aq = self.a_query (prefix)
        q  = getattr (aq, self.op_fct) if value else aq.__eq__
        return q (value)
    # end def query

# end class _String_

class Auto_Complete (_Filter_) :
    """Attribute query filter for auto-completion."""

    op_fct        = "__eq__"
    op_sym        = "auto-complete"

# end class Auto_Complete

class Auto_Complete_S (_String_) :
    """String-Attribute query filter for auto-completion."""

    op_fct        = "STARTSWITH"
    op_sym        = "auto-complete"

# end class Auto_Complete

class Contains (_String_) :
    """Attribute query filter for contains."""

    op_fct        = "CONTAINS"

# end class Contains

class Ends_With (_String_) :
    """Attribute query for ends-with."""

    op_fct        = "ENDSWITH"

# end class Ends_With

class Equal (_Filter_) :
    """Attribute query filter for equality."""

    op_fct        = "__eq__"
    op_sym        = "=="

# end class Equal

class Greater_Equal (_Filter_) :
    """Attribute query filter for greater-equal."""

    op_fct        = "__ge__"
    op_sym        = ">="

# end class Greater_Equal

class Greater_Than (_Filter_) :
    """Attribute query filter for greater-than."""

    op_fct        = "__gt__"
    op_sym        = ">"

# end class Greater_Than

class Less_Equal (_Filter_) :
    """Attribute query filter for less-equal."""

    op_fct        = "__le__"
    op_sym        = "<="

# end class Less_Than

class Less_Than (_Filter_) :
    """Attribute query filter for less-than."""

    op_fct        = "__lt__"
    op_sym        = "<"

# end class Less_Than

class Starts_With (_String_) :
    """Attribute query for starts-with."""

    op_fct        = "STARTSWITH"

# end class Starts_With

class Composite_Auto_Complete (Auto_Complete, _Composite_) :
    """Composite-Attribute query filter for auto-completion."""

# end class Composite_Auto_Complete

class Composite_Equal (Equal, _Composite_) :
    """Composite-Attribute query filter for equality."""

# end class Composite_Equal

class Composite_Greater_Equal (Greater_Equal, _Composite_) :
    """Composite-Attribute query filter for greater-equal."""

# end class Composite_Greater_Equal

class Composite_Greater_Than (Greater_Than, _Composite_) :
    """Composite-Attribute query filter for greater-than."""

# end class Composite_Greater_Than

class Composite_Less_Equal (Less_Equal, _Composite_) :
    """Composite-Attribute query filter for less-than."""

# end class Composite_Less_Equal

class Composite_Less_Than (Less_Than, _Composite_) :
    """Composite-Attribute query filter for less-equal."""

# end class Composite_Less_Than

class Date_Auto_Complete (Auto_Complete, _Date_) :
    """Date-Attribute query filter for auto-completion."""

# end class Date_Auto_Complete

class Date_Equal (Equal, _Date_) :
    """Date-Attribute query filter for equality."""

# end class Date_Equal

class Date_Greater_Equal (Greater_Equal, _Date_) :
    """Date-Attribute query filter for greater-equal."""

# end class Date_Greater_Equal

class Date_Greater_Than (Greater_Than, _Date_) :
    """Date-Attribute query filter for greater-than."""

# end class Date_Greater_Than

class Date_Less_Equal (Less_Equal, _Date_) :
    """Date-Attribute query filter for less-than."""

# end class Date_Less_Equal

class Date_Less_Than (Less_Than, _Date_) :
    """Date-Attribute query filter for less-equal."""

# end class Date_Less_Than

class Id_Entity_Auto_Complete (Auto_Complete, _Id_Entity_) :
    """Id_Entity-Attribute query filter for auto-completion."""

# end class Id_Entity_Auto_Complete

class Id_Entity_Equal (Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for equality."""

# end class Id_Entity_Equal

class Id_Entity_Greater_Equal (Greater_Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for greater-equal."""

# end class Id_Entity_Greater_Equal

class Id_Entity_Greater_Than (Greater_Than, _Id_Entity_) :
    """Id_Entity-Attribute query filter for greater-than."""

# end class Id_Entity_Greater_Than

class Id_Entity_Less_Equal (Less_Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for less-than."""

# end class Id_Entity_Less_Equal

class Id_Entity_Less_Than (Less_Than, _Id_Entity_) :
    """Id_Entity-Attribute query filter for less-equal."""

# end class Id_Entity_Less_Than

class Ckd (TFL.Meta.Object) :

    Table = dict \
        ( AC                 = Auto_Complete
        , __eq__             = Equal
        , __ge__             = Greater_Equal
        , __gt__             = Greater_Than
        , __le__             = Less_Equal
        , __lt__             = Less_Than
        )

    def __init__ (self, attr) :
        self.attr = attr
    # end def __init__

    @TFL.Meta.Once_Property
    def attr_name (self) :
        return self.attr.name
    # end def attr_name

    @TFL.Meta.Once_Property
    def cooker (self) :
        return self.attr.cooked
    # end def cooker

    def __getattr__ (self, name) :
        attr = self.attr
        try :
            result_type = self.Table [name]
        except KeyError :
            try :
                comp = getattr (attr, name)
            except AttributeError :
                raise
            else :
                q = getattr (comp, "Q", None)
                if isinstance (q, Ckd) :
                    result = q
                else :
                    raise AttributeError (name)
        else :
            result = result_type (attr, self.cooker, self.attr_name)
        setattr (self, name, result)
        return result
    # end def __getattr__

    def __str__ (self) :
        return "<%s.Q [Attr.Filter.%s]>" % \
            (self.attr_name, self.__class__.__name__)
    # end def __str__

# end class Ckd

class Composite (Ckd) :

    Table = dict \
        ( AC                 = Composite_Auto_Complete
        , __eq__             = Composite_Equal
        , __ge__             = Composite_Greater_Equal
        , __gt__             = Composite_Greater_Than
        , __le__             = Composite_Less_Equal
        , __lt__             = Composite_Less_Than
        )

# end class Composite

class Date (Ckd) :

    Table = dict \
        ( AC                 = Date_Auto_Complete
        , __eq__             = Date_Equal
        , __ge__             = Date_Greater_Equal
        , __gt__             = Date_Greater_Than
        , __le__             = Date_Less_Equal
        , __lt__             = Date_Less_Than
        )

# end class Date

class Id_Entity (Ckd) :

    Table = dict \
        ( AC                 = Id_Entity_Auto_Complete
        , __eq__             = Id_Entity_Equal
        , __ge__             = Id_Entity_Greater_Equal
        , __gt__             = Id_Entity_Greater_Than
        , __le__             = Id_Entity_Less_Equal
        , __lt__             = Id_Entity_Less_Than
        )

# end class Id_Entity

class String (Ckd) :

    Table = dict \
        ( Ckd.Table
        , AC                 = Auto_Complete_S
        , CONTAINS           = Contains
        , ENDSWITH           = Ends_With
        , STARTSWITH         = Starts_With
        )

# end class String

class Raw (Ckd) :

    Table = String.Table

    @TFL.Meta.Once_Property
    def attr_name (self) :
        return self.attr.raw_name
    # end def attr_name

    @TFL.Meta.Once_Property
    def cooker (self) :
        return unicode
    # end def cooker

# end class Raw

if __name__ != "__main__" :
    MOM.Attr._Export_Module ()
    MOM._Export ("Q")
### __END__ MOM.Attr.Filter
