# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This python module is part of Christian Tanzer's public python library
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
#    umsatzsteuer
#
# Purpose
#    Calculate monthly VAT for the austrian finance ministry
#
# Revision Dates
#    14-Jan-1999 (CT) Creation
#     7-Feb-1999 (CT) Special handling for `source_currency' added to
#                     `code_pat' processing
#    26-Feb-1999 (CT) `help_on_err = 1' passed to Command_Line
#     4-Mar-1999 (CT) Handling of `privat' added
#     3-Jan-2000 (CT) Logic of `umsatzsteuer' factored into
#                     `V_Account.add_lines'
#    26-Dec-2001 (CT) Access to cmd-options simplified
#    26-Dec-2001 (CT) Function `umsatzsteuer` moved to `accounting`
#     6-Jan-2003 (CT) Alias `umsatzsteuer` for `add_account_file` added
#    19-Feb-2006 (CT) Import from package _ATAX
#    15-May-2006 (CT) Call to `finish` added
#    11-Feb-2007 (CT) `string` functions replaced by `str` methods
#    17-Sep-2007 (CT) Modernized
#    17-Sep-2007 (CT) Use `Account.add_file`
#    17-Sep-2007 (CT) `main` refactored
#    ««revision-date»»···
#--

from _ATAX.accounting import *

sep_1000 = { "." : ",", "," : "."}

class main (Main) :

    def _add_files (self, cmd, account, categories, source_currency) :
        self.__super._add_files (cmd, account, categories, source_currency)
        account.finish ()
    # end def _add_files

    def _create_account (self, cmd, categories, source_currency, vst_korrektur) :
        if cmd.online_format :
            EUC.target_currency.decimal_sign = ","
            EUC.target_currency.sep_1000     = ""
        else :
            EUC.target_currency.decimal_sign = cmd.decimal_sign
            EUC.target_currency.sep_1000     = sep_1000 [cmd.decimal_sign]
        return V_Account (vst_korrektur = vst_korrektur)
    # end def _create_account

    def _output (self, cmd, account, categories, source_currency) :
        if cmd.online_format :
            account.print_summary_online ()
        else :
            if not cmd.summary :
                account.print_entries ("\f")
                if cmd.reverse :
                    account.print_entries_by_group ("\f")
            account.print_summary ()
    # end def _output

    @classmethod
    def _opt_spec (cls) :
        return Main._opt_spec () + \
            ( "-decimal_sign:S=."
            , "-online_format:B?Format for cope/paste into online form"
            , "-reverse"
            , "-summary"
            )
    # end def _opt_spec

# end class main

if __name__ == "__main__":
    main (main.command_spec ())
### __END__ ATAX.umsatzsteuer
