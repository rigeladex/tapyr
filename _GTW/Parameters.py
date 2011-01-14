# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW.Parameters
#
# Purpose
#    Support definition of parameters for media, i.e., CSS and JS, fragments
#
# Revision Dates
#    14-Jan-2011 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

from   _TFL._Meta.Property        import Lazy_Property
from   _TFL._Meta.Once_Property   import Once_Property

import _TFL._Meta.Object
import _TFL.Caller
import _TFL.Filter
import _TFL.Q_Exp

import itertools

P = TFL.Attr_Query ()

def ddict (* ds) :
    result = {}
    for d in ds :
        result.update (d)
    return result
# end def ddict

class P_dict (TFL.Q_Exp.Q_Root) :
    """Parameter dict: supports lazy evaluation of dict arguments."""

    def __init__ (self, * args, ** kw) :
        self.args = args
        self.kw   = kw
    # end def __init__

    def __call__ (self, P) :
        result = {}
        Q_Root = TFL.Q_Exp.Q_Root
        for a in self.args :
            if isinstance (a, Q_Root) :
                a = a (P)
            result.update (a)
        for k, v in self.kw.iteritems () :
            if isinstance (v, Q_Root) :
                v = v (P)
            result [k] = v
        return result
    # end def __call__

# end class P_dict

class M_Definition (TFL.Meta.Object.__class__) :
    """Meta class for `Definition`."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        bn = tuple (reversed ([getattr (b, "_nested_", {}) for b in bases]))
        cls._nested_ = _nested_ = ddict (* bn)
        Q_Root = TFL.Q_Exp.Q_Root
        for k, v in dct.iteritems () :
            if isinstance (v, Q_Root) :
                setattr (cls, k, Lazy_Property (k, v))
            elif isinstance (v, M_Definition) :
                _nested_ [k] = v
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = cls.__m_super.__call__ (* args, ** kw)
        for k, v in cls._nested_.iteritems () :
            setattr (result, k, v (R = result))
        return result
    # end def __call__

# end class M_Definition

class Definition (TFL.Meta.Object) :
    """Definition of parameters for media, i.e., CSS and JS, fragments.

    >>> class Defaults (Definition) :
    ...   foo = 1
    ...   bar = P.foo * 2
    ...   class nav_col (Definition) :
    ...     bar = 42
    ...     baz = 0
    ...     class own_links (Definition) :
    ...       qux = P.R.bar * 2
    ...       quy = P.T.bar * 2
    ...       quz = P.T.foo * 0.5
    ...     spec = P_dict (a = P.bar)
    ...
    >>> class App (Defaults) :
    ...   foo = 2
    ...   class nav_col (Defaults.nav_col) :
    ...     bar = 137
    ...
    >>> D = Defaults ()
    >>> E = App ()
    >>> D.foo, E.foo
    (1, 2)
    >>> D.bar, E.bar
    (2, 4)
    >>> D.nav_col.own_links.qux, E.nav_col.own_links.qux
    (84, 274)
    >>> D.nav_col.own_links.quy, E.nav_col.own_links.quy
    (4, 8)
    >>> D.nav_col.own_links.quz, E.nav_col.own_links.quz
    (0.5, 1.0)
    >>> D.nav_col.spec, E.nav_col.spec
    ({'a': 42}, {'a': 137})
    """

    __metaclass__ = M_Definition

    def __init__ (self, R = None) :
        self.R = R
    # end def __init__

    @Once_Property
    def T (self) :
        R = self.R
        if R is not None :
            return R.T
        else :
            return self
    # end def T

# end class Definition

if __name__ != "__main__" :
    GTW._Export_Module ()
### __END__ GTW.Parameters
