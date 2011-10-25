# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.PAP.Person
#
# Purpose
#    Model a Person
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#    29-Jan-2010 (CT) `middle_name` added
#    10-Feb-2010 (CT) `birth_date (A_Date)` replaced by `date (A_Lifetime)`
#    22-Feb-2010 (CT) `ignore_case` set for primary attributes
#    24-Feb-2010 (CT) s/Lifetime/Date_Interval/
#    10-May-2010 (CT) `ui_display_format` redefined
#     4-Jun-2010 (CT) `sex` added
#    13-Oct-2010 (CT) `example` added
#     8-Jun-2011 (MG) `_AC_Query_LN_` and `last_name.ac_query` added
#     9-Jun-2011 (MG) `_AC_Query_LN_` enhanced
#     6-Jul-2011 (CT) s/_AC_Query_LN_/_AC_Query_FL_/, added to `first_name`, too
#     6-Jul-2011 (CT) `e_completer` added to primary attributes
#     6-Jul-2011 (CT) `f_completer` added to primary attributes and `salutation`
#    16-Jul-2011 (CT) `_AC_Query_FL_` derived from (newly factored) `_AC_Query_S_`
#    17-Jul-2011 (CT) s/f_completer/completer/, removed `e_completer`
#    12-Sep-2011 (CT) `prefix` added to `_AC_Query_FL_.query`
#    25-Oct-2011 (CT) `ui_display_format` format changed (put `last_name` first)
#    ««revision-date»»···
#--

from   _MOM.import_MOM             import *
from   _MOM._Attr.Date_Interval    import *

from   _GTW._OMP._PAP.Attr_Type    import *

from   _GTW                        import GTW
from   _GTW._OMP._PAP              import PAP
from   _TFL.I18N                   import _

import _GTW._OMP._PAP.Entity

_Ancestor_Essence = MOM.Object

class _AC_Query_FL_ (MOM.Attr._AC_Query_S_) :
    """Special auto-complete query function for the `first_name` and
       `last_name` of a person (to better handling of double names like
       Franz-Ferdinand).
    """

    def query (self, value, prefix = None) :
        aq = self.a_query (prefix)
        if value == "" :
            return aq.__eq__ (value)
        elif "-" in value :
            return aq.STARTSWITH (value)
        else :
            pvalue = "-%s" % (value, )
            return aq.STARTSWITH (value) | aq.CONTAINS (pvalue)
    # end def query

# end class _AC_Query_FL_

class _PAP_Person_ (PAP.Entity, _Ancestor_Essence) :
    """Model a person."""

    _real_name = "Person"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class _personal_name_ (A_String) :

            kind           = Attr.Primary
            ignore_case    = True

            @TFL.Meta.Once_Property
            def ac_query (self) :
                return _AC_Query_FL_ (self.ckd_name, self.cooked)
            # end def ac_query

        # end class _personal_name_

        class last_name (_personal_name_) :
            """Last name of person"""

            example        = u"Doe"
            max_length     = 48
            rank           = 1

            completer      = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class last_name

        class first_name (_personal_name_) :
            """First name of person"""

            example        = u"John"
            max_length     = 32
            rank           = 2

            completer      = Attr.Completer_Spec  (3, Attr.Selector.primary)

        # end class first_name

        class middle_name (A_String) :
            """Middle name of person"""

            kind           = Attr.Primary_Optional
            ignore_case    = True
            max_length     = 32
            rank           = 1

            completer      = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class middle_name

        class title (A_String) :
            """Academic title."""

            kind           = Attr.Primary_Optional
            ignore_case    = True
            max_length     = 20
            rank           = 2
            ui_name        = _("Academic title")

            completer      = Attr.Completer_Spec  (1)

        # end class title

        class lifetime (A_Date_Interval) :
            """Date of birth [`start`] (and death [`finish`])"""

            kind           = Attr.Optional

        # end class lifetime

        class salutation (A_String) :
            """Salutation to be used when communicating with person (e.g., in
               a letter or email).
            """

            kind               = Attr.Optional
            max_length         = 80

            completer          = Attr.Completer_Spec (1)

        # end class salutation

        class sex (A_Sex) :

            kind           = Attr.Necessary

        # end class sex

    # end class _Attributes

    @property
    def ui_display_format (self) :
        result = []
        if self.title :
            result.append ("%(title)s")
    @property
    def ui_display_format (self) :
        result = ["%(last_name)s %(first_name)s"]
        if self.middle_name :
            result.append (" %(middle_name)s")
        if self.title :
            result.append (", %(title)s")
        return "".join (result)
    # end def ui_display_format

Person = _PAP_Person_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Person
