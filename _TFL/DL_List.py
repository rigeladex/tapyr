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
#    ««revision-date»»···
#--

from   __future__  import generators

from   _TFL        import TFL

import _TFL._Meta.Object

class DL_Item (TFL.Meta.Object) :
    """Item in a doubly linked list"""

    _None = type ("Empty_Node", (), {})

    def __init__ (self, value = _None, next = None, prev = None) :
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

    def __nonzero__ (self) :
        return self.value is not self._None
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
       >>> dl.first
       0
       >>> dl.last
       4
    """

    def __init__ (self, * items) :
        self.head = h = DL_Item ()
        self.tail     = DL_Item (prev = h)
        self.append (* items)
    # end def __init__

    first = property (lambda s : s.head.next)
    last  = property (lambda s : s.tail.prev)

    def append (self, * items) :
        tail = self.tail
        for item in items :
            DL_Item (item, tail, tail.prev)
    # end def append

    def clear (self) :
        self.head.link_next (self.tail)
    # end def clear

    def __iter__ (self) :
        p = self.head
        while p.next :
            yield p.next
            p = p.next
    # end def __iter__

    def itervalues (self) :
        for item in iter (self) :
            yield item.value
    # end def itervalues

    def pop (self) :
        last   = self.last
        result = last.value
        if last.prev is not None :
            last.prev.link_next (self.tail)
        return result
    # end def pop

    def pop_front (self) :
        first  = self.first
        result = first.value
        if first.next is not None :
            self.head.link_next (first.next)
        return result
    # end def pop_front

    def prepend (self, * items) :
        p = self.head
        for item in items :
            p = DL_Item (item, p.next, p)
    # end def prepend

    def reverse_iter (self) :
        p = self.tail
        while p.prev :
            yield p.prev
            p = p.prev
    # end def reverse_iter

    def __nonzero__ (self) :
        return self.head.next is not self.tail
    # end def __nonzero__

# end class DL_List

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
