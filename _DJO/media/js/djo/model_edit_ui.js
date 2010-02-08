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
**    21-Aug-2009 (MG) Keyboard shortcuts added
**     2-Feb-2010 (MG) Adopted to GTW framework
**     3-Feb-2010 (MG) Swiched form states from int's to char's
**     3-Feb-2010 (MG) Correct form count on submit
++     5-Feb-2010 (MG) `suffix` option added to auto completion
**     6-Feb-2010 (MG) Completion finished
**    ««revision-date»»···
**--
*/

(function ($)
{
  var field_no_pat   = /-M([\dP]+)-/;

  var Many2Many =
    { _init : function ()
      {
          var  self      = this;
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
          /* extract all real forms */
          var $forms = this.element.find (".m2m-inline-instance");
          for (var i = 0; i < $forms.length; i++)
          {
              this._add_delete_button ($forms.eq (i));
          }
          this.element.parents       ("form").many2manysubmit ();
          this._update_button_states ();
          this.element.find (":input[name$=-_lid_a_state_]").each (function ()
          {
              var $this      = $(this);
              var  lid_state = $this.attr   ("value").split (":");
              var  lid       = lid_state [0];
              var  state     = lid_state [1];
              if (state != "P")
              {
                  if (lid)
                      $(this).parents (".m2m-inline-instance")
                             .find    (":input:not([type=hidden])")
                             .attr    ("disabled", "disabled");
                  else
                  {
                      var no = field_no_pat.exec (this.name) [1];
                      self._setup_auto_complete  (no);
                  }
              }
          });
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
      }
    , _add_new_form : function (evt)
      {
          var self       = evt.data;
          var $prototype = self._getData    ("$prototype");
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
          self._setup_auto_complete  (cur_number);
          $new.find ("input[name$=-_lid_a_state_]").attr ("value", ":N");
          evt.preventDefault ();
      }
    , _setup_auto_complete  : function (no)
      {
          var $prototype = this._getData    ("$prototype");
          var  comp_opt  = $prototype.data  ("completion");
          if (comp_opt != undefined)
          {
              var  pf    = comp_opt.prefix + "-M" + no + "-" + comp_opt.suffix;
              for (var field_name in comp_opt.triggers)
              {
                  var real_field_name = pf + field_name;
                  $("[name=" + real_field_name + "]").bind
                      ( "keyup"
                      , {comp_opt : comp_opt, self : this}
                      , this._auto_complete
                      ).bind
                      ( "keypress"
                      , {comp_opt : comp_opt, self : this}
                      , this._auto_complete_navigation
                      );;
              }
          }
      }
    , _auto_complete_navigation : function (evt)
    {
        var  self      = evt.data.self;
        var  comp_opt  = evt.data.comp_opt;
        var $comp_list = $("#" + comp_opt.prefix + "-comp-list");
        var  handled   = false;
        if ($comp_list.length)
        {
            var $curr_selected = $comp_list.find     (".ui-state-hover");
            var $all           = $comp_list.children ();
            var  curr_idx      = $all.index          ($curr_selected);
            switch (evt.keyCode)
            {
                case 40 : curr_idx += 1;
                          handled = true;
                          break;
                case 38 : curr_idx -= 1;
                          handled = true;
                          break;
                case 27 : $comp_list.remove ();
                          handled = true;
                          break;
                case  9 :
                case 13 : $comp_list.remove ();
                          $comp_list.remove ();
                          self._replace_form (evt, $curr_selected, comp_opt);
                          handled = true;
                          break;
            }
            if (handled)
            {
                if (curr_idx <  0          ) curr_idx = $all.length - 1;
                if (curr_idx >= $all.length) curr_idx = 0;
                $curr_selected.    removeClass  ("ui-state-hover");
                $all.eq (curr_idx).addClass     ("ui-state-hover");
                evt.preventDefault  ();
                evt.stopPropagation ();
                self._setData       ("key_handled", true);
                return false;
            }
        }
    }
    , _auto_complete        : function (evt)
    {
        var data     = {};
        var self     = evt.data.self;
        if (self._getData ("key_handled"))
        {
            evt.preventDefault  ();
            evt.stopPropagation ();
            self._setData      ("key_handled", false);
            return false
        }
        var comp_opt = evt.data.comp_opt;
        var trigger  = evt.currentTarget.name.split (field_no_pat) [2];
        trigger      = comp_opt.triggers[trigger.replace (comp_opt.suffix, "")];
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
            var sf = comp_opt.suffix;
            for (var i = 0;  i < trigger.fields.length; i++)
            {
                var mfn   = trigger.fields [i];
                var value =  $("[name=" + pf + sf + mfn + "]").attr ("value");
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
                                        , input     : evt.currentTarget
                                        };
                        var $auto_complete = $(data).attr ("id", id);
                        if ($auto_complete.find (".completion-id").length)
                        {
                            var $input = $(evt.currentTarget);
                            var  pos   = $input.position ();
                            pos.left += $input.width  ();
                            $("#" + id).remove (); /* remove old display */
                            $input.parent ().append ($auto_complete);
                            $auto_complete.css      (pos)
                                          .children ()
                                          .bind ( "click", function (e)
                              {
                                  self._replace_form
                                    (evt, $(e.currentTarget), comp_opt);
                              })
                                          .hover (function (e)
                              {
                                  $(this).addClass ("ui-state-hover");
                              }, function (e)
                              {
                                  $(this).removeClass ("ui-state-hover");
                              });
                        }
                    }
                }
              )
        }
    }
    , _replace_form : function (evt, $selected, comp_opt)
    {
        var id = comp_opt.prefix + "-comp-list";
        var pk = $selected.find    (".completion-id").text ();
        var no = field_no_pat.exec (evt.currentTarget.name) [1];
        var pf = comp_opt.prefix + "-M" + parseInt (no) + "-" + comp_opt.suffix;
        jQuery.getJSON
          ( comp_opt.obj_url
          , { "lid" : pk, "no" : no}
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
    , _update_button_states : function ()
      {
          var $add_button = this.element.find ("legend a[href=#add]");
          var cur_count   = this._getData ("cur_count");
          var min_count   = this._getData ("min_count");
          var max_count   = this._getData ("max_count");
          var $undeletes  = this.element.find
              ("a[href=#delete].ui-icon-circle-close");
          var $deletes    = this.element.find
              ("a[href=#delete].ui-icon-closethick");
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
          var $l_value_elements = $l.find ("[value]:not([type=hidden])");
          var $r_value_elements = $r.find ("[value]:not([type=hidden])");
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
          var self   = evt.data;
          var $proto = self._getData         ("$prototype");
          var $form  = $(evt.target).parents (".m2m-inline-instance");
          if (self._forms_equal ($form, $proto))
          {
              $form.remove ();
              self._setData ("cur_count", self._getData ("cur_count") - 1);
          }
          else
          {
              var $link      = $form.find  ("a[href=#delete]");
              var $elements  = $form.find  (":input:not([type=hidden])");
              var $l_a_s     = $form.find  ("input[name$=-_lid_a_state_]");
              var  lid       = $l_a_s.attr ("value").split (":") [0];
              var  new_state = "L";
              if ($link.hasClass ("ui-icon-closethick"))
              {
                  new_state = "U";
                  $elements.attr        ("disabled","disabled")
                           .addClass    ("ui-state-disabled");
                  $link.removeClass     ("ui-icon-closethick ui-icon-delete")
                       .addClass        ("ui-icon-circle-close ui-icon-add");
                  self._setData ("cur_count", self._getData ("cur_count") - 1);
              }
              else
              {
                  if (lid)
                  {
                      new_state = "L";
                  }
                  else
                  {
                      new_state = "N";
                      $elements.removeAttr  ("disabled")
                  }
                  $elements.removeClass ("ui-state-disabled");
                  $link.removeClass     ("ui-icon-circle-close ui-icon-add")
                       .addClass        ("ui-icon-closethick ui-icon-delete");
                  self._setData ("cur_count", self._getData ("cur_count") + 1);
              }
              $l_a_s.attr ("value", [lid, new_state].join (":"));
          }
          self._update_button_states ();
          evt.preventDefault         ();
      }
    }
  $.widget ("ui.many2many", Many2Many);
  $.extend
    ( $.ui.many2many
    , { version                          : "0.2.ui-icon-circle-close"
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
        , suffix                         : ""
        , field_prefix                   : ""
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
              /* first, let's renumerate the inline-instance's */
              self.element.find (".m2m-inline-form-table").each ( function ()
                  {
                      var $this  = $(this);
                      var  no    = -1; /* the first is the prototype */
                      $this.find (".m2m-inline-instance").each (function ()
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
                                    , $e.attr (n).replace (pattern, new_no)
                                    );
                              }
                          }
                          no = no + 1;
                      });
                      var $m2m_range = $this.find (".many-2-many-range:first");
                      var  m2m_range = $m2m_range.attr ("value").split (":");
                      m2m_range [1]  = no;
                      $m2m_range.attr ("value", m2m_range.join (":"));
                  });
              /* now, let's re-enable all input's so that they are set to the
              ** server
              */
              self.element.find (":input").removeAttr ("disabled");
          }
          );
      }
    };
  $.widget ("ui.many2manysubmit", Many2ManySubmit);
})(jQuery);
