# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.MF3
#
# Purpose
#    Test GTW.MF3
#
# Revision Dates
#    25-Apr-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import Q

import _GTW._OMP._PAP.import_PAP
GTW.OMP.PAP.Phone.change_attribute_default ("country_code", "43")

from   _GTW.__test__.model      import *
from   _GTW._MF3                import Element as MF3_E

from   _TFL.Regexp              import Multi_Re_Replacer, Re_Replacer, re

_cleaner = Re_Replacer \
    ( r"'\$sid' : '[0-9a-f]+'"
    , r"'$sid' : <sid value>"
    )

def show_elements (f, attr) :
    getter = getattr (Q, attr)
    for e in f.elements_transitive () :
        try :
            v = getter (e)
        except AttributeError :
            v = "---"
        if isinstance (v, TFL.Undef) :
            v = "---"
        print (e, v)
# end def show_elements

def show_field_values (f) :
    show_formatted (f.as_json_cargo ["cargo"] ["field_values"])
# end def show_field_values

def show_formatted (x) :
    result = _cleaner (formatted (x))
    print (result)
# end def show_formatted

_test_element = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> p   = PAP.Person ("Tanzer", "Christian", lifetime = ("19590926", ), raw=True)
    >>> ph  = PAP.Phone  ("43", "1", "98765432", raw=True)
    >>> pph = PAP.Person_has_Phone (p, ph, desc = "example", extension = "42", raw=True)

    >>> p_attr_spec= { "lifetime.start" : dict (init = "2000-07-23"), "sex" : dict (init = "M")}
    >>> F_Person   = MF3_E.Entity.Auto (scope.PAP.Person, id_prefix = "X")
    >>> F_Person_s = MF3_E.Entity.Auto (scope.PAP.Person, id_prefix = "Y", attr_spec = { "lifetime.finish" : dict (skip = True)})
    >>> f_Person   = F_Person (scope)
    >>> f_Person_s = F_Person_s (scope, attr_spec = p_attr_spec)
    >>> f_p        = F_Person (scope, p)
    >>> f_p_s      = F_Person_s (scope, p, attr_spec = p_attr_spec)

    >>> F_Person
    <class Entity X-24>

    >>> F_Person ["X-24:lifetime.start"]
    <class Field X-24:lifetime.start>

    >>> F_Person ["lifetime.finish"]
    <class Field X-24:lifetime.finish>

    >>> f_Person ["X-24:lifetime.start"]
    <Field X-24:lifetime.start>

    >>> f_Person ["lifetime.finish"]
    <Field X-24:lifetime.finish>

    >>> show_elements (f_Person, "cooked")
    <Entity X-24> ---
    <Field X-24:last_name>
    <Field X-24:first_name>
    <Field X-24:middle_name>
    <Field X-24:title>
    <Field_Composite X-24:lifetime> ()
    <Field X-24:lifetime.start> None
    <Field X-24:lifetime.finish> None
    <Field X-24:sex> None

    >>> show_elements (f_p, "cooked")
    <Entity X-24> ---
    <Field X-24:last_name> tanzer
    <Field X-24:first_name> christian
    <Field X-24:middle_name>
    <Field X-24:title>
    <Field_Composite X-24:lifetime> (u'1959-09-26', )
    <Field X-24:lifetime.start> 1959-09-26
    <Field X-24:lifetime.finish> None
    <Field X-24:sex> None

    >>> show_elements (f_p, "q_name")
    <Entity X-24> None
    <Field X-24:last_name> last_name
    <Field X-24:first_name> first_name
    <Field X-24:middle_name> middle_name
    <Field X-24:title> title
    <Field_Composite X-24:lifetime> lifetime
    <Field X-24:lifetime.start> lifetime.start
    <Field X-24:lifetime.finish> lifetime.finish
    <Field X-24:sex> sex

    >>> for e in f_p.field_elements :
    ...     print (e)
    <Field X-24:last_name>
    <Field X-24:first_name>
    <Field X-24:middle_name>
    <Field X-24:title>
    <Field X-24:lifetime.start>
    <Field X-24:lifetime.finish>
    <Field X-24:sex>

    >>> show_elements (f_Person, "edit")
    <Entity X-24> ---
    <Field X-24:last_name>
    <Field X-24:first_name>
    <Field X-24:middle_name>
    <Field X-24:title>
    <Field_Composite X-24:lifetime>
    <Field X-24:lifetime.start>
    <Field X-24:lifetime.finish>
    <Field X-24:sex>

    >>> show_elements (f_Person_s, "edit")
    <Entity Y-24> ---
    <Field Y-24:last_name>
    <Field Y-24:first_name>
    <Field Y-24:middle_name>
    <Field Y-24:title>
    <Field_Composite Y-24:lifetime>
    <Field Y-24:lifetime.start> 2000-07-23
    <Field Y-24:sex> M

    >>> show_elements (f_p, "edit")
    <Entity X-24> ---
    <Field X-24:last_name> Tanzer
    <Field X-24:first_name> Christian
    <Field X-24:middle_name>
    <Field X-24:title>
    <Field_Composite X-24:lifetime>
    <Field X-24:lifetime.start> 1959-09-26
    <Field X-24:lifetime.finish>
    <Field X-24:sex>

    >>> show_elements (f_p_s, "edit")
    <Entity Y-24> ---
    <Field Y-24:last_name> Tanzer
    <Field Y-24:first_name> Christian
    <Field Y-24:middle_name>
    <Field Y-24:title>
    <Field_Composite Y-24:lifetime>
    <Field Y-24:lifetime.start> 2000-07-23
    <Field Y-24:sex> M

    >>> show_elements (f_p, "ui_display")
    <Entity X-24> Tanzer Christian
    <Field X-24:last_name> Tanzer
    <Field X-24:first_name> Christian
    <Field X-24:middle_name>
    <Field X-24:title>
    <Field_Composite X-24:lifetime> 1959-09-26
    <Field X-24:lifetime.start> 1959-09-26
    <Field X-24:lifetime.finish>
    <Field X-24:sex>

    >>> show_elements (f_p, "essence")
    <Entity X-24> (u'tanzer', u'christian', u'', u'')
    <Field X-24:last_name> (u'tanzer', u'christian', u'', u'')
    <Field X-24:first_name> (u'tanzer', u'christian', u'', u'')
    <Field X-24:middle_name> (u'tanzer', u'christian', u'', u'')
    <Field X-24:title> (u'tanzer', u'christian', u'', u'')
    <Field_Composite X-24:lifetime> (u'1959-09-26', )
    <Field X-24:lifetime.start> (u'1959-09-26', )
    <Field X-24:lifetime.finish> (u'1959-09-26', )
    <Field X-24:sex> (u'tanzer', u'christian', u'', u'')

    >>> show_elements (f_p, "Entity.essence")
    <Entity X-24> (u'tanzer', u'christian', u'', u'')
    <Field X-24:last_name> (u'tanzer', u'christian', u'', u'')
    <Field X-24:first_name> (u'tanzer', u'christian', u'', u'')
    <Field X-24:middle_name> (u'tanzer', u'christian', u'', u'')
    <Field X-24:title> (u'tanzer', u'christian', u'', u'')
    <Field_Composite X-24:lifetime> (u'tanzer', u'christian', u'', u'')
    <Field X-24:lifetime.start> (u'tanzer', u'christian', u'', u'')
    <Field X-24:lifetime.finish> (u'tanzer', u'christian', u'', u'')
    <Field X-24:sex> (u'tanzer', u'christian', u'', u'')

    >>> show_elements (f_Person, "root")
    <Entity X-24> <Entity X-24>
    <Field X-24:last_name> <Entity X-24>
    <Field X-24:first_name> <Entity X-24>
    <Field X-24:middle_name> <Entity X-24>
    <Field X-24:title> <Entity X-24>
    <Field_Composite X-24:lifetime> <Entity X-24>
    <Field X-24:lifetime.start> <Entity X-24>
    <Field X-24:lifetime.finish> <Entity X-24>
    <Field X-24:sex> <Entity X-24>

    >>> show_elements (f_Person, "Entity")
    <Entity X-24> <Entity X-24>
    <Field X-24:last_name> <Entity X-24>
    <Field X-24:first_name> <Entity X-24>
    <Field X-24:middle_name> <Entity X-24>
    <Field X-24:title> <Entity X-24>
    <Field_Composite X-24:lifetime> <Entity X-24>
    <Field X-24:lifetime.start> <Entity X-24>
    <Field X-24:lifetime.finish> <Entity X-24>
    <Field X-24:sex> <Entity X-24>

    >>> show_elements (f_Person, "template_macro")
    <Entity X-24> Entity_Form
    <Field X-24:last_name> Field
    <Field X-24:first_name> Field
    <Field X-24:middle_name> Field
    <Field X-24:title> Field
    <Field_Composite X-24:lifetime> Field_Composite
    <Field X-24:lifetime.start> Field
    <Field X-24:lifetime.finish> Field
    <Field X-24:sex> Field

    >>> show_elements (f_Person, "template_module")
    <Entity X-24> mf3
    <Field X-24:last_name> None
    <Field X-24:first_name> None
    <Field X-24:middle_name> None
    <Field X-24:title> None
    <Field_Composite X-24:lifetime> mf3_h_cols
    <Field X-24:lifetime.start> None
    <Field X-24:lifetime.finish> None
    <Field X-24:sex> None

    >>> show_field_values (f_p)
    { 'X-24:first_name' :
        { 'init' : 'Christian' }
    , 'X-24:last_name' :
        { 'init' : 'Tanzer' }
    , 'X-24:lifetime.finish' :
        {}
    , 'X-24:lifetime.start' :
        { 'init' : '1959-09-26' }
    , 'X-24:middle_name' :
        {}
    , 'X-24:sex' :
        {}
    , 'X-24:title' :
        {}
    }

    >>> F_PhP   = MF3_E.Entity.Auto (scope.PAP.Person_has_Phone, id_prefix = "X")
    >>> f_PhP   = F_PhP (scope)
    >>> f_pph   = F_PhP (scope, pph)
    >>> F_PhP_s = MF3_E.Entity.Auto (scope.PAP.Person_has_Phone, id_prefix = "Y", attr_spec = { "left.middle_name" : dict (skip = 1), "right.country_code" : dict (init ="49", prefilled = 1)})
    >>> f_PhP_s = F_PhP_s (scope)
    >>> F_PhP_z = MF3_E.Entity.Auto (scope.PAP.Person_has_Phone, id_prefix = "Z", attr_spec = { "left" : dict (attr_selector = MOM.Attr.Selector.editable), "right" : dict (attr_selector = MOM.Attr.Selector.editable)})
    >>> f_PhP_z = F_PhP_z (scope)

    >>> show_elements (f_PhP_z, "Entity")
    <Entity Z-117> <Entity Z-117>
    <Field_Entity Z-117:left> <Entity Z-117>
    <Field Z-117:left.last_name> <Field_Entity Z-117:left>
    <Field Z-117:left.first_name> <Field_Entity Z-117:left>
    <Field Z-117:left.middle_name> <Field_Entity Z-117:left>
    <Field Z-117:left.title> <Field_Entity Z-117:left>
    <Field_Composite Z-117:left.lifetime> <Field_Entity Z-117:left>
    <Field Z-117:left.lifetime.start> <Field_Entity Z-117:left>
    <Field Z-117:left.lifetime.finish> <Field_Entity Z-117:left>
    <Field Z-117:left.sex> <Field_Entity Z-117:left>
    <Field_Entity Z-117:right> <Entity Z-117>
    <Field Z-117:right.country_code> <Field_Entity Z-117:right>
    <Field Z-117:right.area_code> <Field_Entity Z-117:right>
    <Field Z-117:right.number> <Field_Entity Z-117:right>
    <Field Z-117:right.desc> <Field_Entity Z-117:right>
    <Field Z-117:extension> <Entity Z-117>
    <Field Z-117:desc> <Entity Z-117>

    >>> show_elements (f_PhP_z, "q_name")
    <Entity Z-117> None
    <Field_Entity Z-117:left> left
    <Field Z-117:left.last_name> left.last_name
    <Field Z-117:left.first_name> left.first_name
    <Field Z-117:left.middle_name> left.middle_name
    <Field Z-117:left.title> left.title
    <Field_Composite Z-117:left.lifetime> left.lifetime
    <Field Z-117:left.lifetime.start> left.lifetime.start
    <Field Z-117:left.lifetime.finish> left.lifetime.finish
    <Field Z-117:left.sex> left.sex
    <Field_Entity Z-117:right> right
    <Field Z-117:right.country_code> right.country_code
    <Field Z-117:right.area_code> right.area_code
    <Field Z-117:right.number> right.number
    <Field Z-117:right.desc> right.desc
    <Field Z-117:extension> extension
    <Field Z-117:desc> desc

    >>> show_elements (f_PhP_z, "r_name")
    <Entity Z-117> ---
    <Field_Entity Z-117:left> left
    <Field Z-117:left.last_name> last_name
    <Field Z-117:left.first_name> first_name
    <Field Z-117:left.middle_name> middle_name
    <Field Z-117:left.title> title
    <Field_Composite Z-117:left.lifetime> lifetime
    <Field Z-117:left.lifetime.start> lifetime.start
    <Field Z-117:left.lifetime.finish> lifetime.finish
    <Field Z-117:left.sex> sex
    <Field_Entity Z-117:right> right
    <Field Z-117:right.country_code> country_code
    <Field Z-117:right.area_code> area_code
    <Field Z-117:right.number> number
    <Field Z-117:right.desc> desc
    <Field Z-117:extension> extension
    <Field Z-117:desc> desc

    >>> show_elements (f_PhP, "root")
    <Entity X-117> <Entity X-117>
    <Field_Entity X-117:left> <Entity X-117>
    <Field X-117:left.last_name> <Entity X-117>
    <Field X-117:left.first_name> <Entity X-117>
    <Field X-117:left.middle_name> <Entity X-117>
    <Field X-117:left.title> <Entity X-117>
    <Field_Entity X-117:right> <Entity X-117>
    <Field X-117:right.country_code> <Entity X-117>
    <Field X-117:right.area_code> <Entity X-117>
    <Field X-117:right.number> <Entity X-117>
    <Field X-117:extension> <Entity X-117>
    <Field X-117:desc> <Entity X-117>

    >>> show_elements (f_PhP, "Entity")
    <Entity X-117> <Entity X-117>
    <Field_Entity X-117:left> <Entity X-117>
    <Field X-117:left.last_name> <Field_Entity X-117:left>
    <Field X-117:left.first_name> <Field_Entity X-117:left>
    <Field X-117:left.middle_name> <Field_Entity X-117:left>
    <Field X-117:left.title> <Field_Entity X-117:left>
    <Field_Entity X-117:right> <Entity X-117>
    <Field X-117:right.country_code> <Field_Entity X-117:right>
    <Field X-117:right.area_code> <Field_Entity X-117:right>
    <Field X-117:right.number> <Field_Entity X-117:right>
    <Field X-117:extension> <Entity X-117>
    <Field X-117:desc> <Entity X-117>

    >>> show_elements (f_PhP, "Entity.E_Type.type_name")
    <Entity X-117> PAP.Person_has_Phone
    <Field_Entity X-117:left> PAP.Person_has_Phone
    <Field X-117:left.last_name> PAP.Person
    <Field X-117:left.first_name> PAP.Person
    <Field X-117:left.middle_name> PAP.Person
    <Field X-117:left.title> PAP.Person
    <Field_Entity X-117:right> PAP.Person_has_Phone
    <Field X-117:right.country_code> PAP.Phone
    <Field X-117:right.area_code> PAP.Phone
    <Field X-117:right.number> PAP.Phone
    <Field X-117:extension> PAP.Person_has_Phone
    <Field X-117:desc> PAP.Person_has_Phone

    >>> show_elements (f_PhP, "E_Type.type_name")
    <Entity X-117> PAP.Person_has_Phone
    <Field_Entity X-117:left> PAP.Person
    <Field X-117:left.last_name> PAP.Person
    <Field X-117:left.first_name> PAP.Person
    <Field X-117:left.middle_name> PAP.Person
    <Field X-117:left.title> PAP.Person
    <Field_Entity X-117:right> PAP.Phone
    <Field X-117:right.country_code> PAP.Phone
    <Field X-117:right.area_code> PAP.Phone
    <Field X-117:right.number> PAP.Phone
    <Field X-117:extension> PAP.Person_has_Phone
    <Field X-117:desc> PAP.Person_has_Phone

    >>> show_elements (f_PhP, "attr.E_Type.type_name")
    <Entity X-117> ---
    <Field_Entity X-117:left> PAP.Person
    <Field X-117:left.last_name> ---
    <Field X-117:left.first_name> ---
    <Field X-117:left.middle_name> ---
    <Field X-117:left.title> ---
    <Field_Entity X-117:right> PAP.Phone
    <Field X-117:right.country_code> ---
    <Field X-117:right.area_code> ---
    <Field X-117:right.number> ---
    <Field X-117:extension> ---
    <Field X-117:desc> ---

    >>> show_elements (F_PhP, "parent")
    <class Entity X-117> None
    <class Field_Entity X-117:left> <class Entity X-117>
    <class Field X-117:left.last_name> <class Field_Entity X-117:left>
    <class Field X-117:left.first_name> <class Field_Entity X-117:left>
    <class Field X-117:left.middle_name> <class Field_Entity X-117:left>
    <class Field X-117:left.title> <class Field_Entity X-117:left>
    <class Field_Entity X-117:right> <class Entity X-117>
    <class Field X-117:right.country_code> <class Field_Entity X-117:right>
    <class Field X-117:right.area_code> <class Field_Entity X-117:right>
    <class Field X-117:right.number> <class Field_Entity X-117:right>
    <class Field X-117:extension> <class Entity X-117>
    <class Field X-117:desc> <class Entity X-117>

    >>> show_elements (f_PhP, "parent")
    <Entity X-117> None
    <Field_Entity X-117:left> <Entity X-117>
    <Field X-117:left.last_name> <Field_Entity X-117:left>
    <Field X-117:left.first_name> <Field_Entity X-117:left>
    <Field X-117:left.middle_name> <Field_Entity X-117:left>
    <Field X-117:left.title> <Field_Entity X-117:left>
    <Field_Entity X-117:right> <Entity X-117>
    <Field X-117:right.country_code> <Field_Entity X-117:right>
    <Field X-117:right.area_code> <Field_Entity X-117:right>
    <Field X-117:right.number> <Field_Entity X-117:right>
    <Field X-117:extension> <Entity X-117>
    <Field X-117:desc> <Entity X-117>

    >>> for e in f_PhP.entity_elements :
    ...     print (e)
    <Entity X-117>
    <Field_Entity X-117:left>
    <Field_Entity X-117:right>

    >>> for e in f_PhP.field_elements :
    ...     print (e)
    <Field_Entity X-117:left>
    <Field_Entity X-117:right>
    <Field X-117:extension>
    <Field X-117:desc>

    >>> show_elements (F_PhP, "input_widget")
    <class Entity X-117> ---
    <class Field_Entity X-117:left> mf3_input, id_entity
    <class Field X-117:left.last_name> mf3_input, string
    <class Field X-117:left.first_name> mf3_input, string
    <class Field X-117:left.middle_name> mf3_input, string
    <class Field X-117:left.title> mf3_input, string
    <class Field_Entity X-117:right> mf3_input, id_entity
    <class Field X-117:right.country_code> mf3_input, number
    <class Field X-117:right.area_code> mf3_input, number
    <class Field X-117:right.number> mf3_input, number
    <class Field X-117:extension> mf3_input, number
    <class Field X-117:desc> mf3_input, string

    >>> show_elements (f_PhP, "input_widget")
    <Entity X-117> ---
    <Field_Entity X-117:left> mf3_input, id_entity
    <Field X-117:left.last_name> mf3_input, string
    <Field X-117:left.first_name> mf3_input, string
    <Field X-117:left.middle_name> mf3_input, string
    <Field X-117:left.title> mf3_input, string
    <Field_Entity X-117:right> mf3_input, id_entity
    <Field X-117:right.country_code> mf3_input, number
    <Field X-117:right.area_code> mf3_input, number
    <Field X-117:right.number> mf3_input, number
    <Field X-117:extension> mf3_input, number
    <Field X-117:desc> mf3_input, string

    >>> show_elements (f_PhP, "template_macro")
    <Entity X-117> Entity_Form
    <Field_Entity X-117:left> Field_Entity
    <Field X-117:left.last_name> Field
    <Field X-117:left.first_name> Field
    <Field X-117:left.middle_name> Field
    <Field X-117:left.title> Field
    <Field_Entity X-117:right> Field_Entity
    <Field X-117:right.country_code> Field
    <Field X-117:right.area_code> Field
    <Field X-117:right.number> Field
    <Field X-117:extension> Field
    <Field X-117:desc> Field

    >>> show_elements (f_PhP, "cooked")
    <Entity X-117> ---
    <Field_Entity X-117:left> None
    <Field X-117:left.last_name>
    <Field X-117:left.first_name>
    <Field X-117:left.middle_name>
    <Field X-117:left.title>
    <Field_Entity X-117:right> None
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code>
    <Field X-117:right.number>
    <Field X-117:extension>
    <Field X-117:desc>

    >>> show_elements (f_PhP, "edit")
    <Entity X-117> ---
    <Field_Entity X-117:left>
    <Field X-117:left.last_name>
    <Field X-117:left.first_name>
    <Field X-117:left.middle_name>
    <Field X-117:left.title>
    <Field_Entity X-117:right>
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code>
    <Field X-117:right.number>
    <Field X-117:extension>
    <Field X-117:desc>

    >>> show_elements (f_PhP_s, "edit")
    <Entity Y-117> ---
    <Field_Entity Y-117:left>
    <Field Y-117:left.last_name>
    <Field Y-117:left.first_name>
    <Field Y-117:left.title>
    <Field_Entity Y-117:right>
    <Field Y-117:right.country_code> 49
    <Field Y-117:right.area_code>
    <Field Y-117:right.number>
    <Field Y-117:extension>
    <Field Y-117:desc>

    >>> show_elements (f_PhP_s, "prefilled")
    <Entity Y-117> ---
    <Field_Entity Y-117:left> False
    <Field Y-117:left.last_name> False
    <Field Y-117:left.first_name> False
    <Field Y-117:left.title> False
    <Field_Entity Y-117:right> False
    <Field Y-117:right.country_code> 1
    <Field Y-117:right.area_code> False
    <Field Y-117:right.number> False
    <Field Y-117:extension> False
    <Field Y-117:desc> False

    >>> show_elements (f_pph, "cooked")
    <Entity X-117> ---
    <Field_Entity X-117:left> (u'tanzer', u'christian', u'', u'')
    <Field X-117:left.last_name> tanzer
    <Field X-117:left.first_name> christian
    <Field X-117:left.middle_name>
    <Field X-117:left.title>
    <Field_Entity X-117:right> (u'43', u'1', u'98765432')
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code> 1
    <Field X-117:right.number> 98765432
    <Field X-117:extension> 42
    <Field X-117:desc> example

    >>> show_elements (f_pph, "edit")
    <Entity X-117> ---
    <Field_Entity X-117:left> 1
    <Field X-117:left.last_name> Tanzer
    <Field X-117:left.first_name> Christian
    <Field X-117:left.middle_name>
    <Field X-117:left.title>
    <Field_Entity X-117:right> 2
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code> 1
    <Field X-117:right.number> 98765432
    <Field X-117:extension> 42
    <Field X-117:desc> example

    >>> show_elements (f_pph, "ui_display")
    <Entity X-117> Tanzer Christian, 43/1/98765432, 42
    <Field_Entity X-117:left> Tanzer Christian
    <Field X-117:left.last_name> Tanzer
    <Field X-117:left.first_name> Christian
    <Field X-117:left.middle_name>
    <Field X-117:left.title>
    <Field_Entity X-117:right> 43/1/98765432
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code> 1
    <Field X-117:right.number> 98765432
    <Field X-117:extension> 42
    <Field X-117:desc> example

    >>> show_elements (f_pph, "essence")
    <Entity X-117> ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'98765432'), u'42')
    <Field_Entity X-117:left> (u'tanzer', u'christian', u'', u'')
    <Field X-117:left.last_name> (u'tanzer', u'christian', u'', u'')
    <Field X-117:left.first_name> (u'tanzer', u'christian', u'', u'')
    <Field X-117:left.middle_name> (u'tanzer', u'christian', u'', u'')
    <Field X-117:left.title> (u'tanzer', u'christian', u'', u'')
    <Field_Entity X-117:right> (u'43', u'1', u'98765432')
    <Field X-117:right.country_code> (u'43', u'1', u'98765432')
    <Field X-117:right.area_code> (u'43', u'1', u'98765432')
    <Field X-117:right.number> (u'43', u'1', u'98765432')
    <Field X-117:extension> ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'98765432'), u'42')
    <Field X-117:desc> ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'98765432'), u'42')

    >>> show_elements (f_pph, "q_name")
    <Entity X-117> None
    <Field_Entity X-117:left> left
    <Field X-117:left.last_name> left.last_name
    <Field X-117:left.first_name> left.first_name
    <Field X-117:left.middle_name> left.middle_name
    <Field X-117:left.title> left.title
    <Field_Entity X-117:right> right
    <Field X-117:right.country_code> right.country_code
    <Field X-117:right.area_code> right.area_code
    <Field X-117:right.number> right.number
    <Field X-117:extension> extension
    <Field X-117:desc> desc

    >>> show_elements (f_pph, "prefilled")
    <Entity X-117> ---
    <Field_Entity X-117:left> False
    <Field X-117:left.last_name> False
    <Field X-117:left.first_name> False
    <Field X-117:left.middle_name> False
    <Field X-117:left.title> False
    <Field_Entity X-117:right> False
    <Field X-117:right.country_code> False
    <Field X-117:right.area_code> False
    <Field X-117:right.number> False
    <Field X-117:extension> False
    <Field X-117:desc> False

    >>> show_field_values (f_pph)
    { 'X-117:desc' :
        { 'init' : 'example' }
    , 'X-117:extension' :
        { 'init' : '42' }
    , 'X-117:left' :
        { 'init' :
            { 'cid' : 1
            , 'pid' : 1
            }
        }
    , 'X-117:right' :
        { 'init' :
            { 'cid' : 2
            , 'pid' : 2
            }
        }
    , 'X-117:right.area_code' :
        { 'init' : '1' }
    , 'X-117:right.country_code' :
        { 'init' : '43' }
    , 'X-117:right.number' :
        { 'init' : '98765432' }
    }


    >>> show_field_values (f_PhP_s)
    { 'Y-117:desc' :
        {}
    , 'Y-117:extension' :
        {}
    , 'Y-117:left' :
        { 'init' :
            {}
        }
    , 'Y-117:right' :
        { 'init' :
            {}
        }
    , 'Y-117:right.area_code' :
        {}
    , 'Y-117:right.country_code' :
        { 'edit' : '49' }
    , 'Y-117:right.number' :
        {}
    }


    >>> show_field_values (f_PhP_z)
    { 'Z-117:desc' :
        {}
    , 'Z-117:extension' :
        {}
    , 'Z-117:left' :
        { 'init' :
            {}
        }
    , 'Z-117:right' :
        { 'init' :
            {}
        }
    , 'Z-117:right.area_code' :
        {}
    , 'Z-117:right.country_code' :
        { 'edit' : '43' }
    , 'Z-117:right.desc' :
        {}
    , 'Z-117:right.number' :
        {}
    }



    >>> list (x.id for x in F_PhP.elements_transitive ()) == list (x.id for x in f_PhP.elements_transitive ())
    True

    >>> list (x.id for x in f_pph.elements_transitive ()) == list (x.id for x in f_PhP.elements_transitive ())
    True
"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( element = _test_element
        )
    )

### __END__ GTW.__test__.MF3
