# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
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
# ****************************************************************************
#
#++
# Name
#    GTW.Form.Plain
#
# Purpose
#    Simple form's not bound to a MOM instance
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    02-Feb-2010 (MG) `_get_raw`: pass form to `field.get_raw`
#     4-Feb-2010 (MG) `_get_raw` removed
#    18-Feb-2010 (MG) `M_Plain.New`: setup of `fields` added
#    19-Feb-2010 (MG) `__call__` change to calculate the error count
#    22-Feb-2010 (CT) `Instance.__init__` changed to pass `** kw` to `super`
#    23-Feb-2010 (MG) `__init__` fixed
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.I18N
import _TFL._Meta.Object
import _TFL.defaultdict
import _TFL.predicate

from   _GTW               import GTW
import _GTW._Form._Form_
import _GTW._Form.Widget_Spec

class M_Plain (GTW.Form._Form_.__class__) :
    """Meta class for plain forms"""

    def New ( cls
            , name_or_creator
            , * field_group_descriptions
            , ** kw
            ) :
        name         = name_or_creator
        creator      = None
        if TFL.callable (name_or_creator) :
            name     = name_or_creator.__name__
            creator  = name_or_creator
        field_groups = []
        for fgd in field_group_descriptions :
            field_groups.extend (fgd ())
        return cls.__m_super.New \
            ( name
            , fields       = cls._setup_fields (field_groups)
            , field_groups = field_groups
            , creator      = creator
            , ** kw
            )
    # end def New

# end class M_Plain

class Plain (GTW.Form._Form_) :
    """A plain form with no object in the background"""

    __metaclass__ = M_Plain
    widget        = GTW.Form.Widget_Spec ("html/jorm.jnj, object")
    parent        = None

    def __init__ (self, action, instance = None, ** kw) :
        self.__super.__init__ (instance, ** kw)
        self.action = action
    # end def __init__

    def get_required (self, field, error = None) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        value     = self.get_raw (field)
        if not value :
            error = error or TFL.I18N._T \
                (u"Field `%(field)s` is required")
            self.field_errors [field.name].append \
                (error % dict (field = field.name))
        return value
    # end def get_required

    def _validate (self) :
        return 0
    # end def _validate

    def __call__ (self, request_data) :
        self.request_data = request_data
        self._validate ()
        error_count = len (self.errors)
        if not error_count and self.creator :
            if not self.instance :
                self.instance = self.creator (** self.request_data)
            else :
                for name, value in self.request_data.iteritems () :
                    setattr (self.instance, name, value)
        return error_count
    # end def __call__

# end class Plain

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Plain


