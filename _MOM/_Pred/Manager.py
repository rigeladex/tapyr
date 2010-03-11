# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Pred.Manager
#
# Purpose
#    Predicate manager for a specific instance of a MOM.Entity
#
# Revision Dates
#     1-Oct-2009 (CT) Creation (factored from TOM.Pred.Manager)
#    25-Nov-2009 (CT) `attr_map` added and used instead of `attr.invariant`
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    25-Feb-2010 (CT) `check_kind` changed to use `check_pred_p` of predicate
#                     instead of home-grown code
#    11-Mar-2010 (CT) `check_kind` change of `25-Feb` revoked
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Pred.Err_and_Warn_List
import _MOM.Error

import _TFL._Meta.Object

from   _TFL.predicate        import callable, dusplit

class Manager (TFL.Meta.Object) :
    """Predicate manager for instances of MOM entities (objects and links).
    """

    def __init__ (self, pred_spec) :
        self.pred_spec         = pred_spec
        self.pred_dict         = pred_spec._pred_dict
        self.pred_kind         = pred_spec._pred_kind
        self.syntax_checks     = pred_spec._syntax_checks
        self.attr_map          = pred_spec._attr_map
        self.reset_predicates  ()
    # end def __init__

    has_errors   = property (lambda s : any (s.errors.itervalues   ()))
    has_warnings = property (lambda s : any (s.warnings.itervalues ()))

    def reset_predicates (self) :
        self.errors   = errors   = {}
        self.warnings = warnings = {}
        for k in self.pred_kind.iterkeys () :
            errors   [k] = []
            warnings [k] = []
    # end def reset_predicates

    def check_all (self, obj, attr_dict = {}) :
        for k in self.pred_kind.iterkeys () :
            self.check_kind (k, obj, attr_dict)
        return MOM.Pred.Err_and_Warn_List (self.errors, self.warnings)
    # end def check_all

    def check_attribute (self, obj, attr, value) :
        result    = []
        attr_dict = {attr.name : value}
        for pn in self.attr_map [attr] :
            p = self.pred_dict.get (pn)
            if p :
                r = p.check_predicate (obj, attr_dict)
                if not r :
                    result.append (r.error)
        if callable (attr.check_syntax) :
            try :
                attr.check_syntax (obj, value)
            except MOM.Error.Attribute_Syntax_Error as exc :
                result.append (exc)
        return result
    # end def check_attribute

    def check_kind (self, kind, obj, attr_dict = {}) :
        errors   = self.errors   [kind] = []
        warnings = self.warnings [kind] = []
        attrs    = set (attr_dict)
        if attr_dict :
            check_pred_p = lambda pred : attrs.intersection (pred.attrs)
            get_attr_val = lambda attr : attr_dict.get (attr.name)
        else :
            check_pred_p = lambda pred : True
            get_attr_val = lambda attr : obj.raw_attr (attr.name)
        for rank in dusplit (self.pred_kind [kind], lambda p : p.rank) :
            for p in rank  :
                if check_pred_p (p) :
                    result = p.check_predicate (obj, attr_dict)
                    if not result :
                        if result.severe :
                            errors.append   (result.error)
                        else :
                            warnings.append (result.error)
            if errors :
                break
        if kind == "object" :
            for attr in self.syntax_checks :
                try :
                    value = get_attr_val (attr)
                    if value :
                        attr.check_syntax (obj, value)
                except MOM.Error.Attribute_Syntax_Error as exc :
                    errors.append (exc)
        return MOM.Pred.Err_and_Warn_List (errors, warnings)
    # end def check_kind

    def __getattr__ (self, name) :
        prefix = "check_"
        if name.startswith (prefix) :
            kind = name [len (prefix) : ]
            if kind in self.pred_kind :
                return ( lambda obj, attr_dict = {}
                       : self.check_kind (kind, obj, attr_dict)
                       )
            else :
                return lambda obj, attr_dict = {} : []
        raise AttributeError, name
    # end def __getattr__

# end class Manager

__doc__ = """
Class `MOM.Pred.Manager`
========================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Manager

  `MOM.Pred.Manager` manages the predicates of specific instances of an
  :class:`objects<_MOM.Object.Object>` and :class:`links<_MOM.Link.Link>` of
  essential object models. Each essential entity has its own predicate
  manager.

  The predicate manager provides methods for checking the various predicate
  kinds and manages the errors and warnings found during such checks.


"""

if __name__ != "__main__" :
    MOM.Pred._Export ("*")
### __END__ MOM.Pred.Manager
