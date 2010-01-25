# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package TFL.Babel.
#
# This module is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    Extract
#
# Purpose
#    Handel the extraction procedure
#
# Revision Dates
#    21-Jan-2010 (MG) Creation
#    25-Jan-2010 (MG) Convert absolute path to relative path
#    ««revision-date»»···
#--
from   _TFL                          import TFL
from   _TFL.predicate                import any_true
import _TFL.relative_to_search_path
import _TFL._Babel.PO_File
import  os
import  sys

from    babel.util             import pathmatch, relpath
from    babel.messages.extract import empty_msgid_warning

class Existing_Translations (object) :
    """Read multiple POT files and checks whether a certain message is
       already part of another template
    """

    def __init__ (self, packages) :
        self.pot_file
        if packages :
            for pkg in (p.strip () for p in packages.split (",")) :
                module   = __import__ (pkg)
                base_dir = os.path.dirname (module.__file__)
                pot_file = os.path.join (base_dir, "-I18N", "template.pot")
                self.pot_files.append (read_po (open (pot_file)))
    # end def __init__

    def __contains__ (self, message) :
        return any_true (message in pot for pot in self.pot_files)
    # end def __contains__

# end class Existing_Translations

class Skip (StandardError) : pass

Default_Keywords = dict \
    ( _         = (1, )
    , _T        = (1, )
    , _Tn       = (1, 2)
    , N_        = (1, )
    , gettext   = (1, )
    , ugettext  = (1, )
    , ngettext  = (1, 2)
    , ungettext = (1, 2)
    )

def Extract (dirname, template_file, config, cmd) :
    absname = os.path.abspath (dirname)
    po_file = TFL.Babel.PO_File \
        ( project            = cmd.project
        , version            = cmd.version
        , bugs_address       = cmd.bugs_address
        , copyright_holder   = cmd.copyright_holder
        , charset            = cmd.charset
        , width              = cmd.width
        , no_location        = cmd.no_location
        , omit_header        = cmd.omit_header
        , sort               = cmd.sort
        )
    keywords = Default_Keywords.copy ()
    keywords.update (dict (k, None) for k in cmd.keywords)
    for root, dirnames, filenames in os.walk (absname) :
        dirnames.sort  ()
        for filename in sorted (filenames) :
            filename = relpath \
                (os.path.join (root, filename).replace (os.sep, '/'), dirname)
            try :
                for method_name, pattern in config.patterns.items () :
                    if pathmatch (pattern, filename) :
                        for pattern in config.get_list \
                            ("ignore_patterns", method_name) :
                            if pathmatch (pattern, filename) :
                                raise Skip
                        filepath = os.path.join (absname, filename)
                        rfp      = TFL.relative_to_python_path (filepath)
                        print "Method `%-10s`: `%s" % (method_name, filename)
                        for lineno, message, comments in \
                                _extract_from_file    \
                                    ( method_name
                                    , filepath
                                    , config
                                    , cmd
                                    , keywords
                                    ) :
                            po_file.add \
                                ( message, None, [( rfp, lineno)]
                                , auto_comments = comments
                                )
                        break
            except Skip :
                print "Ignore             : `%s" % (filename, )
    print >> sys.stderr, "Create template file", template_file
    po_file.save (template_file)
# end def Extract

def _extract_from_file (method_name, file_name, config, cmd, keywords) :
    method = config.extractors [method_name]
    file   = open (file_name, "U")
    for lineno, funcname, messages, comments in method \
        ( file, keywords
        , comment_tags = ()
        , config       = config
        , method       = method_name
        ) :
        if funcname :
            spec = keywords [funcname] or (1,)
        else:
            spec = (1,)
        if not isinstance (messages, (list, tuple)) :
            messages = [messages]
        if not messages :
            continue
        # Validate the messages against the keyword's specification
        msgs    = []
        invalid = False
        # last_index is 1 based like the keyword spec
        last_index = len (messages)
        for index in spec :
            if last_index < index:
                # Not enough arguments
                invalid = True
                break
            message = messages [index - 1]
            if message is None :
                invalid = True
                break
            msgs.append (message)
        if invalid:
            continue
        first_msg_index = spec [0] - 1
        if not messages [first_msg_index]:
            # An empty string msgid isn't valid, emit a warning
            where = '%s:%i' % (file_name, lineno)
            print >> sys.stderr, empty_msgid_warning % where
            continue
        messages = tuple (msgs)
        if len (messages) == 1:
            messages = messages [0]

        if cmd.strip_comment_tags:
            _strip_comment_tags (comments, comment_tags)
        yield lineno, messages, comments
# end def _extract_from_file

def _strip_comment_tags(comments, tags):
    """Helper function for `extract` that strips comment tags from strings
    in a list of comment lines.  This functions operates in-place.
    """
    def _strip(line):
        for tag in tags:
            if line.startswith(tag):
                return line[len(tag):].strip()
        return line
    comments[:] = map(_strip, comments)
# end def _strip_comment_tags

if __name__ != "__main__" :
    TFL.Babel._Export ("*")
### __END__ TFL.Babel.Extract



