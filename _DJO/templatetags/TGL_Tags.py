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
#    ««revision-date»»···
#--
"""
>>> from django.conf     import settings
>>> settings.configure (ROOT_URLCONF = "_DJO._test_url_conf")
>>> from django.template import add_to_builtins, Template, Context
>>> add_to_builtins ("_DJO.templatetags.TGL_Tags")
>>> template = '''
...   {{ var|starts_with:"foo"}}
...   {{ var|starts_with:"fooa"}}
...   {{ var|starts_with:"afoo"}}
...   {{ var|starts_with:"fo"}}
... '''
>>> t = Template (template)
>>> t.render (Context (dict (var = "foo"))).strip ()
u'True\\n  False\\n  False\\n  True'
>>> t.render (Context (dict (var = ""))).strip ()
u''
"""

from   django                      import template
from   django.template             import defaultfilters
from   django.template.loader      import render_to_string
from   django.core.urlresolvers    import reverse, NoReverseMatch

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

class Path_Starts_With (Tag) :
    """Allows to easily build a navigation link. The tag splits the `content`
       into two parts around the `else` tag.

       If the current URL (request.path) starts with `prefix` the first
       part (from the start to the `else` tag) will be rendered, if not, the
       second part (from the `else` tag to the end) will be rendered.

       The parameters of the tga are:
       * url-or-name
         a real URL or the name of the an url pattern used with the `reverse`
         function. The resulting URl will be used to dermine if the a
         `active` or the `link` block should be rendered.
       * parameters to the `reverse` function in the form of:
         - `parameter`
         - name=`parameter`

         In both cases, `parameter` will be treated as a filter expression
         (which allows you to apply filters to them as well)

       >>> from django.template import Template, Context
       >>> class REQUEST : path = "http://a/b/c/"
       >>> template = '''
       ...   {% path_starts_with "http://a/b/" %}
       ...     aaa
       ...   {% else %}
       ...     <a href="aaa">aaa</a>
       ...   {% endpath_starts_with %}
       ... '''.strip ()
       >>> t = Template (template)
       >>> t.render (Context (dict (request = REQUEST)))
       u'aaa'
       >>> t.render (Context ())
       u'<a href="aaa">aaa</a>'
       >>> template = '''
       ...   {% path_starts_with "test-path-starts-with" %}
       ...     aaa
       ...   {% else %}
       ...     <a href="aaa">aaa</a>
       ...   {% endpath_starts_with %}
       ... '''.strip ()
       >>> t = Template (template)
       >>> REQUEST.path = "/this/is/nice/"
       >>> t.render (Context (dict (request = REQUEST)))
       u'aaa'
       >>> REQUEST.path = "/this/is/not/nice/"
       >>> t.render (Context (dict (request = REQUEST)))
       u'<a href="aaa">aaa</a>'
    """

    def __init__ (self, prefix, node_list_match, node_list_else) :
        self.prefix           = prefix
        self.node_list_match  = node_list_match
        self.node_list_else   = node_list_else
    # end def __init__

    def render (self, context) :
        prefix  = self._as_url (context, * self.prefix)
        request = context.get ("request", None)
        path    = (request and request.path) or ""
        if path.startswith (prefix) :
            ### looks like this should not be a href
            result = self.node_list_match (context)
        else :
            result = self.node_list_else  (context)
        return result
    # end def render

    def _as_url (self, context, name, rev_args, rev_kw) :
        name = name (context)
        try :
            args = [a (context) for a in rev_args]
            kw   = dict ((n, v (context)) for (n, v) in rev_kw.iteritems ())
            return reverse (name, args = args, kwargs = kw)
        except NoReverseMatch :
            return name
    # end def _as_url

    @classmethod
    def _parse_url_spec (cls, parser, rev_spec) :
        rev_args = []
        rev_kw   = {}
        for p in rev_spec.split (";") :
            if "=" in p :
                k, v       = (x.strip () for x in p.split ("=", 1))
                rev_kw [k] = Filter_Exp (parser, v)
            else :
                rev_args.append (Filter_Exp (parser, p))
        return rev_args, rev_kw
    # end def _parse_url_spec

    @classmethod
    def parse (cls, parser, token) :
        name, args           = token.contents.split (" ", 1)
        url_specs            = [p.strip () for p in args.split (" ", 1)]
        url_or_name          = Filter_Exp (parser, url_specs [0])
        rev_args             = ()
        rev_kw               = {}
        if len (url_specs) > 1 :
            rev_args, rev_kw = cls._parse_url_spec (parser, url_specs [1])
        elif len (url_specs) > 2 :
            raise template.TemplateSyntaxError \
                ( "%s only expects 2 parameters (%d given)"
                % (cls.__name__, len (url_specs))
                )
        node_list_match = Block_Exp \
            (parser.parse (("end%s" % (name, ), "else")))
        token             = parser.next_token ()
        if token.contents == "else" :
            node_list_else = Block_Exp (parser.parse (("end%s" % (name,), )))
            parser.delete_first_token    ()
        else :
            node_list_else = Block_Exp ()
        return cls \
            ((url_or_name, rev_args, rev_kw), node_list_match, node_list_else)
    # end def parse

# end class Navigation_Entry

@register.filter
@defaultfilters.stringfilter
def starts_with (value, prefix) :
    """Returns the result of `value.startswith (prefix)`"""
    return value and value.startswith (prefix)
# end def starts_with

@register.filter
def query (query_set, query) :
    """Filters the `query_set` according the `query` spec. The syntac of the
       `query` spec is the same as used in normal python code:
      {{ query_set|query:"name__exact = 'hansi', status__gt = 2"}}
    """
    ### str is needed to convert the unicode string into a normal string or
    ### else manager.filter` will not work
    filter = dict ( ([ str (p).strip () for p in cond.split ("=")]
                         for cond in query.split (",")
                    )
                  )
    return query_set.filter (** filter)
# end def query

@register.filter
def qs_count (query_set) :
    """Runs the `count` method of the passed query set. This could be achived
       using the `length` filter as well. But using the count filter the a
       the calculation will be done by the database engine and not in python
    """
    return query_set.count ()
# end def qs_count

if __name__ != "__main__":
    from _DJO import DJO
    DJO._Export ("*")
### __END__ DJO.templatetags.TGL_Tags
