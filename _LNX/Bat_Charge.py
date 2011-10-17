# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    Bat_Charge
#
# Purpose
#    Provide information about battery charge
#
# Revision Dates
#    15-Feb-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _LNX           import LNX
from   _TFL           import TFL

from   _TFL           import sos
from   _TFL.predicate import first

import _TFL._Meta.Object
import _TFL.Record

class Field (TFL.Meta.Object) :
    """One field describing a battery."""

    def __init__ (self, name, sys_name = None) :
        self.name     = name
        self.sys_name = sys_name or name
    # end def __init__

    def __call__ (self, path) :
        try :
            with open (sos.path.join (path, self.sys_name)) as file :
                result = file.read ().strip ()
            return result
        except :
            pass
    # end def __call__

# end class Field

class Field_F (Field) :
    """A float-valued field describing a battery."""

    def __call__ (self, path) :
        result = self.__super.__call__ (path)
        if result :
            try :
                return float (result)
            except :
                return 0
    # end def __call__

# end class Field_F

class Bat_Charge (TFL.Meta.Object) :
    """Provide information about battery charge."""

    fields = \
        ( Field_F ("design_capacity")
        , Field_F ("last_full_capacity")
        , Field_F ("remaining_capacity")
        , Field_F ("remaining_charging_time")
        , Field_F ("remaining_running_time")
        , Field   ("bat_status", "state")
        )
    path   = "/sys/devices/platform/smapi/BAT"

    def __init__ (self, n = 4) :
        self.batteries = list (self._get_batteries (n))
        self.total     = self._get_total ()
    # end def __init__

    def _get_batteries (self, n) :
        p = self.path
        for i in range (n) :
            pi  = p + str (i)
            bat = TFL.Record \
                (percent = None, time = None, hours = None, minutes = None)
            if sos.path.isdir (pi) :
                for f in self.fields :
                    bat [f.name] = f (pi)
                fc = bat.full_capacity = \
                    bat.last_full_capacity or bat.design_capacity
                if fc and bat.remaining_capacity :
                    bat.percent = (bat.remaining_capacity / fc) * 100
                time = \
                    bat.remaining_charging_time or bat.remaining_running_time
                if time :
                    bat.time = t = int (time)
                    bat.hours, bat.minutes = divmod (t, 60)
                yield bat
    # end def _get_batteries

    def _get_total (self) :
        result = TFL.Record \
            (percent = None, time = None, hours = None, minutes = None)
        bats = self.batteries
        fcs = tuple (b.full_capacity for b in bats if b.full_capacity)
        rcs = tuple \
            (  b.remaining_capacity for b in bats
            if b.remaining_capacity
            )
        ts  = tuple (b.time for b in bats if b.time)
        result.full_capacity      = fc = sum (fcs) if fcs else None
        result.remaining_capacity = rc = sum (rcs) if rcs else None
        if fc and rc :
            result.percent = min ((rc / fc) * 100, 100.)
        result.time = t = sum (ts) if ts else None
        if t :
            result.hours, result.minutes = divmod (t, 60)
        result.bat_status = first \
            ( tuple (b.bat_status for b in bats if b.bat_status != "idle")
            or ("charged", )
            )
        return result
    # end def _get_total

    def __str__ (self) :
        result = []
        for i, b in enumerate (self.batteries) :
            result.append \
                ( "Battery #%d    : %12s, %6.2f%%, %2.2d:%2.2d, %7s / %7s"
                % ( i, b.bat_status
                  , b.percent or 0, b.hours or 0, b.minutes or 0
                  , b.remaining_capacity, b.full_capacity
                  )
                )
        t = self.total
        result.append \
            ( "All batteries : %12s, %6.2f%%, %2.2d:%2.2d, %7s / %7s"
            % ( t.bat_status
              , t.percent or 0, t.hours or 0, t.minutes or 0
              , t.remaining_capacity, t.full_capacity
              )
            )
        return "\n".join (result)
    # end def __str__

# end class Bat_Charge

if __name__ != "__main__" :
    LNX._Export ("*")
if __name__ == "__main__" :
    print Bat_Charge ()
### __END__ Bat_Charge
