#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2001 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TFL/__init__
#
# Purpose
#    Initialize package `TFL`
#
# Revision Dates
#     3-Jul-2001 (CT) Creation (of comment)
#    22-Feb-2002 (CT) `_Export` for `Package_Namespace` added
#    27-Feb-2002 (CT) `TFL.Package_Namespace` assigned instead of using
#                     `_Export` (which leads to circular import again)
#    24-Jun-2002 (CT) Import `Package_Namespace` absolutely (i.e., from `_TFL`)
#    ««revision-date»»···
#--

from _TFL.Package_Namespace import Package_Namespace

TFL = Package_Namespace ()

### We Package_Namespace to `TFL` to avoid circular imports between TFL and
### Package_Namespace
TFL.Package_Namespace = Package_Namespace

del Package_Namespace

### __END__ TFL/__init__
