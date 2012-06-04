#! /bin/bash
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This script is part of the Christian Tanzer's python package set.
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this script. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    babel
#
# Purpose
#    Extract and compile translations from Python modules and Jinja templates
#
# Revision Dates
#    30-Jan-2010 (CT) Creation
#    28-Feb-2012 (CT) Add `ReST`, turn `dirs` into an optional argument
#    11-May-2012 (CT) Rename to babel.sh, add `compile` command
#    23-May-2012 (CT) Use `python`, not `/usr/bin/python` in `compile`
#    ««revision-date»»···
#--

cmd=${1:?"Specify a command: extract | language | compile"}; shift

default_langs="en,de"
default_dirs="_MOM _GTW _GTW/_OMP/_Auth _GTW/_OMP/_PAP _GTW/_OMP/_SWP _GTW/_OMP/_SRM _GTW/_OMP/_EVT _JNJ _ReST"
lib=$(dirname $(python -c 'from _TFL import sos; print sos.path.dirname (sos.__file__)'))

case "$cmd" in
    "extract" )
        dirs=${1:-${default_dirs}}; shift
        python ${lib}/_TFL/Babel.py extract                              \
            -bugs_address        "tanzer@swing.co.at,martin@mangari.org" \
            -charset             iso-8859-15                             \
            -copyright_holder    "Mag. Christian Tanzer, Martin Glueck"  \
            -global_config       ${lib}/_MOM/base_babel.cfg              \
            -project             "MOM/GTW/JNJ"                           \
            -sort                                                        \
                $dirs
        ;;
    "language" )
        langs=${1:-${default_langs}}; shift
        dirs=${1:-${default_dirs}}; shift
        python ${lib}/_TFL/Babel.py language -languages "${langs}" -sort $dirs
        ;;
    "compile" )
        model=${1:-./model.py}; shift
        langs=${1:-${default_langs}}; shift
        for lang in $(IFS=, ; echo ${langs})
        do
            mkdir -p "./locale/${lang}/LC_MESSAGES"
            python "${lib}/_TFL/Babel.py" compile \
               -use_fuzzy \
               -languages "${lang}" -combine -import_file "${model}" \
               -output_file "./locale/${lang}/LC_MESSAGES/messages.mo"
        done
        ;;
    * )
        echo "Unknown command $cmd"
        ;;
esac

### __END__ babel
