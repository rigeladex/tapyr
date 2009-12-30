# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck All rights reserved
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
#    GTW.__Test
#
# Purpose
#    Simple test
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW                   import GTW
import _GTW.Entity_Form
import _GTW.Field_Group_Description
from   _MOM.__doc__           import MOM, BMT ### define a test object model
from   _MOM._EMS.Hash         import Manager as EMS
from   _MOM._DBW._HPS.Manager import Manager as DBW
from   _JNJ.Environment       import HTML
from    jinja2.loaders        import DictLoader

apt = MOM.App_Type (u"BMT", BMT).Derived (EMS, DBW)

ET_Rodent    = apt [u"BMT.Rodent"]
ET_Mouse     = apt [u"BMT.Mouse"]
ET_Otter     = apt [u"BMT.Otter"]
ET_Trap      = apt [u"BMT.Trap"]
ET_Supertrap = apt [u"BMT.Supertrap"]

scope        = MOM.Scope.new (apt, None)
m            = scope.BMT.Mouse ("Mouse_1")
form_rod     = GTW.Entity_Form ("/post", m)

loader      = DictLoader (dict (base = """\
{% import "form.jnj" as Form %}
{{ Form.form (form) }}
"""))

env = HTML (loader = loader)

print env.get_template("base").render(dict (form = form_rod))

### __END__ GTW.__Test


