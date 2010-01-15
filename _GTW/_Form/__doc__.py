# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    GTW.__doc__
#
# Purpose
#    Documentation and test for the GTW library
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--
"""
>>> from   _GTW                   import GTW
>>> import _GTW._Form.Form
>>> import _GTW._Form.Field_Group_Description
>>> from   _MOM.__doc__           import MOM, BMT ### define a test object model
>>> from   _MOM._EMS.Hash         import Manager as EMS
>>> from   _MOM._DBW._HPS.Manager import Manager as DBW
>>>
>>> apt = MOM.App_Type (u"BMT", BMT).Derived (EMS, DBW)
>>>
>>> ET_Rodent    = apt [u"BMT.Rodent"]
>>> ET_Mouse     = apt [u"BMT.Mouse"]
>>> ET_Otter     = apt [u"BMT.Otter"]
>>> ET_Trap      = apt [u"BMT.Trap"]
>>> ET_Supertrap = apt [u"BMT.Supertrap"]
>>>
>>> ET_FGD   = GTW.Form.E_Type_Field_Group_Description

If any enpty E_Type_Field_Group_Description is used, all user editable
attributes of the E-Type will be placed in two field groups:

 - all `epk` attributes will go into one field group
 - all `user_attr` wil go into the second field group

>>> form_rod = GTW.Form.Form ("/post/", None, ET_FGD (ET_Rodent))
>>> [fg.fields for fg in form_rod ]
[[Name `name`], [String `color`, Float `weight`]]

One can also use the `+` wildcard to place all attributes which have been
explicitly named in the form group at the location of wildcard:

>>> form_mou = GTW.Form.Form ("/post/", None, ET_FGD (ET_Mouse, "weight", "*"))
>>> [f for f in form_mou]
[Float `weight`, Name `name`, String `color`]

>>> form_ott = GTW.Form.Form ("/post/", None, ET_FGD (ET_Otter, "weight", "*", "name"))
>>> [f for f in form_ott]
[Float `weight`, String `color`, String `region`, String `river`, Name `name`]

>>> form_ott.field_groups [0].parent is form_ott
True
"""
### __END__ __doc__


