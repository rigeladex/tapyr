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
>>> scope.Auth.Account_EMail_Verification.__class__
<class '_GTW._OMP._Auth.Account_Handling.Account_Token_Manager'>

let's create some accounts
>>> acc1 = scope.Auth.Account_P \\
...     ("user1@example.com", password = "passwd1", enabled = True)
>>> acc2 = scope.Auth.Account_P \\
...     ("user2@example.com", password = "passwd1", enabled = True)
>>> acc1.name, acc2.name
(u'user1@example.com', u'user2@example.com')

Make sure that only hased versions of the passwords are stored
>>> acc1.password != "passwd1", acc2.password != "passwd2"
(True, True)

and that both account's use a different salt
>>> acc1.salt != acc2.salt
True

Now, let's test the login/logout handlers
>>> handler = GET ("/account/login")
>>> handler.context ["login_form"] is not None
True
>>> handler = POST  ("/account/login")
>>> form = handler.context ["login_form"]
>>> sorted (form.field_errors.iteritems ())
[('password', [u'The password is required.']), ('username', [u'A user name is required to login.'])]
>>> handler = POST \\
...   ( "/account/login", username = acc1.name, password = "passwd2")
>>> form = handler.context ["login_form"]
>>> form.errors, sorted (form.field_errors.iteritems ())
([u'Username or password incorrect'], [])
>>> handler = POST \\
...  ("/account/login", username = acc1.name, password = "passwd1", next = "/next")
Traceback (most recent call last):
    ...
Redirect_302: /next
>>> handler.session ["username"] == acc1.name
True

>>> handler = GET ("/account/logout")
Traceback (most recent call last):
    ...
Redirect_302: /
>>> handler.session.get ("username") == acc1.name
False
>>> handler.session.get ("username") is None
True

>>> handler = GET ("/account/logout", headers = dict (Referer = "/i-was-here"))
Traceback (most recent call last):
    ...
Redirect_302: /i-was-here

>>> handler = POST ("/account/login", username = acc1.name, password = "passwd1")
Traceback (most recent call last):
    ...
Redirect_302: /
>>> handler.session ["username"] == acc1.name
True

>>> handler = POST \\
...   ("/account/login", username = acc1.name, password = "passwd2")
>>> handler.session.get ("username") is None
True

Now we test the password change required action
>>> scope.Auth.Account_P.force_password_change (acc1)
>>> scope.Auth.Account_Password_Change_Required.query (account = acc1).count ()
1
>>> scope.Auth.Account_P.force_password_change (acc1)
>>> scope.Auth.Account_Password_Change_Required.query (account = acc1).count ()
1
>>> handler = POST \\
...   ("/account/login", username = acc1.name, password = "passwd1")
Traceback (most recent call last):
    ...
Redirect_302: /account/change_password/2

Test the password change
>>> cpwd_url = "/account/change_password/2"
>>> handler  = GET (cpwd_url)
>>> [f.name for f in handler.context ["form"].fields]
['password', 'npassword1', 'npassword2']
>>> handler = POST (cpwd_url)
>>> sorted (handler.context ["form"].field_errors.iteritems ())
[('npassword1', [u'The new password is required.']), ('npassword2', [u'Please repeat the new password.']), ('password', [u'The old password is required.'])]
>>> handler = POST (cpwd_url, password = "?", npassword1 = "new-passwd", npassword2 = "new-passwd")
>>> form = handler.context ["form"]
>>> form.errors, sorted (form.field_errors.iteritems ())
([u'One of the passwords is incorrect'], [])
>>> handler = POST (cpwd_url, password = "passwd1", npassword1 = "passwd1", npassword2 = "passwd2")
>>> form = handler.context ["form"]
>>> form.errors, sorted (form.field_errors.iteritems ())
([u"Passwords don't match."], [])
>>> handler = POST (cpwd_url, password = "passwd1", npassword1 = "passwdn", npassword2 = "passwdn")
Traceback (most recent call last):
    ....
Redirect_302: /
>>> acc1.verify_password ("passwdn")
True
>>> scope.Auth.Account_Password_Change_Required.query (account = acc1).count ()
0

Next, we test the reset password functions
>>> acc2.active
True
>>> handler = GET ("/account/request_reset_password")
>>> handler = POST ("/account/request_reset_password", username = acc2.name)
Traceback (most recent call last):
    ....
Redirect_302: /
>>> acc2.active
False
>>> handler = POST ("/account/request_reset_password", username = acc2.name)
Traceback (most recent call last):
    ....
Redirect_302: /
>>> reset_pwd  = scope.Auth.Account_Pasword_Reset.query (account = acc2).all ()
>>> new_password_1 = reset_pwd [0].password
>>> new_password_2 = reset_pwd [1].password
>>> len (reset_pwd)
2
>>> scope.Auth.Account_Password_Change_Required.query (account = acc2).count ()
1

Try to verify the `new` passwords
>> acc2.verify_password (new_password_1), acc2.verify_password (new_password_2)
False, False

>>> url = "/account/reset_password/%s/%s" % (acc1.lid, reset_pwd [0].token)
>>> handler = GET (url)
Traceback (most recent call last):
    ....
Error_404
>>> scope.Auth.Account_Pasword_Reset.query (account = acc2).count ()
2
>>> scope.Auth.Account_Password_Change_Required.query (account = acc2).count ()
1
>>> reset_link = reset_pwd [0]
>>> url        = "/account/reset_password/%s/%s" % (acc2.lid, reset_link.token)
>>> handler    = GET (url)
Traceback (most recent call last):
    ....
Redirect_302: /account/change_password/3
>>> acc2.verify_password (reset_link.password)
True
>>> scope.Auth.Account_Pasword_Reset.query (account = acc2).count ()
0
>>> scope.Auth.Account_Password_Change_Required.query (account = acc2).count ()
1
>>> acc1.set (enabled = False)
1
>>> new_password_1 = scope.Auth.Account_P.reset_password (acc1)
Traceback (most recent call last):
    ....
TypeError: Account has been disabled
>>> acc1.set (enabled = True)
1

Account activation
>>> acc3        = scope.Auth.Account_P    ("user3@example.com")
>>> acc3.activation
>>> temp_passwd = acc3.prepare_activation ()
>>> acc3.activation
GTW.OMP.Auth.Account_Activation ((u'user3@example.com'))
>>> handler = GET ("/account/activate")
>>> handler = POST ("/account/activate")
>>> form = handler.context ["form"]
>>> form.errors, sorted (form.field_errors.iteritems ())
([], [('npassword1', [u'The new password is required.']), ('npassword2', [u'Please repeat the new password.']), ('password', [u'The password is required.']), ('username', [u'A user name is required to login.'])])
>>> handler = POST \\
...   ( "/account/activate", username = acc3.name, password = "?"
...   , npassword1 = "passwd3"
...   , npassword2 = "passwd3"
...   )
>>> form = handler.context ["form"]
>>> form.errors, sorted (form.field_errors.iteritems ())
([u'Username or password incorrect'], [])
>>> handler = POST \\
...   ( "/account/activate", username = acc3.name, password = temp_passwd
...   , npassword1 = "passwd3"
...   , npassword2 = "passwd3"
...   )
Traceback (most recent call last):
   ...
Redirect_302: /
>>> acc3.verify_password ("passwd3")
True
>>> acc3.activation
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
    handler = HTTP.Handler (url, "GET", * args, ** kw)
    NAV.universal_view (handler)
    return handler
# end def GET

def POST (url, * args, ** kw) :
    handler = HTTP.Handler (url, "POST", * args, ** kw)
    NAV.universal_view (handler)
    return handler
# end def POST

#print NAV.top.Table
### __END__ GTW.OMP.Auth.__test__


