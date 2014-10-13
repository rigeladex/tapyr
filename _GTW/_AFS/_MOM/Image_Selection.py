# -*- coding: utf-8 -*-
# Copyright (C) 2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.MOM.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.MOM.Image_Selection
#
# Purpose
#    Special field for adding support for the Image_Selection WYSIWYG editor.
#
# Revision Dates
#    29-Jan-2013 (MG) Creation
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _GTW._AFS._MOM           import Element
from   _JNJ                     import JNJ
import _JNJ.Templateer
from   _TFL.I18N                import _T

JNJ.Template \
    ( "afs_img_selection"
    , "html/AFS/img_selection.jnj"
    , parent_name = "afs_div_seq"
    )


class Image_Selection_Field (Element.Field) :
    """A field which allows the selection of an image"""

    renderer     = "afs_img_selection"

    def __init__ (self, * args, ** kw) :
        kw.setdefault ("elfinder", "/elfinder")
        kw.setdefault ("language", "en")
        self.__super.__init__ (* args,  ** kw)
    # end def __init__

# end class Image_Selection_Field

if __name__ != "__main__" :
    GTW.AFS.MOM._Export ("*")
### __END__ GTW.AFS.MOM.Image_Selection
