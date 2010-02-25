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
**    ««revision-date»»···
**--
*/

(function ($)
{
  var field_no_pat = /-M([\dP]+)-/;
  var Autocomplete =
  {
      _create : function ()
      {
          var $fields = this.element.find
              ("[name^=" + this.options.prefix + "]:visible");
          for (var trigger_field in this.options.triggers)
          {
              var $field = $fields.filter ("[name$=" + trigger_field + "]");
              this._setup_completion ($field, trigger_field);
          }
      }
      , _auto_complete_search : function
          (request, trigger, field_name, self, callback, no)
      {
          var data     = {TRIGGER_FIELD : field_name};
          var comp_opt = self.options;
          var pf       = comp_opt.prefix + "-";
          if (no) pf   = pf + "M" + no + "-";
          for (var i = 0;  i < trigger.fields.length; i++)
          {
              var mfn   = trigger.fields [i];
              var value =  $("[name=" + pf + mfn + "]").attr ("value");
              if (value) data [mfn] = value;
          }
          jQuery.getJSON
            ( comp_opt.list_url
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
      , _setup_completion : function ($field, trigger_field)
      {
          var  self     = this;
          var  options  = this.options
          var  trigger  =  options.triggers [trigger_field];
          var  match    = field_no_pat.exec ($field [0].name) || [""]
          var  no       = match  [1];
          $field.autocomplete
              ({ source    : function (request, callback)
                  {
                     self._auto_complete_search
                      (request, trigger, trigger_field, self, callback, no);
                  }
                , minLength : trigger.min_chars
                , select    : function (evt, ui)
                    {
                        self._update_values (ui.item, no);
                    }
               });
      }
      , _update_values : function (item, no)
      {
          var options = this.options;
          var id      = options.prefix + "-comp-list";
          var pf      = options.prefix + "-";
          if (no) pf  = pf + "M" + no + "-";
          jQuery.getJSON
              ( options.obj_url, {"lid" : item.lid}
              , function (data, textStatus)
                {
                    $("#" + id).remove ();
                    if (textStatus == "success")
                    {
                        for (var key in data)
                        {
                            var $field = $("[name=" + pf + key + "]");
                            var tag_name = $field [0].nodeName.toLowerCase ();
                            if (tag_name == "input")
                            {
                                $field.attr ("value", data [key]);
                            }
                            $field.attr ("disabled", "disabled");
                        }
                    }
                }
              );
      }
  }
  $.widget ("ui.mom_autocomplete", Autocomplete);
  $.extend
    ( $.ui.mom_autocomplete
    , { version                          : "0.1"
      , defaults                         :
        { triggers                       : { "subscriber_number"
                                           : { "min_chars" : 2
                                             , "fields"    :
                                                 [ "country_code"
                                                 , "area_code"
                                                 , "subscriber_number"
                                                 ]
                                             }
                                           }
        , list_url                       : "/Admin/Person/complete/Person_has_Address/address"
        , obj_url                        : "/Admin/Person/completed/Person_has_Address/address" /* lid -> pk */
        , prefix                         : "Person__Person_has_Address__address"
        , standalone                     : true
        }
      }
    );
})(jQuery);
