# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SWP.
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
#    GTW.OMP.SWP.Page
#
# Purpose
#    Model a static web page
#
# Revision Dates
#    31-Jan-2010 (CT) Creation
#     2-Feb-2010 (CT) Creation continued
#     9-Feb-2010 (CT) Creation continued..
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _MOM._Attr.Lifetime    import *

from   _GTW                   import GTW

import _GTW._OMP._SWP.Entity
from   _GTW._OMP._SWP.Format  import A_Format

from   _TFL.I18N              import _, _T, _Tn

import datetime

_Ancestor_Essence = GTW.OMP.SWP.Object

class Page (_Ancestor_Essence) :
    """Model a static web page."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class perma_name (A_Date_Slug) :
            """Name used for perma-link."""

            kind               = Attr.Primary
            ui_name            = "Name"

        # end class perma_name

        ### Non-primary attributes

        class contents (A_Text) :
            """Contents of web page in html format"""

            kind               = Attr.Internal
            auto_up_depends    = ("format", "text")

            def computed (self, obj) :
                return obj.format.convert (obj.text)
            # end def computed

        # end class contents

        class date (A_Lifetime_N) :
            """Publication (`birth`) and expiration date (`death`) for the
               web page
            """

            kind               = Attr.Optional

            explanation        = """
              The page won't be visible before the publication date.

              After the expiration date, the page won't be displayed (except
              possibly in an archive).
              """

        # end class date

        class desc (A_String) :
            """Description of the page"""

            kind               = Attr.Optional
            max_length         = 160
            ui_name            = "Description"

        # end class desc

        class format (A_Format) :
            """Markup format used for `text` of web page"""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = GTW.OMP.SWP.Format.ReST


        # end class format

        class text (A_Text) :
            """Text for web page in markup specified by `format`."""

            kind               = Attr.Required
            Kind_Mixins        = (Attr.Mandatory_Mixin, )

        # end class text

        class title (A_String) :
            """Title of the web page"""

            kind               = Attr.Optional
            max_length         = 80

        # end class title

    # end class _Attributes

# end class Page

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Page
