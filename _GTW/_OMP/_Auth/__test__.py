# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
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
#    12-May-2010 (CT) Use `pid`, not `lid`
#    15-Dec-2010 (CT) s/Account_Pasword_Reset/Account_Password_Reset/
#     5-Apr-2012 (CT) Use `.create_new_account_x` to create accounts
#    28-Jan-2013 (CT) Fix spelling of `Action_Expired`
#    ««revision-date»»···
#--

"""
Test if we can set a e-type specific manager class
    >>> scope.Auth.Account.__class__
    <class '_GTW._OMP._Auth.Account.Account_Manager'>
    >>> scope.Auth.Account_EMail_Verification.__class__
    <class '_GTW._OMP._Auth.Account_Handling.Account_Token_Manager'>

let's create some accounts
    >>> acc1 = scope.Auth.Account.create_new_account_x  \\
    ...     ("user1@example.com", password = "passwd1", enabled = True)
    >>> acc2 = scope.Auth.Account.create_new_account_x  \\
    ...     ("user2@example.com", password = "passwd1", enabled = True)
    >>> acc1.suspended = acc2.suspended = False
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
    >>> print handler.session.notifications.discarge ()
    Logout successfull.
    >>> print handler.session.notifications.discarge ()
    <BLANKLINE>
    >>> handler = GET ("/account/logout", headers = dict (Referer = "/i-was-here"))
    Traceback (most recent call last):
        ...
    Redirect_302: /i-was-here
    >>> print handler.session.notifications.discarge ()
    Logout successfull.

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
    >>> scope.Auth.Account.force_password_change (acc1)
    >>> scope.Auth.Account_Password_Change_Required.query (account = acc1).count ()
    1
    >>> scope.Auth.Account.force_password_change (acc1)
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
    >>> print handler.session.notifications.discarge ()
    The password has been changed.
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
    >>> print handler.session.notifications.discarge ()
    The reset password instructions have been sent to your email address.

    >>> acc2.active
    False
    >>> handler = POST ("/account/request_reset_password", username = acc2.name)
    Traceback (most recent call last):
        ....
    Redirect_302: /
    >>> print handler.session.notifications.discarge ()
    The reset password instructions have been sent to your email address.
    >>> reset_pwd  = scope.Auth.Account_Password_Reset.query (account = acc2).all ()
    >>> new_password_1 = reset_pwd [0].password
    >>> new_password_2 = reset_pwd [1].password
    >>> len (reset_pwd)
    2
    >>> scope.Auth.Account_Password_Change_Required.query (account = acc2).count ()
    1

Try to verify the `new` passwords
    >> acc2.verify_password (new_password_1), acc2.verify_password (new_password_2)
    False, False

    >>> url = "/account/action/%s/%s" % (acc1.pid, reset_pwd [0].token)
    >>> handler = GET (url)
    Traceback (most recent call last):
        ....
    Error_404
    >>> scope.Auth.Account_Password_Reset.query (account = acc2).count ()
    2
    >>> scope.Auth.Account_Password_Change_Required.query (account = acc2).count ()
    1
    >>> reset_link = reset_pwd [0]
    >>> url        = "/account/action/%s/%s" % (acc2.pid, reset_link.token)
    >>> handler    = GET (url)
    Traceback (most recent call last):
        ....
    Redirect_302: /account/change_password/3

    >>> acc2.verify_password (reset_link.password)
    True
    >>> scope.Auth.Account_Password_Reset.query (account = acc2).count ()
    0
    >>> scope.Auth.Account_Password_Change_Required.query (account = acc2).count ()
    1
    >>> acc1.set (enabled = False)
    1
    >>> new_password_1 = scope.Auth.Account.reset_password (acc1)
    Traceback (most recent call last):
        ....
    TypeError: Account has been disabled
    >>> acc1.set (enabled = True)
    1

Account activation
    >>> acc3 = scope.Auth.Account ("user3@example.com", enabled = True)
    >>> acc3.active, acc3.suspended
    (False, True)
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
    >>> print handler.session.notifications.discarge ()
    Activation successfull.
    >>> acc3.verify_password ("passwd3")
    True
    >>> acc3.active
    True
    >>> acc3.activation

Change E-Mail address
    >>> cp_url  = "/account/change_email/%s" % (acc3.pid, )
    >>> handler = GET  (cp_url)
    >>> handler = POST (cp_url)
    >>> form = handler.context ["form"]
    >>> form.errors, sorted (form.field_errors.iteritems ())
    ([], [('new_email', [u'The new E-Mail address is required.']), ('password', [u'The old password is required.'])])
    >>> handler = POST \\
    ...   (cp_url, password = "passwd4", new_email = "user4@example.com")
    >>> form = handler.context ["form"]
    >>> form.errors, sorted (form.field_errors.iteritems ())
    ([], [('password', [u'The password is incorrect'])])
    >>> handler = POST \\
    ...   (cp_url, password = "passwd3", new_email = "user4@example.com")
    Traceback (most recent call last):
        ...
    Redirect_302: /
    >>> print handler.session.notifications.discarge ()
    A confirmation email has been sent to the new email address.
    >>> verify_links = scope.Auth.Account_EMail_Verification.query ().all ()
    >>> len (verify_links)
    1
    >>> url = "/account/action/%s/%s" % (acc1.pid, verify_links [0].token)
    >>> handler = GET (url)
    Traceback (most recent call last):
        ...
    Error_404
    >>> url = "/account/action/%s/%s" % (acc3.pid, verify_links [0].token)
    >>> handler = GET (url)
    Traceback (most recent call last):
        ...
    Redirect_302: /
    >>> scope.Auth.Account_EMail_Verification.query ().count ()
    0
    >>> acc3.name
    u'user4@example.com'

Register account
    >>> handler = GET  ("/account/register")
    >>> handler = POST ("/account/register")
    >>> form = handler.context ["form"]
    >>> form.errors, sorted (form.field_errors.iteritems ())
    ([], [('npassword1', [u'The new password is required.']), ('npassword2', [u'Please repeat the new password.']), ('username', [u'A user name is required to login.'])])
    >>> handler = POST \\
    ...     ( "/account/register"
    ...     , username   = acc3.name
    ...     , npassword1 = "passwd5"
    ...     , npassword2 = "passwd6"
    ...     )
    >>> form = handler.context ["form"]
    >>> form.errors, sorted (form.field_errors.iteritems ())
    ([], [('username', [u'This username is already in use.'])])
    >>> handler = POST \\
    ...     ( "/account/register"
    ...     , username   = "user5@example.com"
    ...     , npassword1 = "passwd5"
    ...     , npassword2 = "passwd6"
    ...     )
    >>> form = handler.context ["form"]
    >>> form.errors, sorted (form.field_errors.iteritems ())
    ([u"Passwords don't match."], [])
    >>> handler = POST \\
    ...     ( "/account/register"
    ...     , username   = "user5@example.com"
    ...     , npassword1 = "passwd5"
    ...     , npassword2 = "passwd5"
    ...     )
    Traceback (most recent call last):
        ...
    Redirect_302: /
    >>> form = handler.context ["form"]
    >>> acc5 = scope.Auth.Account.query (name = form.username).one ()
    >>> acc5.active, acc5.enabled, acc5.suspended
    (False, True, True)
    >>> links = scope.Auth.Account_EMail_Verification.query \\
    ...     (account = acc5).all ()
    >>> len (links)
    1
    >>> url = "/account/action/%s/%s" % (acc1.pid, links [0].token)
    >>> handler = GET (url)
    Traceback (most recent call last):
        ...
    Error_404
    >>> url = "/account/action/%s/%s" % (acc5.pid, links [0].token)
    >>> handler = GET (url)
    Traceback (most recent call last):
        ...
    Redirect_302: /
    >>> scope.Auth.Account_EMail_Verification.query (account = acc5).count ()
    0
    >>> acc5.active, acc5.enabled, acc5.suspended
    (True, True, False)

Test the expiration of action
    >>> import datetime
    >>> expires = datetime.datetime.utcnow () - datetime.timedelta (minutes = 1)
    >>> act = scope.Auth.Account_EMail_Verification (acc5, expires = expires)
    >>> act.handle ()
    Traceback (most recent call last):
        ...
    Action_Expired
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
    TFL.Environment.exec_python_startup (); import pdb; pdb.set_trace ()
    NAV.universal_view (handler)
    return handler
# end def GET

def POST (url, * args, ** kw) :
    handler = HTTP.Handler (url, "POST", * args, ** kw)
    NAV.universal_view (handler)
    return handler
# end def POST

### __END__ GTW.OMP.Auth.__test__
