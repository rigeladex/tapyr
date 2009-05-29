# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
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
#    DJO.tests.Model_Form
#
# Purpose
#    Test the model form
#
# Revision Dates
#    29-May-2009 (MG) Creation
#    ««revision-date»»···
#--
"""
>>> fs1       = DJO.Form_Set_Description ()
>>> form1_cls = DJO.Model_Form.New (M.News, fs1)
>>> form1     = form1_cls ()
>>> [bff.name for bff in form1]
['title', 'text', 'date_pub', 'author']
>>> title = form1 ["title"]
>>> print title
<input id="id_title" type="text" name="title" maxlength="80" />
>>> print title.label_tag ()
<label for="id_title">Titel</label>
>>> print title.help_text
Help text for the title
>>> print title.errors
<BLANKLINE>
"""
import  os
os.environ ["DJANGO_SETTINGS_MODULE"] = "_DJO._tests._Nav.settings_test"

import _DJO._tests._Nav.model_1.models as     M
from   _DJO                            import DJO
import _DJO.Forms
import _DJO.Form_Set_Description
### __END__ DJO.tests.Model_Form
