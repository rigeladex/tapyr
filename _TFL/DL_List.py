# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003 Mag. Christian Tanzer. All rights reserved
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
#    DL_List
#
# Purpose
#    Doubly linked list
#
# Revision Dates
#    11-Sep-2003 (CT) Creation
#    12-Sep-2003 (CT) Creation continued
#    ««revision-date»»···
#--

from   __future__  import generators

from   _TFL        import TFL

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
        """Iterator over predecessors of `self`."""
        p = self
        while p.prev :
            p = p.prev
            yield p
    # end def predecessors

    def successors (self) :
        """Iterator over successors of `self`."""
        p = self
        while p.next :
            p = p.next
            yield p
    # end def successors

    def resplice (self, h, t) :
        """Move DL_Items from `h` to `t` after `self` (removing that sequence
           wherever it lived before).
        """
        h.prev.link_next (t.next)
        t.link_next      (self.next)
        self.link_next   (h)
    # end def resplice

    def __getattr__ (self, name) :
        if name.startswith ("__") and name.endswith ("__") :
            raise AttributeError, name
        return getattr (self.value, name)
    # end def __getattr__

    def __nonzero__ (self) :
        return not (self.next is None or self.prev is None)
    # end def __nonzero__

    def __str__ (self) :
        return str (self.value)
    # end def __str__

    def __repr__ (self) :
        return repr (self.value)
    # end def __repr__

# end class DL_Item

class DL_List (TFL.Meta.Object) :
    """Doubly linked list.

       >>> dl = DL_List (0, 1, 2, 3, 4)
       >>> list (dl)
       [0, 1, 2, 3, 4]
       >>> for x in dl :
       ...   print x
       ...
       0
       1
       2
       3
       4
       >>> dl.head
       0
       >>> dl.tail
       4
    """

    def __init__ (self, * items) :
        self._H = h = DL_Item ()
        self._T     = DL_Item ()
        self.clear  ()
        self.append (* items)
    # end def __init__

    head = property (lambda s : s._H.next)
    tail = property (lambda s : s._T.prev)

    def append (self, * items) :
        self._append (self._T.prev, * items)
    # end def append

    def _append (self, p, * items) :
        for item in items :
            p = DL_Item (item, p.next, p)
    # end def _append

    def clear (self) :
        self._H.link_next (self._T)
    # end def clear

    def item (self, index) :
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

    def __iter__ (self) :
        return self._H.successors ()
    # end def __iter__

    def pop (self) :
        return self.remove (self.tail)
    # end def pop

    def pop_front (self) :
        return self.remove (self.head)
    # end def pop_front

    def prepend (self, * items) :
        self._append (self._H, * items)
    # end def prepend

    def remove (self, item) :
        if item is self._H or item is self._T :
            raise IndexError, error
        item.prev.link_next (item.next)
        return item.value
    # end def remove

    def reverse_iter (self) :
        return self._T.predecessors ()
    # end def reverse_iter

    def reverse_values (self) :
        for item in self.reverse_iter () :
            yield item.value
    # end def reverse_values

    def values (self) :
        for item in iter (self) :
            yield item.value
    # end def values

    def __nonzero__ (self) :
        return self._H.next is not self._T
    # end def __nonzero__

# end class DL_List

class DL_List_Counted (DL_List) :
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

    def _append (self, p, * items) :
        self.__super._append (p, * items)
        self.count += len (items)
    # end def _append

    def clear (self) :
        self.__super.clear ()
        self.count = 0
    # end def clear

    def remove (self, item) :
        self.__super.remove (item)
        self.count -= 1
    # end def remove

    def __len__ (self) :
        return self.count
    # end def __len__

# end class DL_List_Counted

### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _doc_test () :
        import DL_List
        return U_Test.run_module_doc_tests (DL_List)
    # end def _doc_test

    def _test () :
        _doc_test  ()
    # end def _test

    if __name__ == "__main__" :
        _test ()
# end if __debug__

### end unit-test code ########################################################

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ DL_List
