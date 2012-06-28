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

    >>> e_types = ( Node
    ...         ( name          = "PAP.Company"
    ...         , description   = "Legal person"
    ...         , entries       =
    ...             ( Leaf (name = "1")
    ...             ,
    ...             )
    ...         )
    ...     , Node
    ...         ( name          = "PAP.Person"
    ...         , description   = "Natural person"
    ...         )
    ...     ,
    ...     )
    >>> root = Root ( HTTP = None
    ...     , language          = "en"
    ...     , entries           =
    ...         ( Leaf
    ...             ( name          = "about"
    ...             )
    ...         , Node
    ...             ( name          = "v1"
    ...             , description   = "Version 1 of test RESTful api"
    ...             , entries       =
    ...                 ( Node
    ...                     ( name          = "Meta"
    ...                     , description   = "Meta information about RESTful api"
    ...                     )
    ...                 ,
    ...                 ) + e_types
    ...             )
    ...         )
    ...     )
    >>> print (formatted (e_types))
    (
      ( <class '_GTW._RST.Resource.Node'>
      , ()
      , { 'description' : 'Legal person'
        , 'entries' :
            (
              ( <class '_GTW._RST.Resource.Leaf'>
              , ()
                , { 'name' : '1' }
              )
            )
        , 'name' : 'PAP.Company'
        }
      )
    ,
      ( <class '_GTW._RST.Resource.Node'>
      , ()
      , { 'description' : 'Natural person'
        , 'name' : 'PAP.Person'
        }
      )
    )
    >>> root
    <Root : />
    >>> root.entries
    [<Leaf about: /about>, <Node v1: /v1>]

    >>> ets = tuple (root.entries_transitive)
    >>> ets
    (<Leaf about: /about>, <Node v1: /v1>, <Node Meta: /v1/Meta>, <Node PAP.Company: /v1/PAP.Company>, <Leaf 1: /v1/PAP.Company/1>, <Node PAP.Person: /v1/PAP.Person>)

    >>> [e.name for e in ets]
    [u'about', u'v1', u'Meta', u'PAP.Company', u'1', u'PAP.Person']
    >>> [e.href for e in ets]
    [u'about', u'v1', u'v1/Meta', u'v1/PAP.Company', u'v1/PAP.Company/1', u'v1/PAP.Person']

    >>> root.entries [1]
    <Node v1: /v1>

    >>> root.entries [1].entries
    [<Node Meta: /v1/Meta>, <Node PAP.Company: /v1/PAP.Company>, <Node PAP.Person: /v1/PAP.Person>]

    >>> c = root.resource_from_href("/v1/PAP.Company")
    >>> c
    <Node PAP.Company: /v1/PAP.Company>
    >>> sorted (c.SUPPORTED_METHODS)
    ['GET', 'HEAD', 'OPTIONS']

    >>> show (root)
    <Root : /> parent = -, top = /
      <Leaf about: /about> parent = /, top = /
      <Node v1: /v1> parent = /, top = /
        <Node Meta: /v1/Meta> parent = /v1, top = /
        <Node PAP.Company: /v1/PAP.Company> parent = /v1, top = /
          <Leaf 1: /v1/PAP.Company/1> parent = /v1/PAP.Company, top = /
        <Node PAP.Person: /v1/PAP.Person> parent = /v1, top = /

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
    XHTML ('xhtml',) (u'application/xhtml+xml',)
    XML ('xml',) (u'text/xml', u'application/xml')

"""

interactive_code = """

from _GTW._RST.Resource import *

e_types = \
    ( Node
        ( name          = "PAP.Company"
        , description   = "Legal person"
        )
    , Node
        ( name          = "PAP.Person"
        , description   = "Natural person"
        )
    ,
    )
root = Root \
    ( HTTP              = None
    , language          = "en"
    , entries           =
        ( Leaf
            ( name          = "about"
            )
        , Node
            ( name          = "v1"
            , description   = "Version 1 of test RESTful api"
            , entries       =
                ( Node
                    ( name          = "Meta"
                    , description   = "Meta information about RESTful api"
                    )
                ,
                ) + e_types
            )
        )
    )

"""

### __END__ GTW.RST.__test__
