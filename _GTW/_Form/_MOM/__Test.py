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
#    GTW.Form.MOM.__Test
#
# Purpose
#    Simple test
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW                   import GTW
import _GTW._Form._MOM.Field_Group_Description
import _GTW._Form._MOM.Instance
import _GTW._Form._MOM.Inline_Description
from   _MOM._EMS.Hash         import Manager as EMS
from   _MOM._DBW._HPS.Manager import Manager as DBW
from   _JNJ.Environment       import HTML
from    jinja2.loaders        import DictLoader

from   _MOM                      import MOM
import _GTW._OMP._PAP.import_PAP

apt = MOM.App_Type \
    (u"HWO", GTW, PNS_Aliases = dict (PAP = GTW.OMP.PAP)
    ).Derived (EMS, DBW)

scope        = MOM.Scope.new (apt, None)

loader      = DictLoader (dict (base = """\
{% import "html/form.jnj" as Form %}
{{ GTW.call_macro (form.widget, form) }}
"""))

ct       = scope.PAP.Person ("Tanzer", "Christian")
ct_a     = scope.PAP.Address ("Glasauergasse 32", "Wien", "1030", "Austria")
ct_h_a   = scope.PAP.Person_has_Address (ct, ct_a)
form_cls = GTW.Form.MOM.Instance.New \
    ( scope.PAP.Person
    , GTW.Form.MOM.Field_Group_Description ()
    , GTW.Form.MOM.Inline_Description
        ( "PAP.Person_has_Address", "person"
        , GTW.Form.MOM.Field_Group_Description
              ( GTW.Form.MOM.Field_Prefixer
                  ("address", "street", "zip", "city", "country", "desc")
              )
        , min_empty = 1
        )
    )

env = HTML (loader = loader)

#print env.get_template ("base").render (form = form_cls ("/None"))
print env.get_template ("base").render (form = form_cls ("/CT", ct))
if 0 :
    form = form_cls ("/Foo")
    form ( { "first_name"                            : "Martin"
           , "last_name"                             : "Glueck"
           , "Person_has_Address-M0-address.street"  : "Langstrasse 4/1"
           , "Person_has_Address-M0-address.zip"     : "2244"
           , "Person_has_Address-M0-address.city"    : "Spannberg"
           , "Person_has_Address-M0-address.country" : "Austria"
           }
         )
print scope.PAP.Person            .query ().all ()
print scope.PAP.Address           .query ().all ()
print scope.PAP.Person_has_Address.query ().all ()
### __END__ GTW.Form.MOM.__Test
