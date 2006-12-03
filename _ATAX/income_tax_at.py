# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    income_tax_at
#
# Purpose
#    Calculate income tax according to Austrian tax law
#
# Revision Dates
#    17-Nov-2002 (CT) Creation
#    14-Jan-2004 (CT) `2005` added
#    14-Dec-2005 (CT) Type of `amount` changed from `I` to `F`
#     3-Dec-2006 (CT) Import from `_TFL`
#    ««revision-date»»···
#--

from   _TFL.Date_Time    import *
from   _TFL.EU_Currency  import *

EUC  = EU_Currency
year = Date ().year

def tax_brackets (year) :
    if year < 2000 :
        return \
            ( (ATS (     50000), 0.10)
            , (ATS (    100000), 0.22)
            , (ATS (    150000), 0.32)
            , (ATS (    400000), 0.42)
            , (ATS (2000000000), 0.50)
            )
    elif year < 2002 :
        return \
            ( (ATS (     50000), 0.00)
            , (ATS (     50000), 0.21)
            , (ATS (    200000), 0.31)
            , (ATS (    400000), 0.41)
            , (ATS (2000000000), 0.50)
            )
    elif year < 2005 :
        return \
            ( (EUR (      3640), 0.00)
            , (EUR (      3630), 0.21)
            , (EUR (     14530), 0.31)
            , (EUR (     29070), 0.41)
            , (EUR (2000000000), 0.50)
            )
    else :
        return \
            ( (EUR (     10000), 0.00)
            , (EUR (     15000), 0.3833)
            , (EUR (     26000), 0.436)
            , (EUR (2000000000), 0.50)
            )
# end def tax_brackets

def tax (amount, year = year) :
    result     = 0
    brackets   = tax_brackets (year)
    remains    = amount
    tax_chunks = []
    for chunk, rate in brackets :
        if remains <= 0.0 :
            break
        if chunk > remains :
            chunk = remains
        ### don't use `-=` here (or `chunk = remains` fails)
        remains  = remains - chunk
        tc       = chunk   * rate
        result  += tc
        tax_chunks.append ((chunk, rate, tc))
    return result, tax_chunks
# end def tax

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line, Opt_L
    from   predicate    import sorted
    currencies = sorted (EU_Currency.Table.keys ())
    return Command_Line \
        ( option_spec =
            ( Opt_L ( selection   = currencies
                    , name        = "source_currency"
                    , type        = "S"
                    , default     = "EUR"
                    , description = "Source currency"
                    )
            , Opt_L ( selection   = currencies
                    , name        = "target_currency"
                    , type        = "S"
                    , default     = "EUR"
                    , description = "Target currency"
                    )
            , "-verbose:B?Show chunks, too"
            , "-year:I=%s?Year of interest" % (year, )
            )
        , arg_spec    = ("amount:F?Amount of taxable income", )
        , min_args    = 1
        , max_args    = 1
        , description = "Calculate income tax for `year`"
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    source_currency        = EUC.Table [cmd.source_currency]
    EUC.target_currency    = EUC.Table [cmd.target_currency]
    year                   = cmd.year
    amount                 = source_currency (cmd.amount)
    tax_amount, tax_chunks = tax (amount, year)
    if cmd.verbose :
        for c, r, t in tax_chunks :
            print "%2d%% for %14s : %14s" % \
                (r * 100, c.as_string_s (), t.as_string_s ())
    f = "For a taxable income of %s you pay a tax of %s (%5.2f%%) and get %s\n"
    print f % \
        ( amount, tax_amount, tax_amount.amount / (amount.amount / 100.0)
        , amount - tax_amount
        )
# end def main

if __name__ == "__main__" :
    main (command_spec ())
### __END__ income_tax_at
