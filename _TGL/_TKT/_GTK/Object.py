# -*- coding: utf-8 -*-
# Copyright (C) 2005-2008 Martin Glück. All rights reserved
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
#     2-Apr-2005 (MG) `_styler`: caching removed (in now done by the `Styler`)
#     3-Apr-2005 (MG) `_before_styler` corrected
#    15-May-2005 (MG) `Delegator_2O` added
#    16-May-2005 (MG) Support for the defintion of new GTK properties added
#    18-May-2005 (MG) `Delegator_EO` added
#    20-May-2005 (MG) `weakref` attribute added
#    20-May-2005 (MG) Widget memory support added
#    20-May-2005 (MG) `idle_add`, `idle_remove`, and `update_idletasks` added
#     5-Jun-2005 (MG) `_Object_` factored, `Object_Wrapper` added
#    17-Jun-2005 (MG) `String_Property` and `Object_Property` added
#    17-Jun-2005 (MG) `_get_property` chabged to return `None` as default
#    28-Jul-2005 (MG) `path` and `std_pathes` moved in here (from
#                     `Image_Manager`)
#    28-Jul-2005 (MG) `read_style_file` added
#     5-Sep-2005 (MG) `read_widget_memory` guard added
#    13-Sep-2005 (MG) Support for pygtk 2.8 added
#    21-Jan-2006 (MG) Imports fixed
#    22-Jan-2006 (MG) `Object`: optional parameter `wtk_object` added
#    29-Aug-2008 (CT) s/super(...)/__m_super/
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
import _TFL.Environment
import _TFL.Filename
import  sys
import _TFL.sos as sos

# this does not work with py2exe
#import  pygtk
#pygtk.require ("2.0")
import gtk
import gobject
import weakref

class Property (property) :
    """Models a simple gtk property using the default `set_property` and
       `get_property` methods.
    """

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

class List_Property (SG_Property) :
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

min_max_values = dict \
   ( [ (k, (-2**x, 2**x - 1))
           for (k, x) in ( (gobject.TYPE_CHAR,   7)
                         , (gobject.TYPE_INT,   15)
                         , (gobject.TYPE_LONG,  31)
                         , (gobject.TYPE_INT64, 63)
                         )
     ] +
     [ (k, (0, 2**x - 1))
           for (k, x) in ( (gobject.TYPE_UCHAR,   8)
                         , (gobject.TYPE_UINT,   16)
                         , (gobject.TYPE_ULONG,  32)
                         , (gobject.TYPE_UINT64, 64)
                         )
     ]
   )

def Number_Property ( p_type
                    , default     = 0
                    , kind        = gobject.PARAM_READWRITE
                    , nick        = ""
                    , description = ""
                    , min_value   = None
                    , max_value   = None) :
    min_d, max_d = min_max_values.get (p_type)
    if min_value is None : min_value = min_d
    if max_value is None : max_value = max_d
    return \
        ( p_type, nick, description, min_value, max_value, default, kind)
# end def Number_Property

def String_Property ( default     = ""
                    , kind        = gobject.PARAM_READWRITE
                    , nick        = ""
                    , description = ""
                    ) :
    return (gobject.TYPE_STRING, nick, description, default, kind)
# end def String_Property

def Object_Property ( kind        = gobject.PARAM_READWRITE
                    , nick        = ""
                    , description = ""
                    ) :
    return (gobject.TYPE_PYOBJECT, nick, description, kind)
# end def Object_Property

def Simple_Property ( p_type
                    , kind        = gobject.PARAM_READWRITE
                    , default     = True
                    , nick        = ""
                    , description = ""
                    ) :
    return (p_type, nick, description, default, kind)
# end def Simple_Property

class _M_Object_ (TFL.Meta.M_Auto_Combine_Dicts, TFL.Meta.M_Class) :
    """Metaclass which generates the new GTK types if a `Class_Name` is
       specified. Additionally, this metaclass will create properties for all
       objects of the `__gtk_properties` sequence.
    """

    GTK_Classes       = {}
    _dicts_to_combine = ("_wtk_delegation", )

    @staticmethod
    def _get_property (self, property) :
        return getattr (self, property.name, None)
    # end def _get_property

    @staticmethod
    def _set_property (self, property, value) :
        setattr (self, property.name, value)
    # end def _set_property

    def __new__ (cls, name, bases, dict) :
        Class_Name = dict.get ("Class_Name", None)
        if Class_Name and Class_Name not in cls.GTK_Classes :
            gtk_base  = gtk_class = dict ["GTK_Class"]
            props     = dict.get ("Properties", {})
            gtk_base  = cls.GTK_Classes.get (gtk_base, gtk_base)
            d         = { "__gsignals__"    : dict.get ("Signals", {})
                        , "__gproperties__" : props
                        , "do_get_property" : cls._get_property
                        , "do_set_property" : cls._set_property
                        , "__gtype_name__"  : Class_Name
                        }
            attr  = "_%s__gtk_properties" % (name, )
            old_p = list (dict.get (attr, ()))
            for pname, pspec in props.iteritems () :
                old_p.append (Property (pname))
            dict [attr] = old_p
            gtk_class = type      (Class_Name, (gtk_base, ), d)
            if gtk.pygtk_version < (2, 8) :
                gobject.type_register (gtk_class)
            cls.GTK_Classes [Class_Name] = dict ["GTK_Class"] = gtk_class
        return super (_M_Object_, cls).__new__ (cls, name, bases, dict)
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        for p in getattr \
                (cls, cls._m_mangled_attr_name ("gtk_properties"), ()) :
            setattr (cls, p.name, p)
    # end def __init__

# end class _M_Object_

class Delegator (TFL.Meta.Object) :
    """Simple function delegator"""

    def __init__ (self, name, gtk_name = None) :
        self.name     = name
        self.gtk_name = gtk_name or name
    # end def __init__

    def __call__ (self, this,  * args, ** kw) :
        return getattr (this.wtk_object, self.gtk_name) (* args, ** kw)
    # end def __call__

# end class Delegator

class Delegator_EO (Delegator) :
    """Delegator for a function of the `wtk_object` and extract the
       `exposed_widget` from the first parameter
    """

    def __call__ (self, this, obj, * args, ** kw) :
        return self.__super.__call__ \
            (this, obj.exposed_widget.wtk_object, * args, ** kw)
    # end def __call__

# end class Delegator_EO

class Delegator_O (Delegator) :
    """Delegator for a function of the `wtk_object` and extract the
       `wtk_object` from the first parameter
    """

    def __call__ (self, this, obj, * args, ** kw) :
        return self.__super.__call__ (this, obj.wtk_object, * args, ** kw)
    # end def __call__

# end class Delegator_O

class Delegator_2O (Delegator) :
    """Delegator for a function of the `wtk_object` and extract the
       `wtk_object` from the second parameter
    """

    def __call__ (self, this, a1, obj, * args, ** kw) :
        return self.__super.__call__ (this, a1, obj.wtk_object, * args, ** kw)
    # end def __call__

# end class Delegator_2O

def Delegation (* args, ** kw) :
    for arg in args :
        kw [arg.name] = arg
    return kw
# end def Delegation

class _Object_ (TGL.TKT.Mixin) :
    """Root class for all GTK related objects (TextBuffer, TreeModel, ...)
       and Widgets (TextView, TreeView, ...)

       >>> class Dummy (Object) :
       ...     Class_Name = "Hansi"
       ...     GTK_Class  = gtk.HBox
       ...
       >>> Dummy.GTK_Class
       <class 'Object.Hansi'>
    """

    __metaclass__     = _M_Object_
    __gtk_properties  = ()
    _wtk_delegation   = {}
    weakref           = False
    memory_attributes = ()

    ### `Class_Name` is the name of the new generated GTK-type
    ### `Signals`    is a dictionary describing the signals of the new GTK-type
    GTK_Class        = gtk.Object

    def __init__ (self, AC = None) :
        self.__super.__init__ (AC = AC)
        self._handlers     = {} ### holds all connected callback functions
        ### set the backref directly in the C-gtk object and not in the
        ### python wrapper !
        if self.weakref :
            self.wtk_object.set_data ("ktw_object", weakref.proxy (self))
        else :
            self.wtk_object.set_data ("ktw_object", self)
            #self.bind_add            (self.TNS.Signal.Destroy, self._del_wtk)
        self._sty_stack = []
    # end def __init__

    def _del_wtk (self, event) :
        self.wtk_object.set_data ("ktw_object", None)
    # end def _del_wtk

    def dump_widget_memory (self, recurse = True, ** data) :
        if self.AC and self.name :
            dump = dict \
                ([(n, getattr (self, n)) for n in self.memory_attributes])
            dump.update (data)
            if dump :
                self.AC.memory.state ["widget_memory"] [self.name] = dump
            if recurse :
                for child in getattr (self, "children", ()) :
                    if hasattr (child, "dump_widget_memory") :
                        child.dump_widget_memory (recurse = recurse)
    # end def dump_widget_memory

    def read_widget_memory (self) :
        if self.AC and self.name and self.AC.memory :
            dump = self.AC.memory.state.get ("widget_memory", {}).get \
                (self.name, {})
            if dump :
                for name in self.memory_attributes :
                    value = dump.get (name, None)
                    if value is not None :
                        setattr (self, name, value)
                    del dump [name]
            return dump
        return {}
    # end def read_widget_memory

    def save_widget_memory (self, recurse = True) :
        if self.AC and hasattr (self.AC, "memory") :
            if "widget_memory" not in self.AC.memory.state :
                self.AC.memory.state ["widget_memory"] = {}
            self.dump_widget_memory (recurse = recurse)
            self.AC.memory.dump     ()
    # end def save_widget_memory

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
            ([(p, getattr (self, p)) for p in styler.option_dict.iterkeys ()])
    # end def _before_styler

    def _styler (self, style, Styler = None) :
        if Styler is None :
            Styler = self.Styler
        return Styler (style)
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

    @classmethod
    def path (cls) :
        """Returns path where module resides"""
        return TFL.Filename \
            (TFL.Environment.module_path ("_PMA.Office")).directory
    # end def path

    _std_pathes = None

    @classmethod
    def std_pathes (cls) :
        """Returns standards pathes where to look for auxiliary files like option
           files and bitmaps.
        """
        if cls._std_pathes is None :
            p           = cls.path ()
            cls._std_pathes = []
            _img_pathes     = []
            seen            = {}
            for s in sys.path :
                si = sos.path.join (s, "-Images")
                if sos.path.isdir (si) :
                    _img_pathes.append (si)
            for q in ( p
                     , TFL.Environment.default_dir
                     , TFL.Environment.home_dir
                     ) + tuple (_img_pathes) :
                if q not in seen :
                    cls._std_pathes.append (q)
                    seen [q] = True
        return cls._std_pathes
    # end def std_pathes

    @staticmethod
    def idle_add (callback, * args) :
        return gobject.idle_add (callback, args)
    # end def idle_add

    @staticmethod
    def idle_remove (idle_id) :
        return gobject.source_remove (idle_id)
    # end def idle_remove

    @classmethod
    def read_style_file (cls, filename, search = False) :
        if not sos.path.isfile (filename) and search :
            if not isinstance (filename, TFL.Filename) :
                filename = TFL.Filename (filename, ".rc")
            if not sos.path.isfile (filename.name) :
                fn = filename.base_ext
                for p in cls.std_pathes () :
                    if TFL.Environment.path_contains (p, fn) :
                        filename = TFL.Filename (fn, default_dir = p)
                        break
            filename.make_absolute ()
            filename = filename.name
        if sos.path.isfile (filename) :
            gtk. rc_parse (filename)
    # end def read_style_file

    @staticmethod
    def update_idletasks () :
        """Update pending GUI-Events"""
        while gtk.events_pending ():
            gtk.main_iteration (block = False)
    # end def update_idletasks

# end class _Object_

class Object (_Object_) :
    """Root class for all GTK related objects (TextBuffer, TreeModel, ...)
       and Widgets (TextView, TreeView, ...)

       >>> class Dummy (Object) :
       ...     Class_Name = "Hansi"
       ...     GTK_Class  = gtk.HBox
       ...
       >>> Dummy.GTK_Class
       <class 'Object.Hansi'>
    """

    def __init__ (self, * args, ** kw) :
        AC = None
        if "AC" in kw :
            AC = kw ["AC"]
            del kw  ["AC"]
        if "wtk_object" in kw :
            self.wtk_object = kw ["wtk_object"]
            del kw ["wtk_object"]
        else :
            self.wtk_object = self.GTK_Class (* args, ** kw)
        self.__super.__init__ (AC = AC)
    # end def __init__

# end class Object

class Object_Wrapper (_Object_) :
    """Base class with alows the wrapping of an already existing GTK object
       passed as the first parameter to the constructor of the class,
    """

    def __init__ (self, wtk_object, AC = None) :
        self.wtk_object    = wtk_object
        self.__super.__init__ (AC = AC)
    # end def __init__

# end class Object_Wrapper

main = gtk.main
quit = gtk.main_quit

if __name__ != "__main__" :
    TGL.TKT.GTK._Export ("*", "gtk", "main", "quit")
else :
    class New_Object (Object) :

        Class_Name = "New_Object"
        GTK_Class = gtk.Label

        Properties = dict \
            ( foo      = Simple_Property (str,               default = "bar")
            , boolprop = Simple_Property (bool,              default = False)
            , number   = Number_Property (gobject.TYPE_UINT, default = 0)
            )
    # end class New_Object

    x = New_Object ()

    print x.wtk_object.get_property ("foo")
    print x.wtk_object.get_property ("boolprop")
    print x.wtk_object.set_property ("foo", "AAA")
    print x.wtk_object.get_property ("foo")
    print x.wtk_object.get_property ("boolprop")
### __END__ TGL.TKT.GTK.Object
