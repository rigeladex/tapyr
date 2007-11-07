# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    CTK_Canvas
#
# Purpose
#    Canvas related classes based on CT_TK
#
# Revision Dates
#    27-Jun-2002 (CT) Creation (factored from _CSE and from OO_Model)
#     9-Dec-2002 (CT) `tag_under_mouse` corrected (use `target` instead of
#                     `canvas` for coordinate transform)
#    16-Mar-2006 (CT) Style
#     7-Nov-2007 (CT) Moved into package _TFL._TKT._Tk
#    ««revision-date»»···
#--

from   _TFL._TKT._Tk.CTK import *
from   _TFL._D2          import D2
import _TFL._D2.Point
import _TFL._D2.Line
import _TFL._D2.Rect

class Canvas_Object (CTK.CT_TK_mixin) :
    """Base class for special canvas-object classes."""

    box_size    = D2.Point ( 5,  5)
    grid        = D2.Point ( 0,  0)
    base_offset = D2.Point ( 0,  0)

    def __init__ (self, canvas, name, pos) :
        self.canvas = canvas
        self.name   = name
        self.tag    = name
        self.pos    = self._coord_trans (pos)
    # end def __init__

    def scaled_font (self, font, scale) :
        font_item = font.split (None, 2)
        if len (font_item) > 1 :
            font_item [1] = repr \
                (self.scaled_font_size (eval (font_item [1], {}, {}), scale))
        else :
            font_item.append (repr (self.scaled_font_size (12, scale)))
        return " ".join (font_item)
    # end def scaled_font

    def scaled_font_size (self, size, scale) :
        return int ((size * scale) + 0.5)
    # end def scaled_font_size

    def bind (self, sequence=None, command=None):
        self.canvas.tag_bind (self.tag, sequence, command)
    # end def bind

    def _coord_trans (self, p) :
        return D2.Point \
            ( self.canvas.canvasx (p.x, self.grid.x)
            , self.canvas.canvasy (p.y, self.grid.y)
            ).shift (self.base_offset)
    # end def _coord_trans

    def _add_tag (self, object, * tags) :
        for t in tags :
            object.addtag (t)
    # end def _add_tag

# end class Canvas_Object

class Tagged_Object :

    key_map = {}

    def tag_under_mouse (self, event, tag_pat, canvas = None) :
        canvas   = canvas or self.canvas
        (xr, yr) = (event.x_root, event.y_root)
        target   = canvas.winfo_containing (xr, yr)
        if target and target.winfo_class () == "Canvas" :
            x = target.canvasx (xr - target.winfo_rootx ())
            y = target.canvasy (yr - target.winfo_rooty ())
            for id in target.find_overlapping (x-1, y-1, x+1, y+1) :
                tags = reversed (target.gettags (id))
                for tag in tags :
                    if tag_pat.search (tag) :
                        return tag
        return None
    # end def tag_under_mouse

# end class Tagged_Object

class Tagged_Canvas (Tagged_Object) :

    tag_list        = ()
    obj_map         = {}

    ###+
    ### the following _delegate_«binding» functions are necessary in order to
    ### avoid individual tag-bindings for different canvas tag types
    ###
    ### we avoid tag-bindings since Tkinter doesn't seem to free them after
    ### the deletion of the corresponding tags (even if we explicitly delete
    ### the tag-bindings)
    ###
    ### as a fringe benefit, this makes the bindings independent of the
    ### stacking order of the canvas object and thus saves some layers
    ###     - one rectangle for each title field (one per host, one per round)
    ###     - one-third of the rectangles of each message
    ### and some tags
    ###
    ### if several objects overlap each other, the priority of the bindings
    ### is defined by the sequence of tag-patterns in `tag_list`
    ###
    ### for each class, the functions to be delegated must be listed in the
    ### `key_map' which associates methods to be called with event-names.
    ### event-names missing from `key_map' are silently ignored
    ###-

    def _delegate_click (self, event, ev_name) :
        obj_map = self.obj_map
        self._clicked_obj = None
        for pat in self.tag_list :
            tag = self.tag_under_mouse (event, pat)
            if tag :
                if tag in obj_map :
                    obj = self._clicked_obj = obj_map [tag]
                    if ev_name in obj.key_map :
                        return obj.key_map [ev_name] (obj, event)
                    ###else : print "Unbound event", ev_name, "for", tag
                else :
                    print "Unknown object tag", tag
                return "break"
        return "break"
    # end def _delegate_click

    def _delegate_drag (self, event, ev_name) :
        if self._clicked_obj :
            obj = self._clicked_obj
            if ev_name in obj.key_map :
                return obj.key_map [ev_name] (obj, event)
        return "break"
    # end def _delegate_drag

    def _delegate_drop (self, event, ev_name) :
        result = "break"
        try :
            if self._clicked_obj :
                obj = self._clicked_obj
                if ev_name in obj.key_map :
                    result = obj.key_map [ev_name] (obj, event)
            else :
                result = self._delegate_click (event, ev_name)
        finally :
            self._clicked_obj = None
        return result
    # end def _delegate_drop

# end class Tagged_Canvas

### __END__ TFL.TKT.Tk.CTK_Canvas
