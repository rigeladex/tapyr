# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.Image_Manager
#
# Purpose
#    Handling of all images used by the application
#
# Revision Dates
#     3-Apr-2005 (MG) Creation
#     5-Apr-2005 (MG) `.png` support added
#     5-Apr-2005 (MG) Store gtk.Pixbuf object's instead of GTK.Image objects
#    16-May-2005 (MG) `std_pathes` changed
#    28-Jul-2005 (MG) `std_pathes` moved to `TGL.TKT.GTK.Object`
#    ««revision-date»»···
#--

from   _TGL                   import TGL
from   _TFL                   import TFL
import _TFL._Meta.Object
import _TGL._TKT._GTK.Image
import _TFL.Environment
import _TFL.sos      as     sos
from   _TFL.Filename import Filename
import  sys

GTK = TGL.TKT.GTK
gtk = GTK.gtk

class _Image_Mgr_ (TFL.Meta.Object) :
    """Root class for management of a collection of bitmaps (.xbm) and/or
       images (.gif)
    """

    Image_class = { ".xbm" : gtk.gdk.pixbuf_new_from_file}

    def __init__ (self, * d) :
        """Construct a Image_Mgr, looking in directories specified by `d' for
           bitmaps and images (in addition to looking in the `std_pathes')
        """
        self.x_map  = {}
        self.files  = {}
        self.pathes = list (d) + GTK.Image.std_pathes ()
    # end def __init__

    def add (self, filename, name = None, ** kw) :
        """Add bitmap or image in `filename' to collection.

           If `name' is not specified, it defaults to `filename.base'.

           `kw' is passed to `BitmapImage' or `PhotoImage', respectively.
        """
        if not isinstance (filename, Filename) :
            filename = Filename (filename, ".xbm")
        assert (self.Image_class.has_key (filename.ext))
        if not sos.path.isfile (filename.name) :
            fn = filename.base_ext
            for p in self.pathes :
                if TFL.Environment.path_contains (p, fn) :
                    filename = Filename (fn, default_dir = p)
                    break
        filename.make_absolute ()
        if not name :
            name = filename.base
        name = self.normalized (name)
        if self.files.has_key (name) :
            if self.files [name].name != filename.name :
                print "Name clash for %s %s: %s vs. %s" \
                      % ( self.Image_class [filename.ext]
                        , name, filename.name, self.files [name].name
                        )
                return None
        else :
            self.files [name] = filename
        if name :
            self.cnf [name] = kw
        return name
    # end def add

    def get (self, name, default = None) :
        try :
            return self [name]
        except KeyError :
            return default
    # end def get

    def normalized (self, name) :
        return sos.path.normcase (name.replace (".", "_"))
    # end def normalized

    def __getitem__ (self, name) :
        return self.x_map [self.normalized (name)]
    # end def __getitem__

    def keys (self) :
        return self.files.keys ()
    # end def keys

# end class _Image_Mgr_

class Image_Mgr (_Image_Mgr_):
    """Provide management of a collection of bitmaps (.xbm) and images (.gif)
    """

    Image_class = { ".xbm" : gtk.gdk.pixbuf_new_from_file
                  , ".gif" : gtk.gdk.pixbuf_new_from_file
                  , ".png" : gtk.gdk.pixbuf_new_from_file
                  }

    def __init__ (self, * d) :
        """Construct a Image_Mgr, looking in directories specified by `d' for
           bitmaps and images (in addition to looking in the `std_pathes')
        """
        self.__super.__init__ (* d)
        self.cnf = {}
    # end def __init__

    def add (self, filename, name = None, ** kw) :
        """Add bitmap or image in `filename' to collection.

           If `name' is not specified, it defaults to `filename.base'.

           `kw' is passed to `BitmapImage' or `PhotoImage', respectively.
        """
        name = self.__super.add (filename, name)
        if name :
            self.cnf [name] = kw
        return name
    # end def add

    def __getitem__ (self, name) :
        name = self.normalized (name)
        if not self.x_map.has_key (name) :
            filename          = self.files [name]
            self.x_map [name] = self.Image_class [filename.ext] \
                (filename.name, ** self.cnf [name])
        return self.x_map [name]
    # end def __getitem__

# end class Image_Mgr

image_mgr = Image_Mgr ()

if __name__ != "__main__" :
    GTK._Export ("image_mgr")
### __END__ TGL.TKT.GTK.Image_Manager


