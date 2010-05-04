/*
** Copyright (C) 2010 Martin Glueck All rights reserved
** Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
** This file is part of the library GTW.
**
** This file is free software: you can redistribute it and/or modify
** it under the terms of the GNU Affero General Public License as published by
** the Free Software Foundation, either version 3 of the License, or
** (at your option) any later version.
**
** This file is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU Affero General Public License for more details.
**
** You should have received a copy of the GNU Affero General Public License
** along with this file. If not, see <http://www.gnu.org/licenses/>.
** ****************************************************************************
**
**++
** Name
**    GTW_Form_C
**
** Purpose
**    Javascipt library form GTW form handling.
**
** Revision Dates
**     2-May-2010 (MG) Creation (based on model_edit_ui.js)
++    ««revision-date»»···
**--
*/
(function ($)
{
  var GTW_Form_C =
    { _create : function ()
      {
        var  edit_link = "a[href=edit]";
        var  save_link = "a[href=save]";
        var $display   = this.element.find (".aid-display").show ();
        var $edit      = this.element.find (".aid-edit").hide    ();
        var $children  = $edit.find ("fieldset").children (":not(legend)")
        var $edit_link = this.element.find (edit_link);
        var $save_link = this.element.find (save_link).hide ();
        $edit_link
          .click
            ( function (e)
                {
                  $edit_link.hide   ()
                  $save_link.show   ()
                  $display.hide     ();
                  $edit.show        ();
                  e.preventDefault  ();
                  e.stopPropagation ();
                }
            );
        var ac_observers = $edit.data ("ac_observers") || [];
        ac_observers.push
          ( function (data)
              {
                  $edit_link.show   ()
                  $save_link.hide   ()
                  $display.text (data ["ui_display"]).show     ();
                  $edit.hide        ();
              }
          );
        $edit.data ("ac_observers", ac_observers);
        $save_link
          .click
            ( function (e)
                {
                  $edit_link.show   ()
                  $save_link.hide   ()
                  $display.show     ();
                  $edit.hide        ();
                  e.preventDefault  ();
                  e.stopPropagation ();
                }
            )
      }
    };
  $.widget ("ui.GTW_Form_C", GTW_Form_C);
  $.extend
      ( $.ui.GTW_Form_C
      , { "version"      : "0.1"
        , "defaults"     :
          {
          }
        }
      )
})(jQuery);
