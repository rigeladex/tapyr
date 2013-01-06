# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.MOM.Client
#
# Purpose
#    Generic client for a RESTful Api as implemented by GTW.RST.MOM
#
# Revision Dates
#     6-Jan-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST._MOM

from   _TFL._Meta.Once_Property import Once_Property
import _TFL._Meta.Object
from   _TFL.Decorator           import getattr_safe
from   _TFL.predicate           import callable

from   posixpath                import join as pp_join

import json
import requests

class _Entity_ (TFL.Meta.Object) :
    """Base class for Object and Resource"""

    def __init__ (self, requester, result) :
        self._requester = requester
        self._result    = result
    # end def __init__

    @TFL.Meta.Once_Property
    @getattr_safe
    def _ad_name (self) :
        return "attributes_raw" if self._requester.raw else "attributes"
    # end def _ad_name

    @TFL.Meta.Once_Property
    @getattr_safe
    def _attrs (self) :
        json = self._json
        if json :
            return dict (json.get (self._ad_name) or {})
    # end def _attrs

    @TFL.Meta.Once_Property
    @getattr_safe
    def _attrs_orig (self) :
        json = self._json
        if json :
            return json.get (self._ad_name, {})
    # end def _attrs_orig

    @property
    @getattr_safe
    def _changed_p (self) :
        return self._attrs != self._attrs_orig
    # end def _changed_p

    @TFL.Meta.Once_Property
    @getattr_safe
    def _entries (self) :
        json = self._json
        if json :
            entries = json.get ("entries", [])
            if entries :
                def gen (requester, entries) :
                    for e in entries :
                        if isinstance (e, dict) :
                            yield self._wrap_dict (requester, e)
                        else :
                            yield requester.get (e)
                return list (gen (self._requester, entries))
    # end def _entries

    def PUT (self) :
        if self._changed_p :
            cargo = json.dumps \
                ( { self._ad_name : self._attrs
                  , "cid"         : self._json ["cid"]
                  }
                )
            return self._requester.put (self._url, data = cargo)
    # end def PUT

    def _wrap_dict (self, requester, result) :
        if self._ad_name in result :
            result = requester.Object (requester, result)
        else :
            result = requester.get \
                (result ["url"], params = dict (closure = True))
        return result
    # end def _wrap_dict

    def __getattr__ (self, name) :
        attrs = self._attrs
        if attrs and name in attrs :
            result = attrs [name]
            if isinstance (result, dict) :
                result = self._wrap_dict (self._requester, result)
            setattr (self, name, result)
            return result
        raise AttributeError (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        entries = self._entries
        if entries :
            return entries [key]
    # end def __getitem__

    def __iter__ (self) :
        entries = self._entries
        if entries :
            return iter (entries)
    # end def __iter__

    def __nonzero__ (self) :
        return bool (self._result)
    # end def __nonzero__

    def __setattr__ (self, name, value) :
        if name.startswith ("_") :
            self.__super.__setattr__ (name, value)
        else :
            attrs = self._attrs
            if attrs is not None :
                attrs [name] = value
            else :
                raise TypeError (name)
    # end def __setattr__

# end class _Entity_

class Object (_Entity_) :
    """Encapsulate a nested object"""

    @TFL.Meta.Once_Property
    @getattr_safe
    def _json (self) :
        return self._result
    # end def _json

    @TFL.Meta.Once_Property
    @getattr_safe
    def _url (self) :
        return self._result.get ("url")
    # end def _url

# end class Object

class Resource (_Entity_) :
    """Encapsulate a RESTful resource"""

    @TFL.Meta.Once_Property
    @getattr_safe
    def _json (self) :
        result = self._result.json
        if callable (result) :
            result = result ()
        return result
    # end def _json

    @TFL.Meta.Once_Property
    @getattr_safe
    def _url (self) :
        json = self._json
        try :
            return json ["url"]
        except KeyError :
            return self._result.url
    # end def _url

# end class Resource

class Requester (TFL.Meta.Object) :
    """Wrapper for `requests`"""

    Object   = Object
    Resource = Resource

    class Wrapper (TFL.Meta.Object) :

        def __init__ (self, name, requester) :
            self.method    = getattr (requester.session, name)
            self.requester = requester
        # end def __init__

        def __call__ (self, path, * args , ** kw) :
            requester = self.requester
            url       = pp_join (requester.prefix, path.lstrip ("/"))
            return requester.Resource \
                (requester, self.method (url, * args, ** kw))
        # end def __call__

    # end class W

    def __init__ (self, prefix, raw = False, ** kw) :
        params = kw.pop ("params", {})
        if raw :
            params.update (raw = True)
        self.prefix  = prefix
        self.raw     = raw
        self.session = s = requests.Session ()
        if params :
            s.params.update (params)
        for k, v in kw.iteritems () :
            setattr (s, k, v)
        s.headers.update ({ "Content-Type" : "application/json" })
    # end def __init__

    def __getattr__ (self, name) :
        return self.Wrapper (name, self)
    # end def __getattr__

# end class Requester

if __name__ != "__main__" :
    GTW.RST.MOM._Export_Module ()
### __END__ GTW.RST.MOM.Client
