# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Attr.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.Attr.Polisher
#
# Purpose
#    Polishers for MOM attributes
#
# Revision Dates
#    24-Sep-2014 (CT) Creation
#    26-Sep-2014 (CT) Add `guard`, `capitalize_if_not_mixed_case`,
#                     `capitalize_if_lower_case`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr

from   _TFL.pyk              import pyk
from   _TFL.Regexp           import *

import _TFL._Meta.Object
import _TFL.predicate

class _Polisher_ (TFL.Meta.Object) :
    """Base class for Polishers"""

    guard = None

    def __init__ (self, ** kw) :
        for k, v in pyk.iteritems (kw) :
            ### use `setattr` to allow `property.__set__` to intervene
            setattr (self, k, v)
    # end def __init__

    def __call__ (self, attr, value_dict, value = None) :
        """Polish value of `attr` in `value_dict`, if any, return polished `value_dict`."""
        result = dict (value_dict)
        name   = attr.name
        if value is None :
            value = value_dict.get (name)
        if isinstance (value, pyk.string_types) :
            guard = self.guard
            value = value.strip ()
            if value and (guard is None or guard (value)) :
                self._polish (attr, name, value, result)
        return result
    # end def __call__

    def _polish (self, attr, name, value, value_dict) :
        raise NotImplementedError \
            ( "%s needs to implement either __call__ or _polish"
            % (self.__class__, )
            )
    # end def __call__

# end class _Polisher_

class Match_Split (_Polisher_) :
    """Polisher splitting a value into several attribute values."""

    def __init__ (self, matcher, ** kw) :
        if isinstance (matcher, (Regexp, ) + pyk.string_types) :
            matcher = Multi_Regexp (matcher)
        self.__super.__init__ (matcher = matcher, ** kw)
    # end def __init__

    def add (self, * matchers, ** kw) :
        self.matcher.add (* matchers, ** kw)
    # end def add

    def _polish (self, attr, name, value, result) :
        match = self.matcher.search (value)
        if match is not None :
            dct = match.groupdict ()
            for k, v in pyk.iteritems (dct) :
                if v is not None :
                    result [k] = v
    # end def _polish

# end class Match_Split

class Replace (_Polisher_) :
    """Polisher replacing matches of regular expressions."""

    def __init__ (self, replacer, ** kw) :
        self.__super.__init__ (replacer = replacer, ** kw)
    # end def __init__

    def _polish (self, attr, name, value, result) :
        result [name] = self.replacer (value)
    # end def _polish

# end class Replace

def _capitalize_words (match) :
    words  = match.group (0).split ("-")
    result = "-".join (w.capitalize () for w in words)
    return result
# end def _capitalize_words

### `_uni_case_word` whould use `[:lower:]` and `[:upper:]` but
### unfortunately Python regular expressions don't support these
_uni_case_word_pat = \
    ( r"("
      r"[a-zäüöß0-9][-a-zäüöß0-9]*"
      r"|"
      r"[A-ZÄÜÖ0-9][-A-ZÄÜÖ0-9]*"
      r")"
    )

capitalize = Replace \
    ( Re_Replacer
        ( r"\b"
        + _uni_case_word_pat
        + r"\b"
        , _capitalize_words
        , re.UNICODE
        )
    )

capitalize_if_lower_case = Replace \
    ( Re_Replacer (r"\w+", _capitalize_words, re.UNICODE)
    , guard = lambda s : s.islower ()
    )

capitalize_if_not_mixed_case = Replace \
    ( Re_Replacer (r"\w+", _capitalize_words, re.UNICODE)
    , guard = TFL.is_not_mixed_case
    )

capitalize_last_word = Replace \
    ( Re_Replacer
        ( r"\b"
        + _uni_case_word_pat
        + r"$"
        , _capitalize_words
        , re.UNICODE
        )
    )

_area_code_pat     = r"(?P<area_code>\d+)"
_country_code_pat  = r"(?:(?:\+ *|00)(?P<country_code>\d+))"
_number_pat        = r"(?P<number>\d+)"

area_code_clean    = Match_Split (r"^0 *" + _area_code_pat + r"$")
country_code_clean = Match_Split (r"^" + _country_code_pat + r"$")
phone_number_split = Match_Split \
    ( Multi_Regexp
        ( Regexp
            ( r"^"
            + r"(?:" + _country_code_pat + " +|0 *)?"
            + _area_code_pat
            + r" "
            + _number_pat
            + r"$"
            , re.UNICODE
            )
        , Regexp
            ( r"^"
            + r"(?:" + _country_code_pat + "|0)? *"
            + r"\("
            + _area_code_pat
            + r"\) *"
            + _number_pat
            + r"$"
            , re.UNICODE
            )
        )
    )

_test_capitalize = """
    >>> from _TFL.Record import Record
    >>> attr = Record (name = "test")
    >>> def test (polisher, value) :
    ...     rd = polisher (attr, dict (test = value))
    ...     print (rd ["test"])

    >>> l = "fröhlich-tanzer"
    >>> m = "Fröhlich-Tanzer"
    >>> u = "FRÖHLICH-TANZER"

    >>> test (capitalize, l)
    Fröhlich-Tanzer
    >>> test (capitalize, m)
    Fröhlich-Tanzer
    >>> test (capitalize, u)
    Fröhlich-Tanzer

    >>> test (capitalize_last_word, l)
    Fröhlich-Tanzer
    >>> test (capitalize_last_word, m)
    Fröhlich-Tanzer
    >>> test (capitalize_last_word, u)
    Fröhlich-Tanzer

    >>> l = "christian fröhlich-tanzer"
    >>> m = "Christian Fröhlich-Tanzer"
    >>> u = "CHRISTIAN FRÖHLICH-TANZER"

    >>> test (capitalize, l)
    Christian Fröhlich-Tanzer
    >>> test (capitalize, m)
    Christian Fröhlich-Tanzer
    >>> test (capitalize, u)
    Christian Fröhlich-Tanzer

    >>> test (capitalize_last_word, l)
    christian Fröhlich-Tanzer
    >>> test (capitalize_last_word, m)
    Christian Fröhlich-Tanzer
    >>> test (capitalize_last_word, u)
    CHRISTIAN Fröhlich-Tanzer

    >>> l = "van der fröhlich-tanzer"
    >>> m = "van der Fröhlich-Tanzer"
    >>> u = "van der FRÖHLICH-TANZER"
    >>> v = "VAN DER FRÖHLICH-TANZER"

    >>> test (capitalize, l)
    Van Der Fröhlich-Tanzer
    >>> test (capitalize, m)
    Van Der Fröhlich-Tanzer
    >>> test (capitalize, u)
    Van Der Fröhlich-Tanzer

    >>> test (capitalize_if_not_mixed_case, l)
    Van Der Fröhlich-Tanzer
    >>> test (capitalize_if_not_mixed_case, m)
    van der Fröhlich-Tanzer
    >>> test (capitalize_if_not_mixed_case, u)
    van der FRÖHLICH-TANZER
    >>> test (capitalize_if_not_mixed_case, v)
    Van Der Fröhlich-Tanzer

    >>> test (capitalize_last_word, l)
    van der Fröhlich-Tanzer
    >>> test (capitalize_last_word, m)
    van der Fröhlich-Tanzer
    >>> test (capitalize_last_word, u)
    van der Fröhlich-Tanzer

    >>> l = "mctanzer"
    >>> m = "McTanzer"
    >>> u = "MCTANZER"

    >>> test (capitalize, l)
    Mctanzer
    >>> test (capitalize, m)
    McTanzer
    >>> test (capitalize, u)
    Mctanzer

    >>> test (capitalize_last_word, l)
    Mctanzer
    >>> test (capitalize_last_word, m)
    McTanzer
    >>> test (capitalize_last_word, u)
    Mctanzer

    >>> l = "mag."
    >>> m = "Mag."
    >>> u = "MAG."

    >>> test (capitalize, l)
    Mag.
    >>> test (capitalize, m)
    Mag.
    >>> test (capitalize, u)
    Mag.

    >>> l = "dipl.ing."
    >>> m = "Dipl.Ing."
    >>> u = "DIPL.ING."

    >>> test (capitalize, l)
    Dipl.Ing.
    >>> test (capitalize, m)
    Dipl.Ing.
    >>> test (capitalize, u)
    Dipl.Ing.

"""

_test_area_code_clean = r"""
    >>> from _TFL.Record import Record

    >>> attr = Record (name = "area_code")

    >>> def show_split (v) :
    ...     r  = area_code_clean (attr, dict (area_code = v))
    ...     vs = ("%s = %s" % (k, v) for k, v in sorted (r.items ()))
    ...     print (", ".join (vs))

    >>> show_split ("664")
    area_code = 664

    >>> show_split ("0664")
    area_code = 664

    >>> show_split ("0 664")
    area_code = 664

"""

_test_country_code_clean = r"""
    >>> from _TFL.Record import Record

    >>> attr = Record (name = "country_code")

    >>> def show_split (v) :
    ...     r  = country_code_clean (attr, dict (country_code = v))
    ...     vs = ("%s = %s" % (k, v) for k, v in sorted (r.items ()))
    ...     print (", ".join (vs))

    >>> show_split ("43")
    country_code = 43

    >>> show_split ("+43")
    country_code = 43

    >>> show_split ("+ 43")
    country_code = 43

    >>> show_split ("0043")
    country_code = 43

"""

_test_phone_number_split = r"""
    >>> from _TFL.Record import Record

    >>> attr = Record (name = "number")

    >>> def show_split (number) :
    ...     r  = phone_number_split (attr, dict (number = number))
    ...     vs = ("%s = %s" % (k, v) for k, v in sorted (r.items ()))
    ...     print (", ".join (vs))

    >>> show_split ("12345678")
    number = 12345678

    >>> show_split ("0043 664 12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_split ("+43 664 12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_split ("0043 664 12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_split ("664 12345678")
    area_code = 664, number = 12345678

    >>> show_split ("0664 12345678")
    area_code = 664, number = 12345678

    >>> show_split ("+43(664)12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_split ("+43 (664) 12345678")
    area_code = 664, country_code = 43, number = 12345678

    >>> show_split ("0(664)12345678")
    area_code = 664, number = 12345678

    >>> show_split ("0 (664) 12345678")
    area_code = 664, number = 12345678

"""

__test__ = dict \
    ( test_area_code_clean    = _test_area_code_clean
    , test_country_code_clean = _test_country_code_clean
    , test_capitalize         = _test_capitalize
    , test_phone_number_split = _test_phone_number_split
    )

if __name__ != "__main__" :
    MOM.Attr._Export_Module ()
### __END__ MOM.Attr.Polisher
