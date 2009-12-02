# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
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
#    MOM.EMS._Manager_
#
# Purpose
#    Base class for entity manager strategies
#
# Revision Dates
#     2-Dec-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS

import _TFL._Meta.Object
import _TFL.Q_Result

from   _TFL.I18N             import _, _T, _Tn

import itertools

class _Manager_ (TFL.Meta.Object) :
    """Base class for entity managers."""

    type_name          = "XXX"

    Q_Result           = TFL.Q_Result
    Q_Result_Composite = TFL.Q_Result_Composite

    def __init__ (self, scope) :
        self.scope = scope
    # end def __init__

    def count (self, Type, * filters, ** kw) :
        return self.query (Type, * filters, ** kw).count ()
    # end def count

    def exists (self, Type, epk) :
        epk_dict = dict (zip (Type.epk_sig, epk))
        entities = self.query (Type).filter (** epk_dict)
        scope    = self.scope
        result   = list (getattr (scope, e.type_name) for e in entities)
        return result
    # end def exists

    def instance (self, Type, epk) :
        root = Type.relevant_root
        if root :
            epk_dict = dict (zip (Type.epk_sig, epk))
            try :
                result = self.query (Type).filter (** epk_dict).one ()
            except IndexError :
                result = None
            else :
                if not isinstance (result, Type.Essence) :
                    result = None
            return result
        raise TypeError \
            ( "\n".join
                ( ( _T ("Cannot query `instance` of non-root type `%s`.")
                  , _T ("Use one of the types %s instead.")
                  )
                )
            % (Type.type_name, ", ".join (sorted (Type.relevant_roots)))
            )
    # end def instance

    def query (self, Type, * filters, ** kw) :
        root   = Type.relevant_root
        strict = kw.pop ("strict", False)
        if root :
            result = self._query_single_root (Type, root)
        else :
            result = self._query_multi_root (Type)
        if filters or kw :
            result = result.filter (* filters, ** kw)
        if strict :
            result = result.filter (type_name = Type.type_name)
        return result
    # end def query

    def r_query (self, Type, rkw, * filters, ** kw) :
        return self.query (Type, * filters, ** dict (rkw, ** kw))
    # end def r_query

    def _query_multi_root (self, Type) :
        raise NotImplementedError \
            ("%s needs to define %s" % (self.__class__, "_query_multi_root"))
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        raise NotImplementedError \
            ("%s needs to define %s" % (self.__class__, "_query_single_root"))
    # end def _query_single_root

# end class _Manager_

if __name__ != "__main__" :
    MOM.EMS._Export ("_Manager_")
### __END__ MOM.EMS._Manager_
