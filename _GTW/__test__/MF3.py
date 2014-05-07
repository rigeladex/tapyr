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

from   _GTW                       import GTW
from   _MOM.import_MOM            import Q

import _GTW._OMP._PAP.import_PAP
GTW.OMP.PAP.Phone.change_attribute_default ("country_code", "43")

from   _GTW.__test__.model        import *
from   _GTW._MF3                  import Element as MF3_E

from   _TFL._Meta.Single_Dispatch import Single_Dispatch
from   _TFL.Formatter             import formatted_1
from   _TFL.Regexp                import Multi_Re_Replacer, Re_Replacer, re

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
        print (("%s %s" % (e, v)).strip ())
# end def show_elements

@Single_Dispatch (T = MF3_E._Base_)
def elem_x (x, getters, default = "---") :
    nick   = "_".join \
        (p [0] for p in x.__class__.__name__.strip ("_").split ("_"))
    result = ["%-2s   " % (nick, )]
    for getter in getters :
        try :
            tail  = getter (x)
        except AttributeError :
            tail = default
        if isinstance (tail, TFL.Undef) :
            tail = default
        if isinstance (tail, dict) :
            tail = ", ".join \
                ("%s = %s" % (k, v) for k, v in sorted (pyk.iteritems (tail)))
        if isinstance (tail, (dict, list, tuple)) :
            tail = formatted_1 (tail)
        result.append (str (tail))
    return result
# end def elem_x

def show_elements_x (f, * attrs, ** kw) :
    def _format (lens, elems) :
        return "  ".join \
            (("%-*s" % (l, e)) for l, e in zip (lens, elems)).rstrip ()
    default = kw.get ("---")
    filter  = kw.get ("filter", lambda x : True)
    getters = tuple (getattr (Q, attr) for attr in attrs)
    elems   = tuple \
        (   elem_x (e, getters, default = default)
        for e in f.elements_transitive () if filter (e)
        )
    lens    = list ((max (len (e) for e in es)) for es in zip (* elems))
    print (_format (lens, ("Type", ) + attrs))
    print ("=" * (sum (lens) + 2 * len (lens)))
    for es in elems :
        print (_format (lens, es))
# end def show_elements_x

def show_completers (f, * attrs, ** kw) :
    kw.setdefault ("filter", Q.completer != None)
    return show_elements_x (f, * attrs, ** kw)
# end def show_completers

def show_completers_js (f) :
    show_formatted (f.as_json_cargo ["completers"])
# end def show_completers_js

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
    >>> F_PhP_z = MF3_E.Entity.Auto (scope.PAP.Person_has_Phone, id_prefix = "Z", attr_spec = { "left" : dict (allow_new = True, attr_selector = MOM.Attr.Selector.editable), "right" : dict (attr_selector = MOM.Attr.Selector.editable)})
    >>> f_PhP_z = F_PhP_z (scope)

    >>> show_elements_x (f_PhP_s, "id", "allow_new", filter = (Q.allow_new != None))
    Type    id           allow_new
    ============================
    F_E     Y-117:left   False
    F_E     Y-117:right  True

    >>> show_elements_x (f_PhP_z, "id", "allow_new", filter = (Q.allow_new != None))
    Type    id           allow_new
    ===========================
    F_E     Z-117:left   True
    F_E     Z-117:right  True

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
    <Field_Entity X-117:right> <Entity X-117>
    <Field X-117:right.country_code> <Entity X-117>
    <Field X-117:right.area_code> <Entity X-117>
    <Field X-117:right.number> <Entity X-117>
    <Field X-117:extension> <Entity X-117>
    <Field X-117:desc> <Entity X-117>

    >>> show_elements (f_PhP, "Entity")
    <Entity X-117> <Entity X-117>
    <Field_Entity X-117:left> <Entity X-117>
    <Field_Entity X-117:right> <Entity X-117>
    <Field X-117:right.country_code> <Field_Entity X-117:right>
    <Field X-117:right.area_code> <Field_Entity X-117:right>
    <Field X-117:right.number> <Field_Entity X-117:right>
    <Field X-117:extension> <Entity X-117>
    <Field X-117:desc> <Entity X-117>

    >>> show_elements (f_PhP, "Entity.E_Type.type_name")
    <Entity X-117> PAP.Person_has_Phone
    <Field_Entity X-117:left> PAP.Person_has_Phone
    <Field_Entity X-117:right> PAP.Person_has_Phone
    <Field X-117:right.country_code> PAP.Phone
    <Field X-117:right.area_code> PAP.Phone
    <Field X-117:right.number> PAP.Phone
    <Field X-117:extension> PAP.Person_has_Phone
    <Field X-117:desc> PAP.Person_has_Phone

    >>> show_elements (f_PhP, "E_Type.type_name")
    <Entity X-117> PAP.Person_has_Phone
    <Field_Entity X-117:left> PAP.Person
    <Field_Entity X-117:right> PAP.Phone
    <Field X-117:right.country_code> PAP.Phone
    <Field X-117:right.area_code> PAP.Phone
    <Field X-117:right.number> PAP.Phone
    <Field X-117:extension> PAP.Person_has_Phone
    <Field X-117:desc> PAP.Person_has_Phone

    >>> show_elements (f_PhP, "attr.E_Type.type_name")
    <Entity X-117> ---
    <Field_Entity X-117:left> PAP.Person
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
    <Field_Entity X-117:right> <Entity X-117>
    <Field X-117:right.country_code> <Field_Entity X-117:right>
    <Field X-117:right.area_code> <Field_Entity X-117:right>
    <Field X-117:right.number> <Field_Entity X-117:right>
    <Field X-117:extension> <Entity X-117>
    <Field X-117:desc> <Entity X-117>

    >>> for e in f_PhP.entity_elements :
    ...     print (e)
    <Entity X-117>
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
    <Field_Entity X-117:right> mf3_input, id_entity
    <Field X-117:right.country_code> mf3_input, number
    <Field X-117:right.area_code> mf3_input, number
    <Field X-117:right.number> mf3_input, number
    <Field X-117:extension> mf3_input, number
    <Field X-117:desc> mf3_input, string

    >>> show_elements (f_PhP, "template_macro")
    <Entity X-117> Entity_Form
    <Field_Entity X-117:left> Field_Entity
    <Field_Entity X-117:right> Field_Entity
    <Field X-117:right.country_code> Field
    <Field X-117:right.area_code> Field
    <Field X-117:right.number> Field
    <Field X-117:extension> Field
    <Field X-117:desc> Field

    >>> show_elements (f_PhP, "cooked")
    <Entity X-117> ---
    <Field_Entity X-117:left> None
    <Field_Entity X-117:right> None
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code>
    <Field X-117:right.number>
    <Field X-117:extension>
    <Field X-117:desc>

    >>> show_elements (f_PhP, "edit")
    <Entity X-117> ---
    <Field_Entity X-117:left>
    <Field_Entity X-117:right>
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code>
    <Field X-117:right.number>
    <Field X-117:extension>
    <Field X-117:desc>

    >>> show_elements (f_PhP_s, "edit")
    <Entity Y-117> ---
    <Field_Entity Y-117:left>
    <Field_Entity Y-117:right>
    <Field Y-117:right.country_code> 49
    <Field Y-117:right.area_code>
    <Field Y-117:right.number>
    <Field Y-117:extension>
    <Field Y-117:desc>

    >>> show_elements (f_PhP_s, "prefilled")
    <Entity Y-117> ---
    <Field_Entity Y-117:left> False
    <Field_Entity Y-117:right> False
    <Field Y-117:right.country_code> 1
    <Field Y-117:right.area_code> False
    <Field Y-117:right.number> False
    <Field Y-117:extension> False
    <Field Y-117:desc> False

    >>> show_elements (f_pph, "cooked")
    <Entity X-117> ---
    <Field_Entity X-117:left> (u'tanzer', u'christian', u'', u'')
    <Field_Entity X-117:right> (u'43', u'1', u'98765432')
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code> 1
    <Field X-117:right.number> 98765432
    <Field X-117:extension> 42
    <Field X-117:desc> example

    >>> show_elements (f_pph, "edit")
    <Entity X-117> ---
    <Field_Entity X-117:left> 1
    <Field_Entity X-117:right> 2
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code> 1
    <Field X-117:right.number> 98765432
    <Field X-117:extension> 42
    <Field X-117:desc> example

    >>> show_elements (f_pph, "ui_display")
    <Entity X-117> Tanzer Christian, 43/1/98765432, 42
    <Field_Entity X-117:left> Tanzer Christian
    <Field_Entity X-117:right> 43/1/98765432
    <Field X-117:right.country_code> 43
    <Field X-117:right.area_code> 1
    <Field X-117:right.number> 98765432
    <Field X-117:extension> 42
    <Field X-117:desc> example

    >>> show_elements (f_pph, "essence")
    <Entity X-117> ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'98765432'), u'42')
    <Field_Entity X-117:left> (u'tanzer', u'christian', u'', u'')
    <Field_Entity X-117:right> (u'43', u'1', u'98765432')
    <Field X-117:right.country_code> (u'43', u'1', u'98765432')
    <Field X-117:right.area_code> (u'43', u'1', u'98765432')
    <Field X-117:right.number> (u'43', u'1', u'98765432')
    <Field X-117:extension> ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'98765432'), u'42')
    <Field X-117:desc> ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'98765432'), u'42')

    >>> show_elements (f_pph, "q_name")
    <Entity X-117> None
    <Field_Entity X-117:left> left
    <Field_Entity X-117:right> right
    <Field X-117:right.country_code> right.country_code
    <Field X-117:right.area_code> right.area_code
    <Field X-117:right.number> right.number
    <Field X-117:extension> extension
    <Field X-117:desc> desc

    >>> show_elements (f_pph, "prefilled")
    <Entity X-117> ---
    <Field_Entity X-117:left> False
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
            , 'display' : 'Tanzer Christian'
            , 'pid' : 1
            }
        }
    , 'X-117:right' :
        { 'init' :
            { 'cid' : 2
            , 'display' : '43/1/98765432'
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
    , 'Z-117:left.first_name' :
        {}
    , 'Z-117:left.last_name' :
        {}
    , 'Z-117:left.lifetime.finish' :
        {}
    , 'Z-117:left.lifetime.start' :
        {}
    , 'Z-117:left.middle_name' :
        {}
    , 'Z-117:left.sex' :
        {}
    , 'Z-117:left.title' :
        {}
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

    >>> set (x.id for x in F_PhP.elements_transitive ()) >= set (x.id for x in f_PhP.elements_transitive ())
    True

    >>> list (x.id for x in f_pph.elements_transitive ()) == list (x.id for x in f_PhP.elements_transitive ())
    True

    >>> SRM     = scope.SRM
    >>> F_BiR   = MF3_E.Entity.Auto (scope.SRM.Boat_in_Regatta, id_prefix = "R")
    >>> f_bir   = F_BiR (scope, attr_spec = { "right" : dict (allow_new = True) })
    >>> f_bir_n = F_BiR (scope)

    >>> show_elements_x (f_bir,   "id", "allow_new", filter = (Q.allow_new != None))
    Type    id                      allow_new
    ======================================
    F_E     R-105:left              True
    F_E     R-105:left.left         True
    F_E     R-105:right             True
    F_E     R-105:right.left        True
    F_E     R-105:right.boat_class  True
    F_E     R-105:skipper           True
    F_E     R-105:skipper.left      True
    F_E     R-105:skipper.club      True

    >>> show_elements_x (f_bir_n, "id", "allow_new", filter = (Q.allow_new != None))
    Type    id                  allow_new
    ===================================
    F_E     R-105:left          True
    F_E     R-105:left.left     True
    F_E     R-105:right         False
    F_E     R-105:skipper       True
    F_E     R-105:skipper.left  True
    F_E     R-105:skipper.club  True

    >>> show_elements_x (f_bir, "id", "Entity.id")
    Type    id                              Entity.id
    ================================================================
    E       R-105                           R-105
    F_E     R-105:left                      R-105
    F_E     R-105:left.left                 R-105:left
    F       R-105:left.left.name            R-105:left.left
    F       R-105:left.left.max_crew        R-105:left.left
    F       R-105:left.sail_number          R-105:left
    F       R-105:left.nation               R-105:left
    F       R-105:left.sail_number_x        R-105:left
    F_E     R-105:right                     R-105
    F_E     R-105:right.left                R-105:right
    F       R-105:right.left.name           R-105:right.left
    F_C     R-105:right.left.date           R-105:right.left
    F       R-105:right.left.date.start     R-105:right.left
    F       R-105:right.left.date.finish    R-105:right.left
    F_E     R-105:right.boat_class          R-105:right
    F       R-105:right.boat_class.name     R-105:right.boat_class
    F_E     R-105:skipper                   R-105
    F_E     R-105:skipper.left              R-105:skipper
    F       R-105:skipper.left.last_name    R-105:skipper.left
    F       R-105:skipper.left.first_name   R-105:skipper.left
    F       R-105:skipper.left.middle_name  R-105:skipper.left
    F       R-105:skipper.left.title        R-105:skipper.left
    F       R-105:skipper.nation            R-105:skipper
    F       R-105:skipper.mna_number        R-105:skipper
    F_E     R-105:skipper.club              R-105:skipper
    F       R-105:skipper.club.name         R-105:skipper.club
    F       R-105:place                     R-105
    F       R-105:points                    R-105

    >>> show_elements_x (f_bir, "q_name", "r_name", "E_Type.type_name")
    Type    q_name                    r_name         E_Type.type_name
    ======================================================================
    E       None                      None           SRM.Boat_in_Regatta
    F_E     left                      left           SRM.Boat
    F_E     left.left                 left           SRM.Boat_Class
    F       left.left.name            name           SRM.Boat_Class
    F       left.left.max_crew        max_crew       SRM.Boat_Class
    F       left.sail_number          sail_number    SRM.Boat
    F       left.nation               nation         SRM.Boat
    F       left.sail_number_x        sail_number_x  SRM.Boat
    F_E     right                     right          SRM.Regatta
    F_E     right.left                left           SRM.Regatta_Event
    F       right.left.name           name           SRM.Regatta_Event
    F_C     right.left.date           date           MOM.Date_Interval_C
    F       right.left.date.start     date.start     MOM.Date_Interval_C
    F       right.left.date.finish    date.finish    MOM.Date_Interval_C
    F_E     right.boat_class          boat_class     SRM._Boat_Class_
    F       right.boat_class.name     name           SRM._Boat_Class_
    F_E     skipper                   skipper        SRM.Sailor
    F_E     skipper.left              left           PAP.Person
    F       skipper.left.last_name    last_name      PAP.Person
    F       skipper.left.first_name   first_name     PAP.Person
    F       skipper.left.middle_name  middle_name    PAP.Person
    F       skipper.left.title        title          PAP.Person
    F       skipper.nation            nation         SRM.Sailor
    F       skipper.mna_number        mna_number     SRM.Sailor
    F_E     skipper.club              club           SRM.Club
    F       skipper.club.name         name           SRM.Club
    F       place                     place          SRM.Boat_in_Regatta
    F       points                    points         SRM.Boat_in_Regatta

    >>> show_elements_x (f_bir, "attr.e_type.type_name", "parent.E_Type.type_name")
    Type    attr.e_type.type_name  parent.E_Type.type_name
    ==================================================
    E       None                 None
    F_E     SRM.Boat_in_Regatta  SRM.Boat_in_Regatta
    F_E     SRM.Boat             SRM.Boat
    F       SRM.Boat_Class       SRM.Boat_Class
    F       SRM.Boat_Class       SRM.Boat_Class
    F       SRM.Boat             SRM.Boat
    F       SRM.Boat             SRM.Boat
    F       SRM.Boat             SRM.Boat
    F_E     SRM.Boat_in_Regatta  SRM.Boat_in_Regatta
    F_E     SRM.Regatta          SRM.Regatta
    F       SRM.Regatta_Event    SRM.Regatta_Event
    F_C     SRM.Regatta_Event    SRM.Regatta_Event
    F       MOM.Date_Interval    MOM.Date_Interval_C
    F       MOM.Date_Interval_C  MOM.Date_Interval_C
    F_E     SRM.Regatta          SRM.Regatta
    F       SRM._Boat_Class_     SRM._Boat_Class_
    F_E     SRM.Boat_in_Regatta  SRM.Boat_in_Regatta
    F_E     SRM.Sailor           SRM.Sailor
    F       PAP.Person           PAP.Person
    F       PAP.Person           PAP.Person
    F       PAP.Person           PAP.Person
    F       PAP.Person           PAP.Person
    F       SRM.Sailor           SRM.Sailor
    F       SRM.Sailor           SRM.Sailor
    F_E     SRM.Sailor           SRM.Sailor
    F       SRM.Club             SRM.Club
    F       SRM.Boat_in_Regatta  SRM.Boat_in_Regatta
    F       SRM.Boat_in_Regatta  SRM.Boat_in_Regatta

    >>> show_completers (f_bir, "q_name", "attr.completer.kind")
    Type    q_name                    attr.completer.kind
    =============================================
    F       left.left.name            Atom
    F       left.sail_number          Atom
    F       left.sail_number_x        Atom
    F       right.left.name           Atom
    F_C     right.left.date           Composite
    F       right.left.date.start     Atom
    F       right.left.date.finish    Atom
    F       right.boat_class.name     Atom
    F_E     skipper.left              Id_Entity
    F       skipper.left.last_name    Atom
    F       skipper.left.first_name   Atom
    F       skipper.left.middle_name  Atom
    F       skipper.left.title        Atom
    F       skipper.mna_number        Atom
    F_E     skipper.club              Id_Entity
    F       skipper.club.name         Atom

    >>> show_completers (f_bir, "q_name", "attr.completer.as_json_cargo")
    Type    q_name                    attr.completer.as_json_cargo
    ==============================================================================================================================
    F       left.left.name            entity_p = True, names = ['name'], treshold = 1
    F       left.sail_number          entity_p = True, names = ['sail_number', 'left', 'nation', 'sail_number_x'], treshold = 1
    F       left.sail_number_x        entity_p = True, names = ['sail_number_x', 'left', 'sail_number', 'nation'], treshold = 1
    F       right.left.name           entity_p = True, names = ['name', 'date'], treshold = 1
    F_C     right.left.date           entity_p = True, names = ['date', 'name'], treshold = 1
    F       right.left.date.start     entity_p = False, names = ['start'], treshold = 4
    F       right.left.date.finish    entity_p = False, names = ['finish'], treshold = 4
    F       right.boat_class.name     entity_p = True, names = ['name'], treshold = 1
    F_E     skipper.left              entity_p = True, names = ['left', 'nation', 'mna_number', 'club'], treshold = 1
    F       skipper.left.last_name    entity_p = True, names = ['last_name', 'first_name', 'middle_name', 'title'], treshold = 2
    F       skipper.left.first_name   entity_p = True, names = ['first_name', 'last_name', 'middle_name', 'title'], treshold = 2
    F       skipper.left.middle_name  entity_p = True, names = ['middle_name', 'last_name', 'first_name', 'title'], treshold = 2
    F       skipper.left.title        entity_p = False, names = ['title'], treshold = 1
    F       skipper.mna_number        entity_p = True, names = ['mna_number', 'left', 'nation', 'club'], treshold = 1
    F_E     skipper.club              entity_p = True, names = ['club', 'left', 'nation', 'mna_number'], treshold = 1
    F       skipper.club.name         entity_p = True, names = ['name'], treshold = 1

    >>> show_completers (f_bir, "q_name", "completer.id", "completer.as_json_cargo")
    Type    q_name                    completer.id  completer.as_json_cargo
    ======================================================================================================================================================================================================================================================================================================================
    F       left.left.name            0     entity_p = True, fields = ['R-105:left.left.name'], treshold = 1
    F       left.sail_number          1     entity_p = True, fields = ['R-105:left.left', 'R-105:left.nation', 'R-105:left.sail_number', 'R-105:left.sail_number_x'], treshold = 1
    F       left.sail_number_x        1     entity_p = True, fields = ['R-105:left.left', 'R-105:left.nation', 'R-105:left.sail_number', 'R-105:left.sail_number_x'], treshold = 1
    F       right.left.name           2     entity_p = True, fields = ['R-105:right.left.date.finish', 'R-105:right.left.date.start', 'R-105:right.left.name'], treshold = 1
    F_C     right.left.date           None  entity_p = True, fields = ['R-105:right.left.date.finish', 'R-105:right.left.date.start', 'R-105:right.left.name'], treshold = 1
    F       right.left.date.start     3     entity_p = False, fields = ['R-105:right.left.date.start'], treshold = 4
    F       right.left.date.finish    4     entity_p = False, fields = ['R-105:right.left.date.finish'], treshold = 4
    F       right.boat_class.name     5     entity_p = True, fields = ['R-105:right.boat_class.name'], treshold = 1
    F_E     skipper.left              6     entity_p = True, fields = ['R-105:skipper.club.name', 'R-105:skipper.left', 'R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.mna_number', 'R-105:skipper.nation'], treshold = 1
    F       skipper.left.last_name    7     entity_p = True, fields = ['R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title'], treshold = 2
    F       skipper.left.first_name   7     entity_p = True, fields = ['R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title'], treshold = 2
    F       skipper.left.middle_name  7     entity_p = True, fields = ['R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title'], treshold = 2
    F       skipper.left.title        8     entity_p = False, fields = ['R-105:skipper.left.title'], treshold = 1
    F       skipper.mna_number        9     entity_p = True, fields = ['R-105:skipper.club.name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.mna_number', 'R-105:skipper.nation'], treshold = 1
    F_E     skipper.club              10    entity_p = True, fields = ['R-105:skipper.club', 'R-105:skipper.club.name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.mna_number', 'R-105:skipper.nation'], treshold = 1
    F       skipper.club.name         11    entity_p = True, fields = ['R-105:skipper.club.name'], treshold = 1

    >>> show_completers (f_bir, "q_name", "completer.id", "completer.sig")
    Type    q_name                    completer.id  completer.sig
    =========================================================================================================================================================================================================================================================================================
    F       left.left.name            0     (('R-105:left.left.name',), 1, True)
    F       left.sail_number          1     (('R-105:left.left', 'R-105:left.nation', 'R-105:left.sail_number', 'R-105:left.sail_number_x'), 1, True)
    F       left.sail_number_x        1     (('R-105:left.left', 'R-105:left.nation', 'R-105:left.sail_number', 'R-105:left.sail_number_x'), 1, True)
    F       right.left.name           2     (('R-105:right.left.date.finish', 'R-105:right.left.date.start', 'R-105:right.left.name'), 1, True)
    F_C     right.left.date           None  (('R-105:right.left.date.finish', 'R-105:right.left.date.start', 'R-105:right.left.name'), 1, True)
    F       right.left.date.start     3     (('R-105:right.left.date.start',), 4, False)
    F       right.left.date.finish    4     (('R-105:right.left.date.finish',), 4, False)
    F       right.boat_class.name     5     (('R-105:right.boat_class.name',), 1, True)
    F_E     skipper.left              6     (('R-105:skipper.club.name', 'R-105:skipper.left', 'R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.mna_number', 'R-105:skipper.nation'), 1, True)
    F       skipper.left.last_name    7     (('R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title'), 2, True)
    F       skipper.left.first_name   7     (('R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title'), 2, True)
    F       skipper.left.middle_name  7     (('R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title'), 2, True)
    F       skipper.left.title        8     (('R-105:skipper.left.title',), 1, False)
    F       skipper.mna_number        9     (('R-105:skipper.club.name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.mna_number', 'R-105:skipper.nation'), 1, True)
    F_E     skipper.club              10    (('R-105:skipper.club', 'R-105:skipper.club.name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.mna_number', 'R-105:skipper.nation'), 1, True)
    F       skipper.club.name         11    (('R-105:skipper.club.name',), 1, True)

    >>> show_completers_js (f_bir)
    { 0 :
        { 'entity_p' : True
        , 'fields' : [ 'R-105:left.left.name' ]
        , 'treshold' : 1
        }
    , 1 :
        { 'entity_p' : True
        , 'fields' :
            [ 'R-105:left.left'
            , 'R-105:left.nation'
            , 'R-105:left.sail_number'
            , 'R-105:left.sail_number_x'
            ]
        , 'treshold' : 1
        }
    , 2 :
        { 'entity_p' : True
        , 'fields' :
            [ 'R-105:right.left.date.finish'
            , 'R-105:right.left.date.start'
            , 'R-105:right.left.name'
            ]
        , 'treshold' : 1
        }
    , 3 :
        { 'entity_p' : False
        , 'fields' : [ 'R-105:right.left.date.start' ]
        , 'treshold' : 4
        }
    , 4 :
        { 'entity_p' : False
        , 'fields' : [ 'R-105:right.left.date.finish' ]
        , 'treshold' : 4
        }
    , 5 :
        { 'entity_p' : True
        , 'fields' : [ 'R-105:right.boat_class.name' ]
        , 'treshold' : 1
        }
    , 6 :
        { 'entity_p' : True
        , 'fields' :
            [ 'R-105:skipper.club.name'
            , 'R-105:skipper.left'
            , 'R-105:skipper.left.first_name'
            , 'R-105:skipper.left.last_name'
            , 'R-105:skipper.left.middle_name'
            , 'R-105:skipper.left.title'
            , 'R-105:skipper.mna_number'
            , 'R-105:skipper.nation'
            ]
        , 'treshold' : 1
        }
    , 7 :
        { 'entity_p' : True
        , 'fields' :
            [ 'R-105:skipper.left.first_name'
            , 'R-105:skipper.left.last_name'
            , 'R-105:skipper.left.middle_name'
            , 'R-105:skipper.left.title'
            ]
        , 'treshold' : 2
        }
    , 8 :
        { 'entity_p' : False
        , 'fields' : [ 'R-105:skipper.left.title' ]
        , 'treshold' : 1
        }
    , 9 :
        { 'entity_p' : True
        , 'fields' :
            [ 'R-105:skipper.club.name'
            , 'R-105:skipper.left.first_name'
            , 'R-105:skipper.left.last_name'
            , 'R-105:skipper.left.middle_name'
            , 'R-105:skipper.left.title'
            , 'R-105:skipper.mna_number'
            , 'R-105:skipper.nation'
            ]
        , 'treshold' : 1
        }
    , 10 :
        { 'entity_p' : True
        , 'fields' :
            [ 'R-105:skipper.club'
            , 'R-105:skipper.club.name'
            , 'R-105:skipper.left.first_name'
            , 'R-105:skipper.left.last_name'
            , 'R-105:skipper.left.middle_name'
            , 'R-105:skipper.left.title'
            , 'R-105:skipper.mna_number'
            , 'R-105:skipper.nation'
            ]
        , 'treshold' : 1
        }
    , 11 :
        { 'entity_p' : True
        , 'fields' : [ 'R-105:skipper.club.name' ]
        , 'treshold' : 1
        }
    }


    >>> show_completers (f_bir, "q_name", "completer.entity_p")
    Type    q_name                    completer.entity_p
    =========================================
    F       left.left.name            True
    F       left.sail_number          True
    F       left.sail_number_x        True
    F       right.left.name           True
    F_C     right.left.date           True
    F       right.left.date.start     False
    F       right.left.date.finish    False
    F       right.boat_class.name     True
    F_E     skipper.left              True
    F       skipper.left.last_name    True
    F       skipper.left.first_name   True
    F       skipper.left.middle_name  True
    F       skipper.left.title        False
    F       skipper.mna_number        True
    F_E     skipper.club              True
    F       skipper.club.name         True

    >>> show_completers (f_bir, "q_name", "completer.anchor")
    Type    q_name                    completer.anchor
    =========================================================================
    F       left.left.name            <Field_Entity R-105:left.left>
    F       left.sail_number          <Field_Entity R-105:left>
    F       left.sail_number_x        <Field_Entity R-105:left>
    F       right.left.name           <Field_Entity R-105:right.left>
    F_C     right.left.date           <Field_Entity R-105:right.left>
    F       right.left.date.start     <Field_Entity R-105:right.left>
    F       right.left.date.finish    <Field_Entity R-105:right.left>
    F       right.boat_class.name     <Field_Entity R-105:right.boat_class>
    F_E     skipper.left              <Field_Entity R-105:skipper>
    F       skipper.left.last_name    <Field_Entity R-105:skipper>
    F       skipper.left.first_name   <Field_Entity R-105:skipper>
    F       skipper.left.middle_name  <Field_Entity R-105:skipper>
    F       skipper.left.title        <Field_Entity R-105:skipper.left>
    F       skipper.mna_number        <Field_Entity R-105:skipper>
    F_E     skipper.club              <Field_Entity R-105:skipper>
    F       skipper.club.name         <Field_Entity R-105:skipper>

    >>> show_completers (f_bir, "q_name", "completer.field_ids")
    Type    q_name                    completer.field_ids
    ==================================================================================================================================================================================================================================================
    F       left.left.name            ('R-105:left.left.name',)
    F       left.sail_number          ('R-105:left.sail_number', 'R-105:left.left', 'R-105:left.nation', 'R-105:left.sail_number_x')
    F       left.sail_number_x        ('R-105:left.sail_number_x', 'R-105:left.left', 'R-105:left.sail_number', 'R-105:left.nation')
    F       right.left.name           ('R-105:right.left.name', 'R-105:right.left.date.start', 'R-105:right.left.date.finish')
    F_C     right.left.date           ('R-105:right.left.date.start', 'R-105:right.left.date.finish', 'R-105:right.left.name')
    F       right.left.date.start     ('R-105:right.left.date.start',)
    F       right.left.date.finish    ('R-105:right.left.date.finish',)
    F       right.boat_class.name     ('R-105:right.boat_class.name',)
    F_E     skipper.left              ('R-105:skipper.left.last_name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.nation', 'R-105:skipper.mna_number', 'R-105:skipper.club.name')
    F       skipper.left.last_name    ('R-105:skipper.left.last_name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title')
    F       skipper.left.first_name   ('R-105:skipper.left.first_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title')
    F       skipper.left.middle_name  ('R-105:skipper.left.middle_name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.title')
    F       skipper.left.title        ('R-105:skipper.left.title',)
    F       skipper.mna_number        ('R-105:skipper.mna_number', 'R-105:skipper.left.last_name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.nation', 'R-105:skipper.club.name')
    F_E     skipper.club              ('R-105:skipper.club.name', 'R-105:skipper.left.last_name', 'R-105:skipper.left.first_name', 'R-105:skipper.left.middle_name', 'R-105:skipper.left.title', 'R-105:skipper.nation', 'R-105:skipper.mna_number')
    F       skipper.club.name         ('R-105:skipper.club.name',)

    >>> show_completers (f_bir, "q_name", "completer.etn", "completer.attr_names")
    Type    q_name                    completer.etn      completer.attr_names
    ===================================================================================================================================================================
    F       left.left.name            SRM.Boat_Class     ('name',)
    F       left.sail_number          SRM.Boat           ('sail_number', 'left', 'nation', 'sail_number_x')
    F       left.sail_number_x        SRM.Boat           ('sail_number_x', 'left', 'sail_number', 'nation')
    F       right.left.name           SRM.Regatta_Event  ('name', 'date.start', 'date.finish')
    F_C     right.left.date           SRM.Regatta_Event  ('date.start', 'date.finish', 'name')
    F       right.left.date.start     SRM.Regatta_Event  ('date.start',)
    F       right.left.date.finish    SRM.Regatta_Event  ('date.finish',)
    F       right.boat_class.name     SRM._Boat_Class_   ('name',)
    F_E     skipper.left              SRM.Sailor         ('left.last_name', 'left.first_name', 'left.middle_name', 'left.title', 'nation', 'mna_number', 'club.name')
    F       skipper.left.last_name    SRM.Sailor         ('left.last_name', 'left.first_name', 'left.middle_name', 'left.title')
    F       skipper.left.first_name   SRM.Sailor         ('left.first_name', 'left.last_name', 'left.middle_name', 'left.title')
    F       skipper.left.middle_name  SRM.Sailor         ('left.middle_name', 'left.last_name', 'left.first_name', 'left.title')
    F       skipper.left.title        PAP.Person         ('title',)
    F       skipper.mna_number        SRM.Sailor         ('mna_number', 'left.last_name', 'left.first_name', 'left.middle_name', 'left.title', 'nation', 'club.name')
    F_E     skipper.club              SRM.Sailor         ('club.name', 'left.last_name', 'left.first_name', 'left.middle_name', 'left.title', 'nation', 'mna_number')
    F       skipper.club.name         SRM.Sailor         ('club.name',)

    >>> show_elements_x (f_p, "q_name", "completer.id", "completer.as_json_cargo")
    Type    q_name           completer.id  completer.as_json_cargo
    ================================================================================================================================================
    E       None             None  None
    F       last_name        0     entity_p = True, fields = ['X-24:first_name', 'X-24:last_name', 'X-24:middle_name', 'X-24:title'], treshold = 2
    F       first_name       0     entity_p = True, fields = ['X-24:first_name', 'X-24:last_name', 'X-24:middle_name', 'X-24:title'], treshold = 2
    F       middle_name      0     entity_p = True, fields = ['X-24:first_name', 'X-24:last_name', 'X-24:middle_name', 'X-24:title'], treshold = 2
    F       title            1     entity_p = False, fields = ['X-24:title'], treshold = 1
    F_C     lifetime         None  None
    F       lifetime.start   2     entity_p = False, fields = ['X-24:lifetime.start'], treshold = 4
    F       lifetime.finish  3     entity_p = False, fields = ['X-24:lifetime.finish'], treshold = 4
    F       sex              None  None

    >>> show_elements_x (f_p, "q_name", "completer.id", "completer.sig")
    Type    q_name           completer.id  completer.sig
    ===================================================================================================================
    E       None             None  None
    F       last_name        0     (('X-24:first_name', 'X-24:last_name', 'X-24:middle_name', 'X-24:title'), 2, True)
    F       first_name       0     (('X-24:first_name', 'X-24:last_name', 'X-24:middle_name', 'X-24:title'), 2, True)
    F       middle_name      0     (('X-24:first_name', 'X-24:last_name', 'X-24:middle_name', 'X-24:title'), 2, True)
    F       title            1     (('X-24:title',), 1, False)
    F_C     lifetime         None  None
    F       lifetime.start   2     (('X-24:lifetime.start',), 4, False)
    F       lifetime.finish  3     (('X-24:lifetime.finish',), 4, False)
    F       sex              None  None

    >>> show_completers (f_p, "q_name", "completer.name", "completer.entity_p")
    Type   q_name           completer.name   completer.entity_p
    ================================================
    F      last_name        last_name        True
    F      first_name       first_name       True
    F      middle_name      middle_name      True
    F      title            title            False
    F      lifetime.start   lifetime.start   False
    F      lifetime.finish  lifetime.finish  False

    >>> show_completers (f_p, "q_name", "completer.anchor")
    Type   q_name           completer.anchor
    =======================================
    F      last_name        <Entity X-24>
    F      first_name       <Entity X-24>
    F      middle_name      <Entity X-24>
    F      title            <Entity X-24>
    F      lifetime.start   <Entity X-24>
    F      lifetime.finish  <Entity X-24>

    >>> show_completers (f_p, "q_name", "completer.field_ids")
    Type   q_name           completer.field_ids
    =================================================================================================
    F      last_name        ('X-24:last_name', 'X-24:first_name', 'X-24:middle_name', 'X-24:title')
    F      first_name       ('X-24:first_name', 'X-24:last_name', 'X-24:middle_name', 'X-24:title')
    F      middle_name      ('X-24:middle_name', 'X-24:last_name', 'X-24:first_name', 'X-24:title')
    F      title            ('X-24:title',)
    F      lifetime.start   ('X-24:lifetime.start',)
    F      lifetime.finish  ('X-24:lifetime.finish',)

    >>> show_completers (f_p, "q_name", "completer.etn", "completer.attr_names")
    Type   q_name           completer.etn  completer.attr_names
    =========================================================================================
    F      last_name        PAP.Person  ('last_name', 'first_name', 'middle_name', 'title')
    F      first_name       PAP.Person  ('first_name', 'last_name', 'middle_name', 'title')
    F      middle_name      PAP.Person  ('middle_name', 'last_name', 'first_name', 'title')
    F      title            PAP.Person  ('title',)
    F      lifetime.start   PAP.Person  ('lifetime.start',)
    F      lifetime.finish  PAP.Person  ('lifetime.finish',)

    >>> show_completers_js (f_p)
    { 0 :
        { 'entity_p' : True
        , 'fields' :
            [ 'X-24:first_name'
            , 'X-24:last_name'
            , 'X-24:middle_name'
            , 'X-24:title'
            ]
        , 'treshold' : 2
        }
    , 1 :
        { 'entity_p' : False
        , 'fields' : [ 'X-24:title' ]
        , 'treshold' : 1
        }
    , 2 :
        { 'entity_p' : False
        , 'fields' : [ 'X-24:lifetime.start' ]
        , 'treshold' : 4
        }
    , 3 :
        { 'entity_p' : False
        , 'fields' : [ 'X-24:lifetime.finish' ]
        , 'treshold' : 4
        }
    }


    >>> show_elements_x (f_bir, "q_name", "field_elements")
    Type    q_name                    field_elements
    ===========================================================================================================================================================================================
    E       None                      (<Field_Entity R-105:left>, <Field_Entity R-105:right>, <Field_Entity R-105:skipper>, <Field R-105:place>, <Field R-105:points>)
    F_E     left                      (<Field_Entity R-105:left.left>, <Field R-105:left.sail_number>, <Field R-105:left.nation>, <Field R-105:left.sail_number_x>)
    F_E     left.left                 (<Field R-105:left.left.name>, <Field R-105:left.left.max_crew>)
    F       left.left.name            ()
    F       left.left.max_crew        ()
    F       left.sail_number          ()
    F       left.nation               ()
    F       left.sail_number_x        ()
    F_E     right                     (<Field_Entity R-105:right.left>, <Field_Entity R-105:right.boat_class>)
    F_E     right.left                (<Field R-105:right.left.name>, <Field R-105:right.left.date.start>, <Field R-105:right.left.date.finish>)
    F       right.left.name           ()
    F_C     right.left.date           (<Field R-105:right.left.date.start>, <Field R-105:right.left.date.finish>)
    F       right.left.date.start     ()
    F       right.left.date.finish    ()
    F_E     right.boat_class          (<Field R-105:right.boat_class.name>,)
    F       right.boat_class.name     ()
    F_E     skipper                   (<Field_Entity R-105:skipper.left>, <Field R-105:skipper.nation>, <Field R-105:skipper.mna_number>, <Field_Entity R-105:skipper.club>)
    F_E     skipper.left              (<Field R-105:skipper.left.last_name>, <Field R-105:skipper.left.first_name>, <Field R-105:skipper.left.middle_name>, <Field R-105:skipper.left.title>)
    F       skipper.left.last_name    ()
    F       skipper.left.first_name   ()
    F       skipper.left.middle_name  ()
    F       skipper.left.title        ()
    F       skipper.nation            ()
    F       skipper.mna_number        ()
    F_E     skipper.club              (<Field R-105:skipper.club.name>,)
    F       skipper.club.name         ()
    F       place                     ()
    F       points                    ()

    >>> show_elements_x (f_p, "q_name", "field_elements")
    Type    q_name           field_elements
    =======================================================================================================================================================================================================
    E       None             (<Field X-24:last_name>, <Field X-24:first_name>, <Field X-24:middle_name>, <Field X-24:title>, <Field X-24:lifetime.start>, <Field X-24:lifetime.finish>, <Field X-24:sex>)
    F       last_name        ()
    F       first_name       ()
    F       middle_name      ()
    F       title            ()
    F_C     lifetime         (<Field X-24:lifetime.start>, <Field X-24:lifetime.finish>)
    F       lifetime.start   ()
    F       lifetime.finish  ()
    F       sex              ()


    >>> show_completers (f_bir, "q_name", "completer.own_elems")
    Type    q_name                    completer.own_elems
    ============================================================================================================================================================================================================================================================================================
    F       left.left.name            (<Field R-105:left.left.name>,)
    F       left.sail_number          (<Field R-105:left.sail_number>, <Field_Entity R-105:left.left>, <Field R-105:left.nation>, <Field R-105:left.sail_number_x>)
    F       left.sail_number_x        (<Field R-105:left.sail_number_x>, <Field_Entity R-105:left.left>, <Field R-105:left.sail_number>, <Field R-105:left.nation>)
    F       right.left.name           (<Field R-105:right.left.name>, <Field R-105:right.left.date.start>, <Field R-105:right.left.date.finish>)
    F_C     right.left.date           (<Field R-105:right.left.date.start>, <Field R-105:right.left.date.finish>, <Field R-105:right.left.name>, <Field R-105:right.left.date.start>, <Field R-105:right.left.date.finish>)
    F       right.left.date.start     (<Field R-105:right.left.date.start>,)
    F       right.left.date.finish    (<Field R-105:right.left.date.finish>,)
    F       right.boat_class.name     (<Field R-105:right.boat_class.name>,)
    F_E     skipper.left              (<Field R-105:skipper.left.last_name>, <Field R-105:skipper.left.first_name>, <Field R-105:skipper.left.middle_name>, <Field R-105:skipper.left.title>, <Field R-105:skipper.nation>, <Field R-105:skipper.mna_number>, <Field R-105:skipper.club.name>)
    F       skipper.left.last_name    (<Field R-105:skipper.left.last_name>, <Field R-105:skipper.left.first_name>, <Field R-105:skipper.left.middle_name>, <Field R-105:skipper.left.title>)
    F       skipper.left.first_name   (<Field R-105:skipper.left.first_name>, <Field R-105:skipper.left.last_name>, <Field R-105:skipper.left.middle_name>, <Field R-105:skipper.left.title>)
    F       skipper.left.middle_name  (<Field R-105:skipper.left.middle_name>, <Field R-105:skipper.left.last_name>, <Field R-105:skipper.left.first_name>, <Field R-105:skipper.left.title>)
    F       skipper.left.title        (<Field R-105:skipper.left.title>,)
    F       skipper.mna_number        (<Field R-105:skipper.mna_number>, <Field R-105:skipper.left.last_name>, <Field R-105:skipper.left.first_name>, <Field R-105:skipper.left.middle_name>, <Field R-105:skipper.left.title>, <Field R-105:skipper.nation>, <Field R-105:skipper.club.name>)
    F_E     skipper.club              (<Field R-105:skipper.club.name>, <Field R-105:skipper.left.last_name>, <Field R-105:skipper.left.first_name>, <Field R-105:skipper.left.middle_name>, <Field R-105:skipper.left.title>, <Field R-105:skipper.nation>, <Field R-105:skipper.mna_number>)
    F       skipper.club.name         (<Field R-105:skipper.club.name>,)

    >>> show_completers (f_p, "q_name", "completer.own_elems")
    Type   q_name           completer.own_elems
    =========================================================================================================================
    F      last_name        (<Field X-24:last_name>, <Field X-24:first_name>, <Field X-24:middle_name>, <Field X-24:title>)
    F      first_name       (<Field X-24:first_name>, <Field X-24:last_name>, <Field X-24:middle_name>, <Field X-24:title>)
    F      middle_name      (<Field X-24:middle_name>, <Field X-24:last_name>, <Field X-24:first_name>, <Field X-24:title>)
    F      title            (<Field X-24:title>,)
    F      lifetime.start   (<Field X-24:lifetime.start>,)
    F      lifetime.finish  (<Field X-24:lifetime.finish>,)



"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( element = _test_element
        )
    )

### __END__ GTW.__test__.MF3
