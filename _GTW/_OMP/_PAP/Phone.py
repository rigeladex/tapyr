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
#    30-Jul-2015 (CT) Add arguments `essence`, `picky` to `_polished`
#    30-Jul-2015 (CT) Add `_CC_Polisher_`
#    30-Jul-2015 (CT) Change `_NDC_Polisher_` to use `E164.Country`
#    31-Jul-2015 (CT) Factor polishers to `E164.Polisher`
#     3-Aug-2015 (CT) Change attributes `cc`, `ndc`, `sn` to `Primary_Optional`
#                     + Add `min_length` to `cc`, `sn`
#     3-Aug-2015 (CT) Add predicates `ndc_length_valid`, `sn_length_valid`
#                     + Add computed attributes `country`, `ndc_max_length`,
#                       `ndc_min_length`, `sn_max_length`, `sn_min_length`
#     3-Aug-2015 (CT) Set `_init_raw_default` to `True`
#     3-Aug-2015 (CT) Redefine `ui_display.computed` to use `formatted_sn`
#    ««revision-date»»···
#--

from   __future__               import unicode_literals

from   _MOM.import_MOM          import *
from   _GTW                     import GTW
from   _GTW._OMP._PAP           import PAP

import _GTW._OMP._PAP.Property
import _GTW._OMP._PAP._E164.Polisher

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = PAP.Property

class _PAP_Phone_ (_Ancestor_Essence) :
    """Model a phone number"""

    _real_name                 = "Phone"

    ui_display_sep             = "-"
    _init_raw_default          = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class cc (A_Numeric_String) :
            """International country code of phone number (without prefix)"""

            kind               = Attr.Primary_Optional
            max_length         = 3
            min_length         = 1
            check              = ("value != '0'", )
            example            = "43"
            rank               = 1
            format             = "+%s"
            ui_name            = _ ("Country code")
            ui_rank            = -1

            completer          = Attr.Completer_Spec  (1)
            polisher           = PAP.E164.Polisher.CC ()

        # end class cc

        class ndc (A_Numeric_String) :
            """National destination code of phone number (without prefix).

               The national destination code selects a geographic area, e.g.,
               a city or district, a mobile provider, or a specific service.
            """

            kind               = Attr.Primary_Optional
            max_length         = 5
            check              = ("value != '0'", )
            example            = "1"
            rank               = 2
            ui_name            = _ ("Network destination code")
            ui_rank            = -2

            completer          = Attr.Completer_Spec \
                (1, Attr.Selector.Name ("cc"))
            polisher           = PAP.E164.Polisher.NDC ()

        # end class ndc

        class sn (A_Numeric_String) :
            """Subscriber number (without country code, network destination code, extension)"""

            kind               = Attr.Primary_Optional
            max_length         = 14
            min_length         = 3
            check              = ("value != '0'", )
            example            = "234567"
            rank               = 3
            ui_name            = _ ("Subscriber number")
            ui_rank            = -3

            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)
            polisher           = PAP.E164.Polisher.SN ()

        # end class sn

        ### Non-primary attributes

        class country (A_Blob) :

            kind               = Attr.Computed
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                cc = obj.cc
                if cc :
                    try :
                        return PAP.E164.Country (cc)
                    except Exception :
                        pass
            # end def computed

        # end class country

        class ndc_max_length (A_Int) :
            """Maximum permissible length of value for `ndc`."""

            kind               = Attr.Computed
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                country = obj.country
                if country :
                    return country.ndc_max_length
                return 4
            # end def computed

        # end class ndc_max_length

        class ndc_min_length (A_Int) :
            """Minimum permissible length of value for `ndc`."""

            kind               = Attr.Computed
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                country = obj.country
                if country :
                    return country.ndc_min_length
                return 1
            # end def computed

        # end class ndc_min_length

        class sn_max_length (A_Int) :
            """Maximum permissible length of value for `sn`."""

            kind               = Attr.Computed
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                country = obj.country
                if country :
                    return country.sn_max_length (obj.ndc)
                return 15
            # end def computed

        # end class sn_max_length

        class sn_min_length (A_Int) :
            """Minimum permissible length of value for `sn`."""

            kind               = Attr.Computed
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                country = obj.country
                if country :
                    return country.sn_min_length (obj.ndc)
                return 3
            # end def computed

        # end class sn_min_length

        class ui_display (_Ancestor.ui_display) :

            def computed (self, obj) :
                country = obj.country
                FO      = obj.FO
                cc      = FO.cc
                ndc     = FO.ndc
                sn      = FO.sn
                if country is not None :
                    sn  = country.formatted_sn (sn)
                return obj.ui_display_sep.join (x for x in (cc, ndc, sn) if x)
            # end def computed

        # end class ui_display

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class ndc_length_valid (Pred.Condition) :
            """Value for `ndc` must contain at least `ndc_min_length`
               digits, must not be longer than `ndc_max_length` digits.
            """

            kind               = Pred.Region
            assertion          = "ndc_min_length <= length <= ndc_max_length"
            attributes         = ("ndc", "ndc_max_length", "ndc_min_length")
            bindings           = dict \
                ( length       = "len (ndc)"
                )

        # end class ndc_length_valid

        class sn_length_valid (Pred.Condition) :
            """Value for `sn` must contain at least `sn_min_length`
               digits, must not be longer than `sn_max_length` digits.
            """

            kind               = Pred.Region
            assertion          = "sn_min_length <= length <= sn_max_length"
            attributes         = ("sn", "sn_max_length", "sn_min_length")
            bindings           = dict \
                ( length       = "len (sn)"
                )

        # end class sn_length_valid

    # end class _Predicates

Phone = _PAP_Phone_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Phone
