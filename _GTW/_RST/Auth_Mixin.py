# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
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
#    GTW.RST.Auth_Mixin
#
# Purpose
#    Mixin for resources authenticating via GTW.OMP.Auth.Account
#
# Revision Dates
#     1-May-2013 (CT) Creation
#     6-May-2013 (CT) Change error format in `_authenticate`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource

from   _TFL.I18N                import _, _T, _Tn

import _TFL._Meta.Object

import collections

class Errors (collections.defaultdict) :

    __metaclass__ = TFL.Meta.M_Class

    def __init__ (self) :
        self.__super.__init__ (list)
    # end def __init__

# end class Errors

class Auth_Mixin (TFL.Meta.Object) :
    """Mixin for resources authenticating via GTW.OMP.Auth.Account"""

    active_account_required    = True
    skip_etag                  = True

    class _Auth_Mixin_POST_ (GTW.RST.POST) :

        _real_name             = "POST"
        account                 = None

        def get_account (self, resource, username, debug = False) :
            try :
                self.account = resource.account_manager.query \
                    (name = username).one ()
            except IndexError :
                self.account = None
                if debug :
                    self.errors ["username"].append \
                        ( "No account with username `%s` found"
                        % (username, )
                        )
                return False
            else :
                return True
        # end def get_account

        def _authenticate (self, resource, username, password, debug = False) :
            result = False
            self.get_account (resource, username, debug)
            if password and self.account :
                result = self.account.verify_password (password)
                if not result and debug :
                    self.errors ["password"].append \
                        ( "Password is wrong:\n"
                               "  'password' : '%s'\n"
                               "  hash db `%s`\n"
                               "  hash in `%s`"
                        % ( password
                          , self.account.password
                          , self.account.password_hash (password, self.account)
                          )
                        )
            return result
        # end def _authenticate

        def get_required (self, request, field_name, error) :
            value = request.req_data.get (field_name)
            if not value :
                self.errors [field_name].append (error)
            return value
        # end def get_required

        def get_username (self, request, field_name = "username") :
            return self.get_required \
                (request, field_name, _T ("A user name is required to login."))
        # end def get_required

        def get_password \
                ( self, request
                , field_name   = "password"
                , verify_field = None
                ) :
            password = self.get_required \
                (request, field_name, _T ("The password is required."))
            if verify_field :
                verify = self.get_required \
                    ( request, verify_field
                    , _T ("Repeat the password for verification.")
                    )
                if password and verify and (password != verify) :
                    self.errors [field_name].append \
                        (_T ("The passwords don't match."))
            return password
        # end def get_password

        def _credentials_validation \
                ( self, resource, request
                , username = "username"
                , password = "password"
                , debug    = False
                ) :
            username     = self.get_username (request, username)
            password     = self.get_password (request, password)
            error_add    = lambda e : self.errors [None].append (e)
            if not username :
                error_add (_T ("Please enter a username"))
            elif not self._authenticate \
                   (resource, username, password, debug) :
                error_add (_T ("Username or password incorrect"))
            elif resource.active_account_required and not self.account.active :
                error_add (_T ("This account is currently inactive"))
            elif self.errors and debug :
                error_add (repr (request.req_data))
            return username, password
        # end def _credentials_validation

    POST = _Auth_Mixin_POST_ # end class

# end class Auth_Mixin

if __name__ != "__main__" :
    GTW.RST._Export ("*")
### __END__ GTW.RST.Auth_Mixin
