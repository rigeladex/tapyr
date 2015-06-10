# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    18-Jun-2013 (CT) Add `import_MOM`, fix `root3._template_names` output
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM           import *
from   _GTW._RST._TOP.import_TOP import *

from   _TFL.portable_repr        import portable_repr
from   _TFL.pyk                  import pyk

import _TFL.I18N

TFL.I18N.load ("en", "de")

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

    >>> print (portable_repr (sorted (root3._template_names)))
    ['account_change_email', 'account_change_password', 'account_make_cert', 'account_register', 'account_reset_password', 'calendar', 'calendar_day', 'console', 'e_type_admin', 'e_type_aggregator', 'e_type_display', 'e_type_mf3', 'gallery', 'login', 'photo', 'regatta_calendar', 'regatta_page', 'regatta_page_r', 'site_admin']

    >>> auth = root3.SC.Auth
    >>> auth
    <Auth Auth: /Auth>
    >>> print (portable_repr (sorted (auth._entry_map)))
    []
    >>> auth._get_child ("login")
    <_Login_ login: /Auth/login>
    >>> print (portable_repr (sorted (auth._entry_map)))
    ['login']
    >>> auth._get_child ("register")
    <_Register_ register: /Auth/register>
    >>> print (portable_repr (sorted (auth._entry_map)))
    ['login', 'register']
    >>> auth._get_child ("activate")
    <_Activate_ activate: /Auth/activate>
    >>> print (portable_repr (sorted (auth._entry_map)))
    ['activate', 'login', 'register']

    >>> l10n = root3.SC.L10N
    >>> print (portable_repr (sorted (l10n._entry_map)))
    ['de', 'en']
    >>> print (portable_repr (sorted (l10n._entry_map.items ())))
    [('de', <_Language_ de: /L10N/de>), ('en', <_Language_ en: /L10N/en>)]

    >>> for k, v in sorted (pyk.iteritems (root3.Status.Status.Table)) :
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
    <HTTP status 411: Length required>
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
