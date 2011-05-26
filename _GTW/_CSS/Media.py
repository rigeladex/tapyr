# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.CSS.
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
#    GTW.CSS.Media
#
# Purpose
#    Model CSS media type and queries
#
#    See: http://www.w3.org/TR/css3-mediaqueries/
#
# Revision Dates
#    30-Dec-2010 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._CSS

import _TFL._Meta.Object

from   _TFL._Meta.Once_Property   import Once_Property

class M_Media (TFL.Meta.Object.__class__) :
    """Meta class for media types and queries."""

    Nick = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.nick :
            cls.Nick [cls.nick] = cls
    # end def __init__

# end class M_Media

class _Media_ (TFL.Meta.Object) :
    """Base class for media types and queries."""

    __metaclass__   = M_Media

    nick            = None

# end class _Media_

class Expression (_Media_) :
    """Media query expression.

    >>> print MX ("color")
    (color)
    >>> print MX ("min_width", "1000px")
    (min-width: 1000px)
    """

    nick = "MX"

    def __init__ (self, feature, expr = None) :
        self.feature = feature.replace ("_", "-")
        self.expr    = expr
    # end def __init__

    def __str__ (self) :
        if self.expr is not None :
            return "(%s: %s)" % (self.feature, self.expr)
        else :
            return "(%s)" % (self.feature, )
    # end def __str__

# end class Expression

class Query (_Media_) :
    """Media query.

    >>> print Query ()
    <BLANKLINE>
    >>> print Query ("screen")
    screen
    >>> print MQ ("screen", "color", min_width = "1000px")
    screen and (color) and (min-width: 1000px)
    >>> print MQ ("all", "color", min_width = "1000px")
    (color) and (min-width: 1000px)
    >>> print MQ (MX ("color"), min_width = "1000px")
    (color) and (min-width: 1000px)

    Beware: skipping `type` and using strings for `* exprs` fails::

    >>> print MQ ("color", min_width = "1000px")
    color and (min-width: 1000px)
    """

    nick = "MQ"

    def __init__ (self, type = None, * exprs, ** kw) :
        if isinstance (type, Expression) :
            exprs = (type, ) + exprs
            type  = None
        self.type = type
        self.flag = kw.pop ("flag", None)
        self._setup_exprs  (exprs, kw)
    # end def __init__

    @property
    def type (self) :
        result = self._type
        if result and result.name == "all" :
            result = None
        return result
    # end def type

    @type.setter
    def type (self, value) :
        if value is not None :
            if not isinstance (value, Type) :
                value = Type (value)
        self._type = value
    # end def type

    def _setup_exprs (self, exprs, kw) :
        self.exprs = []
        add        = self.exprs.append
        for x in exprs :
            if isinstance (x, basestring) :
                x = (x, )
            if not isinstance (x, Expression) :
                x = Expression (* x)
            add (x)
        for f, e in sorted (kw.iteritems ()) :
            add (Expression (f, e))
    # end def _setup_exprs

    def __str__ (self) :
        type  = self.type
        parts = [str (type)] if type else []
        parts.extend (str (x) for x in self.exprs)
        result = " and ".join (parts)
        if result and self.flag :
            result = self.flag + " " + result
        return result
    # end def __str__

# end class Query

class Rule (_Media_) :
    """Media rule: block of CSS rules specific for a list of media queries.

    >>> from _GTW._CSS.Rule import R
    >>> r1 = R ("tr.row1", "div.row1", color = "grey", clear = "both")
    >>> r2 = R ("tr.row2", "div.row2", color = "blue", clear = "both")
    >>> print r1
    tr.row1, div.row1
      { clear : both
      ; color : grey
      }
    >>> print r2
    tr.row2, div.row2
      { clear : both
      ; color : blue
      }
    >>> qr = Rule (MQ ("screen", "color", min_width = "1000px"), rules = (r1, r2))
    >>> print qr
    @media screen and (color) and (min-width: 1000px)
      {
        tr.row1, div.row1
          { clear : both
          ; color : grey
          }
    <BLANKLINE>
        tr.row2, div.row2
          { clear : both
          ; color : blue
          }
      }
    """

    nick = "MR"

    def __init__ (self, * queries, ** kw) :
        assert queries
        self.queries = list (queries)
        self.rules   = list (self._pop_rules (kw))
        assert not kw
    # end def __init__

    def block (self) :
        return "\n\n".join (str (r) for r in self.rules_iter ())
    # end def block

    def rules_iter (self) :
        for r in self.rules :
            for x in r :
                yield x
    # end def rules_iter

    def _pop_rules (self, kw) :
        for r in kw.pop ("rules") :
            if r.media_rule is not None :
                r = r.copy ()
            r.media_rule = self
            r.base_level = 2
            yield r
    # end def _pop_rules

    def __iter__ (self) :
        yield self
    # end def __iter__

    def __str__ (self) :
        queries = tuple (str (s) for s in self.queries)
        ls      = sum   (len (s) for s in queries) + 2 * (len (queries) - 1)
        q_sep   = (",\n%s" % indent0) if (ls >= 80) else ", "
        return "@media %s\n  {\n%s\n  }" % (q_sep.join (queries), self.block ())
    # end def __str__

# end class Rule

class Type (_Media_) :
    """Media type.

    >>> print Type ("screen")
    screen
    >>> print Type ("all")
    all
    >>> Type ("screen") is Type ("screen")
    True
    >>> Type ("screen") is Type ("all")
    False
    >>> Type ("Screen")
    Traceback (most recent call last):
      ...
    ValueError: Screen
    """

    nick  = "MT"
    Table = {}

    def __new__ (cls, name) :
        if name != name.lower () :
            raise ValueError (name)
        if name in cls.Table :
            result = cls.Table [name]
        else :
            result = cls.Table [name] = super (Type, cls).__new__ (cls)
            result.name = name
        return result
    # end def __new__

    def __init__ (self, name) :
        self.name = name
    # end def __init__

    def __str__ (self) :
        return self.name
    # end def __str__

# end class Type

for _t in ("all", "screen", "print") :
    Type (_t)
del _t

_g = globals ()
_g.update (Type.Table)
_g.update (M_Media.Nick)

__all__ = tuple \
    (k for (k, v) in _g.iteritems () if isinstance (v, (M_Media, Type)))
del _g

if __name__ != "__main__" :
    GTW.CSS._Export_Module ()
### __END__ GTW.CSS.Media
