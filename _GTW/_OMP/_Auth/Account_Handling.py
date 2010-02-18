# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.OMP.Auth.
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
#    GTW.OMP.Auth.Account_Handling
#
# Purpose
#    Define the links used during the create/modify process for accounts
#
# Revision Dates
#    18-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

from   _GTW._OMP._Auth        import Auth
import _GTW._OMP._Auth.Entity
import _GTW._OMP._Auth.Account

from   _TFL.I18N              import _, _T, _Tn

_Ancestor_Essence = MOM.Link1

class _Account_Action_ (_Ancestor_Essence) :
    """Base class for different actions for a account."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Account which this action is bound to."""

            role_type     = Auth.Account

        # end class left

        class expires (A_Date_Time) :
            """Exipre time of this action"""

            kind         = Attr.Required

        # end class expires

        class token (A_String) :
            """Unique token which identifies this action."""

            kind         = Attr.Primary

        # end class token

    # end class _Attributes

# end class _Account_Action_

_Ancestor_Essence = _Account_Action_

class Account_Activation (_Ancestor_Essence) :
    """Pending account activation"""

# end class Account_Activation

_Ancestor_Essence = _Account_Action_

class Account_Rename (_Ancestor_Essence) :
    """Pending renaming of an account."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class new_email (A_Email) :
            """The new email address for the linked account."""

            kind               = Attr.Required

        # end class old_email

    # end class _Attributes

# end class Account_Rename

_Ancestor_Essence = _Account_Action_

class Account_Pasword_Reset (_Ancestor_Essence) :
    """A password reset is pending for the linked account."""

# end class Account_Pasword_Reset

_Ancestor_Essence = _Account_Action_

class Account_Oassword_Change_Required (_Ancestor_Essence) :
    """The password of the linked account must be changed after the next
       login.
    """

# end class Account_Oassword_Change_Required

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
### __END__ GTW.OMP.Auth.Account_Handling
