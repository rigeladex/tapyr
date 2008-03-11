# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    DJO.templatetags.TGL_Tags
#
# Purpose
#    Tanzer and Glueck's library of custom django template tags
#
# Revision Dates
#    28-Feb-2008 (CT) Creation
#    29-Feb-2008 (CT) Filter `starts_with` added
#    29-Feb-2008 (CT) `RRender.parse` changed to allow call without bindings
#    11-Mar-2008 (MG) Use `Filter_Exp` for `RRender.file_name`
#    ««revision-date»»···
#--

from   django                      import template
from   django.template             import defaultfilters
from   django.template.loader      import render_to_string

from   _TFL.predicate              import split_hst

register = template.Library ()

class M_Tag (template.Node.__class__) :
    """Meta class for Tag classes"""

    def __init__ (cls, name, bases, dict) :
        super (M_Tag, cls).__init__ (name, bases, dict)
        if "parse" in dict :
            register.tag (name.lower (), cls.parse)
    # end def __init__

# end class M_Tag

class Tag (template.Node) :
    __metaclass__ = M_Tag
# end class Tag

class Block_Exp (object) :
    """A block of a template usable as an expression"""

    def __init__ (self, node_list) :
        self.node_list = node_list
    # end def __init__

    def __call__ (self, context) :
        return self.node_list.render (context).strip ()
    # end def __call__

# end class Block_Exp

class Filter_Exp (object) :
    """A filter expression of a template"""

    def __init__ (self, parser, expression) :
        self.x = parser.compile_filter (expression)
    # end def __init__

    def __call__ (self, context) :
        return self.x.resolve (context)
    # end def __call__

# end class Filter_Exp

class BLet (Tag) :
    """BLet tag"""

    def __init__ (self, name, node_list) :
        self.name  = name
        self.block = Block_Exp (node_list)
    # end def __init__

    def render (self, context) :
        context [self.name] = self.block (context)
        return ""
    # end def render

    @classmethod
    def parse (cls, parser, token) :
        """Add the output of the block as a variable to the context."""
        name, rest   = token.contents.split (" ", 1)
        node_list    = parser.parse         (("end%s" % (name,), ))
        parser.delete_first_token ()
        return cls (rest, node_list)
    # end def parse

# end class BLet

class _Binding_Tag_ (Tag) :
    """Base class for tags that bind some names in the context before
       rendering.
    """

    def render (self, context) :
        context.push ()
        for k, x in self.binding_dict.iteritems () :
            context [k] = x (context)
        result = self._render (context)
        context.pop ()
        return result
    # end def render

    @classmethod
    def _parse_bindings (cls, parser, rest) :
        binding_dict = {}
        if rest :
            args = rest.split (";")
            for k, x in ([t.strip () for t in a.split ("=")] for a in args) :
                binding_dict [k] = Filter_Exp (parser, x)
        return binding_dict
    # end def parse

# end class _Binding_Tag_

class Let (_Binding_Tag_) :
    """Let tag.

       >>> from django.template import Template, Context, add_to_builtins
       >>> from django.conf     import settings
       >>> settings.configure ()
       >>> add_to_builtins ("_DJO.templatetags.TGL_Tags")
       >>> template = '''
       ...   {% let a=42 ; b = "foobar" ; c = Hugo|upper %}
       ...     a = {{ a }}
       ...     b = {{ b }}
       ...     c = {{ c }}
       ...   {% endlet %}
       ... '''.strip ()
       >>> t = Template (template)
       >>> t.render (Context ({}))
       u'\\n    a = 42\\n    b = foobar\\n    c = \\n  '
       >>> t.render (Context ({"Hugo" : "affe"}))
       u'\\n    a = 42\\n    b = foobar\\n    c = AFFE\\n  '

    """

    def __init__ (self, binding_dict, node_list) :
        self.binding_dict = binding_dict
        self.node_list    = node_list
    # end def __init__

    def _render (self, context) :
        return self.node_list.render (context)
    # end def _render

    @classmethod
    def parse (cls, parser, token) :
        """Add a set of values to the context."""
        name, _, rest = split_hst            (token.contents, " ")
        binding_dict  = cls._parse_bindings  (parser, rest)
        node_list     = parser.parse         (("end%s" % (name,), ))
        parser.delete_first_token ()
        return cls (binding_dict, node_list)
    # end def parse

# end class Let

class RRender (_Binding_Tag_) :
    """Render tag."""

    def __init__ (self, template_name, binding_dict) :
        self.template_name = template_name
        self.binding_dict  = binding_dict
    # end def __init__

    def _render (self, context) :
        return render_to_string (self.template_name (context), context)
    # end def _render

    @classmethod
    def parse (cls, parser, token) :
        """Add a set of values to the context."""
        name, args             = token.contents.split (" ", 1)
        template_name, _, rest = split_hst (args.strip (), " ")
        binding_dict           = cls._parse_bindings (parser, rest)
        return cls (Filter_Exp (parser, template_name), binding_dict)
    # end def parse

# end class RRender

@register.filter
@defaultfilters.stringfilter
def starts_with (value, prefix) :
    """Returns the result of `value.startswith (prefix)`"""
    return value and value.startswith (prefix)
# end def starts_with

if __name__ != "__main__":
    from _DJO import DJO
    DJO._Export ("*")
### __END__ DJO.templatetags.TGL_Tags
