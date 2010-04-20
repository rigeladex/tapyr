# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.Page
#
# Purpose
#    Model a web page with information about a sailing regatta
#
# Revision Dates
#    20-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
from   _MOM._Attr.Date_Interval import *

import _GTW._OMP._SRM.Entity
import _GTW._OMP._SRM.Regatta_Event

import _GTW._OMP._SWP.import_SWP

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link1
_Ancestor_Mixin   = GTW.OMP.SWP.Page_Mixin

class _SRM_Page_ (_Ancestor_Essence, _Ancestor_Mixin) :
    """Web page with information about a sailing regatta."""

    _real_name = "Page"
    ui_name    = "Regatta_Page"

    class _Attributes (_Ancestor_Essence._Attributes, _Ancestor_Mixin._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Regatta event to which this page belongs."""

            role_type          = GTW.OMP.SRM.Regatta_Event
            auto_cache         = True
            role_name          = "event"

        # end class event

        class perma_name (A_Date_Slug) :
            """Name used for perma-link."""

            kind               = Attr.Primary
            ui_name            = "Name"

            check              = ("""" " not in value""", )

        # end class perma_name

        ### Non-primary attributes

        class creator (A_Object) :
            """Creator of the contents."""

            kind               = Attr.Optional
            Class              = GTW.OMP.PAP.Person

        # end class creator

        class date (A_Date_Interval_N) :
            """Publication (`start`) and expiration date (`finish`)"""

            kind               = Attr.Optional

            explanation        = """
              The page won't be visible before the start date.

              After the finish date, the page won't be displayed (except
              possibly in an archive).
              """

        # end class date

        class desc (A_String) :
            """Description of the purpose of the page."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Mixin, )
            max_length         = 30

            def computed (self, obj) :
                return obj.perma_name.rsplit (".", 1) [0].capitalize ()
            # end def computed

        # end class desc

        class short_title (A_String) :
            """Short title (used in navigation)."""

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("desc", "left")

            def computed (self, obj) :
                if obj.desc and obj.event :
                    return "%s %s" % (obj.desc, obj.event.short_title)
            # end def computed

        # end class title

        class title (A_String) :
            """Title of the web page"""

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("desc", "left")

            def computed (self, obj) :
                if obj.desc and obj.event :
                    return "%s %s" % (obj.desc, obj.event.title)
            # end def computed

        # end class title

    # end class _Attributes

Page = _SRM_Page_ # end class

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Page
