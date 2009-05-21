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
#    20-May-2008 (MG) Test the delegation_view function
#    20-May-2008 (MG) Additional test for `delegation_view` added
#    22-May-2008 (MG) New `_Site_Entity_.view` and
#                     `_Dir_.default_view_pattern` tested, directory
#                     delagation changed and therfore the test cases changed
#                     as well
#    ««revision-date»»···
#--
"""
For each `name` exactly one Memo_Url_Resolver shall be created (that will
ensure that the Memo_Url_Resolver created during the navigation tree creation
is used by DJANGO as well)
>>> resolver       = urlresolvers.get_resolver ("test.urls")
>>> root_resolver = root.url_resolver ## root is define outside the doctest
>>> root_resolver is resolver
True

Now lets test the basic resolving of a `path` to the appropriate view
function:
>>> view, args, kw = resolver.resolve ("/")
>>> view is view_1, kw ["PAGE"].title
(True, u'Home')

### dir-1 has 5 entries which are matched differently: page-2 with a distinct
### pattern, page-X1 and page-X2 are match with a Multi_Page_Url_Pattern and
### page-1 and page-Y with the default pattern of the directory
>>> for path in ( "/dir-1/page-1.html"
...             , "/dir-1/page-2.html"
...             , "/dir-1/page-X1.html"
...             , "/dir-1/page-X2.html"
...             , "/dir-1/page-Y.html"
...             ) :
...     view, args, kw = resolver.resolve (path)
...     view (None, * args, ** kw)
...
Page 1 True () {}
Page 2
Page X1 True () {}
Page X2 True () {}
Page Y True () {}

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

A directory can also have a delegation view (which will return the response
of the first entry)
>>> for path in "/dir-2/", "/dir-3/sub-dir-2/", "/dir-3/sub-dir-2/sub-sub-dir-2/" :
...     try :
...         view, args, kw = resolver.resolve (path)
...     except urlresolvers.Resolver404, e :
...         print "No match found for", path, "\\n" + str (e)
...     print path, view is delegate_directory_root, kw ["PAGE"].title
...     try :
...         view (None, * args, ** kw)
...     except urlresolvers.Resolver404, e :
...         print "Delegation problem for url", path, "\\n" + str (e)
...
/dir-2/ True Test Dir 2
In Test Dir 2 -> delegate to /dir-2/page-3.html (page-3.html)
Page 3
/dir-3/sub-dir-2/ True Sub Dir 2
In Sub Dir 2 -> delegate to /dir-3/sub-dir-2/page-7.html (sub-dir-2/page-7.html)
Page 7
/dir-3/sub-dir-2/sub-sub-dir-2/ True Sub Sub Dir 2
In Sub Sub Dir 2 -> delegate to /dir-3/sub-dir-2/sub-sub-dir-2/page-8.html (sub-dir-2/sub-sub-dir-2/page-8.html)
Page 8

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
u'dir-1/page-X1.html' u'/dir-1/page-X1.html'
u'dir-1/page-Y.html' u'/dir-1/page-Y.html'
u'dir-1/page-X2.html' u'/dir-1/page-X2.html'
u'dir-2/' u'/dir-2/'
u'dir-2/page-3.html' u'/dir-2/page-3.html'
u'dir-2/page-4.html' u'/dir-2/page-4.html'
u'dir-3/sub-dir-1/page-5.html' u'/dir-3/sub-dir-1/page-5.html'
u'dir-3/sub-dir-1/page-5.html' u'/dir-3/sub-dir-1/page-5.html'
u'dir-3/sub-dir-1/page-5.html' u'/dir-3/sub-dir-1/page-5.html'
u'dir-3/sub-dir-1/sub-sub-dir-1/page-6.html' u'/dir-3/sub-dir-1/sub-sub-dir-1/page-6.html'
u'dir-3/sub-dir-1/sub-sub-dir-1/page-6.html' u'/dir-3/sub-dir-1/sub-sub-dir-1/page-6.html'
u'dir-3/sub-dir-2/' u'/dir-3/sub-dir-2/'
u'dir-3/sub-dir-2/page-7.html' u'/dir-3/sub-dir-2/page-7.html'
u'dir-3/sub-dir-2/sub-sub-dir-2/' u'/dir-3/sub-dir-2/sub-sub-dir-2/'
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

### we cannot use the `delegate_directory_root` view form the
### DJO.Url_Resolver module because it relies on a defined
### DJANGO_SETTINGS_MODULE which we don't like to add for our test
def delegate_directory_root (request, ** kw) :
    page     = kw.get (DJO.Url_Pattern.active_page_parameter_name)
    entry    = page._entries [0]
    rel_path = entry.relative_to (page.url_resolver.nav_href)
    print "In %s -> delegate to %s (%s)" % \
        (page.title, entry.abs_href, rel_path)
    callable, args, kw = page.url_resolver.try_patterns (rel_path, kw)
    return callable (request, * args, ** kw)
# end def delegate_directory_root

class Page_with_View (DJO.Navigation.Page) :
    """A normal page which uses an instance method has view"""

    def view (self, request, PAGE, * args, ** kw) :
        print self.title, self is PAGE, args, kw
    # end def view

# end class Page_with_View

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
            , view         = view_1
            )
          ### dir-1 test is ued to test the `view` attribute of an
          ### `_Site_Entity_` and if the Multi_Page_Url_Pattern matches the
          ### path to the correct navigation element
        , dict
            ( Type         = DJO.Navigation.Dir
            , sub_dir      = 'dir-1'
            , title        = 'Test Dir 1'
            , url_resolver = DJO.Url_Resolver
            , default_view_pattern =
                { Page_with_View.view : "^(?P<page>[^X\.]+.html)$"}
            , _entries     =
                [ dict
                    ( Type         = Page_with_View
                    , name         = 'page-1.html'
                    , title        = 'Page 1'
                    )
                , dict
                    ( Type         = Page_with_View
                    , name         = 'page-2.html'
                    , title        = 'Page 2'
                    , view         = view_3
                    )
                , dict
                    ( Type         = Page_with_View
                    , name         = 'page-X1.html'
                    , title        = 'Page X1'
                    )
                , dict
                    ( Type         = Page_with_View
                    , name         = 'page-Y.html'
                    , title        = 'Page Y'
                    )
                , dict
                    ( Type         = Page_with_View
                    , name         = 'page-X2.html'
                    , title        = 'Page X2'
                    )
                ]
            )
        , dict
            ( Type            = DJO.Navigation.Dir
            , sub_dir         = 'dir-2'
            , title           = 'Test Dir 2'
            , url_resolver    = DJO.Url_Resolver
            , delegation_view = delegate_directory_root
            , _entries        =
                [ dict
                    ( Type         = DJO.Navigation.Page
                    , name         = 'page-3.html'
                    , title        = 'Page 3'
                    , view         = view_4
                    )
                , dict
                    ( Type         = DJO.Navigation.Page
                    , name         = 'page-4.html'
                    , title        = 'Page 4'
                    , view         = view_5
                    )
                ]
            )
        , dict
            ( Type         = DJO.Navigation.Dir
            , sub_dir      = 'dir-3'
            , title        = 'Test Dir 3'
            , url_resolver = DJO.Url_Resolver
            , view         = view_dir_3
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
                            , view         = view_6
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
                                    #, view         = view_7
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
                    , delegation_view = delegate_directory_root
                    , _entries     =
                        [ dict
                            ( Type         = DJO.Navigation.Page
                            , name         = 'page-7.html'
                            , title        = 'Page 7'
                            , view         = view_8
                            )
                        , dict
                            ( Type         = DJO.Navigation.Dir
                            , sub_dir      = 'sub-sub-dir-2'
                            , title        = 'Sub Sub Dir 2'
                            , delegation_view = delegate_directory_root
                            , _entries     =
                                [ dict
                                    ( Type         = DJO.Navigation.Page
                                    , name         = 'page-8.html'
                                    , title        = 'Page 8'
                                    , view         = view_9
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
    ### XXX this is only code with makes debugging easier
    def _print_resolver_pattern (prefix, resolver) :
        for p in resolver.urlpatterns :
            print "%s%s" % (prefix, p)
            if isinstance (p, DJO.Url_Resolver) :
                _print_resolver_pattern ("  " + prefix, p)
    if 0 :
       _print_resolver_pattern ("", root.url_resolver)
    if 0 :
       resolver = urlresolvers.get_resolver ("test.urls")
       view, args, kw = resolver.resolve ("/dir-1/page-1.html")
       view (None, * args, ** kw)
### __END__ DJO._test
