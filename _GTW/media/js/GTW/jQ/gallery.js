//-*- coding: utf-8 -*-
// Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW_Gallery
//
// Purpose
//    jQuery plugin for a photo gallery
//
//
// Revision Dates
//     7-Oct-2010 (CT) Creation
//     8-Oct-2010 (CT) Creation continued
//    30-Nov-2010 (CT) Calls to `.button` added
//    30-Nov-2010 (CT) `scroll` added and used
//    20-Jan-2011 (CT) Rename function `GTW_Gallery` to `gtw_gallery`
//    26-Jan-2011 (CT) Style change
//    30-Nov-2011 (CT) Use `return false` instead of .`preventDefault`
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    $.fn.gtw_gallery = function (opts) {
        var controls = $.extend
            ( { head        : "button.first"
              , next        : "button.next"
              , play        : "button.play"
              , prev        : "button.prev"
              , tail        : "button.last"
              }
            , opts && opts ["controls"] || {}
            );
        var options  = $.extend
            ( { delay           : 3000
              , inline_selector : ".gallery .inline"
              , photo_selector  : ".photo img"
              , play_class      : "playing"
              , selected_class  : "selected"
              , url_transformer : function (name)
                  { return name.replace (/\/th\//, "/im/"); }
              }
            , opts || {}
            , { controls        : controls }
            );
        var scroll = function (thumb$) {
            var w1  = options.th_div$.width ();
            var w2  = options.th_box$.width ();
            var pos, left;
            if (w1 < w2) {
                options.th_box$.css    ("margin-left", 0);
                pos  = thumb$.position ();
                if ((pos.left + thumb$.width ()) > w1) {
                    left = Math.min (pos.left, w2 - w1);
                    options.th_box$.css ("margin-left", "-" + left + "px");
                };
            };
        };
        var show = function (index, event) {
            var len   = options.thumbnails$.length;
            var photo = $(options.photo_selector);
            var alt   = photo.attr ("alt");
            var thumb, url;
            if (index < 0) {
                index += len;
            };
            $(options.thumbnails$ [options.current]).removeClass ("selected");
            index = options.current = index % len;
            thumb = options.thumbnails$ [index];
            url   = options.url_transformer (thumb.src);
            photo.attr (
                { src   : url
                , title :
                    (alt ? alt + ":" : "Photo") + " " + (index+1) + "/" + len
                }
            );
            scroll ($(thumb));
            $(thumb).addClass ("selected");
            return false;
        };
        var next  = function (event) { return show (options.current + 1, event); };
        var prev  = function (event) { return show (options.current - 1, event); };
        var start = function (event) {
            options.play_cb = window.setInterval (next, options.delay);
            $(options.controls.play)
                .addClass (options.play_class)
                .unbind   ("click")
                .click    (stop)
                .button
                    ({ icons : { primary : "ui-icon-pause" }, text : false });
            next ();
        };
        var stop = function (event) {
            if ($(options.controls.play).hasClass (options.play_class)) {
                window.clearInterval (options.play_cb);
                $(options.controls.play)
                    .unbind      ("click")
                    .click       (start)
                    .removeClass (options.play_class)
                    .button
                        ({ icons: { primary: "ui-icon-play" }, text: false });
            };
        };
        this.addClass ("inline");
        options.current = 0;
        options.th_div$     = this;
        options.th_box$     = $(".box", this);
        options.thumbnails$ = $("img",  this);
        options.th_div$.css ("overflow", "hidden");
        options.thumbnails$
            .each ( function (n) { $(this).data ("GTW-gallery-index", n); })
            .click
                ( function (ev) {
                    stop (ev);
                    return show ($(this).data ("GTW-gallery-index"), ev);
                  }
                );
        $(options.controls.next)
            .click (function (ev) { stop (ev); return next (ev); })
            .button
                ({ icons : { primary : "ui-icon-seek-next" }, text : false });
        $(options.controls.prev)
            .click (function (ev) { stop (ev); return prev (ev); })
            .button
                ({ icons : { primary : "ui-icon-seek-prev" }, text : false });
        $(options.controls.head)
            .click (function (ev) { stop (ev); return show (0, ev); })
            .button
                ({ icons : { primary : "ui-icon-seek-start" }, text : false });
        $(options.controls.tail)
            .click (function (ev) { stop (ev); return show (-1, ev); })
            .button
                ({ icons : { primary : "ui-icon-seek-end" }, text : false });
        $(options.controls.play)
            .click  (start)
            .button ({ icons : { primary : "ui-icon-play" }, text : false });
        $(options.inline_selector).show ();
        show (0);
        return this;
    };
  }
) (jQuery);

// __END__ GTW_Gallery.js
