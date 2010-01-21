# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This module is part of the package TFL.
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
#    TFL.Babel
#
# Purpose
#    Some extension for the translation system Babel
#
# Revision Dates
#    20-Jan-2010 (MG) Creation
#    21-Jan-2010 (MG) Option to ignore files added
#    21-Jan-2010 (MG) Doc strings are only added specified in the options.
#                     Indent of doc strings is normalized
#    21-Jan-2010 (MG) Command interface added
#    21-Jan-2010 (MG) `Translations` replaced by `Existing_Translations`
#    ««revision-date»»···
#--

from   _TFL           import TFL
import _TFL._Babel.Extract
import _TFL._Babel.Config_File
import _TFL.CAO
import  os

def _add_option (cmd_line, * options) :
    cmd_line.extend (options)
# end def _add_option

def _prefix_path (filename, * prefix) :
    if not os.path.isabs (filename) :
        prefix   = prefix + (filename, )
        filename = os.path.abspath (os.path.join (* prefix))
    return filename
# end def _prefix_path

def extract (cmd) :
    for base_dir in cmd.argv :
        config        = TFL.Babel.Config_File \
            (_prefix_path (cmd.extraction_config, base_dir))
        template_file = _prefix_path (cmd.template_file,     base_dir, "-I18N")
        keywords      = cmd.keywords
        TFL.Babel.Extract (base_dir, template_file, config, cmd)
# end def extract


Extract = TFL.CAO.Cmd \
    ( extract
    , name = "extract"
    , args =
        ( "directories:P"
            "?Directories where the extraction should start"
        ,
        )
    , opts =
        ( "bugs_address:S=bugs@domain.com?"
            "Email address to report translation bugs"
        , "charset:S=utf-8?Encoding for the pot file"
        , "copyright_holder:S=Company?Copyright holer"
        , "extraction_config:S=babel.cfg?"
            "Name of the extraction config fileconfig"
        , "keywords:S,?Additional extraction keyowrds"
        , "no_location:B?Suppress the location information"
        , "omit_header:B?Omit the header in the POT file"
        , "sort:B?Generated template should be alphabetical sorted"
        , "strip_comment_tags:B?Strip the comment tags"
        , "project:S=Project?Name of the project/application"
        , "template_file:P=template.pot?Name of the template file"
        , "version:S=1.0?Product version"
        , "width:I=76?Output with in the POT file"
        )
    , min_args = 1
    )

def language (cmd) :
    """Create or update the messahe catalog for a language."""
    from babel.messages.frontend import CommandLineInterface
    babel         = CommandLineInterface ()
    language      = cmd.argv.pop (0)
    for base_dir in cmd.argv :
        output_dir = _prefix_path (cmd.output_directory,  base_dir)
        pot_file   = _prefix_path (cmd.template_file,     base_dir, "-I18N")
        po_file    = os.path.join (output_dir, "%s.po" % (language, ))
        if os.path.exists (po_file) :
            babel_cmd     = [__file__, "update"]
            for opt, option in ( (cmd.previous,        "--previous")
                               , (cmd.ignore_obsolete, "--ignore-obsolete")
                               , (cmd.no_fuzzy,         "--no-fuzzy-matching")
                               ) :
                if opt :
                    babel_cmd.append (option)
        else :
            babel_cmd     = [__file__, "init"]
        _add_option (babel_cmd, "-l", language)
        _add_option (babel_cmd, "-i", pot_file, "-o", po_file)
        if cmd.dry_run :
            print " ".join (babel_cmd)
        else :
            babel.run        (babel_cmd)
            ### need to clear the handlers to prevent multiple outputs
            babel.log.handlers = []
# end def language

Language = TFL.CAO.Cmd \
    ( language
    , name = "language"
    , args =
        ( "language:S?Which language should be processed"
        , "directories:P"
            "?Directories where the extraction should start"
        ,
        )
    , opts =
        ( "template_file:P=template.pot?Name of the template file"
        , "ignore_obsolete:B?"
            "Do not include obsolete messages in the output"
        , "no_fuzzy:B?Do not use fuzzy matching (default False)"
        , "output_directory:P=-I18N?Output directory"
        , "previous:B?Keep previous msgids of translated messages"
        )
    , min_args = 2
    )
Compile = TFL.CAO.Cmd \
    ( None
    , name = "compile"
    )

_Cmd = TFL.CAO.Cmd \
    ( name = "TFL.Babel"
    , args = (TFL.CAO.Cmd_Choice ("command", Extract, Language, Compile), )
    , opts = ( "dry_run:B?Show the babel command line instead of "
                 "running the command"
             ,
             )
    )
if __name__ == "__main__" :
    _Cmd ()
### __END__ TFL.Babel
