#! /usr/bin/python
# Copyright (C) 1998 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    EU_Currency
#
# Purpose
#    Provide classes for management of European Currencies
#
# Revision Dates
#    28-Dec-1998 (CT) Creation
#    31-Dec-1998 (CT) Rates entered
#    31-Jan-1999 (CT) `__cmp__', `__neg__', `__pos__', and `__abs__' added
#    27-Sep-1999 (CT) `command_spec' and `main' factored
#    29-Sep-1999 (CT) Use `Opt_L' for `-source' and `-target'
#     4-Jan-2000 (CT) `__float__' added
#     4-Jan-2000 (CT) `sep_1000' added
#    21-May-2001 (CT) `main': show evaluated argument (`b') if expression
#    29-Jul-2001 (CT) Inplace operators added
#    26-Dec-2001 (CT) Use attribute notation to access cmd-options
#    28-Dec-2001 (CT) Return statement added to inplace operators
#    29-Dec-2001 (CT) `as_source_s` added
#     1-Jan-2002 (CT) Argument `round_to_euro` added to `rounded` and its
#                     callers
#     1-Jan-2002 (CT) `_formatted` factored
#     5-Jan-2002 (CT) `EUR` alias added
#    12-Feb-2002 (CT) Argument `round_to_euro` renamed to `round`
#    12-Feb-2002 (CT) `rounded` corrected (must reset `cent` values < 50 for
#                     true values of `round`)
#    12-Feb-2002 (CT) `rounded_as_target` added
#    12-Feb-2002 (CT) `__nonzero__` added
#    13-Feb-2002 (CT) `rounded` corrected to handle negative numbers correctly
#    13-Feb-2002 (CT) `rounded_as_target` simplified
#    ««revision-date»»···
#--
import re
import string

### see Fri97, p.229, p.292
sep_1000_pat = re.compile ("(\d{1,3}) (?= (?: \d\d\d)+ (?! \d) )", re.X)

class EU_Currency :
    """Root class of currency hierarchy"""

    ### if `target_currency' is not set, output is done in Euro
    target_currency = None
    to_euro_factor  = 1
    name            = "EUR"
    sloppy_name     = "EUR"
    decimal_sign    = "."
    sep_1000        = ","

    Table           = {}
    extension       = []

    def __init__ (self, amount = 0) :
        if isinstance (amount, EU_Currency) :
            self.amount = amount.amount
        else :
            self.amount = self.to_euro (amount)
    # end def __init__

    def to_euro (self, amount) :
        """Converts `amount' into Euro."""
        return amount / self.to_euro_factor
    # end def to_euro

    def __str__ (self) :
        """Return `self.amount' as string representation of
           `self.target_currency'.
        """
        (amount, cent, target_currency) = self.as_target ()
        return "%d%s%02d %s" % ( amount
                               , target_currency.decimal_sign
                               , cent
                               , target_currency.sloppy_name
                               )
    # end def __str__

    def as_target (self, round = 0, target_currency = None) :
        target_currency = target_currency or self.target_currency
        if target_currency :
            target_currency = target_currency (0)
            amount          = self.amount * target_currency.to_euro_factor
        else :
            target_currency = EU_Currency (0)
            amount          = self.amount
        (amount, cent) = target_currency.rounded (amount, round)
        return (amount, cent, target_currency)
    # end def as_target

    def rounded_as_target (self) :
        (amount, cent, target_currency) = self.as_target (round = 1)
        return target_currency.__class__ (amount)
    # end def rounded_as_target

    def as_string (self, round = 0) :
        """Return `self.amount' as string representation of
           `self.target_currency' (without currency name).
        """
        (amount, cent, target_currency) = self.as_target (round)
        return self._formatted \
            (amount, cent, target_currency.decimal_sign, round)
    # end def as_string

    def as_string_s (self, round = 0) :
        """Return result of `self.as_string ()' with 1000 separators"""
        (amount, cent, target_currency) = self.as_target (round)
        result = self._formatted \
            (amount, cent, target_currency.decimal_sign, round)
        result = sep_1000_pat.sub \
            (r"\g<1>%s" % target_currency.sep_1000, result)
        return result
    # end def as_string_s

    def as_source_s (self, round = 0) :
        """Return `self.amount` as string representation of `self.__class__`
           with 1000 separators.
        """
        (amount, cent, target_currency) = \
                 self.as_target (round, self.__class__)
        result = self._formatted \
            (amount, cent, target_currency.decimal_sign, round)
        result = sep_1000_pat.sub \
            (r"\g<1>%s" % target_currency.sep_1000, result)
        return result
    # end def as_source_s

    def rounded (self, amount, round = 0) :
        """Return `amount' rounded to (euro, cent)."""
        euro = int (amount)
        cent = abs (int (((amount - euro) + 0.005) * 100))
        if cent == 100 :
            ### for some reason sometimes `cent == 100' results
            ### `amount' and `euro' differ by 1 in this case ???
            ### print "%f, %d, %f, %d" % (amount, euro, (amount - euro), cent)
            euro += 1
            cent  = 0
        if round :
            if cent >= 50 :
                if euro >= 0 :
                    euro += 1
                else :
                    euro -= 1
            cent  = 0
        return (euro, cent)
    # end def rounded

    def formatted (self, amount, cent, name, decimal_sign) :
        """Return a string representation of `amount.cent'."""
        return "%d%s%02d %s" % (amount, decimal_sign, cent, name)
    # end def formatted

    def _formatted (self, amount, cent, decimal_sign, round) :
        if round :
            return "%d"       % (amount, )
        else :
            return "%d%s%02d" % (amount, decimal_sign, cent)
    # end def _formatted

    def __float__ (self) :
        if self.target_currency :
            target_currency = self.target_currency (0)
            amount          = self.amount * target_currency.to_euro_factor
        else :
            target_currency = EU_Currency (0)
            amount          = self.amount
        return float (amount)
    # end def __float__

    def __add__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount + rhs)
    # end def __add__

    __radd__ = __add__

    def __sub__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount - rhs)
    # end def __sub__

    __rsub__ = __sub__

    def __mul__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount * rhs)
    # end def __mul__

    __rmul__ = __mul__

    def __div__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount / rhs)
    # end def __div__

    __rdiv__ = __div__

    def __mod__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount % rhs)
    # end def __mod__

    __rmod__ = __mod__

    def __divmod__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (divmod (self.amount, rhs))
    # end def __divmod__

    __rdivmod__ = __divmod__

    def __cmp__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return cmp (self.amount, rhs)
    # end def __cmp__

    def __neg__ (self) :
        return EU_Currency (- self.amount)
    # end def __neg__

    def __pos__ (self) :
        return EU_Currency (self.amount)
    # end def __pos__

    def __abs__ (self) :
        return EU_Currency (abs (self.amount))
    # end def __abs__

    def __iadd__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        self.amount += rhs
        return self
    # end def __iadd__

    def __isub__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        self.amount -= rhs
        return self
    # end def __isub__

    def __imul__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        self.amount *= rhs
        return self
    # end def __imul__

    def __idiv__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        self.amount /= rhs
        return self
    # end def __idiv__

    def __nonzero__ (self) :
        return self.amount != 0.0
    # end def __nonzero__

# end class EU_Currency

EUR = EU_Currency

def register (currency) :
    EU_Currency.Table [currency.name]                       = currency
    EU_Currency.Table [string.lower (currency.name)]        = currency
    EU_Currency.Table [string.upper (currency.name)]        = currency
    EU_Currency.Table [currency.sloppy_name]                = currency
    EU_Currency.Table [string.lower (currency.sloppy_name)] = currency
    EU_Currency.Table [string.upper (currency.sloppy_name)] = currency
    EU_Currency.extension.append (currency)
# end def register

class ATS (EU_Currency) :
    """Austrian currency ATS"""

    to_euro_factor = 13.7603
    name           = "ATS"
    sloppy_name    = "öS"
    decimal_sign    = ","
    sep_1000        = "."
# end class ATS

class DEM (EU_Currency) :
    """German currency DEM"""

    to_euro_factor = 1.95583
    name           = "DEM"
    sloppy_name    = "DM"
# end class DEM

class FRF (EU_Currency) :
    """French currency FRF"""

    to_euro_factor = 6.55957
    name           = "FRF"
    sloppy_name    = "FF"
# end class FRF

class ITL (EU_Currency) :
    """Italian currency ITL"""

    to_euro_factor = 1936.27
    name           = "ITL"
    sloppy_name    = "ITL"
# end class ITL

class BEF (EU_Currency) :
    """Belgian currency BEF"""

    to_euro_factor = 40.3399
    name           = "BEF"
    sloppy_name    = "BF"
# end class BEF

class NLG (EU_Currency) :
    """Netherland's currency NLG"""

    to_euro_factor = 2.20371
    name           = "NLG"
    sloppy_name    = "NLG"
# end class NLG

class ESP (EU_Currency) :
    """Spanish currency ESP"""

    to_euro_factor = 166.386
    name           = "ESP"
    sloppy_name    = "ESP"
# end class ESP

class PTE (EU_Currency) :
    """Porugese currency PTE"""

    to_euro_factor = 200.482
    name           = "PTE"
    sloppy_name    = "PTE"
# end class PTE

class FIM (EU_Currency) :
    """Finnish currency FIM"""

    to_euro_factor = 5.94573
    name           = "FIM"
    sloppy_name    = "FIM"
# end class FIM

class IEP (EU_Currency) :
    """Irish currency IEP"""

    to_euro_factor = 0.787564
    name           = "IEP"
    sloppy_name    = "IEP"
# end class IEP

class LUF (EU_Currency) :
    """Luxenburg's currency LUF"""

    to_euro_factor = 40.3399
    name           = "LUF"
    sloppy_name    = "LUF"
# end class BEF

for c in EU_Currency, ATS, DEM, FRF, ITL, BEF, NLG, ESP, PTE, FIM, IEP, LUF :
    register (c)
EU_Currency.extension.sort (lambda l, r : cmp (l.name, r.name))

def currency (name) :
    return EU_Currency.Table [name]
# end def currency

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line, Opt_L
    from   predicate    import sorted
    currencies = sorted (EU_Currency.Table.keys ())
    return Command_Line ( option_spec =
                            ( Opt_L ( selection   = currencies
                                    , name        = "source"
                                    , type        = "S"
                                    , default     = "ATS"
                                    , description = "Source currency"
                                    )
                            , Opt_L ( selection   = currencies
                                    , name        = "target"
                                    , type        = "S"
                                    , default     = "EUR"
                                    , description = "Target currency"
                                    )
                            )
                        , arg_spec    = ("amount:S?Amount to convert", )
                        , description = "Convert between two Euro currencies"
                        , arg_array   = arg_array
                        )
# end def command_spec

def main (cmd) :
    Table                       = EU_Currency.Table
    source                      = Table [cmd.source]
    EU_Currency.target_currency = Table [cmd.target]
    s = source (0)
    for a in cmd.argv.body :
        if not a : continue
        b = eval   (a)
        c = source (b)
        if str (b) != a :
            b = " [%s]" % b
        else :
            b = ""
        print "%s%s %s = %s" % (a, b, source.sloppy_name, c)
        s = s + c
    if s != 0 : print "Total : %s" % s
# end def main

if __name__ == "__main__":
    main (command_spec ())
