# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2008 Mag. Christian Tanzer. All rights reserved
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
#    ATAX.accounting
#
# Purpose
#    Provide classes for accounting (adapted to Austrian tax law)
#
# Revision Dates
#    31-Jan-1999 (CT)  Creation (factored from `umsatzsteuer.py')
#    31-Jan-1999 (CT)  Use `\s' instead of ` ' in regexes
#     7-Feb-1999 (CT)  `v' added to processing of `self.g_or_n'
#     4-Mar-1999 (CT)  `perl_dict_pat' added
#     4-Mar-1999 (CT)  `privat' added
#     7-Mar-1999 (CT)  Category `z' added for Einfuhrumsatzsteuer
#     3-Jan-2000 (CT)  `V_Account.add_lines' factored from
#                      `umsatzsteuer.umsatzsteuer'
#     4-Jan-2000 (CT)  `add_lines' moved from `V_Account' to `Account'
#     4-Jan-2000 (CT)  `eval_line' factored from `add_lines'
#     4-Jan-2000 (CT)  Parameter `categ_interest' moved from `add_lines' to
#                      `add'
#     4-Jan-2000 (CT)  `T_Account' and `Konto_Desc' added
#     5-Jan-2000 (CT)  `g_anteil' added
#     9-Jan-2000 (CT)  Erlösminderung und Ausgabenminderung considered in
#                      `V_Account', too
#     9-Jan-2000 (CT)  `_add_ausgabe', `_add_einnahme', `_add_umsatz', and
#                      `_add_vorsteuer' factored
#    24-Jan-2000 (CT)  Replace `/' by `*1.0/' to avoid integer truncation by
#                      division
#    24-Jan-2000 (CT)  `Account_Entry.time_cmp' added
#    24-Jan-2000 (CT)  `Account.add_lines': sort `entries' by `time'
#     6-Feb-2000 (CT)  `Account_Entry': handling of `s' in `cat' corrected
#                      (invert `self.netto', too)
#     6-Feb-2000 (CT)  `T_Account': for entries with accounts matching
#                      `t_konto_ignore_pat', vat is added if `u' in `cat'
#     6-Feb-2000 (CT)  `T_Account': handle `i' in `cat' correctly (must be
#                      added to both `vorsteuer' and `ust')
#     6-Nov-2000 (CT)  `#' added to `ignor_pat'
#     6-Nov-2000 (CT)  Exception handler added to `Account_Entry.__init__'
#    22-Feb-2001 (CT)  Use `raise' instead of `raise exc' for re-raise
#    26-Dec-2001 (CT)  `Konto_Desc` converted to class (and added `reverse`)
#    26-Dec-2001 (CT)  `umsatzsteuer` moved in here
#    27-Dec-2001 (CT)  `H_Account_Entry` and `H_Account` added
#    28-Dec-2001 (CT)  `*_total` added to `T_Account`
#    28-Dec-2001 (CT)  `umsatzsteuer` renamed to `add_account_file`
#    12-Feb-2002 (CT)  `print_summary` changed to use argument `round` instead
#                      of home-grown code for rounding of `vat_saldo`
#    13-Feb-2002 (CT)  `print_*` changed to include `target_currency` in output
#    13-Feb-2002 (CT)  `print_sep_line` changed to use `=` instead of `-`
#     4-Aug-2002 (CT)  `ignore` dictionary added to `Account`
#     4-Aug-2002 (CT)  `830[01][23]` removed from `t_konto_ignore_pat`
#     4-Aug-2002 (CT)  `print_ein_aus_rechnung` changed to print `saldo` and
#                      to skip accounts other than 4___ and 8___ for income
#                      and accounts other than 5___, 6___, and 7___ for
#                      expenses
#    11-Mar-2003 (CT)  `V_Account.print_summary` adapted to recent changes of
#                      Austrian tax law
#    11-Mar-2003 (CT)  Code `f` added to `g_or_n`
#    15-Jun-2003 (CT)  `Privatanteil` for VAT added
#    16-Jun-2003 (CT)  `_fix_vorsteuer_privat` fixed (all of the Privatanteil
#                      is VAT-taxed, <shucks>)
#    17-Jun-2003 (CT)  Various modernizations (`+=`)
#    17-Jun-2003 (CT)  `eust_gkonto` and `ige_gkonto` added and used
#    17-Jun-2003 (CT)  Unused ballast removed (e.g., `einnahmen_total`)
#     1-Nov-2003 (CT)  `print_summary_online` added
#    21-Dec-2003 (CT)  `H_Account.__init__` redefined to set `ignore` to `{}`
#    21-Dec-2003 (CT)  `_effective_amount` factored in `T_Account` and
#                      redefined in `H_Account`
#    21-Dec-2003 (CT)  `einnahmen_total` and friends re-introduced (is used
#                      after all by bk_abrechnung.py)
#    22-Dec-2003 (CT)  `print_konten` changed to restrict `head`s length to 64
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#    24-Mar-2005 (CT)  Use `TFL.PL_Dict` and `_TFL.predicate`
#    29-Jul-2005 (CT)  `7020` added to `ausgaben_minderung_pat`
#    18-Nov-2005 (RSC) `7500` added to `ausgaben_minderung_pat`
#    11-Feb-2006 (CT)  Moved into package `ATAX`
#     1-May-2006 (CT)  `Account_Entry.__init__` changed to handle
#                      `erloes_minderung` properly
#     1-May-2006 (CT)  `Account_Entry.kontenzeile` fixed
#     8-May-2006 (CT)  Style
#     8-May-2006 (CT)  Use `TFL.defaultdict` instead of `TFL.PL_Dict`
#    15-May-2006 (CT)  `V_Account.finish` added (and then left empty, because
#                      adding correction for `privat` means major surgery)
#    11-Feb-2007 (CT)  `string` functions replaced by `str` methods
#    11-Feb-2007 (CT)  `T_Account.finish` changed to handle `vat` for
#                      `privat` correctly
#    11-Feb-2007 (CT)  `V_Account.finish` changed to consider `privat`
#    11-Feb-2007 (CT)  `T_Account._add_einnahme` and `T_Account._add_ausgabe`
#                      changed to check `entry.cat` for `u`
#    13-Jun-2007 (CT)  Argument `entry` of `V_Account._add_umsatz` made
#                      optional
#    13-Jun-2007 (CT)  `V_Account.finish` changed to consider `privat` properly
#    13-Jun-2007 (CT)  `T_Account.finish` changed to consider `privat` properly
#    13-Jun-2007 (CT)  s/_fix_vorsteuer_privat/_fix_ust_privat/g
#    13-Jun-2007 (CT)  Changed `T_Account._fix_ust_privat` to do the right
#                      thing
#    17-Sep-2007 (CT)  Function `add_account_file` replaced by method
#                      `add_file`
#    17-Sep-2007 (CT)  `Main` added
#    17-Sep-2007 (CT)  `_load_config` added
#                      * `erloes_minderung_pat` and `ausgaben_minderung_pat`
#                        moved from module-level into `Account_Entry`
#                      * CT-specific settings moved into external config file
#    17-Sep-2007 (CT)  `Account_Entry` changed to compute `minderung` based on
#                      occurrence of `~` (`erloes_minderung_pat` and
#                      `ausgaben_minderung_pat` only kept to support old input
#                      files)
#     4-Jan-2008 (CT)  `Main._load_config` changed to classmethod `load_config`
#     4-Jan-2008 (CT)  Use `Regexp` instead of `re.compile`
#    18-Feb-2008 (CT)  `kz_add` added and used
#    22-Feb-2008 (RSC) Add reverse charge
#    19-Mar-2008 (RSC) Fix issues with rev charge in Jahresabschluss
#     6-Apr-2008 (CT)  `print_summary_online` changed to only show non-zero
#                      categories
#    11-Apr-2008 (RSC) add suffix 'r' or 'i' for rev-Charge/igE in Ust column for kontenzeile
#                      (requested by E. Pichler-Fruhstorfer)
#                      Fix gkonto description for rev. Charge (cut & paste error) in finish
#    ««revision-date»»···
#--

from   _ATAX             import ATAX
from   _TFL.Command_Line import Command_Line
from   _TFL.Date_Time    import *
from   _TFL.EU_Currency  import *
from   _TFL.defaultdict  import defaultdict
from   _TFL.predicate    import *
from   _TFL.Regexp       import *

import _TFL._Meta.Object

from   _TGL              import TGL
import _TGL.load_config_file

import math
import sys
from   UserDict          import UserDict

ignor_pat              = Regexp ( r"^\s*[«%#]")
empty_pat              = Regexp ( r"^\s*$")
ws_head_pat            = Regexp ( r"^\s*")
ws_tail_pat            = Regexp ( r"\s*\n?$")
code_pat               = Regexp ( r"^\s*\$")
perl_dict_pat          = Regexp ( r"""\{\s*"?(\s*\d+\s*)"?\s*\}""")
split_pat              = Regexp ( r"\s*&\s*")
currency_pat           = Regexp ( r"([A-Za-z]+)$")
desc_strip_pat         = Regexp ( r"\s*&\s*$")

def underlined (text) :
    bu = "\b_"
    return bu.join (text) + bu
# end def underlined

class Account_Entry :
    """Entry of accounting file."""

    """Cat (several letters can be combined)::

            e       include in income tax calculations
            f       financial planning
            i       Innergemeinschaftlicher Erwerb
            k       correction
            r       reverse charge (for VAT, Article 19 [057/066 in VAT form])
            s       storno
            u       include in VAT calculations
            z       pure VAT amount

        g_or_n (exactly one letter)::

            b       gross amount
            f       VAT free
            n       net amount
            v       pure VAT amount
    """

    ### The following class variables can be overriden in a config file
    ### (e.g., ATAX.config)
    erloes_minderung_pat   = Regexp ( r"Legacy: use `~` instead")
    ausgaben_minderung_pat = Regexp ( r"Legacy: use `~` instead")

    def __init__ (self, line, source_currency, vst_korrektur = 1.0) :
        self.line = line
        try :
            ( self.date, self.number, self.vat_txt, gross,    self.g_or_n
            , self.soll, self.haben,  self.dir,     self.cat, self.plan_kat
            , self.desc
            )               = split_pat.split    (line, 10)
            self.dtuple     = day_to_time_tuple  (self.date)
        except (ValueError, TypeError), exc :
            print exc
            print line
            raise
        self.vst_korrektur  = vst_korrektur
        self.time           = mktime             (self.dtuple)
        self.desc           = desc_strip_pat.sub ("", self.desc)
        self.vat_type       = ' '
        for k in 'ir' :
            if k in self.cat :
                self.vat_type = k
                break
        currency_match      = currency_pat.search (gross)
        if currency_match :
            source_currency = EU_Currency.Table [currency_match.group (1)]
            gross           = currency_pat.sub ("", gross)
        ### avoid integer truncation by division
        ### otherwise `1/2' evaluates to `0.0' :-(
        gross      = gross.replace   ("/", "*1.0/")
        ###
        self.gross = source_currency (eval (gross, {}, {}))
        self.netto = source_currency (self.gross)
        if   "s" in self.cat :
            self.gross = - self.gross
            self.netto = - self.netto
            self.flag  = "S"
        elif "k" in self.cat :
            self.flag  = "k"
        else :
            self.flag  = " "
        self.vat_p = (eval (self.vat_txt or "0", {}, {}) / 100.0) + 1.0;
        if   "n" == self.g_or_n :
            self.gross = self.netto * self.vat_p
        elif "b" == self.g_or_n :
            self.netto = self.gross / self.vat_p
        elif "v" == self.g_or_n :
            ### entry is pure VAT amount (Einfuhr-Umsatzsteuer)
            self.netto = source_currency (0)
        self.vat       = self.gross - self.netto
        self.vat_vstk  = source_currency (0)
        self.vat_x     = source_currency (0)
        self.is_change = 1
        self.minderung = "~" in self.dir
        if   "-" in self.dir :
            self.soll_betrag   = self.netto
            self.haben_betrag  = source_currency (0)
            self.minderung     = \
                self.minderung or self.erloes_minderung_pat.match (self.haben)
            if not self.minderung :
                self.konto         = self.soll
                self.gegen_konto   = self.haben
                if self.vat_p != 1 :
                    self.vat_vstk  = self.vat
                    self.vat       = self.vat * vst_korrektur
                    self.vat_vstk -= self.vat
                    self.vat_x    = self.vat
            else :
                self.konto         = self.haben
                self.gegen_konto   = self.soll
        elif "+" in self.dir :
            self.minderung     = \
                (  self.minderung
                or self.ausgaben_minderung_pat.match (self.haben)
                )
            self.haben_betrag  = self.netto
            self.soll_betrag   = source_currency (0)
            self.konto         = self.haben
            self.gegen_konto   = self.soll
        else :
            self.is_change     = 0
        self.cati = " "
    # end def __init__

    def time_cmp (self, other) :
        """Return result of `cmp' of self and other's time"""
        return cmp (self.time, other.time)
    # end def time_cmp

    def __getattr__ (self, name) :
        return getattr (self.dtuple, name)
    # end def __getattr__

    def __str__ (self) :
        return "%6s %2.2f%s%10s %10s %10s  %-5s  %-5s %s%1s %s" % \
            ( self.date, self.vat_p, self.cati
            , self.vat.as_string   ()
            , self.netto.as_string ()
            , self.gross.as_string ()
            , self.soll, self.haben, self.dir
            , self.flag, self.desc [:18]
            )
    # end def __str__

    def kontenzeile (self) :
        ## print self.vat_p, type (self.vat_p) # self.soll_betrag, self.haben_betrag
        try :
            vat_type = getattr (self, "vat_type", ' ')
            return "%02d%02d  %-5s  %-35.35s %2s%1s %12s  %12s" % \
                ( self.day, self.month
                , self.gegen_konto
                , self.desc
                , self.vat_txt
                , vat_type
                , self._soll_betrag  ()
                , self._haben_betrag ()
                )
        except Exception, exc :
            print exc, type (self.soll_betrag), self.soll_betrag, type (self.haben_betrag), self.haben_betrag
            ### raise
    # end def kontenzeile

    def _soll_betrag (self) :
        if self.soll_betrag != 0 or "-" in self.dir :
            return self.soll_betrag.as_string_s ()
        else :
            ### if "+" not in self.dir : return "<< %s >>" % self.dir
            return ""
    # end def _soll_betrag

    def _haben_betrag (self) :
        if self.haben_betrag != 0 or "+" in self.dir :
            return self.haben_betrag.as_string_s ()
        else :
            ### if "-" not in self.dir : return "<< %s >>" % self.dir
            return ""
    # end def _haben_betrag

    def _init (self, soll_betrag, haben_betrag, gegen_konto = "3293", konto = "") :
        self.konto        = konto
        self.soll_betrag  = EU_Currency (soll_betrag)
        self.haben_betrag = EU_Currency (haben_betrag)
        self.dtuple       = day_to_time_tuple  (self.date)
        self.gegen_konto  = gegen_konto
        self.vat_txt      = self.vat_p = self.cat_i = ""
        self.soll         = self.haben = self.flag  = self.dir = ""
        self.gross        = self.netto = self.vat = EU_Currency (0)
    # end def _init

# end class Account_Entry

class Ust_Gegenbuchung (Account_Entry) :

    def __init__ (self, month, konto, soll_betrag, haben_betrag, desc) :
        self.date = "%s.%s" % (Time_Tuple.day_per_month [month - 1], month)
        self._init  (soll_betrag, haben_betrag, konto = konto)
        self.desc = "%-12s %02d" % (desc, self.dtuple.month)
    # end def __init__

# end class Ust_Gegenbuchung

class Privatanteil (Account_Entry) :

    def __init__ (self, gegen_konto, soll_betrag, haben_betrag, desc, konto = "") :
        self.date = "31.12."
        self._init  (soll_betrag, haben_betrag, gegen_konto, konto)
        self.desc = "%-12s" % (desc, )
    # end def __init__

# end class Privatanteil

class Account :
    """Account for a specific time interval (e.g., month, quarter, or year)"""

    Entry = Account_Entry

    def __init__ (self, name = "", vst_korrektur = 1.0) :
        self.name           = name
        self.vst_korrektur  = vst_korrektur
        self.gewerbe_anteil = 0
        self.entries        = []
        self.privat         = {}
        self.ignore         = set (("83003", "83013", "83006", "83016"))
        self._finished      = False
    # end def __init__

    account_vars = set (("vst_korrektur", "firma", "gewerbe_anteil"))

    def add_file (self, file_name, categ_interest, source_currency) :
        file = open (file_name, "r")
        try :
            self.add_lines (file, categ_interest, source_currency)
        finally :
            file.close ()
    # end def add_file

    def add_lines (self, lines, categ_interest, source_currency) :
        """Add entries given by `lines' to account `self'."""
        self.source_currency = source_currency
        entries = []
        for line in lines :
            if ignor_pat.match (line) : continue
            if empty_pat.match (line) : continue
            line                      = ws_head_pat.sub ("", line, count = 1)
            line                      = ws_tail_pat.sub ("", line, count = 1)
            if not line               : continue
            if code_pat.match  (line) :
                self.eval_line (line)
            else :
                entry = self.Entry \
                    (line, self.source_currency, self.vst_korrektur)
                if (categ_interest.search (entry.cat) and entry.is_change) :
                    entries.append (entry)
        entries.sort (Account_Entry.time_cmp)
        self.entries.extend (entries)
        for entry in entries :
            self.add (entry)
    # end def add_lines

    def eval_line (self, line) :
        line = code_pat.sub ("", line, count = 1)
        if perl_dict_pat.search (line) :
            line = perl_dict_pat.sub ("""["\\1"]""", line)
        ### use temporary dict for exec
        ### (`locals ()' cannot be changed by `exec')
        tmp  = { "privat" : {}, "ignore" : {}}
        try :
            ### `tmp' must be passed to the local-dict argument because
            ### Python adds some junk to the global-dict argument of `exec'
            exec line in {}, tmp
            if tmp.has_key ("source_currency") :
                self.source_currency = EUC.Table [tmp ["source_currency"]]
                del tmp ["source_currency"]
            self.privat.update (tmp ["privat"])
            self.ignore.update (tmp ["ignore"])
            del tmp ["privat"]
            del tmp ["ignore"]
            try :
                for k, v in tmp.items () :
                    if k in self.account_vars :
                        setattr (self, k, v)
                        ### print k, v, getattr (self, k)
                    else :
                        print "Invalid assignment `%s'" % line
            except Exception, exc :
                print "Exception `%s' during local-dict update `%s'" % (exc, tmp_cmd)
        except Exception, exc :
            print "Exception `%s' encountered during execution of line\n   `%s'"\
                % (exc, line)
    # end def eval_line

# end class Account

class V_Account (Account) :
    """VAT Account for a specific time interval (e.g., month, quarter, or year)"""

    ### The following class variables can be overriden in a config file
    ### (e.g., ATAX.config)
    vat_private = 1.20 ### VAT rate applicable for private part
    kz_add      = \
        { "????"  : ("027", "In 060/065 enthaltene Vorsteuern betreffend KFZ")
        }

    def __init__ (self, name = "", vst_korrektur = 1.0) :
        Account.__init__ (self, name, vst_korrektur)
        self.ausgaben_b              = EU_Currency (0)
        self.ausgaben_n              = EU_Currency (0)
        self.erwerb_igE              = EU_Currency (0)
        self.reverse_charge          = EU_Currency (0)
        self.umsatz                  = EU_Currency (0)
        self.umsatz_frei             = EU_Currency (0)
        self.ust                     = EU_Currency (0)
        self.ust_igE                 = EU_Currency (0)
        self.ust_revCharge           = EU_Currency (0)
        self.vorsteuer               = EU_Currency (0)
        self.vorsteuer_igE           = EU_Currency (0)
        self.vorsteuer_revCh         = EU_Currency (0)
        self.vorsteuer_EUst          = EU_Currency (0)
        self.erwerb_igE_dict         = defaultdict (EU_Currency)
        self.reverse_charge_dict     = defaultdict (EU_Currency)
        self.umsatz_dict             = defaultdict (EU_Currency)
        self.ust_dict                = defaultdict (EU_Currency)
        self.ust_igE_dict            = defaultdict (EU_Currency)
        self.ust_revC_dict           = defaultdict (EU_Currency)
        self.vorsteuer_kzs           = defaultdict (EU_Currency)
        self.umsatzsteuer_entries    = []
        self.vorsteuer_entries       = []
        self.vorsteuer_entries_igE   = []
        self.vorsteuer_entries_revC  = []
        self.vorsteuer_entries_EUst  = []
    # end def __init__

    def add (self, entry) :
        """Add `entry' to U_Account."""
        assert (isinstance (entry, Account_Entry))
        vst_korrektur = entry.vst_korrektur
        netto         = entry.netto
        gross         = entry.gross
        vat           = entry.vat
        vat_p         = entry.vat_p
        if   "-" in entry.dir :
            self.ausgaben_b  += gross
            self.ausgaben_n  += netto
            if "i" in entry.cat :
                self.vorsteuer_igE += vat
                self.ust_igE       += vat
                self.vorsteuer_entries_igE.append (entry)
                entry.cati = "i"
                self.ust_igE_dict  [vat_p]   += vat
                self.erwerb_igE              += netto
                self.erwerb_igE_dict [vat_p] += netto
                if vst_korrektur != 1.0 :
                    sys.stderr.write \
                        ( "Cannot handle expenses resulting from "
                          "innergemeinschaftlichem Erwerb for a "
                          "VAT correction of %d\n       %s\n"
                        % (vst_korrektur, entry)
                        )
                elif "b" == entry.g_or_n :
                    sys.stderr.write \
                        ( "**** igE entries must be netto****\n       %s\n"
                        % entry
                        )
                if entry.konto in self.kz_add :
                    self.vorsteuer_kzs [self.kz_add [entry.konto]] += vat
            elif "r" in entry.cat :
                self.vorsteuer_revCh     += vat
                self.ust_revCharge       += vat
                self.vorsteuer_entries_revC.append (entry)
                entry.cati = "r"
                self.ust_revC_dict  [vat_p]      += vat
                self.reverse_charge              += netto
                self.reverse_charge_dict [vat_p] += netto
                if vst_korrektur != 1.0 :
                    sys.stderr.write \
                        ( "Cannot handle expenses resulting from "
                          "reverse Charge for a "
                          "VAT correction of %d\n       %s\n"
                        % (vst_korrektur, entry)
                        )
                elif "b" == entry.g_or_n :
                    sys.stderr.write \
                        ( "**** reverse Charge entries must be netto****\n"
                          "       %s\n"
                        % entry
                        )
                if entry.konto in self.kz_add :
                    self.vorsteuer_kzs [self.kz_add [entry.konto]] += vat
            elif "z" in entry.cat :
                self.vorsteuer_EUst += vat
                self.vorsteuer_entries_EUst.append (entry)
                entry.cati = "E"
                if vst_korrektur != 1.0 :
                    sys.stderr.write \
                        ( "Cannot handle Einfuhrumsatzsteuer for a "
                          "VAT correction of %d\n       %s\n"
                        % (vst_korrektur, entry)
                        )
            else : ### neither "i" nor "z" nor "r"
                self.vorsteuer_entries.append (entry)
                if entry.minderung :
                    ## Erlösminderung instead of Ausgabe
                    self._add_umsatz    (- netto, - vat, vat_p, entry)
                else :
                    self._add_vorsteuer (vat)
                    if entry.konto in self.kz_add :
                        self.vorsteuer_kzs [self.kz_add [entry.konto]] += vat
        elif "+" in entry.dir :
            self.umsatzsteuer_entries.append (entry)
            if "i" in entry.cat :
                sys.stderr.write \
                    ( "Cannot handle income resulting from "
                      "innergemeinschaftlichem Erwerb\n       %s\n"
                    % entry
                    )
            if "r" in entry.cat :
                sys.stderr.write \
                    ( "Cannot handle income resulting from "
                      "reverse Charge\n       %s\n"
                    % entry
                    )
            if entry.minderung :
                ## Ausgabenminderung instead of Einnahme
                self._add_vorsteuer (- vat)
            else :
                self._add_umsatz    (netto, vat, vat_p, entry)
    # end def add

    def _add_umsatz (self, netto, vat, vat_p, entry = None) :
        self.ust                  += vat
        self.umsatz               += netto
        self.umsatz_dict [vat_p]  += netto
        if entry and entry.g_or_n == "f" :
            self.umsatz_frei      += netto
        elif vat_p != 1.0 :
            self.ust_dict [vat_p] += vat
    # end def _add_umsatz

    def _add_vorsteuer (self, vat) :
        self.vorsteuer += vat
    # end def _add_vorsteuer

    def finish (self) :
        if not self._finished :
            self._finished = True
            netto = EU_Currency (0)
            p_vat = EU_Currency (0)
            vat_p = self.vat_private
            for entry in self.vorsteuer_entries :
                k = entry.konto
                if k in self.privat and entry.netto > 0 :
                    factor = self.privat [k] / 100.0
                    corr   = entry.netto * factor
                    netto += corr
                    p_vat += corr * (vat_p - 1.00)
            if netto :
                self._add_umsatz (netto, p_vat, vat_p)
    # end def finish

    def header_string (self) :
        return " %s   %8s%7s   %8s   %8s  %-5s %-5s %s  %s\n%s" % \
            ( "Tag"
            ,      "MSt-Satz"
            ,         "MWSt"
            ,               "Netto"
            ,                     "Brutto"
            ,                          "Soll"
            ,                               "Haben"
            ,                                    "  "
            ,                                        "Text"
            ,                                            "=" * 80
            )
    # end def header_string

    def print_entries (self, trailer = None) :
        """Print `self.entries' followed by trailer"""
        self.print_entries_ (self.entries, self.header_string (), trailer)
    # end def print_entries

    def print_entries_by_group (self, trailer = None) :
        """Print `self.vorsteuer_entries', `self.vorsteuer_entries_igE', and
           `self.umsatzsteuer_entries' followed by trailer.
        """
        if  (  self.vorsteuer_entries
            or self.vorsteuer_entries_EUst
            or self.vorsteuer_entries_igE
            or self.vorsteuer_entries_revC
            or self.umsatzsteuer_entries
            ) :
            print self.header_string ()
        self.print_entries_ (self.vorsteuer_entries,      trailer = "\n")
        self.print_entries_ (self.vorsteuer_entries_EUst, trailer = "\n")
        self.print_entries_ (self.vorsteuer_entries_igE,  trailer = "\n")
        self.print_entries_ (self.vorsteuer_entries_revC, trailer = "\n")
        self.print_entries_ (self.umsatzsteuer_entries)
        if  (  self.vorsteuer_entries
            or self.vorsteuer_entries_EUst
            or self.vorsteuer_entries_igE
            or self.vorsteuer_entries_revC
            or self.umsatzsteuer_entries
            ) :
            if trailer : print trailer
    # end def print_entries_by_group

    def print_entries_ (self, entries, header = None, trailer = None) :
        if entries :
            if header        : print header
            for e in entries : print e
            if trailer       : print trailer
    # end def print_entries_

    def print_summary_old (self) :
        """Print summary for Umsatzsteuervoranmeldung."""
        vat_saldo = self.ust - self.vorsteuer - self.vorsteuer_EUst
        meldung   = ("Überschuss", "Vorauszahlung") [vat_saldo >= 0]
        sign      = (-1.0,         +1.0)            [vat_saldo >= 0]
        print "%-16s : %14s"   % \
            ("Ausgaben brutto", self.ausgaben_b.as_string_s ())
        print "%-16s : %14s"   % \
            ("Ausgaben netto",  self.ausgaben_n.as_string_s ())
        print "\n%s\n"         % ( "=" * 80, )
        print "%-16s : %14s"   % ( "Umsatz", self.umsatz.as_string_s ())
        print "%-16s : %14s"   % \
            ( "Steuerpflichtig"
            , (self.umsatz - self.umsatz_dict [1.0]).as_string_s ()
            )
        self.print_ust_dict_     ( self.umsatz_dict, self.ust_dict)
        print "\n%-16s : %14s" % \
            ("Erwerbe igE", self.erwerb_igE.as_string_s ())
        self.print_ust_dict_     ( self.erwerb_igE_dict, self.ust_igE_dict)
        print "\n%-16s : %14s" % \
            ("Reverse Charge", self.reverse_charge.as_string_s ())
        self.print_ust_dict_     ( self.reverse_charge_dict, self.ust_revC_dict)
        print "\n%-16s :                %14s" % \
            ( "USt Übertrag"
            , (self.ust + self.ust_igE + self.ust_revCharge).as_string_s ()
            )
        print "--------------- ./.. ---------------------------";
        print "%-16s :                %14s" % \
            ( "USt Übertrag"
            , (self.ust + self.ust_igE + self.ust_revCharge).as_string_s ()
            )
        print "%-16s : %14s" % \
            ( "Vorsteuer", self.vorsteuer.as_string_s ())
        print "%-16s : %14s"   % \
            ("Einfuhrumsatzst.", self.vorsteuer_EUst.as_string_s ())
        print "%-16s : %14s"   % \
            ( "Vorsteuer igE", self.vorsteuer_igE.as_string_s ())
        print "%-16s : %14s %14s" % \
            ( "Summe Vorsteuer"
            , ( self.vorsteuer     + self.vorsteuer_EUst
              + self.vorsteuer_igE + self.vorsteuer_revCh
              ).as_string_s ()
            , ( self.vorsteuer     + self.vorsteuer_EUst
              + self.vorsteuer_igE + self.vorsteuer_revCh
              ).as_string_s ()
            )
        if vat_saldo.target_currency == EU_Currency :
            ### no rounding for Euro
            print "\n%-16s :                %14s %s" % \
                ( meldung
                , vat_saldo.as_string_s (), vat_saldo.target_currency.name
                )
        else :
            ### rounding is necessary
            print "\n%-16s :             %14s%s00 %s     (%s)" % \
                ( meldung
                , vat_saldo.as_string_s (round = 1)
                , vat_saldo.target_currency.decimal_sign
                , vat_saldo.target_currency.name
                , vat_saldo.as_string_s ()
                )
    # end def print_summary_old

    def print_summary (self) :
        """Print summary for Umsatzsteuervoranmeldung."""
        vat_saldo    = self.ust - self.vorsteuer - self.vorsteuer_EUst
        meldung      = ("Überschuss", "Vorauszahlung") [vat_saldo >= 0]
        sign         = (-1.0,         +1.0)            [vat_saldo >= 0]
        umsatz_vat   = self.umsatz - self.umsatz_frei
        print "%-30s     : %29s" % \
            ("Ausgaben brutto", self.ausgaben_b.as_string_s ())
        print "%-30s     : %29s" % \
            ("Ausgaben netto", self.ausgaben_n.as_string_s ())
        print "\n%s\n"           % ( "=" * 80, )
        print "%-30s %3s : %29s" % \
            ("Nichtsteuerbar Ausland", "005", self.umsatz_frei.as_string_s())
        print "%-30s %3s : %29s" % \
            ("Lieferungen, sonstige", "000", umsatz_vat.as_string_s ())
        print "%-30s     : %29s" % \
            ("Summe Bemessungsgrundlage", umsatz_vat.as_string_s ())
        print
        print "%-30s     : %29s" % \
            ("Gesamt steuerpflichtig", umsatz_vat.as_string_s ())
        self.print_ust_dict_  (self.umsatz_dict, self.ust_dict, self._ust_cat)
        print "%-30s %3s : %29s" % \
            ("Reverse Charge §19", "057", self.vorsteuer_revCh.as_string_s ())
        print
        print "%-30s     : %29s" % ( "USt Übertrag", self.ust.as_string_s ())
        print "--------------------------------- ./.. ---------------------------"

        print "%-30s     : %29s" % ( "USt Übertrag", self.ust.as_string_s ())

        print "%-30s %3s : %14s" % \
            ("Erwerbe igE", "070", self.erwerb_igE.as_string_s ())
        self.print_ust_dict_ \
            (self.erwerb_igE_dict, self.ust_igE_dict, self._ige_cat)

        print "%-30s %3s : %29s" % \
            ("Vorsteuer", "060", self.vorsteuer.as_string_s ())
        print "%-30s %3s : %29s" % \
            ("Einfuhrumsatzsteuer", "061", self.vorsteuer_EUst.as_string_s())
        print "%-30s %3s : %29s" % \
            ("Vorsteuer igE", "065", self.vorsteuer_igE.as_string_s ())
        print "%-30s %3s : %29s" % \
            ("Reverse Charge §19", "066", self.vorsteuer_revCh.as_string_s ())
        for (k, d), vst in sorted (self.vorsteuer_kzs.iteritems ()) :
            print "%-30.30s %3s : %29s" % (d, k, vst.as_string_s ())
        print "%-30s     : %29s" % \
            ( "Gesamtbetrag Vorsteuer"
            , ( self.vorsteuer     + self.vorsteuer_EUst
              + self.vorsteuer_igE + self.vorsteuer_revCh
              ).as_string_s ()
            )
        print
        if vat_saldo.target_currency == EU_Currency :
            ### no rounding for Euro
            print "%-30s %3s : %29s %s" % \
                ( meldung, "095"
                , vat_saldo.as_string_s (), vat_saldo.target_currency.name
                )
        else :
            ### rounding is necessary
            print "%-30s %3s : %29s%s00 %s     (%s)" % \
                ( meldung, "095"
                , vat_saldo.as_string_s (round = 1)
                , vat_saldo.target_currency.decimal_sign
                , vat_saldo.target_currency.name
                , vat_saldo.as_string_s ()
                )
    # end def print_summary

    def print_summary_online (self) :
        """Print summary for Umsatzsteuervoranmeldung for online entry."""
        vat_saldo    = self.ust - self.vorsteuer - self.vorsteuer_EUst
        meldung      = ("Überschuss", "Vorauszahlung") [vat_saldo >= 0]
        sign         = (-1.0,         +1.0)            [vat_saldo >= 0]
        umsatz_vat   = self.umsatz - self.umsatz_frei
        print "*** Lieferungen, sonstige Leistungen und Eigenverbrauch ***"
        print "=" * 67
        if umsatz_vat :
            print "%-50s %3s : %10s" % \
                ("Lieferungen, sonstige", "000", umsatz_vat.as_string_s ())
        if self.umsatz_frei :
            print "%-50s %3s : %10s" % \
                ( "Nichtsteuerbar Ausland", "005"
                , self.umsatz_frei.as_string_s ()
                )
        if umsatz_vat :
            print
            print "Steuersätze"
            print "=" * 67
            self.print_ust_dict_online (self.umsatz_dict, self._ust_cat)
        if self.vorsteuer_revCh :
            print "\n%-50s %3s : %10s" % \
                ( "Reverse Charge §19", "057"
                , self.vorsteuer_revCh.as_string_s ()
                )
        print "\n\n"
        print "*** Innergemeinschaftliche Erwerbe ***"
        print "=" * 67
        if self.erwerb_igE :
            print "%-50s %3s : %10s" % \
                ("Erwerbe igE", "070", self.erwerb_igE.as_string_s ())
            print
            print "Steuersätze"
            print "=" * 47
            self.print_ust_dict_online (self.erwerb_igE_dict, self._ige_cat)

        print "\n\n"
        print "*** Vorsteuer ***"
        print "=" * 67
        print "%-50s %3s : %10s" % \
            ("Vorsteuer", "060", self.vorsteuer.as_string_s ())
        if self.vorsteuer_EUst:
            print "%-50s %3s : %10s" % \
                ("Einfuhrumsatzsteuer", "061", self.vorsteuer_EUst.as_string_s())
        if self.vorsteuer_igE :
            print "%-50s %3s : %10s" % \
                ("Vorsteuer igE", "065", self.vorsteuer_igE.as_string_s ())
        if self.vorsteuer_revCh :
            print "%-50s %3s : %10s" % \
                ("Reverse Charge §19", "066", self.vorsteuer_revCh.as_string_s ())
        for (k, d), vst in sorted (self.vorsteuer_kzs.iteritems ()) :
            print "%-50.50s %3s : %10s" % (d, k, vst.as_string_s ())
        print "\n\n"
        print "*" * 67
        if vat_saldo.target_currency == EU_Currency :
            ### no rounding for Euro
            print "%-50s %3s : %10s %s" % \
                ( meldung, "095"
                , vat_saldo.as_string_s (), vat_saldo.target_currency.name
                )
        else :
            ### rounding is necessary
            print "%-50s %3s : %10s%s00 %s     (%s)" % \
                ( meldung, "095"
                , vat_saldo.as_string_s (round = 1)
                , vat_saldo.target_currency.decimal_sign
                , vat_saldo.target_currency.name
                , vat_saldo.as_string_s ()
                )
    # end def print_summary_online

    _ust_cat = {20 : "022", 10 : "029", 0 : ""}
    _ige_cat = {20 : "072", 10 : "073", 0 : ""}

    def print_ust_dict_ (self, umsatz_dict, ust_dict, cat) :
        for vat_p in sorted (umsatz_dict, reverse = True) :
            vp = int (((vat_p - 1) * 100) + 0.5)
            print "davon %2d%%                      %3s : %14s %14s" % \
                ( vp, cat [vp]
                , umsatz_dict [vat_p].as_string_s ()
                , ust_dict    [vat_p].as_string_s ()
                )
    # end def print_ust_dict_

    def print_ust_dict_online (self, umsatz_dict, cat) :
        for vat_p in sorted (umsatz_dict, reverse = True) :
            ust = umsatz_dict [vat_p]
            if ust :
                vp = int (((vat_p - 1) * 100) + 0.5)
                hd = "davon %2d%%" % (vp, )
                print "%-50s %3s : %10s" % (hd, cat [vp], ust.as_string_s ())
    # end def print_ust_dict_online

# end class U_Account

class T_Account (Account) :
    """Account total for a specific time interval (e.g., month, quarter, or year.)"""

    ### The following class variables can be overriden in a config file
    ### (e.g., ATAX.config)
    eust_gkonto        = "9997"
    ige_gkonto         = "9998"
    rvc_gkonto         = "9996"
    ust_gkonto         = "9999"
    vorsteuer_gkonto   = "9999"
    t_konto_ignore_pat = Regexp (r"^[01239]\d\d\d\d?", re.X)
    firma              = "<<<Specify in config file, e.g., ATAX.config>>>"

    def __init__ (self, name = "", year = 0, konto_desc = None, vst_korrektur = 1.0) :
        Account.__init__ (self, name, vst_korrektur)
        self.year                           = year or \
             day_to_time_tuple ("1.1").year - 1
        self.konto_desc                     = konto_desc or {}
        self.soll_saldo                     = defaultdict (EU_Currency)
        self.haben_saldo                    = defaultdict (EU_Currency)
        self.ausgaben                       = defaultdict (EU_Currency)
        self.einnahmen                      = defaultdict (EU_Currency)
        self.vorsteuer                      = defaultdict (EU_Currency)
        self.vorsteuer_EUst                 = defaultdict (EU_Currency)
        self.ust                            = defaultdict (EU_Currency)
        self.ust_igE                        = defaultdict (EU_Currency)
        self.ust_revCharge                  = defaultdict (EU_Currency)
        self.buchung_zahl                   = defaultdict (int)
        self.ausgaben_total                 = EU_Currency (0)
        self.einnahmen_total                = EU_Currency (0)
        self.vorsteuer_total                = EU_Currency (0)
        self.ust_total                      = EU_Currency (0)
        self.k_entries                      = defaultdict (list)
        self.kblatt                         = defaultdict (list)
        self.kblatt [self.vorsteuer_gkonto] = []
        self.kblatt [self.ust_gkonto]       = []
    # end def __init__

    def add (self, entry) :
        """Add `entry' to account `self'."""
        assert (isinstance (entry, Account_Entry))
        self.buchung_zahl [entry.konto]       += 1
        self.buchung_zahl [entry.gegen_konto] += 1
        self.kblatt       [entry.konto].append (entry.kontenzeile ())
        self.k_entries    [entry.konto].append (entry)
        if "-" in entry.dir :
            self.soll_saldo  [entry.konto]       += entry.soll_betrag
            self.haben_saldo [entry.gegen_konto] += entry.soll_betrag
            if  (  (not self.t_konto_ignore_pat.match (entry.konto))
                or ("u" in entry.cat)
                ) :
                betrag = (entry.soll_betrag, 0) \
                    [(    self.t_konto_ignore_pat.match (entry.konto)
                      and "u" in entry.cat
                     ) or entry.konto in self.ignore
                    ]
                betrag = self._effective_amount (entry, entry.soll_betrag)
                if entry.minderung :
                    ## Erlösminderung instead of Ausgabe
                    self._add_einnahme (entry, - betrag, - entry.vat)
                else :
                    self._add_ausgabe  (entry, + betrag, + entry.vat)
            else :
                pass
                #print "%s not added to self.ausgaben" % entry.konto
        elif "+" in entry.dir :
            self.haben_saldo [entry.konto]       += entry.haben_betrag
            self.soll_saldo  [entry.gegen_konto] += entry.haben_betrag
            if  (  (not self.t_konto_ignore_pat.match (entry.konto))
                or ("u" in entry.cat) ### ???  6-Feb-2000 ??? ###
                ) :
                betrag = (entry.haben_betrag, 0) \
                    [(    self.t_konto_ignore_pat.match (entry.konto)
                      and "u" in entry.cat
                     ) or entry.konto in self.ignore
                    ]
                betrag = self._effective_amount (entry, entry.haben_betrag)
                if entry.minderung :
                    ## Ausgabenminderung instead of Einnahme
                    self._add_ausgabe  (entry, - betrag, - entry.vat)
                else :
                    self._add_einnahme (entry, + betrag, + entry.vat)
            else :
                pass #print "%s not added to self.einnahmen" % entry.konto
    # end def add

    def _effective_amount (self, entry, amount) :
        if  (    self.t_konto_ignore_pat.match (entry.konto)
            and "u" in entry.cat
            ) or entry.konto in self.ignore :
            return 0
        else :
            return amount
    # end def _effective_amount

    def _add_ausgabe (self, entry, betrag, vat) :
        if "u" in entry.cat :
            if "i" in entry.cat :
                vat_dict = self.ust_igE
            elif "r" in entry.cat :
                vat_dict = self.ust_revCharge
            elif "z" in entry.cat :
                vat_dict = self.vorsteuer_EUst
            else :
                vat_dict = self.vorsteuer
            vat_dict      [entry.month] += vat
            self.vorsteuer_total        += vat
        self.ausgaben [entry.konto] += betrag
        self.ausgaben_total         += betrag
    # end def _add_ausgabe

    def _add_einnahme (self, entry, betrag, vat) :
        if "u" in entry.cat :
            if "i" in entry.cat :
                ust_dict = self.ust_igE
            elif "r" in entry.cat :
                ust_dict = self.ust_revCharge
            else :
                if "z" in entry.cat :
                    print "*** Einnahme cannot include Einfuhrumsatzsteuer"
                    print entry.line
                ust_dict = self.ust
            ust_dict       [entry.month] += vat
            self.ust_total               += vat
        self.einnahmen [entry.konto] += betrag
        self.einnahmen_total         += betrag
     # end def _add_einnahme

    def finish (self) :
        if not self._finished :
            self._finished = True
            self._do_gkonto \
                ( self.vorsteuer,   self.vorsteuer_gkonto
                , self.soll_saldo,  "Vorsteuer"
                , lambda s : (s, 0)
                )
            self._do_gkonto \
                ( self.vorsteuer_EUst, self.eust_gkonto
                , self.soll_saldo,     "Einfuhrumsatzsteuer"
                , lambda s : (s, 0)
                )
            self._do_gkonto \
                ( self.ust,            self.ust_gkonto
                , self.haben_saldo,    "Umsatzsteuer"
                , lambda s : (0, s)
                )
            self._do_gkonto \
                ( self.ust_igE,        self.ige_gkonto
                , self.soll_saldo,     "Vor- und Umsatzsteuer igE"
                , lambda s : (s, s)
                , self.haben_saldo
                )
            self._do_gkonto \
                ( self.ust_revCharge,  self.rvc_gkonto
                , self.soll_saldo,     "Vor- und Umsatzsteuer rev. Ch."
                , lambda s : (s, s)
                , self.haben_saldo
                )
            for k in sorted (self.kblatt) :
                if k in self.privat :
                    pa      = self.privat [k]
                    factor  = pa / 100.0
                    p_soll  = self.soll_saldo  [k] * factor
                    p_haben = self.haben_saldo [k] * factor
                    p_desc  = ("%2d%% Privatanteil" % (int (pa + 0.5),))
                    k_desc  = self.konto_desc.get (k, "")
                    self.soll_saldo  [k] -= p_soll
                    self.haben_saldo [k] -= p_haben
                    self.ausgaben    [k] *= (1 - factor)
                    self.einnahmen   [k] *= (1 - factor)
                    self.konto_desc  [k]  = "%s (abz. %s)" % (k_desc, p_desc)
                    self.kblatt [k].append \
                        ( Privatanteil
                            ("9200", -p_soll, -p_haben, p_desc).kontenzeile ()
                        )
                    p_vat = p_soll * 0.20
                    self._fix_ust_privat (k, k_desc, p_vat, p_desc)
    # end def finish

    def _do_gkonto (self, ust, gkonto, saldo, txt, soll_haben, saldo2 = None) :
        for m in sorted (ust) :
            if ust.get (m, 0) != 0 :
                self.buchung_zahl [gkonto] += 1
                saldo             [gkonto] += ust [m]
                if saldo2 is not None :
                    saldo2        [gkonto] += ust [m]
                s, h                        = soll_haben (ust [m])
                self.kblatt.setdefault (gkonto, []).append \
                    (Ust_Gegenbuchung (m, gkonto, s, h, txt).kontenzeile ())
    # end def _do_gkonto

    def _fix_ust_privat (self, k, k_desc, p_soll, p_desc) :
        p_desc = "%s [%s (%s)]" % (p_desc, k, k_desc)
        gkonto = self.ust_gkonto
        self.buchung_zahl [gkonto] += 1
        self.haben_saldo  [gkonto] -= p_soll
        self.kblatt.setdefault (gkonto, []).append \
            (Privatanteil ("9200", 0, p_soll, p_desc, gkonto).kontenzeile ())
    # end def _fix_ust_privat

    def print_konten (self) :
        self.finish ()
        tc = EU_Currency.target_currency.name
        for k in sorted (self.kblatt) :
            head  = "%s    %s" % (self.year, self.konto_desc.get (k, "")) [:64]
            tail  = "Konto-Nr. %5s" % k
            belly = " " * (79 - len (head) - len (tail))
            print "\n\n%s%s%s" % (head, belly, tail)
            self.print_sep_line ()
            print "%-4s %-6s  %-35s%-3s  %12s  %12s" % \
                ("Tag", "Gegkto", "Text", "Ust", "Soll", "Haben")
            self.print_sep_line ()
            print "\n".join (self.kblatt [k])
            print "\n%12s %-38s  %12s  %12s" % \
                ( "", "Kontostand neu"
                , self.soll_saldo  [k].as_string_s ()
                , self.haben_saldo [k].as_string_s ()
                )
            print "\n%12s %-48s  %12s %s" % \
                ( ""
                , "Saldo      neu"
                , (self.soll_saldo [k] - self.haben_saldo [k]).as_string_s ()
                , tc
                )
            self.print_sep_line ()
    # end def print_konten

    def print_konto_summary (self) :
        self.finish ()
        tc = EU_Currency.target_currency.name
        print "Zusammenfassung Konten %-52s %s" % (self.year, tc)
        self.print_sep_line ()
        print "%-5s %12s %12s  %12s %s" % \
            ("Konto", "Soll", "Haben", "Saldo", "Text")
        self.print_sep_line ()
        for k in sorted (self.kblatt) :
            print "%-5s%13s%13s %13s %s" % \
                ( k
                , self.soll_saldo  [k].as_string_s ()
                , self.haben_saldo [k].as_string_s ()
                , (self.soll_saldo [k] - self.haben_saldo [k]).as_string_s ()
                , self.konto_desc.get (k, "") [:33]
                )
    # end def print_konto_summary

    def print_sep_line (self) :
        print "%s" % ("=" * 79, )
    # end def print_sep_line

    def print_ein_aus_rechnung (self) :
        self.finish ()
        tc = EU_Currency.target_currency.name
        print self.firma
        print underlined \
            ("Einnahmen/Ausgabenrechnung %s (%s)" % (self.year, tc))
        print "\n"
        print underlined ("Betriebseinnahmen")
        print "\n"
        format  = "%-40s %15s %15s"
        format1 = "%-40s -%14s %15s"
        e_total = EU_Currency (0)
        for k in sorted (self.einnahmen) :
            einnahmen = self.einnahmen [k] - self.ausgaben [k]
            if k [0] not in ("4", "8") : continue
            if einnahmen == 0          : continue
            e_total = e_total + einnahmen
            print format % \
                ( self.konto_desc.get (k, "") [:40], ""
                , einnahmen.as_string_s ()
                )
        print format % ("", "", "_" * 15)
        print format % ("", "", e_total.as_string_s ()), tc
        print "\n"
        print underlined ("Betriebsausgaben")
        print "\n"
        a_total = EU_Currency (0)
        for k in sorted (self.ausgaben) :
            ausgaben = self.ausgaben [k] - self.einnahmen [k]
            if k [0] not in ("5", "6", "7") : continue
            if ausgaben == 0                : continue
            a_total = a_total + ausgaben
            print format % \
                ( self.konto_desc.get (k, "") [:40]
                , ausgaben.as_string_s (), ""
                )
        if self.vst_korrektur != 1 :
            p_anteil = a_total * (1 - self.vst_korrektur)
            print format  % ( "", "_" * 15, "")
            print format  % ( "", a_total.as_string_s (), "")
            print format1 % \
                ( "Privatanteil  %5.2f%%" % ((1 - self.vst_korrektur) * 100, )
                , p_anteil.as_string_s (), ""
                )
            if self.gewerbe_anteil :
                self.g_anteil = g_anteil = a_total * self.gewerbe_anteil
                print format1 % \
                    ( "Gewerbeanteil %5.2f%%" % (self.gewerbe_anteil * 100, )
                    , g_anteil.as_string_s (), ""
                    )
            else :
                g_anteil = 0
            a_total = a_total - p_anteil - g_anteil
        print format  % ( "", "_" * 15, "_" * 15)
        print format1 % \
            ( ""
            , a_total.as_string_s ()
            , (e_total - a_total).as_string_s ()
            ), tc
        print \
            ( "\nDas Ergebnis wurde gemäß Par.4/3 EStG nach der "
              "Nettomethode erstellt."
            )
    # end def print_ein_aus_rechnung

    g_anteil = EU_Currency (0)

# end class T_Account

class H_Account_Entry (Account_Entry) :
    """Entry of H_Account"""

    Ancestor = __Ancestor = Account_Entry

    def __init__ (self, * args, ** kw) :
        self.__Ancestor.__init__ (self, * args, ** kw)
        if "-" in self.dir and self.vat_p != 1 :
            self.netto       += self.vat_vstk
            self.soll_betrag += self.vat_vstk
    # end def __init__

    def kontenzeile (self) :
        try :
            return \
                ( "\\Einzelposten{%s\\hfill %s}{%s%s}"
                % (self.desc, self.date, self.dir, self.netto.as_string ())
                )
        except Exception, exc :
            print exc
            print sorted (self.__dict__.items ())
            raise
    # end def kontenzeile

# end class H_Account_Entry

class H_Account (T_Account) :
    """House account for a specific time interval."""

    Ancestor = __Ancestor = T_Account
    Entry    = H_Account_Entry
    t_konto_ignore_pat = Regexp (r"^DON'T MATCH ANYTHING HERE$", re.X)

    def __init__ (self, * args, ** kw) :
        self.__Ancestor.__init__ (self, * args, ** kw)
        self.ignore = set ()
    # end def __init__

    def _effective_amount (self, entry, amount) :
        return amount
    # end def _effective_amount

# end class H_Account

class Konto_Desc (UserDict) :
    """Model kontenplan of austrian accounting system"""

    def __init__ (self, file) :
        UserDict.__init__ (self)
        k_d = self.data
        d_k = self.reverse = {}
        if isinstance (file, str) :
            file = open (file, "r")
        pat   = Regexp (r"^[0-9]")
        s_pat = Regexp (r"\s*:\s*")
        for line in file :
            if not pat.match (line) : continue
            (konto, desc)  = s_pat.split (line)
            konto          = konto.replace ("_", "0").strip ()
            desc           = desc.replace  ('"', "" ).strip ()
            k_d [konto]    = desc
            d_k [desc]     = konto
    # end def __init__

# end class Konto_Desc

class Main (TFL.Meta.Object) :
    """Main class for accounting scripts"""

    default_categories  = "u"
    max_args            = None
    min_args            = None

    def __init__ (self, cmd) :
        self.load_config (cmd)
        if cmd.all :
            categories  = "."
        else :
            categories  = "[" + "".join (cmd.categories) + "]"
        categories      = Regexp (categories)
        source_currency = cmd.source_currency
        vst_korrektur   = cmd.vst_korrektur
        account         = self._create_account \
            (cmd, categories, source_currency, vst_korrektur)
        self._add_files (cmd, account, categories, source_currency)
        self._output    (cmd, account, categories, source_currency)
    # end def __init__

    @classmethod
    def command_spec (cls, arg_array = None) :
        return Command_Line \
            ( option_spec = cls._opt_spec ()
            , arg_spec    = cls._arg_spec ()
            , description = cls.__doc__ or ""
            , min_args    = cls.min_args
            , max_args    = cls.max_args
            , help_on_err = 1
            , arg_array   = arg_array
            )
    # end def command_spec

    @classmethod
    def load_config (cls, cmd) :
        globs   = globals ()
        cf_dict = dict    (ATAX = ATAX)
        for cf in cmd.Config :
            TGL.load_config_file (cf, globs, cf_dict)
    # end def load_config

    def _add_files (self, cmd, account, categories, source_currency) :
        if cmd.argn > 0 :
            for file_name in cmd.argv.body :
                account.add_file (file_name, categories, source_currency)
        else :
            account.add_lines    (sys.stdin, categories, source_currency)
    # end def _add_files

    @classmethod
    def _arg_spec (cls) :
        return ()
    # end def _arg_spec

    @classmethod
    def _opt_spec (cls) :
        return \
            ( "-all"
            , "-categories:S,=%s" % cls.default_categories
            , "-Config:P,?Config file(s)"
            , "-vst_korrektur:F=1.0"
            , EUC_Opt_SC ()
            , EUC_Opt_TC ()
            )
    # end def _opt_spec

# end class Main

if __name__ != "__main__" :
    ATAX._Export ("*")
### __END__ ATAX.accounting
