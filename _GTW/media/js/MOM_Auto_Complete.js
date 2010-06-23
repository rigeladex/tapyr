/*
** Copyright (C) 2009-2010 Martin Glück All rights reserved
** Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
**
** This library is free software; you can redistribute it and/or
** modify it under the terms of the GNU Library General Public
** License as published by the Free Software Foundation; either
** version 2 of the License, or (at your option) any later version.
**
** This library is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
** Library General Public License for more details.
**
** You should have received a copy of the GNU Library General Public
** License along with this library; if not, write to the Free
** Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
** ****************************************************************************
**
**++
** Name
**    MOM_Auto_Complete
**
** Purpose
**    Define a jQuery UI widget handling the auto completion of MOM Entites
**
** Revision Dates
**    24-Feb-2010 (MG) Creation
**    12-May-2010 (MG) `s/lid/pid/g`
**    ««revision-date»»···
**--
*/

(function ($)
{
  var field_no_pat = /-M([\dP]+)_/;
  var Auto_Complete =
    {
      _create : function ()
      {
        var  options  = this.options
        var  field    = this.options.field
        var  trigger  = options.triggers [field];
        var  match    = field_no_pat.exec (this.element [0].name) || [""]
        var  no       = match  [1];
        var  self     = this;
        this.element.autocomplete
            ({ source    : function (request, callback)
                {
                   self._auto_complete_search
                    (request, trigger, field, self, callback, no);
                }
              , minLength : trigger.min_chars
              , select    : function (evt, ui)
                  {
                      self._update_values (ui.item, no);
                  }
             });
      }
      , _auto_complete_search : function
          (request, trigger, field_name, self, callback, no)
      {
        var data     = {TRIGGER_FIELD : field_name};
        var comp_opt = self.options;
        var pf       = comp_opt.field_prefix;
        if (no) pf   = pf + "-M" + no;
        if (comp_opt.field_postfix)
            pf       = pf + "__" + comp_opt.field_postfix;
        pf           = pf + "__"
        for (var i = 0;  i < trigger.fields.length; i++)
        {
            var mfn   = trigger.fields [i];
            var value = $("[name=" + pf + mfn + "]").attr ("value");
            if (value) data [mfn] = value;
        }
        jQuery.getJSON
          ( comp_opt.suggest_url
          , data
          , function (data, textStatus)
              {
                if (textStatus == "success")
                  {
                    callback (data);
                  }
              }
          )
      }
      , _update_values : function (item, no)
      {
        var self    = this;
        var options = this.options;
        var pf      = options.field_prefix;
        if (no) pf  = pf + "-M" + no;
        if (options.field_postfix)
            pf      = pf + "__" + options.field_postfix;
        pf          = pf + "__"
        jQuery.getJSON
            ( options.complete_url, {"pid" : item.pid}
            , function (data, textStatus)
              {
                  if (textStatus == "success")
                  {
                      var $field = self._set_form_values (pf, data, false);
                      observers = $field.parents (".inline-instance")
                           .data ("ac_observers") || [];
                      for (var i = 0; i < observers.length; i++)
                        {
                          observers [i] (data);
                        }
                  }
              }
            );
      }
      , _set_form_values : function (pf, data, disable)
      {
        var $result;
        for (var key in data)
          {
            var value  = data [key];
            if (typeof value == "object")
              {
                this._set_form_values (pf + key + "__", value, disable)
              }
            else
              {
                var $field = $("[name=" + pf + key + "]");
                if ($field.length)
                  {
                    $result = $field;
                    $field.attr ("value", value);
                    if (disable)
                        $field.attr ("disabled", "disabled");
                  }
              }
          }
        return $result;
      }
  }
  $.widget ("ui.MOM_Auto_Complete", Auto_Complete);
  $.extend
    ( $.ui.MOM_Auto_Complete
    , { version                          : "0.1"
      }
    );
})(jQuery);
