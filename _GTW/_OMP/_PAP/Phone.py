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
#    29-Jul-2015 (CT) Change attribute names to `cc`, `ndc`, `sn`
#    29-Jul-2015 (CT) Change `ui_display_sep` from "/" to "-"
#    ««revision-date»»···
#--

from   __future__               import unicode_literals

from   _MOM.import_MOM          import *
from   _GTW                     import GTW
from   _GTW._OMP._PAP           import PAP

import _GTW._OMP._PAP.Property

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T

class _NDC_Polisher_ (MOM.Attr.Polisher._Polisher_) :
    """Polisher for `ndc`, `cc` attributes."""

    @Once_Property
    def splitter (self) :
        return Attr.Polisher.phone_ndc_split
    # end def splitter

    def _polished (self, attr, name, value, value_dict) :
        result  = self.splitter._polished (attr, name, value, value_dict)
        if result and (name not in result or value == "0") :
            ### user entered a `cc` or just `0` into the
            ### input-field for `ndc` --> remove that value
            result [name] = ""
        return result
    # end def _polished

# end class _NDC_Polisher_

class _SN_Polisher_ (MOM.Attr.Polisher._Polisher_) :
    """Polisher for `cc`, `ndc`, `sn` attributes."""

    @Once_Property
    def splitter (self) :
        return Attr.Polisher.phone_sn_split
    # end def splitter

    def _polished (self, attr, name, value, value_dict) :
        value  = Attr.Polisher.compress_spaces.replacer (value)
        result = self.splitter (attr, value_dict, value)
        cc     = result.get ("cc",  "")
        ndc    = result.get ("ndc", "")
        if ndc and ndc == cc :
            ### user entered something like `43 123456789` into the
            ### input-field for `sn` while there was a value of `43` in
            ### the input-field for `cc`
            ### --> remove that value unless the user explicitly entered
            ###     `43 43 123456789`
            match = self.splitter.matcher.search (value)
            if match :
                dct   = match.groupdict ()
                ndc_m = dct.get ("ndc")
                cc_m  = dct.get ("cc")
                if ndc_m and cc_m :
                    ndc = ""
            if ndc :
                result.pop ("ndc")
        return result
    # end def _polished

# end class _SN_Polisher_

_test_polisher = """

    >>> from _TFL.Record import Record

    >>> attr     = Record (name = "sn")
    >>> polisher = _SN_Polisher_ ()
    >>> def show_c_a_n (sn, ** kw) :
    ...     r  = polisher (attr, dict (sn = sn, ** kw))
    ...     vs = ("%s = %s" % (k, v) for k, v in sorted (r.items ()) if v)
    ...     print (", ".join (vs))

    >>> show_c_a_n ("43 66412345678", cc = "43")
    cc = 43, sn = 66412345678

    >>> show_c_a_n ("43 43 66412345678", cc = "43")
    cc = 43, sn = 43 43 66412345678

    >>> show_c_a_n ("+43 43 66412345678", cc = "43")
    cc = 43, ndc = 43, sn = 66412345678

    >>> show_c_a_n ("12345678")
    sn = 12345678

    >>> show_c_a_n ("0043 664 12345678")
    cc = 43, ndc = 664, sn = 12345678

    >>> show_c_a_n ("+43 664 12345678")
    cc = 43, ndc = 664, sn = 12345678

    >>> show_c_a_n ("0043 664 12345678")
    cc = 43, ndc = 664, sn = 12345678

    >>> show_c_a_n ("664 12345678")
    ndc = 664, sn = 12345678

    >>> show_c_a_n ("0664 12345678")
    ndc = 664, sn = 12345678

    >>> show_c_a_n ("+43(664)12345678")
    cc = 43, ndc = 664, sn = 12345678

    >>> show_c_a_n ("+43 (664) 12345678")
    cc = 43, ndc = 664, sn = 12345678

    >>> show_c_a_n ("0(664)12345678")
    ndc = 664, sn = 12345678

    >>> show_c_a_n ("0 (664) 12345678")
    ndc = 664, sn = 12345678

    >>> show_c_a_n ("43 66412345678", cc = "43")
    cc = 43, sn = 66412345678

    >>> show_c_a_n ("+43 66412345678", cc = "43")
    cc = 43, sn = 66412345678

    >>> attr     = Record (name = "ndc")
    >>> polisher = _NDC_Polisher_ ()
    >>> def show_c_a (value, ** kw) :
    ...     r  = polisher (attr, dict (ndc = value, ** kw))
    ...     vs = ("%s = %s" % (k, v) for k, v in sorted (r.items ()) if v)
    ...     print (", ".join (vs))

    >>> show_c_a ("664")
    ndc = 664

    >>> show_c_a ("0664")
    ndc = 664

    >>> show_c_a ("0 664")
    ndc = 664

    >>> show_c_a ("664", cc = "43")
    cc = 43, ndc = 664

    >>> show_c_a ("(664)", cc = "43")
    cc = 43, ndc = 664

    >>> show_c_a ("+44 664", cc = "43")
    cc = 44, ndc = 664

    >>> show_c_a ("+44 664 ", cc = "43")
    cc = 44, ndc = 664

    >>> show_c_a ("+44/664", cc = "43")
    cc = 44, ndc = 664

    >>> show_c_a ("+44/664/", cc = "43")
    cc = 44, ndc = 664

    >>> show_c_a ("+44 (664)", cc = "43")
    cc = 44, ndc = 664

    >>> show_c_a ("+44", cc = "43")
    cc = 44

    >>> show_c_a ("0", cc = "43")
    cc = 43

"""

__test__ = dict \
    ( test_polisher = _test_polisher
    )

_Ancestor_Essence = PAP.Property

class _PAP_Phone_ (_Ancestor_Essence) :
    """Model a phone number"""

    _real_name     = "Phone"

    ui_display_sep = "-"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class cc (A_Numeric_String) :
            """International country code of phone number (without prefix)"""

            kind           = Attr.Primary
            max_length     = 3
            check          = ("value != '0'", )
            example        = "43"
            rank           = 1
            format         = "+%s"
            ui_name        = _ ("Country code")
            ui_rank        = -1

            completer      = Attr.Completer_Spec  (1)
            polisher       = Attr.Polisher.phone_cc_clean

        # end class cc

        class ndc (A_Numeric_String) :
            """National destination code of phone number (without prefix).

               The national destination code selects a geographic area, e.g.,
               a city or district, a mobile provider, or a specific service.
            """

            kind           = Attr.Primary
            max_length     = 5
            check          = ("value != '0'", )
            example        = "1"
            rank           = 2
            ui_name        = _ ("Network destination code")
            ui_rank        = -2

            completer      = Attr.Completer_Spec  \
                (1, Attr.Selector.Name ("cc"))
            polisher       = _NDC_Polisher_ ()

        # end class ndc

        class sn (A_Numeric_String) :
            """Subscriber number (without country code, network destination code, extension)"""

            kind           = Attr.Primary
            max_length     = 14
            check          = ("value != '0'", )
            example        = "234567"
            rank           = 3
            ui_name        = _ ("Subscriber number")
            ui_rank        = -3

            completer      = Attr.Completer_Spec  (1, Attr.Selector.primary)
            polisher       = _SN_Polisher_ ()

        # end class sn

    # end class _Attributes

Phone = _PAP_Phone_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Phone
