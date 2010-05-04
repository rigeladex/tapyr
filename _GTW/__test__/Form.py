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
    >>> PAP = scope.PAP
    >>> form_cls = GTW.Form.MOM.Instance.New \
    ...    ( PAP.Person
    ...    , FGD ()
    ...    , LID ( "PAP.Person_has_Address", legend = "Addresses")
    ...    , LID ( "PAP.Person_has_Phone",   legend = "Phones")
    ...    )
    >>> form_cls.sub_forms
    {'Person_has_Address': <class '_GTW._Form._MOM.Inline_Instance.Link_Inline_Instance_Person__Person_has_Address'>, 'Person_has_Phone': <class '_GTW._Form._MOM.Inline_Instance.Link_Inline_Instance_Person__Person_has_Phone'>}

Test if it is possible to only create an person address link and lefting the
peson has phone fields empty:
    >>> form = form_cls ("/post/")
    >>> PD   = dict ()
    >>> PD ["Person__last_name"]                             = "Last"
    >>> PD ["Person__first_name"]                            = "First"
    >>> PD ["Person__Person_has_Address-M0__right__street"]  = "Street"
    >>> PD ["Person__Person_has_Address-M0__right__zip"]     = "zip"
    >>> PD ["Person__Person_has_Address-M0__right__city"]    = "Vienna"
    >>> PD ["Person__Person_has_Address-M0__right__country"] = "Austria"
    >>> form (PD)
    0
    >>> form.instance
    GTW.OMP.PAP.Person (u'last', u'first', u'', u'')
    >>> PAP.Person            .query ().all ()
    [GTW.OMP.PAP.Person (u'last', u'first', u'', u'')]
    >>> PAP.Address           .query ().all ()
    [GTW.OMP.PAP.Address (u'street', u'zip', u'vienna', u'austria', u'')]
    >>> PAP.Phone             .query ().all ()
    []
    >>> PAP.Person_has_Address.query ().all ()
    [GTW.OMP.PAP.Person_has_Address ((u'last', u'first', u'', u''), (u'street', u'zip', u'vienna', u'austria', u''))]
    >>> PAP.Person_has_Phone  .query ().all ()
    []
"""

from _GTW.__test__.model import *
import _GTW._Form._MOM.Instance
from   _GTW._Form._MOM.Inline_Description       import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
from   _GTW._Form._MOM.Field_Group_Description  import \
    ( Field_Group_Description as FGD
    , Wildcard_Field          as WF
    )

### __END__ GTW.__test__.Form


