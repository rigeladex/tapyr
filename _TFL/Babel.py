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
import _TFL.defaultdict
import _TFL._Babel.Extract
import _TFL._Babel.Config_File
import _TFL.CAO
import  os
import  sys
import  glob
import  tempfile
import  shutil

class Language_File_Collection (object) :
    """Collect messsage catalog files."""

    def __init__ (self, directories, lang = None) :
        self.languages          = set ()
        self.directories        = set ()
        self.files_per_language = TFL.defaultdict (list)
        for d in directories :
            self._add_languages (d, set (lang))
    # end def __init__

    @classmethod
    def from_sys_modules (cls, lang = None) :
        directories = set ()
        i18n_dirs   = set ()
        for mod in sys.modules.values () :
            if isinstance (getattr (mod, "__file__", None), basestring) :
                directories.add (os.path.dirname (mod.__file__))
        for directory in directories :
            i18n = os.path.join (directory, "-I18N")
            if os.path.isdir (i18n) :
                i18n_dirs.add (directory)
        return cls (i18n_dirs, lang)
    # end def from_sys_modules

    def _add_languages (self, directory, restrict_langs) :
        i18n_dir = os.path.abspath (os.path.join (directory, "-I18N"))
        if restrict_langs :
            self.languages.update (restrict_langs)
            for lang in restrict_langs :
                self.files_per_language [lang].append \
                    (os.path.join (i18n_dir, "%s.po" % (lang, )))
        else :
            for f in glob.glob (os.path.join (i18n_dir, "*.po")) :
                lang = os.path.splitext               (os.path.basename (f)) [0]
                if restrict_langs and lang not in restrict_langs :
                    continue
                self.files_per_language [lang].append (f)
                self.languages.add                    (lang)
                self.directories.add (os.path.dirname (f))
    # end def _add_languages

    def init_or_update (self, cmd) :
        for lang, files in self.files_per_language.iteritems () :
            for f in files :
                output_dir = os.path.dirname (f)
                pot_file   = os.path.join    (output_dir, cmd.template_file)
                templ      = TFL.Babel.PO_File.load (pot_file, locale = lang)
                if os.path.exists (f) :
                    self._update  (lang, f, cmd, templ, pot_file)
                else :
                  print "Creating catalog %r based on %r" % (f, pot_file)
                  templ.save (f, fuzzy = False)
    # end def init_or_update

    def _update (self, lang, po_file_n, cmd, pot_file, pot_file_n) :
        print "Update catalog `%s` based on `%s`" % (po_file_n, pot_file_n)
        po_file = TFL.Babel.PO_File.load (po_file_n, locale = lang)
        po_file.update                   (pot_file, cmd.no_fuzzy)
        tmpname = os.path.join\
            ( os.path.dirname (po_file_n)
            , "%s%s.po" % (tempfile.gettempprefix (), lang)
            )
        try :
            po_file.save \
                ( tmpname
                , ignore_obsolete  = cmd.ignore_obsolete
                , include_previous = cmd.previous
                )
        except :
            os.remove (tmpname)
            raise
        try :
            os.rename (tmpname, po_file_n)
        except OSError:
            # We're probably on Windows, which doesn't support atomic
            # renames, at least not through Python
            # If the error is in fact due to a permissions problem, that
            # same error is going to be raised from one of the following
            # operations
            os.remove   (po_file_n)
            shutil.copy (tmpname, po_file_n)
            os.remove   (tmpname)
    # end def _update

    def compile (self, cmd) :
        for lang, files in self.files_per_language.iteritems () :
            for po_file_n in files :
                output_dir = os.path.dirname (po_file_n)
                mo_file_n  = os.path.join (output_dir, "%s.mo" % (lang, ))
                po_file    = TFL.Babel.PO_File.load (po_file_n)
                if po_file.fuzzy and not cmd.use_fuzzy :
                    print "Catalog %r is marked as fuzzy, skipping" % (po_file_n, )
                    continue
                for message, errors in po_file.catalog.check ():
                    for error in errors :
                        print >> sys.stderr, \
                            "Error: %s:%d: %s", (po_file_n, message.lineno, error)
                print "compiling catalog %r to %r" % (po_file_n, mo_file_n)
                po_file.generate_mo (mo_file_n)
    # end def compile

    def compile_combined (self, cmd, mo_file_n) :
        for lang, files in self.files_per_language.iteritems () :
            po_file   = TFL.Babel.PO_File.combined (* files)
            if po_file.fuzzy and not cmd.use_fuzzy :
                print "Catalog %r is marked as fuzzy, skipping" % (files [0], )
                continue
            for message, errors in po_file.catalog.check ():
                for error in errors :
                    print >> sys.stderr, "Error: %s", (error)
            print "compiling combined catalog %r to %r" % (files, mo_file_n)
            po_file.generate_mo (mo_file_n)
    # end def compile_combined

# end class Language_File_Collection

def _prefix_path (filename, * prefix) :
    if not os.path.isabs (filename) :
        prefix   = prefix + (filename, )
        filename = os.path.abspath (os.path.join (* prefix))
    return filename
# end def _prefix_path

def extract (cmd) :
    for base_dir in cmd.argv :
        config        = TFL.Babel.Config_File \
            ( _prefix_path (cmd.extraction_config, base_dir)
            , parent = cmd.global_config
            )
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
    lang_files = Language_File_Collection (cmd.argv, cmd.languages)
    lang_files.init_or_update (cmd)
# end def language

Language = TFL.CAO.Cmd \
    ( language
    , name = "language"
    , args =
        ( "directories:P"
            "?Directories where the extraction should start"
        ,
        )
    , opts =
        ( "languages:S,?Which language should be processed"
        , "ignore_obsolete:B?"
            "Do not include obsolete messages in the output"
        , "no_fuzzy:B?Do not use fuzzy matching (default False)"
        , "output_directory:P=-I18N?Output directory"
        , "previous:B?Keep previous msgids of translated messages"
        , "template_file:P=template.pot?Name of the template file"
        )
    , min_args = 1
    )

def compile (cmd) :
    if cmd.import_file :
        execfile (cmd.import_file)
        lang_coll = Language_File_Collection.from_sys_modules (cmd.languages)
    else :
        lang_coll = Language_File_Collection (cmd.argv, cmd.languages)
    if cmd.combined_name :
        lang_coll.compile_combined (cmd, cmd.combined_name)
    else :
        lang_coll.compile          (cmd)
# end def compile

Compile = TFL.CAO.Cmd \
    ( compile
    , name = "compile"
    , args =
        ( "directories:P?Directories XXX"
        ,
        )
    , opts =
        ( "combined_name:P?Combine all files for a langage into one mo file"
        , "import_file:P?Determine directories from imported modules after "
            "importing this files"
        , "languages:S,?Which language should be processed"
        , "output_directory:P=-I18N?Output directory"
        , "use_fuzzy:B?Compile fuzzy files as well (default False)"
        )
    , min_args = 0
    )

_Command = TFL.CAO.Cmd \
    ( name = "TFL.Babel"
    , args = (TFL.CAO.Cmd_Choice ("command", Extract, Language, Compile), )
    , opts =
        ( "global_config:P?A global config file"
        ,
        )
    )

if __name__ == "__main__" :
    _Command ()
### __END__ TFL.Babel
