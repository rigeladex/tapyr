# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
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
#    JNJ.Onion
#
# Purpose
#    Provide Jinja extension for a `onion` tag
#
# Revision Dates
#    29-Dec-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _JNJ               import JNJ

from   jinja2     import nodes
from   jinja2.ext import Extension

class Onion (Extension) :
    """Jinja extension providing a `onion` tag.

       >>> from _JNJ.Environment import HTML

       >>> env = HTML ()
       >>> template = '''
       ...   {%- onion foo %}
       ...     {% head %}
       ...       I am the onion then head
       ...     {% else %}
       ...       I am the onion else head
       ...     {% body %}
       ...       And this is the body which should be enclosed by the head/tail
       ...     {% tail %}
       ...       I am the onion then tail
       ...     {% else %}
       ...       I am the onion else tail
       ...   {% endonion -%}
       ... '''
       >>> t = env.from_string (template)
       >>> t.render (foo = True)
       u'\\n      I am the onion then head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion then tail\\n    '
       >>> t.render (foo = False)
       u'\\n      I am the onion else head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion else tail\\n  '

       ### The else tags inside the head/tail are optional
       >>> template = '''
       ...   {%- onion foo %}
       ...     {% head %}
       ...       I am the onion then head
       ...     {% body %}
       ...       And this is the body which should be enclosed by the head/tail
       ...     {% tail %}
       ...       I am the onion then tail
       ...     {% else %}
       ...       I am the onion else tail
       ...   {% endonion -%}
       ... '''
       >>> t = env.from_string (template)
       >>> t.render (foo = True)
       u'\\n      I am the onion then head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion then tail\\n    '
       >>> t.render (foo = False)
       u'\\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion else tail\\n  '
       >>> template = '''
       ...   {% onion foo %}
       ...     {% head %}
       ...       I am the onion then head
       ...     {% else %}
       ...       I am the onion else head
       ...     {% body %}
       ...       And this is the body which should be enclosed by the head/tail
       ...     {% tail %}
       ...       I am the onion then tail
       ...   {% endonion %}
       ... '''.strip ()
       >>> t = env.from_string (template)
       >>> t.render (foo = True)
       u'\\n      I am the onion then head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion then tail\\n  '
       >>> t.render (foo = False)
       u'\\n      I am the onion else head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    '
    """

    tags = set (("onion", ))

    def parse (self, parser) :
        tag    = parser.stream.current
        lineno = parser.stream.next ().lineno
        cond   = parser.parse_expression ()
        ### first, seek to the start of the "head" token
        parser.parse_statements (["name:head"], drop_needle = True)
        h_then = parser.parse_statements (["name:else", "name:body"])
        if parser.stream.current.value == "else" :
            parser.stream.next ()
            h_else = parser.parse_statements (["name:body"])
        else :
            h_else = None
        parser.stream.next ()
        body   = parser.parse_statements (["name:endonion", "name:tail"])
        result = [nodes.If ( cond, h_then, h_else)]
        result.extend (body)
        if parser.stream.current.value == "tail" :
            parser.stream.next ()
            t_then = parser.parse_statements (["name:else", "name:endonion"])
            if parser.stream.current.value == "else" :
                parser.stream.next ()
                t_else = parser.parse_statements (["name:endonion"])
            else :
                t_else = None
            result.append (nodes.If (cond, t_then, t_else))
        parser.stream.next ()
        return result
    # end def parse

# end class Onion

if __name__ != "__main__" :
    JNJ._Export ("Onion")
### __END__ JNJ.Onion
