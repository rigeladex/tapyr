#! /usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2001-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    10-Feb-2010 (MG) `BREAK` added
#     8-Apr-2010 (CT) `BREAK` removed
#    ««revision-date»»···
#--

from _TFL.Package_Namespace import Package_Namespace

TFL = Package_Namespace ()

### We Package_Namespace to `TFL` to avoid circular imports between TFL and
### Package_Namespace
TFL.Package_Namespace = Package_Namespace

del Package_Namespace

### __END__ TFL/__init__
