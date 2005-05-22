# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
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
#    PMA.Mailbox
#
# Purpose
#    Model a mailbox
#
# Revision Dates
#     3-Sep-2004 (CT) Creation
#     4-Sep-2004 (CT) Creation continued
#    12-Sep-2004 (CT) Creation continued...
#    15-Sep-2004 (CT) Creation continued....
#    19-Sep-2004 (CT) Creation continued.....
#    22-May-2005 (CT) `delete` added
#    22-May-2005 (CT) `_copy_msg_file` changed to use `message.save` instead
#                     of home-grown code
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib
import _PMA.Message
import _TFL._Meta.Object
import _TFL.B64 as B64

import Environment
from   predicate               import *
from   Record                  import Record
from   subdirs                 import subdirs

import cPickle                 as     pickle
import errno
import sos
import time

class _Mailbox_ (TFL.Meta.Object) :
    """Root class for mailbox classes"""

    messages           = property (lambda s : s._get_messages ())
    sub_boxes          = property (lambda s : s._box_dict.values ())

    _deliveries        = {} ### `time.time ()` : number of mails delivered

    def __init__ (self, path, name = None, prefix = None) :
        if name is None :
            name       = sos.path.split (path) [-1]
        if prefix is None :
            qname      = name
        else :
            qname      = "/".join ((prefix, name))
        self.name      = name
        self.qname     = qname
        self.path      = path
        self._box_dict = {}
        self._messages = None
        self._msg_dict = {}
        self._msg_stat = {}
        self._read_msg_status (path)
    # end def __init__

    def md_name (cls, message = None) :
        t = int (time.time ())
        p = sos.getpid ()
        n = cls._deliveries.setdefault (t, 0)
        h = Environment.hostname
        cls._deliveries [t] += 1
        return cls._md_name (t, p, n, h)
    md_name = classmethod (md_name)

    def sort (self, decorator = None) :
        if self._messages is None :
            self._get_messages () ### calls self._sort
        else :
            self._sort ()
    # end def sort

    def summary (self, format = "%-99.99s") :
        return "\n".join ([format % m.summary () for m in self.messages])
    # end def summary

    def _add (self, * messages) :
        if messages :
            md = self._msg_dict
            ms = self._msg_stat
            for m in messages :
                md [m.name] = m
                ms [m.name] = m.status
            self._messages = None
    # end def _add

    def _copy_msg_file (self, message, target) :
        message.save (target)
    # end def _copy_msg_file

    def _get_messages (self) :
        if self._messages is None :
            if not self._msg_dict :
                self._setup_messages ()
            self._messages = self._msg_dict.values ()
            self._sort ()
        return self._messages
    # end def _get_messages

    def _md_name (cls, t, p, n, h) :
        ### use `B64.itoa` to make name short enough to fit into 80-column
        ### xterm with `ls -l`
        return "%s.%s_%s.%s" % (B64.itoa (t), B64.itoa (p), B64.itoa (n), h)
    _md_name = classmethod (_md_name)

    def _new_message (self, m) :
        name = m._pma_path
        return PMA.Message \
            ( email   = m
            , name    = name
            , mailbox = self
            , status  = self._msg_stat.get (name)
            )
    # end def _new_message

    def _read_msg_status (self, path) :
        pass
    # end def _read_msg_status

    def _save_msg_status (self) :
        pass
    # end def _save_msg_status

    def _sort (self, decorator = None) :
        if decorator is None :
            decorator = lambda m : m.time
        self._messages = dusort (self._messages, decorator)
        for i, m in enumerate (self._messages) :
            m.number = i
    # end def _sort

    def __str__ (self) :
        return self.summary ()
    # end def __str__

    def __repr__ (self) :
        if self._messages is None :
            return "%s %s: %d sub-boxes" % \
                (self.__class__.__name__, self.path, len (self._box_dict))
        else :
            return "%s %s: %d messages, %d sub-boxes" % \
                ( self.__class__.__name__, self.path
                , len (self._messages), len (self._box_dict)
                )
    # end def __repr__

# end class _Mailbox_

class _Mailbox_in_Dir_ (_Mailbox_) :
    """Model directory-based mailbox"""

    def __init__ (self, path, prefix = None) :
        if not sos.path.isdir (path) :
            sos.mkdir (path)
        self.parser = Lib.Parser ()
        self.__super.__init__ (path, prefix = prefix)
        for s in self._subdirs (path) :
            self._new_subbox (s)
    # end def __init__

    def delete (self, * messages) :
        try :
            for m in messages :
                sos.unlink (m.path)
                del self._msg_dict [m.name]
                del self._msg_stat [m.name]
        finally :
            self._messages = None
    # end def delete

    def _copy_msg_file (self, message, target) :
        source = message.path
        try :
            sos.link (source, target)
        except OSError, exc :
            if exc.args [0] != errno.EXDEV :
                raise
            self.__super._copy_msg_file (message, target)
    # end def _copy_msg_file

    def _new_email (self, fp) :
        result = self.parser.parse (fp, headersonly = True)
        result._pma_parsed_body = False
        return result
    # end def _new_email

    def _new_subbox (self, path) :
        result = self.__class__ (path, prefix = self.qname)
        self._box_dict [result.name] = result
        return result
    # end def _new_subbox

    def _read_msg_status (self, path) :
        msp = self._msg_stat_path = sos.path.join (path, ".status")
        try :
            f = open (msp)
        except IOError :
            pass
        else :
            try :
                try :
                    msg_stat = pickle.load (f)
                except KeyboardInterrupt :
                    raise
                except StandardError :
                    pass
                else :
                    self._msg_stat = msg_stat
            finally :
                f.close ()
    # end def _read_msg_status

    def _save_msg_status (self) :
        if self._msg_stat :
            print "Saving message status", self.name
            f = open    (self._msg_stat_path, "wb")
            pickle.dump (self._msg_stat, f, pickle.HIGHEST_PROTOCOL)
            f.close     ()
    # end def _save_msg_status

    def _setup_messages (self) :
        self._add \
            (* [ self._new_message (m)
                 for m in self.MB_Type (self.path, self._new_email)
               ]
            )
    # end def _setup_messages

    def _subdirs (self, path) :
        return subdirs (path)
    # end def _subdirs

# end class _Mailbox_in_Dir_

class _Mailbox_in_Dir_S_ (_Mailbox_in_Dir_) :
    """Model simple directory-based mailbox"""

    def _new_email (self, fp) :
        result = self.__super._new_email   (fp)
        result._pma_path  = sos.path.split (fp.name) [1]
        result._pma_dir   = None
        return result
    # end def _new_email

    def _new_message (self, m) :
        result = self.__super._new_message (m)
        result.path = sos.path.join (self.path, result.name)
        return result
    # end def _new_message

# end class _Mailbox_in_Dir_S_

class _Mailbox_in_File_ (_Mailbox_) :
    """Model file-based mailbox"""

    def _new_email (self, fp) :
        result  = Lib.message_from_file (fp)
        result._pma_parsed_body = True
        self.n += 1
        result._pma_path = str (self.n)
        result._pma_dir  = None
        return result
    # end def _new_email

    def _setup_messages (self) :
        f = open (self.path, "r")
        self.n = 0
        try :
            self._add \
                (* [ self._new_message (m)
                     for m in self.MB_Type (f, self._new_email)
                   ]
                )
        finally :
            f.close ()
    # end def _setup_messages

# end class _Mailbox_in_File_

class Unix_Mailbox (_Mailbox_in_File_) :
    """Model a Unix style mailbox"""

    MB_Type = Lib.mailbox.UnixMailbox

# end class Unix_Mailbox

class MH_Mailbox (_Mailbox_in_Dir_S_) :
    """Model a MH style mailbox"""

    MB_Type = Lib.mailbox.MHMailbox

# end class MH_Mailbox

class Maildir (_Mailbox_in_Dir_) :
    """Model a Maildir style mailbox"""

    MB_Type = Lib.mailbox.Maildir

    def md_name (cls, message = None) :
        if message is None :
            return super (Maildir, cls).md_name ()
        else :
            r = cls.name_split (message.name)
            try :
                t = int (r.time)
            except (TypeError, ValueError) :
                t = int (time.time ())
            try :
                p = int (r.proc)
            except (TypeError, ValueError) :
                p = sos.getpid ()
            try :
                n = int (r.deli)
            except (TypeError, ValueError) :
                n = cls._deliveries.setdefault (t, 0)
                cls._deliveries [t] += 1
            return cls._md_name (t, p, n, r.host or Environment.hostname)
    md_name = classmethod (md_name)

    def name_split (cls, name) :
        """Return parts of `name`.

           The result is a Record with attributes `time`, `proc`, `deli`,
           `host`, and `flags`.
        """
        t, p, h = (name.split (".", 2) + [None, None]) [:3]
        p, d    = (p.split    ("_")    + [None])       [:2]
        h, i    = (h.split    (":")    + [None])       [:2]
        if i :
            if i.startswith ("2,") :
                i = i [2:]
            else :
                i = None
        return Record (time = t, proc = p, deli = d, host = h, info = i)
    name_split = classmethod (name_split)

    def _new_email (self, fp) :
        result = self.__super._new_email (fp)
        d, n   = sos.path.split (fp.name)
        _, d   = sos.path.split (d)
        result._pma_path  = n
        result._pma_dir   = d
        return result
    # end def _new_email

    def _new_message (self, m) :
        result = self.__super._new_message (m)
        result.path = sos.path.join (self.path, "cur", result.name)
        return result
    # end def _new_message

    def _setup_messages (self) :
        self.__super._setup_messages ()
        join = sos.path.join
        path = self.path
        for m in self._msg_dict.itervalues () :
            if m.email._pma_dir == "new" :
                n = "%s:2," % (m.name, )
                s = join   (path, "new", m.name)
                t = join   (path, "cur", n)
                sos.link   (s, t)
                sos.unlink (s)
                m.name           = n
                m.email._pma_dir = "cur"
                m.path           = join (path, "cur", n)
    # end def _setup_messages

    def _subdirs (self, path) :
        ### XXX for nested subfolders this doesn't work properly
        ### XXX don't want to waste time on that braindead scheme right now
        return [d for d in self.__super._subdirs (path) if d.startswith (".")]
    # end def _subdirs

# end class Maildir

class Mailbox (_Mailbox_in_Dir_S_) :
    """Model PMA-style mailbox which is like a MH_Mailbox with a variant of
       Maildir-like messages naming.
    """

    def MB_Type (cls, path, factory) :
        for f in sos.listdir_full (path) :
            if not (f.startswith (".") or sos.path.isdir (f)) :
                fp = open (f)
                try :
                    m = factory (fp)
                finally :
                    fp.close ()
                yield m
    MB_Type = classmethod (MB_Type)

    def add_messages (self, * messages) :
        if self._messages is None :
            ### get messages from disk first
            self._get_messages ()
        for message in messages :
            old_box = message.mailbox
            if old_box is not None :
                name = old_box.md_name (message)
            else :
                name = self.md_name    (message)
            new_m = PMA.Message \
                ( email   = message.email
                , name    = name
                , mailbox = self
                , status  = message.status
                )
            self._add (new_m)
            old_box._copy_msg_file (message, sos.path.join (self.path, name))
    # end def add_messages

    def add_subbox (self, b, transitive = False) :
        print "Adding sub-box", b.qname
        if b.name in self._box_dict :
            s = self._box_dict  [b.name]
        else :
            s = self._new_subbox (sos.path.join (self.path, b.name))
        s.add_messages (* b.messages)
        if transitive :
            for sb in b._box_dict.itervalues () :
                s.add_subbox (sb, transitive)
    # end def add_subbox

    def import_from_mailbox (self, mailbox, transitive = False) :
        self.add_messages (* mailbox.messages)
        if transitive :
            for b in mailbox._box_dict.itervalues () :
                self.add_subbox (b, transitive)
    # end def import_from_mailbox

    def md_name (self, message = None) :
        if message is None :
            return super (Mailbox, cls).md_name ()
        else :
            return message.name
    # end def md_name

# end class Mailbox

"""
from   _PMA                    import PMA
import _PMA.Mailbox
#mb=PMA.Maildir ("/swing/private/.Tanzer/Maildir")
mb=PMA.Maildir ("/tmp/Maildir")
mb=PMA.Unix_Mailbox ("/var/mail/appoyer")
mb=PMA.MH_Mailbox ("/swing/private/tanzer/MH/CT")
mb=PMA.MH_Mailbox ("/swing/private/tanzer/MH/inbox")
print mb.summary ().encode ("iso-8859-1", "replace")
m = mb.messages [-3]
mb=PMA.MH_Mailbox ("/swing/private/tanzer/MH/inbox")
m = mb.messages [60]
print u"\n".join (list (m.formatted ()) [:100]).encode ("iso-8859-1", "replace")
print u"\n".join (m.formatted ()).encode ("iso-8859-1", "replace")
m = mb.messages [-3]
tb = PMA.Mailbox ("/swing/private/tanzer/PMA/S")
tb.import_from_mailbox (mb, transitive = True)
tb.add_messages (m)
print tb.summary ().encode ("iso-8859-1", "replace")
sb = mb.sub_boxes[0]

"""

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Mailbox
