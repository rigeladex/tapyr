#!/swing/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This python module is part of Christian Tanzer's public python library
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
#    jahresabschluss
#
# Purpose
#    Sum accounting categories for one year (as required by Austrian tax law)
#
# Revision Dates
#     4-Jan-2000 (CT) Creation
#     5-Jan-2000 (CT) `gewerbeanteil' added
#     5-Jan-2000 (CT) `-plain' added
#    29-Jul-2001 (CT) Take advantage of `Command_Line.__getattr__` to access
#                     options without fuss
#    12-Feb-2002 (CT) Use `cmd.gewerbeanteil` instead of dictionary access
#     1-Dec-2002 (CT) Default of `-source_currency` and `-target_currency`
#                     changed from `ats` to `eur`
#    19-Feb-2006 (CT) Import from package _ATAX
#    11-Feb-2007 (CT) `string` functions replaced by `str` methods
#    17-Sep-2007 (CT) Modernized
#    17-Sep-2007 (CT) Use `Account.add_file`
#    ««revision-date»»···
#--

from _ATAX.accounting import *

if __name__ == "__main__":
    from _TFL.Command_Line   import Command_Line
    from sys                 import stdin
    cmd = Command_Line  \
        ( option_spec =
            ( "-all"
            , "-categories:S,=e"
            , "-gewerbeanteil:S?File to write gewerbe-anteil into"
            , "-plain:B?Don't underline"
            , "-source_currency:S=eur"
            , "-summary"
            , "-target_currency:S=eur"
            , "-vst_korrektur:F=1.0"
            )
        , arg_spec    = ( "year", "kontenplan", "account_file")
        , min_args    = 2
        , help_on_err = 1
        )
    vst_korrektur       = cmd.vst_korrektur
    summary_only        = cmd.summary
    plain               = cmd.plain
    if plain :
        def underlined (text) : return text
        from _ATAX import accounting
        accounting.underlined = underlined
    if cmd.all :
        categories      = "."
    else :
        categories      = "[" + "".join (cmd.categories) + "]"
    categ_interest      = re.compile (categories)
    source_currency     = EUC.Table [cmd.source_currency]
    EUC.target_currency = EUC.Table [cmd.target_currency]
    year                = cmd.argv.shift ()
    konto_desc          = Konto_Desc     (cmd.argv.shift ())
    account             = T_Account \
        ( year          = year
        , konto_desc    = konto_desc
        , vst_korrektur = vst_korrektur
        )
    if cmd.argn > 0 :
        for file_name in cmd.argv.body :
            account.add_file (file_name, categ_interest, source_currency)
    else :
        account.add_lines    (stdin,     categ_interest, source_currency)
    if not summary_only :
        account.print_konto_summary ()
        account.print_konten        ()
        print "\f"
    account.print_ein_aus_rechnung  ()
    if cmd.option ["gewerbeanteil"] and account.g_anteil != 0 :
        gfile = open (cmd.gewerbeanteil, "w")
        gfile.write \
            ( """$source_currency = "%s";\n""" % EUC.target_currency.name)
        gfile.write \
            ( (" 31.12.  &    &     & %8.2f & b  & 7001  & 2000  "
               "& -  & e &  & Büroaufwand %s \n"
              )
            % (account.g_anteil, year)
            )
