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
#    GTW.__test__.Subjects
#
# Purpose
#    Test PAP.Subject subclasses and links
#
# Revision Dates
#    24-Mar-2012 (CT) Creation
#    14-Sep-2012 (CT) Add test for role attributes of `Person_has_Address`
#    20-Sep-2012 (CT) Add tests for `Person_has_Phone`, `Subject_has_Property`
#    21-Sep-2012 (CT) Add test for polymorphic link creation
#     6-Mar-2013 (CT) Add import of `Association`
#     6-Mar-2013 (CT) Adapt to new attribute `Company.registered_in`
#     6-Mar-2013 (CT) Add test for `polymorphic_epk` using `children_trans_iter`
#     8-Mar-2013 (CT) Add subclasses of `Association` to test
#                     `polymorphic_epk` over multiple inheritance levels
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> print (PAP.Subject.count, PAP.Company.count_strict, PAP.Person.count_strict)
    0 0 0

    >>> pg = PAP.Person ("Glueck", "Martin")
    >>> ps = PAP.Person ("Schlatterbeck", "Ralf")
    >>> pt = PAP.Person ("Tanzer", "Christian")
    >>> print (PAP.Subject.count, PAP.Company.count_strict, PAP.Person.count_strict)
    3 0 3

    >>> cl = PAP.Company ("Lucky Software", short_name = "LS")
    >>> co = PAP.Company ("Open Source Consulting", short_name = "OSC")
    >>> print (PAP.Subject.count, PAP.Company.count_strict, PAP.Person.count_strict)
    5 2 3

    >>> PAP.Subject.query_s ().all ()
    [PAP.Person (u'glueck', u'martin', u'', u''), PAP.Company (u'lucky software', u''), PAP.Company (u'open source consulting', u''), PAP.Person (u'schlatterbeck', u'ralf', u'', u''), PAP.Person (u'tanzer', u'christian', u'', u'')]
    >>> PAP.Company.query_s ().all ()
    [PAP.Company (u'lucky software', u''), PAP.Company (u'open source consulting', u'')]
    >>> PAP.Person.query_s ().all ()
    [PAP.Person (u'glueck', u'martin', u'', u''), PAP.Person (u'schlatterbeck', u'ralf', u'', u''), PAP.Person (u'tanzer', u'christian', u'', u'')]

    >>> eg  = PAP.Email ("martin@mangari.org")
    >>> es  = PAP.Email ("ralf@runtux.com")
    >>> et1 = PAP.Email ("tanzer@swing.co.at")
    >>> et2 = PAP.Email ("tanzer@gg32.com")

    >>> _ = PAP.Subject_has_Property (pg, eg)
    >>> _ = PAP.Subject_has_Property (ps, es)
    >>> _ = PAP.Subject_has_Property (pt, et1)
    >>> _ = PAP.Subject_has_Property (pt, et2)

    >>> _ = PAP.Company_has_Email (cl, PAP.Email ("lucky@mangari.org"))
    >>> _ = PAP.Company_has_Email (co, PAP.Email ("office@runtux.com"))

    >>> _ = PAP.Person_has_Phone  (pg, PAP.Phone ("43", "1", "234567", raw = True))
    >>> _ = PAP.Person_has_Phone  (ps, PAP.Phone ("43", "1", "987654", raw = True))
    >>> _ = PAP.Person_has_Phone  (pt, PAP.Phone ("43", "1", "135790", raw = True))
    >>> _ = PAP.Company_has_Phone (co, PAP.Phone ("43", "1", "246802", raw = True), extension = "16", raw = True)

    >>> PAP.Subject_has_Email.query_s ().all ()
    [PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), PAP.Company_has_Email ((u'lucky software', u''), (u'lucky@mangari.org', )), PAP.Company_has_Email ((u'open source consulting', u''), (u'office@runtux.com', )), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]
    >>> PAP.Company_has_Email.query_s ().all ()
    [PAP.Company_has_Email ((u'lucky software', u''), (u'lucky@mangari.org', )), PAP.Company_has_Email ((u'open source consulting', u''), (u'office@runtux.com', ))]
    >>> PAP.Person_has_Email.query_s ().all ()
    [PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> PAP.Subject_has_Email.query_s (Q.right.address.ENDSWITH ("@mangari.org")).all ()
    [PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), PAP.Company_has_Email ((u'lucky software', u''), (u'lucky@mangari.org', ))]
    >>> PAP.Subject_has_Email.query_s (Q.right.address.CONTAINS (".co")).all ()
    [PAP.Company_has_Email ((u'open source consulting', u''), (u'office@runtux.com', )), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]
    >>> PAP.Person_has_Email.query_s (Q.right.address.ENDSWITH ("@mangari.org")).all ()
    [PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', ))]
    >>> PAP.Person_has_Email.query_s (Q.right.address.CONTAINS (".co")).all ()
    [PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> sorted (pg.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'martin@mangari.org')]
    >>> sorted (ps.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'ralf@runtux.com')]
    >>> sorted (pt.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'tanzer@gg32.com'), PAP.Email (u'tanzer@swing.co.at')]

    >>> _ = PAP.Company_has_Email (co, "ralf@runtux.com")

    >>> sorted (cl.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'lucky@mangari.org')]
    >>> sorted (co.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'office@runtux.com'), PAP.Email (u'ralf@runtux.com')]

    >>> rr = PAP.Email.instance ("ralf@runtux.com")
    >>> sorted (rr.persons, key = PAP.Person.sorted_by)
    [PAP.Person (u'schlatterbeck', u'ralf', u'', u'')]
    >>> sorted (rr.companies, key = PAP.Company.sorted_by)
    [PAP.Company (u'open source consulting', u'')]

    >>> PAP.Subject_has_Property.query_s ().all ()
    [PAP.Person_has_Phone ((u'glueck', u'martin', u'', u''), (u'43', u'1', u'234567'), u''), PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), PAP.Company_has_Email ((u'lucky software', u''), (u'lucky@mangari.org', )), PAP.Company_has_Phone ((u'open source consulting', u''), (u'43', u'1', u'246802'), u'16'), PAP.Company_has_Email ((u'open source consulting', u''), (u'office@runtux.com', )), PAP.Company_has_Email ((u'open source consulting', u''), (u'ralf@runtux.com', )), PAP.Person_has_Phone ((u'schlatterbeck', u'ralf', u'', u''), (u'43', u'1', u'987654'), u''), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Phone ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'135790'), u''), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]
    >>> PAP.Subject_has_Property.query_s (left = pt).all ()
    [PAP.Person_has_Phone ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'135790'), u''), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    #>>> PAP.Subject_has_Property.query_s (subject = pt).all ()
    [PAP.Person_has_Phone ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'135790'), u''), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> PAP.Subject_has_Phone.query_s (Q.right.number.CONTAINS ("2")).all ()
    [PAP.Person_has_Phone ((u'glueck', u'martin', u'', u''), (u'43', u'1', u'234567'), u''), PAP.Company_has_Phone ((u'open source consulting', u''), (u'43', u'1', u'246802'), u'16')]

    >>> PAP.Subject_has_Phone.query_s (Q.extension != "").all ()
    [PAP.Company_has_Phone ((u'open source consulting', u''), (u'43', u'1', u'246802'), u'16')]

    >>> def show_emails (ET) :
    ...     attr = ET.emails
    ...     print (attr.attr.__class__, ":", attr.description, "[", attr.Ref_Type.type_name, "]")
    >>> show_emails (PAP.Subject)
    <class '_GTW._OMP._PAP.Subject.emails'> : `Email` linked to `Subject` [ PAP.Subject_has_Email ]

    >>> show_emails (PAP.Company)
    <class '_GTW._OMP._PAP.Company.emails'> : `Email` linked to `Company` [ PAP.Company_has_Email ]

    >>> show_emails (PAP.Person)
    <class '_GTW._OMP._PAP.Person.emails'> : `Email` linked to `Person` [ PAP.Person_has_Email ]

    >>> ET = PAP.Person_has_Address.E_Type
    >>> sorted (ET.role_map)
    ['Address', 'PAP.Address', 'PAP.Person', 'Person', u'address', u'left', u'person', u'right']
    >>> ET.Roles
    (Person `left`, Address `right`)
    >>> ET.edit_attr
    (Person `left`, Address `right`, String `desc`)
    >>> ET.attributes ["left"], ET.attributes ["person"]
    (Person `left`, Person `left`)
    >>> ET.attributes ["right"], ET.attributes ["address"]
    (Address `right`, Address `right`)

    >>> for T, l in children_trans_iter (scope.PAP.Subject_has_Property) :
    ...     rr = T.relevant_root.type_name if T.relevant_root else sorted (T.relevant_roots)
    ...     print ("%%-32s %%-5s %%s" %% ("%%s%%s" %% ("  " * l, T.type_name), T.is_partial, rr))
    PAP.Subject_has_Property         True  PAP.Subject_has_Property
      PAP.Subject_has_Address        True  PAP.Subject_has_Property
        PAP.Company_has_Address      False PAP.Subject_has_Property
        PAP.Person_has_Address       False PAP.Subject_has_Property
        PAP.Association_has_Address  False PAP.Subject_has_Property
      PAP.Subject_has_Email          True  PAP.Subject_has_Property
        PAP.Company_has_Email        False PAP.Subject_has_Property
        PAP.Person_has_Email         False PAP.Subject_has_Property
        PAP.Association_has_Email    False PAP.Subject_has_Property
      PAP.Subject_has_Phone          True  PAP.Subject_has_Property
        PAP.Company_has_Phone        False PAP.Subject_has_Property
        PAP.Person_has_Phone         False PAP.Subject_has_Property
        PAP.Association_has_Phone    False PAP.Subject_has_Property
      PAP.Subject_has_Url            True  PAP.Subject_has_Property
        PAP.Company_has_Url          False PAP.Subject_has_Property
        PAP.Person_has_Url           False PAP.Subject_has_Property
        PAP.Association_has_Url      False PAP.Subject_has_Property

    >>> fmt = "%%(type_name)-20s %%(is_relevant)-5s %%(polymorphic_epk)-5s %%(polymorphic_epks)-6s %%(epk_sig)s"
    >>> for i, et in enumerate (scope.app_type._T_Extension) :
    ...   if not i :
    ...     print (fmt %% (dict (type_name = "type_name", is_relevant = "relev", epk_sig = "epk_sig", polymorphic_epk = "p_epk", polymorphic_epks = "p_epks")))
    ...     print ("=" * 75)
    ...   if issubclass (et, scope.PAP.Subject.E_Type) :
    ...     print (fmt %% TFL.Caller.Object_Scope (et))
    type_name            relev p_epk p_epks epk_sig
    ===========================================================================
    PAP.Subject          False True  True   ()
    PAP.Legal_Entity     False True  True   ('name',)
    PAP.Company          True  False False  ('name', 'registered_in')
    PAP.Person           True  False False  ('last_name', 'first_name', 'middle_name', 'title')
    PAP.Association      True  True  True   ('name',)
    PAP.Association_S    True  True  True   ('name',)
    PAP.Association_T    True  False False  ('name', 'epk_new')

    >>> sk = lambda x : (not bool (x.children), x.i_rank)
    >>> for i, (T, l) in enumerate (children_trans_iter (scope.MOM.Id_Entity, sort_key = sk)) :
    ...     if not i :
    ...         print ("%%-50s   %%6s %%6s %%6s %%6s" %% ("type_name", "relev", "p_epk", "p_epks", "pr_epk"))
    ...         print ("=" * 80)
    ...     et = T.E_Type
    ...     fs = (et.is_relevant, et.polymorphic_epk, et.polymorphic_epks, et.polymorphic_relevant_epk)
    ...     if any (fs) :
    ...         hd  = "%%s%%s" %% ("  " * l, et.type_name)
    ...         hdl = len (hd)
    ...         sep = (" " if hdl %% 2 else "") + ". " * ((50 - hdl) // 2)
    ...         ts  = tuple ((x or "") for x in fs)
    ...         print (("%%s %%s %%6s %%6s %%6s %%6s" %% ((hd, sep) + ts)).rstrip ())
    type_name                                             relev  p_epk p_epks pr_epk
    ================================================================================
    MOM.Id_Entity  . . . . . . . . . . . . . . . . . .           True   True
      MOM.Link . . . . . . . . . . . . . . . . . . . .           True   True
        MOM.Link1  . . . . . . . . . . . . . . . . . .           True   True
          Auth.Link1 . . . . . . . . . . . . . . . . .           True   True
            Auth._Account_Action_  . . . . . . . . . .           True   True
                Auth.Account_EMail_Verification  . . .    True
                Auth.Account_Password_Reset  . . . . .    True
              Auth.Account_Activation  . . . . . . . .    True
              Auth.Account_Password_Change_Required  .    True
          EVT.Link1  . . . . . . . . . . . . . . . . .           True   True
            EVT._Recurrence_Mixin_ . . . . . . . . . .           True   True
              EVT.Recurrence_Spec  . . . . . . . . . .    True          True
              EVT.Recurrence_Rule  . . . . . . . . . .    True          True
            EVT.Event  . . . . . . . . . . . . . . . .    True          True
            EVT.Event_occurs . . . . . . . . . . . . .    True          True
          PAP.Link1  . . . . . . . . . . . . . . . . .           True   True
            PAP.Address_Position . . . . . . . . . . .    True
          SRM.Link1  . . . . . . . . . . . . . . . . .           True   True
            SRM.Regatta  . . . . . . . . . . . . . . .    True
              SRM.Regatta_C  . . . . . . . . . . . . .    True
              SRM.Regatta_H  . . . . . . . . . . . . .    True
            SRM.Boat . . . . . . . . . . . . . . . . .    True
            SRM.Sailor . . . . . . . . . . . . . . . .    True
            SRM.Race_Result  . . . . . . . . . . . . .    True
            SRM.Team . . . . . . . . . . . . . . . . .    True
          SWP.Link1  . . . . . . . . . . . . . . . . .           True   True
            SWP.Clip_O . . . . . . . . . . . . . . . .    True          True
            SWP.Picture  . . . . . . . . . . . . . . .    True
        MOM._MOM_Link_n_ . . . . . . . . . . . . . . .           True   True
          MOM.Link2  . . . . . . . . . . . . . . . . .           True   True
              Auth.Account_in_Group  . . . . . . . . .    True
            PAP.Link2  . . . . . . . . . . . . . . . .           True   True
              PAP.Subject_has_Property . . . . . . . .    True   True   True   True
                PAP.Subject_has_Address  . . . . . . .    True          True
                  PAP.Company_has_Address  . . . . . .    True
                  PAP.Person_has_Address . . . . . . .    True
                  PAP.Association_has_Address  . . . .    True          True
                PAP.Subject_has_Email  . . . . . . . .    True          True
                  PAP.Company_has_Email  . . . . . . .    True
                  PAP.Person_has_Email . . . . . . . .    True
                  PAP.Association_has_Email  . . . . .    True          True
                PAP.Subject_has_Phone  . . . . . . . .    True          True   True
                  PAP.Company_has_Phone  . . . . . . .    True
                  PAP.Person_has_Phone . . . . . . . .    True
                  PAP.Association_has_Phone  . . . . .    True          True
                PAP.Subject_has_Url  . . . . . . . . .    True          True
                  PAP.Company_has_Url  . . . . . . . .    True
                  PAP.Person_has_Url . . . . . . . . .    True
                  PAP.Association_has_Url  . . . . . .    True          True
              PAP.Person_has_Account . . . . . . . . .    True
              SRM.Boat_in_Regatta  . . . . . . . . . .    True
              SRM.Crew_Member  . . . . . . . . . . . .    True
              SRM.Team_has_Boat_in_Regatta . . . . . .    True
          PAP._MOM_Link_n_ . . . . . . . . . . . . . .           True   True
        Auth.Link  . . . . . . . . . . . . . . . . . .           True   True
        EVT.Link . . . . . . . . . . . . . . . . . . .           True   True
        PAP.Link . . . . . . . . . . . . . . . . . . .           True   True
        SRM.Link . . . . . . . . . . . . . . . . . . .           True   True
        SWP.Link . . . . . . . . . . . . . . . . . . .           True   True
      MOM.Object . . . . . . . . . . . . . . . . . . .           True   True
        Auth.Object  . . . . . . . . . . . . . . . . .           True   True
          Auth._Account_ . . . . . . . . . . . . . . .    True
            Auth.Account_Anonymous . . . . . . . . . .    True
            Auth.Account . . . . . . . . . . . . . . .    True
          Auth.Certificate . . . . . . . . . . . . . .    True
          Auth.Group . . . . . . . . . . . . . . . . .    True
        EVT.Object . . . . . . . . . . . . . . . . . .           True   True
          EVT.Calendar . . . . . . . . . . . . . . . .    True
        SWP.Object . . . . . . . . . . . . . . . . . .           True   True
          SWP.Object_PN  . . . . . . . . . . . . . . .           True   True
            SWP.Page . . . . . . . . . . . . . . . . .    True   True   True   True
              SWP.Page_Y . . . . . . . . . . . . . . .    True                 True
              SWP.Clip_X . . . . . . . . . . . . . . .    True
              SRM.Page . . . . . . . . . . . . . . . .    True                 True
            SWP.Gallery  . . . . . . . . . . . . . . .    True
        PAP.Object . . . . . . . . . . . . . . . . . .           True   True
          PAP.Property . . . . . . . . . . . . . . . .           True   True
            PAP.Address  . . . . . . . . . . . . . . .    True
            PAP.Email  . . . . . . . . . . . . . . . .    True
            PAP.Phone  . . . . . . . . . . . . . . . .    True
            PAP.Url  . . . . . . . . . . . . . . . . .    True
          PAP.Subject  . . . . . . . . . . . . . . . .           True   True
            PAP.Legal_Entity . . . . . . . . . . . . .           True   True
              PAP.Association  . . . . . . . . . . . .    True   True   True   True
                PAP.Association_S  . . . . . . . . . .    True   True   True   True
                  PAP.Association_T  . . . . . . . . .    True                 True
              PAP.Company  . . . . . . . . . . . . . .    True
            PAP.Person . . . . . . . . . . . . . . . .    True
        SRM.Object . . . . . . . . . . . . . . . . . .           True   True
          SRM._Boat_Class_ . . . . . . . . . . . . . .    True
            SRM.Boat_Class . . . . . . . . . . . . . .    True
            SRM.Handicap . . . . . . . . . . . . . . .    True
          SRM.Club . . . . . . . . . . . . . . . . . .    True
          SRM.Regatta_Event  . . . . . . . . . . . . .    True
      Auth.Id_Entity . . . . . . . . . . . . . . . . .           True   True
      EVT.Id_Entity  . . . . . . . . . . . . . . . . .           True   True
      SWP.Id_Entity  . . . . . . . . . . . . . . . . .           True   True
      PAP.Id_Entity  . . . . . . . . . . . . . . . . .           True   True
      SRM.Id_Entity  . . . . . . . . . . . . . . . . .           True   True


"""

### XXX auto cached roles are currently not supported
### XXX * either remove _test_acr or re-add auto-cached roles and fix _test_acr
_test_acr = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> PAP.Subject_has_Email.acr_map.get ("left", False)
    False
    >>> PAP.Company_has_Email.acr_map.get ("left", False)
    <Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) company --> companies [GTW.OMP.PAP.Email]>
    >>> PAP.Person_has_Email.acr_map.get ("left", False)
    <Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) person --> persons [GTW.OMP.PAP.Email]>

    >>> PAP.Subject_has_Email.acr_map.get ("right", False)
    <Role_Cacher_n (GTW.OMP.PAP.Subject_has_Email) email --> emails [GTW.OMP.PAP.Subject]>
    >>> PAP.Company_has_Email.acr_map.get ("right", False)
    <Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) email --> emails [GTW.OMP.PAP.Company]>
    >>> PAP.Person_has_Email.acr_map.get ("right", False)
    <Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) email --> emails [GTW.OMP.PAP.Person]>

    >>> sorted (PAP.Subject_has_Email.acr_map.values (), key = TFL.Getter.attr_name)
    [<Role_Cacher_n (GTW.OMP.PAP.Subject_has_Email) email --> emails [GTW.OMP.PAP.Subject]>]
    >>> sorted (PAP.Company_has_Email.acr_map.values (), key = TFL.Getter.attr_name)
    [<Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) company --> companies [GTW.OMP.PAP.Email]>, <Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) email --> emails [GTW.OMP.PAP.Company]>]
    >>> sorted (PAP.Person_has_Email.acr_map.values (), key = TFL.Getter.attr_name)
    [<Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) email --> emails [GTW.OMP.PAP.Person]>, <Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) person --> persons [GTW.OMP.PAP.Email]>]

"""

from   _GTW.__test__.model      import *
from   _MOM.import_MOM          import Q
from   _MOM.inspect             import children_trans_iter

from   itertools                import chain as ichain

import _GTW._OMP._PAP.Association

_Ancestor_Essence = GTW.OMP.PAP.Association

class Association_S (_Ancestor_Essence) :
    """Descendent of Association with identical epk_sig"""
# end class Association_S

_Ancestor_Essence = Association_S

class Association_T (_Ancestor_Essence) :
    """Descendent of Association_S with different epk_sig"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class epk_new (A_Int) :
            """Additional epk attribute"""

            kind               = Attr.Primary

        # end class epk_new

    # end class _Attributes

# end class Association_T

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Subjects
