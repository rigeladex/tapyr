# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT._test_HTD
#
# Purpose
#    Tool kit independent doctest for TGL.UI.HTD
#
# Revision Dates
#    31-Mar-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TGL._UI.HTD    import *
from   _TGL._UI.Styled import Styled

HTD_interface_test = """
    >>> from   _TFL._UI.App_Context import App_Context
    >>> def show (t) :
    ...     x = t.get    ()
    ...     y = x.rstrip ()
    ...     for l in y.split (nl) :
    ...         print l.strip ()
    ...     print "%s characters with %s trailing whitespace chars" % (
    ...           len (x), len (x) - len (y))
    ...
    >>> ac  = App_Context (TGL)
    >>> nl  = chr (10)
    >>> r   = Root (ac, nl.join (("R.line 1", "R.line 2")))
    >>> t   = r.tkt_text
    >>> show (t)
    R.line 1
    R.line 2
    18 characters with 1 trailing whitespace chars
    >>> n1 = Node ( r
    ...           , ( r.Style.T ("n1.line 1 ", "yellow")
    ...             , nl, "n1 line 2"
    ...             , Styled ("continued", r.Style.blue)
    ...             ))
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    49 characters with 2 trailing whitespace chars
    >>> n2 = Node_B  (r, nl.join (("n2 line 1", "n2 line 2")))
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    71 characters with 2 trailing whitespace chars
    >>> n3 = Node_B2 ( r
    ...              , ( ["n3 closed line 1"]
    ...                , ["n3 open line 1", nl, "n3 open line 2"])
    ...              , r.Style.light_gray)
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    n3 closed line 1
    90 characters with 2 trailing whitespace chars
    >>> n3.inc_state ()
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    n3 open line 1
    n3 open line 2
    103 characters with 2 trailing whitespace chars
    >>> m1 = Node_B2 ( n3
    ...              , ( ["m1 closed line 1"]
    ...                , ["m1 open line 1", nl, "m1 open line 2"]))
    >>> m2 = Node    ( n3, ("m2 line 1", nl, "m2 line 2"))
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    n3 open line 1
    n3 open line 2
    m1 closed line 1
    m2 line 1
    m2 line 2
    144 characters with 3 trailing whitespace chars
    >>> m1.inc_state ()
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    n3 open line 1
    n3 open line 2
    m1 open line 1
    m1 open line 2
    m2 line 1
    m2 line 2
    157 characters with 3 trailing whitespace chars
    >>> m1.inc_state ()
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    n3 open line 1
    n3 open line 2
    m1 closed line 1
    m2 line 1
    m2 line 2
    144 characters with 3 trailing whitespace chars
    >>> n3.inc_state ()
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    n3 closed line 1
    90 characters with 2 trailing whitespace chars
    >>> n3.inc_state ()
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    n3 open line 1
    n3 open line 2
    m1 closed line 1
    m2 line 1
    m2 line 2
    144 characters with 2 trailing whitespace chars
    >>> n4 = Node_B2 ( r, ( ["n4 closed line 1"]
    ...                   , ["n4 open line 1", nl, "n4 open line 2"])
    ...              , r.Style.light_blue)
    >>> show (t)
    R.line 1
    R.line 2
    n1.line 1
    n1 line 2continued
    n2 line 1
    n2 line 2
    n3 open line 1
    n3 open line 2
    m1 closed line 1
    m2 line 1
    m2 line 2
    n4 closed line 1
    163 characters with 2 trailing whitespace chars
    """

### __END__ TGL.TKT._test_HTD
