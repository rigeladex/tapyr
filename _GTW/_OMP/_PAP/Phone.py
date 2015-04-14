# -*- coding: utf-8 -*-
# Copyright (C) 2009-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.PAP.Phone
#
# Purpose
#    Model a phone number
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#     3-Feb-2010 (MG) `extension`  removed
#    28-Feb-2010 (CT) Use `A_Numeric_String` instead of `A_Int` and
#                     `A_Decimal` for `country_code`, `area_code`, and `number`
#     7-Sep-2011 (CT) `completer` specifications for `country_code`,
#                     `area_code`, and `number` added
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#     7-Aug-2012 (CT) Add `example`
#    12-Sep-2012 (CT) Derive from `Property`
#     7-Mar-2014 (CT) Add `ui_rank` in reverse order of `rank`
#                     (to improve completion)
#    24-Sep-2014 (CT) Add `polisher` to `country_code`, `area_code`, `number`
#    26-Feb-2015 (CT) Add `_Area_Code_Polisher_`, `_Number_Polisher_` to fix
#                     erroneous input values
#    14-Apr-2015 (CT) Lower completer treshold for `number`
#    ««revision-date»»···
#--

from   __future__               import unicode_literals

from   _MOM.import_MOM          import *
from   _GTW                     import GTW
from   _GTW._OMP._PAP           import PAP

import _GTW._OMP._PAP.Property

from   _TFL._Meta.Once_Property import Once_Property

class _Area_Code_Polisher_ (MOM.Attr.Polisher._Polisher_) :
    """Polisher for `area_code`, `country_code` attributes."""

    @Once_Property
    def splitter (self) :
        return Attr.Polisher.area_code_split
    # end def splitter

    def _polished (self, attr, name, value, value_dict) :
        result  = self.splitter._polished (attr, name, value, value_dict)
        if result and (name not in result or value == "0") :
            ### user entered a `country_code` or just `0` into the
            ### input-field for `area_code` --> remove that value
            result [name] = ""
        return result
    # end def _polished

# end class _Area_Code_Polisher_

class _Number_Polisher_ (MOM.Attr.Polisher._Polisher_) :
    """Polisher for `country_code`, `area_code`, `number` attributes."""

    @Once_Property
    def splitter (self) :
        return Attr.Polisher.phone_number_split
    # end def splitter

    def _polished (self, attr, name, value, value_dict) :
        result = self.splitter (attr, value_dict, value)
        cc     = result.get ("country_code", "")
        ac     = result.get ("area_code",    "")
        if ac and ac == cc :
            ### user entered something like `43 123456789` into the
            ### input-field for `number` while there was a value of `43` in
            ### the input-field for `country_code`
            ### --> remove that value unless the user explicitly entered
            ###     `43 43 123456789`
            match = self.splitter.matcher.search (value)
            if match :
                dct = match.groupdict ()
                acm = dct.get ("area_code")
                ccm = dct.get ("country_code")
                if acm and ccm :
                    ac = ""
            if ac :
                result.pop ("area_code")
        return result
    # end def _polished

# end class _Number_Polisher_

_test_polisher = """

    >>> from _TFL.Record import Record

    >>> attr     = Record (name = "number")
    >>> polisher = _Number_Polisher_ ()
    >>> def show_c_a_n (number, ** kw) :
    ...     r  = polisher (attr, dict (number = number, ** kw))
    ...     vs = ("%s = %s" % (k, v) for k, v in sorted (r.items ()) if v)
    ...     print (", ".join (vs))

    >>> show_c_a_n ("43 66412345678", country_code = "43")
    country_code = 43, number = 66412345678

    >>> show_c_a_n ("43 43 66412345678", country_code = "43")
    country_code = 43, number = 43 43 66412345678

    >>> show_c_a_n ("+43 43 66412345678", country_code = "43")
    area_code = 43, country_code = 43, number = 66412345678

    >>> show_c_a_n ("12345678")
    number = 12345678

    >>> show_c_a_n ("0043 664 12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_c_a_n ("+43 664 12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_c_a_n ("0043 664 12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_c_a_n ("664 12345678")
    area_code = 664, number = 12345678

    >>> show_c_a_n ("0664 12345678")
    area_code = 664, number = 12345678

    >>> show_c_a_n ("+43(664)12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_c_a_n ("+43 (664) 12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_c_a_n ("0(664)12345678")
    area_code = 664, number = 12345678

    >>> show_c_a_n ("0 (664) 12345678")
    area_code = 664, number = 12345678

    >>> show_c_a_n ("43 66412345678", country_code = "43")
    country_code = 43, number = 66412345678

    >>> show_c_a_n ("+43 66412345678", country_code = "43")
    country_code = 43, number = 66412345678

    >>> attr     = Record (name = "area_code")
    >>> polisher = _Area_Code_Polisher_ ()
    >>> def show_c_a (value, ** kw) :
    ...     r  = polisher (attr, dict (area_code = value, ** kw))
    ...     vs = ("%s = %s" % (k, v) for k, v in sorted (r.items ()) if v)
    ...     print (", ".join (vs))

    >>> show_c_a ("664")
    area_code = 664

    >>> show_c_a ("0664")
    area_code = 664

    >>> show_c_a ("0 664")
    area_code = 664

    >>> show_c_a ("664", country_code = "43")
    area_code = 664, country_code = 43

    >>> show_c_a ("(664)", country_code = "43")
    area_code = 664, country_code = 43

    >>> show_c_a ("+44 664", country_code = "43")
    area_code = 664, country_code = 44

    >>> show_c_a ("+44 664 ", country_code = "43")
    area_code = 664, country_code = 44

    >>> show_c_a ("+44/664", country_code = "43")
    area_code = 664, country_code = 44

    >>> show_c_a ("+44/664/", country_code = "43")
    area_code = 664, country_code = 44

    >>> show_c_a ("+44 (664)", country_code = "43")
    area_code = 664, country_code = 44

    >>> show_c_a ("+44", country_code = "43")
    country_code = 44

    >>> show_c_a ("0", country_code = "43")
    country_code = 43

"""

__test__ = dict \
    ( test_polisher = _test_polisher
    )

_Ancestor_Essence = PAP.Property

class _PAP_Phone_ (_Ancestor_Essence) :
    """Model a phone number"""

    _real_name     = "Phone"

    ui_display_sep = "/"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class country_code (A_Numeric_String) :
            """International country code of phone number (without prefix)"""

            kind           = Attr.Primary
            max_length     = 3
            check          = ("value != '0'", )
            example        = "43"
            rank           = 1
            ui_rank        = -1

            completer      = Attr.Completer_Spec  (1)
            polisher       = Attr.Polisher.country_code_clean

        # end class country_code

        class area_code (A_Numeric_String) :
            """National area code of phone number (without prefix)"""

            kind           = Attr.Primary
            max_length     = 5
            check          = ("value != '0'", )
            example        = "1"
            rank           = 2
            ui_rank        = -2

            completer      = Attr.Completer_Spec  \
                (1, Attr.Selector.Name ("country_code"))
            polisher       = _Area_Code_Polisher_ ()

        # end class area_code

        class number (A_Numeric_String) :
            """Phone number proper (without country code, area code, extension)"""

            kind           = Attr.Primary
            max_length     = 14
            check          = ("value != '0'", )
            example        = "234567"
            rank           = 3
            ui_rank        = -3

            completer      = Attr.Completer_Spec  (1, Attr.Selector.primary)
            polisher       = _Number_Polisher_ ()

        # end class number

    # end class _Attributes

Phone = _PAP_Phone_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Phone
