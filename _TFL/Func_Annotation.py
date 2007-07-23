# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Daniel Albeseder <dal@tttech.com>
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ****************************************************************************
#
#++
# Name
#    TFL.Func_Annotation
#
# Purpose
#    Documents a function's or method's parameters and return value
#
# Revision Dates
#    26-Jun-2007 (DAL) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from _TFL    import TFL
from inspect import getargspec

def func_annotate (func, param_doc, return_doc = None) :
    """Annotates the parameters and the return value of a function similar
       to PEP3107 (proposed for Python 2.6) in the dictionary attribute
       `func_annotation` of the supplied function.
    """
    func.func_annotation     = {}
    args, varargs, kwargs, _ = getargspec (func)
    args                     = (  args
                               + ([varargs] if varargs else [])
                               + ([kwargs]  if kwargs  else [])
                               )

    if   isinstance (param_doc, dict) :
        for k, v in param_doc.items () :
            if k in args :
                func.func_annotation [k] = v
            else :
                raise ValueError, \
                   "'%s' not a parameter of function '%s'" % (k, func.__name__)
    elif isinstance (param_doc, list) or isinstance (param_doc, tuple) :
        assert len (args) == len (param_doc), (args, param_doc)
        for k, v in zip (args, param_doc) :
            func.func_annotation [k] = v
    else :
        raise TypeError

    if return_doc is not None :
        func.func_annotation ['return'] = return_doc
# end def func_annotate

func_annotate \
    (func_annotate, { "func":       "function or method to be annotated"
                    , "param_doc":  "parameters docstrings as list or tuple "
                                    "in order of parameters or as dictonary "
                                    "where the key is the parameter name and "
                                    "the value is the docstring for this "
                                    "parameter"
                    , "return_doc": "description of return value"
                    }
     )

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Func_Annotation
