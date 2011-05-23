#! /bin/bash
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    babel_extract
#
# Purpose
#    Extract translations from Python modules and Jinja templates
#
# Revision Dates
#    30-Jan-2010 (CT) Creation
#    ««revision-date»»···
#--

cmd=${1:?"Specify a command: extract | language"}; shift

dirs="_MOM _GTW _GTW/_OMP/_Auth _GTW/_OMP/_PAP _GTW/_OMP/_SWP _GTW/_OMP/_SRM _GTW/_OMP/_EVT _GTW/_NAV/example _JNJ"

case "$cmd" in
    "extract" )
        python _TFL/Babel.py extract                            \
            -bugs_address        "tanzer@swing.co.at,martin@mangari.org" \
            -charset             iso-8859-1                              \
            -copyright_holder    "Mag. Christian Tanzer, Martin Glueck"  \
            -global_config       _MOM/base_babel.cfg                     \
            -project             "MOM/GTW/JNJ"                           \
            -sort                                                        \
                $dirs
        ;;
    "language" )
        lang=${1:-"de"}
        /usr/bin/python _TFL/Babel.py language -languages "$lang" -sort $dirs
        ;;
    * )
        echo "Unknown command $cmd"
        ;;
esac

### __END__ babel_extract
