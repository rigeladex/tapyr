# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
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
#    GTW.__test__.NAV
#
# Purpose
#    Test GTW.NAV functionality
#
# Revision Dates
#    27-Jan-2012 (CT) Creation
#     2-Jun-2012 (CT) Rename `suppress_translation_loading` to `load_I18N`
#    26-Jul-2012 (CT) Adapt to use of `GTW.RST.TOP` instead of `GTW.NAV`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_test_code = """

    >>> nav_root = app
    >>> TTT      = nav_root.Templateer.Template_Type
    >>> print nav_root.abs_href
    /

    >>> for t in sorted (nav_root.template_iter ()) :
    ...    print t.name
    400
    401
    403
    404
    405
    408
    500
    503
    account_activate
    account_change_email
    account_change_password
    account_register
    account_reset_password
    console
    e_type_admin
    e_type_afs
    e_type_afs|afs_div_seq
    e_type_afs|afs_div_seq|afs_fc_horizo
    e_type_aggregator
    e_type_delete
    gallery
    html/static.jnj
    login
    photo
    regatta_calendar
    regatta_page
    regatta_registration
    regatta_result
    regatta_result_teamrace
    site_admin

    >>> for k in sorted (TTT.css_href_map) :
    ...    print k
    400
    401
    403
    404
    405
    408
    500
    503
    account_activate
    account_change_email
    account_change_password
    account_register
    account_reset_password
    console
    e_type_admin
    e_type_afs
    e_type_afs|afs_div_seq
    e_type_afs|afs_div_seq|afs_fc_horizo
    gallery
    html/static.jnj
    login
    photo
    site_admin

    >>> for owl in nav_root.own_links_transitive :
    ...   if not owl.hidden:
    ...     print owl.href, owl.template.name
    Admin site_admin
    Admin/Benutzerverwaltung site_admin
    Admin/Personenverwaltung site_admin
    Admin/Personenverwaltung/Address e_type_admin
    Admin/Personenverwaltung/Company e_type_admin
    Admin/Personenverwaltung/Company_has_Address e_type_admin
    Admin/Personenverwaltung/Company_has_Email e_type_admin
    Admin/Personenverwaltung/Company_has_Phone e_type_admin
    Admin/Personenverwaltung/Email e_type_admin
    Admin/Personenverwaltung/Entity_created_by_Person e_type_admin
    Admin/Personenverwaltung/Person e_type_admin
    Admin/Personenverwaltung/Person_has_Address e_type_admin
    Admin/Personenverwaltung/Person_has_Email e_type_admin
    Admin/Personenverwaltung/Person_has_Phone e_type_admin
    Admin/Personenverwaltung/Phone e_type_admin
    Admin/Regattaverwaltung site_admin
    Admin/Regattaverwaltung/Boat e_type_admin
    Admin/Regattaverwaltung/Boat_Class e_type_admin
    Admin/Regattaverwaltung/Boat_in_Regatta e_type_admin
    Admin/Regattaverwaltung/Club e_type_admin
    Admin/Regattaverwaltung/Regatta_C e_type_admin
    Admin/Regattaverwaltung/Regatta_Event e_type_admin
    Admin/Regattaverwaltung/Regatta_H e_type_admin
    Admin/Regattaverwaltung/Regatta_Page e_type_admin
    Admin/Regattaverwaltung/Sailor e_type_admin
    Admin/Regattaverwaltung/Team e_type_admin
    Admin/Regattaverwaltung/Team_has_Boat_in_Regatta e_type_admin
    Admin/Webseitenverwaltung site_admin
    Admin/Webseitenverwaltung/Calendar e_type_admin
    Admin/Webseitenverwaltung/Clip_X e_type_admin
    Admin/Webseitenverwaltung/Event e_type_admin
    Admin/Webseitenverwaltung/Gallery e_type_admin
    Admin/Webseitenverwaltung/Page e_type_admin
    Admin/Webseitenverwaltung/Picture e_type_admin

    >>> php = nav_root.resource_from_href ("Admin/Personenverwaltung/Person_has_Phone/create")
    >>> print php.href, php.template.name
    Admin/Personenverwaltung/Person_has_Phone/create e_type_afs|afs_div_seq

    >>> css_map = TFL.defaultdict (list)
    >>> for k, v in TTT.css_href_map.iteritems () :
    ...     css_map [v].append (k)
    >>> css_users = sorted (sorted (vs) for vs in css_map.itervalues ())
    >>> print formatted (css_users)
    [
      [ 400
      , 401
      , 403
      , 404
      , 405
      , 408
      , 500
      , 503
      , 'account_activate'
      , 'account_change_email'
      , 'account_change_password'
      , 'account_register'
      , 'account_reset_password'
      , 'html/static.jnj'
      , 'login'
      ]
    , [ 'console' ]
    , [ 'e_type_admin' ]
    ,
      [ 'e_type_afs'
      , 'e_type_afs|afs_div_seq'
      , 'e_type_afs|afs_div_seq|afs_fc_horizo'
      ]
    , [ 'gallery' ]
    , [ 'photo' ]
    , [ 'site_admin' ]
    ]

"""

import os
os.environ.update \
    ( dict
        ( GTW_FULL_OBJECT_MODEL = "True"
        )
    )

from   _GTW.__test__.model      import *

from   _TFL.Formatter           import Formatter

formatted = Formatter (width = 240)

__test__ = dict \
    ( NAV_test = _test_code
    )

app = Scaffold \
    ( [ "wsgi"
      , "-db_url",    "hps://"
      , "-db_name",   "test"
      , "-debug",     "yes"
      , "-load_I18N", "no"
      ]
    )

### __END__ GTW.__test__.NAV
