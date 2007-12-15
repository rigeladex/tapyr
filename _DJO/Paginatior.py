# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2007 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin.glueck@gmail.com
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
#    DJO.Paginatior
#
# Purpose
#    Pagination object which extends the django version with the `page_range`
#    and some other properties used in the templates.
#
# Revision Dates
#    29-May-2007 (MG) Creation
#    15-Dec-2007 (MG) Missing import added
#    ««revision-date»»···
#--
#
from   django.core.paginator      import ObjectPaginator

class Paginatior (ObjectPaginator) :
    """Simple extension of the ObjectPaginator"""
    _page_numbers    = None
    results_per_page = property (lambda s : s.num_per_page)
    next             = property (lambda s : s.page + 1)
    previous         = property (lambda s : s.page - 1)
    has_next         = property (lambda s : s.has_next_page     (s.page - 1))
    has_previous     = property (lambda s : s.has_previous_page (s.page - 1))
    show_first       = property (lambda s : 1       not in s.page_numbers)
    show_last        = property (lambda s : s.pages not in s.page_numbers)

    def __init__ ( self, query_set, num_per_page
                 , orphans        = 0
                 , adjecent_pages = 0
                 ) :
        super (Paginatior, self).__init__ (query_set, num_per_page, orphans)
        self.adjecent_pages = adjecent_pages
    # end def __init__

    def get_page (self, page_number) :
        self.objects       = super (Paginatior, self).get_page \
            (page_number - 1)
        self.page          = page_number
        self._page_numbers = None
        return self.objects
    # end def get_page

    def page_numbers (self) :
        if self._page_numbers is None :
            pages              = self.pages
            page               = self.page
            adjecent           = self.adjecent_pages
            self._page_numbers = \
                [ p for p in range (page - adjecent, page + adjecent + 1)
                    if (p > 0) and  (p <= pages)
                ]
        return self._page_numbers
    # end def page_numbers
    page_numbers     = property (page_numbers)
# end class Paginatior

if __name__ != "__main__" :
    from _DJO import DJO
    DJO._Export ("*")
### __END__ DJO.Paginatior
