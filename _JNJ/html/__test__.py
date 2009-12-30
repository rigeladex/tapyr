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
#    __test__
#
# Purpose
#    Doctest for thml templates of package namespace `JNJ`
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    ««revision-date»»···
#--
"""

    >>> page = Record (copyright = None, Media = None, NAV = None, top = None)
    >>> env5 = HTML (globals = dict (page = page))
    >>> envx = HTML (version = "html/x.jnj", globals = dict (page = page))
    >>> t5 = env5.from_string (template)
    >>> tx = envx.from_string (template)

    >>> print t5.render (page = page)
    <!DOCTYPE html>
    <html lang="en">
      <head>
      <!--[if IE]>
        <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
      <![endif]-->
      <meta http-equiv="Content-Type"
            content="text/html; charset=iso-8859-15"
          />
              <title>None</title>
    <BLANKLINE>
            <meta name="copyright" content=" " />
            <meta name="generator" content="Jinja2" />
            <meta name="Content-URL" content=""/>
    </head>
      <body >
        <header id="header"></header>
        <div id="main" class="main">
          <nav id="navigate">
    <BLANKLINE>
    </nav>
          <div id="document" class="body">
      <input type="text" class="text" id="user_name" maxlength="30"/>
      <input type="password" class="password" id="pass_word" maxlength="40"/>
      <input type="hidden" class="text" readonly="1" id="email"/>
      <textarea cols="40" rows="4" id="Area">
        A sample text in a sample textarea.
      </textarea>
    </div>
        </div>
        <footer id="footer"></footer>
      </body>
    </html>
    >>> print tx.render (page = page)
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
    >
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" >
      <head>
      <meta http-equiv="Content-Type"
            content="text/html; charset=iso-8859-15"
          />
              <title>None</title>
    <BLANKLINE>
            <meta name="copyright" content=" " />
            <meta name="generator" content="Jinja2" />
            <meta http-equiv="Content-URL" content=""/>
    </head>
      <body >
        <div class="header" id="header"></div>
        <div id="main" class="main">
          <div class="nav" id="navigate">
    <BLANKLINE>
    </div>
          <div id="document" class="body">
      <input type="text" class="text" id="user_name" maxlength="30"/>
      <input type="password" class="password" id="pass_word" maxlength="40"/>
      <input type="hidden" class="text" readonly="1" id="email"/>
      <textarea cols="40" rows="4" id="Area">
        A sample text in a sample textarea.
      </textarea>
    </div>
        </div>
        <div class="footer" id="footer"></div>
      </body>
    </html>

"""

from _JNJ.Environment import HTML
from _TFL.Record import *

template = """\
{%- extends "html/base.jnj" %}
{%- import html_version as X -%}
{%- block document scoped %}
  {{ X.input.text (id="user_name", maxlength="30") }}
  {{ X.input.password (id="pass_word", maxlength="40") }}
  {% call X.input.hidden (id="email", readonly="1") -%}{%- endcall %}
  {% call X.input.textarea (id="Area", rows=4, cols=40) -%}
    A sample text in a sample textarea.
  {%- endcall %}
{% endblock document %}
"""
### __END__ __test__
