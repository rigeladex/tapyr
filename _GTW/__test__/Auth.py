# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.Auth
#
# Purpose
#    Tests for the GTW.RST.TOP.Auth classes
#
# Revision Dates
#    16-Aug-2012 (MG) Creation
#    25-Sep-2012 (CT) Fix `_register` errors
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

_login_logout = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite", "-smtp=None"])
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> resp   = simulate_post (root, "/Auth/login.html")
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          A user name is required to login.
        </li><li class="error">
          The password is required.
        </li>

    >>> data   = dict (username = "a1")
    >>> resp   = simulate_post (root, "/Auth/login.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          The password is required.
        </li>

    >>> data ["password"] = "p2"
    >>> resp   = simulate_post (root, "/Auth/login.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Username or password incorrect
        </li>

    >>> data ["password"] = "p1"
    >>> data ["next"]     = "/after/login"
    >>> resp   = simulate_post (root, "/Auth/login.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <BLANKLINE>
    >>> resp.headers ["Location"] ### login
    'http://localhost/after/login'

    >>> resp = simulate_post (root, "/Auth/logout.html", data = dict (next = "/after/logout"))
    >>> resp
    <BaseResponse 9 bytes [303 SEE OTHER]>
    >>> resp.headers ["Location"] ### logout
    'http://localhost/after/logout'

    >>> data ["username"] = "a3"
    >>> data ["password"] = "p3"
    >>> resp   = simulate_post (root, "/Auth/login.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          This account is currently inactive
        </li>

    >>> a2 = Auth.Account.query (name = "a2").one ()
    >>> a2.password_change_required
    >>> data ["username"] = "a2"
    >>> data ["password"] = "p2"
    >>> resp   = simulate_post (root, "/Auth/login.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    >>> resp.headers ["Location"] ### login a2
    'http://localhost/after/login'

    >>> Auth.Account.force_password_change (a2)
    >>> a2.password_change_required
    Auth.Account_Password_Change_Required ((u'a2', ))
    >>> resp   = simulate_post (root, "/Auth/login.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    >>> resp.headers ["Location"] ### login a2 - redirect to change passwd
    'http://localhost/Auth/change_password?p=2'

    >>> scope.destroy ()
"""

_activate        = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite"])
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> a2     = Auth.Account.query (name = "a2").one ()
    >>> passwd = a2.prepare_activation ()
    >>> scope.commit ()

    >>> resp   = simulate_get (root, "/Auth/activate.html", query_string = "p=%d" % (a2.pid, ))
    >>> print ("".join (str (t) for t in find_tag (resp, "li", id = "account-name")))
    <li id="account-name">a2</li>

    >>> data   = dict (username = a2.name)
    >>> resp   = simulate_post (root, "/Auth/activate.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Username or password incorrect
        </li><li class="error">
          The password is required.
        </li><li class="error">
          The password is required.
        </li><li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["password"] = passwd
    >>> resp   = simulate_post (root, "/Auth/activate.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          The password is required.
        </li><li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["npassword"] = "P2"
    >>> resp   = simulate_post (root, "/Auth/activate.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["vpassword"] = "p2"
    >>> resp   = simulate_post (root, "/Auth/activate.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          The passwords don't match.
        </li>

    >>> data ["vpassword"] = "P2"
    >>> resp   = simulate_post (root, "/Auth/activate.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <BLANKLINE>

    >>> scope.destroy ()
"""

_register        = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite"]) # doctest:+ELLIPSIS
    ...
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> resp   = simulate_get (root, "/Auth/register.html")
    >>> print ("\n".join (str (sorted (t.attrs)) for t in find_tag (resp, "input")))
    [(u'id', u'F_username'), (u'name', u'username'), (u'type', u'text')]
    [(u'id', u'F_npassword'), (u'name', u'npassword'), (u'type', u'password')]
    [(u'id', u'F_vpassword'), (u'name', u'vpassword'), (u'type', u'password')]
    [(u'title', u'Update Email'), (u'type', u'submit'), (u'value', u'Update Email')]
    [(u'name', u'next'), (u'type', u'hidden')]

    >>> data   = dict ()
    >>> resp   = simulate_post (root, "/Auth/register.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          A user name is required to login.
        </li><li class="error">
          The password is required.
        </li><li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["username"] = "a2"
    >>> resp   = simulate_post (root, "/Auth/register.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Account with this Email address already registered
        </li><li class="error">
          The password is required.
        </li><li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["username"] = "new-account"
    >>> data ["npassword"] = "new-pass"
    >>> resp   = simulate_post (root, "/Auth/register.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["vpassword"] = "newpass"
    >>> resp   = simulate_post (root, "/Auth/register.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          The passwords don't match.
        </li>

    >>> data ["vpassword"] = "new-pass"
    >>> resp   = simulate_post (root, "/Auth/register.html", data = data) # doctest:+ELLIPSIS
    Email via localhost from webmaster@ to ['new-account']
    Content-type: text/plain; charset=utf-8
    Date: ...
    Subject: Email confirmation for localhost
    To: new-account
    From: webmaster@
    <BLANKLINE>
    Confirm new email address new-account
    <BLANKLINE>
    To verify the new email address, please click the following link: http://localhost/Auth/action?...
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <BLANKLINE>

    >>> a = Auth.Account.query (name = "new-account").one ()
    >>> links = Auth._Account_Token_Action_.query ().all ()
    >>> len (links)
    1
    >>> resp = simulate_get (root, "/Auth/action.html?p=%d&t=%s" % (a.pid, links [0].token))
    >>> resp.headers ["Location"]
    'http://localhost/'

    >>> links = Auth._Account_Token_Action_.query ().all ()
    >>> len (links)
    0

    >>> scope.destroy ()
"""

_change_email    = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite", "-smtp="])
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> a2     = Auth.Account.query (name = "a2").one ()
    >>> passwd = "p2"

    >>> resp   = simulate_get (root, "/Auth/change_email.html", query_string = "p=%d" % (a2.pid, ))
    >>> print ("".join (str (t) for t in find_tag (resp, "li", id = "account-name")))
    <li id="account-name">a2</li>

    >>> data   = dict (username = a2.name)
    >>> resp   = simulate_post (root, "/Auth/change_email.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Username or password incorrect
        </li><li class="error">
          The password is required.
        </li><li class="error">
          The Email is required.
        </li><li class="error">
          Repeat the EMail for verification.
        </li>

    >>> data ["password"] = passwd
    >>> resp   = simulate_post (root, "/Auth/change_email.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          The Email is required.
        </li><li class="error">
          Repeat the EMail for verification.
        </li>

    >>> data ["nemail"] = "new-email"
    >>> resp   = simulate_post (root, "/Auth/change_email.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Repeat the EMail for verification.
        </li>

    >>> data ["vemail"] = "newemail"
    >>> resp   = simulate_post (root, "/Auth/change_email.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          The Email's don't match.
        </li>

    >>> data ["vemail"] = "new-email"
    >>> resp   = simulate_post (root, "/Auth/change_email.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <BLANKLINE>

    >>> links = Auth._Account_Token_Action_.query ().all ()
    >>> len (links)
    1
    >>> resp = simulate_get (root, "/Auth/action.html?p=2&t=%s" % links [0].token)
    >>> resp.headers ["Location"]
    'http://localhost/'

    >>> links = Auth._Account_Token_Action_.query ().all ()
    >>> len (links)
    0

    >>> scope.destroy ()
"""

_change_password = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite"])
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> a2     = Auth.Account.query (name = "a2").one ()
    >>> passwd = "p2"
    >>> scope.commit ()

    >>> resp   = simulate_get (root, "/Auth/change_password.html", query_string = "p=%d" % (a2.pid, ))
    >>> print ("".join (str (t) for t in find_tag (resp, "li", id = "account-name")))
    <li id="account-name">a2</li>

    >>> data   = dict (username = a2.name)
    >>> resp   = simulate_post (root, "/Auth/change_password.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Username or password incorrect
        </li><li class="error">
          The password is required.
        </li><li class="error">
          The password is required.
        </li><li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["password"] = passwd
    >>> resp   = simulate_post (root, "/Auth/change_password.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          The password is required.
        </li><li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["npassword"] = "P2"
    >>> resp   = simulate_post (root, "/Auth/change_password.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Repeat the password for verification.
        </li>

    >>> data ["vpassword"] = "p2"
    >>> resp   = simulate_post (root, "/Auth/change_password.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          The passwords don't match.
        </li>

    >>> data ["vpassword"] = "P2"
    >>> resp   = simulate_post (root, "/Auth/change_password.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <BLANKLINE>

    >>>
    >>> scope.destroy ()
"""

_password_reset  = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite", "-smtp="])
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> data   = dict ()
    >>> resp   = simulate_post (root, "/Auth/request_reset_password.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          A user name is required to login.
        </li>

    >>> data ["username"]= "a5"
    >>> resp   = simulate_post (root, "/Auth/request_reset_password.html", data = data)
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))
    <li class="error">
          Account could not be found
        </li>

    >>> data ["username"]= "a2"
    >>> resp   = simulate_post (root, "/Auth/request_reset_password.html", data = data)# doctest:+ELLIPSIS
    >>> errors = find_tag (resp, "li", class_ = "error")
    >>> print ("".join (str (e)for e in errors))

    >>> scope.destroy ()
"""


from  _GTW.__test__.model import *
import BeautifulSoup
from   werkzeug.test     import Client
from   werkzeug.wrappers import BaseResponse
from  _TFL.User_Config   import user_config


def fixtures (self, scope) :
    Auth  = scope.Auth
    a1    = Auth.Account.create_new_account_x \
        ("a1", "p1", enabled = True,  suspended = False, superuser = True)
    a2    = Auth.Account.create_new_account_x \
        ("a2", "p2", enabled = True,  suspended = False, superuser = False)
    a3    = Auth.Account.create_new_account_x \
        ("a3", "p3", enabled = True,  suspended = True,  superuser = False)
    a3    = Auth.Account.create_new_account_x \
        ("a4", "p4", enabled = False, suspended = True , superuser = False)
    scope.commit ()
# end def fixtures

user_config.time_zone = "Europe/Vienna"

def simulate_post (root, url, ** options) :
    client       = Client      (root.wsgi_app, BaseResponse)
    response     = client.post (url, ** options)
    response.BS  = BeautifulSoup.BeautifulSoup (response.data)
    return response
# end def simulate_post

def simulate_get (root, url, ** options) :
    client       = Client     (root.wsgi_app, BaseResponse)
    response     = client.get (url, ** options)
    response.BS  = BeautifulSoup.BeautifulSoup (response.data)
    return response
# end def simulate_get

def find_tag (response, tag_pat, ** attrs) :
    if "class_" in attrs :
        attrs ["class"] = attrs.pop ("class_")
    return response.BS.findAll (tag_pat, ** attrs)
# end def find_tag

Scaffold.__class__.fixtures = fixtures

__test1__ = dict \
    ( login_logout    = _login_logout
    , activate        = _activate
    , reset_password  = _password_reset
    , register        = _register
    , change_password = _change_password
    , change_email    = _change_email
    )
__doc__ = _register
### __END__ GTW.__test__.Auth
