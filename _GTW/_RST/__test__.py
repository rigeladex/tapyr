# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.__test__
#
# Purpose
#    Doctest for package GTW.RST
#
# Revision Dates
#    11-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW._RST.Resource       import *

from   _TFL.Formatter           import Formatter, formatted_1

formatted = Formatter (width = 240)

def show_1 (resource, level) :
    p = resource.parent.abs_href if resource.parent else "-"
    t = resource.top.abs_href
    print ("%s%s parent = %s, top = %s" % ("  " * level, resource, p, t))
# end def show_1

def show (resource, level = 0) :
    show_1 (resource, level)
    for e in resource.entries :
        show (e, level + 1)
# end def show

__doc__ = """

    >>> e_types = ( Dir
    ...         ( name          = "PAP-Company"
    ...         , description   = "Legal person"
    ...         , entries       =
    ...             ( Leaf (name = "1", implicit = True)
    ...             ,
    ...             )
    ...         )
    ...     , Dir
    ...         ( name          = "PAP-Person"
    ...         , description   = "Natural person"
    ...         )
    ...     ,
    ...     )
    >>> root = Root ( HTTP = None
    ...     , language          = "en"
    ...     , entries           =
    ...         ( Leaf
    ...             ( name          = "about"
    ...             , implicit      = True
    ...             )
    ...         , Dir
    ...             ( name          = "v1"
    ...             , description   = "Version 1 of test RESTful api"
    ...             , entries       =
    ...                 ( Dir
    ...                     ( name          = "Meta"
    ...                     , description   = "Meta information about RESTful api"
    ...                     )
    ...                 ,
    ...                 ) + e_types
    ...             )
    ...         , Dir
    ...             ( name          = "v2"
    ...             )
    ...         )
    ...     )
    >>> print (formatted (e_types))
    (
      ( <class '_GTW._RST.Resource.Dir'>
      , ()
      , { 'description' : 'Legal person'
        , 'entries' :
            (
              ( <class '_GTW._RST.Resource.Leaf'>
              , ()
                , { 'implicit' : True
                  , 'name' : '1'
                  }
              )
            )
        , 'name' : 'PAP-Company'
        }
      )
    ,
      ( <class '_GTW._RST.Resource.Dir'>
      , ()
      , { 'description' : 'Natural person'
        , 'name' : 'PAP-Person'
        }
      )
    )
    >>> root
    <Root : />
    >>> root.entries
    [<Leaf about: /about>, <Dir v1: /v1>, <Dir v2: /v2>]

    >>> ets = tuple (root.entries_transitive)
    >>> ets
    (<Leaf about: /about>, <Dir v1: /v1>, <Dir Meta: /v1/Meta>, <Dir PAP-Company: /v1/PAP-Company>, <Leaf 1: /v1/PAP-Company/1>, <Dir PAP-Person: /v1/PAP-Person>, <Dir v2: /v2>)

    >>> [e.name for e in ets]
    [u'about', u'v1', u'Meta', u'PAP-Company', u'1', u'PAP-Person', u'v2']
    >>> [e.href for e in ets]
    [u'about', u'v1', u'v1/Meta', u'v1/PAP-Company', u'v1/PAP-Company/1', u'v1/PAP-Person', u'v2']

    >>> print (root.href_pat_frag)
    v2|v1(?:/(?:PAP\-Person|PAP\-Company|Meta))?

    >>> for e in ets :
    ...     print (e.href, e.href_pat_frag)
    about None
    v1 v1(?:/(?:PAP\-Person|PAP\-Company|Meta))?
    v1/Meta Meta
    v1/PAP-Company PAP\-Company
    v1/PAP-Company/1 None
    v1/PAP-Person PAP\-Person
    v2 v2

    >>> root.entries [1]
    <Dir v1: /v1>

    >>> root.entries [1].entries
    [<Dir Meta: /v1/Meta>, <Dir PAP-Company: /v1/PAP-Company>, <Dir PAP-Person: /v1/PAP-Person>]

    >>> c = root.resource_from_href("/v1/PAP-Company")
    >>> c
    <Dir PAP-Company: /v1/PAP-Company>
    >>> sorted (c.SUPPORTED_METHODS)
    ['GET', 'HEAD', 'OPTIONS']

    >>> show (root)
    <Root : /> parent = -, top = /
      <Leaf about: /about> parent = /, top = /
      <Dir v1: /v1> parent = /, top = /
        <Dir Meta: /v1/Meta> parent = /v1, top = /
        <Dir PAP-Company: /v1/PAP-Company> parent = /v1, top = /
          <Leaf 1: /v1/PAP-Company/1> parent = /v1/PAP-Company, top = /
        <Dir PAP-Person: /v1/PAP-Person> parent = /v1, top = /
      <Dir v2: /v2> parent = /, top = /

    >>> print (formatted_1 (root.GET.render_man.by_extension))
    {'json' : [<class '_GTW._RST.Mime_Type.JSON'>]}
    >>> print (formatted_1 (root.GET.render_man.by_mime_type))
    {'application/json' : [<class '_GTW._RST.Mime_Type.JSON'>]}

    >>> GTW.RST.Mime_Type.JSON
    <class '_GTW._RST.Mime_Type.JSON'>
    >>> GTW.RST.Mime_Type.JSON.extensions
    ('json',)
    >>> GTW.RST.Mime_Type.JSON.mime_types
    (u'application/json',)

    >>> for n, r in sorted (GTW.RST.Mime_Type.JSON.Table.iteritems ()) :
    ...     print (r.name, r.extensions, r.mime_types)
    ATOM ('atom',) (u'application/atom+xml',)
    CSV ('csv',) (u'text/csv',)
    HTML (u'html', u'htm') (u'text/html',)
    HTML_T (u'html', u'htm') (u'text/html',)
    JSON ('json',) (u'application/json',)
    TXT ('txt',) (u'text/plain',)
    XHTML ('xhtml',) (u'application/xhtml+xml',)
    XML ('xml',) (u'text/xml', u'application/xml')

    >>> root2 = Root ( HTTP = None
    ...     , language          = "en"
    ...     , entries           =
    ...         ( Leaf
    ...             ( name          = "about"
    ...             , implicit      = True
    ...             )
    ...         , Dir
    ...             ( name          = "v1"
    ...             , description   = "Version 1 of test RESTful api"
    ...             , entries       =
    ...                 ( Dir
    ...                     ( name          = "Meta"
    ...                     , description   = "Meta information about RESTful api"
    ...                     )
    ...                 ,
    ...                 ) + e_types
    ...             )
    ...         , Dir
    ...             ( name          = "v2"
    ...             , entries       = list (e_types)
    ...             )
    ...         )
    ...     )
    >>> ets2 = tuple (root2.entries_transitive)
    >>> ets2
    (<Leaf about: /about>, <Dir v1: /v1>, <Dir Meta: /v1/Meta>, <Dir PAP-Company: /v1/PAP-Company>, <Leaf 1: /v1/PAP-Company/1>, <Dir PAP-Person: /v1/PAP-Person>, <Dir v2: /v2>, <Dir PAP-Company: /v2/PAP-Company>, <Leaf 1: /v2/PAP-Company/1>, <Dir PAP-Person: /v2/PAP-Person>)

    >>> [e.name for e in ets2]
    [u'about', u'v1', u'Meta', u'PAP-Company', u'1', u'PAP-Person', u'v2', u'PAP-Company', u'1', u'PAP-Person']
    >>> [e.href for e in ets2]
    [u'about', u'v1', u'v1/Meta', u'v1/PAP-Company', u'v1/PAP-Company/1', u'v1/PAP-Person', u'v2', u'v2/PAP-Company', u'v2/PAP-Company/1', u'v2/PAP-Person']

    >>> print (root2.href_pat_frag)
    v2(?:/(?:PAP\-Person|PAP\-Company))?|v1(?:/(?:PAP\-Person|PAP\-Company|Meta))?

    >>> for e in ets2 :
    ...     r = root2.resource_from_href (e.href)
    ...     if r is None :
    ...         print ("No resource_from_href for", e.href, e)

"""

interactive_code = """

from _GTW._RST.Resource import *

e_types = \
    ( Dir
        ( name          = "PAP-Company"
        , description   = "Legal person"
        )
    , Dir
        ( name          = "PAP-Person"
        , description   = "Natural person"
        )
    ,
    )
root2 = Root ( HTTP = None
    , language          = "en"
    , entries           =
        ( Leaf
            ( name          = "about"
            , implicit      = True
            )
        , Dir
            ( name          = "v1"
            , description   = "Version 1 of test RESTful api"
            , entries       =
                ( Dir
                    ( name          = "Meta"
                    , description   = "Meta information about RESTful api"
                    )
                ,
                ) + e_types
            )
        , Dir
            ( name          = "v2"
            , entries       = list (e_types)
            )
        )
    )

"""

### __END__ GTW.RST.__test__
