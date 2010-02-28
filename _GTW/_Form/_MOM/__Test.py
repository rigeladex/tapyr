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
import _GTW._Form._MOM.Instance
from   _GTW._Form._MOM.Inline_Description import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
from   _GTW._Form._MOM.Field_Group_Description import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )
from   _MOM._EMS.Hash         import Manager as EMS
from   _MOM._DBW._HPS.Manager import Manager as DBW
from   _MOM._EMS.SAS          import Manager as EMS
from   _MOM._DBW._SAS.Manager import Manager as DBW
from   _JNJ.Environment       import HTML
from    jinja2.loaders        import DictLoader

from   _MOM                      import MOM
from   _MOM.Product_Version      import Product_Version, IV_Number

GTW.Version = Product_Version \
    ( productid           = u"GTW Test"
    , productnick         = u"GTW"
    , productdesc         = u"Example web application "
    , date                = "20-Jan-2010"
    , major               = 0
    , minor               = 5
    , patchlevel          = 42
    , author              = u"Christian Tanzer, Martin Glück"
    , copyright_start     = 2010
    , db_version          = IV_Number
        ( "db_version"
        , ("Hello World", )
        , ("Hello World", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".how"
        )
    )
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP .import_PAP
import _GTW._OMP._PAP.Nav

apt = MOM.App_Type \
    (u"HWO", GTW, PNS_Aliases = dict (PAP = GTW.OMP.PAP, Auth = GTW.OMP.Auth)
    ).Derived (EMS, DBW)

scope        = MOM.Scope.new (apt, None)

loader      = DictLoader (dict (base = """\
{% import "html/form.jnj" as Form %}
{{ GTW.call_macro (form.widget, form) }}
"""))

env = HTML (loader = loader)

def display_values (form, indent = "") :
    print "%s%s" % (indent, form.prefix or "Toplevel")
    for f in form.fields :
        print "  %s%-20s :%r" % (indent, form.get_id (f), form.get_raw (f))
    for ig in form.inline_groups :
        for ifo in ig.forms :
            display_values (ifo, indent + "  ")
# end def display_values


add = False
per = False
php = True

if per :
    form_cls = GTW.Form.MOM.Instance.New \
        ( scope.PAP.Person
        , * GTW.OMP.PAP.Nav.Admin.Person ["Form_args"]
        )
if add :
    form_cls = GTW.Form.MOM.Instance.New \
        ( scope.PAP.Address
        , * GTW.OMP.PAP.Nav.Admin.Address ["Form_args"]
        )
if php :
    form_cls = GTW.Form.MOM.Instance.New \
        ( scope.PAP.Person_has_Phone
        )
if per :
    p = scope.PAP.Person  ("Glueck", "Martin")
    a1 = scope.PAP.Address ("Langstrasse 4", "2244", "Spannberg", "Asutria")
    a2 = scope.PAP.Address ("Oberzellergasse 14", "1030", "Wien", "Asutria")
    scope.PAP.Person_has_Address (p, a1, desc = "home")
    scope.PAP.Person_has_Address (p, a2, desc = "home")
    form = form_cls ("/post/", p)

    #display_values (form)
    #print env.get_template ("base").render (form = form)
if add :
    form = form_cls ("/post/")
    #print env.get_template ("base").render (form = form)
    #display_values (form)
    print form.inline_groups [0].forms [0]


### __END__ GTW.Form.MOM.__Test
