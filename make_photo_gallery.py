# -*- coding: utf-8 -*-
# Copyright (C) 2008-2014 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
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
#    14-Jan-2011 (CT) `-format`, `-color`, `-x_off`, and `-y_off` added
#    16-Jun-2013 (CT) Use `TFL.CAO`, not `TFL.Command_Line`
#     1-Oct-2014 (CT) Add `fix_rotation`
#    ««revision-date»»···
#--

from   _CAL.Date          import Date

from   _TFL               import TFL
from   _TFL               import sos
from   _TFL.Filename      import *
from   _TFL.Regexp        import Regexp, re

import _TFL.CAO
import _TFL.FCM

import warnings
warnings.filterwarnings ("ignore", module = "^PIL.*")
warnings.filterwarnings \
    ( "ignore", "in 3.x, __getslice__ has been removed; use __getitem__")

from   PIL import Image, ImageDraw, ImageFile, ImageFont, ExifTags

try :
    import plumbum
except ImportError :
    plumbum = None

### http://mail.python.org/pipermail/image-sig/1999-August/000816.html
### to avoid exception
###     IOError: encoder error -2 when writing image file

ImageFile.MAXBLOCK = 1000000 # default is 64k

_rotate_pat = Regexp (r"Rotate\s+(?P<angle>\d+)\s+CW")

def convert_one \
        ( src, name, i_size, t_size, holder, year, font, imp, thp
        , format, color, x_off, y_off
        , temp_dir = None
        ) :
    f_src = fix_rotation (src, temp_dir)
    im    = Image.open   (f_src)
    th    = im.copy      ()
    im.thumbnail (i_size, Image.ANTIALIAS)
    th.thumbnail (t_size, Image.ANTIALIAS)
    if holder :
        xo   = x_off if x_off > 0 else im.size [0] + x_off
        yo   = y_off if y_off > 0 else im.size [1] + y_off
        draw = ImageDraw.Draw (im)
        draw.text \
            ((xo, yo), "(C) %s %s" % (year, holder), fill = color, font = font)
    print (name, im.size, th.size)
    im.save (imp, format, progressive = True)
    th.save (thp, format, progressive = True)
# end def convert_one

def fix_rotation (src, temp_dir) :
    result = src
    if plumbum is not None :
        pbl     = plumbum.local
        rot_pat = _rotate_pat
        jt_rot  = pbl ["jpegtran"] \
            ["-copy", "all", "-perfect", "-optimize", "-rotate"]
        xt      = pbl ["exiftool"] ["-Orientation"]
        orient  = xt (src)
        if rot_pat.search (orient) :
            angle  = rot_pat.angle
            result = Filename (Filename (src).base_ext, default_dir = temp_dir).name
            cmd    = jt_rot [str (angle), src] > result
            cmd ()
    return result
# end def fix_rotation

def _main (cmd) :
    font   = ImageFont.load_default ()
    color  = cmd.color
    fmt    = cmd.format
    ext    = fmt.lower ()
    if ext == "jpeg" :
        ext = "jpg"
    holder = cmd.photographer
    x_off  = cmd.x_off
    y_off  = cmd.y_off
    year   = cmd.year
    i_size = cmd.i_size, cmd.i_size
    t_size = cmd.t_size, cmd.t_size
    td     = sos.expanded_path (cmd.target_dir)
    with TFL.temp_dir () as temp_dir :
        if cmd.add_to_dir :
            if not sos.path.isdir (td) :
                print ("Making directory %s" % (td, ))
                sos.mkdir_p (td)
            for src in cmd.argv [1:] :
                src, name = src.split ("=")
                if not name :
                    name = src
                name = Filename (name).base
                imp  = sos.path.join (td, "%s_im.%s" % (name, ext))
                thp  = sos.path.join (td, "%s_th.%s" % (name, ext))
                convert_one \
                    ( src, name, i_size, t_size, holder, year, font, imp, thp
                    , fmt, color, x_off, y_off
                    , temp_dir
                    )
        else :
            td_im = sos.path.join (td, "im")
            td_th = sos.path.join (td, "th")
            for x in td_im, td_th :
                if not sos.path.isdir (x) :
                    print ("Making directory %s" % (x, ))
                    sos.mkdir_p (x)
            pid  = cmd.start_pid
            for src in sorted (sos.expanded_globs (* cmd.argv [1:])) :
                pid  += 1
                name  = "%04d.%s" % (pid, ext)
                imp   = sos.path.join (td_im, name)
                thp   = sos.path.join (td_th, name)
                convert_one \
                    ( src, name, i_size, t_size, holder, year, font, imp, thp
                    , fmt, color, x_off, y_off
                    , temp_dir
                    )
# end def _main

today = Date ()
year  = today.year

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "target_dir:P?Directory to put gallery into"
        , "picture:P?Name of picture(s) to convert and put into `target_dir`"
        )
    , opts          =
        ( "add_to_dir:B"
            "?Add pictures to existing directory "
            "(no `im` and `th` subdirectories)"
        , "color:S=white?Color to use for copyright notice"
        , "format:S=JPEG?Image format used for output"
        , "i_size:I=800?Size of images in gallery (larger dimension)"
        , "photographer:S?Name of photographer"
        , "start_pid:I=0?Start value for picture count"
        , "t_size:I=150?Size of thumbnails in gallery (larger dimension)"
        , "x_off:I=5?X offset of copyright notice"
        , "y_off:I=-15?Y offset of copyright notice"
        , "-year:I=%s?Year for copyright" % (year, )
        )
    , min_args      = 2
    )

if __name__ == "__main__" :
    _Command ()
### __END__ make_photo_gallery
