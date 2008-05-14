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
#    ««revision-date»»···
#--
"""
For each `name` exactly one Root_Url_Resolver shall be created (that will
ensure that the Root_Url_Resolver created during the navigation tree creation
is used by DJANGO as well)
>>> root_resolver = DJO.Root_Url_Resolver.root_url_resolvers.values () [0]
>>> resolver = DJO.Root_Url_Resolver ("^/", "test.urls")
>>> root_resolver is resolver
True

Now lets test the basic resolving of a `path` to the appropriate view
function:
>>> view, args, kw = resolver.resolve ("/")
>>> view is view_1
True
>>> kw ["PAGE"].title
u'Home'

>>> view, args, kw = resolver.resolve ("/dir-1/page-1.html")
>>> view is view_2
True
>>> kw ["PAGE"].title
u'Page 1'

>>> view, args, kw = resolver.resolve ("/dir-3/sub-dir-1/page-6.html")
>>> view is view_7
True
>>> kw ["PAGE"].title
u'Page 6'
"""

from   _DJO                import DJO
import _DJO.Navigation
import _DJO.Url_Resolver

def view_1 (request, PAGE) : print PAGE.title
def view_2 (request, PAGE) : print PAGE.title
def view_3 (request, PAGE) : print PAGE.title
def view_4 (request, PAGE) : print PAGE.title
def view_5 (request, PAGE) : print PAGE.title
def view_6 (request, PAGE) : print PAGE.title
def view_7 (request, PAGE) : print PAGE.title
def view_8 (request, PAGE) : print PAGE.title
def view_9 (request, PAGE) : print PAGE.title

root = DJO.Navigation.Root.from_dict_list \
    ( Type         = DJO.Navigation.Root
    , Dir_Type     = DJO.Navigation.Dir
    , src_dir      = ''
    , url_resolver = DJO.Root_Url_Resolver ("^/", "test.urls")
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
                            ( Type         = DJO.Navigation.Page
                            , name         = 'page-6.html'
                            , title        = 'Page 6'
                            , url_patterns = (view_7, )
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
root = DJO.Navigation.Root.from_dict_list \
    ( Type         = DJO.Navigation.Root
    , src_dir      = ''
    , url_resolver = DJO.Root_Url_Resolver ("^/", "test.urls")
    , _entries     =
        [ dict
            ( Type         = DJO.Navigation.Dir
            , sub_dir      = 'dir-3'
            , title        = 'Test Dir 3'
            , url_resolver = DJO.Url_Resolver
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
                        ]
                    )
                ]
            )
        ]
    )
#import pdb; pdb.set_trace ()
#resolver = DJO.Root_Url_Resolver ("^/", "test.urls")
#view, args, kw = resolver.resolve ("/dir-3/sub-dir-1/page-6.html")
### __END__ DJO._test


