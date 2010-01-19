# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
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
#    GTW.Form.MOM.Inline
#
# Purpose
#    Add a `Inline` object to a form
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

from   _GTW                                 import GTW
import _GTW._Form._MOM

class Inline (TFL.Meta.Object) :
    """A Inline `form` inside a real form."""

    def __init__ ( self, inline_description, inline_form_cls, parent = None) :
        self.inline_description = inline_description
        self.inline_form_cls    = inline_form_cls
        self.parent             = parent
    # end def __init__

    def clone (self, parent) :
        return self.__class__ \
            (self.inline_description, self.inline_form_cls, parent)
    # end def clone

    @TFL.Meta.Once_Property
    def inline_forms (self) :
        iform_cls     = self.inline_form_cls
        et_man        = iform_cls.et_man
        parent        = self.parent
        if parent.instance :
            instances = et_man.query \
                (** {self.own_role_name : parent.instance}).all ()
        else :
            instances = ()
        count = 0
        try :
            count = int (parent.get_field ().split (":") [1])
        except :
            pass
        form_count  = min \
            ( self.max_count
            , max
                ( self.min_count
                , len (instances) + self.min_empty
                , self.min_required
                , count
                )
            )
        result      = []
        prefix_fmt  = "%s-M%%s" % (et_man.type_base_name, )
        for no in xrange (form_count) :
            prefix   = prefix_fmt % no
            instance = None
            if no < len (instances) :
                instance = instances [no]
            result.append \
                (iform_cls (instance, prefix = prefix, parent = parent))
        return result
    # end def inline_forms

    def __call__ (self, request_data) :
        return sum (ifo (request_data) for ifo in self.inline_forms)
    # end def __call__

    def __getattr__ (self, name) :
        return getattr (self.inline_description, name)
    # end def __getattr__

# end class Inline

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline
