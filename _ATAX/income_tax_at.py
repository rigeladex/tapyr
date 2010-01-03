# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2010 Mag. Christian Tanzer. All rights reserved
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
#    17-Sep-2007 (CT) Use `EUC_Opt_SC` and `EUC_Opt_TC` instead of home-grown
#                     code
#     8-Jan-2009 (CT) Display `raw_value` of `cmd.amount`
#     9-Jan-2009 (CT) `2009` added, display `year`
#    16-Mar-2009 (CT) `main` changed to work with `Euro` using `Decimal`
#    16-Mar-2009 (CT) `tax_brackets` for `2009` changed to final version of law
#     3-Jan-2010 (CT) Use `TFL.CAO` instead of `TFL.Command_Line`
#    ««revision-date»»···
#--

from   _TFL.Date_Time    import *
from   _TFL.EU_Currency  import *

import _TFL.CAO

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
    elif year < 2009 :
        return \
            ( (EUR (     10000), 0.00)
            , (EUR (     15000), 0.3833)
            , (EUR (     26000), 0.436)
            , (EUR (2000000000), 0.50)
            )
    else :
        return \
            ( (EUR (     11000), 0.000)
            , (EUR (     14000), 0.3635)
            , (EUR (     35000), 0.4321429)
            , (EUR (2000000000), 0.500)
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

def _main (cmd) :
    source_currency        = cmd.source_currency
    year                   = cmd.year
    amount                 = source_currency (cmd.amount)
    tax_amount, tax_chunks = tax (amount, year)
    if cmd.verbose :
        for c, r, t in tax_chunks :
            print "%2d%% for %14s : %14s" % \
                (r * 100, c.as_string_s (), t.as_string_s ())
    f = ( "In %s, for a taxable income of %s [%s]\n"
          "    you pay a tax of %s (%5.2f%%) and get %s\n"
        )
    print f % \
        ( year, amount, cmd ["amount:raw"], tax_amount
        , (tax_amount / (amount / 100.0)).amount
        , amount - tax_amount
        )
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler     = _main
    , args        = ("amount:F?Amount of taxable income", )
    , min_args    = 1
    , max_args    = 1
    , opts        =
        ( "-verbose:B?Show chunks, too"
        , "-year:I=%s?Year of interest" % (year, )
        , EUC_Source ()
        , EUC_Target ()
        )
    , description = "Calculate income tax for `year`"
    )

if __name__ == "__main__" :
    _Command ()
### __END__ ATAX.income_tax_at
