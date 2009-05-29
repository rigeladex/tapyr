# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Model_Field_Man
#
# Purpose
#    Manager for the fields of a model
#
# Revision Dates
#    28-May-2009 (CT) Creation
#    29-May-2009 (CT) `finalize` changed to not override existing attributes
#    ««revision-date»»···
#--

from   _TFL                               import TFL
import _TFL._Meta.M_Class
import _TFL.NO_List

from   _DJO                               import DJO
import _DJO.Model_Field                   as     MF

import itertools

def _sort_key (x) :
    return getattr (x, "sort_key", x.creation_counter)
# end def _sort_key

class Model_Field_Man (TFL.Meta.Object) :
    """Manager for the fields of a model.

       Allows convenient access to fields of related models, too.
    """

    _finalized = False
    _extension = []

    def __init__ (self, model) :
        self._extension.append (self)
        self.model = model
        self.Own   = Own = self.All = TFL.NO_List ()
        fields = itertools.chain (model._meta.fields + model._meta.many_to_many)
        for f in sorted (fields, key = _sort_key) :
            Own.append (f)
    # end def __init__

    def finalize (self) :
        if self._finalized :
            return
        self._finalized = Model_Field_Man._finalized = True
        model           = self.model
        All  = self.All = TFL.NO_List ()
        for f in self.Own :
            if isinstance (f, MF.One_to_One) :
                ledom = f.rel.to
                ledom._F.finalize ()
                for g in ledom._F.All :
                    if g.name not in self.Own :
                        All.append (g)
                        self._setup_delegated_field (model, ledom, f, g)
                    else :
                        All.append (f)
            else :
                All.append (f)
    # end def finalize

    def _setup_delegated_field (self, model, ledom, field, dleif) :
        def _get (this) :
            l = getattr (this, field.name, None)
            if l is not None :
                return getattr (l, dleif.name)
        def _set (this, value) :
            l = getattr (this, field.name, None)
            if l is None :
                l = ledom ()
                setattr (this, field.name, l)
            if get (this) != value :
                setattr (l, dleif.name, value)
                this._save_callbacks.add (l.save)
        def _del (this) :
            l = getattr (this, field.name, None)
            if l is not None :
                setattr (l, dleif.name, dleif.Null)
        setattr \
            (model, dleif.name, property (_get, _set, _del, dleif.help_text))
    # end def _setup_delegated_field

    def __getattr__ (self, name) :
        d = self.All
        try :
            return d [name]
        except KeyError :
            raise AttributeError, name
    # end def __getattr__

    def __iter__ (self) :
        return iter (self.All)
    # end def __iter__

# end class Model_Field_Man

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Model_Field_Man
