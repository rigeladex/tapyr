# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package JNJ.
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
    >>> glbs = dict (page = page, next = "/logout/")
    >>> env5 = HTML (globals = glbs)
    >>> envx = HTML (version = "html/x.jnj", globals = glbs)
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
      <input type="text" placeholder="Please enter your user-name" id="user_name" maxlength="30"/>
      <input type="password" id="pass_word" maxlength="40"/>
      <input type="email" readonly="1" id="email"/>
      <input type="number" max="8" min="2"/>
      <textarea cols="40" rows="4" id="Area">
        A sample text in a sample textarea.
    <BLANKLINE>
      </textarea>
    <BLANKLINE>
      <form action="/login/" method="post">
        <ul>
          <li><label for="F_username">Username</label></li>
          <li>
            <input type="text" placeholder="Please enter your user-name" id="F_username" maxlength="30"/>
          </li>
          <li><label for="F_password">Password</label></li>
          <li>
            <input type="password" placeholder="Please enter your password" id="F_password"/>
          </li>
          <li>
            <input type="submit" value="Login"/>
            <input type="hidden" name="next" value="/logout/"/>
          </li>
        </ul>
      </form>
    <BLANKLINE>
      <form action="/login/" method="post">
    <BLANKLINE>
          Using `call` of `GTW.get_macro`
    <BLANKLINE>
        <ul>
          <li><label for="F_username">Username</label></li>
          <li>
            <input type="text" placeholder="Please enter your user-name" id="F_username" maxlength="30"/>
          </li>
          <li><label for="F_password">Password</label></li>
          <li>
            <input type="password" placeholder="Please enter your password" id="F_password"/>
          </li>
          <li>
            <input type="submit" value="Login"/>
            <input type="hidden" name="next" value="/logout/"/>
          </li>
        </ul>
      </form>
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
        <div class="header " id="header"></div>
        <div id="main" class="main">
          <div class="nav " id="navigate">
    <BLANKLINE>
    </div>
          <div id="document" class="body">
      <input type="text" class="text" id="user_name" maxlength="30"/>
      <input type="password" class="password" id="pass_word" maxlength="40"/>
      <input type="text" class="email" readonly="1" id="email"/>
      <input type="text" class="number"/>
      <textarea cols="40" rows="4" id="Area">
        A sample text in a sample textarea.
    <BLANKLINE>
      </textarea>
    <BLANKLINE>
      <form action="/login/" method="post">
        <ul>
          <li><label for="F_username">Username</label></li>
          <li>
            <input type="text" class="text" id="F_username" maxlength="30"/>
          </li>
          <li><label for="F_password">Password</label></li>
          <li>
            <input type="password" class="password" id="F_password"/>
          </li>
          <li>
            <input type="submit" class="submit" value="Login"/>
            <input type="hidden" class="text" name="next" value="/logout/"/>
          </li>
        </ul>
      </form>
    <BLANKLINE>
      <form action="/login/" method="post">
    <BLANKLINE>
          Using `call` of `GTW.get_macro`
    <BLANKLINE>
        <ul>
          <li><label for="F_username">Username</label></li>
          <li>
            <input type="text" class="text" id="F_username" maxlength="30"/>
          </li>
          <li><label for="F_password">Password</label></li>
          <li>
            <input type="password" class="password" id="F_password"/>
          </li>
          <li>
            <input type="submit" class="submit" value="Login"/>
            <input type="hidden" class="text" name="next" value="/logout/"/>
          </li>
        </ul>
      </form>
    </div>
        </div>
        <div class="footer " id="footer"></div>
      </body>
    </html>

"""

from   _JNJ.Environment import HTML
from   _TFL.Record import *
import _TFL.I18N

template = """\
{%- extends "html/base.jnj" %}
{%- import html_version as X -%}
{%- import "html/form.jnj" as form -%}

{%- macro _render (typ) -%}
  {{- typ (** kwargs) -}}
{%- endmacro -%} {#- _render -#}

{%- block document scoped %}
  {{ _render (typ = X.input.text, id="user_name", maxlength="30", placeholder="Please enter your user-name") }}
  {{ X.input.password (id="pass_word", maxlength="40") }}
  {% call X.input.email (id="email", readonly="1") -%}{%- endcall %}
  {{ X.input.number (min = 2, max = 8) }}
  {% call X.input.textarea (id="Area", rows=4, cols=40) -%}
    A sample text in a sample textarea.
  {% endcall %}
  {{ GTW.call_macro ("html/form.jnj, login") }}
  {% call GTW.get_macro ("html/form.jnj, login") () -%}
    Using `call` of `GTW.get_macro`
  {% endcall %} {# GTW.get_macro #}
{% endblock document %}
"""
### __END__ __test__
