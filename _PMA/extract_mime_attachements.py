# -*- coding: utf-8 -*-
# Copyright (C) 2019 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    PMA.extract_mime_attachements
#
# Purpose
#    Extract specified MIME attachement from mail message(s)
#
# Revision Dates
#    19-Aug-2019 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _TFL                    import TFL
from   _PMA                    import PMA

from   _TFL.Filename           import *
from   _TFL.pyk                import pyk
from   _TFL.Re_Filter          import Re_Filter, re
from   _TFL                    import sos

import _PMA.Message
import _TFL.CAO

_is_false = lambda x : False

def extract_mime_attachements \
        ( msg, directory
        , def_ext      = None
        , ignore       = _is_false
        , main_type    = _is_false
        , name_pat     = _is_false
        , part_indices = None
        , sub_type     = _is_false
        ) :
    if def_ext and not def_ext.startswith (".") :
        def_ext    = "." + def_ext
    if not part_indices :
        part_indices   = pyk.range (len (msg.parts))
    for i in part_indices :
        p          = msg.parts [i]
        specified  = (not ignore (p.content_type)) and \
            (  main_type (p.main_type)
            or name_pat  (p.filename)
            or sub_type  (p.sub_type)
            )
        if specified :
            name   = p.filename or ("%s_%s" % (msg.name, i))
            fn     = Filename (directory, name).name
            if def_ext :
                fn = Filename (def_ext, fn).name
            print ("    Saving", name)
            PMA.save (fn, p.body)
        elif p.main_type in ("multipart", "message") :
            extract_mime_attachements \
                ( p, directory
                , def_ext, ignore, main_type, name_pat, part_indices, sub_type
                )
# end def extract_mime_attachements

def _main (cmd) :
    msg_base_dirs  = cmd.msg_base_dirs or PMA.msg_base_dirs
    directory      = cmd.directory
    if directory and not directory.endswith (sos.sep) :
        directory  = directory + sos.sep
    c_type     = cmd.content_type
    def_ext    = cmd.extension_default
    ignore     = cmd.ignore   or None
    name_pat   = cmd.name_pat or None
    parts      = cmd.Parts
    s_type     = cmd.sub_type
    if not cmd.regexp :
        if c_type :
            c_type = re.escape (c_type)
        if s_type :
            s_type = re.escape (s_type)
    c_type     = Re_Filter (c_type)   if c_type   else _is_false
    s_type     = Re_Filter (s_type)   if s_type   else _is_false
    ignore     = Re_Filter (ignore)   if ignore   else _is_false
    name_pat   = Re_Filter (name_pat) if name_pat else _is_false
    for msg in PMA.messages_from_args (cmd.argv, msg_base_dirs) :
        print (msg.path)
        extract_mime_attachements \
            (msg, directory, def_ext, ignore, c_type, name_pat, parts, s_type)
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "message:S?Message(s) to extract MIME attachements from"
        ,
        )
    , opts          =
        ( "-content_type:S?Type of attachements to extract"
        , "-directory:P=~/scratch?"
            "Name of directory to put the attachements into"
        , "-extension_default:S"
            "?Default extension to use for extracted attachements"
        , "-ignore:S?Types to ignore (regular expression)"
        , "-msg_base_dirs:Q:?Base directories for searching `message`"
        , "-name_pat:S?Regular expression for attachement names to extract"
        , "-Parts:I,?"
            "Specifies which parts of the mail to extract "
            "(default: all).\nThis must be a list of indices."
        , "-regexp:B?Interpret `content-type' and `sub_type` as regular expression"
        , "-sub_type:S?Subtype of attachements to extract"
        )
    , description   = "Format mail messages for viewing and printing"
    )

if __name__ != "__main__" :
    PMA._Export ("*")
else :
    PMA.load_user_config  ()
    _Command              ()
### __END__ PMA.extract_mime_attachements
