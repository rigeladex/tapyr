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
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _TFL              import TFL

import _TFL._Meta.Single_Dispatch

import json

@TFL.Meta.Single_Dispatch
def default (o) :
    raise TypeError (repr (o) + " is not JSON serializable")
# end def default

json._default_encoder.default = default

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ json_dump
