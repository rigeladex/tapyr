# -*- coding: iso-8859-1 -*-
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
    >>> form_cls.sub_forms
    {'Person_has_Address': <class '_GTW._Form._MOM.Inline_Instance.Link_Inline_Instance_Person__Person_has_Address'>}
    >>> form = form_cls ("/post/")
    >>> form.form_name
    'Person'
    >>> [il.form_cls.form_name for il in form.inline_groups]
    ['Person__Person_has_Address']
    >>> for l in form.Media.js_on_ready : print l
    /* setup form `GTW_OMP_PAP_Person` */
    <BLANKLINE>
    $(".GTW_OMP_PAP_Person").GTW_Form
    <BLANKLINE>
      ( {"inlines": [{"instance_class": "inline-instance", "prefix": "Person__Person_has_Address", "allow_copy": true}], "completers": []}
      );
    <BLANKLINE>
"""

from _GTW.__test__.model import *
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
    PAP               = scope.PAP
    address_completer = GTW.Form.Javascript.Multi_Completer \
        ( GTW.Form.MOM.Javascript.Completer
            ( fields    = ("street", "city", "zip", "country")
            , triggers  = dict (street = dict (min_chars = 3))
            )
        , zip       = GTW.Form.MOM.Javascript.Field_Completer
            ( "zip", ("zip", "city", "country", "region")
            , min_chars = 1
            )
        , city      = GTW.Form.MOM.Javascript.Field_Completer
            ( "city", ("city", "country", "region")
            , min_chars = 2
            )
        , name      = "Address_Completer"
        )
    return GTW.Form.MOM.Instance.New \
        ( PAP.Person
        , FGD ()
        , LID ( "PAP.Person_has_Address"
              , legend        = "Addresses"
              , field_attrs   = dict
                    (address  = dict (completer = address_completer))
              )
        )
# end def Person_Form

### __END__ GTW.__test__.Form


