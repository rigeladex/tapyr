# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
#    TGL.TKT.GTK.Image_Manager
#
# Purpose
#    Handling of all images used by the application
#
# Revision Dates
#     3-Apr-2005 (MG) Creation
#     5-Apr-2005 (MG) `.png` support added
#    ««revision-date»»···
#--

from   _TGL                   import TGL
from   _TFL                   import TFL
import _TFL._Meta.Object
import _TGL._TKT._GTK.Image
import  Environment
import _TFL.sos      as     sos
from   _TFL.Filename import Filename
GTK = TGL.TKT.GTK
gtk = GTK.gtk

def path () :
    """Returns path where module resides"""
    return Environment.module_path ("CT_TK")
# end def path

_std_pathes = None

def std_pathes () :
    """Returns standards pathes where to look for auxiliary files like option
       files and bitmaps.
    """
    global _std_pathes
    if _std_pathes is None :
        p           = path ()
        _std_pathes = []
        seen        = {}
        for q in ( p
                 , sos.path.join (p, "-Images")
                 , Environment.default_dir
                 , Environment.home_dir
                 ) :
            if q not in seen :
                _std_pathes.append (q)
                seen [q] = True
    return _std_pathes
# end def std_pathes

class _Image_Mgr_ (TFL.Meta.Object) :
    """Root class for management of a collection of bitmaps (.xbm) and/or
       images (.gif)
    """

    Image_class = { ".xbm" : GTK.Image}

    def __init__ (self, * d) :
        """Construct a Image_Mgr, looking in directories specified by `d' for
           bitmaps and images (in addition to looking in the `std_pathes')
        """
        self.x_map  = {}
        self.files  = {}
        self.pathes = list (d) + std_pathes ()
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
                if Environment.path_contains (p, fn) :
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

    Image_class = { ".xbm" : GTK.Image
                  , ".gif" : GTK.Image
                  , ".png" : GTK.Image
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


