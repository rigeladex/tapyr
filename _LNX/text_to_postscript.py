# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    text_to_postscript
#
# Purpose
#    Wrapper around `a2ps` and `enscript`
#
# Revision Dates
#    19-Dec-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _LNX                    import LNX
from   _TFL                    import TFL

from   _TFL                    import sos
from   _TFL.FCM                import open_tempfile
from   _TFL.Filename           import Filename
from   _TFL.predicate          import split_hst
from   _TFL.pyk                import pyk

import _TFL.Accessor
import _TFL.Ascii
import _TFL.Command
import _TFL.FCM

from   plumbum                 import local as pbl

import time

class _TTP_Sub_Command_ (TFL.Command.Sub_Command) :

    _rn_prefix              = "_TTP"

    time_fmt                = "%Y/%m/%d %H:%M"

    def handler (self, cmd) :
        return self._root._handler (self, cmd)
    # end def handler

    def _header_fields (self, header, file_name, file_time) :
        l, m, r  = ":", ":", ":"
        if header :
            l, _, x = split_hst (header, "|")
            if _ :
                m, _, r = split_hst (x,  "|")
                if m == ":" and not _ :
                    m, r = "", ":"
            else :
                l, m, r = "", l, ""
        def _gen (l, m, r, file_name, file_time) :
            now = time.strftime (self.time_fmt, time.localtime ())
            for x in (l, m, r) :
                if x == "$n" :
                    x = file_name
                elif x == "$t" :
                    x = now
                yield x
        l, m, r = tuple (_gen (l, m, r, file_name, file_time))
        return \
            ( l if l != ":" else file_time
            , m if m != ":" else file_name
            , r if r != ":" else self._page_number_header ()
            )
    # end def _header_fields

    def _time_header (self) :
        return "%D{%Y/%m/%d %H:%M}"
    # end def _time_header

_Sub_Command_ = _TTP_Sub_Command_ # end class

class TTP_Command (TFL.Command.Root_Command) :
    """Command wrapper around `a2ps` and `enscript`"""

    _rn_prefix              = "TTP_"

    min_args                = 1

    _opts                   = \
        ( "-borders:B?Print borders around virtual pages"
        , "-Copies:I=1?Number of copies to print"
        , "-Display:B"
              "?Display postscript output with program by -display_program"
        , "-display_program:S=gv"
        , "-dry_run:B?Don't actually run the command"
        , "-header:S?Header to use for each page"
        , "-medium:S=A4?Medium used for output"
        , "-Print:B?Print the file(s)"
        , "-printer_name:S=%s?Name of printer to print to"
            % pbl.env.get ("PRINTER", "lp")
        , "-Output:Q?Write output to specified file"
        , "-time_format:S=%Y/%m/%d %H:%M?Format used for time header"
        , "-verbose:B"
        , TFL.CAO.Opt.Int
            ( name          = "Line_numbers"
            , description   = "Add line number to every line"
            , implied_value = 1
            , needs_value   = False
            )
        , TFL.CAO.Opt.Input_Encoding ()
        , TFL.CAO.Opt.Output_Encoding
            ( default       = "iso8859-1"
            , description   = "Default encoding passed to `a2ps` and `enscript`"
            )
        )

    class _TTP_A2PS_ (_Sub_Command_) :
        """Use `a2ps` to convert text to postscript"""

        _opts               = \
            ( "-columns:I=2"
            , "-font_scale:F=1.0?Scale font up or down by specified factor"
            , "-margin:I?Define an interior margin"
            , "-portrait:B?Use portrait instead of landscape orientation"
            ,
            )

        @TFL.Meta.Once_Property
        def pbl_cmd (self) :
            return pbl ["/usr/bin/a2ps"]
        # end def pbl_cmd

        def options (self, cmd, file_name, file_time) :
            """Options for `a2ps` reflecting `cmd`"""
            portrait = cmd.portrait
            cols     = cmd.columns
            cpl      = (80 if portrait else 160) / cols
            result   = \
                [ "--borders=%d"        % cmd.borders
                , "--columns=%d"        % cols
                , "--copies=%d"         % cmd.Copies
                , "--no-header"
                , "--medium=%s"         % cmd.medium
                ]
            l, m, r  = self._header_fields (cmd.header, file_name, file_time)
            result.extend \
                ( [ "--left-title=%s"   % l
                  , "--center-title=%s" % m
                  , "--right-title=%s"  % r
                  ]
                )
            lnums    = cmd.Line_numbers
            if lnums :
                right.append ("--line-numbers=%d" % lnums)
            margin   = cmd.margin
            if margin :
                result.append ("--margin=%d" % margin)
            if portrait :
                result.append ("--portrait")
            Print    = cmd.Print
            if Print :
                result.append ("--printer=%s" % cmd.printer_name)
            else :
                result.append ("--output=%s" % (cmd.Output or "-"))
            ### last option influencing font size wins
            result.append ("--chars-per-line=%d" % (cpl / cmd.font_scale))
            return result
        # end def options

        def _page_number_header (self) :
            return "$p./$p#"
        # end def _page_number_header

    _A2PS_ = _TTP_A2PS_ # end class

    class _TTP_Enscript_ (_Sub_Command_) :
        """Use `enscript` to convert text to postscript"""

        _opts               = \
            ( "-Baselineskip:F?Baselineskip in PostScript points (default = 1)"
            , "-columns:I=1"
            , "-Font:S=Courier"
            , "-font_size:F=8.0?Font size in points"
            , "-Header_Font:S=Courier"
            , "-Header_Font_Size:F=14.0?Header font size in points"
            , "-landscape:B?Use landscape instead of portrait orientation"
            , "-margins:I:#4?Define margins for LEFT:RIGHT:TOP:BOTTOM"
            ,
            )

        @TFL.Meta.Once_Property
        def pbl_cmd (self) :
            return pbl ["enscript"]
        # end def pbl_cmd

        def options (self, cmd, file_name, file_time) :
            """Options for `a2ps` reflecting `cmd`"""
            cols   = cmd.columns
            result = \
                [ "--columns=%d"        % cols
                , "--copies=%d"         % cmd.Copies
                , "--font=%s@%g"        % (cmd.Font, cmd.font_size)
                , "--media=%s"          % cmd.medium
                ]
            bls = cmd.Baselineskip
            if bls :
                result.append ("--baselineskip=%g" % bls)
            if cmd.borders :
                result.append ("--borders")
            header  = cmd.header
            if header :
                header = "|".join \
                    (self._header_fields (header, file_name, file_time))
                result.append ("--header=%s" % header)
            lands  = cmd.landscape
            if lands :
                result.append ("--landscape")
            lnums  = cmd.Line_numbers
            if lnums :
                right.append ("--line-numbers=%d" % lnums)
            margins = cmd.margins
            if margins :
                l = len (margins)
                if l == 1 :
                    margins = margins * 4
                elif l == 2 :
                    margins = margins [:1] * 2 + margins [1:] * 2
                elif l == 3 :
                    margins.append (margins [-1])
                elif l > 4 :
                    raise ValueError \
                        ( "--margins needs between 1 and 4 values, got %d: %s"
                        % (l, margins)
                        )
                result.append \
                    ("--margins=%s" % ":".join (str (m) for m in margins))
            Print  = cmd.Print
            if Print :
                result.append ("--printer=%s" % cmd.printer_name)
            else :
                result.append ("--output=%s" % (cmd.Output or "-"))
            return result
        # end def options

        def _page_number_header (self) :
            return "$%/$="
        # end def _page_number_header

    _Enscript_ = _TTP_Enscript_ # end class

    def _handler (self, sub, cmd) :
        time_format        = _Sub_Command_.time_fmt = cmd.time_format
        i_enc              = cmd.input_encoding
        o_enc              = cmd.output_encoding
        pbl.env ["LC_ALL"] = "en_US.%s" % o_enc.replace ("-", "")
        for arg in cmd.argv :
            ft = time.strftime \
                (time_format, time.localtime (sos.path.getmtime (arg)))
            fn = Filename (arg).relative_to ("~/")
            with open (arg, "rb") as fi :
                txt = fi.read ().decode (i_enc)
            txt_out = txt.encode (o_enc, "replace")
            options = tuple (sub.options (cmd, fn, ft))
            pbl_cmd = sub.pbl_cmd.__getitem__ (options)
            with open_tempfile () as (fo, no) :
                fo.write (txt_out)
                fo.close ()
                cx  = pbl_cmd [no]
                if cmd.verbose or cmd.dry_run :
                    print (pbl_cmd, arg, "[%s]" % no)
                if not cmd.dry_run :
                    if cmd.Display :
                        if cmd.Print :
                            print \
                                ( "Specify either -Display or -Print, "
                                  "but not both"
                                )
                            raise SystemExit (10)
                        with open_tempfile () as (fd, nd) :
                            fd.write (cx ())
                            fd.close ()
                            pbl [cmd.display_program] [nd] ()
                    else :
                        cx ()
    # end def _handler

Command = TTP_Command # end class

if __name__ != "__main__" :
    GTW._Export_Module ()
if __name__ == "__main__" :
    Command () ()
### __END__ text_to_postscript
