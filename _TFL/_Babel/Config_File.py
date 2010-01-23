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
#    TFL.Babel.Config_File
#
# Purpose
#    Parse the config file for the translations extraction
#
# Revision Dates
#    21-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._Meta.Object
import _TFL._Babel.Extractor
import  ConfigParser
from    babel.util             import odict

class Config_File (TFL.Meta.Object) :
    """A extractor config file.
       >>> import cStringIO
       >>> source = '''[defaults]
       ... load_translations = _MOM, _GTW
       ...
       ... [extractors]
       ... MOM = _MOM.Babel:Extract
       ...
       ... [MOM: **/__babel__.py]
       ...
       ... [python: **.py]
       ... ignore_pattern = **/__*__.py, **/_OMP/**.py
       ... '''
       >>> file = cStringIO.StringIO (source)
       >>> cfg = Config_File (file)
       >>> cfg.defaults
       {'load_translations': '_MOM, _GTW'}
       >>> sorted (cfg.extractors.iteritems ())# doctest:+ELLIPSIS
       [('mom', ...), ('python', <function Python at ...>)]
       >>> cfg.patterns.keys ()
       ['MOM', 'python']
    """

    load_translation_key = "load_translations"

    def __init__ (self, filename, parent = None) :
        self.__super.__init__ ()
        config = self._as_config_parser (filename)
        parent = self._as_config_parser (parent)
        print parent
        self.patterns        = odict ()
        self.extractors      = dict (python = TFL.Babel.Extractor.Python)
        self.defaults        = dict  ()
        self._method_options = dict  ()
        for cfg in parent, config :
            if cfg :
                self._add_config (cfg)
    # end def __init__

    def _add_config (self, config) :
        for section in config.sections () :
            if section == "extractors" :
                for name, module_spec in config.items (section) :
                    self.extractors [name] = self._load_function (module_spec)
            elif section == "defaults" :
                self.defaults      = dict (config.items (section))
            else :
                extractor, pattern               = section.split (":")
                extractor                        = extractor.lower ()
                self.patterns [extractor]        = pattern.strip ()
                self._method_options [extractor] =  dict (config.items
                                                          (section))
        self.defaults ["loaded_translations"] = self._load_pkg_translations \
           (self.defaults.get (self.load_translation_key))
        for mo in self._method_options.values () :
           self._method_options ["loaded_translations"] = \
               self._load_pkg_translations (mo.get (self.load_translation_key))
    # end def _add_config

    def _as_config_parser (self, filename) :
        config = None
        if filename :
            config = ConfigParser.RawConfigParser (dict_type = odict)
            if not hasattr (filename, "read") :
                filename         = open  ((filename))
            config.readfp                (filename)
        return config
    # end def _as_config_parser

    def _load_pkg_translations (self, pkg) :
        if pkg :
            return TFL.Babel.PO_File.combine_package_translations \
                (pkg.split (","))
        return dict ()
    # end def _load_pkg_translations

    def get (self, option, method = None, default = None) :
        mo = self._method_options.get (method, {})
        de = self.defaults
        return mo.get (option, de.get (option, default))
    # end def get

    def get_list (self, option, method = None, default = ()) :
        value = self.get (option, method, default)
        if isinstance (value, basestring) :
            return [p.strip () for p in value.split (",")]
        return value
    # end def get_list

    def _load_function (self, spec) :
        module_spec, fct_name = spec.split (":")
        module                = __import__ (module_spec)
        for p in module_spec.split (".") [1:] :
            module = getattr (module, p)
        return getattr (module, fct_name)
    # end def _load_function

# end class Config_File

if __name__ != "__main__" :
    TFL.Babel._Export ("*")
### __END__ TFL.Babel.Config_File
