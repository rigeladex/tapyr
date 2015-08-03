# -*- coding: utf-8 -*-
# Copyright (C) 2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.Phone
#
# Purpose
#    «text»···
#
# Revision Dates
#     3-Aug-2015 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW.__test__.model      import *

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> at = PAP.Phone ("43", "1", "234567")

    >>> print (at.ui_display)
    +43-1-234567

    >>> print (at.country)
    Country (43) [Austria]

    >>> print (at.ndc_min_length, at.ndc_max_length, at.sn_min_length, at.sn_max_length)
    1 4 3 12

    >>> atp = PAP.Phone ("+43 1 234 56 78")

    >>> print (atp.ui_display)
    +43-1-2345678

    >>> print (atp.country)
    Country (43) [Austria]

    >>> at1 = PAP.Phone ("43", "2287", "1234567890")
    >>> print (at1.ui_display)
    +43-2287-1234567890
    >>> print (at1.ndc_min_length, at1.ndc_max_length, at1.sn_min_length, at1.sn_max_length)
    1 4 3 9

    >>> with expect_except (MOM.Error.Invariants) :
    ...     scope.commit ()
    Invariants: Condition `sn_length_valid` : Value for `sn` must contain at least `sn_min_length`
    digits, must not be longer than `sn_max_length` digits. (sn_min_length <= length <= sn_max_length)
        length = 10 << len (sn)
        sn = '1234567890'
        sn_max_length = 9
        sn_min_length = 3
    >>> scope.rollback ()

    >>> dk = PAP.Phone ("45", "", "12345678")

    >>> print (dk.ui_display)
    +45-12345678

    >>> print (portable_repr ([dk.cc, dk.ndc, dk.sn]))
    ['45', '', '12345678']

    >>> print (dk.country)
    Country (45) [Denmark]

    >>> with expect_except (MOM.Error.Invariants) :
    ...     PAP.Phone ("45", "", "")
    Invariants: Condition `AC_check_sn_length` : Value for sn must contain at least 3 characters; must not be longer than 14 characters (3 <= length <= 14)
        length = 0 << len (sn)
        sn = None
    >>> scope.rollback ()

    >>> dk = PAP.Phone ("45", "12", "345678")
    >>> with expect_except (MOM.Error.Invariants) :
    ...     scope.commit ()
    Invariants: Condition `ndc_length_valid` : Value for `ndc` must contain at least `ndc_min_length`
    digits, must not be longer than `ndc_max_length` digits. (ndc_min_length <= length <= ndc_max_length)
        length = 2 << len (ndc)
        ndc = '12'
        ndc_max_length = 0
        ndc_min_length = 0
    >>> scope.rollback ()

    >>> with expect_except (MOM.Error.Invariants) :
    ...     PAP.Phone ("", "", "123")
    Invariants: Condition `AC_check_cc_length` : Value for cc must contain at least 1 characters; must not be longer than 3 characters (1 <= length <= 3)
        cc = None
        length = 0 << len (cc)

    >>> with expect_except (MOM.Error.Invariants) :
    ...     PAP.Phone ("43", "", "")
    Invariants: Condition `AC_check_sn_length` : Value for sn must contain at least 3 characters; must not be longer than 14 characters (3 <= length <= 14)
        length = 0 << len (sn)
        sn = None

    >>> with expect_except (MOM.Error.Invariants) :
    ...     x = PAP.Phone ("699", "123", "456789")
    Invariants: Can't set primary attribute Phone.cc to '699'.
        Unknown country code 699

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_code           = _test_code
        )
    )

### __END__ GTW.__test__.Phone
