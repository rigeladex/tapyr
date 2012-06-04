# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.Document
#
# Purpose
#    Model a document linked to some other entity
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *

_Ancestor_Essence = MOM.Link1

class Document (_Ancestor_Essence) :
    """Model a document linked to some other entity."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Entity the document applies to."""

            role_type          = MOM.Id_Entity
            role_name          = "entity"

        # end class left

        class url (A_Url) :
            """Location of document."""

            kind               = Attr.Primary
            completer          = Attr.Completer_Spec  (4, Attr.Selector.primary)

        # end class url

        class type (A_String) :
            """Type of document (e.g., picture, user manual)."""

            kind               = Attr.Primary_Optional
            max_length         = 24
            ignore_case        = True
            completer          = Attr.Completer_Spec (1)

        # end class type

        ### Non-primary attributes

        class desc (A_String) :
            """Description of document."""

            kind               = Attr.Optional
            max_length         = 160
            ui_name            = "Description"

        # end class description

    # end class _Attributes

# end class Document

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Document
