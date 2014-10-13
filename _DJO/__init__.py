# -*- coding: utf-8 -*-
# Copyright (C) 2007-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    DJO.__init__
#
# Purpose
#    Package with Django specific classes and functions
#
# Revision Dates
#    14-Dec-2007 (CT) Creation
#    15-Dec-2007 (MG) Creation of `Package_Namespace` guarded to allow usage
#                     of the package without `TFL`
#    28-May-2009 (CT) Guard removed
#    28-May-2009 (CT) `AppCache._populate` monkey-patched to send signal
#                     `models_loaded`
#    29-May-2009 (CT) Monkeypatching removed
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
DJO = Package_Namespace ()
del Package_Namespace

from   _TFL.Decorator import Override_Method

from django.dispatch import Signal
DJO.models_loaded_signal = Signal ()

### __END__ DJO.__init__
