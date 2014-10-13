# -*- coding: utf-8 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
