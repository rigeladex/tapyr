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
#    17-Sep-2007 (CT) `main` refactored
#    ��revision-date�����
#--

from _ATAX.accounting   import *

par_sub_pat = re.compile ("\(([^)]+)\)")

def kassabuch (account, file) :
    """Write entries in `account' to kassabuch `file'"""
    for e in account.entries :
        if not isinstance (e, Account_Entry) :
            continue
        e.desc = par_sub_pat.sub ("[\\1]", e.desc)
        if "-" in e.dir :
            file.write \
                ( "\\A %6s %-50s (%8s) [%s]\n"
                % (e.date, e.desc, e.gross.as_string (), e.number)
                )
        elif "+" in e.dir :
            print "Income entries not yet implemented", e
# end def kassabuch

class main (Main) :

    def _create_account (self, cmd, categories, source_currency, vst_korrektur) :
        return V_Account (vst_korrektur = vst_korrektur)
    # end def _create_account

    def _output (self, cmd, account, categories, source_currency) :
        if cmd.output :
            file = open (cmd.output, "w")
        else :
            file = sys.stdout
        kassabuch (account, file)
    # end def _output

    @classmethod
    def _opt_spec (cls) :
        return super (main, cls)._opt_spec () + ("-output:S", )
    # end def _opt_spec

# end class main

if __name__ == "__main__":
    main (main.command_spec ())
### __END__ ATAX.kassabuch
