# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 DI Christian Eder. All rights reserved
# eder@tttech.com
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
#    TFL.Meta.M_Autoprotection
#
# Purpose
#    Provide custom metaclasses for classes using
#    access-protected attributes
#
# Revision Dates
#    20-Feb-2004 (CED, ABR) Creation
#    ««revision-date»»···
#--
#

from   _TFL             import TFL
import _TFL._Meta.M_Class
import _TFL.Caller      as Caller


class _Protected_Descriptor_ (object) :

    def __init__ (self, initval) :
        self.initval   = initval
        self._obj_dict = {}
    #end def __init__

    def __get__ (self, obj, cls) :
        self._check_get_protection (cls)
        result = self._obj_dict.get (obj, self.initval)
        if callable (result) :
            def bound (* args, ** kw) :
                return self._obj_dict.get (obj, self.initval)\
                   (obj, * args, ** kw)
            result = bound
        return result
    # end def __get__

    def __set__ (self, obj, val) :
        self._check_set_protection (obj.__class__)
        self._obj_dict [obj] = val
    # end def __set__

    def _check_set_protection (self, cls) :
        pass
    # end def _check_set_protection

    _check_get_protection = _check_set_protection

# end class _Protected_Descriptor_

class Private_Descriptor (_Protected_Descriptor_) :

    _kind = "private"

    def _check_get_protection (self, cls) :
        self._check_protection_inner (self._get_caller ())
    # end def _check_protection

    def _check_set_protection (self, cls) :
        self._check_protection_inner (self._get_caller ())
    # end def _check_set_protection

    def _check_protection_inner (self, caller_fct) :
        line = caller_fct.co_firstlineno
        file = caller_fct.co_filename
        if (   (file == self._def_cls._file)
           and (line in self._def_cls._func_object)
           ) :
            return
        raise AttributeError, \
            ( "Illegal acces to %s member %s of class %s from "
              "%s"
            % ( self._kind, self._name, self._def_cls.__name__
              , caller_fct.co_name
              )
            )
    # end def _check_protection_inner

    def _get_caller (self) :
        return Caller.code (2)
    # end def _get_caller

# end class Private_Descriptor

class Protected_Descriptor (Private_Descriptor) :

    _kind = "protected"

    def _check_protection_inner (self, (caller_obj, caller_fct)) :
        if caller_obj and self._def_cls in caller_obj.__class__.__mro__ :
            return
        raise AttributeError, \
            ( "Illegal acces to %s member %s of class %s from "
              "%s"
            % ( self._kind, self._name, self._def_cls.__name__
              , caller_fct.co_name
              )
            )
    # end def _check_protection_inner

    def _get_caller (self) :
        return Caller.locals (2).get ("self", None), Caller.code (2)
    # end def _get_caller

# end class Protected_Descriptor

class M_Autoprotection (TFL.Meta.M_Class) :
    """Custom metaclasses for classes using access-protected attributes"""

    def __init__ (cls, name, bases, dict) :
        super   (M_Autoprotection, cls).__init__ (name, bases, dict)
        cls._setup_class_protections (name, dict)
    # end def __init__

    def _setup_class_protections (cls, name, dict) :
        cls._func_object= {}
        for n, v in dict.items () :
            if callable (v) and n != "__metaclass__" :
                cls._func_object [v.func_code.co_firstlineno] = True
                cls._file = v.func_code.co_filename
            if v.__class__ is Private_Descriptor :
                v._def_cls = cls
                v._name    = n
            elif v.__class__ is Protected_Descriptor :
                v._def_cls = cls
                v._name    = n
    # end def _setup_class_protections

# end class M_Autoprotection

if __name__ != "__main__" :
    TFL.Meta._Export ("*")

### __END__ M_Autoprotection


