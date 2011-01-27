/*
** Copyright (C) 2010-2011 Martin Glueck All rights reserved
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
**    GTW_Form
**
** Purpose
**    Javascipt library form GTW form handling.
**
** Revision Dates
**    25-Feb-2010 (MG) Creation (based on model_edit_ui.js)
**    27-Feb-2010 (MG) `_form_submit` renumeration of forms added
**    12-May-2010 (MG) UI-Display style started
**    12-May-2010 (MG) `s/lid/pid/g`
**    13-May-2010 (MG) Pid and state are now two separate fields, UI-display
**                     continued
**    20-May-2010 (MG) UI-Display style finished
**    28-May-2010 (MG) New form creation bug fixes
**    24-Jun-2010 (MG) Button order and text for popup form are now specified
**                     in the template
**     3-Aug-2010 (MG) Bug with copying link inlines fixed
**    ««revision-date»»···
**--
*/

(function ($)
{
  var _T;
  var _;
  var _Tn;

  if ($.I18N === undefined)
    {
      _T = _ = _Tn = function (t) { return t; }
    }
  else
    {
      _T = _ = $.I18N._T;
      _Tn    = $.I18N._Tn;
    }
  var form_buttons =
      [ { name           : "add"
        , title          : _("Add new form")
        , css_class      : "inline-form-add"
        , add_to_inline  : "false"
        , href           : "#add"
        , enabled        : "cur_count < max_count"
        , icon           : "ui-icon-plusthick"
        , callback       : "_add_new_inline"
        }
      , { name           : "delete"
        , add_to_inline  : "true"
        , href           : "#delete-recover"
        , default_state  : 0
        , states         :
            [ { name     : "delete"
              , title    : _("Delete")
              , enabled  : "cur_count > min_count"
              , icon     : "ui-icon-trash"
              , callback : "_delete_inline"
              }
            , { name     : "recover"
              , title    : _("Undelete")
              , enabled  : "cur_count < max_count"
              , icon     : "ui-icon-plus"
              , callback : "_undelete_inline"
              }
            ]
        }
      , { name           : "rename"
        , href           : "#rename"
        , add_to_inline  : "pid"
        , default_state  : 0
        , states         :
            [ { name     : "unlock"
              , title    : _("Rename")
              , enabled  : "true"
              , icon     : "ui-icon-pencil"
              , callback : "_unlock_inline"
              }
            , { name     : "lock"
              , title    : _("Undo")
              , enabled  : "true"
              , icon     : "ui-icon-arrowreturnthick-1-w"
              , callback : "_revert_inline"
              }
            ]
        }
      , { name           : "copy"
        , title          : _("Copy")
        , add_to_inline  : "pid"
        , href           : "#copy"
        , enabled        : "cur_count < max_count"
        , icon           : "ui-icon-copy"
        , callback       : "_copy_inline"
        }
      , { name           : "clear"
        , title          : _("Clear")
        , add_to_inline  : "pid"
        , href           : "#clear"
        , enabled        : "true"
        , icon           : "ui-icon-circle-close"
        , callback       : "_clear_inline"
        }
      ];

  var field_no_pat = /-M([\dP]+)_/;
  var GTW_Form =
    { _create : function ()
      {
        var i;
        var popup_form_buttons = {};
        var inlines            = this.options.inlines;
        var self               = this;
        this.mandatory_fields  = this.element.find (":input.Mandatory");
        for (i = 0; i < inlines.length; i++)
          {
            if (inlines [i].type == "Link_Inline_UI_Display")
                this._setup_di_inline (inlines [i]);
            else
                this._setup_inline    (inlines [i]);
          }
        this._setup_completers (this.element);
        this.element.find (":submit").bind ("click", this, this._form_submit);
        var $dialog   = $("#form-dialog").dialog ({ autoOpen : false});
        var $buttons  = $dialog.find ("#popup-form-buttons").children ();
        var callbacks =
            { "save"   : function (evt, $form, $inline)
                       {
                         if (! $form)
                           $form = $dialog.find (".gtw-ui-popup-form");
                         $form.data             ("form-save", true);
                         if ($inline)  self._ui_save_form ($inline, $form)
                         else         $dialog.dialog      ("close");
                         return true;
                       }
            , "cancel" : function (evt, $form, $inline)
                       {
                         if (! $form)
                           $form = $dialog.find (".gtw-ui-popup-form");
                         $form.data             ("form-save", false);
                         if ($inline)  self._ui_save_form ($inline, $form)
                         else         $dialog.dialog      ("close");
                         return true;
                       }
            , "reset"  : function (evt, $form, $inline)
                       {
                         if (! $form)
                             $form = $dialog.find (".gtw-ui-popup-form");
                         var prefix = $form.data  ("form-prefix");
                         var data   = $form.data  ("form-data");
                         if (data)
                             self._ui_set_form_values ($form, prefix, data)
                         return false;
                       }
            };
        for (i = $buttons.length - 1; i >= 0; i--)
          {
            var $button = $buttons.eq (i);
            var text = $button.html ()
            var key  = $button.attr ("id").replace ("popup-form-button-", "");
            popup_form_buttons [text] = callbacks [key];
          }
        this.element.data ("popup_form_buttons", popup_form_buttons);
        this.element.data ("$buttons",           $buttons);
        this.element.data ("$dialog",            $dialog);
      }
    , _add_button : function ($element, button, prepend)
      {
        var icon      = button.icon;
        var title     = _T (button.title);
        var css_class = button.css_class;
        if (button.states)
          {
            icon      =     button.states [button.default_state].icon;
            title     = _T (button.states [button.default_state].title);
            css_class =     button.states [button.default_state].css_class;
          }
        if (css_class)
          {
            css_class = ' class="icon-link ' + css_class + '"';
          }
        else
          {
            css_class = ' class="icon-link"'
          }
        var html = '<a href="' + button.href + '"'
                 +   'title="' + title + '"' + css_class
                 + '>'
                 +   '<span class="ui-state-default ui-icon ' + icon + '">'
                 +      button.name
                 +   '</span>'
                 + '</a>'
        if (! prepend) $element.append  (html);
        else           $element.prepend (html);
      }
    , _add_new_inline : function (evt)
      {
        var $inline = $(evt.currentTarget).parents (".inline-root");
        evt.data._copy_form ($inline);
        evt.preventDefault  ();
      }
    , _clear_inline   : function (evt)
      {
        var  self   = evt.data;
        var $form   = $(evt.target).parents (".inline-instance");
        var $inputs = $form.find       (":input")
                           .attr       ("value", "")
                           .removeAttr ("disabled");
        this._clear_internal_fields    ($form, true);
        evt.preventDefault             ();
        evt.stopPropagation            ();
        $inputs.eq (0).focus           ();
      }
    , _clear_internal_fields : function ($form, state)
      {
        /* set pid's to undefined, the state to N (new) */
        $form.find ("input[name$=___pid_]"  ).val ("");
        $form.find ("input[name$=___state_]").val ("");
        if (state)
          {
            /* set the state of ALL inlines to empty */
            $form.find ("input[name$=__instance_state]").val ("");
          }
      }
    , _copy_inline   : function (evt)
      {
        var  self   = evt.data;
        var $inline = $(evt.currentTarget).parents (".inline-root");
        var $source = $(evt.target).parents (".inline-instance");
        var  $new   = self._copy_form ($inline);
        self._restore_form_state      ($new, self._save_form_state ($source));
        this._clear_internal_fields   ($new, true);
        self._update_button_states    ($inline);
        evt.preventDefault            ();
        evt.stopPropagation           ();
      }
    , _copy_form     : function ($inline, form_no)
      {
        var $prototype = $inline.data ("$prototype");
        var $new       = this._copy_form_inner ($inline, form_no) [0];
        /* we are ready to add the new block at the end */
        this._setup_buttons         ($new, $inline.data ("buttons"), $inline);
        $inline.find                (".ui-entities-container").append ($new);
        this._update_button_states  ($inline);
        this._setup_completers      ($inline);
        return $new;
      }
    , _copy_form_inner : function ($inline, form_no)
      {
        var $prototype = $inline.data ("$prototype");
        var $new       = $prototype.clone ().removeClass ("inline-prototype");
        /* now that we have cloned the block, let's change the
        ** name/id/for attributes
        */
        var pattern    = /-MP_/;
        if (form_no === undefined)
          {
            $inline.data ("cur_count", $inline.data ("cur_count") + 1);
            form_no = $inline.data ("cur_number");
            $inline.data ("cur_number", form_no + 1);
          }
        var new_no     = "-M" + form_no + "_";
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
        return [$new, form_no];
      }
    , _delete_inline : function (evt)
      {
        var  self   = evt.data;
        var $inline = $(evt.currentTarget).parents (".inline-root");
        var $proto  = $inline.data                 ("$prototype");
        var $form   = $(evt.target).parents (".inline-instance");
        if ($proto && self._forms_equal ($form, $proto))
        {
            $form.remove ();
        }
        else
        {
            var  button        = form_buttons [1];
            var $link          = $form.find  ("a[href=" + button.href + "]");
            var $button        = $link.find  ("span");
            var $elements      = $form.find  (":input:not([type=hidden])");
            $elements.attr         ("disabled","disabled")
                     .addClass     ("ui-state-disabled");
            $link.attr             ("title", _T (button.states [1].title));
            $button.removeClass    (button.states [0].icon)
                   .addClass       (button.states [1].icon);
            self._state_for_inline ($inline, $form).attr ("value", "U");
        }
        $inline.data ("cur_count", $inline.data ("cur_count") - 1);
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
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
    , _form_submit : function (evt)
      {
        var  self     = evt.data;
        var  pattern  = /M\d+_/;
        var $this     = $(this);
        /* re-enumerate the forms */
        /* first, let's renumerate the inline-instance's */
        self.element.find (".inline-root").each ( function ()
            {
                var $this  = $(this);
                var  no    = 0;
                $this.find (".inline-instance, .ui-entity-container")
                     .each (function ()
                {
                    var $elements      = $(this).find (":input");
                    var  edit_mod_list = ["id", "name"];
                    var  new_no        = "M" + no + "_";
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
        /* re-enable all input elements so that all information is sent to the
        */
        self.element.find (":input").removeAttr ("disabled");
        /* prevent multiple submits use a solution found here:
        ** http://www.norio.be/blog/2008/09/preventing-multiple-form-submissions-revisited
        */
        $this.clone ().insertAfter ($this).attr ("disabled","disabled");
        $this.hide  ();
      }
    , _pid_for_inline : function ($inline, $form)
      {
        return $form.find
          ( "[name^=" + $inline.data ("options").prefix + "]"
          + "[name$=___pid_]"
          );
      }
    , _restore_form_state : function ($form, state)
      {
        var $elements = $form.find  (":input");
        var  form_no  = state ["_form_no_"];
        for (var i = 0; i < $elements.length; i++)
        {
            var $e  = $elements.eq (i);
            var key = $e.attr ("name").replace (field_no_pat, form_no);
            $e.attr ("value", state [key]);
        }
      }
    , _revert_inline   : function (evt)
      {
        var self           = evt.data;
        var $inline        = $(evt.currentTarget).parents (".inline-root");
        var $form          = $(evt.target).parents (".inline-instance");
        var  button        = form_buttons [2];
        var $link          = $form.find  ("a[href=" + button.href + "]");
        var $button        = $link.find  ("span");
        var $elements      = $form.find  (":input");
        self._restore_form_state   ($form, $form.data ("_state"));
        $elements.attr             ("disabled", "disabled");
        $link.attr                 ("title", _T (button.states [0].title));
        $button.removeClass        (button.states [1].icon)
               .addClass           (button.states [0].icon);
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
      }
    , _save_form_state      : function ($form)
      {
        var $elements = $form.find (":input");
        var  match    = field_no_pat.exec ($elements.attr ("name"));
        var  state    = {_form_no_ :  (match || [""]) [0]};
        for (var i = 0; i < $elements.length; i++)
        {
            var $e = $elements.eq (i);
            state [$e.attr ("name")] = $e.attr ("value");
        }
        return state;
      }
    , _setup_buttons : function ($inline_instance, buttons, $inline)
      {
        $inline        = $inline || $inline_instance.parents (".inline-root");
        var $element   = $inline_instance;
        var $first_tag = $element.find (".inline-instance");
        if (! $first_tag.length)
            $first_tag = $element;
        var  first_tag = $first_tag.get (0).tagName.toLowerCase ();
        var  pid       = this._pid_for_inline ($inline, $inline_instance)
                             .attr ("value");
        if (first_tag == "tr")
          {
            var css_class = 'class="width-' + buttons.length + '-icons"';
            var $temp  = $('<td><span ' + css_class + '</span></td>');
            $first_tag.append ($temp);
            $element = $temp.find ("span");
          }
        for (var i = 0; i < form_buttons.length; i++)
          {
            var button = form_buttons [i];
            if (  ($.inArray (button.name, buttons) >= 0)
               && eval (button.add_to_inline)
               )
              {
                this._add_button ($element, button);
              }
          }
      }
    , _setup_completers : function ($root)
    {
      var completers = this.options.completers;
      for (i = 0; i < completers.length; i++)
        {
          var completer = completers [i];
          var prefix    = "[name^=" + completer.field_prefix + "]";
          var middle    = "";
          if (completer.field_postfix)
              middle    = completer.field_postfix + "__";
          for (var field in completer.triggers)
            {
                var options = $.extend ({field : field}, completer);
                $root.find
                    ( prefix + "[name$=" + middle + field + "]"
                    ).MOM_Auto_Complete (options);
            }
        }
    }
    ,  _setup_di_inline : function (inline)
      {
        var $inline = $("." + inline.prefix).addClass ("inline-root");
        var $m2m_range = $inline.find ("input.many-2-many-range:first");
        if ($m2m_range.length)
          {
            var  m2m_range = $m2m_range.attr   ("value").split (":");
            var  cur_count = parseInt (m2m_range [1]);
            var  max_count = parseInt (m2m_range [2]);
            $inline.data ("$m2m_range", $m2m_range);
            $inline.data ("min_count",  parseInt (m2m_range [0]));
            $inline.data ("cur_count",  cur_count);
            $inline.data ("cur_number", cur_count);
            $inline.data ("max_count",  max_count);
          }
        var action = $inline.parents ("form").attr ("action").split ("/");
        var last   = action.pop ();
        if (parseInt (last) == last) action.pop ();
        $inline.data ("base_url", action.join ("/") + "/");
        $inline.data ("prefix",   inline.prefix);
        $inline.data ("popup",    inline.popup);
        var self = this;
        $inline.find ("a[href=#add]").GTW_Button
            ( { icon      : "ui-icon-circle-plus"
              , enabled   : function (btn) { return true; }
              , data      : { self : this , $inline : $inline}
              , callback  : this._ui_add
              }
            );
        $inline.find ("span.ui-icon-circle-triangle-s").GTW_Button
            ( { states   :
                  [ { icon      : "ui-icon-circle-triangle-s"
                    , callback  : this._ui_collapse
                    }
                  , { icon      : "ui-icon-circle-triangle-e"
                    , callback  : this._ui_collapse
                    }
                  ]
              , data      : { self : this }
              , enabled   : function (btn) { return true; }
              }
            );
        $inline.find (".ui-entity-container").each (function () {
            self._setup_di_entity ($(this), $inline);
        });
      }
    , _setup_di_entity : function ($root, $inline)
      {
        $root.find ("a[href=#edit]").GTW_Button
            ( { icon      : "ui-icon-pencil"
              , enabled   : function (btn) { return true; }
              , data      : { self : this , $inline : $inline, copy : false}
              , callback  : this._ui_edit
              }
            );
        $root.find ("span.ui-icon-alert").GTW_Button
            ( { icon      : "ui-icon-alert"
              , enabled   : function (btn) { return true; }
              , data      : { self : this , $inline : $inline, copy : false}
              , callback  : this._ui_edit
              }
            ).css ("cursor", "pointer");
        $root.find ("a[href=#delete]").GTW_Button
            ( { states   :
                  [ { icon      : "ui-icon-trash"
                    , callback  : this._ui_delete_entity
                    }
                  , { icon      : "ui-icon-plus"
                    , callback  : this._ui_delete_entity
                    }
                  ]
              , data    : { self : this }
              , enabled : function (btn) { return true; }
              }
            );
        $root.find ("a[href=#copy]").GTW_Button
            ( { icon      : "ui-icon-copy"
              , enabled   : function (btn) { return true; }
              , data      : { self : this , $inline : $inline, copy : true}
              , callback  : this._ui_edit
              }
            );
        var $pid  = $root.find ("input[name$=___pid_].mom-link");
        var fo_no = field_no_pat.exec ($pid.attr ("name")) [1];
        $root.attr ("id", $inline.data ("prefix") + "-M" + fo_no);
      }
    , _state_for_inline : function ($inline, $form)
      {
        return $form.find
          ( "[name^=" + $inline.data ("options").prefix + "]"
          + "[name$=___state_]"
          );
      }
    , _ui_add           : function (evt, data)
      {
        return data.self._ui_request_form_for ("", data, undefined);
      }
    , _ui_collapse      : function (evt, data)
      {
        var self       = data.self;
        var $container = $(evt.target).parents (".Inline-UI-Display");
        var $header    = $container.find       ("h3 a[href=#hide]");
        var  header    = $header.data          ("content");
        if (! header)
          {
            header = $header.html ();
            $header.data          ("content", header);
          }
        var $body      = $container.find       ("table");
        if ($(evt.target).hasClass ("ui-icon-circle-triangle-e"))
          {
            var count = $container.data ("cur_count");
            $body.slideUp   ();
            $header.html    (header + " (" + count + ")");
          }
        else
          {
            $body.slideDown ();
            $header.html    (header);
          }
      }
    , _ui_convert_to_flat_data : function (prefix, data, flat)
      {
        for (var key in data)
          {
            var name  = prefix + "__" + key;
            var value = (key == "_state_" ? "" : data [key]);
            if (typeof value == "object")
                this._ui_convert_to_flat_data (name, value, flat);
            else
                flat [name] = value;
          }
      }
    , _ui_data_as_post_dict : function ($root, prefix, post)
      {
        $root.find ("[name^=" + prefix + "]").each (function () {
          post [this.name] = $(this).val ();
        });
        return post;
      }
    , _ui_delete_entity : function (evt, data)
      {
        var self       = data.self;
        var $container = $(evt.target).parents (".ui-entity-container")
        var $ui        = $container.find       (".ui-display");
        var state      = "";
        if ($ui.hasClass ("ui-state-disabled"))
          {
            $ui.removeClass ("ui-state-disabled");
          }
        else
          {
            $ui.addClass    ("ui-state-disabled");
            state      = "U";
          }
        $container.find ("input:hidden:first[name$=__state_]")
                  .attr ("value", state);
      }
    , _ui_display_form : function ($dialog, $form, $inline, $entity_root)
      {
        $form.removeClass ("ui-helper-hidden");
        if ($inline.data ("popup"))
          {
            $dialog.empty ().append ($form)
                   .dialog ("option", "title", $form.data ("form-title"))
                   .dialog ("open");
          }
        else
          {
            var $iform =
              $( '<tr><td colspan="100" class="gtw-ui-form-inline">'
               +   '<div class="gtw-ui-form-inline-container"></div>'
               + '</td></tr>'
               );
            $iform.find      (".gtw-ui-form-inline-container")
                  .append    ($form)
                  .append    ('<div class="buttons"></div>')
                  .resizable ({ handles : "e"});
            var $buttons = this.element.data ("$buttons")
            var popup_form_buttons = this.element.data ("popup_form_buttons");
            for (var i = 0; i< $buttons.length; i++)
              {
                var $button  = $buttons.eq (i).clone ();
                var text     = $button.html ()
                $iform.find    ("div.buttons").append ($button);
                $button.data   ("callback", popup_form_buttons [text]);
                $button.button ().click
                  ( function (evt)
                      { evt.preventDefault        ();
                        evt.stopPropagation       ();
                        $form.data  ("inline-width", $iform.width () + "px");
                        if ($(this).data ("callback") (evt, $form, $inline))
                          {
                            $iform.remove             ();
                            if ($entity_root)
                                $entity_root.show     ();
                          }
                      }
                  );
              }
            if ($entity_root === undefined)
              {
                var $table = $inline.find (".ui-entities-container");
                var $last  = $table.find  (".ui-entity-container:last");
                if ($last.length) $last.after   ($iform);
                else              $table.append ($iform);
              }
            else
              {
                $entity_root.after ($iform);
                $entity_root.hide  ();
              }
            $iform.find  (".gtw-ui-form-inline-container")
                  .width ($form.data ("inline-width") || "auto");
          }
        this._setup_completers ($form);
      }
    , _ui_edit          : function (evt, data)
      {
        var $pid  = $(evt.target).parents (".ui-entity-container")
                                 .find    ("input[name$=___pid_].mom-link");
        var fo_no = undefined;
        if (! data.copy)
            fo_no = field_no_pat.exec ($pid.attr ("name")) [1];
        return data.self._ui_request_form_for ($pid.val (), data, fo_no);
      }
    , _ui_request_form_for : function (pid, data, no)
      {
        var  self       = data.self;
        var $inline     = data.$inline;
        var url         = $inline.data ("base_url")
                        + "form/" + $inline.data ("prefix");
        var $prototype  = $inline.data ("$prototype");
        if (! $prototype)
          {
            $.ajax
                ( { url     : url
                  , type    : "GET"
                  , success : function (prototype, textStatus, xmlreq)
                      {
                        var $prototype = $(prototype);
                        $inline.data ("$prototype", $prototype);
                        self._ui_show_form_for ($inline, no, pid);
                      }
                  , error   : function (xmlreq, textStatus, error)
                      {
                        var $dialog = self.element.data ("$dialog");
                        $dialog.dialog
                          ( "option"
                          , { title   : "Communication Error"
                            , buttons :
                                { "Ok": function() { $(this).dialog("close");}}
                            }
                          );
                        $dialog.empty ().append ("Error receiving the form!");
                        $dialog.dialog ("open");
                      }
                  }
               )
          }
        else
            self._ui_show_form_for ($inline, no, pid);
        return false;
      }
    , _ui_save_form : function ($inline, $form)
      {
        var $dialog      = this.element.data ("$dialog");
        if (! $form)
           $form = $dialog.find        (".gtw-ui-popup-form");
        var old_data     = $form.data ("form-data");
        var form_save    = $form.data ("form-save");
        var name         = $form.find (":input").attr ("name");
        var no           = field_no_pat.exec (name) [1];
        var prefix       = $inline.data ("prefix") + "-M" + no;
        var $entity_root = $("#" + prefix);
        var new_entity   = $entity_root.length == 0;
        if (!form_save && old_data)
            this._ui_set_form_values ($form, prefix, old_data);
        if ($form.data ("form-is-new") && !form_save)
          {
            $inline.data ("cur_count", $inline.data ("cur_count") - 1);
          }
        var new_data     = {};
        $form.data  ("form-save", false);
        if (  (new_entity && form_save)
           || this._ui_update_form_values (prefix, old_data, new_data)
           )
          {
            var url       = $inline.data ("base_url")
                          + "test/" + $inline.data ("prefix");
            var post_data = {__FORM_NO__ : no, __NEW__ : new_entity};
            this.mandatory_fields.each (function (idx)
              {
                var $this = $(this);
                post_data [$this.attr ("name")] = $this.val ();
              });
            var self      = this;
            $.ajax
              ( { url      : url
                , type     : "POST"
                , data     : this._ui_data_as_post_dict
                    ($form, prefix, post_data)
                , dataType : "html"
                , success  : function (data, textStatus, xmlreq)
                   {
                     var $data = $(data);
                     if (  $data.hasClass ("ui-display")
                        || $data.hasClass ("ui-entity-container")
                        )
                       {
                         if (new_entity)
                           {
                             $inline.find   (".ui-entities-container")
                                    .append ($data);
                             $data.addClass ("ui-display-changed");
                             $entity_root = $data;
                           }
                         else
                           {
                             $entity_root.find (".ui-display").remove ()
                                         .end  ().prepend ($data)
                                         .addClass ("ui-display-changed");
                           }
                         $entity_root.data  ("form-data", post_data);
                         $form.find (".ui-state-error").remove ();
                         self._ui_hide_form ($entity_root, $form);
                         /* must be done after the form is hidden */
                         if (new_entity)
                             self._setup_di_entity ($entity_root, $inline);
                         else
                           {
                              $entity_root.find ("a[href=#edit]").GTW_Button
                                ( { icon      : "ui-icon-pencil"
                                  , enabled   : function (btn) { return true; }
                                  , data      :
                                      { self    : self
                                      , $inline : $inline
                                      , copy    : false
                                      }
                                  , callback  : self._ui_edit
                                  }
                                 );
                           }
                       }
                     else
                       {
                         var attrs = ["form-is-new", "form-prefix"];
                         $data.addClass ("gtw-ui-popup-form");
                         $data.data ("form-data", post_data);
                         for (var i = 0; i < attrs.length; i++)
                             $data.data (attrs [i], $form.data (attrs [i]));
                         self._ui_display_form
                             ($dialog, $data, $inline, $entity_root);
                       }
                   }
                 }
              );
          }
        else
          {
            $entity_root.data  ("form-data", new_data);
            this._ui_hide_form ($entity_root, $form);
          }
      }
    , _ui_set_form_values : function ($root, prefix, data)
      {
        $root.find ("[name^=" + prefix + "]").each (function () {
          $(this).val (data [this.name]);
        });
      }
    , _ui_show_form_for : function ($inline, no, pid)
      {
         var  add_or_copy = no === undefined;
         var $dialog      = this.element.data ("$dialog");
         var $entity_root = undefined;
         var  prefix      = $inline.data ("prefix") + "-M" + no;
         var $form        = undefined;
         var  self        = this;
         $dialog.empty ();
         if (no)
             $entity_root = $("#" + prefix);
         $dialog.dialog
           ( "option"
           , { width        : "auto"
             , "buttons"    : this.element.data ("popup_form_buttons")
             }
           ).unbind ("dialogbeforeclose")
            .bind   ("dialogbeforeclose", function (evt, ui) {
             return self._ui_save_form ($inline);
           }).data ("form-save", false);
         if (! $entity_root || ! $entity_root.hasClass ("mom-populated"))
           {
             var  temp        = this._copy_form_inner ($inline, no);
             $form            = temp [0];
             $form.data ("form-is-new", no === undefined);
             no               = temp [1];
             prefix           = $inline.data ("prefix") + "-M" + no;
             this._clear_internal_fields ($form, add_or_copy);
             $form.addClass ("gtw-ui-popup-form");
             if (pid)
               {
                 var url  = $inline.data ("base_url")
                          + "fields/" + $inline.data ("prefix");
                 $.ajax
                   ( { url      : url
                     , type     : "GET"
                     , data     : {pid : pid, edit : (add_or_copy ? 0 : 1)}
                     , dataType : "json"
                     , success  : function (hdata, textStatus, xmlreq)
                       {
                         var data = {};
                         self._ui_convert_to_flat_data (prefix, hdata, data);
                         self._ui_set_form_values  ($form, prefix, data);
                         $form.data     ("form-data",       data);
                         $form.data     ("form-prefix",     prefix);
                         $form.data     ("form-title",      hdata.puf_title);
                         if (add_or_copy)
                             self._clear_internal_fields ($form, true);
                         self._ui_display_form
                             ($dialog, $form, $inline, $entity_root);
                       }
                     }
                   );
               }
             else
               {
                 $form.data ("form-title", "New");
                 this._ui_display_form ($dialog, $form, $inline, $entity_root);
               }
           }
         else
           {
             var data = $entity_root.data ("form-data");
             $form    = $entity_root.find (".gtw-ui-popup-form");
             $form.data                   ("form-is-new", false);
             $form.data                   ("form-prefix", prefix);
             $form.data                   ("form-data",   data);
             if (data)
                 $dialog.dialog ("option", "title", data.puf_title);
             this._ui_display_form
                 ($dialog, $form, $inline, $entity_root);
           }
      }
    , _ui_hide_form          : function ($entity_root, $form)
      {
        var $container   = $entity_root.addClass ("mom-populated")
                                       .find     (".ui-display:first");
        $container.find  (".mom-link, .mom-object").remove ();
        $form.addClass ("ui-helper-hidden")
             .appendTo ($container);
      }
    , _ui_update_form_values : function (prefix, data, new_data)
      {
        var changed = 0;
        for (var name in data)
          {
            var $field = $("[name=" + name + "]");
            if ($field.length && (name.substr (name.length - 7) != "_state_"))
              {
                var old_value   = data [name];
                var new_value   = $field.val ();
                new_data [name] = new_value || old_value;
                if ((new_value !== undefined) && (old_value != new_value))
                    changed   += 1;
              }
          }
        return changed;
      }
    , _setup_inline : function (inline)
      {
        var $inline    = $("." + inline.prefix);
        var $prototype = $inline.find (".inline-prototype").remove ()
        var  buttons   = inline ["buttons"];
        $inline.data ("options", inline);
        /* if we have found a prototype we can have the add button */
        if ($prototype.length)
          {
            var $m2m_range = $inline.find ("input.many-2-many-range:first");
            var  m2m_range = $m2m_range.attr   ("value").split (":");
            var  cur_count = parseInt (m2m_range [1]);
            var  max_count = parseInt (m2m_range [2]);
            $inline.data ("$prototype", $prototype);
            $inline.data ("$m2m_range", $m2m_range);
            $inline.data ("min_count",  parseInt (m2m_range [0]));
            $inline.data ("cur_count",  cur_count);
            $inline.data ("cur_number", cur_count);
            $inline.data ("max_count",  max_count);
            this._add_button ($inline.find ("legend"), form_buttons [0], true);
          }
        else
          {
            $inline.data ("min_count",  0);
            $inline.data ("cur_count",  1);
            $inline.data ("cur_number", 0);
            $inline.data ("max_count",  1);
          }
        $inline.data     ("buttons", buttons);
        $inline.addClass ("inline-root");
        var self = this;
        $inline.find
          ("." + inline.instance_class + ":not(.inline-prototype)").each
            (function ()
              {
                var $this   = $(this);
                self._setup_buttons   ($this, buttons);
                var $pid = $this.find ("input[name$=___pid_]");
                if (inline.initial_disabled && $pid.attr ("value"))
                    $this.find (":input").attr ("disabled", "disabled");
              }
            );
        this._update_button_states ($inline);
      }
    , _undelete_inline : function (evt)
      {
        var self           = evt.data;
        var $inline        = $(evt.currentTarget).parents (".inline-root");
        var $proto         = $inline.data ("$prototype");
        var $form          = $(evt.target).parents (".inline-instance");
        var  button        = form_buttons [1];
        var $link          = $form.find  ("a[href=" + button.href + "]");
        var $button        = $link.find  ("span");
        var $elements      = $form.find  (":input:not([type=hidden])");
        var  new_state     = "";
        if (! self._pid_for_inline ($inline, $form).attr ("value"))
        {
            $elements.removeAttr ("disabled")
        }
        $elements.removeClass ("ui-state-disabled");
        $inline.data ("cur_count", $inline.data ("cur_count") + 1);
        self._state_for_inline ($inline, $form).attr ("value", new_state);
        $link.attr                 ("title", _T (button.states [0].title));
        $button.removeClass        (button.states [1].icon)
               .addClass           (button.states [0].icon);
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
      }
    , _unlock_inline   : function (evt)
      {
        var self         = evt.data;
        var $inline      = $(evt.currentTarget).parents (".inline-root");
        var $form        = $(evt.target).parents (".inline-instance");
        var  button      = form_buttons [2];
        var $link        = $form.find    ("a[href=" + button.href + "]");
        var $button      = $link.find    ("span");
        var $elements    = $form.find    (":input");
        var  link_prefix = $inline.data ("options").prefix;
        $form.data                 ("_state", self._save_form_state ($form));
        $elements.removeAttr       ("disabled")
        $link.attr                 ("title", _T (button.states [1].title))
        $button.removeClass        (button.states [0].icon)
               .addClass           (button.states [1].icon);
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
      }
    , _update_button_state  : function ( $root
                                       , cur_count, min_count, max_count
                                       , button, state
                                       )
    {
        var  href    = state.href || button.href;
        var $buttons = $root.find
            ('a[href=' + href + '] .' + state.icon.split (" ") [0])
        /* remove old handlers */
        $buttons.unbind ("click")
        if (eval (state.enabled))
        {
            var cb = this [state.callback];
            $buttons.bind   ("click", this, cb)
                    .parent ().removeClass ("ui-state-disabled");
        }
        else
        {
            $buttons.parent ().addClass ("ui-state-disabled");
        }
    }
    , _update_button_states : function ($root)
      {
        var  cur_count = $root.data ("cur_count");
        var  min_count = $root.data ("min_count");
        var  max_count = $root.data ("max_count");
        var $range     = $root.data ("$m2m_range");
        if ($range)
            $range.attr ("value", [min_count, cur_count, max_count].join (":"));
        for (var i = 0; i < form_buttons.length; i++)
        {
            var button        = form_buttons [i];
            if (button.states)
            {
                for (var si = 0; si < button.states.length; si++)
                {
                    this._update_button_state
                        ( $root, cur_count, min_count, max_count
                        , button, button.states [si]
                        );
                }
            }
            else
            {
                this._update_button_state
                    ($root, cur_count, min_count, max_count, button, button);
            }
        }
      }
    };
  $.widget ("ui.GTW_Form", GTW_Form);
  $.extend
      ( $.ui.GTW_Form
      , { "version"      : "0.1"
        , "defaults"     :
          {
          }
        }
      )
  $.fn.reverse = [].reverse;
})(jQuery);
