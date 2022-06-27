# -*- coding: utf-8 -*-
# Copyright (C) 2014 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    rewrite_license_header
#
# Purpose
#    Rewrite the license header to a different license
#
# Revision Dates
#    13-Oct-2014 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _TFL.predicate           import filtered_join
from   _TFL.pyk                 import pyk
from   _TFL.Regexp              import Multi_Regexp, Regexp, re

import _TFL.CAO

licenses           = dict \
    ( bsd3         = "\n".join
        ( ( "This module is licensed under the terms of the "
            "BSD 3-Clause License"
          , "<https://www.gg32.com/license/bsd_3c.html>."
          )
        )
    )

license_header_pat = Regexp \
    ( r"^"
      r"(?P<head>"
          r"(?P<lead> \s* (?: \#+|\*+|//|;+) \s+)?"
          r"\#\*\*\*\s+<License>\s*\**\#$"
      r")"
      r"(?P<body> .+)"
      r"^"
      r"(?P<tail>"
          r"(?P=lead)"
          r"\#\*\*\*\s+</License>\s*\**\#$"
      r")"
    , re.DOTALL | re.MULTILINE | re.VERBOSE
    )

license_preamble_pat = Regexp \
    ( r"This +\w+ +is +part +of +the +\w+ +(?P<pkg>(?:\w+\.)+) *$"
    , re.MULTILINE
    )

module_kind_pat = Regexp \
    ( r"(?P<head>This +)(?P<kind>\w+)(?P<tail> +is +)"
    , re.MULTILINE
    )

old_license_head_pats = \
    ( Regexp
        ( r"^(?P<lead> *(?:\#+|\*+|//|;+) +)"
          r"This \w+ is free software[;:] you can redistribute it and/or"
          r".*"
          r"Foundation, Inc., 675 Mass Ave, Cambridge, MA q?02139, USA."
        , re.DOTALL | re.MULTILINE
        )
    , Regexp
        ( r"^(?P<lead> *(?:\#+|\*+|//|;+) +)"
          r"This \w+ is free software[;:] you can redistribute it and/or"
          r".*"
          r"51 Franklin St, Fifth Floor, Boston, MA +02110-1301 +USA"
        , re.DOTALL | re.MULTILINE
        )
    , Regexp
        ( r"^(?P<lead> *(?:\#+|\*+|//|;+) +)"
          r"This \w+ is free software[;:] you can redistribute it and/or"
          r".*"
          r"along with this \w+[.;] *[Ii]f not, see <http://www.gnu.org/licenses/>."
        , re.DOTALL | re.MULTILINE
        )
    )

def new_license_with_lead (new_license, lead, sep) :
    return lead + sep.join \
        (s.strip () for s in new_license.strip ().split ("\n"))
# end def new_license_with_lead


def replaced_license_header (source, new_license) :
    """Replace license in header of `source` with `new_license`."""
    lh_pat          = license_header_pat
    olh_pats        = old_license_head_pats
    kind            = "module"
    prea            = None
    replacement     = None
    pat             = None
    if lh_pat.search (source) :
        pat         = lh_pat
        body        = lh_pat.body.strip ()
        head        = lh_pat.head.strip ()
        lead        = lh_pat.lead
        sep         = "\n" + lead
        tail        = lh_pat.tail.strip ()
        if license_preamble_pat.search (body) :
            prea    = license_preamble_pat.group (0).strip ()
        if module_kind_pat.match (new_license) :
            kind_head = module_kind_pat.head
            kind_tail = module_kind_pat.tail
            if module_kind_pat.search (body) :
                new_kind = "".join \
                    ((kind_head, module_kind_pat.kind, kind_tail))
                new_license = module_kind_pat.sub (new_kind, new_license, 1)
        replacement = filtered_join \
            ( "\n"
            , [ head
              , (lead + prea + sep) if prea else None
              , new_license_with_lead (new_license, lead, sep)
              , tail
              ]
            )
    else :
        for olh_pat in olh_pats :
            if olh_pat.search (source) :
                pat         = olh_pat
                lead        = olh_pat.lead
                sep         = "\n" + lead
                replacement = new_license_with_lead (new_license, lead, sep)
                break
    if pat is not None and replacement is not None :
        result = pat.sub (replacement, source, 1)
        return result
# end def replaced_license_header

def rewrite_license_header (path, new_license) :
    """Rewrite license header of file at `path` with `new_license`."""
    with open (path, "rb") as f :
        source = f.read ()
    target = replaced_license_header (source, new_license)
    if target is not None :
        with open (path, "wb") as f :
            f.write (target)
    return target
# end def rewrite_license_header

def _main (cmd) :
    new_license = cmd.license
    verbose     = cmd.verbose
    if cmd.argv and verbose :
        print ("Rewrote license of:")
    for p in cmd.argv :
        t = rewrite_license_header (p, new_license)
        if verbose :
            print ("   ", p, "" if t else "*** not rewritten" )
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "file:P?File(s) for which to rewrite license header", )
    , opts          =
        ( TFL.CAO.Key
            ( licenses
            , name        = "license"
            , description = "Name of new license to use"
            , default     = "bsd3"
            )
        , "-verbose:B?Verbose output"
        )
    )

if __name__ == "__main__" :
    _Command ()
### __END__ rewrite_license_header
