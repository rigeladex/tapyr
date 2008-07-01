# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Admin
#
# Purpose
#    Augment Django admin classes
#
# Revision Dates
#     1-Jul-2008 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                               import TFL
import _TFL._Meta.M_Class

from   _DJO                               import DJO

from   django.contrib                     import admin

class M_AM_Form (TFL.Meta.M_Class, admin.ModelAdmin.form.__class__) :
    """Meta class for model admin form classes with support for `.__super`
       and `_real_name`.
    """
# end class M_AM_Form

class _DJO_AM_Form_ (admin.ModelAdmin.form) :
    """Model admin form class"""

    __metaclass__ = M_AM_Form
    _real_name    = "AM_Form"

AM_Form = _DJO_AM_Form_ # end class _DJO_AM_Form_

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Admin
