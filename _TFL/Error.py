# -*- coding: utf-8 -*-
# Copyright (C) 2008-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Error
#
# Purpose
#    Provide exception classes for TFL package namespace
#
# Revision Dates
#     3-Apr-2008 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                import TFL

class Not_A_File              (Exception) : pass
class Not_A_Dir               (Exception) : pass
class Sync_Conflict           (Exception) : pass
class Already_Open            (Exception) : pass
class Not_Open                (Exception) : pass
class Could_Not_Delete_Old_DB (Exception) : pass

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Error
