# -*- coding: utf-8 -*-
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
>>> fs       = DJO.Field_Group_Description ()
>>> form_cls = DJO.Model_Form.New (M.News, fs)
>>> form     = form_cls (data = {})
>>> [bff.name for bff in form]
['title', 'text', 'date_pub', 'author']
>>> title = form ["title"]
>>> print title
<input id="id_title" type="text" class="" name="title" maxlength="80" />
>>> print title.label_tag ()
<label for="id_title">Titel</label>
>>> print title.help_text
Help text for the title
>>> form     = form_cls (data = dict (title = "Title", text = "Text"))
>>> form.save ()
<News: Title>

### now, let's explicitly specify the field we want in the field_group to show up
>>> fs       = DJO.Field_Group_Description ("title", "text")
>>> form_cls = DJO.Model_Form.New (M.News, fs)
>>> form     = form_cls (data = {})
>>> [bff.name for bff in form]
['title', 'text']

### now we test mutiple form set's
>>> fs1      = DJO.Field_Group_Description ("title", "text")
>>> fs2      = DJO.Field_Group_Description ("author", "date_pub")
>>> form_cls = DJO.Model_Form.New (M.News, fs1, fs2)
>>> form     = form_cls (data = {})
>>> [bff.name for bff in form]
['title', 'text', 'author', 'date_pub']

### now we test the 'Auto_Field_Group_Description' if multiple form set's are specified
>>> fs1      = DJO.Field_Group_Description ("title", "text")
>>> fs2      = DJO.Auto_Field_Group_Description ()
>>> form_cls = DJO.Model_Form.New (M.News, fs1, fs2)
>>> form     = form_cls (data = {})
>>> [bff.name for bff in form]
['title', 'text', 'date_pub', 'author']

### and now combine the "Auto_Field_Group_Description" with an exclude
>>> fs1      = DJO.Field_Group_Description ("title", "text")
>>> fs2      = DJO.Auto_Field_Group_Description (exclude = ("date_pub", ))
>>> form_cls = DJO.Model_Form.New (M.News, fs1, fs2)
>>> form     = form_cls (data = {})
>>> [bff.name for bff in form]
['title', 'text', 'author']

### now, let's use the DJO.Field_Description (FD)
>>> fs       = DJO.Field_Group_Description (FD ("title"), FD ("text"))
>>> form_cls = DJO.Model_Form.New (M.News, fs)
>>> form     = form_cls (data = {})
>>> [bff.name for bff in form]
['title', 'text']
>>> title = form ["title"]
>>> str (title)
'<input id="id_title" type="text" class="" name="title" maxlength="80" />'

### this was boring, so let's use the field descriptor for some fancy
>>> fs       = DJO.Field_Group_Description \\
...     ( FD ("title", widget = forms.HiddenInput)
...     , FD ("text")
...     )
>>> form_cls = DJO.Model_Form.New (M.News, fs)
>>> form     = form_cls (data = {})
>>> [bff.name for bff in form]
['title', 'text']
>>> title = form ["title"]
>>> str (title)
'<input id="id_title" type="hidden" class="" name="title" />'

### create a test navigation root object and the admin for it
>>> root  = DJO.Navigation.Root ("/", encoding = "iso-8859-15", input_encoding  = "iso-8859-15")
>>> admin = DJO.NAV.Site_Admin \\
...     ( models = (M.News, M.News_Extender)
...     , src_dir = "Admin", parent = root
...     , title   = "Admin", template = "test_admin_site.html"
...     )

### just to see that the template we have specified is really used
>>> print admin.rendered ()
Admin Site

### now let's see how the auto_form's look like
>>> news_form_cls          = admin._entries [0].Form
>>> news_extender_form_cls = admin._entries [1].Form
>>> [bff.name for bff in news_form_cls          ()]
['title', 'text', 'date_pub', 'author']
>>> [bff.name for bff in news_extender_form_cls ()]
['title', 'text', 'additional_text']
>>> news_extender_form_cls.field_group_descriptions [0].template
'model_admin_change_table.html'
>>> news_extender_form_cls ({}).full_clean ()

>>> c = DJO.Test.Client ()
>>> response = c.get ("/news_ extender/create")
>>> print response
<form method="post" action="">
    <table>
    <tr><th><label for="id_title">Titel</label></th>
        <td><input id="id_title" type="text" class="" name="title" maxlength="80" /> HT: Help text for the title</td>
    </tr>
    <tr><th><label for="id_text">Text</label></th>
        <td><textarea id="id_text" rows="10" cols="40" name="text" class=""></textarea> HT: </td>
    </tr>
    <tr><th><label for="id_additional_text">Additional text</label></th>
        <td><textarea id="id_additional_text" rows="10" cols="40" name="additional_text" class=""></textarea> HT: </td>
    </tr>
    </table>
    <div class="submit-button">
      <input type="submit" value="Sichern" />
    </div>
  </form>
"""

import  os
os.environ ["DJANGO_SETTINGS_MODULE"] = "_DJO._tests._Nav.settings_test"

import _DJO._tests._Nav.model_1.models as     M
from   _DJO                            import DJO
import _DJO.Model_Form
import _DJO.Field_Group_Description
import _DJO.Navigation
import _DJO._Test.Database
import _DJO._Test.Client

M.News._F.finalize ()
FD = DJO.Field_Description

from django import forms
from django.test import utils as Test_Utils
from django.db   import connection

Test_Utils.setup_test_environment  ()
connection.creation.create_test_db (verbosity = 0)

### XXX hackish
DJO.NAV.Model.Admin.Changer.template = "test_admin_change.html"

"""
import  os
os.environ ["DJANGO_SETTINGS_MODULE"] = "_DJO._tests._Nav.settings_test"

import _DJO._tests._Nav.model_1.models as     M
from   _DJO                            import DJO
import _DJO.Model_Form
import _DJO.Field_Group_Description

M.News._F.finalize ()

fs1       = DJO.Field_Group_Description ()
form1_cls = DJO.Model_Form.New (M.News, fs1)

fs1      = DJO.Field_Group_Description ("title", "text")
fs2      = DJO.Auto_Field_Group_Description ()
form_cls = DJO.Model_Form.New (M.News, fs1, fs2)
"""
### __END__ DJO.tests.Model_Form
