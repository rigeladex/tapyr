# -*- coding: utf-8 -*-
# Copyright (C) 2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    json_dump
#
# Purpose
#    Generic function for `default` argument of `json.dump`, `json.dumps`
#
# Revision Dates
#    13-Apr-2015 (CT) Creation
#     6-May-2015 (CT) Add `to_file`, `to_open_file`, `to_string`
#     6-May-2015 (CT) Add `add_date_time_serializers`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _TFL              import TFL

import _TFL._Meta.Single_Dispatch

import json

__date_time_serializers_added = False

def add_date_time_serializers () :
    """Add json serializers for `datetime.date`, `.datetime`, and `.time`."""
    if not __date_time_serializers_added :
        TFL.json_dump.__date_time_serializers_added = True
        import datetime
        @default.add_type (datetime.date, datetime.time)
        def json_encode_date_or_time (o) :
            return o.isoformat ()
        # end def json_encode_date_or_time

        @default.add_type (datetime.datetime)
        def json_encode_datetime (dt) :
            ### Don't use `isoformat` because its output structure varies
            ### depending on `microsecond` and is thus more difficult to parse
            return dt.strftime ("%Y-%m-%dT%H:%M:%S.%f")
        # end def json_encode_datetime
# end def add_date_time_serializers

@TFL.Meta.Single_Dispatch
def default (o) :
    """Generic function to serialize `o` as json-compatible type.

       Pass `default` to `json.dump` or `json.dumps`.
    """
    raise TypeError (repr (o) + " is not JSON serializable")
# end def default

def to_file (cargo, file_name, default = default, sort_keys = True, ** kw) :
    """Serialize `cargo` as a JSON formatted stream to a file name `file_name`.

       By default, use `TFL.json_dump.default` as serializer function and sort
       output of dictionaries by key.

       The arguments have the same meaning as in `json.dump`.
    """
    with open (file_name, "wb") as fp :
        json.dump (cargo, fp, default = default, sort_keys = sort_keys, ** kw)
# end def to_file

def to_open_file (cargo, fp, default = default, sort_keys = True, ** kw) :
    """Serialize `cargo` as a JSON formatted stream to `fp` (a .write()-supporting file-like object).

       By default, use `TFL.json_dump.default` as serializer function and sort
       output of dictionaries by key.

       The arguments have the same meaning as in `json.dump`.
    """
    json.dump (cargo, fp, default = default, sort_keys = sort_keys, ** kw)
# end def to_open_file

def to_string (cargo, default = default, sort_keys = True, ** kw) :
    """Serialize `cargo` to a JSON `str`.

       By default, use `TFL.json_dump.default` as serializer function and sort
       output of dictionaries by key.

       The arguments have the same meaning as in `json.dump`.
    """
    return json.dumps (cargo, default = default, sort_keys = sort_keys, ** kw)
# end def to_string

__doc__ = """
Module `json_dump`
===================

This modules provides functions to customize json serialization.

.. function:: default(o)

  Return `o` serialized in a format usable as json or raise a TypeError.

  `default` is a generic function that can be specialized for specific
  types. For instance::

      @default.add_type (datetime.date)
      def json_encode_date (o) :
          return str (o)

.. autofunction:: add_date_time_serializers

.. autofunction:: to_file(cargo, file_name, default = 'default', sort_keys = True, ** kw)

.. autofunction:: to_open_file(cargo, fp, default = 'default', sort_keys = sort_keys, ** kw)

.. autofunction:: to_string(cargo, default = 'default', sort_keys = True, ** kw)

Examples::

    >>> import datetime
    >>> dt = datetime.datetime (2015, 5, 6, 12, 50)

    >>> print (to_string (dt))
    Traceback (most recent call last):
    ...
    TypeError: datetime.datetime(2015, 5, 6, 12, 50) is not JSON serializable

    >>> add_date_time_serializers ()
    >>> print (to_string (dt))
    "2015-05-06T12:50:00.000000"

"""

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ json_dump
