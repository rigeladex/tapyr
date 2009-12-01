# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2009 Mag. Christian Tanzer. All rights reserved
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
#    make_photo_gallery
#
# Purpose
#    Make a photo gallery
#
# Revision Dates
#     7-May-2008 (CT) Creation
#     8-May-2008 (CT) `-year` added
#     8-May-2008 (CT) Set `ImageFile.MAXBLOCK` to avoid IOError during `save`
#    20-Mar-2009 (CT) `convert_one` factored and `-add_to_dir` added
#     1-Dec-2009 (CT) Ignore `__getslice__` warnings
#    ««revision-date»»···
#--

from   _TFL               import TFL
from   _TFL               import sos
from   _TFL.Filename      import *


from   PIL import Image, ImageDraw, ImageFile, ImageFont, ExifTags

### http://mail.python.org/pipermail/image-sig/1999-August/000816.html
### to avoid exception
###     IOError: encoder error -2 when writing image file

ImageFile.MAXBLOCK = 1000000 # default is 64k

def convert_one (src, name, i_size, t_size, holder, year, font, imp, thp) :
    im = Image.open (src)
    th = im.copy    ()
    im.thumbnail    (i_size, Image.ANTIALIAS)
    th.thumbnail    (t_size, Image.ANTIALIAS)
    if holder :
        draw = ImageDraw.Draw (im)
        draw.text \
            ((5, im.size [1] - 15), "(C) %s %s" % (year, holder), font=font)
    print name, im.size, th.size
    im.save (imp, "JPEG", progressive = True)
    th.save (thp, "JPEG", progressive = True)
# end def convert_one

def command_spec (arg_array = None) :
    from _TFL.Command_Line import Command_Line
    from _CAL.Date         import Date
    today = Date ()
    year  = today.year
    return Command_Line \
        ( arg_spec    =
            ( "target_dir:P?Directory to put gallery into"
            , "picture:P"
                "?Name of picture(s) to convert and put into `target_dir`"
            )
        , option_spec =
            ( "add_to_dir:B"
                "?Add pictures to existing directory (no `im` and `th` subdirectories)"
            , "photographer:S?Name of photographer"
            , "i_size:I=800?Size of images in gallery (larger dimension)"
            , "t_size:I=150?Size of thumbnails in gallery (larger dimension)"
            , "start_pid:I=0?Start value for picture count"
            , "-year:I=%s?Year for copyright" % (year, )
            )
        , min_args    = 2
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    font   = ImageFont.load_default ()
    holder = cmd.photographer
    year   = cmd.year
    i_size = cmd.i_size, cmd.i_size
    t_size = cmd.t_size, cmd.t_size
    td     = sos.expanded_path (cmd.target_dir)
    if cmd.add_to_dir :
        if not sos.path.isdir (td) :
            print "Making directory %s" % (td, )
            sos.mkdir_p (td)
        for src in cmd.argv [1:] :
            src, name = src.split ("=")
            if not name :
                name = src
            name = Filename (name).base
            imp  = sos.path.join (td, "%s_im.jpg" % name)
            thp  = sos.path.join (td, "%s_th.jpg" % name)
            convert_one \
                (src, name, i_size, t_size, holder, year, font, imp, thp)
    else :
        td_im = sos.path.join (td, "im")
        td_th = sos.path.join (td, "th")
        for x in td_im, td_th :
            if not sos.path.isdir (x) :
                print "Making directory %s" % (x, )
                sos.mkdir_p (x)
        pid  = cmd.start_pid
        for src in sorted (sos.expanded_globs (* cmd.argv [1:])) :
            pid  += 1
            name  = "%04d.jpg" % pid
            imp   = sos.path.join (td_im, name)
            thp   = sos.path.join (td_th, name)
            convert_one \
                (src, name, i_size, t_size, holder, year, font, imp, thp)
# end def main

import warnings
warnings.filterwarnings \
    ( "ignore", "in 3.x, __getslice__ has been removed; use __getitem__")

if __name__ == "__main__" :
    main (command_spec ())
### __END__ make_photo_gallery
