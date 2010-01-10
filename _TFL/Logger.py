# -*- coding: iso-8859-1 -*-
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
#    A small hellper which allows easy lagger creation
#
# Revision Dates
#    13-Sep-2009 (MG) Creation
#    ««revision-date»»···
#--

import logging

def Create ( name
           , format   = "%(message)s"
           , date_fmt = None
           , level    = logging.DEBUG
           ) :
    logger  = logging.getLogger     (name)
    handler = logging.StreamHandler ()
    logger. setLevel                (level)
    handler.setLevel                (level)
    # create formatter
    formatter = logging.Formatter   (format, date_fmt)
    handler.setFormatter            (formatter)
    logger.addHandler               (handler)
    return logger
# end def Create

CRITICAL = logging.CRITICAL
FATAL    = logging.FATAL
ERROR    = logging.ERROR
WARNING  = logging.WARNING
WARN     = logging.WARN
INFO     = logging.INFO
DEBUG    = logging.DEBUG
NOTSET   = logging.NOTSET

if __name__ != "__main__" :
    from _TFL import TFL
    TFL._Export_Module ()
### __END__ TFL.Logger
