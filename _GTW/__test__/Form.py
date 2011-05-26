# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.__test__.Form
#
# Purpose
#    Some additional form tests
#
# Revision Dates
#    29-Apr-2010 (MG) Creation
#    ««revision-date»»···
#--

r"""
    >>> scope = Scaffold.scope ()
    Creating new scope MOMT__Hash__HPS in memory
    >>> form_cls = Person_Form (scope)
    >>> for sf in sorted (form_cls.sub_forms.iteritems ()) : print sf
    ('Person_has_Address', <class '_GTW._Form._MOM.Inline_Instance.Link_Inline_Instance_Person__Person_has_Address'>)
    ('Person_has_Email', <class '_GTW._Form._MOM.Inline_Instance.Link_Inline_Instance_Person__Person_has_Email'>)
    ('Person_has_Phone', <class '_GTW._Form._MOM.Inline_Instance.Link_Inline_Instance_Person__Person_has_Phone'>)
    ('lifetime', <class '_GTW._Form._MOM.Inline_Instance.An_Attribute_Inline_Instance_Person__Date_Interval'>)
    >>> form = form_cls ("/post/")
    >>> form.form_name
    'Person'
    >>> [il.form_cls.form_name for il in form.inline_groups]
    ['Person__Person_has_Phone', 'Person__Person_has_Email', 'Person__Person_has_Address']
    >>> for l in form.Media.js_on_ready : print l
    /* setup form `GTW_OMP_PAP_Person` */
    <BLANKLINE>
    $(".GTW_OMP_PAP_Person").GTW_Form
    <BLANKLINE>
      ( {"inlines": [{"buttons": ["rename", "delete", "clear"], "prefix": "Person__Person_has_Phone", "popup": true, "initial_disabled": true, "type": "Link_Inline_UI_Display", "instance_class": "inline-instance"}, {"buttons": ["rename", "delete", "clear"], "prefix": "Person__Person_has_Email", "popup": true, "initial_disabled": true, "type": "Link_Inline_UI_Display", "instance_class": "inline-instance"}, {"buttons": ["rename", "delete", "clear"], "instance_class": "inline-instance", "initial_disabled": true, "type": "Attribute_Inline", "prefix": "Person__Person_has_Address__address"}, {"buttons": ["rename", "delete", "clear"], "prefix": "Person__Person_has_Address", "popup": false, "initial_disabled": true, "type": "Link_Inline_UI_Display", "instance_class": "inline-instance"}], "completers": [{"suggest_url": "/Admin/Person/complete/last_name", "field_prefix": "Person", "triggers": {"last_name": {"fields": ["last_name"], "min_chars": 2}}, "complete_url": "/Admin/Person/completed/last_name", "type": "Field_Completer", "field_postfix": ""}, {"suggest_url": "/Admin/Person/complete/Person_has_Address__address", "field_prefix": "Person__Person_has_Address", "triggers": {"street": {"fields": ["street", "city", "zip", "country"], "min_chars": 3}}, "complete_url": "/Admin/Person/completed/Person_has_Address__address", "type": "Completer", "field_postfix": "address"}, {"suggest_url": "/Admin/Person/complete/Person_has_Address__address__city", "field_prefix": "Person__Person_has_Address", "triggers": {"city": {"fields": ["city", "country", "region"], "min_chars": 2}}, "complete_url": "/Admin/Person/completed/Person_has_Address__address__city", "type": "Field_Completer", "field_postfix": "address"}, {"suggest_url": "/Admin/Person/complete/Person_has_Address__address__zip", "field_prefix": "Person__Person_has_Address", "triggers": {"zip": {"fields": ["zip", "city", "country", "region"], "min_chars": 1}}, "complete_url": "/Admin/Person/completed/Person_has_Address__address__zip", "type": "Field_Completer", "field_postfix": "address"}]}
      );
    <BLANKLINE>
"""

from   _GTW.__test__.model                      import *
import _GTW._OMP._PAP.Nav
import _GTW._Form._MOM.Instance
import _GTW._Form.Javascript
import _GTW._Form._MOM.Javascript

from   _GTW._Form._MOM.Inline_Description       import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
from   _GTW._Form._MOM.Field_Group_Description  import \
    ( Field_Group_Description as FGD
    , Wildcard_Field          as WF
    )

def Person_Form (scope) :
    Person_Admin = GTW.OMP.PAP.Nav.Admin.Person
    return GTW.Form.MOM.Instance.New \
        (scope.PAP.Person, * Person_Admin ["Form_args"])
# end def Person_Form

### __END__ GTW.__test__.Form
