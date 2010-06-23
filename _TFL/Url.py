# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Url
#
# Purpose
#    Model a URL and its parts
#
# Revision Dates
#    23-Jun-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL        import TFL

from   _TFL.Regexp import *

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

import _TFL.Accessor
import _TFL.Record

class Url (TFL.Meta.Object) :
    """Model a URL and its parts as defined by RFC 3986.

        >>> Url ("http://www.ics.uci.edu/pub/ietf/uri/#Related")
        Url (authority = 'www.ics.uci.edu', fragment = 'Related', path = '/pub/ietf/uri/', query = '', scheme = 'http')
        >>> Url ("scheme://username:password@domain:port/path?foo=bar#anchor")
        Url (authority = 'username:password@domain:port', fragment = 'anchor', path = '/path', query = 'foo=bar', scheme = 'scheme')
        >>> Url ("foo://example.com:8042/over/there?name=ferret#nose")
        Url (authority = 'example.com:8042', fragment = 'nose', path = '/over/there', query = 'name=ferret', scheme = 'foo')
        >>> Url ("/tmp/foo.bar")
        Url (authority = '', fragment = '', path = '/tmp/foo.bar', query = '', scheme = '')
        >>> Url ("http://a/b/c/g;x?y#s")
        Url (authority = 'a', fragment = 's', path = '/b/c/g;x', query = 'y', scheme = 'http')
        >>> Url ("ftp://cnn.example.com&story=breaking_news@10.0.0.1/top_story.htm")
        Url (authority = 'cnn.example.com&story=breaking_news@10.0.0.1', fragment = '', path = '/top_story.htm', query = '', scheme = 'ftp')

        >>> Url ("sqlite://")
        Url (authority = '', fragment = '', path = '', query = '', scheme = 'sqlite')
        >>> Url ("sqlite:///foo.db")
        Url (authority = '', fragment = '', path = '/foo.db', query = '', scheme = 'sqlite')
        >>> Url ("sqlite:////foo.db")
        Url (authority = '', fragment = '', path = '//foo.db', query = '', scheme = 'sqlite')

        >>> Url ("postgresql://scott:tiger@localhost/mydatabase")
        Url (authority = 'scott:tiger@localhost', fragment = '', path = '/mydatabase', query = '', scheme = 'postgresql')
        >>> Url ("postgresql+pg8000://scott:tiger@localhost/mydatabase")
        Url (authority = 'scott:tiger@localhost', fragment = '', path = '/mydatabase', query = '', scheme = 'postgresql+pg8000')

        >>> Url ("hps://test.foo")
        Url (authority = 'test.foo', fragment = '', path = '', query = '', scheme = 'hps')
        >>> Url ("hps:///test.foo")
        Url (authority = '', fragment = '', path = '/test.foo', query = '', scheme = 'hps')
        >>> Url ("hps://")
        Url (authority = '', fragment = '', path = '', query = '', scheme = 'hps')
        >>> Url ("hps:")
        Url (authority = '', fragment = '', path = '', query = '', scheme = 'hps')

    """

    ### Use regexp as given by http://www.ietf.org/rfc/rfc3986.txt
    ### (urlparse is broken because it doesn't parse `query` and `fragments`
    ### for unknown schemes)
    _matcher  = Regexp \
        ( r"""^(?:(?P<scheme>[^:/?#]+):)?"""
          r"""(?://(?P<authority>[^/?#]*))?"""
          r"""(?P<path>[^?#]*)"""
          r"""(?:\?(?P<query>[^#]*))?"""
          r"""(?:#(?P<fragment>.*))?"""
        )

    authority = property (TFL.Getter._parsed.authority)
    fragment  = property (TFL.Getter._parsed.fragment)
    path      = property (TFL.Getter._parsed.path)
    query     = property (TFL.Getter._parsed.query)
    scheme    = property (TFL.Getter._parsed.scheme)
    value     = property (TFL.Getter._value)

    def __init__ (self, value) :
        if self._matcher.match (value) :
            self._value  = value
            attrs        = dict \
                ( (k, v or "")
                for (k, v) in self._matcher.groupdict ().iteritems ()
                )
            self._parsed = TFL.Record (** attrs)
        else :
            raise ValueError (value)
    # end def __init__

    def __repr__ (self) :
        return "Url " + str (self._parsed)
    # end def __repr__

    def __str__ (self) :
        return self._value
    # end def __str__

# end class Url

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Url
