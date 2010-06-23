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
#    Model a URL
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
    """Model a URL as defined by RFC 3986.

        >>> Url ("http://www.ics.uci.edu/pub/ietf/uri/#Related")
        Url (authority = 'www.ics.uci.edu', fragment = 'Related', path = '/pub/ietf/uri/', query = None, scheme = 'http')
        >>> Url ("scheme://username:password@domain:port/path?foo=bar#anchor")
        Url (authority = 'username:password@domain:port', fragment = 'anchor', path = '/path', query = 'foo=bar', scheme = 'scheme')
        >>> Url ("foo://example.com:8042/over/there?name=ferret#nose")
        Url (authority = 'example.com:8042', fragment = 'nose', path = '/over/there', query = 'name=ferret', scheme = 'foo')
        >>> Url ("/tmp/foo.bar")
        Url (authority = None, fragment = None, path = '/tmp/foo.bar', query = None, scheme = None)
        >>> Url ("http://a/b/c/g;x?y#s")
        Url (authority = 'a', fragment = 's', path = '/b/c/g;x', query = 'y', scheme = 'http')
        >>> Url ("ftp://cnn.example.com&story=breaking_news@10.0.0.1/top_story.htm")
        Url (authority = 'cnn.example.com&story=breaking_news@10.0.0.1', fragment = None, path = '/top_story.htm', query = None, scheme = 'ftp')

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

    authority = property (TFL.Getter.__parsed.authority or "")
    fragment  = property (TFL.Getter.__parsed.fragment  or "")
    path      = property (TFL.Getter.__parsed.path      or "")
    query     = property (TFL.Getter.__parsed.query     or "")
    scheme    = property (TFL.Getter.__parsed.scheme    or "")
    value     = property (TFL.Getter.__value)

    def __init__ (self, value) :
        if self._matcher.match (value) :
            self.__value  = value
            self.__parsed = TFL.Record (** self._matcher.groupdict ())
        else :
            raise ValueError (value)
    # end def __init__

    def __repr__ (self) :
        return "Url " + str (self.__parsed)
    # end def __repr__

    def __str__ (self) :
        return self.__value
    # end def __str__

# end class Url

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Url
