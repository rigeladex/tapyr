# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    recode
#
# Purpose
#    Re-encode a file
#
# Revision Dates
#    22-May-2012 (CT) Creation
#    17-Nov-2013 (CT) Simplify, use `file` to determine `input_encoding`
#    18-Nov-2013 (CT) Add `coding_map` and option `-force`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL        import TFL

from   _TFL        import sos
from   _TFL.Regexp import Regexp, re

import _TFL.CAO

from   plumbum     import local as pbl

coding_map = \
    { "binary"       : "iso-8859-15"
    , "iso-8859-1"   : "iso-8859-15"
    , "unknown-8bit" : "iso-8859-15"
    , "us-ascii"     : "iso-8859-15"
    }

coding_pat = Regexp \
    ( r"(?P<head> -\*- \s+ coding: \s+) (?P<encoding> \S+) (?P<tail> \s+ -\*-)"
    , re.VERBOSE
    )

mime_cmd   = pbl ["file"] ["--brief", "--mime"]
mime_pat   = Regexp \
    ( "(?P<type> [^/]+)/(?P<sub_type> [^;]+);"
      "\s+"
      "charset=(?P<encoding> [-a-zA-Z0-9]+)"
    , re.VERBOSE
    )

def file_iter (names, output_encoding, force = False) :
    for name in names :
        t, s, input_encoding = file_mime_type (name)
        if t == "text" or force:
            input_encoding = coding_map.get (input_encoding, input_encoding)
            if input_encoding != output_encoding :
                yield name, input_encoding
# end def file_iter

def file_mime_type (name) :
    result = mime_cmd (name)
    if mime_pat.match (result) :
        return mime_pat.type, mime_pat.sub_type, mime_pat.encoding
    else :
        return None, None, None
# end def file_mime_type

def recode_file \
        (name, input_encoding, output_encoding, backup = None, verbose = False):
    with open (name, "rb") as f :
        source = f.read ()
    coding_rep = r"\g<head>%s\g<tail>" % output_encoding
    if coding_pat.search (source) :
        input_encoding = coding_pat.encoding
    text = source.decode (input_encoding)
    if coding_pat.last_match :
        text = coding_pat.sub (coding_rep, text, 1)
    target = text.encode (output_encoding)
    if backup :
        sos.rename (name, name + backup)
    with open (name, "w+b") as f :
        f.write (target)
    if verbose :
        print \
            ( "Converted %s from %s to %s"
            % (name, input_encoding, output_encoding)
            )
# end def recode_file

def _main (cmd) :
    backup          = cmd.backup
    force           = cmd.force
    output_encoding = cmd.output_encoding
    verbose         = cmd.verbose
    if backup and not backup.startswith (".") :
        backup = "." + backup
    for name, input_encoding in file_iter (cmd.argv, output_encoding, force) :
        recode_file (name, input_encoding, output_encoding, backup, verbose)
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "file:P?File(s) to recode"
        ,
        )
    , opts          =
        ( "-backup:S?Save a backup of `file` with the extension given"
        , "-force:B?"
            "Force conversion even if `file --mime` indicates the file "
            "isn't `text`"
        , TFL.CAO.Opt.Output_Encoding
            ( description   = "Output encoding"
            , default       = "utf-8"
            )
        , "-verbose:B?Print information about files recoded"
        )
    , min_args      = 1
    , description   = "Change file encoding"
    )

if __name__ == "__main__" :
    _Command ()
### __END__ recode
