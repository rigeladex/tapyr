# -*- coding: utf-8 -*-
# Copyright (C) 2004-2020 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TFL.Units.Kind
#
# Purpose
#    Model a unit kind
#
# Revision Dates
#     8-Aug-2004 (CT) Creation
#    29-Sep-2006 (CT) `__add__` and `__sub__` added
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
#    17-Feb-2017 (CT) Delegate conversion to `unit`
#                     + don't use `unit.factor` directly
#    17-Feb-2017 (CT) Add `__str__`
#    19-Feb-2017 (CT) Add `float` conversion to `Kind.__init__`
#     5-Jun-2020 (CT) Add `Command`
#    ««revision-date»»···
#--

from   _TFL                       import TFL

from   _TFL.pyk                   import pyk
from   _TFL.Regexp                import Regexp, re

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL._Meta.totally_ordered import totally_ordered

import _TFL.Command
import _TFL._Meta.Object
import _TFL._Units.M_Kind

@totally_ordered
class Kind (TFL.Meta.Object, metaclass = TFL.Units.M_Kind) :
    """Model a unit kind"""

    base_unit     = None ### redefine in descendents
    _units        = ()   ### redefine in descendents

    def __init__ (self, value, unit = None) :
        if unit is None :
            unit   = self.base_unit
        elif unit in self.u_map :
            unit   = self.u_map [unit]
        self.value = float (value) * unit
        self.unit  = unit
    # end def __init__

    def __add__ (self, rhs) :
        if isinstance (rhs, self.__class__) :
            return self.__class__ (self.value + rhs.value)
        raise TypeError \
            ( "unsupported operand type(s) for +: '%s' and '%s'"
            % (self.__class__.__name__, rhs.__class__.__name__)
            )
    # end def __add__

    def __eq__ (self, rhs) :
        try :
            rhs = rhs.value
        except AttributeError :
            pass
        return self.value == rhs
    # end def __eq__

    def __lt__ (self, rhs) :
        try :
            rhs = rhs.value
        except AttributeError :
            pass
        return self.value < rhs
    # end def __lt__

    def __truediv__ (self, rhs) :
        try :
            rhs = rhs.value
        except AttributeError :
            pass
        return self.value / rhs
    # end def __truediv__

    def __float__ (self) :
        return self.value
    # end def __float__

    def __getattr__ (self, name) :
        if name.startswith ("as_") :
            unit_name = name [3:]
            if unit_name in self.u_map :
                unit = self.u_map [unit_name]
            else :
                raise AttributeError (name)
            return unit.from_base (self.value)
        raise AttributeError (name)
    # end def __getattr__

    def __mul__ (self, rhs) :
        try :
            rhs = rhs.value
        except AttributeError :
            pass
        return self.value * rhs
    # end def __mul__

    def __repr__ (self) :
        return "%.12g" % (self.value, )
    # end def __repr__

    def __sub__ (self, rhs) :
        if isinstance (rhs, self.__class__) :
            return self.__class__ (self.value - rhs.value)
        raise TypeError \
            ( "unsupported operand type(s) for -: '%s' and '%s'"
            % (self.__class__.__name__, rhs.__class__.__name__)
            )
    # end def __sub__

    def __str__ (self) :
        unit = self.unit
        return "%s%s" % (unit (self.value), unit.abbr)
    # end def __str__

# end class Kind

class _Kind_Command_ (TFL.Command.Root_Command) :
    """Base class for commands for classes derived from `TFL.Unit.Kind`."""

    _rn_prefix              = "_Kind_"

    Kind                    = None ### redefine in descendents

    _args                   = \
        ( "value:S?Value(s) to be converted to `-output_unit`"
        ,
        )

    _opts                   = \
        ( "-format:S=%.12g%s <-> %.12g%s?Format used to print conversions."
        ,
        )

    class _Kind_Unit_Base_ (TFL.Command.Key_Option) :

        _rn_prefix              = "_Kind_"
        is_partial              = True

        @Once_Property
        def choice_dict (self) :
            return self.cmd.Kind.u_map
        # end def choice_dict

    # end class _Kind_Unit_Base_

    class _Kind_Input_Unit (_Kind_Unit_Base_) :
        """Unit to use for input values without explicit unit."""

    Input_Unit = _Kind_Input_Unit # end class

    class _Kind_Output_Unit (_Kind_Unit_Base_) :
        """Unit to use for output values."""

        @property
        def default (self) :
            return self.cmd.Kind.base_unit.name
        # end def default

    Output_Unit=  _Kind_Output_Unit # end class

    def handler (self, cmd) :
        Kind    = self.Kind
        format  = cmd.format
        i_unit  = cmd.input_unit
        o_unit  = cmd.output_unit
        tu_pat  = self._trailing_unit_pat
        for i_val in cmd.argv :
            if tu_pat.search (i_val) :
                unit    = Kind.u_map [tu_pat.unit]
                i_val   = i_val [: tu_pat.start (0)]
            else :
                unit    = i_unit or Kind.base_unit
            i_val   = float   (i_val)
            i_kind  = Kind    (i_val, unit)
            o_val   = getattr (i_kind, "as_" + o_unit.name)
            print \
                ( format
                % ( i_val,   unit.abbr or   unit.name
                  , o_val, o_unit.abbr or o_unit.name
                  )
                )
    # end def handler

    @TFL.Meta.Once_Property
    def _trailing_unit_pat (self) :
        pat = "(?P<unit>%s)\s*$" % \
            ( "|".join
                (   re.escape (u)
                for u in sorted (self.Kind.u_map, key = lambda x : (len (x), x))
                )
            ,
            )
        return Regexp (pat)
    # end def _trailing_unit_pat

Kind.Command = _Kind_Command_ # end class

if __name__ != "__main__" :
    TFL.Units._Export ("Kind")
### __END__ TFL.Units.Kind
