# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
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
#    MOM.EMS.SA
#
# Purpose
#    Entity manager strategy using SQLAlchemy session as storeage
#
# Revision Dates
#    16-Oct-2009 (MG) Creation
#    25-Oct-2009 (MG) Updated to support inheritance
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    03-Dec-2009 (MG) Use `MOM.DBW.SA.Q_Result`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS._Manager_
import _MOM.Entity
import _MOM._DBW._SA.Q_Result
import _TFL._Meta.Object

import _TFL.defaultdict

import itertools

from   sqlalchemy import exc as SA_Exception

class Manager (MOM.EMS._Manager_) :
    """Entity manager using hash tables to hold entities."""

    type_name = "SA"

    Q_Result  = MOM.DBW.SA.Q_Result

    def add (self, entity) :
        ses = self.session
        ses.flush () ### add all pending operations to the database transaction
        max_c = entity.max_count
        if max_c and max_c <= self.s_count (entity.Essence) :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        try :
            ses.add   (entity)
            ses.flush ()
        except SA_Exception.IntegrityError as exc :
            ses.rollback ()
            raise MOM.Error.Name_Clash \
                (entity, self.instance (entity.__class__, entity.epk))
    # end def add

    def remove (self, entity) :
        self.session.delete (entity)
        self.session.flush  () ### needed to update auto cache roles
    # end def remove

    def rename (self, entity, new_epk, renamer) :
        old_entity = self.instance (entity.__class__, new_epk)
        if old_entity :
            raise MOM.Error.Name_Clash (entity, old_entity)
        renamer     ()
    # end def rename

    def _query_multi_root (self, Type) :
        QR = self.Q_Result
        S  = self.session
        return self.Q_Result_Composite \
            ([QR (t, S.query (t)) for t in Type.relevant_roots.itervalues ()])
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        return self.Q_Result (Type, self.session.query (Type))
    # end def _query_single_root

    def __iter__ (self) :
        relevant_roots = self.scope.MOM.Id_Entity.relevant_roots.itervalues ()
        return itertools.chain \
            (* (self.query (rr).all () for rr in relevant_roots))
    # end def __iter__

# end class Manager

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.SA
