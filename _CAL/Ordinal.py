# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    CAL.Ordinal
#
# Purpose
#    Support the use of ordinal numbers for weeks, months etc.
#
# Revision Dates
#     3-Jan-2007 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _CAL                    import CAL
import _CAL.Date
import _TFL._Meta.Object

class Month (TFL.Meta.Object) :
    """Ordinal numbers for months."""

    @classmethod
    def to_date (cls, mo) :
        """Return date corresponding to month ordinal `mo`."""
        y, m = divmod (mo, 12)
        return CAL.Date (y, m or 12, 1)
    # end def to_date

    @classmethod
    def to_ordinal (cls, d) :
        """Return month ordinal for date `d`."""
        return d.year * 12 + d.month
    # end def to_ordinal

# end class Month

class Week (TFL.Meta.Object) :
    """Ordinal numbers for weeks"""

    @classmethod
    def to_date (cls, wo) :
        """Return date corresponding to week ordinal `wo`."""
        return CAL.Date.from_ordinal (wo * 7 + 1)
    # end def to_date

    @classmethod
    def to_ordinal (cls, d) :
        """Return week ordinal for date `d`."""
        return d.wk_ordinal
    # end def to_ordinal

# end class Week

class Year (TFL.Meta.Object) :
    """Ordinal numbers for years."""

    @classmethod
    def to_date (cls, yo) :
        """Return date corresponding to year ordinal `yo`."""
        return CAL.Date (yo, 1, 1)
    # end def to_date

    @classmethod
    def to_ordinal (cls, d) :
        """Return year ordinal for date `d`."""
        return d.year
    # end def to_ordinal

# end class Year

if __name__ == "__main__" :
    CAL._Export_Module ()
### __END__ CAL.Ordinal
