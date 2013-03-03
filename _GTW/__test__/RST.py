# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.RST
#
# Purpose
#    Test RESTful api
#
# Revision Dates
#    27-Jun-2012 (CT) Creation
#    31-Jul-2012 (CT) Add `settimeout` to `run_server`, fix `except` clause
#     2-Aug-2012 (CT) Change sequence of tests in `test_post` (Postgresql
#                     wastes pids for a Name_Clash)
#     2-Aug-2012 (CT) Add `change_query_filters` for entities to `test_cqf`
#     7-Aug-2012 (CT) Add `test_doc`
#     8-Aug-2012 (CT) Add `test_example_*`, continue `test_doc`
#    18-Sep-2012 (CT) Factor _GTW/__test__/Test_Command.py
#     4-Oct-2012 (CT) Adapt to `?brief`
#     5-Oct-2012 (CT) Test `.get ("/v1/SRM-Regatta.csv?verbose")`
#     5-Oct-2012 (CT) Test multiple `AQ` arguments for a single `get`
#     5-Oct-2012 (CT) Test `fields` query argument
#    12-Oct-2012 (CT) Adapt to repr change of `An_Entity`
#    21-Nov-2012 (CT) Test invalid `AQ` argument
#    27-Nov-2012 (CT) Test `location` header of `POST`
#     6-Dec-2012 (CT) Remove `Entity_created_by_Person`
#    11-Dec-2012 (CT) Adapt to change in `HTTP_Status` response
#    12-Dec-2012 (CT) Use `+ELLIPSIS` instead of `Re_Replacer`
#     6-Jan-2013 (CT) Add `test_client`
#     9-Jan-2013 (CT) Factor `GTW_RST_Test_Command`, `rst_harness`
#     3-Mar-2013 (CT) Add `link: ...rel=doc` to `headers`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW.__test__.rst_harness  import *
from   _GTW.__test__              import rst_harness

import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._SRM.import_SRM

import _GTW._RST._MOM.Client

import datetime
import json

def run_server (db_url = "hps://", db_name = None) :
    return rst_harness.run_server ("_GTW.__test__.RST", db_url, db_name)
# end def run_server

class _GTW_Test_Command_ (GTW_RST_Test_Command) :

    _rn_prefix            = "_GTW_Test"

    PNS_Aliases           = dict \
        ( PAP             = GTW.OMP.PAP
        , SRM             = GTW.OMP.SRM
        , SWP             = GTW.OMP.SWP
        )

    SALT                  = bytes \
        ( "c9cac445-3fd8-451d-9eff-dd56c7a91485")

    def fixtures (self, scope) :
        PAP   = scope.PAP
        SRM   = scope.SRM
        BiR   = SRM.Boat_in_Regatta
        ct    = PAP.Person ("Tanzer", "Christian", raw = True)
        lt    = PAP.Person ("Tanzer", "Laurens", "William", raw = True)
        cat   = PAP.Person ("Tanzer", "Clarissa", "Anna", raw = True)
        ct_s  = SRM.Sailor (ct,  nation = "AUT", mna_number = "29676", raw = True)
        lt_s  = SRM.Sailor (lt,  nation = "AUT", raw = True)
        cat_s = SRM.Sailor (cat, nation = "AUT", raw = True)
        opti  = SRM.Boat_Class ("Optimist", max_crew = "1")
        b     = SRM.Boat ("Optimist", "AUT", "1107", raw = True)
        ys    = SRM.Handicap ("Yardstick", raw = True)
        rev   = SRM.Regatta_Event ("Himmelfahrt", ("20080501", ), raw = True)
        reg   = SRM.Regatta_C (rev, opti)
        reh   = SRM.Regatta_H (rev, ys)
        rev_g = SRM.Regatta_Event \
            ("Guggenberger", ("20080620", "20080621"), raw = True)
        reg_c = SRM.Regatta_C (rev_g, opti)
        bir   = SRM.Boat_in_Regatta (b, reg,   skipper = lt_s)
        bir_g = SRM.Boat_in_Regatta (b, reg_c, skipper = lt_s)
        scope.commit ()
    # end def fixtures

_Command_  = _GTW_Test_Command_ # end class

Scaffold   = _Command_ ()

### «text» ### The doctest follows::

_test_client = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> CC = GTW.RST.MOM.Client.Requester ("http://localhost:9999", verify = False)
    >>> CR = GTW.RST.MOM.Client.Requester ("http://localhost:9999", raw = True)

    >>> r = CC.get ("")
    >>> r._url
    u'http://localhost:9999/'
    >>> [e._url for e in r]
    [u'http://localhost:9999/v1', u'http://localhost:9999/Doc', u'http://localhost:9999/RAISE']

    >>> r1 = r [0] [0]
    >>> [e._url for e in r1._entries [:3]]
    [u'/v1/MOM-Id_Entity/1', u'/v1/MOM-Id_Entity/2', u'/v1/MOM-Id_Entity/3']

    >>> r2 = r1 [0]
    >>> sorted (r2._attrs.iteritems ())
    [(u'first_name', u'christian'), (u'last_name', u'tanzer'), (u'middle_name', u''), (u'title', u'')]

    >>> r2c = CC.get (r2._url)
    >>> r2c._result.url
    u'http://localhost:9999/v1/MOM-Id_Entity/1'
    >>> r2r = CR.get (r2._url)
    >>> r2r._result.url
    u'http://localhost:9999/v1/MOM-Id_Entity/1?raw=True'
    >>> sorted (r2r._attrs.iteritems ())
    [(u'first_name', u'Christian'), (u'last_name', u'Tanzer'), (u'middle_name', u''), (u'title', u'')]

    >>> r2r._changed_p
    False
    >>> r2r.title = "Mag."
    >>> r2r._changed_p
    True

    >>> sorted (r2r._attrs.iteritems ())
    [(u'first_name', u'Christian'), (u'last_name', u'Tanzer'), (u'middle_name', u''), (u'title', u'Mag.')]
    >>> sorted (r2r._attrs_orig.iteritems ())
    [(u'first_name', u'Christian'), (u'last_name', u'Tanzer'), (u'middle_name', u''), (u'title', u'')]

    >>> r2r_p = r2r.PUT ()
    >>> r2r_p._result.url
    u'http://localhost:9999/v1/MOM-Id_Entity/1?raw=True'


    >>> server.terminate ()

"""

_test_cqf = r"""
    >>> server = Scaffold (["wsgi"] + server_args + ["-db_url", %(p1)s, "-db_name", %(n1)s or ("test." + %(bn1)s)]) # doctest:+ELLIPSIS
    ...
    >>> root   = Scaffold.root
    >>> v1     = root.resource_from_href ("v1")
    >>> pids   = root.resource_from_href ("v1/pid")

    >>> v1
    <Scope v1: /v1>
    >>> pids
    <E_Type MOM-Id_Entity: /v1/MOM-Id_Entity>

    >>> for e in v1.entries :
    ...     print ("%%s\n    %%s" %% (e.name, e.change_query_filters))
    MOM-Id_Entity
        ()
    MOM-Link
        (Q.type_name.in_ (['PAP.Address_Position', 'PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Company_has_Url', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'PAP.Person_has_Url', 'SRM.Boat', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team', 'SRM.Team_has_Boat_in_Regatta', 'SWP.Clip_O', 'SWP.Picture'],),)
    MOM-Link1
        (Q.type_name.in_ (['PAP.Address_Position', 'SRM.Boat', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team', 'SWP.Clip_O', 'SWP.Picture'],),)
    MOM-Link2
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Company_has_Url', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'PAP.Person_has_Url', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    MOM-Object
        (Q.type_name.in_ (['PAP.Address', 'PAP.Company', 'PAP.Email', 'PAP.Person', 'PAP.Phone', 'PAP.Url', 'SRM.Boat_Class', 'SRM.Club', 'SRM.Handicap', 'SRM.Page', 'SRM.Regatta_Event', 'SWP.Gallery', 'SWP.Page'],),)
    MOM-_MOM_Link_n_
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Company_has_Url', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'PAP.Person_has_Url', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    PAP-Address
        (Q.type_name == PAP.Address,)
    PAP-Address_Position
        (Q.type_name == PAP.Address_Position,)
    PAP-Company
        (Q.type_name == PAP.Company,)
    PAP-Company_has_Address
        (Q.type_name == PAP.Company_has_Address,)
    PAP-Company_has_Email
        (Q.type_name == PAP.Company_has_Email,)
    PAP-Company_has_Phone
        (Q.type_name == PAP.Company_has_Phone,)
    PAP-Company_has_Url
        (Q.type_name == PAP.Company_has_Url,)
    PAP-Email
        (Q.type_name == PAP.Email,)
    PAP-Link1
        (Q.type_name.in_ (['PAP.Address_Position'],),)
    PAP-Link2
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Company_has_Url', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'PAP.Person_has_Url'],),)
    PAP-Object
        (Q.type_name.in_ (['PAP.Address', 'PAP.Company', 'PAP.Email', 'PAP.Person', 'PAP.Phone', 'PAP.Url'],),)
    PAP-Person
        (Q.type_name == PAP.Person,)
    PAP-Person_has_Address
        (Q.type_name == PAP.Person_has_Address,)
    PAP-Person_has_Email
        (Q.type_name == PAP.Person_has_Email,)
    PAP-Person_has_Phone
        (Q.type_name == PAP.Person_has_Phone,)
    PAP-Person_has_Url
        (Q.type_name == PAP.Person_has_Url,)
    PAP-Phone
        (Q.type_name == PAP.Phone,)
    PAP-Property
        (Q.type_name.in_ (['PAP.Address', 'PAP.Email', 'PAP.Phone', 'PAP.Url'],),)
    PAP-Subject
        (Q.type_name.in_ (['PAP.Company', 'PAP.Person'],),)
    PAP-Subject_has_Address
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Person_has_Address'],),)
    PAP-Subject_has_Email
        (Q.type_name.in_ (['PAP.Company_has_Email', 'PAP.Person_has_Email'],),)
    PAP-Subject_has_Phone
        (Q.type_name.in_ (['PAP.Company_has_Phone', 'PAP.Person_has_Phone'],),)
    PAP-Subject_has_Property
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Company_has_Url', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'PAP.Person_has_Url'],),)
    PAP-Subject_has_Url
        (Q.type_name.in_ (['PAP.Company_has_Url', 'PAP.Person_has_Url'],),)
    PAP-Url
        (Q.type_name == PAP.Url,)
    SRM-Boat
        (Q.type_name == SRM.Boat,)
    SRM-Boat_Class
        (Q.type_name == SRM.Boat_Class,)
    SRM-Boat_in_Regatta
        (Q.type_name == SRM.Boat_in_Regatta,)
    SRM-Club
        (Q.type_name == SRM.Club,)
    SRM-Crew_Member
        (Q.type_name == SRM.Crew_Member,)
    SRM-Handicap
        (Q.type_name == SRM.Handicap,)
    SRM-Link1
        (Q.type_name.in_ (['SRM.Boat', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team'],),)
    SRM-Link2
        (Q.type_name.in_ (['SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    SRM-Object
        (Q.type_name.in_ (['SRM.Boat_Class', 'SRM.Club', 'SRM.Handicap', 'SRM.Page', 'SRM.Regatta_Event'],),)
    SRM-Page
        (Q.type_name == SRM.Page,)
    SRM-Race_Result
        (Q.type_name == SRM.Race_Result,)
    SRM-Regatta
        (Q.type_name.in_ (['SRM.Regatta_C', 'SRM.Regatta_H'],),)
    SRM-Regatta_C
        (Q.type_name == SRM.Regatta_C,)
    SRM-Regatta_Event
        (Q.type_name == SRM.Regatta_Event,)
    SRM-Regatta_H
        (Q.type_name == SRM.Regatta_H,)
    SRM-Sailor
        (Q.type_name == SRM.Sailor,)
    SRM-Team
        (Q.type_name == SRM.Team,)
    SRM-Team_has_Boat_in_Regatta
        (Q.type_name == SRM.Team_has_Boat_in_Regatta,)
    SRM-_Boat_Class_
        (Q.type_name.in_ (['SRM.Boat_Class', 'SRM.Handicap'],),)
    SWP-Clip_O
        (Q.type_name == SWP.Clip_O,)
    SWP-Clip_X
        (Q.type_name == SWP.Clip_X,)
    SWP-Gallery
        (Q.type_name == SWP.Gallery,)
    SWP-Link1
        (Q.type_name.in_ (['SWP.Clip_O', 'SWP.Picture'],),)
    SWP-Object
        (Q.type_name.in_ (['SWP.Gallery', 'SWP.Page'],),)
    SWP-Object_PN
        (Q.type_name.in_ (['SWP.Gallery', 'SWP.Page'],),)
    SWP-Page
        (Q.type_name == SWP.Page,)
    SWP-Page_Y
        (Q.type_name == SWP.Page_Y,)
    SWP-Picture
        (Q.type_name == SWP.Picture,)

    >>> for e in v1.entries :
    ...     print ("%%s    %%s" %% (e.name, e.attributes))
    MOM-Id_Entity    ()
    MOM-Link    (Left `left`,)
    MOM-Link1    (Left `left`,)
    MOM-Link2    (Left `left`, Right `right`)
    MOM-Object    ()
    MOM-_MOM_Link_n_    (Left `left`, Right `right`)
    PAP-Address    (String `street`, String `zip`, String `city`, String `country`, String `desc`, String `region`)
    PAP-Address_Position    (Address `left`, Position `position`)
    PAP-Company    (String `name`, Date_Interval `lifetime`, String `short_name`)
    PAP-Company_has_Address    (Company `left`, Address `right`, String `desc`)
    PAP-Company_has_Email    (Company `left`, Email `right`, String `desc`)
    PAP-Company_has_Phone    (Company `left`, Phone `right`, Numeric_String `extension`, String `desc`)
    PAP-Company_has_Url    (Company `left`, Url `right`, String `desc`)
    PAP-Email    (Email `address`, String `desc`)
    PAP-Link1    (Left `left`,)
    PAP-Link2    (Left `left`, Right `right`)
    PAP-Object    ()
    PAP-Person    (String `last_name`, String `first_name`, String `middle_name`, String `title`, Date_Interval `lifetime`, String `salutation`, Sex `sex`)
    PAP-Person_has_Address    (Person `left`, Address `right`, String `desc`)
    PAP-Person_has_Email    (Person `left`, Email `right`, String `desc`)
    PAP-Person_has_Phone    (Person `left`, Phone `right`, Numeric_String `extension`, String `desc`)
    PAP-Person_has_Url    (Person `left`, Url `right`, String `desc`)
    PAP-Phone    (Numeric_String `country_code`, Numeric_String `area_code`, Numeric_String `number`, String `desc`)
    PAP-Property    (String `desc`,)
    PAP-Subject    (Date_Interval `lifetime`,)
    PAP-Subject_has_Address    (Subject `left`, Address `right`, String `desc`)
    PAP-Subject_has_Email    (Subject `left`, Email `right`, String `desc`)
    PAP-Subject_has_Phone    (Subject `left`, Phone `right`, Numeric_String `extension`, String `desc`)
    PAP-Subject_has_Property    (Subject `left`, Property `right`, String `desc`)
    PAP-Subject_has_Url    (Subject `left`, Url `right`, String `desc`)
    PAP-Url    (Url `value`, String `desc`)
    SRM-Boat    (Boat_Class `left`, Nation `nation`, Int `sail_number`, String `sail_number_x`, String `name`)
    SRM-Boat_Class    (String `name`, Int `max_crew`, Float `beam`, Float `loa`, Float `sail_area`)
    SRM-Boat_in_Regatta    (Boat `left`, Regatta `right`, Entity `skipper`, Int `place`, Int `points`)
    SRM-Club    (String `name`, String `long_name`)
    SRM-Crew_Member    (Boat_in_Regatta `left`, Sailor `right`, Int `key`, String `role`)
    SRM-Handicap    (String `name`,)
    SRM-Link1    (Left `left`,)
    SRM-Link2    (Left `left`, Right `right`)
    SRM-Object    ()
    SRM-Page    (Date-Slug `perma_name`, Entity `event`, Text `text`, Date_Interval `date`, Format `format`, String `head_line`, Boolean `hidden`, Int `prio`, String `desc`)
    SRM-Race_Result    (Boat_in_Regatta `left`, Int `race`, Int `points`, String `status`, Boolean `discarded`)
    SRM-Regatta    (Regatta_Event `left`, Entity `boat_class`, Int `discards`, Boolean `is_cancelled`, String `kind`, Int `races`, Regatta_Result `result`)
    SRM-Regatta_C    (Regatta_Event `left`, Entity `boat_class`, Int `discards`, Boolean `is_cancelled`, String `kind`, Int `races`, Regatta_Result `result`, Boolean `is_team_race`)
    SRM-Regatta_Event    (String `name`, Date_Interval `date`, Entity `club`, String `desc`, Boolean `is_cancelled`)
    SRM-Regatta_H    (Regatta_Event `left`, Entity `boat_class`, Int `discards`, Boolean `is_cancelled`, String `kind`, Int `races`, Regatta_Result `result`)
    SRM-Sailor    (Person `left`, Nation `nation`, Int `mna_number`, Entity `club`)
    SRM-Team    (Regatta_C `left`, String `name`, Entity `club`, String `desc`, Entity `leader`, Int `place`)
    SRM-Team_has_Boat_in_Regatta    (Team `left`, Boat_in_Regatta `right`)
    SRM-_Boat_Class_    (String `name`,)
    SWP-Clip_O    (Object_PN `left`, Date_Interval `date_x`, Text `abstract`, Int `prio`)
    SWP-Clip_X    (Date-Slug `perma_name`, Text `text`, Date_Interval `date`, String `short_title`, Format `format`, String `head_line`, Boolean `hidden`, Int `prio`, Url `link_to`, String `title`)
    SWP-Gallery    (Date-Slug `perma_name`, Date_Interval `date`, String `short_title`, String `title`, Directory `directory`)
    SWP-Link1    (Left `left`,)
    SWP-Object    ()
    SWP-Object_PN    (Date-Slug `perma_name`, Date_Interval `date`, String `short_title`, String `title`)
    SWP-Page    (Date-Slug `perma_name`, Text `text`, Date_Interval `date`, String `short_title`, String `title`, Format `format`, String `head_line`, Boolean `hidden`, Int `prio`)
    SWP-Page_Y    (Date-Slug `perma_name`, Int `year`, Text `text`, Date_Interval `date`, String `short_title`, String `title`, Format `format`, String `head_line`, Boolean `hidden`, Int `prio`)
    SWP-Picture    (Gallery `left`, Int `number`, String `name`, Picture `photo`, Thumbnail `thumb`)

    >>> print (root.href_pat_frag)
    v1(?:/(?:SWP\-Picture|SWP\-Page\_Y|SWP\-Page|SWP\-Object\_PN|SWP\-Object|SWP\-Link1|SWP\-Gallery|SWP\-Clip\_X|SWP\-Clip\_O|SRM\-\_Boat\_Class\_|SRM\-Team\_has\_Boat\_in\_Regatta|SRM\-Team|SRM\-Sailor|SRM\-Regatta\_H|SRM\-Regatta\_Event|SRM\-Regatta\_C|SRM\-Regatta|SRM\-Race\_Result|SRM\-Page|SRM\-Object|SRM\-Link2|SRM\-Link1|SRM\-Handicap|SRM\-Crew\_Member|SRM\-Club|SRM\-Boat\_in\_Regatta|SRM\-Boat\_Class|SRM\-Boat|PAP\-Url|PAP\-Subject\_has\_Url|PAP\-Subject\_has\_Property|PAP\-Subject\_has\_Phone|PAP\-Subject\_has\_Email|PAP\-Subject\_has\_Address|PAP\-Subject|PAP\-Property|PAP\-Phone|PAP\-Person\_has\_Url|PAP\-Person\_has\_Phone|PAP\-Person\_has\_Email|PAP\-Person\_has\_Address|PAP\-Person|PAP\-Object|PAP\-Link2|PAP\-Link1|PAP\-Email|PAP\-Company\_has\_Url|PAP\-Company\_has\_Phone|PAP\-Company\_has\_Email|PAP\-Company\_has\_Address|PAP\-Company|PAP\-Address\_Position|PAP\-Address|MOM\-\_MOM\_Link\_n\_|MOM\-Object|MOM\-Link2|MOM\-Link1|MOM\-Link|MOM\-Id\_Entity))?|Doc

    >>> for o in sorted (pids.objects, key = Q.pid) :
    ...     e = pids._new_entry (o.pid)
    ...     print ("%%s %%r\n    %%s" %% (e.E_Type.type_name, o.ui_display, e.change_query_filters))
    PAP.Person u'Tanzer Christian'
        (Q.pid == 1,)
    PAP.Person u'Tanzer Laurens William'
        (Q.pid == 2,)
    PAP.Person u'Tanzer Clarissa Anna'
        (Q.pid == 3,)
    SRM.Sailor u'Tanzer Christian, AUT, 29676'
        (Q.pid.in_ ((4, 1),),)
    SRM.Sailor u'Tanzer Laurens William, AUT'
        (Q.pid.in_ ((5, 2),),)
    SRM.Sailor u'Tanzer Clarissa Anna, AUT'
        (Q.pid.in_ ((6, 3),),)
    SRM.Boat_Class u'Optimist'
        (Q.pid == 7,)
    SRM.Boat u'Optimist, AUT 1107'
        (Q.pid.in_ ((8, 7),),)
    SRM.Handicap u'Yardstick'
        (Q.pid == 9,)
    SRM.Regatta_Event u'Himmelfahrt 2008/05/01'
        (Q.pid == 10,)
    SRM.Regatta_C u'Himmelfahrt 2008/05/01, Optimist'
        (Q.pid.in_ ((11, 10, 7),),)
    SRM.Regatta_H u'Himmelfahrt 2008/05/01, Yardstick'
        (Q.pid.in_ ((12, 10, 9),),)
    SRM.Regatta_Event u'Guggenberger 2008/06/20 - 2008/06/21'
        (Q.pid == 13,)
    SRM.Regatta_C u'Guggenberger 2008/06/20 - 2008/06/21, Optimist'
        (Q.pid.in_ ((14, 13, 7),),)
    SRM.Boat_in_Regatta u'Optimist, AUT 1107, Himmelfahrt 2008/05/01, Optimist'
        (Q.pid.in_ ((15, 8, 11, 5),),)
    SRM.Boat_in_Regatta u'Optimist, AUT 1107, Guggenberger 2008/06/20 - 2008/06/21, Optimist'
        (Q.pid.in_ ((16, 8, 14, 5),),)

"""

_test_delete = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (R.get ("/v1/pid?brief")) ### 1
    { 'json' :
        { 'entries' :
            [ 1
            , 2
            , 3
            , 4
            , 5
            , 6
            , 7
            , 8
            , 9
            , 10
            , 11
            , 12
            , 13
            , 14
            , 15
            , 16
            ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?brief'
    }

    >>> _ = show (R.get ("/v1/pid/1"))  ### 2
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'christian'
            , 'last_name' : 'tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (R.delete ("/v1/pid/1")) ### 3
    { 'json' :
        { 'attributes_raw' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'error' : "You need to send the object's `cid` with the request"
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (R.delete ("/v1/pid/1", params = dict (cid = 2))) ### 4
    { 'json' :
        { 'attributes_raw' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'error' : 'Cid mismatch: requested cid = 2, current cid = 1'
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 409
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=2'
    }

    >>> _ = show (R.get ("/v1/pid?count")) ### 5
    { 'json' :
        { 'count' : 16 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (R.delete ("/v1/pid/1", params = dict (cid = 1))) ### 6
    { 'json' :
        { 'attributes_raw' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'status' : 'Object with pid 1 successfully deleted'
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=1'
    }

    >>> _ = show (R.get ("/v1/pid?count")) ### 7
    { 'json' :
        { 'count' : 14 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (R.delete ("/v1/pid/1", params = dict (cid = 1))) ### 8 #doctest: +ELLIPSIS
    { 'json' :
        { 'description' : 'Gone'
        , 'info' : 'It was deleted by user `anonymous` on ...'
        , 'message' : "Id_Entity `1` doesn't exist anymore!"
        }
    , 'status' : 410
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=1'
    }

    >>> _ = show (R.get ("/v1/pid/1")) ### 9 #doctest: +ELLIPSIS
    { 'json' :
        { 'description' : 'Gone'
        , 'info' : 'It was deleted by user `anonymous` on ...'
        , 'message' : "Id_Entity `1` doesn't exist anymore!"
        }
    , 'status' : 410
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (R.get ("/v1/pid?brief")) ### 10
    { 'json' :
        { 'entries' :
            [ 2
            , 3
            , 5
            , 6
            , 7
            , 8
            , 9
            , 10
            , 11
            , 12
            , 13
            , 14
            , 15
            , 16
            ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?brief'
    }

    >>> server.terminate ()

"""

_test_doc = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (R.get ("/Doc?brief"))
    { 'json' :
        { 'entries' :
            [ 'MOM-Id_Entity'
            , 'MOM-Link'
            , 'MOM-Link1'
            , 'MOM-Link2'
            , 'MOM-Link2_Ordered'
            , 'MOM-Link3'
            , 'MOM-Named_Object'
            , 'MOM-Object'
            , 'MOM-_MOM_Link_n_'
            , 'PAP-Address'
            , 'PAP-Address_Position'
            , 'PAP-Company'
            , 'PAP-Company_has_Address'
            , 'PAP-Company_has_Email'
            , 'PAP-Company_has_Phone'
            , 'PAP-Company_has_Url'
            , 'PAP-Email'
            , 'PAP-Id_Entity'
            , 'PAP-Link1'
            , 'PAP-Link2'
            , 'PAP-Link2_Ordered'
            , 'PAP-Link3'
            , 'PAP-Named_Object'
            , 'PAP-Object'
            , 'PAP-Person'
            , 'PAP-Person_has_Address'
            , 'PAP-Person_has_Email'
            , 'PAP-Person_has_Phone'
            , 'PAP-Person_has_Url'
            , 'PAP-Phone'
            , 'PAP-Property'
            , 'PAP-Subject'
            , 'PAP-Subject_has_Address'
            , 'PAP-Subject_has_Email'
            , 'PAP-Subject_has_Phone'
            , 'PAP-Subject_has_Property'
            , 'PAP-Subject_has_Url'
            , 'PAP-Url'
            , 'SRM-Boat'
            , 'SRM-Boat_Class'
            , 'SRM-Boat_in_Regatta'
            , 'SRM-Club'
            , 'SRM-Crew_Member'
            , 'SRM-Handicap'
            , 'SRM-Id_Entity'
            , 'SRM-Link1'
            , 'SRM-Link2'
            , 'SRM-Link2_Ordered'
            , 'SRM-Link3'
            , 'SRM-Named_Object'
            , 'SRM-Object'
            , 'SRM-Page'
            , 'SRM-Race_Result'
            , 'SRM-Regatta'
            , 'SRM-Regatta_C'
            , 'SRM-Regatta_Event'
            , 'SRM-Regatta_H'
            , 'SRM-Sailor'
            , 'SRM-Team'
            , 'SRM-Team_has_Boat_in_Regatta'
            , 'SRM-_Boat_Class_'
            , 'SWP-Clip_O'
            , 'SWP-Clip_X'
            , 'SWP-Gallery'
            , 'SWP-Id_Entity'
            , 'SWP-Link1'
            , 'SWP-Link2'
            , 'SWP-Link2_Ordered'
            , 'SWP-Link3'
            , 'SWP-Named_Object'
            , 'SWP-Object'
            , 'SWP-Object_PN'
            , 'SWP-Page'
            , 'SWP-Page_Y'
            , 'SWP-Picture'
            ]
        , 'url_template' : '/Doc/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc?brief'
    }

    >>> _ = show (R.get ("/Doc/SRM-Boat_in_Regatta"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : 'Boat racing in a regatta.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Boat'
              , 'role_name' : 'boat'
              , 'type' : 'Boat'
              , 'type_name' : 'SRM.Boat'
              , 'ui_name' : 'Boat'
              , 'url' : '/Doc/SRM-Boat'
              }
            , { 'default_value' : ''
              , 'description' : 'Regatta a boat races in.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'right'
              , 'p_type' : 'Regatta'
              , 'role_name' : 'regatta'
              , 'type' : 'Regatta'
              , 'type_name' : 'SRM.Regatta'
              , 'ui_name' : 'Regatta'
              , 'url' : '/Doc/SRM-Regatta'
              }
            , { 'default_value' : ''
              , 'description' : 'Skipper of boat.'
              , 'is_required' : True
              , 'kind' : 'required'
              , 'name' : 'skipper'
              , 'p_type' : 'Sailor'
              , 'type' : 'Entity'
              , 'type_name' : 'SRM.Sailor'
              , 'ui_name' : 'Skipper'
              , 'url' : '/Doc/SRM-Sailor'
              }
            , { 'default_value' : ''
              , 'description' : 'Place of boat in this regatta.'
              , 'example' : 2
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'place'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Place'
              }
            , { 'default_value' : ''
              , 'description' : 'Total points of boat in this regatta.'
              , 'example' : 25
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'points'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Points'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'SRM.Crew_Member'
              , 'url' : '/Doc/SRM-Crew_Member'
              }
            , { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'SRM.Race_Result'
              , 'url' : '/Doc/SRM-Race_Result'
              }
            , { 'attributes' :
    [ 'right' ]
              , 'type_name' : 'SRM.Team_has_Boat_in_Regatta'
              , 'url' : '/Doc/SRM-Team_has_Boat_in_Regatta'
              }
            ]
        , 'description' : 'Boat racing in a regatta.'
        , 'is_partial' : False
        , 'parents' :
            [ { 'type_name' : 'SRM.Link2'
              , 'url' : '/Doc/SRM-Link2'
              }
            ]
        , 'type_name' : 'SRM.Boat_in_Regatta'
        , 'ui_name' : 'SRM.Boat_in_Regatta'
        , 'url' : '/Doc/SRM-Boat_in_Regatta'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Boat_in_Regatta'
    }

    >>> _ = show (R.get ("/Doc/SRM-Regatta"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : 'Regatta event to which this regatta belongs.'
              , 'is_changeable' : False
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Regatta_Event'
              , 'role_name' : 'event'
              , 'type' : 'Regatta_Event'
              , 'type_name' : 'SRM.Regatta_Event'
              , 'ui_name' : 'Event'
              , 'url' : '/Doc/SRM-Regatta_Event'
              }
            , { 'default_value' : ''
              , 'description' : 'Class of boats sailing in this regatta.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'boat_class'
              , 'p_type' : '_Boat_Class_'
              , 'type' : 'Entity'
              , 'type_name' : 'SRM._Boat_Class_'
              , 'ui_name' : 'Boat class'
              , 'url' : '/Doc/SRM-_Boat_Class_'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of discardable races in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'discards'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Discards'
              }
            , { 'default_value' : ''
              , 'description' : 'Indicates that the regatta is cancelled'
              , 'example' : 'no'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'is_cancelled'
              , 'p_type' : 'bool'
              , 'syntax' : 'The following string values are accepted as valid Boolean values: no, yes'
              , 'type' : 'Boolean'
              , 'ui_name' : 'Is cancelled'
              }
            , { 'default_value' : ''
              , 'description' : 'Kind of regatta.'
              , 'example' : 'One race, one beer'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'max_length' : 32
              , 'name' : 'kind'
              , 'p_type' : 'unicode'
              , 'type' : 'String'
              , 'ui_name' : 'Kind'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of races sailed in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'races'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Races'
              }
            , { 'attributes' :
                  [ { 'default_value' : ''
                    , 'description' : 'Date of regatta result.'
                    , 'example' : '1979/08/18'
                    , 'is_required' : False
                    , 'kind' : 'necessary'
                    , 'name' : 'date'
                    , 'p_type' : 'datetime'
                    , 'type' : 'Date-Time'
                    , 'ui_name' : 'Date'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Name of software used for managing the regatta.'
                    , 'example' : 'Blowing Bits Inc.'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'software'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Software'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Status of result (e.g., `preliminary` or `final`).'
                    , 'example' : 'Final'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'status'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Status'
                    }
                  ]
              , 'default_value' : ''
              , 'description' : 'Information about result.'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'result'
              , 'p_type' : 'Regatta_Result'
              , 'type' : 'Regatta_Result'
              , 'type_name' : 'SRM.Regatta_Result'
              , 'ui_name' : 'Result'
              }
            ]
        , 'children' :
            [ { 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/Doc/SRM-Regatta_C'
              }
            , { 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/Doc/SRM-Regatta_H'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'right' ]
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/Doc/SRM-Boat_in_Regatta'
              }
            ]
        , 'description' : 'Sailing regatta for one class or handicap.'
        , 'is_partial' : True
        , 'parents' :
            [ { 'type_name' : 'SRM.Link1'
              , 'url' : '/Doc/SRM-Link1'
              }
            ]
        , 'type_name' : 'SRM.Regatta'
        , 'ui_name' : 'SRM.Regatta'
        , 'url' : '/Doc/SRM-Regatta'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Regatta'
    }

    >>> _ = show (R.get ("/Doc/SRM-Regatta_C"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : 'Regatta event to which this regatta belongs.'
              , 'is_changeable' : False
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Regatta_Event'
              , 'role_name' : 'event'
              , 'type' : 'Regatta_Event'
              , 'type_name' : 'SRM.Regatta_Event'
              , 'ui_name' : 'Event'
              , 'url' : '/Doc/SRM-Regatta_Event'
              }
            , { 'default_value' : ''
              , 'description' : 'Class of boats sailing in this regatta.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'boat_class'
              , 'p_type' : 'Boat_Class'
              , 'type' : 'Entity'
              , 'type_name' : 'SRM.Boat_Class'
              , 'ui_name' : 'Boat class'
              , 'url' : '/Doc/SRM-Boat_Class'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of discardable races in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'discards'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Discards'
              }
            , { 'default_value' : ''
              , 'description' : 'Indicates that the regatta is cancelled'
              , 'example' : 'no'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'is_cancelled'
              , 'p_type' : 'bool'
              , 'syntax' : 'The following string values are accepted as valid Boolean values: no, yes'
              , 'type' : 'Boolean'
              , 'ui_name' : 'Is cancelled'
              }
            , { 'default_value' : ''
              , 'description' : 'Kind of regatta.'
              , 'example' : 'One race, one beer'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'max_length' : 32
              , 'name' : 'kind'
              , 'p_type' : 'unicode'
              , 'type' : 'String'
              , 'ui_name' : 'Kind'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of races sailed in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'races'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Races'
              }
            , { 'attributes' :
                  [ { 'default_value' : ''
                    , 'description' : 'Date of regatta result.'
                    , 'example' : '1979/08/18'
                    , 'is_required' : False
                    , 'kind' : 'necessary'
                    , 'name' : 'date'
                    , 'p_type' : 'datetime'
                    , 'type' : 'Date-Time'
                    , 'ui_name' : 'Date'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Name of software used for managing the regatta.'
                    , 'example' : 'Blowing Bits Inc.'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'software'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Software'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Status of result (e.g., `preliminary` or `final`).'
                    , 'example' : 'Final'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'status'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Status'
                    }
                  ]
              , 'default_value' : ''
              , 'description' : 'Information about result.'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'result'
              , 'p_type' : 'Regatta_Result'
              , 'type' : 'Regatta_Result'
              , 'type_name' : 'SRM.Regatta_Result'
              , 'ui_name' : 'Result'
              }
            , { 'default_value' : 'no'
              , 'description' : 'Boolean attribute.'
              , 'example' : 'no'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'is_team_race'
              , 'p_type' : 'bool'
              , 'syntax' : 'The following string values are accepted as valid Boolean values: no, yes'
              , 'type' : 'Boolean'
              , 'ui_name' : 'Is team race'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'right' ]
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/Doc/SRM-Boat_in_Regatta'
              }
            , { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'SRM.Team'
              , 'url' : '/Doc/SRM-Team'
              }
            ]
        , 'description' : 'Regatta for a single class of sail boats.'
        , 'is_partial' : False
        , 'parents' :
            [ { 'type_name' : 'SRM.Regatta'
              , 'url' : '/Doc/SRM-Regatta'
              }
            ]
        , 'relevant_root' :
            { 'type_name' : 'SRM.Regatta'
            , 'url' : '/Doc/SRM-Regatta'
            }
        , 'type_name' : 'SRM.Regatta_C'
        , 'ui_name' : 'SRM.Regatta_C'
        , 'url' : '/Doc/SRM-Regatta_C'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Regatta_C'
    }

    >>> _ = show (R.get ("/Doc/SRM-Regatta_H"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : 'Regatta event to which this regatta belongs.'
              , 'is_changeable' : False
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Regatta_Event'
              , 'role_name' : 'event'
              , 'type' : 'Regatta_Event'
              , 'type_name' : 'SRM.Regatta_Event'
              , 'ui_name' : 'Event'
              , 'url' : '/Doc/SRM-Regatta_Event'
              }
            , { 'default_value' : ''
              , 'description' : 'Name of handicap system used for this regatta.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'boat_class'
              , 'p_type' : 'Handicap'
              , 'type' : 'Entity'
              , 'type_name' : 'SRM.Handicap'
              , 'ui_name' : 'Handicap'
              , 'url' : '/Doc/SRM-Handicap'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of discardable races in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'discards'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Discards'
              }
            , { 'default_value' : ''
              , 'description' : 'Indicates that the regatta is cancelled'
              , 'example' : 'no'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'is_cancelled'
              , 'p_type' : 'bool'
              , 'syntax' : 'The following string values are accepted as valid Boolean values: no, yes'
              , 'type' : 'Boolean'
              , 'ui_name' : 'Is cancelled'
              }
            , { 'default_value' : ''
              , 'description' : 'Kind of regatta.'
              , 'example' : 'One race, one beer'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'max_length' : 32
              , 'name' : 'kind'
              , 'p_type' : 'unicode'
              , 'type' : 'String'
              , 'ui_name' : 'Kind'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of races sailed in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'races'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Races'
              }
            , { 'attributes' :
                  [ { 'default_value' : ''
                    , 'description' : 'Date of regatta result.'
                    , 'example' : '1979/08/18'
                    , 'is_required' : False
                    , 'kind' : 'necessary'
                    , 'name' : 'date'
                    , 'p_type' : 'datetime'
                    , 'type' : 'Date-Time'
                    , 'ui_name' : 'Date'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Name of software used for managing the regatta.'
                    , 'example' : 'Blowing Bits Inc.'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'software'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Software'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Status of result (e.g., `preliminary` or `final`).'
                    , 'example' : 'Final'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'status'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Status'
                    }
                  ]
              , 'default_value' : ''
              , 'description' : 'Information about result.'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'result'
              , 'p_type' : 'Regatta_Result'
              , 'type' : 'Regatta_Result'
              , 'type_name' : 'SRM.Regatta_Result'
              , 'ui_name' : 'Result'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'right' ]
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/Doc/SRM-Boat_in_Regatta'
              }
            ]
        , 'description' : 'Regatta for boats in a handicap system.'
        , 'is_partial' : False
        , 'parents' :
            [ { 'type_name' : 'SRM.Regatta'
              , 'url' : '/Doc/SRM-Regatta'
              }
            ]
        , 'relevant_root' :
            { 'type_name' : 'SRM.Regatta'
            , 'url' : '/Doc/SRM-Regatta'
            }
        , 'type_name' : 'SRM.Regatta_H'
        , 'ui_name' : 'SRM.Regatta_H'
        , 'url' : '/Doc/SRM-Regatta_H'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Regatta_H'
    }

    >>> _ = show (R.get ("/Doc/SRM-Crew_Member"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : '`Boat_in_Regatta` the crew member sails on.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Boat_in_Regatta'
              , 'role_name' : 'boat_in_regatta'
              , 'type' : 'Boat_in_Regatta'
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'ui_name' : 'Boat in regatta'
              , 'url' : '/Doc/SRM-Boat_in_Regatta'
              }
            , { 'default_value' : ''
              , 'description' : 'Person which sails as crew member on `boat_in_regatta`'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'right'
              , 'p_type' : 'Sailor'
              , 'role_name' : 'sailor'
              , 'type' : 'Sailor'
              , 'type_name' : 'SRM.Sailor'
              , 'ui_name' : 'Sailor'
              , 'url' : '/Doc/SRM-Sailor'
              }
            , { 'default_value' : '0'
              , 'description' : 'The crew members of a boat will be sorted by `key`, if\ndefined, by order of creation otherwise.'
              , 'example' : 7
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'key'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Key'
              }
            , { 'default_value' : ''
              , 'description' : 'Role of crew member.'
              , 'example' : 'trimmer'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'max_length' : 32
              , 'name' : 'role'
              , 'p_type' : 'unicode'
              , 'type' : 'String'
              , 'ui_name' : 'Role'
              }
            ]
        , 'description' : 'Crew member of a `Boat_in_Regatta`.'
        , 'is_partial' : False
        , 'parents' :
            [ { 'type_name' : 'SRM.Link2'
              , 'url' : '/Doc/SRM-Link2'
              }
            ]
        , 'type_name' : 'SRM.Crew_Member'
        , 'ui_name' : 'SRM.Crew_Member'
        , 'url' : '/Doc/SRM-Crew_Member'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Crew_Member'
    }

    >>> server.terminate ()

"""

_test_example_1 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> print ("Count before loop:", scope.MOM.Id_Entity.count)
    Count before loop: 16

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np) :
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')
    PAP.Address_Position : ((u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), (('height', u'1764.0'), ('lat', u'42'), ('lon', u'137')), 'PAP.Address_Position')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Company_has_Phone')
    PAP.Company_has_Url : ((u'John Doe, Inc.', 'PAP.Company'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Company_has_Url')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Person_has_Address')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Person_has_Email')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Person_has_Phone')
    PAP.Person_has_Url : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Person_has_Url')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    PAP.Url : (u'http://xkcd.com/327/', 'PAP.Url')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat_in_Regatta : (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Crew_Member : ------
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Race_Result : ((((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'43', 'SRM.Race_Result')
    SRM.Regatta_C : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C')
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_H : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'IRC', 'SRM.Handicap'), 'SRM.Regatta_H')
    SRM.Sailor : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'AUT', u'499999.5', (u'RORC', 'SRM.Club'), 'SRM.Sailor')
    SRM.Team : (((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team')
    SRM.Team_has_Boat_in_Regatta : ((((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team'), (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), 'SRM.Team_has_Boat_in_Regatta')
    SWP.Clip_O : ((u'20101010_000042_137', 'SWP.Page'), (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SWP.Clip_O')
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')

    >>> print ("Count after loop:", scope.MOM.Id_Entity.count)
    Count after loop: 16

"""

_test_example_2 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np) : ### nummero 2
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')
    PAP.Address_Position : ((u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), (('height', u'1764.0'), ('lat', u'42'), ('lon', u'137')), 'PAP.Address_Position')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Company_has_Phone')
    PAP.Company_has_Url : ((u'John Doe, Inc.', 'PAP.Company'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Company_has_Url')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Person_has_Address')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Person_has_Email')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Person_has_Phone')
    PAP.Person_has_Url : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Person_has_Url')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    PAP.Url : (u'http://xkcd.com/327/', 'PAP.Url')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat_in_Regatta : (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Crew_Member : ------
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Race_Result : ((((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'43', 'SRM.Race_Result')
    SRM.Regatta_C : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C')
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_H : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'IRC', 'SRM.Handicap'), 'SRM.Regatta_H')
    SRM.Sailor : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'AUT', u'499999.5', (u'RORC', 'SRM.Club'), 'SRM.Sailor')
    SRM.Team : (((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team')
    SRM.Team_has_Boat_in_Regatta : ((((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team'), (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), 'SRM.Team_has_Boat_in_Regatta')
    SWP.Clip_O : ((u'20101010_000042_137', 'SWP.Page'), (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SWP.Clip_O')
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')


"""

_test_example_3 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np, reverse = True) :
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Clip_O : ((u'20101010_000042_137', 'SWP.Page'), (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SWP.Clip_O')
    SRM.Team_has_Boat_in_Regatta : ((((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team'), (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), 'SRM.Team_has_Boat_in_Regatta')
    SRM.Team : (((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team')
    SRM.Sailor : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'AUT', u'499999.5', (u'RORC', 'SRM.Club'), 'SRM.Sailor')
    SRM.Regatta_H : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'IRC', 'SRM.Handicap'), 'SRM.Regatta_H')
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_C : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C')
    SRM.Race_Result : ((((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'43', 'SRM.Race_Result')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Crew_Member : ------
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Boat_in_Regatta : (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    PAP.Url : (u'http://xkcd.com/327/', 'PAP.Url')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    PAP.Person_has_Url : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Person_has_Url')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Person_has_Phone')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Person_has_Email')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Person_has_Address')
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Company_has_Url : ((u'John Doe, Inc.', 'PAP.Company'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Company_has_Url')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Company_has_Phone')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Address_Position : ((u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), (('height', u'1764.0'), ('lat', u'42'), ('lon', u'137')), 'PAP.Address_Position')
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')


"""

_test_example_4 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> print ("Count before loop:", scope.MOM.Id_Entity.count)
    Count before loop: 16

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np) : ### nummero 1
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')
    PAP.Address_Position : ((u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), (('height', u'1764.0'), ('lat', u'42'), ('lon', u'137')), 'PAP.Address_Position')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Company_has_Phone')
    PAP.Company_has_Url : ((u'John Doe, Inc.', 'PAP.Company'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Company_has_Url')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Person_has_Address')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Person_has_Email')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Person_has_Phone')
    PAP.Person_has_Url : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Person_has_Url')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    PAP.Url : (u'http://xkcd.com/327/', 'PAP.Url')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat_in_Regatta : (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Crew_Member : ------
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Race_Result : ((((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'43', 'SRM.Race_Result')
    SRM.Regatta_C : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C')
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_H : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'IRC', 'SRM.Handicap'), 'SRM.Regatta_H')
    SRM.Sailor : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'AUT', u'499999.5', (u'RORC', 'SRM.Club'), 'SRM.Sailor')
    SRM.Team : (((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team')
    SRM.Team_has_Boat_in_Regatta : ((((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team'), (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), 'SRM.Team_has_Boat_in_Regatta')
    SWP.Clip_O : ((u'20101010_000042_137', 'SWP.Page'), (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SWP.Clip_O')
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')

    >>> scope.destroy ()

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np) : ### nummero 2
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')
    PAP.Address_Position : ((u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), (('height', u'1764.0'), ('lat', u'42'), ('lon', u'137')), 'PAP.Address_Position')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Company_has_Phone')
    PAP.Company_has_Url : ((u'John Doe, Inc.', 'PAP.Company'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Company_has_Url')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Person_has_Address')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Person_has_Email')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Person_has_Phone')
    PAP.Person_has_Url : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Person_has_Url')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    PAP.Url : (u'http://xkcd.com/327/', 'PAP.Url')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat_in_Regatta : (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Crew_Member : ------
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Race_Result : ((((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'43', 'SRM.Race_Result')
    SRM.Regatta_C : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C')
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_H : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'IRC', 'SRM.Handicap'), 'SRM.Regatta_H')
    SRM.Sailor : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'AUT', u'499999.5', (u'RORC', 'SRM.Club'), 'SRM.Sailor')
    SRM.Team : (((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team')
    SRM.Team_has_Boat_in_Regatta : ((((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team'), (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), 'SRM.Team_has_Boat_in_Regatta')
    SWP.Clip_O : ((u'20101010_000042_137', 'SWP.Page'), (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SWP.Clip_O')
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')

    >>> scope.destroy ()

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np, reverse = True) : ### nummero 3
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Clip_O : ((u'20101010_000042_137', 'SWP.Page'), (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SWP.Clip_O')
    SRM.Team_has_Boat_in_Regatta : ((((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team'), (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), 'SRM.Team_has_Boat_in_Regatta')
    SRM.Team : (((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team')
    SRM.Sailor : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'AUT', u'499999.5', (u'RORC', 'SRM.Club'), 'SRM.Sailor')
    SRM.Regatta_H : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'IRC', 'SRM.Handicap'), 'SRM.Regatta_H')
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_C : ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C')
    SRM.Race_Result : ((((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'43', 'SRM.Race_Result')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Crew_Member : ------
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Boat_in_Regatta : (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    PAP.Url : (u'http://xkcd.com/327/', 'PAP.Url')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    PAP.Person_has_Url : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Person_has_Url')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Person_has_Phone')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Person_has_Email')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Person_has_Address')
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Company_has_Url : ((u'John Doe, Inc.', 'PAP.Company'), (u'http://xkcd.com/327/', 'PAP.Url'), 'PAP.Company_has_Url')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Company_has_Phone')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Address_Position : ((u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), (('height', u'1764.0'), ('lat', u'42'), ('lon', u'137')), 'PAP.Address_Position')
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')


"""

_test_get = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> r = showf (R.options (""))
    { 'headers' :
        { 'allow' : 'GET, HEAD, OPTIONS'
        , 'content-length' : '0'
        , 'content-type' : 'text/plain; charset=utf-8'
        , 'date' : '<datetime instance>'
        , 'server' : '<server>'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = showf (R.head (""))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'content-length' : '0'
        , 'content-type' : 'text/plain; charset=utf-8'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'server' : '<server>'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = show (R.get (""))
    { 'json' :
        { 'entries' :
            [ '/v1'
            , '/Doc'
            , '/RAISE'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = show (R.get ("?brief"))
    { 'json' :
        { 'entries' :
            [ 'v1'
            , 'Doc'
            , 'RAISE'
            ]
        , 'url_template' : '/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/?brief'
    }

    >>> r = show (R.get ("?verbose"))
    { 'json' :
        { 'entries' :
            [ '/v1'
            , '/Doc'
            , '/RAISE'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/?verbose'
    }

    >>> r = show (R.get ("/v0"))
    { 'json' :
        { 'description' : 'Not found' }
    , 'status' : 404
    , 'url' : 'http://localhost:9999/v0'
    }

    >>> r = show (R.get ("/v1?brief"))
    { 'json' :
        { 'entries' :
            [ 'MOM-Id_Entity'
            , 'MOM-Link'
            , 'MOM-Link1'
            , 'MOM-Link2'
            , 'MOM-Object'
            , 'MOM-_MOM_Link_n_'
            , 'PAP-Address'
            , 'PAP-Address_Position'
            , 'PAP-Company'
            , 'PAP-Company_has_Address'
            , 'PAP-Company_has_Email'
            , 'PAP-Company_has_Phone'
            , 'PAP-Company_has_Url'
            , 'PAP-Email'
            , 'PAP-Link1'
            , 'PAP-Link2'
            , 'PAP-Object'
            , 'PAP-Person'
            , 'PAP-Person_has_Address'
            , 'PAP-Person_has_Email'
            , 'PAP-Person_has_Phone'
            , 'PAP-Person_has_Url'
            , 'PAP-Phone'
            , 'PAP-Property'
            , 'PAP-Subject'
            , 'PAP-Subject_has_Address'
            , 'PAP-Subject_has_Email'
            , 'PAP-Subject_has_Phone'
            , 'PAP-Subject_has_Property'
            , 'PAP-Subject_has_Url'
            , 'PAP-Url'
            , 'SRM-Boat'
            , 'SRM-Boat_Class'
            , 'SRM-Boat_in_Regatta'
            , 'SRM-Club'
            , 'SRM-Crew_Member'
            , 'SRM-Handicap'
            , 'SRM-Link1'
            , 'SRM-Link2'
            , 'SRM-Object'
            , 'SRM-Page'
            , 'SRM-Race_Result'
            , 'SRM-Regatta'
            , 'SRM-Regatta_C'
            , 'SRM-Regatta_Event'
            , 'SRM-Regatta_H'
            , 'SRM-Sailor'
            , 'SRM-Team'
            , 'SRM-Team_has_Boat_in_Regatta'
            , 'SRM-_Boat_Class_'
            , 'SWP-Clip_O'
            , 'SWP-Clip_X'
            , 'SWP-Gallery'
            , 'SWP-Link1'
            , 'SWP-Object'
            , 'SWP-Object_PN'
            , 'SWP-Page'
            , 'SWP-Page_Y'
            , 'SWP-Picture'
            ]
        , 'url_template' : '/v1/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1?brief'
    }

    >>> r = show (R.get ("/v1"))
    { 'json' :
        { 'entries' :
            [ '/v1/MOM-Id_Entity'
            , '/v1/MOM-Link'
            , '/v1/MOM-Link1'
            , '/v1/MOM-Link2'
            , '/v1/MOM-Object'
            , '/v1/MOM-_MOM_Link_n_'
            , '/v1/PAP-Address'
            , '/v1/PAP-Address_Position'
            , '/v1/PAP-Company'
            , '/v1/PAP-Company_has_Address'
            , '/v1/PAP-Company_has_Email'
            , '/v1/PAP-Company_has_Phone'
            , '/v1/PAP-Company_has_Url'
            , '/v1/PAP-Email'
            , '/v1/PAP-Link1'
            , '/v1/PAP-Link2'
            , '/v1/PAP-Object'
            , '/v1/PAP-Person'
            , '/v1/PAP-Person_has_Address'
            , '/v1/PAP-Person_has_Email'
            , '/v1/PAP-Person_has_Phone'
            , '/v1/PAP-Person_has_Url'
            , '/v1/PAP-Phone'
            , '/v1/PAP-Property'
            , '/v1/PAP-Subject'
            , '/v1/PAP-Subject_has_Address'
            , '/v1/PAP-Subject_has_Email'
            , '/v1/PAP-Subject_has_Phone'
            , '/v1/PAP-Subject_has_Property'
            , '/v1/PAP-Subject_has_Url'
            , '/v1/PAP-Url'
            , '/v1/SRM-Boat'
            , '/v1/SRM-Boat_Class'
            , '/v1/SRM-Boat_in_Regatta'
            , '/v1/SRM-Club'
            , '/v1/SRM-Crew_Member'
            , '/v1/SRM-Handicap'
            , '/v1/SRM-Link1'
            , '/v1/SRM-Link2'
            , '/v1/SRM-Object'
            , '/v1/SRM-Page'
            , '/v1/SRM-Race_Result'
            , '/v1/SRM-Regatta'
            , '/v1/SRM-Regatta_C'
            , '/v1/SRM-Regatta_Event'
            , '/v1/SRM-Regatta_H'
            , '/v1/SRM-Sailor'
            , '/v1/SRM-Team'
            , '/v1/SRM-Team_has_Boat_in_Regatta'
            , '/v1/SRM-_Boat_Class_'
            , '/v1/SWP-Clip_O'
            , '/v1/SWP-Clip_X'
            , '/v1/SWP-Gallery'
            , '/v1/SWP-Link1'
            , '/v1/SWP-Object'
            , '/v1/SWP-Object_PN'
            , '/v1/SWP-Page'
            , '/v1/SWP-Page_Y'
            , '/v1/SWP-Picture'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1'
    }

    >>> rp = show (R.get ("/v1/PAP-Person"))
    { 'json' :
        { 'entries' :
            [ '/v1/PAP-Person/1'
            , '/v1/PAP-Person/2'
            , '/v1/PAP-Person/3'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> _ = show (R.get ("/v1/PAP-Person?verbose&raw"))
    { 'json' :
        { 'attribute_names' :
            [ 'last_name'
            , 'first_name'
            , 'middle_name'
            , 'title'
            , 'lifetime.start'
            , 'lifetime.finish'
            , 'salutation'
            , 'sex'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'first_name' : 'Christian'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : ''
                  , 'title' : ''
                  }
              , 'cid' : 1
              , 'pid' : 1
              , 'type_name' : 'PAP.Person'
              , 'url' : '/v1/PAP-Person/1'
              }
            , { 'attributes_raw' :
                  { 'first_name' : 'Laurens'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : 'William'
                  , 'title' : ''
                  }
              , 'cid' : 2
              , 'pid' : 2
              , 'type_name' : 'PAP.Person'
              , 'url' : '/v1/PAP-Person/2'
              }
            , { 'attributes_raw' :
                  { 'first_name' : 'Clarissa'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : 'Anna'
                  , 'title' : ''
                  }
              , 'cid' : 3
              , 'pid' : 3
              , 'type_name' : 'PAP.Person'
              , 'url' : '/v1/PAP-Person/3'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person?verbose&raw'
    }

    >>> _ = show (R.get ("/v1/PAP-Person.csv?verbose&raw"))
    { 'content' :
        [ 'last_name,first_name,middle_name,title,lifetime.start,lifetime.finish,salutation,sex'
        , 'Tanzer,Christian,,,,,,'
        , 'Tanzer,Laurens,William,,,,,'
        , 'Tanzer,Clarissa,Anna,,,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person.csv?verbose&raw'
    }

    >>> _ = show (R.get ("/v1/PAP-Person.csv"))
    { 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person.csv'
    }

    >>> rp_json = req_json (rp)
    >>> for e in rp_json ["entries"] :
    ...     _ = show (requests.get ("http://localhost:9999" + e))
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'christian'
            , 'last_name' : 'tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'laurens'
            , 'last_name' : 'tanzer'
            , 'middle_name' : 'william'
            , 'title' : ''
            }
        , 'cid' : 2
        , 'pid' : 2
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/2'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/2'
    }
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'clarissa'
            , 'last_name' : 'tanzer'
            , 'middle_name' : 'anna'
            , 'title' : ''
            }
        , 'cid' : 3
        , 'pid' : 3
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/3'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/3'
    }

    >>> r = show (R.head ("/v1/PAP-Person/1"))
    { 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }

    >>> r = showf (R.get ("/v1/PAP-Person/1"))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'link' : '/Doc/PAP-Person; rel=doc'
        , 'server' : '<server>'
        , 'x-last-cid' : '1'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'christian'
            , 'last_name' : 'tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }

    >>> last_modified = r.headers ["last-modified"]
    >>> last_etag     = r.headers ["etag"]
    >>> r = showf (R.get ("/v1/PAP-Person/1", headers = { "If-Modified-Since" : last_modified }))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'connection' : 'close'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'link' : '/Doc/PAP-Person; rel=doc'
        , 'server' : '<server>'
        , 'x-last-cid' : '1'
        }
    , 'status' : 304
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }

    >>> r = showf (R.get ("/v1/PAP-Person/1", headers = { "If-None-Match" : last_etag }))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'connection' : 'close'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'link' : '/Doc/PAP-Person; rel=doc'
        , 'server' : '<server>'
        , 'x-last-cid' : '1'
        }
    , 'status' : 304
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }

    >>> r = show (R.get ("/v1/SRM-Regatta?brief"))
    { 'json' :
        { 'entries' :
            [ 11
            , 12
            , 14
            ]
        , 'url_template' : '/v1/SRM-Regatta/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?brief'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&closure&ckd"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'max_crew' : 1
                          , 'name' : 'optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : False
                  , 'left' :
                      { 'attributes' :
                          { 'date' :
                              { 'finish' : '2008-05-01'
                              , 'start' : '2008-05-01'
                              }
                          , 'name' : 'himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'name' : 'yardstick' }
                      , 'cid' : 9
                      , 'pid' : 9
                      , 'type_name' : 'SRM.Handicap'
                      , 'url' : '/v1/SRM-Handicap/9'
                      }
                  , 'is_cancelled' : False
                  , 'left' :
                      { 'attributes' :
                          { 'date' :
                              { 'finish' : '2008-05-01'
                              , 'start' : '2008-05-01'
                              }
                          , 'name' : 'himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/SRM-Regatta/12'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'max_crew' : 1
                          , 'name' : 'optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : False
                  , 'left' :
                      { 'attributes' :
                          { 'date' :
                              { 'finish' : '2008-06-21'
                              , 'start' : '2008-06-20'
                              }
                          , 'name' : 'guggenberger'
                          }
                      , 'cid' : 13
                      , 'pid' : 13
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/13'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/14'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&closure&ckd'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&raw&closure"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'name' : 'Yardstick' }
                      , 'cid' : 9
                      , 'pid' : 9
                      , 'type_name' : 'SRM.Handicap'
                      , 'url' : '/v1/SRM-Handicap/9'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/SRM-Regatta/12'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/06/21'
                              , 'start' : '2008/06/20'
                              }
                          , 'name' : 'Guggenberger'
                          }
                      , 'cid' : 13
                      , 'pid' : 13
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/13'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/14'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&raw&closure'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&raw"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'boat_class' :
                      { 'pid' : 7
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'pid' : 10
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'pid' : 9
                      , 'url' : '/v1/SRM-Handicap/9'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'pid' : 10
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/SRM-Regatta/12'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'pid' : 7
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'pid' : 13
                      , 'url' : '/v1/SRM-Regatta_Event/13'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/14'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&raw'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta.csv?verbose&raw&brief"))
    { 'content' :
        [ 'left,boat_class,discards,is_cancelled,kind,races,result.date,result.software,result.status'
        , '10,7,,no,,,,,'
        , '10,9,,no,,,,,'
        , '13,7,,no,,,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta.csv?verbose&raw&brief'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta.csv?verbose&raw"))
    { 'content' :
        [ 'left.pid,left.url,boat_class.pid,boat_class.url,discards,is_cancelled,kind,races,result.date,result.software,result.status'
        , '10,/v1/SRM-Regatta_Event/10,7,/v1/SRM-Boat_Class/7,,no,,,,,'
        , '10,/v1/SRM-Regatta_Event/10,9,/v1/SRM-Handicap/9,,no,,,,,'
        , '13,/v1/SRM-Regatta_Event/13,7,/v1/SRM-Boat_Class/7,,no,,,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta.csv?verbose&raw'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta.csv?verbose&raw&brief&fields=left,boat_class,is_cancelled"))
    { 'content' :
        [ 'left,boat_class,is_cancelled'
        , '10,7,no'
        , '10,9,no'
        , '13,7,no'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta.csv?verbose&raw&brief&fields=left,boat_class,is_cancelled'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&raw&closure"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'name' : 'Yardstick' }
                      , 'cid' : 9
                      , 'pid' : 9
                      , 'type_name' : 'SRM.Handicap'
                      , 'url' : '/v1/SRM-Handicap/9'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/SRM-Regatta/12'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/06/21'
                              , 'start' : '2008/06/20'
                              }
                          , 'name' : 'Guggenberger'
                          }
                      , 'cid' : 13
                      , 'pid' : 13
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/13'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/14'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&raw&closure'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&raw&closure&AQ=boat_class,EQ,9"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'name' : 'Yardstick' }
                      , 'cid' : 9
                      , 'pid' : 9
                      , 'type_name' : 'SRM.Handicap'
                      , 'url' : '/v1/SRM-Handicap/9'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/SRM-Regatta/12'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&raw&closure&AQ=boat_class,EQ,9'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&raw&closure&AQ=boat_class,EQ,7"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/06/21'
                              , 'start' : '2008/06/20'
                              }
                          , 'name' : 'Guggenberger'
                          }
                      , 'cid' : 13
                      , 'pid' : 13
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/13'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/14'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&raw&closure&AQ=boat_class,EQ,7'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&raw&closure&AQ=boat_class,EQ,7&AQ=left,EQ,13"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/06/21'
                              , 'start' : '2008/06/20'
                              }
                          , 'name' : 'Guggenberger'
                          }
                      , 'cid' : 13
                      , 'pid' : 13
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/13'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/14'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&raw&closure&AQ=boat_class,EQ,7&AQ=left,EQ,13'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&raw&closure&AQ=boat_class,EQ,7&AQ=left,EQ,10"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&raw&closure&AQ=boat_class,EQ,7&AQ=left,EQ,10'
    }
    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&raw&closure&AQ=left,EQ,10"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'boat_class.pid'
            , 'boat_class.url'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result.date'
            , 'result.software'
            , 'result.status'
            ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'name' : 'Yardstick' }
                      , 'cid' : 9
                      , 'pid' : 9
                      , 'type_name' : 'SRM.Handicap'
                      , 'url' : '/v1/SRM-Handicap/9'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/SRM-Regatta/12'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&raw&closure&AQ=left,EQ,10'
    }

    >>> r = show (R.get ("/v1/SRM-Regatta_C?brief"))
    { 'json' :
        { 'entries' :
            [ 11
            , 14
            ]
        , 'url_template' : '/v1/SRM-Regatta_C/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta_C?brief'
    }

    >>> r = show (R.get ("/v1/SRM-Regatta_H?brief"))
    { 'json' :
        { 'entries' : [ 12 ]
        , 'url_template' : '/v1/SRM-Regatta_H/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta_H?brief'
    }

    >>> r = show (R.get ("/v1/MOM-Object?verbose&raw"))
    { 'json' :
        { 'attribute_names' :
            []
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'first_name' : 'Christian'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : ''
                  , 'title' : ''
                  }
              , 'cid' : 1
              , 'pid' : 1
              , 'type_name' : 'PAP.Person'
              , 'url' : '/v1/MOM-Object/1'
              }
            , { 'attributes_raw' :
                  { 'first_name' : 'Laurens'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : 'William'
                  , 'title' : ''
                  }
              , 'cid' : 2
              , 'pid' : 2
              , 'type_name' : 'PAP.Person'
              , 'url' : '/v1/MOM-Object/2'
              }
            , { 'attributes_raw' :
                  { 'first_name' : 'Clarissa'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : 'Anna'
                  , 'title' : ''
                  }
              , 'cid' : 3
              , 'pid' : 3
              , 'type_name' : 'PAP.Person'
              , 'url' : '/v1/MOM-Object/3'
              }
            , { 'attributes_raw' :
                  { 'max_crew' : '1'
                  , 'name' : 'Optimist'
                  }
              , 'cid' : 7
              , 'pid' : 7
              , 'type_name' : 'SRM.Boat_Class'
              , 'url' : '/v1/MOM-Object/7'
              }
            , { 'attributes_raw' :
                  { 'name' : 'Yardstick' }
              , 'cid' : 9
              , 'pid' : 9
              , 'type_name' : 'SRM.Handicap'
              , 'url' : '/v1/MOM-Object/9'
              }
            , { 'attributes_raw' :
                  { 'date' :
                      { 'finish' : '2008/05/01'
                      , 'start' : '2008/05/01'
                      }
                  , 'name' : 'Himmelfahrt'
                  }
              , 'cid' : 10
              , 'pid' : 10
              , 'type_name' : 'SRM.Regatta_Event'
              , 'url' : '/v1/MOM-Object/10'
              }
            , { 'attributes_raw' :
                  { 'date' :
                      { 'finish' : '2008/06/21'
                      , 'start' : '2008/06/20'
                      }
                  , 'name' : 'Guggenberger'
                  }
              , 'cid' : 13
              , 'pid' : 13
              , 'type_name' : 'SRM.Regatta_Event'
              , 'url' : '/v1/MOM-Object/13'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/MOM-Object?verbose&raw'
    }

    >>> r = show (R.get ("/v1/MOM-Link?verbose&raw"))
    { 'json' :
        { 'attribute_names' :
    [ 'left' ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'club' : None
                  , 'left' :
                      { 'pid' : 1
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  , 'mna_number' : '29676'
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 4
              , 'pid' : 4
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/4'
              }
            , { 'attributes_raw' :
                  { 'club' : None
                  , 'left' :
                      { 'pid' : 2
                      , 'url' : '/v1/PAP-Person/2'
                      }
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 5
              , 'pid' : 5
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/5'
              }
            , { 'attributes_raw' :
                  { 'club' : None
                  , 'left' :
                      { 'pid' : 3
                      , 'url' : '/v1/PAP-Person/3'
                      }
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 6
              , 'pid' : 6
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/6'
              }
            , { 'attributes_raw' :
                  { 'left' :
                      { 'pid' : 7
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'nation' : 'AUT'
                  , 'sail_number' : '1107'
                  , 'sail_number_x' : ''
                  }
              , 'cid' : 8
              , 'pid' : 8
              , 'type_name' : 'SRM.Boat'
              , 'url' : '/v1/MOM-Link/8'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'pid' : 7
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'pid' : 10
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/MOM-Link/11'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'pid' : 9
                      , 'url' : '/v1/SRM-Handicap/9'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'pid' : 10
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/MOM-Link/12'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'pid' : 7
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'pid' : 13
                      , 'url' : '/v1/SRM-Regatta_Event/13'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/MOM-Link/14'
              }
            , { 'attributes_raw' :
                  { 'left' :
                      { 'pid' : 8
                      , 'url' : '/v1/SRM-Boat/8'
                      }
                  , 'right' :
                      { 'pid' : 11
                      , 'url' : '/v1/SRM-Regatta_C/11'
                      }
                  , 'skipper' :
                      { 'pid' : 5
                      , 'url' : '/v1/SRM-Sailor/5'
                      }
                  }
              , 'cid' : 15
              , 'pid' : 15
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/v1/MOM-Link/15'
              }
            , { 'attributes_raw' :
                  { 'left' :
                      { 'pid' : 8
                      , 'url' : '/v1/SRM-Boat/8'
                      }
                  , 'right' :
                      { 'pid' : 14
                      , 'url' : '/v1/SRM-Regatta_C/14'
                      }
                  , 'skipper' :
                      { 'pid' : 5
                      , 'url' : '/v1/SRM-Sailor/5'
                      }
                  }
              , 'cid' : 16
              , 'pid' : 16
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/v1/MOM-Link/16'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/MOM-Link?verbose&raw'
    }

    >>> r = show (R.get ("/v1/MOM-Link?verbose&raw&closure"))
    { 'json' :
        { 'attribute_names' :
    [ 'left' ]
        , 'entries' :
            [ { 'attributes_raw' :
                  { 'club' : None
                  , 'left' :
                      { 'attributes_raw' :
                          { 'first_name' : 'Christian'
                          , 'last_name' : 'Tanzer'
                          , 'middle_name' : ''
                          , 'title' : ''
                          }
                      , 'cid' : 1
                      , 'pid' : 1
                      , 'type_name' : 'PAP.Person'
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  , 'mna_number' : '29676'
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 4
              , 'pid' : 4
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/4'
              }
            , { 'attributes_raw' :
                  { 'club' : None
                  , 'left' :
                      { 'attributes_raw' :
                          { 'first_name' : 'Laurens'
                          , 'last_name' : 'Tanzer'
                          , 'middle_name' : 'William'
                          , 'title' : ''
                          }
                      , 'cid' : 2
                      , 'pid' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'url' : '/v1/PAP-Person/2'
                      }
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 5
              , 'pid' : 5
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/5'
              }
            , { 'attributes_raw' :
                  { 'club' : None
                  , 'left' :
                      { 'attributes_raw' :
                          { 'first_name' : 'Clarissa'
                          , 'last_name' : 'Tanzer'
                          , 'middle_name' : 'Anna'
                          , 'title' : ''
                          }
                      , 'cid' : 3
                      , 'pid' : 3
                      , 'type_name' : 'PAP.Person'
                      , 'url' : '/v1/PAP-Person/3'
                      }
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 6
              , 'pid' : 6
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/6'
              }
            , { 'attributes_raw' :
                  { 'left' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'nation' : 'AUT'
                  , 'sail_number' : '1107'
                  , 'sail_number_x' : ''
                  }
              , 'cid' : 8
              , 'pid' : 8
              , 'type_name' : 'SRM.Boat'
              , 'url' : '/v1/MOM-Link/8'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/MOM-Link/11'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'name' : 'Yardstick' }
                      , 'cid' : 9
                      , 'pid' : 9
                      , 'type_name' : 'SRM.Handicap'
                      , 'url' : '/v1/SRM-Handicap/9'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/05/01'
                              , 'start' : '2008/05/01'
                              }
                          , 'name' : 'Himmelfahrt'
                          }
                      , 'cid' : 10
                      , 'pid' : 10
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/10'
                      }
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/MOM-Link/12'
              }
            , { 'attributes_raw' :
                  { 'boat_class' :
                      { 'attributes_raw' :
                          { 'max_crew' : '1'
                          , 'name' : 'Optimist'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      , 'url' : '/v1/SRM-Boat_Class/7'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes_raw' :
                          { 'date' :
                              { 'finish' : '2008/06/21'
                              , 'start' : '2008/06/20'
                              }
                          , 'name' : 'Guggenberger'
                          }
                      , 'cid' : 13
                      , 'pid' : 13
                      , 'type_name' : 'SRM.Regatta_Event'
                      , 'url' : '/v1/SRM-Regatta_Event/13'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/MOM-Link/14'
              }
            , { 'attributes_raw' :
                  { 'left' :
                      { 'attributes_raw' :
                          { 'left' :
                              { 'attributes_raw' :
                                  { 'max_crew' : '1'
                                  , 'name' : 'Optimist'
                                  }
                              , 'cid' : 7
                              , 'pid' : 7
                              , 'type_name' : 'SRM.Boat_Class'
                              , 'url' : '/v1/SRM-Boat_Class/7'
                              }
                          , 'nation' : 'AUT'
                          , 'sail_number' : '1107'
                          , 'sail_number_x' : ''
                          }
                      , 'cid' : 8
                      , 'pid' : 8
                      , 'type_name' : 'SRM.Boat'
                      , 'url' : '/v1/SRM-Boat/8'
                      }
                  , 'right' :
                      { 'attributes_raw' :
                          { 'boat_class' :
                              { 'pid' : 7
                              , 'url' : '/v1/SRM-Boat_Class/7'
                              }
                          , 'is_cancelled' : 'no'
                          , 'left' :
                              { 'attributes_raw' :
                                  { 'date' :
                                      { 'finish' : '2008/05/01'
                                      , 'start' : '2008/05/01'
                                      }
                                  , 'name' : 'Himmelfahrt'
                                  }
                              , 'cid' : 10
                              , 'pid' : 10
                              , 'type_name' : 'SRM.Regatta_Event'
                              , 'url' : '/v1/SRM-Regatta_Event/10'
                              }
                          }
                      , 'cid' : 11
                      , 'pid' : 11
                      , 'type_name' : 'SRM.Regatta_C'
                      , 'url' : '/v1/SRM-Regatta_C/11'
                      }
                  , 'skipper' :
                      { 'attributes_raw' :
                          { 'club' : None
                          , 'left' :
                              { 'attributes_raw' :
                                  { 'first_name' : 'Laurens'
                                  , 'last_name' : 'Tanzer'
                                  , 'middle_name' : 'William'
                                  , 'title' : ''
                                  }
                              , 'cid' : 2
                              , 'pid' : 2
                              , 'type_name' : 'PAP.Person'
                              , 'url' : '/v1/PAP-Person/2'
                              }
                          , 'mna_number' : ''
                          , 'nation' : 'AUT'
                          }
                      , 'cid' : 5
                      , 'pid' : 5
                      , 'type_name' : 'SRM.Sailor'
                      , 'url' : '/v1/SRM-Sailor/5'
                      }
                  }
              , 'cid' : 15
              , 'pid' : 15
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/v1/MOM-Link/15'
              }
            , { 'attributes_raw' :
                  { 'left' :
                      { 'attributes_raw' :
                          { 'left' :
                              { 'attributes_raw' :
                                  { 'max_crew' : '1'
                                  , 'name' : 'Optimist'
                                  }
                              , 'cid' : 7
                              , 'pid' : 7
                              , 'type_name' : 'SRM.Boat_Class'
                              , 'url' : '/v1/SRM-Boat_Class/7'
                              }
                          , 'nation' : 'AUT'
                          , 'sail_number' : '1107'
                          , 'sail_number_x' : ''
                          }
                      , 'cid' : 8
                      , 'pid' : 8
                      , 'type_name' : 'SRM.Boat'
                      , 'url' : '/v1/SRM-Boat/8'
                      }
                  , 'right' :
                      { 'attributes_raw' :
                          { 'boat_class' :
                              { 'pid' : 7
                              , 'url' : '/v1/SRM-Boat_Class/7'
                              }
                          , 'is_cancelled' : 'no'
                          , 'left' :
                              { 'attributes_raw' :
                                  { 'date' :
                                      { 'finish' : '2008/06/21'
                                      , 'start' : '2008/06/20'
                                      }
                                  , 'name' : 'Guggenberger'
                                  }
                              , 'cid' : 13
                              , 'pid' : 13
                              , 'type_name' : 'SRM.Regatta_Event'
                              , 'url' : '/v1/SRM-Regatta_Event/13'
                              }
                          }
                      , 'cid' : 14
                      , 'pid' : 14
                      , 'type_name' : 'SRM.Regatta_C'
                      , 'url' : '/v1/SRM-Regatta_C/14'
                      }
                  , 'skipper' :
                      { 'attributes_raw' :
                          { 'club' : None
                          , 'left' :
                              { 'attributes_raw' :
                                  { 'first_name' : 'Laurens'
                                  , 'last_name' : 'Tanzer'
                                  , 'middle_name' : 'William'
                                  , 'title' : ''
                                  }
                              , 'cid' : 2
                              , 'pid' : 2
                              , 'type_name' : 'PAP.Person'
                              , 'url' : '/v1/PAP-Person/2'
                              }
                          , 'mna_number' : ''
                          , 'nation' : 'AUT'
                          }
                      , 'cid' : 5
                      , 'pid' : 5
                      , 'type_name' : 'SRM.Sailor'
                      , 'url' : '/v1/SRM-Sailor/5'
                      }
                  }
              , 'cid' : 16
              , 'pid' : 16
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/v1/MOM-Link/16'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/MOM-Link?verbose&raw&closure'
    }

    >>> _ = show (R.get ("/v1/pid/"))
    { 'json' :
        { 'entries' :
            [ '/v1/MOM-Id_Entity/1'
            , '/v1/MOM-Id_Entity/2'
            , '/v1/MOM-Id_Entity/3'
            , '/v1/MOM-Id_Entity/4'
            , '/v1/MOM-Id_Entity/5'
            , '/v1/MOM-Id_Entity/6'
            , '/v1/MOM-Id_Entity/7'
            , '/v1/MOM-Id_Entity/8'
            , '/v1/MOM-Id_Entity/9'
            , '/v1/MOM-Id_Entity/10'
            , '/v1/MOM-Id_Entity/11'
            , '/v1/MOM-Id_Entity/12'
            , '/v1/MOM-Id_Entity/13'
            , '/v1/MOM-Id_Entity/14'
            , '/v1/MOM-Id_Entity/15'
            , '/v1/MOM-Id_Entity/16'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/'
    }

    >>> _ = show (R.get ("/v1/pid/1"))
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'christian'
            , 'last_name' : 'tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (R.get ("/v1/pid?count&strict"))
    { 'json' :
        { 'count' : 0 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count&strict'
    }

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 16 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (R.get ("/RAISE"))
    { 'json' :
        { 'description' : 'Internal server error'
        , 'message' : 'Wilful raisement'
          }
    , 'status' : 500
    , 'url' : 'http://localhost:9999/RAISE'
    }

    >>> server.terminate ()

"""

_test_options = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = traverse ("http://localhost:9999/")
    / : GET, HEAD, OPTIONS
    /v1/MOM-Id_Entity/1 : DELETE, GET, HEAD, OPTIONS, PUT
    /v1/PAP-Address : GET, HEAD, OPTIONS, POST

    >>> server.terminate ()

"""

_test_post = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 16 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> snoopy_cargo = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict
    ...         ( last_name   = "Dog"
    ...         , first_name  = "Snoopy"
    ...         , middle_name = "the"
    ...         , lifetime    = dict (start = "20001122")
    ...         )
    ...     )
    ... )
    >>> headers = { "Content-Type": "application/json" }
    >>> _ = show (R.post ("/v1/PAP-Person", headers=headers))
    { 'json' :
        { 'error' : 'You need to send the attributes defining the object with the request in `attributes_raw`(content-type "application/json")' }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> _ = show (R.post ("/v1/PAP-Person", data=snoopy_cargo, headers = {}))
    { 'json' :
        { 'error' : 'You need to send the attributes defining the object with the request in `attributes_raw`(content-type "application/json")' }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> r = showf (R.post ("/v1/PAP-Person", data=snoopy_cargo, headers=headers))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'link' : '/Doc/PAP-Person; rel=doc'
        , 'location' : 'http://localhost:9999/v1/PAP-Person/17'
        , 'server' : '<server>'
        }
    , 'json' :
        { 'attributes_raw' :
            { 'first_name' : 'Snoopy'
            , 'last_name' : 'Dog'
            , 'lifetime' :
                { 'start' : '2000/11/22' }
            , 'middle_name' : 'the'
            , 'title' : ''
            }
        , 'cid' : 17
        , 'pid' : 17
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/17'
        }
    , 'status' : 201
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> cargo_bir = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict
    ...         ( left    = dict
    ...             ( left        = ["Optimist"]
    ...             , nation      = "AUT"
    ...             , sail_number = "1134"
    ...             )
    ...         , right   = 11
    ...         , skipper = dict
    ...             ( club        = dict (name = "SC-AMS")
    ...             , left        = 2
    ...             , nation      = "AUT"
    ...             )
    ...         )
    ...     )
    ... )
    >>> _ = show (R.post ("/v1/SRM-Boat_in_Regatta?verbose&raw&closure", data=cargo_bir))
    { 'json' :
        { 'attributes_raw' :
            { 'left' :
                { 'attributes_raw' :
                    { 'left' :
                        { 'attributes_raw' :
                            { 'max_crew' : '1'
                            , 'name' : 'Optimist'
                            }
                        , 'cid' : 7
                        , 'pid' : 7
                        , 'type_name' : 'SRM.Boat_Class'
                        , 'url' : '/v1/SRM-Boat_Class/7'
                        }
                    , 'nation' : 'AUT'
                    , 'sail_number' : '1134'
                    , 'sail_number_x' : ''
                    }
                , 'cid' : 18
                , 'pid' : 18
                , 'type_name' : 'SRM.Boat'
                , 'url' : '/v1/SRM-Boat/18'
                }
            , 'right' :
                { 'attributes_raw' :
                    { 'boat_class' :
                        { 'pid' : 7
                        , 'url' : '/v1/SRM-Boat_Class/7'
                        }
                    , 'is_cancelled' : 'no'
                    , 'left' :
                        { 'attributes_raw' :
                            { 'date' :
                                { 'finish' : '2008/05/01'
                                , 'start' : '2008/05/01'
                                }
                            , 'name' : 'Himmelfahrt'
                            }
                        , 'cid' : 10
                        , 'pid' : 10
                        , 'type_name' : 'SRM.Regatta_Event'
                        , 'url' : '/v1/SRM-Regatta_Event/10'
                        }
                    }
                , 'cid' : 11
                , 'pid' : 11
                , 'type_name' : 'SRM.Regatta_C'
                , 'url' : '/v1/SRM-Regatta_C/11'
                }
            , 'skipper' :
                { 'attributes_raw' :
                    { 'club' :
                        { 'attributes_raw' :
                            { 'name' : 'SC-AMS' }
                        , 'cid' : 19
                        , 'pid' : 19
                        , 'type_name' : 'SRM.Club'
                        , 'url' : '/v1/SRM-Club/19'
                        }
                    , 'left' :
                        { 'attributes_raw' :
                            { 'first_name' : 'Laurens'
                            , 'last_name' : 'Tanzer'
                            , 'middle_name' : 'William'
                            , 'title' : ''
                            }
                        , 'cid' : 2
                        , 'pid' : 2
                        , 'type_name' : 'PAP.Person'
                        , 'url' : '/v1/PAP-Person/2'
                        }
                    , 'mna_number' : ''
                    , 'nation' : 'AUT'
                    }
                , 'cid' : 20
                , 'pid' : 20
                , 'type_name' : 'SRM.Sailor'
                , 'url' : '/v1/SRM-Sailor/20'
                }
            }
        , 'cid' : 21
        , 'pid' : 21
        , 'type_name' : 'SRM.Boat_in_Regatta'
        , 'url' : '/v1/SRM-Boat_in_Regatta/21'
        }
    , 'status' : 201
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta?verbose&raw&closure'
    }

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 21 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (R.post ("/v1/PAP-Person", data=snoopy_cargo, headers=headers))
    { 'json' :
        { 'error' : "The attribute values for ('last_name', 'first_name', 'middle_name', 'title') must be unique for each object\n  The new definition of Person PAP.Person ('Dog', 'Snoopy', 'the', u'') would clash with 1 existing entities\n  Al
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> cargo_c = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict
    ...         ( last_name   = "Tin"
    ...         , first_name  = "Rin"
    ...         , middle_name = "Tin"
    ...         )
    ...     , cid = req_json (r) ["cid"]
    ...     )
    ... )
    >>> ru = requests.utils.urlparse (r.url)
    >>> p  = "%%s://%%s%%s" %% (ru.scheme, ru.netloc, req_json (r) ["url"])
    >>> s  = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' :
        { 'attributes_raw' :
            { 'first_name' : 'Rin'
            , 'last_name' : 'Tin'
            , 'lifetime' :
                { 'start' : '2000/11/22' }
            , 'middle_name' : 'Tin'
            , 'title' : ''
            }
        , 'cid' : 22
        , 'pid' : 17
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/17'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/17'
    }

    >>> s  = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' :
        { 'error' : 'Cid mismatch: requested cid = 17, current cid = 22' }
    , 'status' : 409
    , 'url' : 'http://localhost:9999/v1/PAP-Person/17'
    }

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 21 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> cargo_g = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict
    ...         ( last_name   = "Garfield"
    ...         , first_name  = "James"
    ...         , hates       = "mondays"
    ...         )
    ...     )
    ... )
    >>> _ = show (R.post ("/v1/PAP-Person", data=cargo_g, headers=headers))
    { 'json' :
        { 'error' : "Request contains invalid attribute names ('hates',)" }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 21 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> server.terminate ()

"""

_test_query = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (R.get ("/v1/pid?brief"))
    { 'json' :
        { 'entries' :
            [ 1
            , 2
            , 3
            , 4
            , 5
            , 6
            , 7
            , 8
            , 9
            , 10
            , 11
            , 12
            , 13
            , 14
            , 15
            , 16
            ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?brief'
    }

    >>> _ = show (R.get ("/v1/pid?order_by=pid&FIRST&limit=1&brief"))
    { 'json' :
        { 'entries' : [ 1 ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?order_by=pid&FIRST&limit=1&brief'
    }

    >>> _ = show (R.get ("/v1/pid?order_by=pid&LAST&limit=1&brief"))
    { 'json' :
        { 'entries' : [ 16 ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?order_by=pid&LAST&limit=1&brief'
    }

    >>> for i in range (10) :
    ...     r = R.get ("/v1/pid?brief&order_by=pid&limit=4&offset=" + str (i))
    ...     print (i, ":", formatted_1 (req_json (r)))
    0 : {'entries' : [1, 2, 3, 4], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    1 : {'entries' : [2, 3, 4, 5], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    2 : {'entries' : [3, 4, 5, 6], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    3 : {'entries' : [4, 5, 6, 7], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    4 : {'entries' : [5, 6, 7, 8], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    5 : {'entries' : [6, 7, 8, 9], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    6 : {'entries' : [7, 8, 9, 10], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    7 : {'entries' : [8, 9, 10, 11], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    8 : {'entries' : [9, 10, 11, 12], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    9 : {'entries' : [10, 11, 12, 13], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}

    >>> r = show (R.get ("/v1/PAP-Person.csv?AQ=middle_name,CONTAINS,a&verbose&raw"))
    { 'content' :
        [ 'last_name,first_name,middle_name,title,lifetime.start,lifetime.finish,salutation,sex'
        , 'Tanzer,Laurens,William,,,,,'
        , 'Tanzer,Clarissa,Anna,,,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person.csv?AQ=middle_name,CONTAINS,a&verbose&raw'
    }

    >>> r = show (R.get ("/v1/PAP-Person.csv?AQ=middle_name,EQ,&verbose&raw"))
    { 'content' :
        [ 'last_name,first_name,middle_name,title,lifetime.start,lifetime.finish,salutation,sex'
        , 'Tanzer,Christian,,,,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person.csv?AQ=middle_name,EQ,&verbose&raw'
    }

    >>> cargo = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict
    ...         ( left        = "Optimist"
    ...         , nation      = "AUT"
    ...         , sail_number = "1134"
    ...         )
    ...     )
    ... )
    >>> _ = show (R.post ("/v1/SRM-Boat?brief", data=cargo))
    { 'json' :
        { 'attributes_raw' :
            { 'left' : 7
            , 'nation' : 'AUT'
            , 'sail_number' : '1134'
            , 'sail_number_x' : ''
            }
        , 'cid' : 17
        , 'pid' : 17
        , 'type_name' : 'SRM.Boat'
        , 'url' : '/v1/SRM-Boat/17'
        }
    , 'status' : 201
    , 'url' : 'http://localhost:9999/v1/SRM-Boat?brief'
    }

    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?verbose&raw&brief"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        , '8,14,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?verbose&raw&brief'
    }

    ### API-style attribute query
    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?AQ=left,EQ,8&verbose&raw&brief"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        , '8,14,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?AQ=left,EQ,8&verbose&raw&brief'
    }

    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?AQ=left,EQ,11&verbose&raw&brief"))
    { 'content' :
    [ 'left,right,skipper,place,points' ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?AQ=left,EQ,11&verbose&raw&brief'
    }

    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?AQ=right,EQ,11&verbose&raw&brief"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?AQ=right,EQ,11&verbose&raw&brief'
    }

    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?AQ=skipper,EQ,5&verbose&raw&brief"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        , '8,14,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?AQ=skipper,EQ,5&verbose&raw&brief'
    }

    ### HTML-form-style attribute query
    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?left___EQ=8&verbose&raw&brief"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        , '8,14,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?left___EQ=8&verbose&raw&brief'
    }

    >>> r = show (R.get ("/v1/MOM-Object?count&AQ=last_name,EQ,tanzer"))
    { 'json' :
        { 'description' : 'Bad request'
        , 'message' : 'Query restriction triggered error: MOM.Object.last_name'
        }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/MOM-Object?count&AQ=last_name,EQ,tanzer'
    }
    >>> r = show (R.get ("/v1/PAP-Person?count&AQ=last_name,EQ,tanzer"))
    { 'json' :
        { 'count' : 3 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person?count&AQ=last_name,EQ,tanzer'
    }

    >>> server.terminate ()

"""

_test_qr_local = """

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> b4  = SRM.Boat ("Optimist", "AUT", "1134", raw = True)
    >>> print (b4.pid, b4)
    17 ((u'optimist', ), u'AUT', 1134, u'')

    >>> SRM.Boat_in_Regatta.AQ.boat
    <left.AQ [Attr.Type.Querier Id_Entity]>
    >>> SRM.Boat_in_Regatta.AQ.boat.EQ
    <Attr.Id_Entity_Equal left.EQ [==]>
    >>> SRM.Boat_in_Regatta.AQ.boat.EQ ("8")
    Q.left == 8

    >>> SRM.Boat_in_Regatta.query_s ().all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', (u'2008/06/20', u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]

    >>> b7 = SRM.Boat.query (sail_number = 1107).one ()
    >>> print (b7.pid, b7)
    8 ((u'optimist', ), u'AUT', 1107, u'')

    >>> SRM.Boat_in_Regatta.query_s (boat = b7).all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', (u'2008/06/20', u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]
    >>> SRM.Boat_in_Regatta.query_s (boat = 8).all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', (u'2008/06/20', u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]
    >>> SRM.Boat_in_Regatta.query_s (boat = "8").all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', (u'2008/06/20', u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]

    >>> SRM.Boat_in_Regatta.query_s (SRM.Boat_in_Regatta.AQ.boat.EQ (8)).all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', (u'2008/06/20', u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]
    >>> SRM.Boat_in_Regatta.query_s (SRM.Boat_in_Regatta.AQ.boat.EQ ("8")).all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', (u'2008/06/20', u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]

    >>> SRM.Boat_in_Regatta.query_s (boat = b4).all ()
    []
    >>> SRM.Boat_in_Regatta.query_s (boat = 17).all ()
    []
    >>> SRM.Boat_in_Regatta.query_s (SRM.Boat_in_Regatta.AQ.boat.EQ ("17")).all ()
    []


"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_client     = _test_client
        , test_cqf        = _test_cqf
        , test_delete     = _test_delete
        , test_doc        = _test_doc
        , test_example_1  = _test_example_1
        , test_example_2  = _test_example_2
        , test_example_3  = _test_example_3
        , test_example_4  = _test_example_4
        , test_get        = _test_get
        , test_options    = _test_options
        , test_post       = _test_post
        , test_query      = _test_query
        , test_qr_local   = _test_qr_local
        )
    )

if __name__ == "__main__" :
    rst_harness._main (Scaffold)
### __END__ GTW.__test__.RST
