# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck All rights reserved
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
#    MOM.DBW.SA.Filter
#
# Purpose
#    Extend FTL.Filter to support the generation of the SQLAlchemy specific
#    filter/order_by clauses
#
# Revision Dates
#     1-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL.Filter
import _TFL.Decorator

@TFL.Add_To_Class ("_sa_filter", TFL.Attr_Filter)
def _sa_filter (self, e_type) :
    return getattr (getattr (e_type, self.attr_name), self.operation.__name__) \
        (* self.attr_args, ** self.attr_kw)
# end def _sa_filter

### __END__ MOM.DBW.SA.Filter


