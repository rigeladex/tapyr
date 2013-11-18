# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
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
#    ReST.HTML_Writer
#
# Purpose
#    A custom HTML write which allows the obfuscation of HTML anchors
#    (Inspired by this blog entry:
#    http://www.arnebrodowski.de/blog/write-your-own-restructuredtext-writer.html)
#
# Revision Dates
#    16-Feb-2010 (MG) Creation
#--

from _ReST             import ReST
from  docutils.writers import html4css1
from  docutils         import nodes

class HTML_Translator (html4css1.HTMLTranslator) :
    """Custom HTML translator to change the generation of anchors."""

    def visit_reference(self, node):
        atts = {'class': 'reference'}
        if 'refuri' in node:
            atts['href'] = node['refuri']
            if ( self.settings.cloak_email_addresses
                 and atts['href'].startswith('mailto:')):
                atts['href'] = self.cloak_mailto(atts['href'])
                self.in_mailto = 1
            atts['class'] += ' external'
        else:
            assert 'refid' in node, \
                   'References must have "refuri" or "refid" attribute.'
            atts['href'] = '#' + node['refid']
            atts['class'] += ' internal'
        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts['class'] += ' image-reference'
        self.body.append(self.starttag(node, 'a', '', **atts))
    # end def visit_reference

    def depart_reference(self, node):
        self.body.append('</a>')
        if not isinstance(node.parent, nodes.TextElement):
            self.body.append('\n')
        self.in_mailto = 0
    # end def depart_reference

# end class HTML_Translator

class HTML_Writer (html4css1.Writer) :
    """This docutils writer will use the MyHTMLTranslator class below."""

    def __init__ (self) :
        html4css1.Writer.__init__ (self)
        self.translator_class = HTML_Translator
    #end def __init__

# end class HTML_Writer

if __name__ != "__main__" :
    ReST._Export ("*")
### __END__ ReST.HTML_Writer
