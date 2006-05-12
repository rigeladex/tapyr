# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.DL_List
#
# Purpose
#    Doubly linked list
#
# Revision Dates
#    11-Sep-2003 (CT)  Creation
#    12-Sep-2003 (CT)  Creation continued
#    15-Sep-2003 (CT)  s/_append/insert/g
#    15-Sep-2003 (CT)  `_new_item` factored
#    29-Sep-2003 (CED) `list_of_preds`, `list_of_succs` added
#     7-Oct-2003 (CT)  `list_of_preds`, `list_of_succs` removed
#     2-Dec-2003 (CT)  Already commented-out `__getattr__` finally removed
#     9-Mar-2004 (CT)  `_doc_test` changed to not use `import`
#    30-Jun-2005 (CT)  Style improvements
#     2-Jul-2005 (CT)  `_DL_Chain_` factored
#     2-Jul-2005 (CT)  Class attribute `DL_Item` added to `_DL_Chain_`
#     2-Jul-2005 (CT)  `DL_Item.predecessors` and `DL_Item.successors`
#                      changed to break at `self` (to allow cyclic structures)
#     2-Jul-2005 (CT)  `DL_Ring` added
#     2-Jul-2005 (CT)  `_DL_Counted_` factored and `DL_Ring_Counted` added
#    11-May-2006 (CED) `DL_Ring_Sorted` introduced
#    12-May-2006 (CT)  `DL_Ring_Sorted._insert` simplified (and disobfuscated)
#    12-May-2006 (CED) 'DL_Item_Sortable` added and used
#    ««revision-date»»···
#--

from   _TFL        import TFL
import _TFL.predicate
import _TFL._Meta.Object

class DL_Item (TFL.Meta.Object) :
    """Item in a doubly linked list"""

    def __init__ (self, value = None, next = None, prev = None) :
        self.value = value
        self.link_next (next)
        self.link_prev (prev)
    # end def __init__

    def link_next (self, other) :
        self.next = other
        if other is not None :
            other.prev = self
    # end def link_next

    def link_prev (self, other) :
        self.prev = other
        if other is not None :
            other.next = self
    # end def link_prev

    def predecessors (self) :
        """Generate predecessors of `self`."""
        p = self
        while p.prev :
            p = p.prev
            if p is self :
                break
            yield p
    # end def predecessors

    def successors (self) :
        """Generate successors of `self`."""
        p = self
        while p.next :
            p = p.next
            if p is self :
                break
            yield p
    # end def successors

    def resplice (self, h, t) :
        """Move DL_Items from `h` to `t` after `self`
           (removing that sequence wherever it lived before).
        """
        assert bool (h) and bool (t), "resplice %s: %s %s" % (self, h, t)
        h.prev.link_next (t.next)
        t.link_next      (self.next)
        self.link_next   (h)
    # end def resplice

    def __nonzero__ (self) :
        return not (self.next is None or self.prev is None)
    # end def __nonzero__

    def __str__ (self) :
        if bool (self) :
            return str (self.value)
        else :
            return "<%s at %s: %s, %s, %s>" % \
                ( self.__class__, id (self)
                , id (self.next), id (self.prev), self.value
                )
    # end def __str__

    def __repr__ (self) :
        if self.value is None :
            return "<empty item>"
        else :
            return repr (self.value)
    # end def __repr__

# end class DL_Item

class DL_Item_Sortable (DL_Item) :

    def __init__ (self, value = None, key = None, next = None, prev = None) :
        self.__super.__init__ (value, next, prev)
        self.key = key
    # def __init__

# class DL_Item_Sortable

class _DL_Chain_ (TFL.Meta.Object) :
    """Root class for doubly linked chains."""

    DL_Item = DL_Item

    def __init__ (self, * items) :
        self.clear  ()
        self.append (* items)
    # end def __init__

    def append (self, * items) :
        """Append `items` at end of list"""
        self.insert (self._T.prev, * items)
    # end def append

    def insert (self, pred, * items) :
        """Insert `items` after `pred`"""
        for item in items :
            pred = self._new_item (pred, item)
    # end def insert

    def item (self, index) :
        """Return item at `index` (starting from 0).
           Beware of O(n) behavior for a single call.
        """
        if index >= 0 :
            i = index
            r = self.head
            while i > 0 and r :
                i -= 1
                r  = r.next
        else :
            i = - index - 1
            r = self.tail
            while i > 0 and r :
                i -= 1
                r  = r.prev
        if not r :
            raise IndexError, index
        return r
    # end def item

    def pop (self) :
        """Remove and return last element."""
        return self.remove (self.tail)
    # end def pop

    def pop_front (self) :
        """Remove and return first element."""
        return self.remove (self.head)
    # end def pop_front

    def prepend (self, * items) :
        """Prepend `items` at front of list."""
        self.insert (self._H, * items)
    # end def prepend

    def remove (self, item) :
        """Remove `item` from its list."""
        item.prev.link_next (item.next)
        return item.value
    # end def remove

    def reverse_iter (self) :
        """Generate items in list in reverse order."""
        return self._T.predecessors ()
    # end def reverse_iter

    def reverse_values (self) :
        """Generate values in list in reverse order."""
        for item in self.reverse_iter () :
            yield item.value
    # end def reverse_values

    def values (self) :
        """Generate values in list."""
        for item in iter (self) :
            yield item.value
    # end def values

    itervalues = values ### compatibility to `dict`

    def _new_item (self, pred, item) :
        return self.DL_Item (item, pred.next, pred)
    # end def _new_item

    def __iter__ (self) :
        return self._H.successors ()
    # end def __iter__

# end class _DL_Chain_

class _DL_Counted_ (TFL.Meta.Object) :
    """Mixin counting elements."""

    def clear (self) :
        self.__super.clear ()
        self.count = 0
    # end def clear

    def insert (self, pred, * items) :
        self.__super.insert (pred, * items)
        self.count += len   (items)
    # end def insert

    def remove (self, item) :
        self.__super.remove (item)
        self.count -= 1
    # end def remove

    def __len__ (self) :
        return self.count
    # end def __len__

# end class _DL_Counted_

class DL_List (_DL_Chain_) :
    """Doubly linked list.

       >>> dl = DL_List (0, 1, 2, 3, 4)
       >>> list (dl)
       [0, 1, 2, 3, 4]
       >>> dl.head, dl.tail
       (0, 4)
       >>> list (dl.head.successors ())
       [1, 2, 3, 4]
       >>> list (dl.tail.predecessors ())
       [3, 2, 1, 0]
       >>> dl.item (2)
       2
       >>> dl.item (5)
       Traceback (most recent call last):
       ...
       IndexError: 5
       >>> dl.prepend (42)
       >>> list (dl), list (dl.reverse_values ())
       ([42, 0, 1, 2, 3, 4], [4, 3, 2, 1, 0, 42])
       >>> dl.pop_front ()
       42
       >>> dl.pop ()
       4
       >>> dl.remove (dl.head.next)
       1
       >>> for x in dl :
       ...   print x
       ...
       0
       2
       3
       >>> dl.clear ()
       >>> list (dl)
       []
       >>> dl = DL_List (0, 1, 2, 3, 4)
       >>> dk = DL_List ("a", "b", "c", "d", "e")
       >>> dl.head.resplice (dl.tail.prev, dl.tail)
       >>> list (dl), list (dk)
       ([0, 3, 4, 1, 2], ['a', 'b', 'c', 'd', 'e'])
       >>> dk.head.next.next.resplice (dl.head.next, dl.tail.prev)
       >>> list (dl), list (dk)
       ([0, 2], ['a', 'b', 'c', 3, 4, 1, 'd', 'e'])
    """

    head    = property (lambda s : s._H.next)
    tail    = property (lambda s : s._T.prev)

    def __init__ (self, * items) :
        self._H = self.DL_Item ()
        self._T = self.DL_Item ()
        self.__super.__init__  (* items)
    # end def __init__

    def clear (self) :
        """Remove all items from list."""
        self._H.link_next (self._T)
    # end def clear

    def remove (self, item) :
        if item is self._H or item is self._T :
            raise IndexError, error
        return self.__super.remove (item)
    # end def remove

    def __nonzero__ (self) :
        return self._H.next is not self._T
    # end def __nonzero__

# end class DL_List

class DL_List_Counted (_DL_Counted_, DL_List) :
    """DL_List counting its elements

       >>> dlc = DL_List_Counted (* range (5))
       >>> dlc.count
       5
       >>> dlc.pop()
       >>> len (dlc)
       4
       >>> dlc.append (42)
       >>> len (dlc)
       5
    """

# end class DL_List_Counted

### XXX please make an own module for DL_Ring classes

class DL_Ring (_DL_Chain_) :
    """Doubly linked ring.

       >>> dr = DL_Ring (0, 1, 2, 3, 4)
       >>> list (dr)
       [0, 1, 2, 3, 4]
       >>> dr.head, dr.tail
       (0, 4)
       >>> list (dr.head.successors ()), list (dr.head.predecessors ())
       ([1, 2, 3, 4], [4, 3, 2, 1])
       >>> list (dr.tail.successors ()), list (dr.tail.predecessors ())
       ([0, 1, 2, 3], [3, 2, 1, 0])
       >>> dr.item (2)
       2
       >>> dr.item (5)
       0
       >>> dr.prepend (42)
       >>> list (dr), list (dr.reverse_values ())
       ([42, 0, 1, 2, 3, 4], [4, 3, 2, 1, 0, 42])
       >>> dr.pop_front ()
       42
       >>> dr.pop ()
       4
       >>> dr.remove (dr.head.next)
       1
       >>> for x in dr :
       ...   print x
       ...
       0
       2
       3
       >>> dr.clear ()
       >>> list (dr)
       []
       >>> print dr.head, dr.tail
       None None
       >>> dr = DL_Ring (0, 1, 2, 3, 4)
       >>> list (dr)
       [0, 1, 2, 3, 4]
       >>> dr.rotate_next (4)
       >>> list (dr)
       [4, 0, 1, 2, 3]
       >>> dr.rotate_prev (1)
       >>> list (dr)
       [3, 4, 0, 1, 2]
       >>> dr.rotate_prev (3)
       >>> list (dr)
       [0, 1, 2, 3, 4]
    """

    head    = property (lambda s : s._H and s._H.next)
    tail    = property (lambda s : s._T.prev)
    _H      = property (lambda s : s.mark.prev)
    _T      = property (lambda s : s.mark)
    _NIL    = DL_Item  ()

    def clear (self) :
        """Remove all items from list."""
        self.mark = self._NIL
    # end def clear

    def insert (self, pred, * items) :
        if items :
            if self.mark is self._NIL :
                pred  = self.mark = self._new_item (self._NIL, items [0])
                items = items   [1:]
                pred.link_next  (pred)
            self.__super.insert (pred, * items)
    # end def insert

    def prepend (self, * items) :
        self.__super.prepend (* items)
        self.rotate_prev     (len (items))
    # end def prepend

    def remove (self, item) :
        if item is self._NIL :
            raise IndexError, error
        elif item.next is item.prev is item :
            assert item is self.mark
            self.clear ()
            return item
        else :
            if item is self.mark :
                self.mark = item.next
            return self.__super.remove (item)
    # end def remove

    def reverse_iter (self) :
        if self.mark is not self._NIL :
            for p in self._T.predecessors () :
                yield p
            yield self._T
    # end def reverse_iter

    def rotate_next (self, n) :
        """Move `self.mark` forward (i.e., following `next`) `n` times."""
        for i in xrange (n) :
            self.mark = self.mark.next
    # end def rotate_next

    def rotate_prev (self, n) :
        """Move `self.mark` backward (i.e., following `prev`) `n` times."""
        for i in xrange (n) :
            self.mark = self.mark.prev
    # end def rotate_prev

    def __iter__ (self) :
        if self.mark is not self._NIL :
            for s in self._H.successors () :
                yield s
            yield self._H
    # end def __iter__

    def __nonzero__ (self) :
        return self.mark is not self._NIL
    # end def __nonzero__

# end class DL_Ring

class DL_Ring_Sorted (DL_Ring) :
    """DL_Ring sorting its elements

       >>> drs = DL_Ring_Sorted (2, 1, 3)
       >>> list (drs)
       [1, 2, 3]
       >>> drs.insert (3, 5, 4)
       >>> list (drs)
       [1, 2, 3, 3, 4, 5]
       >>> drs.insert (0, -1, 42)
       >>> list (drs)
       [-1, 0, 1, 2, 3, 3, 4, 5, 42]
       >>> drs.insert (0.25)
       >>> list (drs)
       [-1, 0, 0.25, 1, 2, 3, 3, 4, 5, 42]
    """

    DL_Item = DL_Item_Sortable

    def __init__ (self, * items, ** kw) :
        if "key" in kw :
            self.key = kw ["key"]
        else :
            self.key = TFL.identity
        self.clear  ()
        self.insert (* items)
    # end def __init__

    def append (self, * items) :
        raise TypeError, "Append not allowed for DL_Ring_Sorted"
    # end def append

    def insert (self, * items) :
        for i in items :
            self._insert (i)
    # end def insert

    def prepend (self, items) :
        raise TypeError, "Prepend not allowed for DL_Ring_Sorted"
    # end def prepend

    def _insert (self, other) :
        key = self.key (other)
        try :
            larger = TFL.first (it for it in self if it.key > key)
        except IndexError :
            prev = self.tail
        else :
            prev = larger.prev
        self.__super.insert (prev, other)
        if self.mark.key > key :
            self.rotate_prev (1)
    # end def _insert

    def _new_item (self, pred, item) :
        return self.DL_Item (item, self.key (item), pred.next, pred)
    # end def _new_item

# end class DL_Ring_Sorted

class DL_Ring_Counted (_DL_Counted_, DL_Ring) :
    """DL_Ring counting its elements

       >>> drc = DL_Ring_Counted (* range (5))
       >>> drc.count
       5
       >>> drc.pop()
       >>> len (drc)
       4
       >>> drc.append (42)
       >>> len (drc)
       5
    """

# end class DL_Ring_Counted

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.DL_List
