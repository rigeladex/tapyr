# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.Ticker
#
# Purpose
#    Provide classes to determine tick-marks for data plots
#
# Revision Dates
#     5-Jun-2017 (CT) Creation
#    12-Jul-2018 (CT) Add `** kwds`, `labels` to `_Axis_`
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _TFL                       import TFL
from   _TFL.Divisor_Dag           import Divisor_Dag
from   _TFL.formatted_repr        import formatted_repr
from   _TFL.Math_Func             import log, log10, sign
from   _TFL.portable_repr         import portable_repr
from   _TFL.predicate             import \
    pairwise, rounded_down, rounded_to, rounded_up, uniq
from   _TFL.pyk                   import pyk
from   _TFL.Range                 import Float_Range_Discrete as F_Range

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL._Meta.Property        import Optional_Computed_Once_Property

import _TFL._Meta.Object

import itertools
import operator

class _Axis_ (TFL.Meta.Object) :
    """Axis with tick marks for a data range of a certain `Base`.

    An `Axis` instance is defined by a :class:`Base` instance :attr:`base`, and
    minimum and maximum data values, :attr:`data_min` and :attr:`data_max`, to
    be displayed.

    >>> ax1 = Axis (base_10, 0, 100)

    >>> print (ax1.data_min, ax1.data_max)
    0 100

    Based on :attr:`base` and the data range, an `Axis` instance determines the
    minimum and maximum values of the axis and the tick marks to be displayed.

    :attr:`major_delta` is the distance between major tick marks:
    >>> print (ax1.major_min, ax1.major_max, ax1.major_delta)
    0 100 10

    Axis extreme values:
    >>> print (ax1.ax_min, ax1.ax_max)
    -10 110

    Major tick marks:
    >>> print (ax1.major_range)
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    Medium tick marks:
    >>> print (ax1.medium_range)
    [-5.0, 5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0, 105.0]

    Minor tick marks:
    >>> print (ax1.minor_range)
    [-9.0, -8.0, -7.0, -6.0, -4.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 11.0, 12.0, 13.0, 14.0, 16.0, 17.0, 18.0, 19.0, 21.0, 22.0, 23.0, 24.0, 26.0, 27.0, 28.0, 29.0, 31.0, 32.0, 33.0, 34.0, 36.0, 37.0, 38.0, 39.0, 41.0, 42.0, 43.0, 44.0, 46.0, 47.0, 48.0, 49.0, 51.0, 52.0, 53.0, 54.0, 56.0, 57.0, 58.0, 59.0, 61.0, 62.0, 63.0, 64.0, 66.0, 67.0, 68.0, 69.0, 71.0, 72.0, 73.0, 74.0, 76.0, 77.0, 78.0, 79.0, 81.0, 82.0, 83.0, 84.0, 86.0, 87.0, 88.0, 89.0, 91.0, 92.0, 93.0, 94.0, 96.0, 97.0, 98.0, 99.0, 101.0, 102.0, 103.0, 104.0, 106.0, 107.0, 108.0, 109.0]

    By default `Axis` uses a margin of one major tick mark on each side.
    Passing :attr:`margin` to the `Axis` constructor changes the :attr:`ax_min`
    and :attr:`ax_max`.

    >>> ax2 = Axis (base_10, 0, 100, margin = 0, max_major_ticks = 7)
    >>> print (ax2.data_min, ax2.data_max)
    0 100
    >>> print (ax2.major_min, ax2.major_max, ax2.major_delta)
    0 100 20
    >>> print (ax2.ax_min, ax2.ax_max)
    0 100

    Major tick marks:
    >>> print (ax2.major_range)
    [0, 20, 40, 60, 80, 100]

    Medium tick marks:
    >>> print (ax2.medium_range)
    [10.0, 30.0, 50.0, 70.0, 90.0]

    Minor tick marks:
    >>> print (ax2.minor_range)
    [2.0, 4.0, 6.0, 8.0, 12.0, 14.0, 16.0, 18.0, 22.0, 24.0, 26.0, 28.0, 32.0, 34.0, 36.0, 38.0, 42.0, 44.0, 46.0, 48.0, 52.0, 54.0, 56.0, 58.0, 62.0, 64.0, 66.0, 68.0, 72.0, 74.0, 76.0, 78.0, 82.0, 84.0, 86.0, 88.0, 92.0, 94.0, 96.0, 98.0]

    >>> ax3 = Axis (base_10, 0, 100, margin = 0.5)
    >>> print (ax3.data_min, ax3.data_max)
    0 100
    >>> print (ax3.major_min, ax3.major_max, ax3.major_delta)
    0 100 10
    >>> print (ax3.ax_min, ax3.ax_max)
    -5.0 105.0

    """

    label_fill              = None
    major_lines             = ""
    max_major_ticks         = 20
    max_ticks               = 100
    minor_lines             = ""
    _labels                 = None

    def __init__ \
            ( self, base, data_min, data_max
            , ax_min            = None
            , ax_max            = None
            , margin            = 1
            , max_major_ticks   = None
            , max_ticks         = None
            , major_delta       = None
            , major_offset      = 0
            , medium_ticks      = None
            , minor_ticks       = None
            , round_extrema     = True
            , ** kwds
            ) :
        self.base               = base
        self.data_min           = data_min
        self.data_max           = data_max
        if ax_min is not None :
            self.ax_min         = ax_min
        if ax_max is not None :
            self.ax_max         = ax_max
        self.margin             = margin
        if max_major_ticks is not None :
            self.max_major_ticks= max_major_ticks
        if max_ticks is not None :
            self.max_ticks      = max_ticks
        if major_delta is not None :
            self.major_delta    = major_delta
        self.major_offset       = major_offset
        if medium_ticks is not None :
            self.medium_ticks   = medium_ticks
        if minor_ticks is not None :
            self.minor_ticks    = minor_ticks
        self.round_extrema      = round_extrema
        self.pop_to_self     (kwds, "labels", prefix = "_")
        self.__dict__.update (** kwds)
    # end def __init__

    @Optional_Computed_Once_Property
    def ax_max (self) :
        """Maximum value of axis."""
        d_max   = self.data_max
        m_max   = self.major_max
        delta   = self.margin_delta
        result  = max (m_max, d_max + delta) \
            if d_max != m_max else m_max + delta
        return result
    # end def ax_max

    @Optional_Computed_Once_Property
    def ax_min (self) :
        """Minimum value of axis."""
        d_min   = self.data_min
        m_min   = self.major_min
        delta   = self.margin_delta
        result  = min (m_min, d_min - delta) \
            if d_min != m_min else m_min - delta
        return result
    # end def ax_min

    @Once_Property
    def data_length (self) :
        """Difference between `self.data_max` and `self.data_min`."""
        return abs (self.data_max - self.data_min)
    # end def data_length

    @property
    def labels (self) :
        result = self._labels
        if result is True :
            result = self._labels = \
                tuple (formatted_repr (m) for m in self.major_range)
        return result
    # end def labels

    @labels.setter
    def labels (self, value) :
        self._labels = value
    # end def labels

    @Optional_Computed_Once_Property
    def major_delta (self) :
        """Delta between major tick marks."""
        length      = float (self.data_length)
        deltas      = self.scaled.deltas
        max_ticks   = self.max_major_ticks
        return self._delta (length, deltas, max_ticks)
    # end def major_delta

    @Once_Property
    def major_max (self) :
        """Maximum major tick mark."""
        result = rounded_up (self.data_max, self.major_delta) \
            if self.round_extrema else self.data_max
        if not self.data_length :
            result += self.major_delta
        return result
    # end def major_max

    @Once_Property
    def major_min (self) :
        """Minimum major tick mark."""
        result = rounded_down (self.data_min, self.major_delta) \
            if self.round_extrema else self.data_min
        if not self.data_length :
            result -= self.major_delta
        return result
    # end def major_min

    @Once_Property
    def major_range (self) :
        """Range of values of major tick marks."""
        ax_min       = self.ax_min
        ax_max       = self.ax_max
        data_min     = self.data_min
        data_max     = self.data_max
        major_delta  = self.major_delta
        major_min    = self.major_min + self.major_offset
        major_max    = self.major_max
        margin_delta = self.margin_delta
        if major_min - ax_min > major_delta :
            major_min -= major_delta * int ((major_min - ax_min) / major_delta)
        if ax_max - major_max > major_delta :
            major_max += major_delta * int ((ax_max - major_max) / major_delta)
        bounds       = "".join \
            ( ( "[" if data_min != ax_min or not margin_delta else "("
              , "]" if data_max != ax_max or not margin_delta else ")"
              )
            )
        result = F_Range (major_min, major_max, bounds, delta = major_delta)
        return list (result)
    # end def major_range

    @Once_Property
    def margin_delta (self) :
        """Delta between first/last major tick mark and end of axis."""
        return self.major_delta * self.margin
    # end def margin_delta

    @Once_Property
    def medium_delta (self) :
        """Delta between major and medium tick marks."""
        medium_ticks = self.medium_ticks
        return self.major_delta / (medium_ticks + 1.0) if medium_ticks else 0
    # end def medium_delta

    @Optional_Computed_Once_Property
    def medium_lines (self) :
        return self.major_lines and bool (self.medium_range)
    # end def medium_lines

    @Once_Property
    def medium_range (self) :
        """Range of values of medium tick marks."""
        return list (self._gen_tick_marks (self.medium_delta, self.major_range))
    # end def medium_range

    @Optional_Computed_Once_Property
    def medium_ticks (self) :
        """Number of medium tick marks between each pair of major tick marks."""
        return self.sub_ticks [0]
    # end def medium_ticks

    @Once_Property
    def minor_delta (self) :
        """Delta between major/medium and minor tick marks."""
        minor_ticks = self.minor_ticks
        delta       = self.medium_delta or self.major_delta
        return delta / (minor_ticks + 1.0) if minor_ticks else 0
    # end def minor_delta

    @Once_Property
    def minor_range (self) :
        """Range of values of minor tick marks."""
        delta  = self.minor_delta
        result = []
        if delta :
            higher_range = sorted \
                (itertools.chain (self.major_range, self.medium_range))
            result       = list (self._gen_tick_marks (delta, higher_range))
        return result
    # end def minor_range

    @Optional_Computed_Once_Property
    def minor_ticks (self) :
        """Number of minor tick marks between each pair of major/medium tick marks."""
        return self.sub_ticks [1]
    # end def minor_ticks

    @Once_Property
    def scaled (self) :
        """Base scaled to `data_length`."""
        return self.base.scaled (self.data_length)
    # end def scaled

    @Once_Property
    def sub_ticks (self) :
        i, (medium, minor) = self._sub_ticks ()
        if (medium, minor) > (0, 0) :
            major              = len (self.major_range) - 1
            max_ticks          = self.max_ticks
            medium_plus_minor  = medium + (medium + 1) * minor
            if medium_plus_minor * major > max_ticks :
                minor = 0
                if medium * major > max_ticks :
                    bmd    = self.base.medium_ticks - 1
                    medium = bmd if bmd * major <= max_ticks else 1
            elif medium == 0 and minor < 5 :
                candidates = sorted \
                    (   mi
                    for me, mi in self.base.sub_ticks
                    if  me == minor
                    )
                me = minor
                for mi in reversed (candidates) :
                    if (me + (me + 1) * mi) * major <= max_ticks :
                        break
                else :
                    me, mi = minor, medium
                medium, minor = (me, mi)
        return (medium, minor)
    # end def sub_ticks

    def adjust_major_offset (self, start_value) :
        """Adjust `major_offset`  to force major ticks to multiples of `major_delta`"""
        m_delta = self.major_delta
        rr      = start_value % m_delta
        result  = self.major_offset = m_delta - rr if rr else rr
        return result
    # end def adjust_major_offset

    def _delta (self, length, deltas, max_ticks, default = None) :
        for d in deltas :
            if rounded_up (length / d, 1.0) <= max_ticks :
                result = d
                break
        else :
            result = d if default is None else default
        return result
    # end def _delta

    def _gen_tick_marks (self, delta, higher_tick_marks) :
        if delta :
            def _gen (delta, higher_tick_marks) :
                cmp_op = operator.lt if delta > 0 else operator.gt
                eps    = delta / 10
                for l, r in pairwise (higher_tick_marks) :
                    r  = r - eps
                    t  = l + delta
                    while cmp_op (t, r) :
                        yield t
                        t += delta
            return itertools.chain \
                ( reversed
                    (list (_gen (-delta, [higher_tick_marks [0], self.ax_min])))
                , _gen (delta, higher_tick_marks)
                , _gen (delta, [higher_tick_marks [-1], self.ax_max])
                )
        return ()
    # end def _gen_tick_marks

    def _sub_ticks (self) :
        major_delta = self.major_delta
        bds         = self.base.deltas
        sds         = self.scaled.deltas
        try :
            i = sds.index (major_delta)
        except ValueError :
            ### non-standard number of major tick marks
            sd = sds [-1]
            if major_delta > sd and major_delta % sd == 0 :
                result = len (sds) - 1, (0, int (major_delta / sd) - 1)
            else :
                result  = 0, (1, 1)
        else :
            if i and self.scaled.scale :
                i = len (sds) - 1
            result  = i, self.base.sub_ticks [i]
        return result
    # end def _sub_ticks

    def __str__ (self) :
        result = "%s (%r, %s, %s, %s, %s, %s, %s, %s)" % \
            ( self.__class__.__name__, self.base
            , self.data_min, self.data_max
            , self.ax_min, self.ax_max
            , self.margin
            , self.max_major_ticks, self.max_ticks
            )
        return result
    # end def __str__

# end class _Axis_

class Axis_F (_Axis_) :
    """Axis with tick marks for a non-integral data range of a certain `Base`."""

# end class Axis_F

class Axis_I (_Axis_) :
    """Axis with tick marks for a integral data range of a certain `Base`."""

    @Once_Property
    def medium_ticks (self) :
        result = self.__super.medium_ticks
        delta  = self.major_delta
        if result and delta / (result + 1.0) < 1 :
            result = 0
        return result
    # end def medium_ticks

    @Once_Property
    def minor_ticks (self) :
        """Delta between major/medium and minor tick marks."""
        result = self.__super.minor_ticks
        delta  = self.medium_delta or self.major_delta
        if result and delta / (result + 1.0) < 1 :
            result = 0
        return result
    # end def minor_ticks

    def _delta (self, length, deltas, max_ticks, default = None) :
        result = self.__super._delta (length, deltas, max_ticks, default)
        if result and result < 1 :
            result = 1
        return result
    # end def _delta

# end class Axis_I

def Axis (base, * args, ** kwds) :
    cls = Axis_I if isinstance (base, Base_Integral) else Axis_F
    return cls (base, * args, ** kwds)
# end def Axis

class Base (TFL.Meta.Object) :
    """Number base for tick mark determination.

    >>> b = Base (10)
    >>> print (b)
    10 : (1, 2, 5, 10)

    >>> print (b.scaled (15000))
    10 ^ 3 : (1000, 2000, 5000, 10000)
    >>> print (b.scaled (10000))
    10 ^ 3 : (1000, 2000, 5000, 10000)
    >>> print (b.scaled (1000))
    10 ^ 2 : (100, 200, 500, 1000)
    >>> print (b.scaled (100))
    10 ^ 1 : (10, 20, 50, 100)
    >>> print (b.scaled (10))
    10 : (1, 2, 5, 10)
    >>> print (b.scaled (1))
    10 ^ -1 : (0.1, 0.2, 0.5, 1)
    >>> print (b.scaled (0.1))
    10 ^ -2 : (0.01, 0.02, 0.05, 0.1)
    >>> print (b.scaled (0.01))
    10 ^ -3 : (0.001, 0.002, 0.005, 0.01)
    >>> print (b.scaled (0.001))
    10 ^ -4 : (0.0001, 0.0002, 0.0005, 0.001)
    >>> print (b.scaled (0.0005))
    10 ^ -4 : (0.0001, 0.0002, 0.0005, 0.001)

    """

    def __init__ \
            ( self, base
            , deltas           = None
            , log_round_amount = None
            , scale            = 0
            , sub_ticks        = None
            , medium_delta     = None
            , ** kwds
            ) :
        self.base   = base
        self.deltas = \
            ( None if deltas is None else sorted
                (uniq (itertools.chain (deltas, ([] if scale else [1, base]))))
            )
        self.lra    = log_round_amount
        self.scale  = scale
        if sub_ticks is not None :
            self.sub_ticks = sub_ticks
        if medium_delta is not None :
            self.medium_delta = medium_delta
        self._kwds  = kwds
        self.__dict__.update (kwds)
        if base == 10 :
            self.log = log10
    # end def __init__

    @property
    def deltas (self) :
        """Possible deltas between tick marks for values of this `Base`"""
        result = self._deltas
        if result is None :
            result = self._deltas = tuple (Divisor_Dag (self.base).divisors)
        return result
    # end def deltas

    @deltas.setter
    def deltas (self, value) :
        self._deltas = tuple (value) if value is not None else None
    # end def deltas

    @Optional_Computed_Once_Property
    def medium_delta (self) :
        result = self.deltas [1]
        for delta in self.deltas [1:] :
            if delta > 2 :
                result = delta
                break
        return result
    # end def medium_delta

    @Optional_Computed_Once_Property
    def sub_ticks (self) :
        """Number of medium and minor tick marks for each delta."""
        deltas = self.deltas
        result = [(0, 0)] * len (deltas)
        for k, (i, j) in enumerate (pairwise (deltas), 1) :
            if i > 1 and j % i == 0 :
                r = (1, i - 1)
            else :
                r = (0, j - 1)
            result [k] = r
        result [0] = result [-1]
        return result
    # end def sub_ticks

    def log (self, v) :
        """Logarithm of base `self.base` of `v`."""
        return log (v, self.base)
    # end def log

    def log_rounded (self, v) :
        """Logarithm of base `self.base` of `v` rounded to `int`."""
        log_v  = self.log (v) if v else 1.0
        lra    = self.lra
        if lra is not None :
            result = int (log_v + lra)
        else :
            result = rounded_to (log_v, 1.0)
        return int (result)
    # end def log_rounded

    def scaled (self, delta) :
        """`Base` scaled to range of `delta`"""
        scale = self.log_rounded (delta) - 1
        if scale :
            factor        = self.base ** scale
            scaled_deltas = (delta * factor  for delta in self.deltas)
            result        = self.__class__ \
                (self.base, scaled_deltas, self.lra, scale, ** self._kwds)
        else :
            result        = self
        return result
    # end def scaled

    def __repr__ (self) :
        return "%s (%s, %s)" % \
            (self.__class__.__name__, self.base, self.deltas [1:-1])
    # end def __repr__

    def __str__ (self) :
        s = self.scale
        return "%2d%s : %s" % \
            (self.base, (" ^ %s" % s) if s else "", portable_repr (self.deltas))
    # end def __str__

# end class Base

class Base_Integral (Base) :
    """Intgral number base for tick mark determination."""

# end class Base_Integral

base_10         = Base (10)
base_12         = Base \
    ( 12
    , sub_ticks = [(3, 2), (0, 1), (0, 2), (0, 3), (1, 2), (3, 2)]
    )
base_16         = Base \
    ( 16, (4, 8)
    , sub_ticks = [(3, 3), (1, 1), (1, 3), (3, 3)]
    )
base_day        = Base_Integral \
    ( 28, (7, 14)
    , sub_ticks = [(3, 6), (0, 6), (1, 6), (3, 6)]
    )
base_hour       = Base_Integral \
    ( 24, (3, 6, 12)
    , sub_ticks = [(7, 2), (0, 2), (1, 2), (3, 2), (7, 2)]
    )
base_hour_f     = Base \
    ( 24, (3, 6, 12)
    , sub_ticks = [(7, 2), (0, 2), (1, 2), (3, 2), (7, 2)]
    )
base_month      = Base_Integral \
    ( 12, (3, 6)
    , log_round_amount = 0.0
    , sub_ticks        = [(3, 2), (0, 2), (1, 2), (3, 2)]
    )
base_quarter    = Base_Integral (4, log_round_amount = 0.0)
base_week       = Base_Integral \
    ( 52
    , log_round_amount = 0.0
    , sub_ticks        = [(2, 12), (0, 1), (1, 1), (0, 12), (1, 12), (2, 12)]
    )

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Ticker
