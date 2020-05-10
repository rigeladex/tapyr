#! /bin/bash
# Copyright (C) 2010-2020 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This script is part of the Christian Tanzer's python package set.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    19-Feb-2014 (CT) Use `python -m` to run `_TFL.Babel`
#     4-Jul-2014 (CT) Add `_GTW/_MF3` and `_GTW/_RST*`
#    31-Aug-2014 (CT) Add argument for `PYTHONPATH` to `compile`
#    31-Jul-2015 (CT) Add `_GTW/_OMP/_PAP/_E164`
#     2-Feb-2016 (CT) Add `_CAL`
#     2-Feb-2016 (CT) Change `charset` from `iso-8859-15` to `utf-8`
#    19-May-2016 (CT) Add command `compile-all`
#    27-Mar-2020 (CT) Make Python-3 compatible (`print()`)
#    10-May-2020 (CT) Add `_TFL` to `default_dirs`
#    ««revision-date»»···
#--

cmd=${1:?"Specify a command: extract | language | compile"}; shift

default_langs="en,de"
default_dirs="_CAL _MOM _GTW _GTW/_OMP/_Auth _GTW/_OMP/_PAP _GTW/_OMP/_PAP/_E164 _GTW/_OMP/_SWP _GTW/_OMP/_SRM _GTW/_OMP/_EVT _GTW/_MF3 _GTW/_RST _GTW/_RST/_MOM _GTW/_RST/_TOP _GTW/_RST/_TOP/_MOM _JNJ _ReST _TFL"
lib=$(dirname $(python -c 'from _TFL import sos; print (sos.path.dirname (sos.__file__))'))

### `python -m _TFL.Babel` won't add `.../_TFL` to `sys.path`

case "$cmd" in
    "extract" )
        dirs=${1:-${default_dirs}}; shift
        python -m _TFL.Babel extract                                     \
            -bugs_address        "tanzer@swing.co.at,martin@mangari.org" \
            -charset             utf-8                                   \
            -copyright_holder    "Mag. Christian Tanzer, Martin Glueck"  \
            -global_config       ${lib}/_MOM/base_babel.cfg              \
            -project             "MOM/GTW/JNJ"                           \
            -sort                                                        \
                $dirs
        ;;
    "language" )
        langs=${1:-${default_langs}}; shift
        dirs=${1:-${default_dirs}}; shift
        python -m _TFL.Babel language -languages "${langs}" -sort $dirs
        ;;
    "compile" )
        model=${1:-./model.py}; shift
        langs=${1:-${default_langs}}; shift
        pypa=${1}
        if [ -n "$pypa" ]
        then
            export PYTHONPATH=$pypa
            echo $PYTHONPATH
        fi
        for lang in $(IFS=, ; echo ${langs})
        do
            mkdir -p "./locale/${lang}/LC_MESSAGES"
            python -m _TFL.Babel compile \
               -use_fuzzy \
               -languages "${lang}" -combine -import_file "${model}" \
               -output_file "./locale/${lang}/LC_MESSAGES/messages.mo"
        done
        ;;
    "compile-all" )
        langs=${1:-${default_langs}}; shift
        pypa=${1}
        if [ -n "$pypa" ]
        then
            export PYTHONPATH=$pypa
            echo $PYTHONPATH
        fi
        for lang in $(IFS=, ; echo ${langs})
        do
            mkdir -p "./locale/${lang}/LC_MESSAGES"
            python -m _TFL.Babel compile \
               -use_fuzzy \
               -languages "${lang}" -combine \
               -output_file "./locale/${lang}/LC_MESSAGES/messages.mo" \
               ${default_dirs}
        done
        ;;
    * )
        echo "Unknown command $cmd"
        ;;
esac

### __END__ babel
