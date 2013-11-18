# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    Render_Mode
#
# Purpose
#    Test of the render mode handling in templates.
#
# Revision Dates
#     5-May-2010 (MG) Creation
#    ««revision-date»»···
#--
r"""
    >>> macros = '''
    ... {% macro mode_1_macro_1 (obj) -%}
    ...    Mode-1  --  Macro 1
    ...    call macro 2 in same mode (should be mode 1)
    ...    {{ GTW.render_fofi_widget (obj, "macro_2", obj) -}}
    ... {%- endmacro -%}
    ... {%- macro mode_1_macro_2 (obj) -%}
    ...    Mode-1  --  Macro 2
    ...    call macro 1 but switch to mode 2
    ...        {{ GTW.render_fofi_widget (obj, "macro_1", obj, render_mode = "mode_2") -}}
    ... {%- endmacro -%}
    ... {%- macro mode_2_macro_1 (obj) -%}
    ...        Mode-2  --  Macro 1
    ...        call macro 2 in same mode (should be mode 2)
    ...        {{ GTW.render_fofi_widget (obj, "macro_2", obj) }}
    ...        call macro 3 in same mode (should be mode 2)
    ...        {{ GTW.render_fofi_widget (obj, "macro_3", obj) }}
    ... {%- endmacro -%}
    ... {%- macro mode_2_macro_2 (obj) -%}
    ...        Mode-2  --  Macro 2
    ...        call macro 1 but switch to mode 3
    ...            {{ GTW.render_fofi_widget (obj, "macro_1", obj, render_mode = "mode_3") }}
    ... {%- endmacro -%}
    ... {%- macro mode_2_macro_3 (obj) -%}
    ...        Mode-2  --  Macro 3
    ... {%- endmacro -%}
    ... {% macro mode_3_macro_1 (obj) -%}
    ...                Mode-3  --  Macro 1
    ... {%- endmacro -%}
    ... '''

    >>> template = '''
    ...    {{ GTW.render_fofi_widget (obj, "macro_1", obj) }}
    ... '''
    >>> env = HTML (loader = DictLoader (dict (macros = macros)))
    >>> obj = Object ()
    >>> obj.render_mode_description = GTW.Form.Render_Mode_Description \
    ...     ( mode_1 = GTW.Form.Widget_Spec
    ...                  ( "macros, default"
    ...                  , macro_1 = "macros, mode_1_macro_1"
    ...                  , macro_2 = "macros, mode_1_macro_2"
    ...                  )
    ...     , mode_2 = GTW.Form.Widget_Spec
    ...                  ( "macros, default"
    ...                  , macro_1 = "macros, mode_2_macro_1"
    ...                  , macro_2 = "macros, mode_2_macro_2"
    ...                  , macro_3 = "macros, mode_2_macro_3"
    ...                  )
    ...     , mode_3 = GTW.Form.Widget_Spec
    ...                  ( "macros, default"
    ...                  , macro_1 = "macros, mode_3_macro_1"
    ...                  )
    ...     )
    >>> obj.default_render_mode = "mode_1"
    >>> print env.from_string (template).render (obj = obj)
    <BLANKLINE>
       Mode-1  --  Macro 1
       call macro 2 in same mode (should be mode 1)
       Mode-1  --  Macro 2
       call macro 1 but switch to mode 2
           Mode-2  --  Macro 1
           call macro 2 in same mode (should be mode 2)
           Mode-2  --  Macro 2
           call macro 1 but switch to mode 3
               Mode-3  --  Macro 1
           call macro 3 in same mode (should be mode 2)
           Mode-2  --  Macro 3
"""

from _JNJ.Environment import HTML
from _TFL.Record      import *
from  jinja2          import DictLoader
from _GTW             import GTW

import _GTW._Form.Render_Mode_Description

class Object (object) : pass

### __END__ GTW.__test__.Render_Mode
