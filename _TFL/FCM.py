# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.FCM
#
# Purpose
#    Provide context managers for handling files safely
#
# Revision Dates
#    18-Mar-2009 (CT) Creation
#    ««revision-date»»···
#--

from   __future__          import with_statement

from   _TFL                import TFL
from   _TFL                import sos

import _TFL.Decorator

import errno
import tempfile

@TFL.Contextmanager
def open_fsynced (file_name, mode = "w", buffering = -1) :
    """Context manager that opens `file_name` and will `fsync` it before
       closing.
    """
    with open (file_name, mode, buffering) as file :
        try :
            yield file
        finally :
            file.flush ()
            sos.fsync  (file.fileno ())
# end def open_fsynced

@TFL.Contextmanager
def open_tempfile (mode = "w", buffering = -1, suffix = "", prefix = "", dir = "", auto_remove = True, create_dir = False) :
    """Context manager that opens a temporary file."""
    if create_dir and not sos.path.isdir (dir) :
        sos.mkdir (dir)
    fd, temp_name = tempfile.mkstemp \
        (suffix = suffix, prefix = prefix, dir = dir, text = "t" in mode)
    try :
        file = sos.fdopen (fd, mode, buffering)
    except :
        sos.close  (fd)
        sos.remove (temp_name)
        raise
    else :
        try :
            try :
                yield (file, temp_name)
            except :
                if sos.path.exists (temp_name) :
                    sos.remove (temp_name)
                raise
        finally :
            if not file.closed :
                file.close ()
            if auto_remove and sos.path.exists (temp_name) :
                sos.remove (temp_name)
# end def open_tempfile

@TFL.Contextmanager
def open_to_replace (file_name, mode = "w", buffering = -1, backup_name = None) :
    """Context manager that opens a file with a temporary name and renames it
       to `file_name` after syncing and closing. If `backup_name` is
       specified, the old file is renamed to `backup_name`.
    """
    dir, name = sos.path.split (file_name)
    with open_tempfile (mode, buffering, prefix = name, dir = dir) as \
             (file, temp_name) :
        yield file
        file.flush ()
        sos.fsync  (file.fileno ())
        file.close ()
        if backup_name :
            try :
                sos.rename (file_name, backup_name)
            except sos.error, exc :
                if exc.args [0] != errno.ENOENT :
                    traceback.print_exc ()
        sos.rename (temp_name, file_name)
# end def open_to_replace

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.FCM
