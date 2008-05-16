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
#    DJO._test
#
# Purpose
#    Test for the Navigation and Url_Resolver classes
#
# Revision Dates
#    14-May-2008 (MG) Creation
#    16-May-2008 (MG) Tests extended
#    16-May-2008 (MG) Test for `href` and `abs_href` added
#    ««revision-date»»···
#--
"""
For each `name` exactly one Memo_Url_Resolver shall be created (that will
ensure that the Memo_Url_Resolver created during the navigation tree creation
is used by DJANGO as well)
>>> resolver       = urlresolvers.get_resolver ("test.urls")
>>> root_resolver = root.url_resolver
>>> root_resolver is resolver
True

Now lets test the basic resolving of a `path` to the appropriate view
function:
>>> view, args, kw = resolver.resolve ("/")
>>> view is view_1, kw ["PAGE"].title
(True, u'Home')

>>> view, args, kw = resolver.resolve ("/dir-1/page-1.html")
>>> view is view_2, kw ["PAGE"].title
(True, u'Page 1')

Let's check how sub directories with there own url resolver work:
>>> view, args, kw = resolver.resolve ("/dir-3/sub-dir-1/sub-sub-dir-1/page-6.html")
>>> view is view_7, kw ["PAGE"].title
(True, u'Page 6')

>>> view, args, kw = resolver.resolve ("/dir-3/sub-dir-2/sub-sub-dir-2/page-8.html")
>>> view is view_9, kw ["PAGE"].title
(True, u'Page 8')

Let see what happens if we try a path which does not exist:
>>> view, args, kw = resolver.resolve ("/dir-NOT/sub-dir-1/page-6.html")
Traceback (most recent call last):
 ...
Resolver404: {'path': 'dir-NOT/sub-dir-1/page-6.html', 'tried': [u'^$', u'^dir-1/', u'^dir-2/', u'^dir-3/', '^admin/', '^admin/', '^i18n/', '^user/', '^databrowse/(.*)$']}

A directory can also have it's own url_pattern. In our case, dir-3 has a
special pattern:
>>> view, args, kw = resolver.resolve ("/dir-3/")
>>> view is view_dir_3, kw ["PAGE"].title
(True, u'Test Dir 3')

>>> view, args, kw = resolver.resolve ("/admin/")
>>> view is std_view_1, kw
(True, {})

Test some of the attributes of the navigation list:
>>> for link in root.own_links_transitive :
...    print repr (link.href), repr (link.abs_href)
...
'' '/'
u'dir-1/page-1.html' u'/dir-1/page-1.html'
u'dir-1/page-1.html' u'/dir-1/page-1.html'
u'dir-1/page-2.html' u'/dir-1/page-2.html'
u'dir-2/page-3.html' u'/dir-2/page-3.html'
u'dir-2/page-3.html' u'/dir-2/page-3.html'
u'dir-2/page-4.html' u'/dir-2/page-4.html'
u'dir-3/sub-dir-1/page-5.html' u'/dir-3/sub-dir-1/page-5.html'
u'dir-3/sub-dir-1/page-5.html' u'/dir-3/sub-dir-1/page-5.html'
u'dir-3/sub-dir-1/page-5.html' u'/dir-3/sub-dir-1/page-5.html'
u'dir-3/sub-dir-1/sub-sub-dir-1/page-6.html' u'/dir-3/sub-dir-1/sub-sub-dir-1/page-6.html'
u'dir-3/sub-dir-1/sub-sub-dir-1/page-6.html' u'/dir-3/sub-dir-1/sub-sub-dir-1/page-6.html'
u'dir-3/sub-dir-2/page-7.html' u'/dir-3/sub-dir-2/page-7.html'
u'dir-3/sub-dir-2/page-7.html' u'/dir-3/sub-dir-2/page-7.html'
u'dir-3/sub-dir-2/sub-sub-dir-2/page-8.html' u'/dir-3/sub-dir-2/sub-sub-dir-2/page-8.html'
u'dir-3/sub-dir-2/sub-sub-dir-2/page-8.html' u'/dir-3/sub-dir-2/sub-sub-dir-2/page-8.html'
"""

from   _DJO                import DJO
import _DJO.Navigation
import _DJO.Url_Resolver
from    django.core        import urlresolvers

def view_1     (request, PAGE) : print PAGE.title
def view_2     (request, PAGE) : print PAGE.title
def view_3     (request, PAGE) : print PAGE.title
def view_4     (request, PAGE) : print PAGE.title
def view_5     (request, PAGE) : print PAGE.title
def view_6     (request, PAGE) : print PAGE.title
def view_7     (request, PAGE) : print PAGE.title
def view_8     (request, PAGE) : print PAGE.title
def view_9     (request, PAGE) : print PAGE.title
def view_dir_3 (request, PAGE) : print PAGE.title
def std_view_1 (request, PAGE) : print PAGE.title
def std_view_2 (request, PAGE) : print PAGE.title
def gen_view_1 (request, PAGE) : print PAGE.title
def gen_view_2 (request, PAGE) : print PAGE.title

root = DJO.Navigation.Root.from_dict_list \
    ( Type         = DJO.Navigation.Root
    , Dir_Type     = DJO.Navigation.Dir
    , src_dir      = ''
    , url_resolver = DJO.Singleton_Url_Resolver ("^/", "test.urls")
    , _entries     =
        [ dict
            ( Type         = DJO.Navigation.Page
            , name         = ''
            , title        = 'Home'
            , url_patterns = ((view_1, "view_1"), ) ###
            )
        , dict
            ( Type         = DJO.Navigation.Dir
            , sub_dir      = 'dir-1'
            , title        = 'Test Dir 1'
            , url_resolver = DJO.Url_Resolver
            , _entries     =
                [ dict
                    ( Type         = DJO.Navigation.Page
                    , name         = 'page-1.html'
                    , title        = 'Page 1'
                    , url_patterns = (view_2, )
                    )
                , dict
                    ( Type         = DJO.Navigation.Page
                    , name         = 'page-2.html'
                    , title        = 'Page 2'
                    , url_patterns = (view_3, )
                    )
                ]
            )
        , dict
            ( Type         = DJO.Navigation.Dir
            , sub_dir      = 'dir-2'
            , title        = 'Test Dir 2'
            , url_resolver = DJO.Url_Resolver
            , _entries     =
                [ dict
                    ( Type         = DJO.Navigation.Page
                    , name         = 'page-3.html'
                    , title        = 'Page 3'
                    , url_patterns = (view_4, )
                    )
                , dict
                    ( Type         = DJO.Navigation.Page
                    , name         = 'page-4.html'
                    , title        = 'Page 4'
                    , url_patterns = (view_5, )
                    )
                ]
            )
        , dict
            ( Type         = DJO.Navigation.Dir
            , sub_dir      = 'dir-3'
            , title        = 'Test Dir 3'
            , url_resolver = DJO.Url_Resolver
            , url_patterns = (view_dir_3, )
            , _entries     =
                [ dict
                    ( Type         = DJO.Navigation.Dir
                    , sub_dir      = 'sub-dir-1'
                    , title        = 'Sub Dir 1'
                    , _entries     =
                        [ dict
                            ( Type         = DJO.Navigation.Page
                            , name         = 'page-5.html'
                            , title        = 'Page 5'
                            , url_patterns = (view_6, )
                            )
                        , dict
                            ( Type         = DJO.Navigation.Dir
                            , sub_dir      = 'sub-sub-dir-1'
                            , title        = 'Sub Sub Dir 1'
                            , _entries     =
                                [ dict
                                    ( Type         = DJO.Navigation.Page
                                    , name         = 'page-6.html'
                                    , title        = 'Page 6'
                                    , url_patterns = (view_7, )
                                    , url_resolver = DJO.Url_Resolver
                                    )
                                ]
                            )
                        ]
                    )
                , dict
                    ( Type         = DJO.Navigation.Dir
                    , sub_dir      = 'sub-dir-2'
                    , title        = 'Sub Dir 2'
                    , _entries     =
                        [ dict
                            ( Type         = DJO.Navigation.Page
                            , name         = 'page-7.html'
                            , title        = 'Page 7'
                            , url_patterns = (view_8, )
                            )
                        , dict
                            ( Type         = DJO.Navigation.Dir
                            , sub_dir      = 'sub-sub-dir-2'
                            , title        = 'Sub Sub Dir 2'
                            , _entries     =
                                [ dict
                                    ( Type         = DJO.Navigation.Page
                                    , name         = 'page-8.html'
                                    , title        = 'Page 8'
                                    , url_patterns = (view_9, )
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

### fake Url_Resolvers to support the test
admin = DJO.Singleton_Url_Resolver ("^admin/", "django_docs.urls")
admin.append_pattern \
    ( urlresolvers.RegexURLPattern
        ( r"^$", std_view_1, name = "databrowse")
    )
root.url_resolver.append_pattern \
    ( urlresolvers.RegexURLResolver ("^admin/", "django_docs.urls")
    , urlresolvers.RegexURLResolver ("^admin/", "django.contrib.admin.urls")
    , urlresolvers.RegexURLResolver ("^i18n/",  "django.conf.urls.i18n")
    , urlresolvers.RegexURLResolver ("^user/",  "pages.mangari_org.user_urls")
    , urlresolvers.RegexURLPattern
        ( r"^databrowse/(.*)$"
        , std_view_1
        , name = "databrowse"
        )
    )
if __name__ == "__main__" :
    def _print_resolver_pattern (prefix, resolver) :
        for p in resolver.urlpatterns :
            print "%s%s" % (prefix, p)
            if isinstance (p, DJO.Url_Resolver) :
                _print_resolver_pattern ("  " + prefix, p)
    _print_resolver_pattern ("", root.url_resolver)
    resolver = urlresolvers.get_resolver ("test.urls")
    view, args, kw = resolver.resolve ("/admin/")
    print view, args, kw
### __END__ DJO._test


