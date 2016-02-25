# -*- coding: utf-8 -*-
# Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.Subject_has_VAT_IDN
#
# Purpose
#    Test PAP.Subject_has_VAT_IDN
#
# Revision Dates
#    24-Feb-2016 (CT) Creation
#    25-Feb-2016 (CT) Add tests for `Wrong_Type`
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> p1  = PAP.Person ("Doe", "Jane", title = "Dr.", raw = True)
    >>> p2  = PAP.Person ("Doe", "John", raw = True)
    >>> c1  = PAP.Company_1P (person = p1, raw = True)
    >>> c2  = PAP.Company ("John Doe, Inc.", "Paris")
    >>> c3  = PAP.Company ("Jane Doe, Inc.", "Paris")

    >>> print (PAP.Company_1P.E_Type.vat_idn.description)
    VAT identification number of Company_1P.

    >>> print (p1.ui_display, ": VAT-IDN =", p1.vat_idn)
    Doe Jane, Dr. : VAT-IDN = None

    >>> print (c1.ui_display, ": VAT-IDN =", c1.vat_idn)
    Doe Jane, Dr. : VAT-IDN = None

    >>> print (c2.ui_display, ": VAT-IDN =", c2.vat_idn)
    John Doe, Inc., Paris : VAT-IDN = None

    >>> eu1 = PAP.Person_has_VAT_IDN  (p1, vin = "GB999 9999 73")

    >>> _   = PAP.Person_has_VAT_IDN  (c3, vin = "GB999 9999 72")
    Traceback (most recent call last):
      ...
    Wrong_Type: Company 'Jane Doe, Inc., Paris' not eligible for attribute left,
        must be instance of Person

    >>> _   = PAP.Company_has_VAT_IDN (p2, vin = "GB999 9999 72")
    Traceback (most recent call last):
      ...
    Wrong_Type: Person 'Doe John' not eligible for attribute left,
        must be instance of Company

    >>> _   = PAP.Company_has_VAT_IDN (c1, vin = "GB999 9999 72")
    Traceback (most recent call last):
      ...
    Wrong_Type: Company_1P 'Doe Jane, Dr.' not eligible for attribute left,
        must be instance of Company, but not Company_1P

    >>> eu2 = PAP.Company_has_VAT_IDN (c2, vin = "FR83,404,833,048")

    >>> eu1
    PAP.Person_has_VAT_IDN (('doe', 'jane', '', 'dr.'), GB999999973)

    >>> eu2
    PAP.Company_has_VAT_IDN (('john doe, inc.', 'paris'), FR83404833048)

    >>> print (eu1.ui_display)
    Doe Jane, Dr., GB999999973

    >>> print (eu2.ui_display)
    John Doe, Inc., Paris, FR83404833048

    >>> _   = PAP.Person_has_VAT_IDN  (p2, vin = "FR83,404,833,048") # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    Invariants: The attribute values for 'vin' must be unique for each object
      The new definition of Person_has_VAT_IDN PAP.Person_has_VAT_IDN (('Doe', 'John', '', '', 'PAP.Person'), 'FR83404833048') would clash with 1 existing entities
      Already existing:
        PAP.Company_has_VAT_IDN (('John Doe, Inc.', 'Paris', 'PAP.Company'), 'FR83404833048')

    >>> print (p1.ui_display, ": VAT-IDN =", p1.vat_idn)
    Doe Jane, Dr. : VAT-IDN = GB999999973

    >>> print (c1.ui_display, ": VAT-IDN =", c1.vat_idn)
    Doe Jane, Dr. : VAT-IDN = GB999999973

    >>> print (c2.ui_display, ": VAT-IDN =", c2.vat_idn)
    John Doe, Inc., Paris : VAT-IDN = FR83404833048

    >>> _   = PAP.Company_has_VAT_IDN (c3, vin = "GB999 9999 73") # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    Invariants: The attribute values for 'vin' must be unique for each object
      The new definition of Company_has_VAT_IDN PAP.Company_has_VAT_IDN (('Jane Doe, Inc.', 'Paris', 'PAP.Company'), 'GB999999973') would clash with 1 existing entities
      Already existing:
        PAP.Person_has_VAT_IDN (('Doe', 'Jane', '', 'Dr.', 'PAP.Person'), 'GB999999973')

"""

_test_saw = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_table (apt, apt._SAW.et_map ["PAP.Subject_has_VAT_IDN"])
    PAP.Subject_has_VAT_IDN (MOM.Id_Entity) <Table pap_subject_has_vat_idn>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey('mom_id_entity.pid')
        Column vin                       : Text                 Primary VAT-IDN vin

    >>> show_table (apt, apt._SAW.et_map ["PAP.Company_has_VAT_IDN"])
    PAP.Company_has_VAT_IDN (PAP.Subject_has_VAT_IDN) PAP.Subject_has_VAT_IDN <Table pap_company_has_vat_idn>
        Column left                      : Integer              Link_Role__Init_Only Company left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey('pap_subject_has_vat_idn.pid')

    >>> show_table (apt, apt._SAW.et_map ["PAP.Person_has_VAT_IDN"])
    PAP.Person_has_VAT_IDN (PAP.Subject_has_VAT_IDN) PAP.Subject_has_VAT_IDN <Table pap_person_has_vat_idn>
        Column left                      : Integer              Link_Role__Init_Only Person left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey('pap_subject_has_vat_idn.pid')

    >>> for tn in ("PAP.Subject_has_VAT_IDN", "PAP.Company_has_VAT_IDN", "PAP.Person_has_VAT_IDN") :
    ...     T   = apt [tn]
    ...     ETW = T._SAW
    ...     ui  = ETW.unique_i
    ...     uo  = ETW.unique_o
    ...     if T.show_in_ui and ETW.unique :
    ...         tail = "" if ui == uo else \\
    ...             (((" + " if ui else "") + ", ".join (uo)) if uo else " =")
    ...         print (("%%-30s %%s%%s" %% (ETW.type_name, ", ".join (ui), tail)).strip ())
    PAP.Subject_has_VAT_IDN        vin
    PAP.Company_has_VAT_IDN        vin + left
    PAP.Person_has_VAT_IDN         vin + left

    >>> qr_ShV = apt.DBW.PNS.Q_Result.E_Type (apt ["PAP.Subject_has_VAT_IDN"], _strict = False)
    >>> qr_ChV = apt.DBW.PNS.Q_Result.E_Type (apt ["PAP.Company_has_VAT_IDN"], _strict = False)
    >>> qr_PhV = apt.DBW.PNS.Q_Result.E_Type (apt ["PAP.Person_has_VAT_IDN"], _strict = False)

    >>> print (qr_ShV.filter (left = 1))
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company_has_vat_idn."left" AS pap_company_has_vat_idn_left,
           pap_company_has_vat_idn.pid AS pap_company_has_vat_idn_pid,
           pap_person_has_vat_idn."left" AS pap_person_has_vat_idn_left,
           pap_person_has_vat_idn.pid AS pap_person_has_vat_idn_pid,
           pap_subject_has_vat_idn.pid AS pap_subject_has_vat_idn_pid,
           pap_subject_has_vat_idn.vin AS pap_subject_has_vat_idn_vin
         FROM mom_id_entity
           JOIN pap_subject_has_vat_idn ON mom_id_entity.pid = pap_subject_has_vat_idn.pid
           LEFT OUTER JOIN pap_company_has_vat_idn ON pap_subject_has_vat_idn.pid = pap_company_has_vat_idn.pid
           LEFT OUTER JOIN pap_person_has_vat_idn ON pap_subject_has_vat_idn.pid = pap_person_has_vat_idn.pid
         WHERE pap_company_has_vat_idn."left" = :left_1
            OR pap_person_has_vat_idn."left" = :left_2

    >>> print (qr_ChV.filter (left = 1))
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company_has_vat_idn."left" AS pap_company_has_vat_idn_left,
           pap_company_has_vat_idn.pid AS pap_company_has_vat_idn_pid,
           pap_subject_has_vat_idn.pid AS pap_subject_has_vat_idn_pid,
           pap_subject_has_vat_idn.vin AS pap_subject_has_vat_idn_vin
         FROM mom_id_entity
           JOIN pap_subject_has_vat_idn ON mom_id_entity.pid = pap_subject_has_vat_idn.pid
           JOIN pap_company_has_vat_idn ON pap_subject_has_vat_idn.pid = pap_company_has_vat_idn.pid
         WHERE pap_company_has_vat_idn."left" = :left_1

    >>> print (qr_PhV.filter (left = 1))
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person_has_vat_idn."left" AS pap_person_has_vat_idn_left,
           pap_person_has_vat_idn.pid AS pap_person_has_vat_idn_pid,
           pap_subject_has_vat_idn.pid AS pap_subject_has_vat_idn_pid,
           pap_subject_has_vat_idn.vin AS pap_subject_has_vat_idn_vin
         FROM mom_id_entity
           JOIN pap_subject_has_vat_idn ON mom_id_entity.pid = pap_subject_has_vat_idn.pid
           JOIN pap_person_has_vat_idn ON pap_subject_has_vat_idn.pid = pap_person_has_vat_idn.pid
         WHERE pap_person_has_vat_idn."left" = :left_1


    >>> show_query (qr_PhV.filter (Q.vin.STARTSWITH ("AT"), left = 1))
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person_has_vat_idn."left" AS pap_person_has_vat_idn_left,
           pap_person_has_vat_idn.pid AS pap_person_has_vat_idn_pid,
           pap_subject_has_vat_idn.pid AS pap_subject_has_vat_idn_pid,
           pap_subject_has_vat_idn.vin AS pap_subject_has_vat_idn_vin
         FROM mom_id_entity
           JOIN pap_subject_has_vat_idn ON mom_id_entity.pid = pap_subject_has_vat_idn.pid
           JOIN pap_person_has_vat_idn ON pap_subject_has_vat_idn.pid = pap_person_has_vat_idn.pid
         WHERE (pap_subject_has_vat_idn.vin LIKE :vin_1 || '%%%%')
            AND pap_person_has_vat_idn."left" = :left_1
    Parameters:
         left_1               : 1
         vin_1                : 'AT'

"""

from   _GTW.__test__.model               import *
from   _GTW.__test__._SAW_test_functions import show_query, show_table
from   _MOM.import_MOM                   import Q
from   _TFL.pyk                          import pyk

import _GTW._OMP._PAP.Company_1P
import _GTW._OMP._PAP.Subject_has_VAT_IDN
import _GTW._OMP._PAP.Company_has_VAT_IDN
import _GTW._OMP._PAP.Person_has_VAT_IDN

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_main        = _test_code
        )
    )

__test__.update \
    ( Scaffold.create_test_dict \
        ( dict
            ( test_saw     = _test_saw
            )
        , ignore           = ("HPS", "MYS")
        )
    )

### __END__ GTW.__test__.Subject_has_VAT_IDN
