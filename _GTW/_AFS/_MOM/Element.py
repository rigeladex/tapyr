# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.MOM.Element
#
# Purpose
#    Model MOM-specific elements of AJAX-enhanced forms
#
# Revision Dates
#    23-Feb-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW._AFS.Element import *
import _GTW._AFS._MOM

class _MOM_Entity_ (Entity) :
    """Model a MOM-specific sub-form for a single entity."""

    _real_name = "Entity"

    def __call__ (self, arg, ** kw) :
        if isinstance (arg, type) :
            entity = None
            e_type = arg
        else :
            entity = arg
            e_type = entity.__class__
        result = dict \
            ( cid = getattr (entity, "cid", None)
            , pid = getattr (entity, "pid", None)
            )
        for c in self.children :
            result [c.id] = c (entity, e_type, ** kw)
        return result
    # end def __call__

# end class _MOM_Entity_

class _MOM_Entity_Link_ (Entity_Link, Entity) :
    """Model a MOM-specific sub-form for a link to entity in containing
       sub-form.
    """

    _real_name = "Entity_Link"

    def __call__ (self, entity, e_type, ** kw) :
        assoc = link = self._get_assoc (kw)
        if entity is not None :
            try :
                link = assoc.query (** { self.role_name : entity }).one ()
            except IndexError :
                pass
        return self.__super.__call__ (link, ** kw)
    # end def __call__

    def instance_call (self, link, ** kw) :
        return self.__super.__call__ (link, ** kw)
    # end def instance_call

    def _get_assoc (self, kw) :
        scope = kw ["scope"]
        return scope [self.type_name]
    # end def _get_assoc

Entity_Link = _MOM_Entity_Link_ # end class

class _MOM_Entity_List_  (Entity_List) :
    """Model a MOM-specific sub-form for a list of entities."""

    _real_name = "Entity_List"

    def __call__ (self, entity, e_type, ** kw) :
        proto  = self.proto
        result = []
        if isinstance (proto, Entity_Link) :
            if entity is not None :
                assoc  = self._get_assoc (kw)
                for link in assoc.query_s (** { self.role_name : entity }) :
                    ### XXX need to add a child for each link ???
                    result.append (proto.instance_call (link, ** kw))
        else :
            raise NotImplementedError ("%r for %r" % (proto, entity or e_type))
        return result
    # end def __call__

Entity_List = _MOM_Entity_List_ # end class

class _MOM_Field_ (Field) :
    """Model a MOM-specific field of an AJAX-enhanced form."""

    _real_name = "Field"

    def __call__ (self, entity, e_type, ** kw) :
        ### XXX allow `init` to be specified in `kw`
        attr   = e_type.attributes [self.name]
        result = dict \
            ( init = attr.get_raw (entity)
            )
        return result
    # end def __call__

Field = _MOM_Field_ # end class

class _MOM_Field_Composite_ (Field_Composite) :
    """Model a MOM-specific composite field of a AJAX-enhanced form."""

    _real_name = "Field_Composite"

    def __call__ (self, entity, e_type, ** kw) :
        attr     = e_type.attributes [self.name]
        c_type   = attr.C_Type
        c_entity = getattr (entity, self.name, None)
        result   = {}
        for c in self.children :
            result [c.id] = c (c_entity, c_type, ** kw)
        return result
    # end def __call__

Field_Composite = _MOM_Field_Composite_ # end class

if __name__ != "__main__" :
    GTW.AFS.MOM._Export_Module ()
### __END__ GTW.AFS.MOM.Element
