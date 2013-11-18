# -*- coding: utf-8 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    DJO.QF
#
# Purpose
#    Encapsulate query filters
#
# Revision Dates
#    16-Jan-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                               import TFL
from   _DJO                               import DJO

from   django.db.models import Q as QF

def _isnull_p (a) :
    return {("%s__isnull" % a) : True}
# end def _isnull_p

def _isempty_p (a) :
    return {("%s__exact" % a) : ""}
# end def _isempty_p

def _QF_opt (p, ** kw) :
    result = None
    for k, v in kw.iteritems () :
        a = k.split ("__", 1)
        q = QF (** p (a)) | QF (** {k : v})
        if result is None :
            result = q
        else :
            result = result & q
    return result
# end def _QF_opt

def QF_o (** kw) :
    """Query filter for optional attribute(s)"""
    return _QF_opt (_isnull_p, ** kw)
# end def QF_o

def QF_s (** kw) :
    """Query filter for optional string-valued attribute(s)"""
    return _QF_opt (_isempty_p, ** kw)
# end def QF_s

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.QF
