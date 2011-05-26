# -*- coding: iso-8859-15 -*-
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
#    TGL.TKT.GTK.Text_Buffer
#
# Purpose
#    Wrapper for the GTK widget TextBuffer
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#     2-Apr-2005 (MG) `TFL.TKT.Text` interface implemented
#     2-Apr-2005 (MG) Optional argument `tag` added to `apply_style` and
#                      `_tag`
#     2-Apr-2005 (MG) `tags_at` added
#     3-Apr-2005 (MG) `insert_image` added
#     3-Apr-2005 (MG)
#     3-Apr-2005 (MG) `_tag`: pass `AC` to the tag creation
#     5-Apr-2005 (MG) `mark_at` changed to allow `name` to be a mark which
#                     shall be `moved`
#     5-Apr-2005 (MG) `Styler` removed
#     7-Apr-2005 (MG) `eot_pos` changed to use internal created `__END__` mark
#    14-Apr-2005 (CT)  `bot_pos`, `eot_pos`, and `current_pos` replaced by
#                      `buffer_head`, `buffer_tail`, and `insert_mark`,
#                      respectively
#    10-Jun-2005 (MG) `_tag`: delete tag if a tag with the passed name
#                     already exists
#     5-Sep-2005 (MG) `remove_style`: check if the style to remove has a tag
#    ««revision-date»»···
#--

from   _TGL                   import TGL
import _TGL._TKT._GTK.Object
import _TGL._TKT._GTK.Text_Tag
import _TGL._TKT.Text
import  weakref

GTK = TGL.TKT.GTK
gtk = GTK.gtk

class Text_Buffer (GTK.Object, TGL.TKT.Text) :
    """Wrapper for the GTK widget TextBuffer"""

    GTK_Class        = gtk.TextBuffer
    __gtk_properties = \
        ( GTK.Property            ("tag_table")
        ,
        )

    def __init__ (self, AC = None) :
        self.__super.__init__ (AC = AC)
        self._tag_map   = weakref.WeakKeyDictionary ()
        self._end_mark  = self.mark_at \
            (0, left_gravity = False, name = "__END__")
    # end def __init__

    bot_iter    = property (lambda s : s.wtk_object.get_start_iter ())
    eot_iter    = property (lambda s : s.wtk_object.get_end_iter   ())

    buffer_head = 0
    buffer_tail = property (lambda s : s._end_mark)
    insert_mark = property (lambda s : s.wtk_object.get_insert ())

    def apply_style ( self
                    , style
                    , head  = None
                    , tail  = None
                    , delta = 0
                    , lift  = False
                    , tag   = None
                    ) :
        if head is None :
            ### head is None -> apply the style to the complete widget
            ### instead of a text range
            self.__super.apply_style (style)
        else :
            tag = self._tag (style, tag)
            self.wtk_object.apply_tag \
                ( tag.wtk_object
                , self._move_iter     (self._iter_from_pom (head), delta)
                , self._iter_from_pom (tail or self.buffer_tail)
                )
            if lift :
                tag.priority = self.tag_table.get_size ()
    # end def apply_style

    def delete (self, start = None, end = None) :
        self.wtk_object.delete (start or self.bot_iter, end or self.eot_iter)
    # end def delete

    def bol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        pos = self._iter_from_pom (pos_or_mark)
        ### move iter to start of line
        self._move_iter           (pos, delta, line_delta)
        pos.set_line_offset       (0)
        return pos.get_offset     ()
    # end def bol_pos

    clear = delete

    def eol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        pos = self._iter_from_pom (pos_or_mark)
        ### move iter to end of line
        self._move_iter           (pos, delta, line_delta).get_offset ()
        pos.forward_to_line_end   ()
        return pos.get_offset     ()
    # end def eol_pos

    def find (self, text, head = None, tail = None, delta = 0, backwards = False) :
        start = (self.bot_iter, self.eot_iter) [backwards]
        head  = self._move_iter (self._iter_from_pom (head or start), delta)
        if tail :
            tail = self._iter_from_pom (tail, copy_pos = False)
        search   = (head.forward_search, head.backward_search) [backwards]
        result   = search \
            ( text
            , limit = tail
            , flags = gtk.TEXT_SEARCH_VISIBLE_ONLY | gtk.TEXT_SEARCH_TEXT_ONLY
            )
        return result and result [0].get_offset ()
    # end def find

    def free_mark (self, * mark) :
        for m in mark :
            self.wtk_object.delete_mark (m)
    # end def free_mark

    def get (self, head = None, tail = None, delta= 0) :
        head = self._iter_from_pom (head or self.bot_iter)
        tail = self._iter_from_pom (tail or self.eot_iter, copy_pos = False)
        head = self._move_iter (head, delta)
        return self.wtk_object.get_text (head, tail)
    # end def get

    def insert (self, pos_or_mark, text, style = None, delta = 0) :
        head = self._move_iter (self._iter_from_pom (pos_or_mark), delta)
        tag  = self._tag (style)
        if tag :
            return self.wtk_object.insert_with_tags \
                (head, text, tag.wtk_object)
        return self.wtk_object.insert_with_tags (head, text)
    # end def insert

    def insert_image (self, pos_or_mark, image_name, style = None, delta = 0) :
        image  = GTK.image_mgr [image_name].get_pixbuf ()
        start  = self._move_iter (self._iter_from_pom (pos_or_mark), delta)
        self.wtk_object.insert_pixbuf (start, image)
        if style :
            end = self._iter_from_pom (self.insert_mark)
            self.wtk_object.apply_tag \
                (self._tag (style).wtk_object, start, end)
    # end def insert_image

    def insert_widget (self, pos_or_mark, widget, style = None, delta = 0) :
        raise NotImplementedError, \
            "insert_widget cannot be implemented for a Text-Buffer"
    # end def insert_widget

    def mark_at (self, pos, delta = 0, name = None, left_gravity = False) :
        pos = self._move_iter (self._iter_from_pom (pos), delta)
        if not isinstance (name, GTK.gtk.TextMark) :
            return self.wtk_object.create_mark (name, pos, left_gravity)
        self.wtk_object.move_mark (name, pos)
        return name
    # end def mark_at

    def place_cursor (self, pos_or_mark) :
        return self.wtk_object.place_cursor \
            (self._iter_from_pom (pos_or_mark, copy_pos = False))
    # end def place_cursor

    def pos_at (self, pos, delta = 0) :
        return self._move_iter (self._iter_from_pom (pos), delta)
    # end def pos_at

    def remove (self, head, tail = None, delta = 0) :
        head = self._iter_from_pom (head, copy_pos = False)
        if tail is None :
            tail = self._move_iter     (head.copy (), delta)
        else :
            tail = self._iter_from_pom (tail)
        return self.delete (head, tail)
    # end def remove

    def remove_style (self, style, head, tail = None, delta = 0) :
        if style in self._tag_map :
            self.wtk_object.remove_tag \
                ( self._tag_map [style].wtk_object
                , self._move_iter     (self._iter_from_pom (head), delta)
                , self._iter_from_pom (tail or self.buffer_tail)
                )
    # end def remove_style

    def see (self, pos_or_mark) :
        raise NotImplementedError, \
            "`see` cannot be implemented by a Text-Buffer"
    # end def see

    def set_tabs (self, * tabs) :
        raise NotImplementedError, \
            "`set_tabs` cannot be implemented by a Text-Buffer"
    # end def set_tabs

    def tags_at (self, pos_or_mark) :
        iter = self._iter_from_pom (pos_or_mark)
        return [t.get_property ("name") for t in iter.get_tags ()]
    # end def tags_at

    ### only internal functions
    def _move_iter (self, iter, delta = 0, line_delta = 0) :
        if delta :
            iter.forward_chars (delta)
        if line_delta :
            iter.forward_lines (line_delta)
        return iter
    # end def _move_iter

    def _iter_from_pom (self, pos_or_mark, copy_pos = True) :
        if isinstance (pos_or_mark, GTK.gtk.TextMark) :
            return self.wtk_object.get_iter_at_mark (pos_or_mark)
        elif isinstance (pos_or_mark, gtk.TextIter) :
            if copy_pos :
                return pos_or_mark.copy ()
            return pos_or_mark
        return self.wtk_object.get_iter_at_offset (pos_or_mark)
    # end def _iter_from_pom

    def _tag (self, style, name = None) :
        result = None
        if style is not None :
            if style not in self._tag_map :
                if name :
                    tt  = self.tag_table
                    tag = tt.lookup (name)
                    if tag :
                        tt.remove (tag)
                self._tag_map [style]  = tag = GTK.Text_Tag (name, AC = self.AC)
                tag.apply_style (style)
                self.tag_table.add (tag.wtk_object)
            result = self._tag_map [style]
        return result
    # end def _tag

# end class Text_Buffer

Text = Text_Buffer

def _doctest_AC () :
    ### Restricted to doctest use, only
    import _TGL._UI
    import _TGL._UI.App_Context
    return TGL.UI.App_Context (TGL)
# end def _doctest_AC

__test__ = dict (interface_test = TGL.TKT.Text._interface_test)

if __name__ != "__main__" :
    GTK._Export ("Text_Buffer")
### __END__ TGL.TKT.GTK.Text_Buffer
