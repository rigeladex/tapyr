/*
** Copyright (C) 2010 Martin Glueck All rights reserved
** Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
** This file is part of the library GTW.
**
** This module is licensed under the terms of the BSD 3-Clause License
** <http://www.c-tanzer.at/license/bsd_3c.html>.
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
        var $inline      = $edit.find (".inline-instance");
        var ac_observers = $inline.data ("ac_observers") || [];
        ac_observers.push
          ( function (data)
              {
                  $edit_link.show   ()
                  $save_link.hide   ()
                  $display.text (data ["ui_display"]).show     ();
                  $edit.hide        ();
              }
          );
        $inline.data ("ac_observers", ac_observers);
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
