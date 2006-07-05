#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

from _ATAX.accounting import *

umsatzsteuer = add_account_file

sep_1000 = { "." : ",", "," : "."}

if __name__ == "__main__":
    from Command_Line   import Command_Line
    from sys            import stdin
    cmd = Command_Line  \
        ( option_spec =
            ( "-all"
            , "-categories:S=u#5"
            , "-decimal_sign:S=."
            , "-online_format:B"
                "?Format for cope/paste into online form"
            , "-reverse"
            , "-source_currency:S=eur#2"
            , "-target_currency:S=eur"
            , "-summary"
            , "-vst_korrektur:F=1.0"
            )
        , help_on_err = 1
        )
    vst_korrektur       = cmd.vst_korrektur
    summary_only        = cmd.summary
    if cmd.option ["all"] :
        categories      = "."
    else :
        categories      = "[" + \
                          (  string.join ( cmd.option ["categories"].value.body
                                         , ""
                                         )
                          or cmd.option ["categories"].value_1 ()
                          ) + "]"
    source_currency     = EUC.Table [cmd.source_currency]
    EUC.target_currency = EUC.Table [cmd.target_currency]
    if cmd.online_format :
        EUC.target_currency.decimal_sign = ","
        EUC.target_currency.sep_1000     = ""
    else :
        EUC.target_currency.decimal_sign = cmd.decimal_sign
        EUC.target_currency.sep_1000     = sep_1000 [cmd.decimal_sign]
    account             = V_Account (vst_korrektur = vst_korrektur)
    if cmd.argn > 0 :
        for file_name in cmd.argv.body :
            file = open (file_name, "r")
            add_account_file (file,  categories, source_currency, account)
    else :
        add_account_file     (stdin, categories, source_currency, account)
    account.finish ()
    if cmd.online_format :
        account.print_summary_online ()
    else :
        if not summary_only :
            account.print_entries ("\f")
            if cmd.reverse :
                account.print_entries_by_group ("\f")
        account.print_summary ()
