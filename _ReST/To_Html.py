# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package ReST.
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
#    ReST.To_Html
#
# Purpose
#    Convert re-structured text to HTML
#
# Revision Dates
#    17-Mar-2010 (CT) Creation
#    22-Feb-2012 (CT) Import `_ReST.Directives`
#    ««revision-date»»···
#--

from   _ReST                    import ReST
from   _TFL                     import TFL

import _ReST.Roles
import _ReST.Directives

from   _TFL.predicate           import uniq
from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object

import itertools

class To_Html (TFL.Meta.Object) :
    """Convert re-structured text to HTML."""

    include  = ("html_title", "html_subtitle", "fragment")
    settings = dict \
        ( embed_stylesheet              = False
        , initial_header_level          = "2"
        , input_encoding                = "unicode"
        , output_encoding               = "utf8"
        , output_encoding_error_handler = "xmlcharrefreplace"
        , language_code                 = "en"
        , cloak_email_addresses         = False
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
            ( source             = unicode (text)
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
