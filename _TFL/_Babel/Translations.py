# -*- coding: utf-8 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.Babel.
#
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
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Babel.Translations
#
# Purpose
#    Add better support for singular/plural to babel.support.Translations
#
# Revision Dates
#    18-Jun-2010 (CT) Creation (factored from TFL.I18N)
#    ««revision-date»»···
#--

from   _TFL                    import TFL

import _TFL._Babel

import babel.support
import struct

class Translations (babel.support.Translations) :
    """Add better support for singular/plural"""

    def _parse (self, fp):
        """Slighly modifiey version of gettext.GNUTranslations._parse."""
        unpack   = struct.unpack
        filename = getattr (fp, "name", "")
        # Parse the .mo file header, which consists of 5 little endian 32
        # bit words.
        self._catalog = catalog = {}
        self.plural   = lambda n: int (n != 1) # germanic plural by default
        buf           = fp.read ()
        buflen        = len     (buf)
        # Are we big endian or little endian?
        magic = unpack ("<I", buf [:4]) [0]
        if magic == self.LE_MAGIC :
            version, msgcount, masteridx, transidx = unpack ("<4I", buf [4:20])
            ii = "<II"
        elif magic == self.BE_MAGIC:
            version, msgcount, masteridx, transidx = unpack (">4I", buf [4:20])
            ii = ">II"
        else:
            raise IOError (0, "Bad magic number", filename)
        # Now put all messages from the .mo file buffer into the catalog
        # dictionary.
        for i in xrange (0, msgcount):
            mlen, moff = unpack (ii, buf [masteridx : masteridx + 8])
            tlen, toff = unpack (ii, buf [transidx  : transidx  + 8])
            mend       = moff + mlen
            tend       = toff + tlen
            if mend < buflen and tend < buflen:
                msg  = buf [moff:mend]
                tmsg = buf [toff:tend]
            else:
                raise IOError (0, "File is corrupt", filename)
            # See if we're looking at GNU .mo conventions for metadata
            if not mlen :
                # Catalog description
                lastk = k = None
                for item in tmsg.splitlines ():
                    item = item.strip ()
                    if not item:
                        continue
                    if ":" in item :
                        k, v           = item.split (":", 1)
                        k              = k.strip ().lower ()
                        v              = v.strip ()
                        self._info [k] = v
                        lastk          = k
                    elif lastk :
                        self._info [lastk] += "\n" + item
                    if k == "content-type" :
                        self._charset = v.split ("charset=") [1]
                    elif k == "plural-forms" :
                        v           = v.split     (";")
                        plural      = v [1].split ("plural=") [1]
                        self.plural = c2py        (plural)
            # Note: we unconditionally convert both msgids and msgstrs to
            # Unicode using the character encoding specified in the charset
            # parameter of the Content-Type header.  The gettext documentation
            # strongly encourages msgids to be us-ascii, but some appliations
            # require alternative encodings (e.g. Zope's ZCML and ZPT).  For
            # traditional gettext applications, the msgid conversion will
            # cause no problems since us-ascii should always be a subset of
            # the charset encoding.  We may want to fall back to 8-bit msgids
            # if the Unicode conversion fails.
            if "\x00" in msg :
                # Plural forms
                msgid1, msgid2 = msg.split  ("\x00")
                tmsg           = tmsg.split ("\x00")
                if self._charset:
                    msgid1 = unicode (msgid1, self._charset)
                    msgid2 = unicode (msgid2, self._charset)
                    tmsg   = [unicode (x, self._charset) for x in tmsg]
                for i, msg in enumerate (tmsg) :
                    catalog [(msgid1, i)] = msg
                ### In addtion to the two keys to the catalog as well to be
                ### able to have access to the singular and the last plural
                ### translation as well
                catalog [msgid1] = tmsg [ 0]
                catalog [msgid2] = tmsg [-1]
            else:
                if self._charset :
                    msg       = unicode (msg,  self._charset)
                    tmsg      = unicode (tmsg, self._charset)
                catalog [msg] = tmsg
            # advance to next entry in the seek tables
            masteridx += 8
            transidx  += 8
    # end def _parse

# end class Translations

if __name__ != "__main__" :
    TFL.Babel._Export ("*")
### __END__ TFL.Babel.Translations
