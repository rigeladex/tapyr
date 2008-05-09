# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Martin Glück All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
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
#    DJO.templatetags.TGL_Filters
#
# Purpose
#    Tanzer and Glueck's library of custom django template filters
#
# Revision Dates
#     9-May-2008 (MG) Creation
#    ««revision-date»»···
#--
"""
>>> from django.conf     import settings
>>> settings.configure (ROOT_URLCONF = "_DJO._test_url_conf")
>>> from django.template import add_to_builtins, Template, Context
>>> add_to_builtins ("_DJO.templatetags.TGL_Filters")
>>> template = '''
...   {{ var|starts_with:"foo"}}
...   {{ var|starts_with:"fooa"}}
...   {{ var|starts_with:"afoo"}}
...   {{ var|starts_with:"fo"}}
... '''
>>> t = Template (template)
>>> t.render (Context (dict (var = "foo"))).strip ()
u'True\\n  False\\n  False\\n  True'
>>> t.render (Context (dict (var = ""))).strip ()
u''
"""
from   django.template             import defaultfilters
from   django                      import template

register = template.Library ()

@register.filter
@defaultfilters.stringfilter
def starts_with (value, prefix) :
    """Returns the result of `value.startswith (prefix)`"""
    return value and value.startswith (prefix)
# end def starts_with


### __END__ DJO.templatetags.TGL_Filters
