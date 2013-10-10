# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer All rights reserved
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
#    TFL.Q_Exp
#
# Purpose
#    Query expression language
#
# Revision Dates
#     4-Dec-2009 (CT) Creation
#     7-Dec-2009 (CT) `Base.undef` and `Bin.undefs` added and used
#    10-Dec-2009 (CT) `Bin.__nonzero__` defined to raise a `TypeError` to
#                     avoid `Q.a < Q.b < Q.c` silently discarding `Q.a <`
#    10-Dec-2009 (CT) `Exp_B` added (and `_Exp_` factored),
#                     and used as base for `Bin_Bool`
#     9-Feb-2010 (CT) Support for queries of nested attributes added
#    10-Feb-2010 (CT) `ENDSWITH` and `STARTSWITH` changed to *not* use
#                     unbound methods of `str` (fail for unicode values, duh)
#    10-Feb-2010 (MG) Converted `lambda` in `startswith` and `endswith` to
#                     functions which have aproper `__name__` which is needed
#                     by the SA instrumentation
#    12-Feb-2010 (CT) `__nonzero__` added to `Base`, `Call`, and `_Exp_`
#     1-Sep-2010 (CT) Reflected binary operators added (__radd__ and friends)
#     2-Sep-2010 (CT) `Get.name`  changed to `Get._name` (ditto for
#                     `Get.getter`)
#    14-Dec-2010 (CT) `Exp.D`, `Exp.DT`, and `Q._Date_` added
#    14-Jan-2011 (CT) Common base `Q_Root` added to all query classes
#    14-Jan-2011 (CT) `Bin` and `__binary` changed to honor `reverse`
#    22-Jul-2011 (CT) `__call__` factored up to `Q_Root`
#    22-Jul-2011 (CT) `LOWER` (and `Func`) added
#    13-Sep-2011 (CT) All internal classes renamed to `_<<name>>_`
#    14-Sep-2011 (CT) `SUM` added
#    16-Sep-2011 (MG) `_SUM_._name` added
#    21-Sep-2011 (CT) `BETWEEN` changed to guard against `val is None`
#    22-Dec-2011 (CT) Change `_Bin_.__repr__` to honor `reverse`
#    22-Feb-2013 (CT) Use `TFL.Undef ()` not `object ()`
#    25-Feb-2013 (CT) Change `_Get_.predicate` to set `Q.undef.exc`
#     9-Jul-2013 (CT) Add support for unary minus (`_Una_Expr_`, `__neg__`)
#    11-Jul-2013 (CT) Add support for unary not   (`_Una_Bool_`, `__invert__`)
#    27-Jul-2013 (CT) Add `BVAR` to support bound variables
#    28-Jul-2013 (CT) Add `_BVAR_Get_.NEW`, `BVAR.bind`, `BVAR.predicate`
#    28-Jul-2013 (CT) Add `BVAR_Man`
#    30-Aug-2013 (CT) Fix `__div__`
#    30-Aug-2013 (CT) Add `display`
#    30-Aug-2013 (CT) Move `__invert__` up to `_Exp_Base_` (from `_Exp_`)
#    30-Aug-2013 (CT) Add and use `_una_bool`, `_una_expr`;
#                     add `_Bin_.Table`, `_Una_.Table`
#     5-Sep-2013 (CT) Change `_Func_` to inherit from `(_Call_, _Exp_)`,
#                     not `(_Exp_, _Call_)`; add `_Call_.Table`
#    25-Sep-2013 (CT) Remove `LOWER`, `_Func_`
#    30-Sep-2013 (CT) Remove obsolete `SET`
#    30-Sep-2013 (CT) Add `SELF`
#    10-Oct-2013 (CT) Factor `_derive_expr_class`
#    10-Oct-2013 (CT) Call `_derive_expr_class` for `_Call_` and `_Sum_`, too
#    11-Oct-2013 (CT) Factor `_Aggr_`, `_derive_aggr_class`, add `_Avg_`...
#    ««revision-date»»···
#--

"""
Module `Q_Exp`
===============

This module implements a query expression language::

    >>> from _TFL.Record import Record as R
    >>> from datetime import date, datetime
    >>> r1 = R (foo = 42, bar = 137, baz = 11, quux = R (a = 1, b = 200))
    >>> r2 = R (foo = 3,  bar = 9,   qux = "abcdef", d = date (2010, 12, 14), dt = datetime (2010, 12, 14, 11, 36))
    >>> r3 = R (foo = 42, bar = "AbCd", baz = "ABCD", qux = "abcd")
    >>> r4 = R (foo = 45)
    >>> q0 = Q.foo
    >>> q0._name
    'foo'
    >>> q0.predicate (r1)
    42

    >>> qm = - q0
    >>> qm
    - Q.foo
    >>> qm.predicate (r1)
    -42

    >>> q1 = Q.foo == Q.bar
    >>> q1, q1.lhs, q1.rhs, q1.op.__name__
    (Q.foo == Q.bar, Q.foo, Q.bar, '__eq__')
    >>> q1.lhs._name, q1.rhs._name
    ('foo', 'bar')
    >>> q1.predicate (r1)
    False

    >>> q2 = Q.foo + Q.bar
    >>> q2, q2.lhs, q2.rhs, q2.op.__name__
    (Q.foo + Q.bar, Q.foo, Q.bar, '__add__')
    >>> q2.predicate (r1)
    179

    >>> q3 = Q.foo % Q.bar == Q.baz
    >>> q3, q3.lhs, q3.rhs
    (Q.foo % Q.bar == Q.baz, Q.foo % Q.bar, Q.baz)
    >>> q3.predicate (r1)
    False
    >>> q4 = Q.bar % Q.foo
    >>> q4.predicate (r1), Q.baz.predicate (r1)
    (11, 11)
    >>> (q4 == Q.baz).predicate (r1)
    True
    >>> (~ (q4 == Q.baz)).predicate (r1)
    False

    >>> q3.lhs.predicate (r1)
    42

    >>> q5 = Q.foo.BETWEEN (10, 100)
    >>> q5, q5.lhs, q5.args, q5.op.__name__
    (Q.foo.between (10, 100), Q.foo, (10, 100), 'between')
    >>> q5.predicate (r1)
    True
    >>> q5.predicate (r2)
    False

    >>> q6 = Q.foo.IN ((1, 3, 9, 27))
    >>> q6.predicate (r1)
    False
    >>> q6.predicate (r2)
    True

    >>> QQ = Q.__class__ (Ignore_Exception = (AttributeError, ))
    >>> QQ.qux.predicate (r1) is QQ.undef
    True
    >>> Q.qux.predicate (r1) is Q.undef
    Traceback (most recent call last):
      ...
    AttributeError: qux

    >>> q7 = QQ.qux.CONTAINS ("bc")
    >>> q7.predicate (r1)
    >>> q7.predicate (r2)
    True
    >>> q8 = QQ.qux.ENDSWITH ("fg")
    >>> q8.predicate (r1)
    >>> q8.predicate (r2)
    False
    >>> q9 = QQ.qux.ENDSWITH ("ef")
    >>> q9.predicate (r1)
    >>> q9.predicate (r2)
    True

    >>> qa = QQ.qux.STARTSWITH ("abc")
    >>> qa.predicate (r1)
    >>> qa.predicate (r2)
    True

    >>> Q [0] ((2,4))
    2
    >>> Q [1] ((2,4))
    4
    >>> Q [-1] ((2,4))
    4
    >>> Q [-2] ((2,4))
    2

    >>> Q.foo * -1
    Q.foo * -1
    >>> -1 * Q.foo
    -1 * Q.foo

    >>> qm = Q.foo.D.MONTH (2, 2010)
    >>> qm, qm.lhs, qm.op.__name__
    (Q.foo.between (datetime.date(2010, 2, 1), datetime.date(2010, 2, 28)), \
        Q.foo, 'between')

    >>> Q.foo.D.MONTH (2, 2000)
    Q.foo.between (datetime.date(2000, 2, 1), datetime.date(2000, 2, 29))

    >>> Q.foo.DT.QUARTER (4, 2010)
    Q.foo.between (datetime.datetime(2010, 10, 1, 0, 0), \
      datetime.datetime(2010, 12, 31, 23, 59, 59))

    >>> Q.foo.D.YEAR (2011)
    Q.foo.between (datetime.date(2011, 1, 1), datetime.date(2011, 12, 31))
    >>> Q.foo.DT.YEAR (2012)
    Q.foo.between (datetime.datetime(2012, 1, 1, 0, 0), \
        datetime.datetime(2012, 12, 31, 23, 59, 59))

    >>> Q.d.D.MONTH (12, 2010) (r2)
    True
    >>> Q.d.D.MONTH (1, 2010) (r2)
    False
    >>> Q.d.D.QUARTER (4, 2010) (r2)
    True
    >>> Q.dt.D.QUARTER (4, 2010) (r2)
    Traceback (most recent call last):
      ...
    TypeError: can't compare datetime.datetime to datetime.date
    >>> Q.dt.DT.QUARTER (4, 2010) (r2)
    True

    >>> (Q.bar == Q.baz) (r3)
    False
    >>> Q.bar.STARTSWITH ("ab") (r3)
    False
    >>> Q.bar.CONTAINS ("bc") (r3)
    False

    >>> print ("%.3f" % ((Q.foo / 7) (r4), ))
    6.429
    >>> (Q.foo // 7) (r4)
    6
    >>> print ("%.3f" % ((70 / Q.foo) (r4), ))
    1.556
    >>> (70 // Q.foo) (r4)
    1

Python handles `a < b < c` as `(a < b) and (b < c)`. Unfortunately, there is
no way to simulate this by defining operator methods. Therefore,
`_Bin_.__nonzero__` raises a TypeError to signal that an expression like
`Q.a < Q.b < Q.c` isn't possible::

    >>> Q.a < Q.b < Q.c # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...

Query operators with boolean results, i.e., equality and ordering operators,
cannot be used with any operators except `==` and `!=`::

    >>> (Q.a < Q.b) < Q.c
    Traceback (most recent call last):
      ...
    TypeError: Operator `<` not applicable to boolean result of `Q.a < Q.b`, rhs: `Q.c`

    >>> Q.a < Q.b + Q.c
    Q.a < Q.b + Q.c
    >>> Q.z + Q.a < Q.b + Q.c
    Q.z + Q.a < Q.b + Q.c
    >>> (Q.a < Q.b) == (Q.a % 2)
    Q.a < Q.b == Q.a % 2
    >>> (Q.a < Q.b) == (Q.a > 2)
    Q.a < Q.b == Q.a > 2
    >>> q = (Q.a < Q.b) == (Q.a % 2)
    >>> q.lhs
    Q.a < Q.b
    >>> q.rhs
    Q.a % 2
    >>> q.op
    <built-in function __eq__>

But explicit parenthesis are necessary in some cases::

    >>> Q.a < Q.b == Q.a % 2 # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...

Queries for nested attributes are also possible::

    >>> qn = Q.quux.a
    >>> qn._name
    'quux.a'
    >>> qn.predicate (r1)
    1
    >>> qm = Q.quux.b
    >>> qm.predicate (r1)
    200
    >>> (qn > Q.foo) (r1)
    False
    >>> (qm > Q.foo) (r1)
    True

Q.SUM needs documenting::

    >>> print (Q.SUM (1))
    Q.SUM (1)
    >>> print (Q.SUM (Q.finish - Q.start))
    Q.SUM (Q.finish - Q.start)

    >>> Q.SUM (1) (r1)
    1
    >>> Q.SUM (42) (r1)
    42
    >>> Q.SUM (Q.bar - Q.foo)  (r1)
    95
    >>> Q.SUM (Q.foo - Q.bar)  (r1)
    -95

`display` (also available as `TFL.Q.DISPLAY`) displays the structure of
q-expressions::

    >>> display (Q.foo < 42)
    '__lt__ (Q.foo, 42)'
    >>> display (42 <= Q.foo)
    '__ge__ (Q.foo, 42)'

    >>> display (Q.foo * 42)
    '__mul__ (Q.foo, 42)'
    >>> display (Q.foo / 42)
    '__truediv__ (Q.foo, 42)'
    >>> display (Q.foo // 42)
    '__floordiv__ (Q.foo, 42)'

    >>> display (42 / Q.foo)
    '__truediv__/r (Q.foo, 42)'
    >>> display (42 * Q.foo)
    '__mul__/r (Q.foo, 42)'

    >>> Q.DISPLAY (Q.foo % 2 == 0)
    '__eq__ (__mod__ (Q.foo, 2), 0)'
    >>> Q.DISPLAY (Q.foo % 2 == Q.bar * 3)
    '__eq__ (__mod__ (Q.foo, 2), __mul__ (Q.bar, 3))'
    >>> Q.DISPLAY (Q.foo % 2 == -Q.bar * 3)
    '__eq__ (__mod__ (Q.foo, 2), __mul__ (__neg__ (Q.bar), 3))'
    >>> Q.DISPLAY (- (Q.foo % 2 * -Q.bar / 3))
    '__neg__ (__truediv__ (__mul__ (__mod__ (Q.foo, 2), __neg__ (Q.bar)), 3))'

    >>> Q.DISPLAY (~ (Q.foo % 2 * -Q.bar / 3))
    '__not__ (__truediv__ (__mul__ (__mod__ (Q.foo, 2), __neg__ (Q.bar)), 3))'

    >>> Q.DISPLAY (Q.baz.STARTSWITH ("qux"))
    'Call:startswith: (Q.baz, qux)'

    >>> Q.DISPLAY (Q.foo.D.YEAR (2013))
    'Call:between: (Q.foo, 2013-01-01, 2013-12-31)'

    >>> Q.DISPLAY (Q.foo.IN ((1, 2, 3)))
    'Call:in_: (Q.foo, (1, 2, 3))'

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

"""

from   __future__                 import division, print_function

from   _TFL                       import TFL
from   _TFL.pyk                   import pyk

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Decorator
import _TFL.Undef

from   _TFL._Meta.Single_Dispatch import Single_Dispatch
from   _TFL.predicate             import callable

import operator

@pyk.adapt__bool__
class Base (TFL.Meta.Object) :
    """Query generator"""

    class Ignore_Exception (Exception) : pass

    expr_class_names = []
    undef            = TFL.Undef ("value")

    def __init__ (self, Ignore_Exception = None) :
        if Ignore_Exception is not None :
            self.Ignore_Exception = Ignore_Exception
    # end def __init__

    @property
    def SELF (self) :
        return self._Self_ (self)
    # end def SELF

    def __getattr__ (self, name) :
        if "." in name :
            getter = getattr (TFL.Getter, name)
        else :
            getter = operator.attrgetter (name)
        return self._Get_ (self, name, getter)
    # end def __getattr__

    def __getitem__ (self, item) :
        assert not isinstance (item, slice)
        return self._Get_ (self, item, operator.itemgetter (item))
    # end def __getitem__

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

# end class Base

Q = Base ()

class Q_Root (TFL.Meta.Object) :
    """Base class for all classes modelling queries"""

    def __call__ (self, obj) :
        return self.predicate (obj)
    # end def __call__

# end class Q_Root

@TFL.Add_New_Method (Base)
class _Aggr_ (Q_Root) :
    """Base for aggregation functions"""

    Table          = {}

    def __init__ (self, Q, rhs = 1) :
        self.Q     = Q
        self.rhs   = rhs
    # end def __init__

    @classmethod
    def derived (cls, subcls) :
        name    = subcls.__name__
        op_name = subcls.op_name = name.strip ("_").upper ()
        cls.Table [op_name] = subcls
        setattr (Base, name, subcls)
        return subcls
    # end def derived

    def predicate (self, obj) :
        try :
            pred   = self.rhs.predicate
        except AttributeError :
            result = self.rhs
        else :
            result = pred (obj)
        return result
    # end def predicate

    def __repr__ (self) :
        return "Q.%s (%r)" % (self.op_name, self.rhs, )
    # end def __repr__

# end class _Aggr_

@TFL.Add_New_Method (Base)
@pyk.adapt__bool__
@pyk.adapt__div__
class _Bin_ (Q_Root) :
    """Binary query expression"""

    op_map               = dict \
        ( __add__        = "+"
        , __eq__         = "=="
        , __div__        = "/"
        , __floordiv__   = "//"
        , __ge__         = ">="
        , __gt__         = ">"
        , __le__         = "<="
        , __lt__         = "<"
        , __mod__        = "%"
        , __mul__        = "*"
        , __rmul__       = "*"
        , __pow__        = "**"
        , __sub__        = "-"
        , __truediv__    = "/"
        )

    rop_map              = dict \
        ( __radd__       = "__add__"
        , __rdiv__       = "__truediv__"
        , __rfloordiv__  = "__floordiv__"
        , __rmod__       = "__mod__"
        , __rmul__       = "__mul__"
        , __rpow__       = "__pow__"
        , __rsub__       = "__sub__"
        , __rtruediv__   = "__truediv__"
        )

    predicate_precious_p = True

    Table                = {}

    def __init__ (self, lhs, op, rhs, undefs, reverse = False) :
        self.Q       = lhs.Q
        self.lhs     = lhs
        self.op      = op
        self.rhs     = rhs
        self.undefs  = undefs
        self.reverse = reverse
    # end def __init__

    def predicate (self, obj) :
        l = self.lhs.predicate (obj)
        try :
            pred = self.rhs.predicate
        except AttributeError :
            r = self.rhs
        else :
            r = pred (obj)
        if not any ((v is u) for v in (l, r) for u in self.undefs) :
            ### Call `op` only if neither `l` nor `v` is an undefined value
            if self.reverse :
                l, r = r, l
            return self.op (l, r)
    # end def predicate

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

    def __repr__ (self) :
        op = self.op.__name__
        lhs, rhs = self.lhs, self.rhs
        if self.reverse :
            lhs, rhs = rhs, lhs
        return "%s %s %s" % (lhs, self.op_map.get (op, op), rhs)
    # end def __repr__

# end class _Bin_

@TFL.Add_New_Method (Base)
@pyk.adapt__bool__
class _Una_ (Q_Root) :
    """Unary query expression"""

    op_map               = dict \
        ( __invert__     = "~"
        , __not__        = "~"
        , __neg__        = "-"
        )
    op_patch             = dict \
        ( _Una_Bool_     = dict
            ( __invert__ = "__not__"
            )
        , _Una_Expr_     = {}
        )

    predicate_precious_p = True

    Table                = {}

    def __init__ (self, lhs, op, undefs) :
        self.Q       = lhs.Q
        self.lhs     = lhs
        self.op      = op
        self.undefs  = undefs
    # end def __init__

    def predicate (self, obj) :
        l = self.lhs.predicate (obj)
        if not any ((l is u) for u in self.undefs) :
            ### Call `op` only if `l` is not an undefined value
            return self.op (l)
    # end def predicate

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

    def __repr__ (self) :
        op  = self.op.__name__
        lhs = self.lhs
        return "%s %s" % (self.op_map.get (op, op), lhs)
    # end def __repr__

# end class _Una_

@TFL.Add_New_Method (Base)
@pyk.adapt__bool__
class _Call_ (Q_Root) :
    """Query expression calling a method."""

    predicate_precious_p = True

    Table                = {}

    def __init__ (self, lhs, op, * args, ** kw) :
        self.Q      = lhs.Q
        self.lhs    = lhs
        self.op     = op
        self.args   = args
        self.kw     = kw
    # end def __init__

    def predicate (self, obj) :
        l = self.lhs.predicate (obj)
        if l is not self.Q.undef :
            return self.op (l, * self.args, ** self.kw)
    # end def predicate

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

    def __repr__ (self) :
        op = self.op.__name__
        return "%s.%s %r" % (self.lhs, op, self.args)
    # end def __repr__

# end class _Call_

def __binary (op_fct, Class) :
    name    = op_fct.__name__
    reverse = name in _Bin_.rop_map
    key     = _Bin_.rop_map [name] if reverse else name
    op      = getattr (operator, key)
    if name in ("__eq__", "__ne__") :
        ### Allow `x == None` and `x != None`
        undefs = (Q.undef, )
    else :
        ### Ignore `None` for all other operators
        undefs = (None, Q.undef)
    def _ (self, rhs) :
        return getattr (self.Q, Class) (self, op, rhs, undefs, reverse)
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = op_fct.__module__
    if op not in _Bin_.Table :
        _Bin_.Table [name] = (op, reverse)
    return _
# end def __binary

def _bin_bool (op) :
    return __binary (op, "_Bin_Bool_")
# end def _bin_bool

def _bin_expr (op) :
    return __binary (op, "_Bin_Expr_")
# end def _bin_expr

def _method (meth) :
    name = meth.__name__
    op   = meth ()
    def _ (self, * args, ** kw) :
        return self.Q._Call_Bool_ (self, op, * args, ** kw)
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = meth.__module__
    if name not in _Call_.Table :
        _Call_.Table [op.__name__] = op
    return _
# end def _method

def _type_error (op) :
    name = op.__name__
    def _ (self, rhs) :
        raise TypeError \
            ( "Operator `%s` not applicable to boolean result of `%s`"
              ", rhs: `%s`"
            % (_Bin_.op_map.get (name, name), self, rhs)
            )
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = op.__module__
    return _
# end def _type_error

def __unary (op_fct, Class) :
    name   = op_fct.__name__
    op     = getattr (operator, _Una_.op_patch [Class].get (name, name))
    undefs = (None, Q.undef)
    def _ (self) :
        return getattr (self.Q, Class) (self, op, undefs)
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = op_fct.__module__
    if op not in _Una_.Table :
        _Una_.Table [name] = op
    return _
# end def __unary

def _una_bool (op) :
    return __unary (op, "_Una_Bool_")
# end def _una_bool

def _una_expr (op) :
    return __unary (op, "_Una_Expr_")
# end def _una_expr

@TFL.Add_New_Method (Base)
class _Date_ (TFL.Meta.Object) :

    class Date (TFL.Meta.Object) :

        import datetime

        type       = datetime.date
        lom_delta  = datetime.timedelta (days=1)

    # end class Date

    class Date_Time (TFL.Meta.Object) :

        import datetime

        type       = datetime.datetime
        lom_delta  = datetime.timedelta (seconds=1)

    # end class Date_Time

    def __init__ (self, exp, D_Type) :
        self.exp    = exp
        self.D_Type = D_Type
    # end def __init__

    def MONTH (self, m, y) :
        D_Type = self.D_Type
        m      = int (m)
        y      = int (y)
        if m < 12 :
            n  = m + 1
            z  = y
        else :
            n  = 1
            z  = y + 1
        lhs    = D_Type.type (y, m, 1)
        rhs    = D_Type.type (z, n, 1) - D_Type.lom_delta
        return self.exp.BETWEEN (lhs, rhs)
    # end def MONTH

    def QUARTER (self, q, y) :
        D_Type = self.D_Type
        q      = int (q)
        y      = int (y)
        m      = 1 + 3 * (q - 1)
        if q < 4 :
            n  = m + 3
            z  = y
        else :
            n  = 1
            z  = y + 1
        lhs    = D_Type.type (y, m, 1)
        rhs    = D_Type.type (z, n, 1) - D_Type.lom_delta
        return self.exp.BETWEEN (lhs, rhs)
    # end def QUARTER

    def YEAR (self, y) :
        D_Type = self.D_Type
        y      = int (y)
        return self.exp.BETWEEN \
            ( D_Type.type (y,   1, 1)
            , D_Type.type (y+1, 1, 1) - D_Type.lom_delta
            )
    # end def YEAR

# end class _Date_

@pyk.adapt__bool__
class _Exp_Base_ (Q_Root) :

    ### Equality queries
    @_bin_bool
    def __eq__ (self, rhs) : pass

    @_bin_bool
    def __ne__ (self, rhs) : pass

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

    def __hash__ (self) :
        ### Override `__hash__` just to silence DeprecationWarning:
        ###     Overriding __eq__ blocks inheritance of __hash__ in 3.x
        raise NotImplementedError
    # end def __hash__

    ### Unary queries
    @_una_bool
    def __invert__ (self) : pass

# end class _Exp_Base_

@pyk.adapt__div__
class _Exp_ (_Exp_Base_) :
    """Query expression"""

    ### Order queries
    @_bin_bool
    def __ge__ (self, rhs) : pass

    @_bin_bool
    def __gt__ (self, rhs) : pass

    @_bin_bool
    def __le__ (self, rhs) : pass

    @_bin_bool
    def __lt__ (self, rhs) : pass

    ### Binary non-boolean queries
    @_bin_expr
    def __add__ (self, rhs) : pass

    @_bin_expr
    def __floordiv__ (self, rhs) : pass

    @_bin_expr
    def __mod__ (self, rhs) : pass

    @_bin_expr
    def __mul__ (self, rhs) : pass

    @_bin_expr
    def __pow__ (self, rhs) : pass

    @_bin_expr
    def __sub__ (self, rhs) : pass

    @_bin_expr
    def __truediv__ (self, rhs) : pass

    ### Binary non-boolean reflected queries
    @_bin_expr
    def __radd__ (self, rhs) : pass

    @_bin_expr
    def __rfloordiv__ (self, rhs) : pass

    @_bin_expr
    def __rmod__ (self, rhs) : pass

    @_bin_expr
    def __rmul__ (self, rhs) : pass

    @_bin_expr
    def __rpow__ (self, rhs) : pass

    @_bin_expr
    def __rsub__ (self, rhs) : pass

    @_bin_expr
    def __rtruediv__ (self, rhs) : pass

    ### Unary queries
    @_una_expr
    def __neg__ (self) : pass

    ### Method calls
    @_method
    def BETWEEN () :
        def between (val, lhs, rhs) :
            """between(val, lhs, rhs) -- Returns result of `lhs <= val <= rhs`"""
            return val is not None and lhs <= val <= rhs
        return between
    # end def BETWEEN

    @_method
    def CONTAINS () :
        return operator.contains
    # end def CONTAINS

    @property
    def D (self) :
        return self.Q._Date_ (self, self.Q._Date_.Date)
    # end def D

    @property
    def DT (self) :
        return self.Q._Date_ (self, self.Q._Date_.Date_Time)
    # end def DT

    @_method
    def ENDSWITH () :
        def endswith (l, r) :
            return l.endswith (r)
        return endswith
    # end def ENDSWITH

    @_method
    def IN () :
        def in_ (val,  rhs) :
            """in_(val, lhs) -- Returns result of `val in rhs`"""
            return val in rhs
        return in_
    # end def IN

    @_method
    def STARTSWITH () :
        def startswith (l, r) :
            return l.startswith (r)
        return startswith
    # end def STARTSWITH

# end class _Exp_

@pyk.adapt__div__
class _Exp_B_ (_Exp_Base_) :
    """Query expression for query result of type Boolean"""

    ### Order queries
    @_type_error
    def __ge__ (self, rhs) : pass

    @_type_error
    def __gt__ (self, rhs) : pass

    @_type_error
    def __le__ (self, rhs) : pass

    @_type_error
    def __lt__ (self, rhs) : pass

    ### Binary non-boolean queries
    @_type_error
    def __add__ (self, rhs) : pass

    @_type_error
    def __floordiv__ (self, rhs) : pass

    @_type_error
    def __mod__ (self, rhs) : pass

    @_type_error
    def __mul__ (self, rhs) : pass

    @_type_error
    def __pow__ (self, rhs) : pass

    @_type_error
    def __sub__ (self, rhs) : pass

    @_type_error
    def __truediv__ (self, rhs) : pass

    ### Binary non-boolean reflected queries
    @_type_error
    def __radd__ (self, rhs) : pass

    @_type_error
    def __rfloordiv__ (self, rhs) : pass

    @_type_error
    def __rmod__ (self, rhs) : pass

    @_type_error
    def __rmul__ (self, rhs) : pass

    @_type_error
    def __rpow__ (self, rhs) : pass

    @_type_error
    def __rsub__ (self, rhs) : pass

    @_type_error
    def __rtruediv__ (self, rhs) : pass

# end class _Exp_B_

@TFL.Add_New_Method (Base)
class _Get_ (_Exp_) :
    """Query getter"""

    predicate_precious_p = True

    def __init__ (self, Q, name, getter) :
        self.Q       = Q
        self._name   = name
        self._getter = getter
    # end def __init__

    def predicate (self, obj) :
        Q = self.Q
        try :
            return self._getter (obj)
        except Q.Ignore_Exception as exc :
            Q.undef.exc = exc
            return Q.undef
    # end def predicate

    def __getattr__ (self, name) :
        full_name = ".".join ((self._name, name))
        getter    = getattr (TFL.Getter, full_name)
        return self.__class__ (self.Q, full_name, getter)
    # end def __getattr__

    def __repr__ (self) :
        return "Q.%s" % (self._name, )
    # end def __repr__

# end class _Get_

@TFL.Add_New_Method (Base)
class _Self_ (_Get_) :
    """Query reference to object to which query is applied."""

    _name      = "SELF"

    def __init__ (self, Q) :
        self.Q = Q
    # end def __init__

    def predicate (self, obj) :
        return obj
    # end def predicate

    def __getattr__ (self, name) :
        return getattr (self.Q, name)
    # end def __getattr__

# end class _Self_

class _BVAR_Get_ (TFL.Meta.Object) :
    """Syntactic sugar for creating bound variables for query expressions."""

    _unique_count = 0

    def __init__ (self, Q) :
        self.Q = Q
    # end def __init__

    @property
    def NEW (self) :
        """Create a new unique BVAR"""
        cls                = self.__class__
        cls._unique_count += 1
        name               = "__bv_%d" % (cls._unique_count, )
        return self.BVAR (self.Q, name)
    # end def NEW

    def __getattr__ (self, name) :
        return self.BVAR (self.Q, name)
    # end def __getattr__

# end class _BVAR_Get_

class _BVAR_Descriptor_ (object) :
    """Descriptor to create bound variables for query expression.

       The descriptor is assigned to `Base` and returns a `_BVAR_Get_`
       instance that is bound to the `Q` object for which the descriptor was
       invoked. The `_BVAR_Get_` instance returns a bound variable for
       each attribute access. Bound variable are `_Exp_` instances and can
       therefore participate in further query expressions like operator
       application or function calls...
    """

    def __get__ (self, obj, cls) :
        if obj is None :
            return self
        return _BVAR_Get_ (obj)
    # end def __get__

# end class _RAW_DESC_

Base.BVAR = _BVAR_Descriptor_ ()

@TFL.Add_New_Method (_BVAR_Get_)
class BVAR (_Exp_) :
    """Bound variable for query expression.

    >>> Q.foo == Q.BVAR.bar
    Q.foo == Q.BVAR.bar

    >>> Q.BVAR.foo == 42
    Q.BVAR.foo == 42

    >>> Q.baz == Q.BVAR.NEW
    Q.baz == Q.BVAR.__bv_1

    """

    predicate_precious_p = True

    def __init__ (self, Q, name) :
        self.Q      = Q
        self._name  = name
        self._value = None
    # end def __init__

    def bind (self, value) :
        self._value = value
    # end def bind

    def predicate (self, obj) :
        return self._value
    # end def predicate

    def __repr__ (self) :
        return "Q.BVAR.%s" % (self._name, )
    # end def __repr__

# end class BVAR

@TFL.Add_New_Method (Base)
@pyk.adapt__bool__
class BVAR_Man (TFL.Meta.Object) :
    """Manager for bound variables"""

    def __init__ (self, bvar_man = None) :
        self.bvars    = bvars    = {}
        self.bindings = bindings = {}
        if bvar_man is not None :
            bvars.update    (bvar_man.bvars)
            bindings.update (bvar_man.bindings)
    # end def __init__

    def add (self, * bvars) :
        for bv in bvars :
            self.bvars [bv._name] = bv
    # end def add

    def bind (self, ** bindings) :
        self.bindings.update (bindings)
    # end def bind

    def clone (self) :
        return self.__class__ (self)
    # end def clone

    def __bool__ (self) :
        return bool (self.bvars)
    # end def __bool__

# end class BVAR_Man

def _derive_expr_class (cls, base, name) :
    derived  = base.__class__ \
        ( "_Q_Exp_%s" % name
        , (cls, base)
        , dict
            ( __doc__    = base.__doc__
            , _real_name = name
            )
        )
    setattr (Base, name, derived)
    Base.expr_class_names.append (name)
    return derived
# end def _derive_expr_class

_derive_expr_class (_Bin_,  _Exp_B_, "_Bin_Bool_")
_derive_expr_class (_Bin_,  _Exp_,   "_Bin_Expr_")
_derive_expr_class (_Call_, _Exp_B_, "_Call_Bool_")
_derive_expr_class (_Una_,  _Exp_B_, "_Una_Bool_")
_derive_expr_class (_Una_,  _Exp_,   "_Una_Expr_")

def _derive_aggr_class (name, doc) :
    cls = _Aggr_.derived \
        (_Aggr_.__class__ (name, (_Aggr_, ), dict (__doc__ = doc)))
    expr_cls = _derive_expr_class (cls, _Exp_, "%sExpr" % (name, ))
    @TFL.Attributed (__name__ = cls.op_name, __doc__ = doc)
    def _ (self, rhs = 1) :
        T = getattr (self, expr_cls.__name__)
        return T (self, rhs)
    setattr (Base, cls.op_name, _)
    return cls
# end def _derive_aggr_class

_derive_aggr_class ("_Avg_",   "Query function building the average")
_derive_aggr_class ("_Count_", "Query function finding the count")
_derive_aggr_class ("_Max_",   "Query function finding the maximum")
_derive_aggr_class ("_Min_",   "Query function finding the minimum")
_derive_aggr_class ("_Sum_",   "Query function building the sum")

###############################################################################
### Generic functions to display Q expressions

@TFL.Add_To_Class ("DISPLAY", Base)
@Single_Dispatch
def display (q) :
    return str (q)
# end def display

@display.add_type (_Bin_)
def _display_bin_ (q) :
    rs = "/r" if q.reverse else ""
    lhs, rhs = q.lhs, q.rhs
    return "%s%s (%s, %s)" % (q.op.__name__, rs, display (lhs), display (rhs))
# end def _display_bin_

@display.add_type (_Una_)
def _display_una_ (q) :
    return "%s (%s)" % (q.op.__name__, display (q.lhs))
# end def _display_una_

@display.add_type (_Call_)
def _display_call_ (q) :
    args = (q.lhs, ) + q.args
    return "Call:%s: (%s)" % \
        (q.op.__name__, ", ".join (display (a) for a in args))
# end def _display_call_

if __name__ != "__main__" :
    TFL._Export ("Q")
    TFL._Export_Module ()
### __END__ TFL.Q_Exp
