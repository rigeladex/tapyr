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
#    GTW.OMP.SWP.Clip
#
# Purpose
#    Model a news clip
#
# Revision Dates
#     9-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
from   _MOM._Attr.Date_Interval import *

import _GTW._OMP._SWP.Page
from   _GTW._OMP._SWP.Format    import A_Format

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SWP.Link1

class Clip_O (_Ancestor_Essence) :
    """News clip for a object."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Object the news clip refers to"""

            role_type          = GTW.OMP.SWP.Object_PN
            role_name          = "object"
            auto_cache         = "clips"

        # end class left

        class date (A_Date_Interval) :
            """Publication (`start`) and expiration date (`finish`).
               Unspecified values will be taken from the web page the clip
               belongs to.
            """

            kind               = Attr.Primary_Optional
            ui_name            = "date"

        # end class date

        ### Non-primary attributes

        class abstract (A_Text) :
            """Text for news clip in markup specified by `format`."""

            kind               = Attr.Mandatory

        # end class abstract

        class alive (A_Boolean) :
            """Specifies whether entity is currently alive, i.e., the current
               date lies between `date.start` and `date.finish`.
            """

            kind               = Attr.Query
            auto_up_depends    = ("date", "left")
            ### need to recompute each time `alive` is accessed
            Kind_Mixins        = (Attr.Computed, )

            def query_fct (self) :
                return (Q.date.alive == True) ###  | (Q.left.alive == True)
            # end def query_fct

        # end class alive

        class date_z (A_Date_Interval) :

            kind               = Attr.Computed

            def computed (self, obj) :
                result = obj.date_x
                if result and obj.left :
                    if not (result.start and result.finish) :
                        result = self.C_Type \
                            ( start  = result.start  or obj.left.date.start
                            , finish = result.finish or obj.left.date.finish
                            )
                return result
            # end def computed

        # end class date

        class contents (A_Text) :
            """Contents of web page in html format"""

            kind               = Attr.Internal
            auto_up_depends    = ("abstract", )

            def computed (self, obj) :
                if obj.left :
                    return obj.left.format.convert (obj.abstract)
            # end def computed

        # end class contents

    # end class _Attributes

# end class Clip_O

_Ancestor_Essence = GTW.OMP.SWP.Page

class Clip_X (_Ancestor_Essence) :
    """News clip for the front page of a website referring to an external web
       page.
    """

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        head_line = None

        class link_to (A_Url) :
            """Url of external web page providing information about this clip"""

            kind               = Attr.Optional

        # end class link_to

        short_title = None

        class text (_Ancestor.text) :
            """Text for news clip in markup specified by `format`."""

        # end class text

        class title (_Ancestor.title) :
            """Title of news clip."""

        # end class title

    # end class _Attributes

# end class Clip_X

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Clip
