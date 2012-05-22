# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL        import TFL

from   _TFL        import sos
from   _TFL.Regexp import Regexp, re

import _TFL.CAO

_cc_pat = Regexp \
    ( r"(?P<head> -\*- \s+ coding: \s+) (?P<encoding> \S+) (?P<tail> \s+ -\*-)"
    , re.VERBOSE
    )

def recode (source, input_encoding, output_encoding) :
    """Change encoding of `source` from `input_encoding` to `output_encoding`"""
    cc_pat = _cc_pat
    cc_rep = r"\g<head>%s\g<tail>" % output_encoding
    if cc_pat.search (source) :
        input_encoding = cc_pat.encoding
    text = source.decode (input_encoding)
    if cc_pat.last_match :
        text = cc_pat.sub (cc_rep, text, 1)
    return text.encode (output_encoding)
# end def recode

def _main (cmd) :
    backup          = cmd.backup
    input_encoding  = cmd.input_encoding
    output_encoding = cmd.output_encoding
    if backup and not backup.startswith (".") :
        backup = "." + backup
    for name in cmd.argv :
        with open (name, "rb") as f :
            source = f.read ()
        target = recode (source, input_encoding, output_encoding)
        if cmd.inplace :
            if backup :
                sos.rename (name, name + backup)
            with open (name, "w+b") as f :
                f.write (target)
        elif cmd.target_dir :
            if sos.path.isabs (name) :
                _, name   = sos.path.split (name)
            target_name   = sos.path.join  (cmd.target_dir, name)
            target_dir, _ = sos.path.split (target_name)
            if not sos.path.isdir (target_dir) :
                sos.makedirs (target_dir)
            with open (target_name, "wb") as f :
                f.write (target)
        else :
            print (target)
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "file:P?File(s) to recode"
        ,
        )
    , opts          =
        ( "-backup:S=.bak?Save a backup of `file` with the extension given"
        , "-inplace:B?Change `file` in place"
        , TFL.CAO.Opt.Input_Encoding
            ( description   = "Default encoding for source files"
            , default       = "iso-8859-1"
            )
        , TFL.CAO.Opt.Output_Encoding
            ( description   = "Output encoding"
            , default       = "utf-8"
            )
        , "-target_dir:P?Target directory to write re-encoded files into"
        )
    , min_args      = 1
    , description   = "Change file encoding"
    )

if __name__ == "__main__" :
    _Command ()
### __END__ recode
