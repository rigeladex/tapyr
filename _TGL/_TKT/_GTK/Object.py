# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TGL.TKT.GTK.Object
#
# Purpose
#    Root class for all GTK related objects and widgets
#
# Revision Dates
#    21-Mar-2005 (MG) Creation
#    25-Mar-2005 (CT) Moved to TGL
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
import _TGL._TKT
import _TGL._TKT.Mixin
import _TGL._TKT._GTK
import _TFL._Meta.M_Class
import _TFL._Meta.M_Auto_Combine_Dicts

import  pygtk
pygtk.require ("2.0")
import gtk
import gobject
import weakref

class Property (property) :
    """Models a simple gtk property using the default `set_property` and
       `get_property` methods
    ."""

    __metaclass__ = TFL.Meta.M_Autosuper

    def __init__ (self
                 , name
                 , get      = True
                 , set      = True
                 , doc      = None
                 , gtk_name = None
                 ) :
        """Use `None` for `get` or `set` if no set or get function should be
           registered.
        """
        self.name = name
        gtk_name  = gtk_name or name
        if get is True :
            get = lambda s    : s.wtk_object.get_property (gtk_name)
        if set is True :
            set = lambda s, v : s.wtk_object.set_property (gtk_name, v)
        self.__super.__init__  (get, set, doc = doc)
    # end def __init__

# end class Property

class SG_Property (property) :
    """Models a simple gtk property using custom set/get functions."""

    __metaclass__ = TFL.Meta.M_Autosuper

    def __init__ (self
                 , name
                 , get          = True
                 , set          = True
                 , get_fct_name = None
                 , set_fct_name = None
                 , doc          = None
                 , gtk_name     = None
                 ) :
        """Use `None` for `get` or `set` if no set or get function should be
           registered.
        """
        self.name = name
        gtk_name  = gtk_name or name
        if get is True :
            get = self._default_get (get_fct_name or "get_" + gtk_name)
        if set is True :
            set = self._default_set (set_fct_name or "set_" + gtk_name)
        self.__super.__init__       (get, set, doc = doc)
    # end def __init__

    def _default_set (self, name) :
        return lambda s, v : getattr (s.wtk_object, name) (v)
    # end def _default_set

    def _default_get (self, name) :
        return lambda s : getattr (s.wtk_object, name) ()
    # end def _default_get

# end class SG_Property

class List_Property (Property) :
    """Models a property which requires a list as parameter for the `set`
       function.
    """

    def _default_set (self, name) :
        return lambda s, v : getattr (s.wtk_object, name) (* v)
    # end def _default_set

# end class List_Property

def Signal_Spec ( sig_type       = gobject.SIGNAL_RUN_LAST
                , sig_return     = gobject.TYPE_BOOLEAN
                , sig_parameters = ()
                ) :
    return (sig_type, sig_return, sig_parameters)
# end def Signal_Spec

class _M_Object_ (TFL.Meta.M_Auto_Combine_Dicts, TFL.Meta.M_Class) :
    """Metaclass which generates the new GTK types if a `Class_Name` is
       specified. Additionally, this metaclass will create properties for all
       objects of the `__gtk_properties` sequence.
    """

    GTK_Classes       = {}
    _dicts_to_combine = ("_wtk_delegation", )

    def __new__ (cls, name, bases, dict) :
        Class_Name = dict.get ("Class_Name", None)
        if Class_Name and Class_Name not in cls.GTK_Classes :
            gtk_base  = gtk_class = dict ["GTK_Class"]
            gtk_base  = cls.GTK_Classes.get (gtk_base, gtk_base)
            d         = {"__gsignals__" : dict.get ("Signals", {})}
            gtk_class = type      (Class_Name, (gtk_base, ), d)
            gobject.type_register (gtk_class)
            cls.GTK_Classes [Class_Name] = dict ["GTK_Class"] = gtk_class
        return super (_M_Object_, cls).__new__ (cls, name, bases, dict)
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        super (_M_Object_, cls).__init__ (name, bases, dict)
        for p in getattr \
                (cls, cls._m_mangled_attr_name ("gtk_properties"), ()) :
            setattr (cls, p.name, p)
    # end def __init__

# end class _M_Object_

class Object (TGL.TKT.Mixin) :
    """Root class for all GTK related objects (TextBuffer, TreeModel, ...)
       and Widgets (TextView, TreeView, ...)

       >>> class Dummy (Object) :
       ...     Class_Name = "Hansi"
       ...     GTK_Class  = gtk.HBox
       ...
       >>> Dummy.GTK_Class
       <class 'Object.Hansi'>
    """

    __metaclass__    = _M_Object_
    __gtk_properties = ()
    _wtk_delegation  = {}

    ### `Class_Name` is the name of the new generated GTK-type
    ### `Signals`    is a dictionary describing the signals of the new GTK-type
    GTK_Class        = gtk.Object

    def __init__ (self, * args, ** kw) :
        AC = None
        if "AC" in kw :
            AC = kw ["AC"]
            del kw ["AC"]
        self.__super.__init__ (AC = AC)
        self.wtk_object = self.GTK_Class (* args, ** kw)
        ### set the backref directly in the C-gtk object and not in the
        ### python wrapper !
        self.wtk_object.set_data ("ktw_object", weakref.proxy (self))
    # end def __init__

    def __getattr__ (self, name) :
        if name in self._wtk_delegation :
            result = getattr (self.wtk_object, self._wtk_delegation [name])
            setattr (self, name, result)
            return result
        raise AttributeError, name
    # end def __getattr__

# end class Object

main = gtk.main
quit = gtk.main_quit

if __name__ != "__main__" :
    TGL.TKT.GTK._Export ("*", "gtk", "main", "quit")
### __END__ TGL.TKT.GTK.Object
