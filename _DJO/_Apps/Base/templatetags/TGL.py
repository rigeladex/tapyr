# -*- coding: iso-8859-15 -*-
# Copyright (C) 2008-2009 Martin Glück All rights reserved
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
#    DJO.Apps.Base.templatetags.TGL
#
# Purpose
#    Combine TGL_Tags and TGL_Filters into one loadbale module
#
# Revision Dates
#     9-May-2008 (MG) Creation
#    14-May-2008 (CT) Enforce that TGL_Filters only defines filters, TGL_Tags
#                     only defines tags
#    14-May-2009 (CT) Moved to `_DJO._Apps.Base`
#    ««revision-date»»···
#--

"""
>>> from django.conf     import settings
>>> settings.configure (ROOT_URLCONF = "_DJO._test_url_conf")
>>> from django.template import add_to_builtins, Template, Context
>>> add_to_builtins ("_DJO._Apps.Base.templatetags.TGL")
>>> template = '''
...   {% onion path|eq:"/" %}
...     {% head %}
...       I am the onion then head
...     {% else %}
...       I am the onion else head
...     {% body %}
...       And this is the body which should be enclosed by the head/tail
...     {% tail %}
...       I am the onion then tail
...     {% else %}
...       I am the onion else tail
...   {% endonion %}
... '''.strip ()
>>> t = Template (template)
>>> t.render (Context (dict (path = "/a")))
u'\\n      I am the onion else head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion else tail\\n  '
>>> t.render (Context (dict (path = "/")))
u'\\n      I am the onion then head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion then tail\\n    '
"""

from   django                      import template
register = template.Library ()

from _DJO._Apps.Base.templatetags.TGL_Tags    import register as tags
from _DJO._Apps.Base.templatetags.TGL_Filters import register as filters

assert not tags.filters
assert not filters.tags

register.filters.update (filters.filters)
register.tags.update    (tags.tags)

### __END__ DJO.Apps.Base.templatetags.TGL
