# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2006 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
#    TFL.CDG.Table_Checker
#
# Purpose
#    Provide general functionality to check generated cdg tables
#
# Revision Dates
#    22-Feb-2007 (MZO) Creation
#    28-Mar-2007 (MZO) Creation .
#     8-May-2007 (MZO) Creation ..
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from    _TFL                    import TFL
from    _TTA                    import TTA
import  _TFL._Meta.Object
import  _TFL._Meta.M_Class
import  _TFL.predicate
import  _TFL._CDG.Bin_Block
import  sos

class File2Meta_Struct (TFL.Meta.Object) :

    def __init__ (self, ms, filename = "", text = "") :
        if filename :
            lines = self._readfile (filename)
        else :
            lines = text.split ("\n")
        ms = self._convert (lines, ms)
    # end def __init__

    def _convert (self, lines, ms) :
        ms_cls_names                = ms.classes.keys ()
        current_ms_cls_name         = None
        current_ms_cls              = None
        expected_ms_prefix          = ""
        expected_ms_struct_length   = 0
        for line in lines :
            line = line.strip ()
            is_ms_struct_start = [k for k in ms_cls_names if k in line]
            if line.startswith ("/*") :    # c- comment
                continue
            elif line.startswith ("#") :   # XXX check consistancy tag
                continue
            elif is_ms_struct_start :
                # `MHL_Partition_Config` is sub of `MHL_Partition_Config_Data`
                is_ms_struct_start = max (is_ms_struct_start)
                if current_ms_cls_name is not None :    # empty struct
                    assert len (ms.classes [current_ms_cls_name].extension) == 0
                    current_ms_cls_name = None          # same as in };
                assert current_ms_cls_name is None, (current_ms_cls_name, is_ms_struct_start)
                current_ms_cls_name = is_ms_struct_start
                prefix = line [:line.find (current_ms_cls_name)]
                if not expected_ms_prefix :
                    expected_ms_prefix = prefix
                assert prefix == expected_ms_prefix, \
                    (perfix,expected_ms_prefix, line)
                expected_ms_struct_length = 0           # XXX find [5]
            elif line.count ("{") >= 1 :   # XXX use re # array and struct start
                if current_ms_cls_name : # ignore removed struct
                    current_ms_cls = ms.classes [current_ms_cls_name] ()
                    n, v = self._line2values (line)
                    setattr (current_ms_cls, n, v)
            elif line.count ("};") == 1 :                # array end
                # XXXX
                # assert expected_ms_struct_length ==
                # len (ms.classes [current_ms_cls_name].extension)
                current_ms_cls_name = None
            elif line.count ("}") == 1 :                 # struct end
                current_ms_cls = None
            elif line.count (",") == 1 :                 # struct end
                if current_ms_cls_name : # ignore removed struct
                    n, v = self._line2values (line)
                    setattr (current_ms_cls, n, v)
            else :
                pass
        return ms
    # end def _convert

    def _readfile (self, filename) :
        f       = open (filename, "rU")
        lines   = f.readlines ()
        f.close ()
        return lines
    # end def _readfile

    def _line2values (self, line) :  # XXX use re instead of find
        comment = line [line.find ("/*") + 2: line.rfind ("*/")]
        pos = line.rfind ("{")
        if pos < 0 :
            pos = line.rfind (",")
        pos = pos or 0
        v = line [pos + 1: line.rfind ("/*")]
        v = v.strip ()
        try :
            v = int (v)
        except :
            pass
        return comment.strip (), v
    # end def _line2values

    def _write_ms (self, ms, filename) :
        c_code_creator = TFL.CDG.C_Code_Creator ()
        c_code_creator (TFL.SDG.C, ms, None, filename = filename)
    # end def _write_ms

# end class File2Meta_Struct

class M_Check_Rule (TFL.Meta.M_Class) :
    """Meta class for M_Check_Rule classes"""

    classes = {}

    def __init__ (cls, name, bases, dict) :
        super (M_Check_Rule, cls).__init__ (name, bases, dict)
        cls.classes [name] = cls
        cls.reset_extension ()
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result     = super (M_Check_Rule, cls).__call__ (* args, ** kw)
        cls.extension.append (result)
        result.id  = cls.count
        return result
    # end def __call__

    def reset_extension (cls) :
        cls.extension = []
        cls.count     = 0
    # end def reset_extension

# end class M_Check_Rule

class Check_Reference_Mixin (TFL.Meta.Object) :

    def _ref_to_index (self, text) :
        if isinstance (text, str) :  # c code
            assert text.startswith ("&"), text  # & (xy_buffer [  0])
            val_str = text [text.find ("[") + 1 : text.find ("]")]
        else :
            val_str = text         # bin
        return int (val_str)
    # end def _ref_to_index

    def _ref_to_ms_cls (self, ms, ref_sf) :
        cls = None
        for cls in ms.classes.itervalues () :
            ref = getattr (cls, "reference_field", None)
            if ref == ref_sf :
                break
        return cls
    # end def _ref_to_ms_cls

# end class Check_Reference_Mixin

class Check_Rule (Check_Reference_Mixin) :

    __metaclass__ =  M_Check_Rule

    def __call__ (self, fcl_ms, mhl_ms, app_data) :
        result = self._rule (fcl_ms, mhl_ms, app_data)
#        self._out (result)
        return result
    # end def __call__

    def _out (self, text) :
        if __debug__ :
            print "*" * 79
            print self.__class__, text
            print "*" * 79
    # end def _out

    def _rule (self, fcl_ms, mhl_ms, app_data) :
        return True
    # end def _rule

# end class Check_Rule

class Table_Checker (TFL.Meta.Object) :

    def _execute_checks (self, *args, **kw) :
        cr = Check_Rule ()
        cnt_ok  = 0
        cnt_nok = 0
        for name, rule_cls in cr.__class__.classes.iteritems () :
            rule = rule_cls ()
            result = rule (*args, **kw)
            if not result :
                print \
                    ( "Test failed (%s) %s"
                    % (name, rule.__doc__)
                    )
                cnt_nok += 1
            else :
                cnt_ok  += 1
        print "-" * 79 + "\n"
        print "Table_Checker Result: %s ok, %s failed" % (cnt_ok, cnt_nok)
        return (cnt_ok, cnt_nok)
    # end def _execute_checks

# end class Table_Checker

if __name__ != "__main__":
    TFL.CDG._Export ("*")
### __END__ TFL.CDG.Table_Checker
