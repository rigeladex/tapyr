# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@smangari.org
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
#    model_1.models
#
# Purpose
#    A test model to test the `admin` features
#
# Revision Dates
#     8-Oct-2008 (MG) Creation
#    ««revision-date»»···
#--

from   __future__                 import with_statement

from   _DJO                       import DJO
### import _DJO.Admin
import _DJO.Forms
import _DJO.Models
import _DJO.Model_Field           as     MF

from   _TFL.Decorator             import Attributed
from   _TFL.Function              import Function

import datetime

from   django.db                  import models
from   django.contrib.auth.models import User
from   django.template            import defaultfilters

class News (DJO.Model) :
    """A imple news entry model."""

    class Meta :
        verbose_name_plural = "news"
    # end class Meta

    title    = MF.Char ( "Titel", max_length   = 80)
    text     = MF.Text ()
    creator  = models.ForeignKey \
        ( User
        , blank        = True
        , editable     = False
        , null         = True
        , verbose_name = "Eingabe durch"
        )
    date_cre = MF.Date_Time \
        ( "Eingabe-Datum"
        , blank        = True
        , editable     = False
        , null         = True
        )
    date_pub = MF.Date_Time \
        ( "Erscheinungs-Datum"
        , blank        = True
        , null         = True
        )
    author   = MF.Char     \
        ( "Autor"
        , blank        = True
        , max_length   = 80
        )
# end class News

### __END__ model_1.models


