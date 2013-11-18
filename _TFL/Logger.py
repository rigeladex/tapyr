# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    TFL.Logger
#
# Purpose
#    A small helper simplifying logger creation
#
# Revision Dates
#    13-Sep-2009 (MG) Creation
#    11-Jan-2010 (CT) Esthetics
#    ««revision-date»»···
#--

from   _TFL import TFL

import logging

CRITICAL = logging.CRITICAL
FATAL    = logging.FATAL
ERROR    = logging.ERROR
WARNING  = logging.WARNING
WARN     = logging.WARN
INFO     = logging.INFO
DEBUG    = logging.DEBUG
NOTSET   = logging.NOTSET

def Create \
        ( name
        , format   = "%(message)s"
        , date_fmt = None
        , level    = DEBUG
        ) :
    formatter = logging.Formatter     (format, date_fmt)
    handler   = logging.StreamHandler ()
    logger    = logging.getLogger     (name)
    logger.setLevel      (level)
    handler.setLevel     (level)
    handler.setFormatter (formatter)
    logger.addHandler    (handler)
    return logger
# end def Create

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Logger
