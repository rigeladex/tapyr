/*
** Copyright (C) 2009 Martin Glück All rights reserved
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
**    model_edit_ui
**
** Purpose
**    Define a jQuery UI widget handling the nested many to many forms
**
** Revision Dates
**    20-Jun-2009 (MG) Creation
**    12-Jul-2009 (MG) Min and Max count's are considered for enable/disable
**                     of add/delete button's
**    20-Aug-2009 (MG) Completer added and completion functions added to
**                     Many2Many
**    ««revision-date»»···
**--
*/

(function ($)
{
  var field_name_pat = /-M[\dP]+-/;
  var field_no_pat   = /-M([\dP]+)-/;

  var Many2Many =
    { _init : function ()
      {
          var $legend    = this.element.find ("legend");
          var add_class  = this._getData     ("add_class");
          var $m2m_range = this.element.find ("input.many-2-many-range:first");
          var  m2m_range = $m2m_range.attr   ("value").split (":");
          var  cur_count = parseInt (m2m_range [1]);
          var  max_count = parseInt (m2m_range [2]);
          this._setData ("$prototype", this.element.find (".m2m-prototype"));
          this._setData ("$m2m_range", $m2m_range);
          this._setData ("min_count",  parseInt (m2m_range [0]));
          this._setData ("cur_count",  cur_count);
          this._setData ("cur_number", cur_count);
          this._setData ("max_count",  max_count);
          $legend.prepend
              ( '<a href="#add" class="ui-icon-add ui-icon-plusthick '
              + add_class
              + '" title="Add ' + $legend.attr ("title")
              + '">Add</a> '
              );
          var $forms = this.element.find (".m2m-nested-form");
          for (var i = 0; i < $forms.length; i++)
          {
              this._add_delete_button ($forms.eq (i));
          }
          this.element.parents ("form").many2manysubmit ();
          this._update_button_states ();
      }
    , _add_delete_button : function ($form)
      {
          var $link = $form.find ("a[href=#delete]");
          if (! $link.length)
          {
              var  first_tag = $form.get (0).tagName.toLowerCase ();
              $link          =
                  $('<a href="#delete" class="ui-icon-delete ui-icon-closethick">Delete</a>');
              var $element = $link;
              if (first_tag == "tr")
                  $element = $("<td></td>").append ($link);
              $form.append ($element);
          }
          /* we can only bind callback's once the element is part of the DOM */
          $link.bind ("click", this, this._delete_form);
      }
    , _add_new_form : function (evt)
      {
          var self       = evt.data;
          var $prototype = self._getData    ("$prototype");
          var  comp_opt  = $prototype.data  ("completion");
          var $new       = $prototype.clone ().removeClass ("m2m-prototype");
          /* now that we have cloned the block, let's change the
          ** name/id/for attributes
          */
          self._setData ("cur_count", self._getData ("cur_count") + 1);
          var cur_number = self._getData ("cur_number");
          self._setData ("cur_number", cur_number + 1);
          var pattern    = /MP-/;
          var new_no     = "M" + cur_number + "-";
          var $labels    = $new.find     ("label")
          for (var i = 0; i < $labels.length; i++)
          {
              var $l = $labels.eq (i);
              $l.attr ("for", $l.attr ("for").replace (pattern, new_no));
          }
          var $edit_elements = $new.find (":input");
          var  edit_mod_list = ["id", "name"];
          for (var i = 0; i < $edit_elements.length; i++)
          {
              var $e = $edit_elements.eq (i);
              for (var j = 0; j < edit_mod_list.length; j++)
              {
                  var n = edit_mod_list [j];
                  $e.attr (n, $e.attr (n).replace (pattern, new_no));
              }
          }
          /* we are ready to add the new block at the end */
          self._add_delete_button    ($new);
          $prototype.parent          ().append ($new);
          self._update_button_states ();
          if (comp_opt != undefined)
          {
              var pf = comp_opt.prefix + "-" + new_no;
              for (var field_name in comp_opt.triggers)
              {
                  var real_field_name = pf + field_name;
                  $("[name=" + real_field_name + "]").bind
                      ( "keyup"
                      , {comp_opt : comp_opt, self :self}
                      , self._auto_complete
                      );
              }
          }
          $new.find          ("input[name$=-_state_]").attr ("value", "3");
          evt.preventDefault ();
      }
    , _model_field_name     : function (name)
    {
        return name.split (field_name_pat) [1];
    }
    , _auto_complete        : function (evt)
    {
        //console.log ("Key up");
        var data     = {};
        var self     = evt.data.self;
        var comp_opt = evt.data.comp_opt;
        var trigger  = evt.currentTarget.name.split (field_name_pat) [1];
        trigger      = comp_opt.triggers [trigger];
        var fields   = trigger ["fields"];
        var value    = evt.currentTarget.value;
        var id       = comp_opt.prefix + "-comp-list"
        $("#" + id).remove (); /* remove old display */
        if (  (trigger.min_chars != undefined)
           && (value.length      >= trigger.min_chars)
           )
        {
            var no = field_no_pat.exec (evt.currentTarget.name) [1];
            var pf = comp_opt.prefix + "-M" + parseInt (no) + "-";
            for (var i = 0;  i < trigger.fields.length; i++)
            {
                var mfn   = trigger.fields [i];
                var value =  $("[name=" + pf + mfn + "]").attr ("value");
                if (value) data [mfn] = value;
            }
            jQuery.get
              ( comp_opt.list_url
              , data
              , function (data, textStatus)
                {
                    if (textStatus == "success")
                    {
                        var comp_data = { comp_data : comp_data
                                        , input     :  evt.originalTarget
                                        };
                        var $auto_complete = $(data).attr ("id", id);
                        if ($auto_complete.find (".completion-id").length)
                        {
                            $(evt.originalTarget).parent ()
                                                 .append ($auto_complete);
                            $auto_complete.children ()
                                          .bind ( "click", function (e)
                              {
                                  var pk = $(e.originalTarget).find
                                    (".completion-id").text ();
                                  var no = field_no_pat.exec
                                    (evt.currentTarget.name) [1];
                                  jQuery.getJSON
                                    ( comp_opt.obj_url
                                    , { "id" : pk, "no" : no}
                                    , function (data, textStatus)
                                      {
                                          $("#" + id).remove ();
                                          if (textStatus == "success")
                                          {
                                              self._replace_fields (data, pf);
                                          }
                                          console.log (data);
                                      }
                                    );
                              })
                                          .bind ( "click", function (e)
                        }
                    }
                }
              )
        }
    }
    , _replace_fields       : function (fields, pf)
    {
        for (var key in fields)
        {
            $("[name=" + pf + key + "]").replaceWith (fields [key]);
        }
    }
    , _update_button_states : function ()
      {
          var $add_button = this.element.find ("legend a[href=#add]");
          var cur_count   = this._getData ("cur_count");
          var min_count   = this._getData ("min_count");
          var max_count   = this._getData ("max_count");
          var $undeletes  = this.element.find
              (".m2m-nested-form a[href=#delete].ui-icon-circle-close");
          var $deletes    = this.element.find
              (".m2m-nested-form a[href=#delete].ui-icon-closethick");
          if (cur_count < max_count)
          {
              $add_button.bind        ("click", this, this._add_new_form)
                         .removeClass ("ui-state-disabled");
              $undeletes .bind        ("click", this, this._delete_form)
                         .removeClass ("ui-state-disabled");
          }
          else
          {
              $add_button.unbind   ("click", this._add_new_form)
                         .addClass ("ui-state-disabled");
              $undeletes. unbind   ("click", this._delete_form)
                         .addClass ("ui-state-disabled");
          }
          if (cur_count == min_count)
          {
              $deletes.addClass    ("ui-state-disabled")
                      .unbind      ("click", this._delete_form);
          }
          else
          {
              $deletes.removeClass ("ui-state-disabled")
                      .bind        ("click", this, this._delete_form);
          }
          this._getData ("$m2m_range").attr
              ("value", [min_count, cur_count, max_count].join (":"));
      }
    , _forms_equal : function ($l, $r)
      {
          /* Returns whether the values of the two forms are equal */
          var $l_value_elements = $l.find ("[value]");
          var $r_value_elements = $r.find ("[value]");
          if ($l_value_elements.length != $r_value_elements.length)
              return false;
          for (var i = 0; i < $l_value_elements.length; i++)
          {
              if (  $l_value_elements.eq (i).attr ("value")
                 != $r_value_elements.eq (i).attr ("value")
                 )
                  return false;
          }
          return true;
      }
    , _delete_form : function (evt)
      {
          var self       = evt.data;
          var $prototype = self._getData         ("$prototype");
          var $form      = $(evt.target).parents (".m2m-nested-form");
          var $state     = $form.find            ("input[name$=-_state_]");
          if (self._forms_equal ($form, $prototype))
          {
              $form.remove ();
              self._setData ("cur_count", self._getData ("cur_count") - 1);
          }
          else
          {
              var $link     = $form.find ("a[href=#delete]");
              var $elements = $form.find (":input:not([type=hidden])");
              if ($link.hasClass ("ui-icon-closethick"))
              {
                  $state.attr           ("value", "1")
                  $elements.attr        ("disabled","disabled")
                           .addClass    ("ui-state-disabled");
                  $link.removeClass     ("ui-icon-closethick ui-icon-delete")
                       .addClass        ("ui-icon-circle-close ui-icon-add");
                  self._setData ("cur_count", self._getData ("cur_count") - 1);
              }
              else
              {
                  if ($form.find ("input:[name$=-id]").attr ("value"))
                      $state.attr       ("value", "0");
                  else
                      $state.attr       ("value", "3");
                  $elements.removeAttr  ("disabled")
                           .removeClass ("ui-state-disabled");
                  $link.removeClass     ("ui-icon-circle-close ui-icon-add")
                       .addClass        ("ui-icon-closethick ui-icon-delete");
                  self._setData ("cur_count", self._getData ("cur_count") + 1);
              }
          }
          self._update_button_states ();
          evt.preventDefault         ();
      }
    }
  $.widget ("ui.many2many", Many2Many);
  $.extend
    ( $.ui.many2many
    , { version                          : "0.1"
      , defaults                         :
        { add_class                      : "m2m-add"
        }
      }
    );
  var Completer =
    { _init : function ()
      {
          var options = {};
          for (var key in $.ui.completer.defaults)
          {
              options [key] = this._getData (key);
          }
          this.element.find (".m2m-prototype").data ("completion", options);
      }
    }
  $.widget ("ui.completer", Completer);
  $.extend
    ( $.ui.completer
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
        , list_url                       : ""
        , obj_url                        : "" // id -> pk, no ->number
        , prefix                         : ""
        }
      }
    );
  var Many2ManySubmit =
    { _init : function ()
      {
          var pattern    = /M\d+-/;
          var self       = this;
          this.element.bind ("submit", function (evt)
          {
              //evt.preventDefault ();
              /* first, let's renumerate the forms */
              self.element.find
                  (".nested-many-2-many, .nested-many-2-many-table")
                          .each ( function ()
                  {
                      var no = -1; /* the first is the prototype */
                      $(this).find (".m2m-nested-form").each (function ()
                      {
                          var $elements      = $(this).find (":input");
                          var  edit_mod_list = ["id", "name"];
                          var  new_no        = "M" + no + "-";
                          for (var i = 0; i < $elements.length; i++)
                          {
                              var $e = $elements.eq (i);
                              for (var j = 0; j < edit_mod_list.length; j++)
                              {
                                  var n = edit_mod_list [j];
                                  $e.attr
                                    ( n
                                    , $e.attr (n).replace (pattern, new_no));
                              }
                          }
                          no = no + 1;
                      });
                  });
              console.log ("Form Submit")
          }
          );
      }
    };
  $.widget ("ui.many2manysubmit", Many2ManySubmit);
})(jQuery);
