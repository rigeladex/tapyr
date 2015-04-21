# -*- coding: utf-8 -*-
# Copyright (C) 2010-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package ReST.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    ReST.To_Html
#
# Purpose
#    Convert re-structured text to HTML
#
# Revision Dates
#    17-Mar-2010 (CT) Creation
#    22-Feb-2012 (CT) Import `_ReST.Directives`
#    21-Apr-2015 (CT) Disable `file_insertion_enabled`, `raw_enabled`
#    ««revision-date»»···
#--

from   _ReST                    import ReST
from   _TFL                     import TFL

import _ReST.Roles
import _ReST.Directives

from   _TFL.predicate           import uniq
from   _TFL.pyk                 import pyk
from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object

import itertools

class To_Html (TFL.Meta.Object) :
    """Convert re-structured text to HTML."""

    include  = ("html_title", "html_subtitle", "fragment")

    ### http://docutils.sourceforge.net/docs/user/config.html
    ### http://docutils.sourceforge.net/docs/howto/security.html
    settings = dict \
        ( cloak_email_addresses         = False
        , embed_stylesheet              = False
        , file_insertion_enabled        = False
        , initial_header_level          = "2"
        , input_encoding                = "unicode"
        , language_code                 = "en"
        , output_encoding               = "utf8"
        , output_encoding_error_handler = "xmlcharrefreplace"
        , raw_enabled                   = False
        , smart_quotes                  = False
        , _disable_config               = True
        )

    def __init__ (self, * replacers, ** kw) :
        self.include   = kw.pop ("include", self.include)
        self.replacers = list   (replacers)
        self.settings  = dict   (self.settings, ** kw)
    # end def __init__

    def __call__ (self, text, encoding = "utf8", language = "en", include = None, ** kw) :
        settings = dict \
            ( self.settings
            , output_encoding = encoding
            , language_code   = language
            , ** kw
            )
        parts = self._publish_parts \
            ( source             = pyk.decoded (text)
            , writer_name        = "html4css1"
            , settings_overrides = settings
            )
        if include is None :
            include = self.include
        result = "\n".join (p for p in (parts [i] for i in include) if p)
        for rep in self.replacers :
            result = rep (result)
        return result
    # end def __call__

    def add_replacers (self, * replacers) :
        self.replacers = list \
            (uniq (itertools.chain (self.replacers, replacers)))
    # end def add_replacers

    @Once_Property
    def _publish_parts (self) :
        import _ReST.Roles
        from   docutils.core import publish_parts
        return publish_parts
    # end def _publish_parts

# end class To_Html

to_html = To_Html ()

__doc__ = """
    >>> text = u'''
    ... Test of ReST.to_html
    ... ====================
    ...
    ... Section
    ... -------
    ...
    ... A paragraph by any other name.
    ...
    ... Another section
    ... ---------------
    ...
    ... With another paragraph.
    ...
    ... The end...
    ... '''
    >>> print ReST.to_html (text, encoding = "utf-8")
    <h1 class="title">Test of ReST.to_html</h1>
    <BLANKLINE>
    <div class="section" id="section">
    <h2>Section</h2>
    <p>A paragraph by any other name.</p>
    </div>
    <div class="section" id="another-section">
    <h2>Another section</h2>
    <p>With another paragraph.</p>
    <p>The end...</p>
    </div>

"""

if __name__ != "__main__" :
    ReST._Export ("*")
### __END__ ReST.To_Html
