# -*- coding: utf-8 -*-
# Copyright (C) 2009-2014 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    MOM.import_MOM
#
# Purpose
#    Provide all imports necessary to define application-specific essential
#    classes based on the MOM meta object model
#
#    Usage:
#        from MOM.import_MOM import *
#
# Revision Dates
#    22-Oct-2009 (CT) Creation
#     7-Dec-2009 (CT) `Q` added
#    22-Dec-2009 (CT) `Sequence_Number` removed
#     4-May-2010 (CT) `Q` moved to `MOM.Attr.Type`
#     5-Jul-2011 (CT) `MOM.Attr.Selector` added
#    19-Jul-2011 (CT) `MOM.Q_Exp_Raw` added
#    15-Jun-2013 (CT) Import `Derived_PNS`
#     9-Sep-2014 (CT) Rename `MOM.Q_Exp_Raw` to `MOM.Q_Exp`
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM.App_Type
import _MOM.Entity
import _MOM.Error
import _MOM.Link
import _MOM.Object
import _MOM.Q_Exp
import _MOM.Scope

import _MOM._Attr.Selector

from   _MOM._Attr.Type  import *
from   _MOM._Attr       import Attr
from   _MOM._Pred       import Pred

import _MOM.Derived_PNS

### __END__ MOM.import_MOM
