# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.RST.MOM.Mixin
#
# Purpose
#    Define mixin classes for GTW.RST.MOM
#
# Revision Dates
#    22-Jun-2012 (CT) Creation
#     3-Jul-2012 (CT) Factored from _GTW/_RST/MOM.py
#     3-Jul-2012 (CT) Add support for `Query_Restriction`
#     5-Jul-2012 (CT) Add support for nested entities to `_PUT_POST_Mixin_`
#                     * factor `_resolve_request_attrs`
#                     * add and use `_resolve_nested_request_attrs`
#    17-Jul-2012 (CT) Factor `_changed_cid`
#    17-Jul-2012 (CT) Include `_change_info` in `_handle_method_context`
#    18-Jul-2012 (CT) Use `scope.pid_query`, not `ETM.pid_query`, in
#                     `_get_child_query` (don't want `Gone` for type mismatch)
#    19-Jul-2012 (CT) Add `RST_Entity_Mixin`: factored from `GTW.RST.MOM.Entity`
#    19-Jul-2012 (CT) Change `RST_E_Type_Mixin._get_child` to call
#                     `__super._get_child` before, not after, `_get_child_query`
#    19-Jul-2012 (CT) Turn `_change_info` into property, use `top._change_infos`
#    20-Jul-2012 (CT) Factor `pid_query_request`
#    23-Jul-2012 (CT) Add argument `response` to `_handle_method_context`
#    31-Jul-2012 (CT) Use `formatted_1`, not `repr`, in `_resolve_request_attrs`
#     2-Aug-2012 (CT) Use `id_entity_attr` in
#                     `RST_Entity_Mixin.change_query_filters`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST.HTTP_Method
import _GTW._RST._MOM.Query_Restriction

from   _MOM.import_MOM          import MOM, Q

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Formatter           import formatted_1
from   _TFL.I18N                import _, _T, _Tn

import _TFL._Meta.Object

class _PUT_POST_Mixin_ (GTW.RST.HTTP_Method) :

    failure_code = 400 ### Bad request

    def _request_attrs (self, resource, request, response) :
        try :
            result = request.json ["attributes"]
        except KeyError :
            raise ValueError \
                ("""You need to send the attributes defining """
                 """the object with the request """
                 """(content-type "application/json")"""
                )
        else :
            self._resolve_request_attrs \
                (resource, request, response, resource.E_Type, result)
        return result
    # end def _request_attrs

    def _resolve_nested_request_attrs \
            (self, resource, request, response, E_Type, attrs) :
        ieas  = E_Type.id_entity_attr
        scope = resource.scope
        for iea in ieas :
            k = iea.name
            if k in attrs :
                etn = iea.E_Type.type_name
                ETM = scope [etn]
                v   = attrs [k]
                if isinstance (v, dict) :         ### attribute dictionary
                    self._resolve_request_attrs \
                        (resource, request, response, iea.E_Type, v)
                    v = ETM.instance_or_new (raw = True, ** v)
                elif isinstance (v, int) :        ### pid
                    v = scope.pid_query (v)
                elif isinstance (v, basestring) : ### single epk argument
                    v = ETM.instance_or_new (v, raw = True)
                elif isinstance (v, list) :       ### list of epk arguments
                    v = ETM.instance_or_new (* v, raw = True)
                else :
                    raise ValueError \
                        ("Invalid value %r for %s" % (v, etn))
                attrs [k] = v
    # end def _resolve_nested_request_attrs

    def _resolve_request_attrs \
            (self, resource, request, response, E_Type, attrs) :
        allowed  = set   (a.name for a in E_Type.edit_attr)
        invalids = tuple (k for k in attrs if k not in allowed)
        if invalids :
            raise ValueError \
                ( "Request contains invalid attribute names "
                + formatted_1 (invalids)
                )
        self._resolve_nested_request_attrs \
            (resource, request, response, E_Type, attrs)
    # end def _resolve_request_attrs

    def _response_body (self, resource, request, response) :
        try :
            attrs = self._request_attrs (resource, request, response)
            obj   = self._apply_attrs   (resource, request, response, attrs)
        except Exception as exc :
            resource.scope.rollback ()
            response.status_code = self.failure_code
            result               = dict (error = str (exc))
        else :
            resource.scope.commit ()
            response.status_code = self.success_code
            e      = resource._new_entry (obj.pid)
            result = e.GET ()._response_body (e, request, response)
        return result
    # end def _response_body

# end class _PUT_POST_Mixin_

class RST_Mixin (TFL.Meta.Object) :
    """Mixin for MOM-specific RST classes."""

    objects                    = property (lambda s : s._get_objects ())

    _attributes                = None
    _exclude_robots            = True
    _objects                   = []
    _old_cid                   = -1
    _sort_key_cid_reverse      = TFL.Sorted_By ("-cid")

    @Once_Property
    def E_Type (self) :
        ETM = self._ETM
        if isinstance (ETM, basestring) :
            result = self.top.App_Type [ETM]
        else :
            result = ETM.E_Type
        return result
    # end def E_Type

    @Once_Property
    def ETM (self) :
        result = self._ETM
        if isinstance (result, basestring) :
            result = self.top.scope [result]
        return result
    # end def ETM

    @property
    def attributes (self) :
        result = self._attributes
        if result is None :
            result = self._attributes = self.E_Type.edit_attr
        return result
    # end def attributes

    @attributes.setter
    def attributes (self, value) :
        def _gen (vs) :
            AQ = self.E_Type.AQ
            for v in vs :
                if isinstance (v, basestring) :
                    try :
                        v = getattr (AQ, v)._attr
                    except AttributeError as exc :
                        print ("*" * 4, exc, E_Type, v)
                        pass
                    else :
                        yield v
        self._attributes = tuple (_gen (value)) if value is not None else None
    # end def attributes

    @property
    def change_info (self) :
        result = self._change_info
        if result is None :
            result = self._change_info = self._get_change_info ()
        return result
    # end def change_info

    @Once_Property
    def type_name (self) :
        return self.E_Type.type_name
    # end def type_name

    @property
    def _change_info (self) :
        return self.top._change_infos.get (self.href)
    # end def _change_info

    @_change_info.setter
    def _change_info (self, value) :
        self.top._change_infos [self.href] = value
    # end def _change_info

    def pid_query_request (self, pid, E_Type = None, raise_not_found = True) :
        if E_Type is None :
            E_Type = self.E_Type
        scope  = self.top.scope
        Status = self.Status
        try :
            ipid = int (pid)
        except (ValueError, TypeError) :
            pass
        else :
            try :
                result = scope.pid_query (ipid)
            except LookupError as exc :
                if 0 < ipid <= scope.max_pid :
                    error = \
                        (  _T ("%s `%s` doesn't exist anymore!")
                        % (_T (E_Type.ui_name), pid)
                        )
                    raise Status.Gone
            else :
                if isinstance (result, E_Type) :
                    return result
                elif raise_not_found :
                    error = \
                        (  _T ("`%s` refers to %s, not %s")
                        % (pid, _T (result.E_Type.ui_name), _T (E_Type.ui_name))
                        )
                    raise Status.Bad_Request (error)
        if raise_not_found :
            error = (_T ("%s `%s` doesn't exist!") % (_T (E_Type.ui_name), pid))
            raise Status.Not_Found (error)
    # end def pid_query_request

    def query_changes (self) :
        scope = self.top.scope
        cqfs  = self.change_query_filters
        if cqfs is not None :
            return scope.query_changes \
                (* cqfs).order_by (self._sort_key_cid_reverse)
    # end def query_changes

    def _changed_cid (self) :
        change_info = self.change_info
        cid         = change_info and change_info.cid
        if self._old_cid != cid :
            return cid
    # end def _changed_cid

    def _get_change_info (self) :
        result = None
        qc     = self.query_changes ()
        if qc is not None :
            lc = qc.first ()
            if lc is not None :
                result = TFL.Record \
                    ( cid           = lc.cid
                    , etag          = "ET-%s-%s" % (lc.time, lc.cid)
                    , last_modified = lc.time.replace (microsecond = 0)
                    )
        return result
    # end def _get_change_info

    def _get_objects (self) :
        cid = self._changed_cid ()
        if cid is not None :
            self._old_cid = cid
            self._objects = self.query ().all ()
        return self._objects
    # end def _get_objects

    @TFL.Contextmanager
    def _handle_method_context (self, method, request, response) :
        with self.__super._handle_method_context (method, request, response) :
            with self.LET (_change_info = self._get_change_info ()) :
                yield
    # end def _prepare_handle_method

# end class RST_Mixin

class RST_Entity_Mixin (RST_Mixin) :
    """Mixin for classes of handling E_Type instances."""

    @Once_Property
    def change_query_filters (self) :
        result = ()
        obj    = self.obj
        if obj :
            result = (Q.pid == obj.pid, )
            E_Type = obj.__class__
            if E_Type.id_entity_attr :
                def _gen (self, E_Type) :
                    yield obj.pid
                    for iea in E_Type.id_entity_attr :
                        v = iea.get_value (obj)
                        if v and v.pid :
                            yield v.pid
                pids = tuple (_gen (self, E_Type))
                if len (pids) > 1 :
                    result = (Q.pid.IN (pids), )
        return result
    # end def change_query_filters

# end class RST_Entity_Mixin

class RST_E_Type_Mixin (RST_Mixin) :
    """Mixin for classes of handling E_Types."""

    QR                         = GTW.RST.MOM.Query_Restriction

    default_qr_kw              = dict ()
    query_restriction          = None
    sort_key                   = None

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "ETM", prefix = "_")
        if "name" not in kw :
            kw ["name"] = self.type_name.replace (".", "-")
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def count (self) :
        if self.query_filters :
            result = self.query ().count ()
        else :
            result = self.ETM.count
        return result
    # end def count

    @Once_Property
    def change_query_filters (self) :
        result = ()
        E_Type = self.E_Type
        if E_Type.is_partial :
            if E_Type.type_name != "MOM.Id_Entity" :
                result = (Q.type_name.IN (sorted (E_Type.children_np)), )
        else :
            result = (Q.type_name == E_Type.type_name, )
        return result
    # end def change_query_filters

    @Once_Property
    def query_filters (self) :
        return tuple ()
    # end def query_filters

    def query (self, sort_key = None) :
        result = self.ETM.query \
            (* self.query_filters, sort_key = sort_key or self.sort_key)
        if self.query_restriction is not None :
            result = self.query_restriction (result)
        return result
    # end def query

    def _get_child (self, child, * grandchildren) :
        self.objects ### trigger recomputation/load-from-db, if necessary
        result = self.__super._get_child (child, * grandchildren)
        if result is None :
            obj = self._get_child_query (child)
            if obj is not None :
                result = self._new_entry (obj)
                if grandchildren :
                    result = result._get_child (* grandchildren)
                return result
        return result
    # end def _get_child

    def _get_child_query (self, child) :
        return self.pid_query_request (child, raise_not_found = False)
    # end def _get_child_query

    def _get_objects (self) :
        _old_objects = self._objects
        result       = self.__super._get_objects ()
        if result is not _old_objects :
            ### invalidate `_entry_map`, `_entries`
            self._entry_map = {}
            self._entries   = []
        return result
    # end def _get_objects

    @TFL.Contextmanager
    def _handle_method_context (self, method, request, response) :
        with self.__super._handle_method_context (method, request, response) :
            qr = self.QR.from_request \
                (self.E_Type, request, ** self.default_qr_kw)
            kw = dict (query_restriction = qr)
            if qr.attributes :
                kw ["attributes"] = qr.attributes
            if qr :
                ### temporarily invalidate cached information to trigger
                ### reload with `query_restriction`
                ### old caches will be restored after `_handle_method` completes
                kw.update \
                    ( _change_info = None
                    , _entries     = []
                    , _entry_map   = {}
                    , _objects     = []
                    , _old_cid     = object ()
                    )
            with self.LET (** kw) :
                yield
    # end def _prepare_handle_method

    def _new_entry (self, instance, ** kw) :
        return self.Entity (obj = instance, parent = self, ** kw)
    # end def _new_entry

# end class RST_E_Type_Mixin

if __name__ != "__main__" :
    GTW.RST.MOM._Export ("*", "_PUT_POST_Mixin_")
### __END__ GTW.RST.MOM.Mixin
