# -*- coding: utf-8 -*-
# Copyright (C) 2013-2019 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#     3-Jan-2014 (CT) Change `-header` to `U`, use `pyk.encoded` for `options`
#    11-Feb-2014 (CT) Add support for STDIN
#     3-Oct-2014 (CT) Add `$b` for header (to select basename of file)
#    27-Aug-2017 (CT) Lstrip newlines, rstrip whitespace to avoid empty pages
#    22-Sep-2017 (CT) Replace some unicode chars with latin-1 approximations
#     5-Nov-2018 (CT) Add option `-PDF`
#                     + Factor `_check_print`, `_output_option`
#                     + Improve Python-3 compatibility
#    24-Nov-2019 (CT) Add `_header_encode_map` with german Umlaute
#                     + Apply `_header_encode_rep` to `header`
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
from   _TFL.Regexp             import Regexp, Re_Replacer, Dict_Replacer, re
from   _TFL.User_Config        import user_config

import _TFL.Accessor
import _TFL.Ascii
import _TFL.Command
import _TFL.FCM

from   plumbum                 import local as pbl

import sys
import time

_encode_map        = \
    { "€"   : "EUR"
    , "­"   : "-"
    , "–"   : "--"
    , "—"   : "---"
    , "×"   : "*"
    , "÷"   : "/"
    , "±"   :"+/-"
    , "Ä"   : "Ae"
    , "Ö"   : "Oe"
    , "Ü"   : "Ue"
    , "ä"   : "ae"
    , "ö"   : "oe"
    , "ü"   : "ue"
    , "ß"   : "ss"
    }
_header_encode_map = dict \
    ( _encode_map
    , ** { "Ä"   : "Ae"
         , "Ö"   : "Oe"
         , "Ü"   : "Ue"
         , "ä"   : "ae"
         , "ö"   : "oe"
         , "ü"   : "ue"
         , "ß"   : "ss"
         }
    )
_encode_rep        = Dict_Replacer (_encode_map)
_header_encode_rep = Dict_Replacer (_header_encode_map)

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
                if x == "$b" :
                    x = Filename (file_name).base
                elif x == "$n" :
                    x = file_name
                elif x == "$t" :
                    x = now
                elif x != ":" :
                    x = _header_encode_rep (x)
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
        , "-header:U?Header to use for each page"
        , "-medium:S=A4?Medium used for output"
        , "-PDF:B?Create a pdf file"
        , "-pdf_program:S=ps2pdf"
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
            )

        @TFL.Meta.Once_Property
        def pbl_cmd (self) :
            return pbl ["/usr/bin/a2ps"]
        # end def pbl_cmd

        def options (self, cmd, file_name, file_time, * xtra_opts) :
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
            result.extend (xtra_opts)
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
            , "-Header_Font:S=Courier-Bold@14"
            , "-landscape:B?Use landscape instead of portrait orientation"
            , "-margins:I:#4?Define margins for LEFT:RIGHT:TOP:BOTTOM"
            )

        @TFL.Meta.Once_Property
        def pbl_cmd (self) :
            return pbl ["enscript"]
        # end def pbl_cmd

        def options (self, cmd, file_name, file_time, * xtra_opts) :
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
            result.extend (xtra_opts)
            return result
        # end def options

        def _page_number_header (self) :
            return "$%/$="
        # end def _page_number_header

    _Enscript_ = _TTP_Enscript_ # end class

    def _check_print (self, cmd, other_opt) :
        if cmd.Print :
            print ("Specify either -%s or -Print, but not both" % other_opt)
            raise SystemExit (10)
    # end def _check_print

    def _encoded (self, txt, enc) :
        result = _encode_rep (txt)
        return result.encode (enc, "replace")
    # end def _encoded

    def _handler (self, sub, cmd) :
        time_format        = _Sub_Command_.time_fmt = cmd.time_format
        i_enc              = cmd.input_encoding
        o_enc              = cmd.output_encoding
        pbl.env ["LC_ALL"] = "en_US.%s" % o_enc.replace ("-", "")
        for arg in cmd.argv :
            if arg in ("-", "STDIN") :
                file_time = time.localtime ()
                fn        = "STDIN"
                txt_in    = sys.stdin.read ()
            else :
                file_time = time.localtime (sos.path.getmtime (arg))
                fn        = Filename (arg).relative_to ("~/")
                with open (arg, "rb") as fi :
                    txt_in = fi.read ()
            txt     = txt_in.decode       (i_enc).lstrip ("\n").rstrip ()
            ft      = time.strftime       (time_format, file_time)
            txt_out = self._encoded       (txt, o_enc)
            out_opt = self._output_option (cmd)
            options = self._pbl_options   (* sub.options (cmd, fn, ft, out_opt))
            pbl_cmd = sub.pbl_cmd.__getitem__ (options)
            with open_tempfile ("wb") as (fo, no) :
                fo.write (txt_out)
                fo.close ()
                cx  = pbl_cmd [no]
                if cmd.verbose or cmd.dry_run :
                    print (pbl_cmd, arg, "[%s]" % no)
                if not cmd.dry_run :
                    if cmd.Display :
                        self._check_print (cmd, "Display")
                        with open_tempfile () as (fd, nd) :
                            fd.write (cx ())
                            fd.close ()
                            pbl [cmd.display_program] [nd] ()
                    elif cmd.PDF :
                        self._check_print (cmd, "PDF")
                        if fn == "-" :
                            target = "-"
                        else :
                            target = cmd.Output or \
                                (arg.replace (".", "__") + ".pdf")
                        pdf_opts   = self._pbl_options ("-", target)
                        px  = cx \
                            | (pbl [cmd.pdf_program].__getitem__ (pdf_opts))
                        px ()
                    else :
                        cx ()
    # end def _handler

    def _pbl_options (self, * opts) :
        return tuple (pyk.text_type (o) for o in opts)
    # end def _pbl_options

    def _output_option (self, cmd) :
        if cmd.Print :
            result = "--printer=%s" % cmd.printer_name
        else :
            fn     = ("" if cmd.PDF else cmd.Output) or "-"
            result = "--output=%s"  % fn
        return result
    # end def _output_option

Command = TTP_Command # end class

if __name__ != "__main__" :
    GTW._Export_Module ()
if __name__ == "__main__" :
    Command () ()
### __END__ text_to_postscript
