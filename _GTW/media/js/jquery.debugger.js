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
**    jquery.debugger
**
** Purpose
**    Javascipt library to provide the interactive python console.
**    This script is based on the debugger.js from werkzeug
**    (http://werkzeug.pocoo.org/)
**
** Revision Dates
**     2-Aug-2010 (MG) Creation
**     3-Aug-2010 (MG) Clear button added
**    ��revision-date�����
**--
*/

(function ($)
{

  // if we have javascript we submit by ajax anyways, so no need for the
  // not scaling textarea.
  var plainTraceback = $("div.plain textarea");
  plainTraceback.replaceWith ($("<pre>").text (plainTraceback.text ()));

/**
 * Helper function for shell initialization
 */
function open_shell ($consoleNode, frameID)
{
  var $target = this.find ("div.inner").empty ();
  var  href   = $(location).attr ("href");
  if ($consoleNode)
    return $consoleNode.slideToggle ("fast");
  var $consoleNode = $('<pre class="console">')
      .appendTo       ($target.parent ())
      .hide           ();
  $(this).parent ().resizable   ({handles: "se"});
  var historyPos = 0
    var history  = [""];
  var $output    = $('<div class="output">[console ready]</div>')
    .appendTo       ($consoleNode);
  var $form = $('<form><span id="Py-Console-Prompt">&gt;&gt;&gt;</span> </form>')
    .submit (function()
        {
          var cmd = $command.val ();
          $.getJSON
                ( href
                , {cmd: cmd}
                , function (data)
                    {
                      var $tmp = $("<div>").html (data.html);
                      $("span.extended", $tmp).each (function ()
                        {
                          var $hidden = $(this).wrap ("<span>").hide ();
                          $hidden
                            .parent ()
                            .append ($('<a href="#" class="toggle">&nbsp;&nbsp;</a>')
                            .click (function ()
                              {
                                $hidden.toggle      ();
                                $(this).toggleClass ("open")
                                return false;
                              }));
                        });
                      $output.append ($tmp);
                      var prompt = "&gt;&gt;&gt;";
                      if (data.more)
                        prompt   = "...";
                      $form.find     ("#Py-Console-Prompt").html (prompt);
                      $command.focus ();
                      var old = history.pop ();
                      history.push          (cmd);
                      if (typeof old != "undefined") history.push(old);
                      historyPos = history.length - 1;
                    });
          $command.val ("");
          return false;
        }).
    appendTo   ($consoleNode);
  var $compNode = $('<div class="completion"></div>').appendTo (this);
  var $command = $('<input type="text">')
    .appendTo  ($form)
    .keydown   (function(e)
      {
        if (e.which == 100 && e.ctrlKey)
          {
            $output.text ("--- screen cleared ---");
            return false;
          }
        else if (e.which == 9)
          {
            var cmd = $(this).val ();
          $.getJSON
                ( href
                , {complete: cmd}
                , function (data)
                    {
                      $compNode.empty ();
                      if (!data.completed)
                        $compNode.html (data.cands);
                      $command.val     (data.input);
                    });
            return false;
          }
        else if (e.charCode == 0 && (e.keyCode == 38 || e.keyCode == 40))
          {
            if      (e.keyCode == 38 && historyPos > 0)
              historyPos--;
            else if (e.keyCode == 40 && historyPos < history.length)
              historyPos++;
            $command.val (history [historyPos]);
            return false;
          }
      });
  $(this).parent ().find ("button").click
    ( function (evt)
        {
          $output.text   ("--- screen cleared ---");
          $command.focus ();
          return false;
        }
      );

  return $consoleNode.slideDown ("fast", function() {$command.focus (); });
}

$.fn.open_shell = open_shell;
})(jQuery);
