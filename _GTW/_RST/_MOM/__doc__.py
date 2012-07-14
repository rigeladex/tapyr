# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.MOM.
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
#    GTW.RST.MOM.__doc__
#
# Purpose
#    Documentation for package GTW.RST.MOM
#
# Revision Dates
#    14-Jul-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW._RST._MOM.import_MOM import *

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

Package `GTW.RST.MOM`
======================

This package provides classes implementing a generic `RESTful web service`_
for an application based on the MOM meta object model.

A RESTful web service is a set of URLs, each URL referring to a specific
resource and supporting one or more of the `standard HTTP methods`_. At a
minimum, each resource supports the safe HTTP methods `GET`, `HEAD`, and
`OPTIONS`. Some resources also support HTTP methods with side effects, such
as `DELETE`, `POST`, and `PUT`.

The `OPTIONS` methods returns the list of HTTP methods supported by the
specified resource.

Depending on the setup, a RESTful web service implemented by `GTW.RST.MOM`
provides access to one or more databases, each holding a different instance
of a MOM model. In the following documentation, we'll assume the simplest
case of just a single database, with the web service mapped to `/`.

`Scope`
-------

For a specific database, the top URL of the RESTful web service refers to a
so-called `Scope`. The scope provides access to all essential entity types,
aka `E-Types`, that comprise the object model. The scope does not support
HTTP methods with side effects.

Use the HTTP method `GET` to retrieve the list of `E-Types` defined by the
`scope`. `GET` returns a `JSON`_ object with the attribute `entries` listing
the URLs or URL fragments of the scopes `e-types`.

For instance, the elided result of a `GET` request for the URL `/&verbose`
might look like::

        { 'entries' :
            [ '/MOM-Id_Entity'
            , '/MOM-Link'
            , '/MOM-Link1'
            , '/MOM-Link2'
            , '/MOM-Object'
            , '/PAP-Address'
            , '/PAP-Subject'
            , '/PAP-Company'
            , '/PAP-Email'
            , '/PAP-Phone'
            , '/PAP-Person'
            , '/PAP-Subject_has_Property'
            , '/PAP-Subject_has_Address'
            , '/PAP-Company_has_Address'
            , '/PAP-Subject_has_Email'
            , '/PAP-Company_has_Email'
            , '/PAP-Subject_has_Phone'
            , '/PAP-Company_has_Phone'
            , '/PAP-Person_has_Address'
            , '/PAP-Person_has_Email'
            , '/PAP-Person_has_Phone'
            ]
        }

`E-Type`
---------

An `E-Type` describes a specific essential entity type of a MOM model. The
RESTful resource for a `e-type` allows read and write access to all instances
of the `e-type` in question.

`GET`
~~~~~

Use the HTTP method `GET` to retrieve the list of instances of the `e-type`.
`GET` without any parameters returns a `JSON`_ object with the attribute
`entries` listing the permanent ids, aka `pids`, of the instances of the
`e-type`. `GET` with the query parameter `verbose` returns a `JSON`_ object
with the attributes:

- `attribute_names`: the list of attribute names for instances of the
  `e-type`.

- `entries`: the list of instances; for each instance a JSON object
  containing:

  * `pid`: permanent id of instance.

  * `cid`: id of last change.

  * `attributes`: JSON object mapping attribute names to values.

    - if the value of an attribute refers to an instance of another `e-type`,
      only the pid is returned, unless the `GET` request contained the query
      parameter `closure`, in which case a nested JSON object with the
      information about the nested object is returned here.

  * `type_name`: name of essential entity type.

  * `url`: URL of resource referring to this instance.

For instance (using the Python package `requests`_)::

    >>> requests.get ("/PAP-Person").json
    { 'entries' :
        [ 1
        , 2
        , 3
        ]
    , 'url_template' : '/PAP-Person/{entry}'
    }

    >>> requests.get ("/PAP-Person?verbose").json
    { 'attribute_names' :
        [ 'last_name'
        , 'first_name'
        , 'middle_name'
        , 'title'
        , 'lifetime'
        , 'salutation'
        , 'sex'
        ]
    , 'entries' :
        [ { 'attributes' :
              { 'first_name' : 'Christian'
              , 'last_name' : 'Tanzer'
              , 'middle_name' : ''
              , 'title' : ''
              }
          , 'cid' : 1
          , 'pid' : 1
          , 'type_name' : 'PAP.Person'
          , 'url' : '/PAP-Person/1'
          }
        ...
        ]
    }

You can use additional query parameters to restrict the number of instances
returned or to search for specific instances. Possible query parameters are:

- `count`: Return just the count, not the list, of instances.

- `limit`: Restrict the number of instances to the value specified.

- `offset`: Number of first instance to return; can be used together with
  `limit` and `order_by` to iterate over all instances.

- `order_by`: Criteria used to sort the `results`; comma separated list of
  attribute names and/or `pid`. Each criterion may be preceded by `-` to
  sort the results in descending direction for that criterion.

- `strict`: Limit the results to strict instances of the e-type in question,
  i.e., don't include instances of derived e-types. If you specify `strict`
  for a partial, aka abstract, e-type you'll get an empty list of results.

- `AQ`: restrict results to those matching the attribute query specified. The
  value for this query parameter is a comma-separated tuple of attribute
  name, operation, and value.

  Possible operations include:

  * `EQ`: equal

  * `NE`: not equal

  * `GE`: greater than or equal

  * `GT`: greater than

  * `LE`: less than or equal

  * `LT`: less than

  * `CONTAINS`: attribute value contains the specified query value

  * `ENDSWITH`: attribute value ends with the specified query value

  * `STARTSWITH`: attribute value starts with the specified query value

- `FIRST`: Results start with first instance, according to `order_by`.

- `LAST`: Results end with last instance, according to `order_by`.


`POST`
~~~~~~

Use the HTTP method `POST` to create a new instance of the `e-type`. The
request body for the `POST` must be a JSON object with the attribute
`attributes` which in turn must be a JSON object that maps attribute names to
attribute values.

For instance::

    >>> cargo = json.dumps (
    ...   dict
    ...     ( attributes = dict
    ...         ( last_name   = "Dog"
    ...         , first_name  = "Snoopy"
    ...         , middle_name = "the"
    ...         , lifetime    = dict (start = "20001122")
    ...         )
    ...     )
    ... )
    >>> headers = { "Content-Type": "application/json" }
    >>> requests.post ("/PAP-Person", data = cargo, headers = headers).json
    { 'attributes' :
        { 'first_name' : 'Snoopy'
        , 'last_name' : 'Dog'
        , 'lifetime' :
            [
              [ 'start'
              , '2000/11/22'
              ]
            ]
        , 'middle_name' : 'the'
        , 'title' : ''
        }
    , 'cid' : 17
    , 'pid' : 17
    , 'type_name' : 'PAP.Person'
    , 'url' : '/PAP-Person/17'
    }

A successful `POST` request returns a JSON object describing the newly
created instance. This JSON object has the same format as the result of a
`GET` request for the instance.

`Instance`
--------------

The RESTful resource for an instance allows read and write access to the
instance. For HTTP methods with side effects, you need to pass the `cid` of
the instance as returned by a `GET` method.

`GET`
~~~~~

Use the HTTP method `GET` to retrieve the value of the instance. `GET`
returns a `JSON`_ object with the same structure as a `verbose` `GET` applied
to the resource of the instance's e-type.

For instance::

    >>> requests.get ("/PAP-Person/1")
    { 'attributes' :
        { 'first_name' : 'Christian'
        , 'last_name' : 'Tanzer'
        , 'middle_name' : ''
        , 'title' : ''
        }
    , 'cid' : 1
    , 'pid' : 1
    , 'type_name' : 'PAP.Person'
    , 'url' : '/PAP-Person/1'
    }

`PUT`
~~~~~

Use the HTTP method `PUT` to change the value of an instance. The
request body for the `PUT` must be a JSON object with the attributes:

- `cid`: the id of the last change of the instance, as returned by a previous
  `GET` (or possibly `POST`) request.

  If the `cid` of the instance has changed in the meantime, the `PUT` request
  will fail with a HTTP status code of 409.

- `attributes`: a JSON object that maps attribute names to
  changed attribute values. Attributes not listed in `attributes` are not
  changed by the `PUT` request.

`DELETE`
---------

Use the HTTP method `DELETE` to remove the instance from the database; this
will also remove all links to the instance in question. You need to pass
`cid` as query parameter. If the `cid` of the instance has changed in the
meantime, the `DELETE` request will fail with a HTTP status code of 409.


.. _`RESTful web service`: http://en.wikipedia.org/wiki/Representational_State_Transfer
.. _`standard HTTP methods`: http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods
.. _`JSON`: http://en.wikipedia.org/wiki/JSON
.. _`requests`: http://pypi.python.org/pypi/requests

"""

### __END__ GTW.RST.MOM.__doc__
