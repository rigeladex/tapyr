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
#    ««revision-date»»···
#--
import string

class EU_Currency :
    """Root class of currency hierarchy"""

    ### if `target_currency' is not set, output is done in Euro
    target_currency = None
    to_euro_factor  = 1
    name            = "EUR"
    sloppy_name     = "EUR"
    decimal_sign    = "."

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
    
    def as_target (self) :
        if self.target_currency :
            target_currency = self.target_currency (0)
            amount          = self.amount * target_currency.to_euro_factor
        else :
            target_currency = EU_Currency (0)
            amount          = self.amount
        (amount, cent) = target_currency.rounded (amount)
        return (amount, cent, target_currency)
    # end def as_target    
        
    def as_string (self) :
        """Return `self.amount' as string representation of
           `self.target_currency' (without currency name).
        """
        (amount, cent, target_currency) = self.as_target ()
        return "%d%s%02d" % (amount, target_currency.decimal_sign, cent)
    # end def as_string
    
    def rounded (self, amount) :
        """Return `amount' rounded to (euro, cent)."""
        euro = int (amount)
        cent = abs (int (((amount - euro) + 0.005) * 100))
        if cent == 100 :
            ### for some reason sometimes `cent == 100' results
            ### `amount' and `euro' differ by 1 in this case ???
            ### print "%f, %d, %f, %d" % (amount, euro, (amount - euro), cent)
            euro = euro + 1
            cent = 0
        return (euro, cent)
    # end def rounded
    
    def formatted (self, amount, cent, name, decimal_sign) :
        """Return a string representation of `amount.cent'."""
        return "%d%s%02d %s" % (amount, decimal_sign, cent, name)
    # end def formatted

    def __add__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount + rhs)

    __radd__ = __add__

    def __sub__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount - rhs)

    __rsub__ = __sub__
                               
    def __mul__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount * rhs)   

    __rmul__ = __mul__
    
    def __div__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount / rhs)

    __rdiv__ = __div__

    def __mod__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (self.amount % rhs)

    __rmod__ = __mod__

    def __divmod__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return EU_Currency (divmod (self.amount, rhs))

    __rdivmod__ = __divmod__

    def __cmp__ (self, rhs) :
        if isinstance (rhs, EU_Currency) : rhs = rhs.amount
        return cmp (self.amount, rhs)

    def __neg__ (self) :
        return EU_Currency (- self.amount)
    
    def __pos__ (self) :
        return EU_Currency (self.amount)
    
    def __abs__ (self) :
        return EU_Currency (abs (self.amount))
    
# end class EU_Currency

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
    source                      = Table [cmd.option ["source"].value_1 ()]
    EU_Currency.target_currency = Table [cmd.option ["target"].value_1 ()]
    s = source (0)
    for a in cmd.argv.body :
        if not a : continue
        c = source (eval (a))
        print "%s %s = %s" % (a, source.sloppy_name, c)
        s = s + c
    if s != 0 : print "Total : %s" % s
# end def 

if __name__ == "__main__":
    main (command_spec ())
    
