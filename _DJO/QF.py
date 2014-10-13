# -*- coding: utf-8 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
