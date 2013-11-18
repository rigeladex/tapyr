# -*- coding: utf-8 -*-
# Copyright (C) 2006-2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin.glueck@gmail.com
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
#    DJO.Apps.Base.templatetags.Tags
#
# Purpose
#    Collection of useful template tags.
#
# Revision Dates
#    22-Jul-2006 (MG) Creation
#     2-Dec-2006 (MG) Style dependency added to `Stylesheet_Links`
#    10-Dec-2006 (MG) `Style_Image` added
#    16-Dec-2006 (MG) Use new function `user_style_url`
#    16-Dec-2006 (MG) Usage of `URL_PREFIX` removed
#    06-May-2007 (MG) Re-Creation
#    06-May-2007 (MG) Generalized the `stylesheet` handling to support
#                     javascript as well
#    12-Jun-2007 (MG) Do not use thread locals anymore
#    18-Jun-2007 (MG) `_Node_.iter_render` added
#    02-Oct-2007 (MG) `token_parse` support for `remainig` added
#    02-Oct-2007 (MG) New `remainig` featue used in `add_include_file`
#    18-Nov-2007 (MG) `add_include_file`: `weight` parameter made optional
#     3-Dec-2007 (MG) `cond_url:Conditional_URL_Node` tag added
#    14-Dec-2007 (MG) `_Mode_.iter_render` removed again
#    14-Dec-2007 (CT) Moved into package DJO
#    17-Dec-2007 (MG) `Menu_Block_Node` fixed
#     5-Jan-2008 (MG) `Conditional_URL_Node`: allow parameter less revers urls
#    10-Jan-2008 (MG) Support varuable lookup in `Menu_Block_Node`
#    17-Feb-2008 (MG) `add_include_file`: default weight changed to 500
#    17-Feb-2008 (MG) `token_parse` Parameter `remove_quotes` added
#    17-Feb-2008 (MG) `menublock` tag changed to `menuitem`
#    14-May-2009 (CT) Moved to `_DJO._Apps.Base`
#    ««revision-date»»···
#--

from   django                      import template
import django.template.loader
from   django.core.urlresolvers    import reverse

from   django.conf import settings
import sys
import os
import re

user_style = "default"

register = template.Library ()

class _Node_ (template.Node) :
    """Simplifies the subclassing of template.Node"""

    defaults = dict ()

    def __init__ (self, ** kw) :
        for k, v in kw.iteritems () :
            if v is None :
                v = self.defaults.get (k, v)
            setattr (self, k, v)
    # end def __init__

# end class _Node_

class Render_Context_Node (_Node_) :
    """"""

    def render (self, context) :
        return self.content.render (context).strip ()
    # end def render

# end class Render_Context_Node

class _Template_Node_ (_Node_) :
    """Root class for node which renders a template."""

    template_name = None
    nodelist      = None
    display       = True

    def __init__ (self, ** kw) :
        for k, v in kw.iteritems () :
            if v is None :
                v = self.defaults.get (k, v)
            setattr (self, k, v)
        self._attrs = kw.keys ()
        if self.nodelist is None :
            self.__class__.nodelist = \
                template.loader.get_template (self.template_name).nodelist
    # end def __init__

    def render (self, context) :
        context ["FP"] = dict ()
        if hasattr (self, "content") :
            context ["FP"] ["content"] = self.content.render (context).strip ()
        self._update_context (context)
        if self.display :
            return self.nodelist.render (context).strip ()
        return ""
    # end def render

    def _update_context (self, context) :
        FP = context ["FP"]
        for attr in self._attrs :
            if attr not in FP :
                FP [attr] = getattr (self, attr)
    # end def _update_context

    @classmethod
    def New (cls, name, template_name) :
        return type (cls) (name, (cls, ), dict (template_name = template_name))
    # end def New

    def __repr__ (self) :
        return "<%s `%s`>" % (self.__class__.__name__, self.template_name)
    # end def __repr__

# end class _Template_Node_

def token_parse ( token
                , map           = ()
                , optional      = sys.maxint
                , tag           = None
                , pattern       = None
                , end_tag       = None
                , parser        = None
                , remainig      = None
                , remove_quotes = True
                ) :
    if not isinstance (token, (list, tuple)) :
        parts  = token.split_contents ()
    else :
        parts  = token
    tag_name   = parts [0]
    if tag and tag != tag_name :
        msg  = "Unexpected tag found (Expected %r, found %r)" % (tag, tag_name)
        raise template.TemplateSyntaxError, msg
    parameters = parts [1:]
    if pattern :
        para_string = " ".join (parameters)
        match       = pattern.search (para_string)
        if not match :
            msg = "Parameter could not be parsed for %r (%r, Pattern %r)" \
                % (tag_name, para_string, pattern.pattern)
            raise template.TemplateSyntaxError, msg
        md = match.groupdict ()
        if md :
            return tag_name, md
        parameters = match.groups ()
    else :
        if remove_quotes :
            parameters = [p.strip ('"') for p in parameters]
        else :
            parameters = list (parameters)
        if map :
            map_len  = len (map)
            if remainig is None :
                max_length = map_len
            else :
                max_length = sys.maxint
            min_length = min (optional, max_length)
            if not (min_length <= len (parameters) <= max_length) :
                if len (parameters) < min_length  :
                    msg = "%r requires at least %d parameters (only %d given)" \
                        % (tag_name, min_length, len (parameters))
                else :
                    msg = "%r takes at most %d parameters (%d given)" \
                        % (tag_name, max_length, len (parameters))
                raise template.TemplateSyntaxError, msg
            result = {}
            values = parameters + [None] * (map_len - len (parameters))
            for name, value in zip (map, values) :
                if name is not None :
                    result [name] = value
            if remainig :
                result [remainig] = values [map_len:]
        elif remainig :
            result = { remainig : parameters}
        else :
            result = dict (enumerate (parameters))
    if parser :
        if not end_tag :
            end_tag = ("end%s" % (tag_name, ), )
        result ["content"] = parser.parse (end_tag)
        ### the parser stops right at the end token (but has not yet consumed
        ### it)
        parser.delete_first_token         ()
    return tag_name, result
# end def token_parse

def new_block_template_tag (register, name, Node_Class, * args, ** kw) :
    def _parse_tag (parser, token) :
        if "parser" in kw :
            kw ["parser"] = parser
        tag, parameters = token_parse (token, tag = name, * args, ** kw)
        return Node_Class (** parameters)
    # end def _parse_tag
    register.tag (name, _parse_tag)
# end def new_block_template_tag

Empty       = template.TextNode ("")

Include_Files = {}

@register.tag
def add_include_file (parser, token) :
    tag, param = token_parse \
        ( token, ("weight", "file"), 1
        , remainig = "additional_files"
        , tag      = "add_include_file"
        )
    files  = list (param ["additional_files"])
    file   = param ["file"]
    if file :
        files.insert (0, file)
    weight = param ["weight"]
    try :
        weight = int (weight or "500")
    except ValueError :
        if weight :
            files.insert (0, weight)
        weight = 500
    Include_Files.setdefault \
        (settings.SITE_ID, {}).setdefault (weight, []).extend (files)
    return Empty
# end def add_include_file

class Include_File_Link (_Node_) :

    tags = dict \
        ( css = (True,  '<link rel="stylesheet" type="text/css" href="%s" />')
        , js  = (True,  '<script src="%s" type="text/javascript"></script>'  )
        )

    def render (self, context) :
        global Include_Files
        result = []
        files  = Include_Files.get (settings.SITE_ID, {})
        for _, files in sorted \
            (files.iteritems (), key = lambda (w, f) : w) :
            for file in files :
                kind = os.path.splitext (file) [-1] [1:]
                style, tag = self.tags [kind]
                url = file
                result.append (tag % (url, ))
        Include_Files = {}
        return "\n  ".join (result).strip ()
    # end def render

# end class Include_File_Link

new_block_template_tag (register, "include_file_tags", Include_File_Link)

class Style_Image (_Node_) :
    """Renders an image tag with the actual image url being style dependent"""

    var_pattern = re.compile ("{{\s*([\w.]+)\s*}}")

    def _resolve_var (self, match) :
        return template.resolve_variable (match.group (1), self.context)
    # end def _resolve_var

    def render (self, context) :
        self.context = context
        image        = self.var_pattern.sub (self._resolve_var, self.image)
        url          = Style.user_style_url \
            ("%sstatic/images/%%s/%s" % (settings.MEDIA_URL, image)) [0]
        size_atts    = []
        for attr in "width", "height" :
            size = getattr (self, attr, None)
            if size is not None :
                size_atts.append (' %s="%s"' % (attr, size))
        alt = self.var_pattern.sub \
            (self._resolve_var, self.alt or os.path.basename (self.image))
        return '<img src="%s" alt="%s"%s />' % (url, alt, "".join (size_atts))
    # end def render

# end class Style_Image

new_block_template_tag \
    ( register, "image", Style_Image
    , ("image", "alt", "width", "height"), 1
    )

class Conditional_URL_Node (_Node_) :
    """Conditional reverse lookup for urls."""

    literal_pat      = re.compile ("^[\"'].*[\"#]$")
    context_variable = None

    def __init__ (self, * args, ** kw) :
        super (Conditional_URL_Node, self).__init__ (* args, ** kw)
        if self.parameters [-2].strip () == "as" :
            self.context_variable = self.parameters [-1]
            self.parameters       = self.parameters [:-2]
    # end def __init__

    def render (self, context) :
        decision = self.decision
        if not self.literal_pat.match (decision) :
            decision = template.resolve_variable (decision, context)
        fct = int if len (self.parameters) > 2 else bool
        try :
            decision = fct (decision)
        except TypeError :
            return "error"
        split = self.parameters [decision].split ("=", 1)
        args  = []
        kw    = {}
        if len (split) > 1 :
            url_name, para_spec = split
            for value in para_spec.split (",") :
                name = None
                if "=" in value :
                    name, value = value.split ("=", 1)
                if value != "NONE" :
                    if not self.literal_pat.match (value) :
                        value = template.resolve_variable (value, context)
                    if name :
                        kw [name] = value
                    else :
                        args.append (value)
        else :
            url_name = split [0]
        url = reverse (url_name, args = args, kwargs = kw)
        if self.context_variable :
            context [self.context_variable] = url
            return ""
        return url
    # end def render

# end class Conditional_URL_Node

new_block_template_tag \
    ( register, "cond_url", Conditional_URL_Node
    , ("decision", )
    , optional = 1
    , remainig = "parameters"
    )

class Menu_Block_Node (_Node_) :

    def __init__ ( self, content, name = None, match_url = None
                 , href              = None
                 , anchor_attributes = ()
                 ) :
        ### import pdb; pdb.set_trace ()
        self.name                  = name
        self.content               = content
        self.match_url             = match_url
        self.href                  = href or match_url
        anchor_attributes          = []
        for p in anchor_attributes :
            name, value            = p.split ("=", 1)
            anchor_attributes.append \
                ('%s="%s"' % (name.strip (), value.strip ('"').strip ()))
        self.anchor_attributes     = ""
        if anchor_attributes :
            self.anchor_attributes = " %s" % (" ".join (anchor_attributes))
    # end def __init__

    def _reverse_url (self, spec, context = None) :
        if spec.startswith ('"') :
            ### literal url
            return spec.strip ('"').strip ()
        args = []
        kw   = {}
        if "|" in spec :
            spec, parameters = spec.split ("|")
            for v in parameters.split (":") :
                n = None
                if "=" in v :
                    n, v = p.split ("=")
                if context and not v.startswith ('"') :
                    try :
                        v = template.resolve_variable (v, context)
                    except template.VariableDoesNotExist :
                        v = ""
                if n :
                    kw [n] = v
                else :
                    args.append (v)
        try :
            return reverse (spec, args = args, kwargs = kw)
        except :
            return "<<no-reverse-match>>"
    # end def _reverse_url

    def render (self, context) :
        ### import pdb; pdb.set_trace ()
        href      = self._reverse_url (self.href,      context = context)
        match     = self._reverse_url (self.match_url, context = context)
        match_len = len (match)
        path      = context ["request"].path
        as_link   = True
        if path [:match_len] == match :
            as_link     = False
            #if exact and len (path) != match_len :
            #    as_link = True
        result    = []
        item_name = "menu_item_%s" % (self.name, )
        ### import pdb; pdb.set_trace ()
        if as_link :
            result.append ('<a href="%s"%s>' % (href, self.anchor_attributes, ))
            context [item_name] = "hidden"
        else :
            context [item_name] = ""
        result.append     (self.content.render (context).strip ())
        if as_link :
            result.append ("</a>")
        ## import pdb; pdb.set_trace ()
        return "".join (result)
    # end def render

# end class Menu_Block_Node

new_block_template_tag \
    ( register, "menuitem", Menu_Block_Node, ("name", "match_url", "href")
    , optional      = 2
    , remainig      = "anchor_attributes"
    , parser        = True
    , remove_quotes = False
    )

### __END__ DJO.Apps.Base.templatetags.Tags
