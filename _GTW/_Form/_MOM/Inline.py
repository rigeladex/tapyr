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
#    20-Jan-2010 (MG) Error handling added (includig checking of
#                     `min_required` and `max_count`)
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

from   _GTW                                 import GTW
import _GTW._Form.Field_Error
import _GTW._Form._MOM

class Inline (TFL.Meta.Object) :
    """A Inline `form` inside a real form."""

    def __init__ ( self, inline_description, inline_form_cls, parent = None) :
        self.inline_description = inline_description
        self.inline_form_cls    = inline_form_cls
        self.parent             = parent
        self.errors             = GTW.Form.Error_List ()
    # end def __init__

    def clone (self, parent) :
        return self.__class__ \
            (self.inline_description, self.inline_form_cls, parent)
    # end def clone

    def get_errors (self) :
        return self.errors
    # end def get_errors

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
        error_count   = 0
        correct_forms = 0
        for ifo in self.inline_forms :
            ifo_errors   = ifo (request_data)
            error_count += ifo_errors
            if not ifo_errors and ifo.instance :
                correct_forms += 1
        if correct_forms < self.min_required :
            self.errors.append \
                (u"At least %(min)d inline instances are required"
                  "(%(current)d)"
                % dict (current = correct_forms, min = self.min_required)
                )
        if correct_forms > self.max_count :
            self.errors.append \
                ( u"More that %(max)d instance specified (%(current)d)"
                % dict (current = correct_forms, min = self.max_count)
                )
        return error_count + len (self.errors)
    # end def __call__

    def __getattr__ (self, name) :
        return getattr (self.inline_description, name)
    # end def __getattr__

# end class Inline

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline
