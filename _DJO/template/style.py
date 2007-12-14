# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2007 Martin Glueck. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    DJO.template.style
#
# Purpose
#    Template loader which can handle different styles based on a
#    user_profile setting
#
# Revision Dates
#    06-May-2007 (MG) Creation (reused form a previous attempt)
#    06-May-2007 (MG) Use `_thread_locals` to support mod_python/FasfCGI in
#                     the future as well
#    13-Jun-2007 (MG) Do not use thread.locals anymore (causes some problems
#                     with mod_python)
#    14-Dec-2007 (CT) Moved into package DJO
#    ««revision-date»»···
#--

from   django.conf            import settings
from   django.core.exceptions import ImproperlyConfigured
from   django.template        import TemplateDoesNotExist
import os.path                as     P
import urllib2

# At compile time, cache the directories to search.
default_style = "default"
user_style    = "default"
app_temp_dirs = {}

for app in settings.INSTALLED_APPS:
    i = app.rfind (".")
    if i == -1 :
        m, a = app, None
    else:
        m, a = app [:i], app[i+1:]
    try:
        if a is None:
            mod = __import__ (m, "", "", [])
        else:
            mod = getattr (__import__ (m, "", "",  [a]), a)
    except ImportError, e:
        raise ImproperlyConfigured, 'ImportError %s: %s' % (app, e.args [0])
    template_dir = P.join (P.dirname (mod.__file__), "templates")
    if P.isdir (P.join (template_dir, default_style)) :
        app_temp_dirs [mod.__file__.split (P.sep) [-2]] = template_dir
### for app in settings.INSTALLED_APPS
### and now, lets see if we have a `templates` directory which contains at
### least the default style in the project's root directory
try :
    project_root = P.dirname \
        (__import__ (settings.SETTINGS_MODULE, {}, {}, ['']).__file__)
    template_dir = P.join (project_root, "templates")
    if P.isdir (P.join (template_dir, default_style)) :
        app_temp_dirs [None] = template_dir
except ImportError :
    ### later on this error will be reported anyways -> so we can ignore it
    ### here for the moment
    pass

def set_user_style (request) :
    profile    = getattr (request.user, "profile", None)
    user_style = getattr (profile,      "style",   default_style)
    return {}
# end def set_user_style

def get_template_sources (template_name, template_dirs = None) :
    parts = template_name.split ("/", 1)
    if len (parts) > 1 :
        app_name, template_name = parts
        root = app_temp_dirs.get (app_name, None)
        if root is None :
            root          = app_temp_dirs [None]
            template_name = P.join (app_name, template_name)
        yield P.join (root, user_style,     template_name)
        yield P.join (root, default_style,  template_name)
# end def get_template_sources

def load_template_source (template_name, template_dirs = None) :
    for filepath in get_template_sources (template_name, template_dirs) :
        try:
            return (open (filepath).read (), filepath)
        except IOError:
            pass
    raise TemplateDoesNotExist, template_name
# end def load_template_source

load_template_source.is_usable = True

def user_style_url (format) :
    for style in user_style, default_style :
        url = format % style
        try :
            uo = urllib2.urlopen (url)
            uo.close             ()
            break
        except :
            pass
    return url, style
# end def user_style_url

### __END__ DJO.template.style
