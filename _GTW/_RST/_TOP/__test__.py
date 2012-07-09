# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
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
#    GTW.RST.TOP.__test__
#
# Purpose
#    Doctest for package GTW.RST.TOP
#
# Revision Dates
#     5-Jul-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW._RST._TOP.import_TOP import *

from   _TFL.Formatter            import Formatter, formatted_1

formatted = Formatter (width = 240)

__doc__ = """

    >>> entries = ( Page
    ...             ( name          = "about"
    ...             )
    ...         , Dir
    ...             ( name          = "news"
    ...             , entries       =
    ...                 ( Page
    ...                     ( name  = "Sensation"
    ...                     )
    ...                 ,
    ...                 )
    ...             )
    ...         )

    >>> root1 = Root (HTTP = None)
    >>> root1
    <Root : />
    >>> root1.entries
    []

    >>> root2 = Root (HTTP = None
    ...     , language = "en"
    ...     , entries  = entries
    ...     )
    >>> root2
    <Root : />
    >>> root2.entries
    [<Page about: /about>, <Dir news: /news>]
    >>> ets = tuple (root2.entries_transitive)
    >>> ets
    (<Page about: /about>, <Dir news: /news>, <Page Sensation: /news/Sensation>)

    >>> root3 = Root (HTTP = None
    ...     , language = "en"
    ...     , entries  = entries +
    ...         ( GTW.RST.TOP.Auth (name = "Auth")
    ...         ,
    ...         )
    ...     )

    >>> root3
    <Root : />
    >>> root3.entries
    [<Page about: /about>, <Dir news: /news>, <Auth Auth: /Auth>]

    >>> ets = tuple (root3.entries_transitive)
    >>> ets
    (<Page about: /about>, <Dir news: /news>, <Page Sensation: /news/Sensation>, <Auth Auth: /Auth>)

    >>> sorted (root3._template_names)
    [u'account_activate', u'account_change_email', u'account_change_password', u'account_register', u'account_reset_password', u'login']

    >>> auth = root3.SC.Auth
    >>> auth
    <Auth Auth: /Auth>
    >>> sorted (auth._entry_map)
    []
    >>> auth._get_child ("login")
    <_Login_ login: /Auth/login>
    >>> sorted (auth._entry_map)
    [u'login']
    >>> auth._get_child ("register")
    <_Register_ register: /Auth/register>
    >>> sorted (auth._entry_map)
    [u'login', u'register']
    >>> auth._get_child ("activate")
    <_Activate_ activate: /Auth/activate>
    >>> sorted (auth._entry_map)
    [u'activate', u'login', u'register']

"""

### __END__ GTW.RST.TOP.__test__
