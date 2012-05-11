# -*- coding: iso-8859-15 -*-
# Copyright (C) 1999-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package ATAX.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
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
#     3-Jan-2010 (CT) Use `TFL.CAO` instead of `TFL.Command_Line`
#    ««revision-date»»···
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

class Command (Command) :

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

    def _opt_spec (self) :
        return self.__super._opt_spec () + ("-output:S", )
    # end def _opt_spec

# end class Command

if __name__ == "__main__":
    Command ()
### __END__ ATAX.kassabuch
