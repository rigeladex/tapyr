# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2010 Mag. Christian Tanzer. All rights reserved
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
#    17-Sep-2007 (CT) `main` refactored
#     3-Jan-2010 (CT) Use `TFL.CAO` instead of `TFL.Command_Line`
#    ««revision-date»»···
#--

from _ATAX.accounting import *

class Command (Command) :

    default_categories  = "e"
    min_args            = 2

    def _create_account (self, cmd, categories, source_currency, vst_korrektur) :
        year       = cmd.argv.pop (0)
        konto_desc = Konto_Desc   (cmd.argv.pop (0))
        return T_Account \
            ( year          = year
            , konto_desc    = konto_desc
            , vst_korrektur = vst_korrektur
            )
    # end def _create_account

    def _output (self, cmd, account, categories, source_currency) :
        if cmd.plain :
            ATAX._.accounting.underlined = identity
        if not cmd.summary :
            account.print_konto_summary ()
            account.print_konten        ()
            print "\f"
        account.print_ein_aus_rechnung  ()
        if cmd.gewerbeanteil and account.g_anteil != 0 :
            gfile = open (cmd.gewerbeanteil, "w")
            gfile.write \
                ( """$source_currency = "%s";\n""" % EUC.target_currency.name)
            gfile.write \
                ( (" 31.12.  &    &     & %8.2f & b  & 7001  & 2000  "
                   "& -  & e &  & Büroaufwand %s \n"
                  )
                % (account.g_anteil, cmd.year)
                )
    # end def _output

    def _arg_spec (self) :
        return ("year:S", "kontenplan:P", "account_file:S")
    # end def _arg_spec

    def _opt_spec (self) :
        return self.__super._opt_spec () + \
            ( "-gewerbeanteil:P?File to write gewerbe-anteil into"
            , "-plain:B?Don't underline"
            , "-summary:B"
            )
    # end def _opt_spec

# end class Command

if __name__ == "__main__":
    Command ()
### __END__ ATAX.jahresabschluss
