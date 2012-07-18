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

import _TFL.I18N

TFL.I18N.load ("en", "de")

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
    ...         , GTW.RST.TOP.L10N (name = "L10N", country_map = {"de" : "AT"})
    ...         )
    ...     )

    >>> root3
    <Root : />
    >>> root3.entries
    [<Page about: /about>, <Dir news: /news>, <Auth Auth: /Auth>, <L10N L10N: /L10N>]

    >>> ets = tuple (root3.entries_transitive)
    >>> ets
    (<Page about: /about>, <Dir news: /news>, <Page Sensation: /news/Sensation>, <Auth Auth: /Auth>, <L10N L10N: /L10N>, <_Language_ de: /L10N/de>, <_Language_ en: /L10N/en>)

    >>> sorted (root3._template_names)
    [u'account_activate', u'account_change_email', u'account_change_password', u'account_register', u'account_reset_password', u'console', u'e_type_aggregator', u'gallery', u'login', u'photo', u'regatta_calendar', u'regatta_page', u'regatta_registration', u'regatta_result', u'regatta_result_teamrace']

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

    >>> l10n = root3.SC.L10N
    >>> sorted (l10n._entry_map)
    [u'de', u'en']
    >>> sorted (l10n._entry_map.items ())
    [(u'de', <_Language_ de: /L10N/de>), (u'en', <_Language_ en: /L10N/en>)]

    >>> for k, v in sorted (root3.Status.Status.Table.iteritems ()) :
    ...     print (v)
    <HTTP status 100: Continue>
    <HTTP status 101: Switching protocols>
    <HTTP status 200: Ok>
    <HTTP status 201: Created>
    <HTTP status 202: Accepted>
    <HTTP status 203: Non authoritative information>
    <HTTP status 204: No content>
    <HTTP status 205: Reset content>
    <HTTP status 206: Partial content>
    <HTTP status 300: Multiple choices>
    <HTTP status 301: Moved permanently>
    <HTTP status 302: Found (moved temporarily)>
    <HTTP status 303: See other>
    <HTTP status 304: Not modified>
    <HTTP status 305: Use proxy>
    <HTTP status 307: Temporary redirect>
    <HTTP status 400: Bad request>
    <HTTP status 401: Unauthorized>
    <HTTP status 403: Forbidden>
    <HTTP status 404: Not found>
    <HTTP status 405: Method not allowed>
    <HTTP status 406: Not acceptable>
    <HTTP status 407: Proxy authentication required>
    <HTTP status 408: Request timeout>
    <HTTP status 409: Conflict>
    <HTTP status 410: Gone>
    <HTTP status 411: Lengthrequired>
    <HTTP status 412: Precondition failed>
    <HTTP status 413: Request entity too large>
    <HTTP status 414: Request uri too long>
    <HTTP status 415: Unsupported media type>
    <HTTP status 416: Requested range not satisfiable>
    <HTTP status 417: Expectation failed>
    <HTTP status 500: Internal server error>
    <HTTP status 501: Not implemented>
    <HTTP status 502: Bad gateway>
    <HTTP status 503: Service unavailable>
    <HTTP status 504: Gateway timeout>
    <HTTP status 505: Http version not supported>

"""

### __END__ GTW.RST.TOP.__test__
