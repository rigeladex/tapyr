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
#    26-Mar-2005 (MG) `num_opt_val` and `option_value` added
#    26-Mar-2005 (MG) `*bind*` functions added
#    27-Mar-2005 (MG) `SG_Object_*Property` added
#    27-Mar-2005 (MG) `FP_Object_Extract` added and `__getattr__` changed to
#                     support method wrappers
#     1-Apr-2005 (MG) `_wtk_delegation` handling changed
#     2-Apr-2005 (MG) Style handling added
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
import _TGL._TKT
import _TGL._TKT.Mixin
import _TGL._TKT._GTK
import _TFL._Meta.Object
import _TFL._Meta.M_Class
import _TFL._Meta.M_Auto_Combine_Dicts
import _TGL._TKT._GTK.Eventname

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

class SG_Object_Property (SG_Property) :
    """Models a property with sets/returns a GTK object."""

    def _default_set (self, name) :
        return lambda s, v : getattr (s.wtk_object, name) (v and v.wtk_object)
    # end def _default_set

    def _default_get (self, name) :
        return lambda s : self.widget (getattr (s.wtk_object, name) ())
    # end def _default_get

    def widget (self, widget) :
        return widget and (widget.get_data ("ktw_object") or widget)
    # end def widget

# end class SG_Object_Property

class SG_Object_List_Property (SG_Object_Property) :
    """Models a property with sets/returns a GTK object."""

    def _default_set (self, name) :
        return lambda s, v : \
            getattr (s.wtk_object, name) ([w.wtk_object for w in v])
    # end def _default_set

    def widget (self, values) :
        return [w and (w.get_data ("ktw_object") or w) for w in values]
    # end def widget

# end class SG_Object_List_Property

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

class Delegator (TFL.Meta.Object) :
    """Simple function delegator"""

    def __init__ (self, name) :
        self.name = name
    # end def __init__

    def __call__ (self, this,  * args, ** kw) :
        return getattr (this.wtk_object, self.name) (* args, ** kw)
    # end def __call__

# end class Delegator

class Delegator_O (Delegator) :
    """Delegator for a function of the `wtk_object` and extract the
       `wtk_object` from the first parameter
    """

    def __call__ (self, this, obj, * args, ** kw) :
        return self.__super.__call__ (this, obj.wtk_object, * args, ** kw)
    # end def __call__

# end class Delegator_O

def Delegation (* args, ** kw) :
    for arg in args :
        kw [arg.name] = arg
    return kw
# end def Delegation

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
    _sty_map         = {}

    ### `Class_Name` is the name of the new generated GTK-type
    ### `Signals`    is a dictionary describing the signals of the new GTK-type
    GTK_Class        = gtk.Object

    def __init__ (self, * args, ** kw) :
        AC = None
        if "AC" in kw :
            AC = kw ["AC"]
            del kw  ["AC"]
        self.__super.__init__ (AC = AC)
        self.wtk_object    = self.GTK_Class (* args, ** kw)
        self._handlers     = {} ### holds all connected callback functions
        ### set the backref directly in the C-gtk object and not in the
        ### python wrapper !
        self.wtk_object.set_data ("ktw_object", weakref.proxy (self))
        self._sty_stack = []
    # end def __init__

    def _bind_single_ (self, signal, connect, func, args, kw) :
        for cid in self._handlers.get (signal, ()) :
            signal.disconnect (self.wtk_object, id)
            self._handlers [signal] = []
        return self._bind_ (signal, connect, func, args, kw)
    # end def _bind_single_

    def _bind_ (self, signal, connect_name, func, args, kw) :
        cid = getattr (signal, connect_name) (self.wtk_object, func, args, kw)
        self._handlers.setdefault (signal, []).append (cid)
        return cid
    # end def _bind_

    def bind_replace (self, signal, func, * args, ** kw) :
        return self._bind_single_ (signal, "connect", func, args, kw)
    # end def bindDelegator

    def bind_after_replace (self, signal, func, * args, ** kw) :
        return self._bind_single_ (signal, "connect_after", func, args, kw)
    # end def bind_after

    def bind_add (self, signal, func, * args, ** kw) :
        """Connect TGW or GTK signal to `func`. `signal` is a string for
           GTK-signals, or a `TGW.Signal` object for TGW-signals.
        """
        return self._bind_ (signal, "connect", func, args, kw)
    # end def bind_add

    def bind_after_add (self, signal, func, * args, ** kw) :
        """Connect TGW or GTK signal to `func`. `signal` is a string for
           GTK-signals, or a `TGW.Signal` object for TGW-signals.
        """
        return self._bind_ (signal, "connect_after", func, args, kw)
    # end def bind_after_add

    def unbind (self, signal, cid) :
        self._handlers [signal].remove (cid)
        return signal.disconnect (self.wtk_object, cid)
    # end def unbind

    def emit (self, signal, * args) :
        return signal.emit (self.wtk_object, * args)
    # end def emit

    ### style API
    def _set_style (self, v) :
        return self.__setattr__ (* v)
    # end def _set_style

    def apply_style (self, style, * args, ** kw) :
        map (self._set_style, self._styler (style).option_dict.iteritems())
        self._apply_style_bindings   (style)
    # end def apply_style

    def pop_style (self) :
        map (self._set_style, self._sty_stack.pop ().iteritems ())
    # end def pop_style

    def push_style (self, style) :
        assert style.callback is None
        styler = self._styler  (style)
        self._sty_stack.append (self._before_styler (styler))
        map (self._set_style, styler.option_dict.iteritems ())
    # end def push_style

    def _apply_style_bindings (self, style, binder = None) :
        if style is not None and style.callback :
            if binder is None :
                binder = self.bind_add
            for name, cb in style.callback.iteritems () :
                binder (getattr (self.TNS.Eventname, name), cb)
    # end def _apply_style_bindings

    def _before_styler (self, styler) :
        return dict \
            ([(p, getatt (self, p)) for p in styler.option_dict.iterkeys ()])
    # end def _before_styler

    def _styler (self, style, Styler = None) :
        sty_map = self._sty_map
        if Styler is None :
            Styler = self.Styler
        if Styler not in sty_map :
            sty_map [Styler] = weakref.WeakKeyDictionary ()
        sty_map = sty_map [Styler]
        if style not in sty_map :
            sty_map [style] = Styler (style)
        return sty_map [style]
    # end def _styler

    ### XXX implement me, please !!!
    def num_opt_val (self, name, default) :
        return default
    # end def num_opt_val

    ### XXX implement me, please !!!
    def option_value (self, name, default, separator = None) :
        return default
    # end def option_value

    ##XXX # replace me using meta class trickery
    def __getattr__ (self, name) :
        if name in self._wtk_delegation :
            result = \
                (  lambda * args, ** kw
                : self._wtk_delegation [name] (self, * args, ** kw)
                )
            result.__name__ = name
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
