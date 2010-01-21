# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
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
#    JNJ.Environment
#
# Purpose
#    Provide wrapper around jinja2.Environment
#
# Revision Dates
#    29-Dec-2009 (CT) Creation
#    13-Jan-2010 (CT) `GTW` converted from module to class instance
#    21-Jan-2010 (MG) `I18N` support added
#    21-Jan-2010 (CT) Bug fixed
#    ««revision-date»»···
#--

from   _JNJ               import JNJ
from   _TFL               import TFL

import _JNJ.Onion
import _JNJ.GTW

from   _TFL               import sos
from   _TFL.predicate     import uniq
import _TFL.I18N

from   jinja2             import Environment, FileSystemLoader, ChoiceLoader

def HTML \
        ( version   = "html/5.jnj"
        , load_path = ()
        , loader    = None
        , globals   = {}
        , i18n      = False
        , ** kw
        ) :
    if load_path :
        assert loader is None
        encoding = kw.pop ("encoding", "iso-8859-1")
        loader   = FileSystemLoader (load_path, encoding)
    jnj_loader   = FileSystemLoader (sos.path.dirname (__file__), "iso-8859-1")
    if loader is None :
        loader   = jnj_loader
    else :
        loader   = ChoiceLoader ((loader, jnj_loader))
    extensions   = \
        ( kw.pop ("extensions", [])
        + ["jinja2.ext.loopcontrols", "jinja2.ext.do", JNJ.Onion]
        )
    if i18n :
        extensions.append ("jinja2.ext.i18n")
    result = Environment  \
        ( extensions = uniq (extensions), loader = loader, ** kw)
    result.globals.update \
        ( globals
        , GTW          = JNJ.GTW (result)
        , html_version = version
        )
    if translation :
        env.install_gettext_translations (TFL.I18N)
    return result
# end def HTML

__doc__ = """
`HTML` creates an environment suitable for generating HTML from jinja
templates. Per default, `HTML` sets `html_version` to a macro template
for HTML5.

    >>> env5 = HTML ()

Passing `version = "html/x.jnj"` to `HTML` sets up an environment with
`html_version` referring to a macro template for XHTML.

    >>> envx = HTML (version = "html/x.jnj")

By importing `html_version` as `x` and calling macros defined by `X`,
a single template can generate either HTML5 or XHTML output, depending
on how the environment was set up::

    >>> template = '''
    ... {%- import html_version as X -%}
    ... {%- call X.html (lang = "de") -%}
    ...   {%- call X.section (id = "foo", class = "bar") -%}
    ...     A sample section for testing the differences between
    ...     html5 and xhtml.
    ...   {%- endcall -%}
    ...
    ...   {%- set a = None %}
    ...   {%- set b = 42 %}
    ...   {%- set c = "cccc" %}
    ...   {{ GTW.firstof (a, b, c, d, "default first of") }}
    ...   {{ GTW.firstof (b, c, d, "default first of") }}
    ...   {{ GTW.firstof (c, d, "default first of") }}
    ...   {{ GTW.firstof (d, "default first of") }}
    ...   {{ GTW.firstof ("default first of") }}
    ... {%- endcall -%}
    ... '''

    >>> t5 = env5.from_string (template)
    >>> tx = envx.from_string (template)
    >>> print t5.render ()
    <!DOCTYPE html>
    <html lang="de">
    <BLANKLINE>
    <section  id="foo" class="bar">
      A sample section for testing the differences between
        html5 and xhtml.
    </section>
    <BLANKLINE>
      42
      42
      cccc
      default first of
      default first of
    </html>
    <BLANKLINE>
    >>> print tx.render ()
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
    >
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de" lang="de" >
    <BLANKLINE>
    <div class="section bar"  id="foo">
      A sample section for testing the differences between
        html5 and xhtml.
    </div>
    <BLANKLINE>
      42
      42
      cccc
      default first of
      default first of
    </html>
    <BLANKLINE>
    >>> print t5.render (d = "qux")
    <!DOCTYPE html>
    <html lang="de">
    <BLANKLINE>
    <section  id="foo" class="bar">
      A sample section for testing the differences between
        html5 and xhtml.
    </section>
    <BLANKLINE>
      42
      42
      cccc
      qux
      default first of
    </html>
    <BLANKLINE>
    >>> print tx.render (d = "qux")
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
    >
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de" lang="de" >
    <BLANKLINE>
    <div class="section bar"  id="foo">
      A sample section for testing the differences between
        html5 and xhtml.
    </div>
    <BLANKLINE>
      42
      42
      cccc
      qux
      default first of
    </html>
    <BLANKLINE>

"""

if __name__ != "__main__" :
    JNJ._Export_Module ()
### __END__ JNJ.Environment
