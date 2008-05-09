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
#    14-Mar-2008 (MG) `Path_Starts_With` tag and `query` and `count` filters
#                     added
#    17-Mar-2008 (MG) `Path_Starts_With` removed, tag `Iterate` added
#     9-May-2008 (CT) Style
#     9-May-2008 (MG) `Onion` tag added
#    ««revision-date»»···
#--

"""
>>> from django.conf     import settings
>>> settings.configure (ROOT_URLCONF = "_DJO._test_url_conf")
>>> from django.template import add_to_builtins, Template, Context
>>> add_to_builtins ("_DJO.templatetags.TGL_Tags")
"""

from   django                      import template
from   django.template.loader      import render_to_string

from   _DJO                        import DJO
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

    def __init__ (self, node_list = None) :
        self.node_list = node_list or template.NodeList ()
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

       >>> from django.template import Template, Context
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

class Iterate (Tag) :
    """Add an iterable to the context. Calling `iter.next` will change the
       current value of `iter`. Once the end of the sequence is readched, it
       will be reset and starts all over again.
       This is simmilar to the cycle that except that `cycling` trough the
       list of values and receving the current value is seperated.

       >>> from django.template import Template, Context
       >>> template = '''
       ...   {% iterate "a", "b", "c" as iter%}
       ...   {{ iter.next }}
       ...   {{ iter.next }}
       ...   {{ iter }}
       ...   {{ iter.next }}
       ...   {{ iter.next }}
       ...   {{ iter }}
       ...   {{ iter.next }}
       ...   {{ iter }}
       ... '''.strip ()
       >>> t = Template (template)
       >>> t.render (Context ({}))
       u'\\n  a\\n  b\\n  b\\n  c\\n  a\\n  a\\n  b\\n  b'
    """

    def __init__ (self, name, sequence) :
        self.name     = name
        self.sequence = sequence
    # end def __init__

    def render (self, context) :
        context [self.name] = self.sequence
        self.sequence.update_filters (context)
        return ""
    # end def render

    class _Iterable_ (object) :

        def __init__ (self, sequence) :
            self.sequence = sequence
            self.length   = len (sequence)
            self.index    = -1
        # end def __init__

        def update_filters (self, context) :
            self.sequence = [item (context) for item in self.sequence]
        # end def update_filters

        def next (self) :
            self.index    = (self.index + 1) % self.length
            return str (self)
        # end def netx

        def __str__ (self) :
            return self.sequence [self.index]
        # end def __str__
    # end class _Iterable_

    @classmethod
    def parse (cls, parser, token) :
        name, args             = token.contents.split (" ", 1)
        sequence, _, name      = args.strip ().rsplit (" ", 2)
        sequence = \
            [Filter_Exp (parser, p.strip ()) for p in sequence.split (",")]
        template_name, _, rest = split_hst (args.strip (), ",")
        return cls (name, cls._Iterable_ (sequence))
    # end def parse

# end class Iterate

class Onion (Tag) :
    """Enclose a block with a head/tail based on a condition:

       >>> from django.template import Template, Context
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
       ...     {% else %}
       ...       I am the onion else tail
       ...   {% endonion %}
       ... '''.strip ()
       >>> t = Template (template)
       >>> t.render (Context (dict (foo = True)))
       u'\\n      I am the onion then head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion then tail\\n    '
       >>> t.render (Context (dict (foo = False)))
       u'\\n      I am the onion else head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion else tail\\n  '

       ### The else tag inside the head/tail or optionally
       >>> template = '''
       ...   {% onion foo %}
       ...     {% head %}
       ...       I am the onion then head
       ...     {% body %}
       ...       And this is the body which should be enclosed by the head/tail
       ...     {% tail %}
       ...       I am the onion then tail
       ...     {% else %}
       ...       I am the onion else tail
       ...   {% endonion %}
       ... '''.strip ()
       >>> t = Template (template)
       >>> t.render (Context (dict (foo = True)))
       u'\\n      I am the onion then head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion then tail\\n    '
       >>> t.render (Context (dict (foo = False)))
       u'\\n      I am the onion then head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion else tail\\n  '
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
       >>> t = Template (template)
       >>> t.render (Context (dict (foo = True)))
       u'\\n      I am the onion then head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion then tail\\n  '
       >>> t.render (Context (dict (foo = False)))
       u'\\n      I am the onion else head\\n    \\n      And this is the body which should be enclosed by the head/tail\\n    \\n      I am the onion then tail\\n  '
    """

    def __init__ (self, condition, node_list, head, tail) :
        self.condition = condition
        self.head      = head
        self.tail      = tail
        self.node_list = node_list
    # end def __init__

    def render (self, context) :
        use_else = not bool (self.condition (context))
        head     = self.head [use_else] or self.head [0]
        tail     = self.tail [use_else] or self.tail [0]
        return "".join \
            ( ( head and  head.render (context)
              , self.node_list.render (context)
              , tail and  tail.render (context)
              )
            )
    # end def render

    @classmethod
    def parse (cls, parser, token) :
        name, condition = token.contents.split (" ", 1)
        condition  = Filter_Exp                (parser, condition)
        skip       = parser.parse              (("head", ))
        parser.delete_first_token              ()
        head       = cls._then_else            (parser, "body")
        node_list  = parser.parse              (("tail", ))
        parser.delete_first_token              ()
        tail       = cls._then_else            (parser, "endonion")
        return cls (condition, node_list, head, tail)
    # end def parse

    @classmethod
    def _then_else (cls, parser, end_token) :
        then_block = parser.parse      (("else", end_token))
        token      = parser.next_token ()
        if token.contents == "else" :
            else_block = parser.parse   ((end_token, ))
            parser.delete_first_token   ()
        else :
            else_block = None
        return then_block, else_block
    # end def _then_else

# end class Onion

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.templatetags.TGL_Tags
