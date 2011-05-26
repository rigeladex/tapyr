# -*- coding: iso-8859-15 -*-
# Copyright (C) 2007-2009 Mag. Christian Tanzer. All rights reserved
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
