# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2007 Mag. Christian Tanzer. All rights reserved
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
#    kassabuch
#
# Purpose
#    Write kassabuch file for a month
#
# Revision Dates
#     9-Feb-1999 (CT) Creation
#     6-Feb-2000 (CT) `vst_korrektur' passed to `V_Account' instead of to
#                     `umsatzsteuer'
#     5-Jul-2006 (CT) Import from `_ATAX`
#    17-Sep-2007 (CT) Modernized
#    17-Sep-2007 (CT) Use `Account.add_file`
#    ««revision-date»»···
#--

from _ATAX.accounting   import *

EUC  = EU_Currency

par_sub_pat = re.compile ("\(([^)]+)\)")

def kassabuch (account, file) :
    """Write entries in `account' to kassabuch `file'"""
    for e in account.entries :
        if not isinstance (e, Account_Entry) : continue
        e.desc = par_sub_pat.sub ("[\\1]", e.desc)
        if e.dir == "-" :
            file.write \
                ( "\\A %6s %-50s (%8s) [%s]\n"
                % (e.date, e.desc, e.gross.as_string (), e.number)
                )
        elif e.dir == "+" :
            print "Income entries not yet implemented", e
# end def kassabuch

if __name__ == "__main__":
    from _TFL.Command_Line   import Command_Line
    from sys                 import stdin, stdout
    cmd = Command_Line  \
        ( option_spec =
            ( "-source_currency:S=eur#2"
            , "-target_currency:S=eur"
            , "-vst_korrektur:F=1.0"
            , "-output:S"
            )
        )
    categories          = re.compile ("[u]")
    source_currency     = EUC.Table [cmd.source_currency]
    EUC.target_currency = EUC.Table [cmd.target_currency]
    vst_korrektur       = cmd.vst_korrektur
    account             = V_Account (vst_korrektur = vst_korrektur)
    if cmd.argn > 0 :
        for file_name in cmd.argv.body :
            account.add_file (file_name, categories, source_currency)
    else :
        account.add_lines    (stdin,     categories, source_currency)
    if cmd.output :
        file = open (cmd.output, "w")
    else :
        file = stdout
    kassabuch (account, file)
