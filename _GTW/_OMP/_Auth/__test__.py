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
#    GTW.OMP.Auth.__test__
#
# Purpose
#    Test for the Auth object model
#
# Revision Dates
#    18-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--
"""
Test if we can set a e-type specific manager class
>>> scope.Auth.Account_P.__class__
<class '_GTW._OMP._Auth.Account.Account_P_Manager'>
>>> scope.Auth.Account_Activation.__class__
<class '_GTW._OMP._Auth.Account_Handling.Account_Token_Manager'>

let's create some accounts
>>> acc1 = scope.Auth.Account_P ("user1@example.com", password = "passwd1")
>>> acc2 = scope.Auth.Account_P ("user2@example.com", password = "passwd1")
>>> acc1.name, acc2.name
(u'user1@example.com', u'user2@example.com')

Make sure that only hased versions of the passwords are stored
>>> acc1.password != "passwd1", acc2.password != "passwd2"
(True, True)

and that both account's use a different salt
>>> acc1.salt != acc2.salt
True

Now, let's test the login/logout handlers
>>> GET ("/account/login")
>>> HTTP.Handler.context ["login_form"] is not None
True
>>> POST  ("/account/login")
>>> form = HTTP.Handler.context ["login_form"]
>>> sorted (form.field_errors.iteritems ())
[('password', [u'The password is required.']), ('username', [u'A user name is required to login.'])]
>>> POST ( "/account/login", username = acc1.name, password = "passwd2")
>>> form = HTTP.Handler.context ["login_form"]
>>> form.errors, sorted (form.field_errors.iteritems ())
([u'Username or password incorrect'], [])
>>> POST ("/account/login", username = acc1.name, password = "passwd1", next = "/next")
Traceback (most recent call last):
    ...
Redirect_302: /next
>>> HTTP.Handler.session ["username"] == acc1.name
True

>>> GET ("/account/logout")
Traceback (most recent call last):
    ...
Redirect_302: /
>>> HTTP.Handler.session.get ("username") == acc1.name
False
>>> HTTP.Handler.session.get ("username") is None
True

>>> GET ("/account/logout", headers = dict (Referer = "/i-was-here"))
Traceback (most recent call last):
    ...
Redirect_302: /i-was-here

>>> POST ("/account/login", username = acc1.name, password = "passwd1")
Traceback (most recent call last):
    ...
Redirect_302: None
>>> HTTP.Handler.session ["username"] == acc1.name
True

>>> POST ("/account/login", username = acc1.name, password = "passwd2")
>>> NAV.universal_view \\
...   ( HTTP.Handler
...       ( "/account/login", "POST"
...       , username = acc1.name
...       , password = "passwd2"
...       , next     = "/next"
...       )
...   )
>>> HTTP.Handler.session.get ("username") is None
True


>>> action_1 = scope.Auth.Account_Activation               (acc1)
>>> action_2 = scope.Auth.Account_Rename                   (acc1)
>>> action_3 = scope.Auth.Account_Pasword_Reset            (acc1)
>>> action_4 = scope.Auth.Account_Password_Change_Required (acc1)
>>> actions = scope.Auth._Account_Action_.query (account = acc1).all ()
>>> [(a.type_name, a.account.name) for a in actions] # doctest: +NORMALIZE_WHITESPACE
[('GTW.OMP.Auth.Account_Pasword_Reset', u'user1@example.com'), ('GTW.OMP.Auth.Account_Password_Change_Required', u'user1@example.com'), ('GTW.OMP.Auth.Account_Rename', u'user1@example.com'), ('GTW.OMP.Auth.Account_Activation', u'user1@example.com')]
"""
from   _MOM.__test__                 import *
from   _GTW                          import GTW
from   _MOM._EMS.Hash                import Manager as EMS
from   _MOM._DBW._HPS.Manager        import Manager as DBW
import _GTW._NAV.Base
import _GTW._NAV.Auth
from   _GTW._NAV._Test               import HTTP
from   _GTW._NAV._Test               import Templateer
import _GTW._OMP._Auth
import _GTW._OMP._Auth.import_Auth

apt       = define_app_type ("Auth_Test", GTW, EMS, DBW, Auth = GTW.OMP.Auth)
scope     = MOM.Scope.new                (apt, None)
anonymous = scope.Auth.Account_Anonymous ("anonymous")
NAV       = GTW.NAV.Root \
    ( src_dir           = "."
    , copyright_start   = 2008
    , encoding          = "iso-8859-15"
    , input_encoding    = "iso-8859-15"
    , account_manager   = scope.Auth.Account
    , anonymous         = anonymous
    , scope             = scope
    , HTTP              = HTTP
    , Templateer        = Templateer
    )
NAV.add_entries \
    ( ( dict
          ( src_dir         = "account"
          , prefix          = "account"
          , title           = u"Accounthandling"
          , Type            = GTW.NAV.Auth
          )
      ,
      )
    )

def GET (url, * args, ** kw) :
    return NAV.universal_view (HTTP.Handler (url, "GET", * args, ** kw))
# end def GET

def POST (url, * args, ** kw) :
    return NAV.universal_view (HTTP.Handler (url, "POST", * args, ** kw))
# end def POST

#print NAV.top.Table
### __END__ GTW.OMP.Auth.__test__


