# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.Password_Hasher
#
# Purpose
#    Library of password hashers
#
# Revision Dates
#     5-Jan-2013 (CT) Creation
#     6-Jan-2013 (CT) Fix `Bcrypt.verify`
#     1-May-2013 (CT) Change to use `passlib` instead of `bcrypt`
#     2-May-2013 (CT) Use `hash_cmp` to `verify`
#     5-May-2013 (CT) Test `bcrypt` before defining `Bcrypt`
#                     (passlib fails *after* import if bcrypt's c-extension
#                     is AWOL)
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
#    28-May-2013 (CT) Use `@subclass_responsibility` instead of home-grown code
#    25-Jun-2013 (CT) Make doctest Python-2.6 compatible
#    12-Oct-2014 (CT) Use `TFL.Secure_Hash`
#    ««revision-date»»···
#--

from   __future__          import absolute_import, division
from   __future__          import print_function, unicode_literals

from   _TFL                import TFL

from   _TFL._Meta          import Meta
from   _TFL.Decorator      import subclass_responsibility
from   _TFL.portable_repr  import portable_repr
from   _TFL.pyk            import pyk

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.Secure_Hash

import binascii
import uuid

class M_Password_Hasher (Meta.Object.__class__) :
    """Meta class for password hashers"""

    Table = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "Password_Hasher" and not name.startswith ("_") :
            cls._m_add (name, cls.Table)
            cls.name = name
    # end def __init__

    @TFL.Meta.Once_Property
    def default (cls) :
        return max \
            ((t for t in pyk.itervalues (cls.Table)), key = lambda t : t.rank)
    # end def default

    def _m_add (cls, name, Table) :
        name = pyk.text_type (name)
        assert name not in Table, "Name clash: `%s` <-> `%s`" % \
            (name, Table [name].__class__)
        Table [name] = cls
    # end def _m_add

    def __getattr__ (cls, name) :
        try :
            return cls.Table [name]
        except KeyError :
            raise AttributeError (name)
    # end def __getattr__

    def __getitem__ (cls, key) :
        return cls.Table [key]
    # end def __getitem__

# end class M_Password_Hasher

class M_Password_Hasher_SHA (M_Password_Hasher) :
    """Meta class for password hashers using secure hash algorithms."""

    @TFL.Meta.Once_Property
    def Hasher (cls) :
        return getattr (TFL.Secure_Hash, cls.__name__)
    # end def Hasher

    @TFL.Meta.Once_Property
    def rank (cls) :
        return cls.Hasher ().digest_size
    # end def rank

# end class M_Password_Hasher_SHA

class Password_Hasher (Meta.BaM (Meta.Object, metaclass = M_Password_Hasher)) :
    """Base class for password hashers

    >>> pr = "Ao9ug9wahWae"
    >>> ph = Password_Hasher.hashed (pr, "salt") # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    NotImplementedError: Password_Hasher must implement method ...

    >>> Password_Hasher.verify (pr, pr) # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    NotImplementedError: Password_Hasher must implement method ...

    """

    def __init__ (self, * args, ** kw) :
        raise TypeError ("Cannot instantiate %s" % (self.__class__, ))
    # end def __init__

    @subclass_responsibility
    @classmethod
    def hashed (cls, clear_password, salt = None) :
        """Hashed value of `clear_password` using `salt`"""
    # end def hashed

    @classmethod
    def salt (cls, * args, ** kw) :
        return uuid.uuid4 ().hex
    # end def salt

    @subclass_responsibility
    @classmethod
    def verify (cls, clear_password, hashed_password) :
        """True if `clear_password` and `hashed_password` match"""
    # end def verify

# end class Password_Hasher

class _Password_Hasher_SHA_ \
          (Meta.BaM (Password_Hasher, metaclass = M_Password_Hasher_SHA)) :
    """Password Hasher based on secure hash algorithm"""

    sep           = b"::"

    @classmethod
    def hashed (cls, clear_password, salt = None) :
        """Hashed value of `clear_password` using `salt`"""
        Hasher = cls.Hasher
        if salt is None :
            salt = cls.salt ()
        salt   = Hasher._encoded  (salt)
        hashed = binascii.hexlify (Hasher.pbkdf2_hmac (clear_password, salt))
        return cls.sep.join       ((salt, hashed))
    # end def hashed

    @classmethod
    def verify (cls, clear_password, hashed_password) :
        """True if `clear_password` and `hashed_password` match"""
        try :
            salt, _ = hashed_password.split (cls.sep, 1)
        except Exception :
            return False
        else :
            return cls.Hasher.compare_hexdigest \
                (hashed_password, cls.hashed (clear_password, salt))
    # end def verify

# end class _Password_Hasher_SHA_

class sha224 (_Password_Hasher_SHA_) :
    """Password Hasher using `sha224` for hashing.

    >>> pr = "Ao9ug9wahWae"
    >>> ph = Password_Hasher.sha224.hashed (pr, "salt")
    >>> print (portable_repr (ph))
    'salt::373ea460b8c323c468673a3702d7f0a90214dd48414bfa6cb7a639c4'

    >>> Password_Hasher.sha224.verify (pr, ph)
    True
    >>> Password_Hasher.sha224.verify (pr, pr)
    False
    >>> Password_Hasher.sha224.verify (ph, pr)
    False

    """

# end class sha224

try :
    from passlib.hash import bcrypt
    bcrypt.encrypt ("123", rounds = 4)
except Exception :
    pass
else :
    class Bcrypt (Password_Hasher) :
        """Password Hasher using bcrypt

        ### `salt` set to some random value extracted from a b-crypted password
        >>> salt = bcrypt.normhash ("WCXrf6O517rQFabeyr7xtO")

        >>> pr = "Ao9ug9wahWae"
        >>> ph = Password_Hasher.Bcrypt.hashed (pr, salt)
        >>> print (ph)
        $2a$12$WCXrf6O517rQFabeyr7xtOb3t0GkVQzCYFjPZvAQ237y2C3TL.XcO

        >>> Password_Hasher.Bcrypt.verify (pr, ph)
        True
        >>> Password_Hasher.Bcrypt.verify (pr, salt)
        False
        >>> Password_Hasher.Bcrypt.verify (pr, pr)
        False

        """

        default_rounds = 12
        rank           = 10000

        @classmethod
        def hashed (cls, clear_password, salt = None) :
            """Hashed value of `clear_password` using `salt`"""
            return bcrypt.encrypt \
                (clear_password, rounds = cls.default_rounds, salt = salt)
        # end def hashed

        @classmethod
        def verify (cls, clear_password, hashed_password) :
            """True if `clear_password` and `hashed_password` match"""
            try :
                return bcrypt.verify (clear_password, hashed_password)
            except Exception :
                return False
        # end def verify

    # end class Bcrypt

if __name__ != "__main__" :
    TFL._Export ("Password_Hasher")
### __END__ TFL.Password_Hasher
