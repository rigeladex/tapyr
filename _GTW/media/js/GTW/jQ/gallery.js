//-*- coding: utf-8 -*-
// Copyright (C) 2010-2015 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
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
//    30-Nov-2011 (CT) Use `return false` instead of `.preventDefault`
//     8-Apr-2014 (CT) Remove `css` rule to hide `overflow` to `th_div$`
//     5-Dec-2014 (CT) Add `gallery$`, click-binding for `photo_selector`
//    23-Jun-2015 (CT) Use `pure-button` with font-awesome icons
//    ««revision-date»»···
//--

( function ($) {
    "use strict";
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
            ( { delay               : 3000
              , gallery_selector    : ".gallery"
              , inline_selector     : ".inline"
              , photo_selector      : ".photo img"
              , play_class          : "playing"
              , selected_class      : "selected"
              , url_transformer     : function (name)
                  { return name.replace (/\/th\//, "/im/"); }
              }
            , opts || {}
            , { controls            : controls }
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
            var photo = $(options.photo_selector, gallery$);
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
            $(options.controls.play, gallery$)
                .unbind   ("click")
                .click    (stop)
                .find     (".fa")
                    .addClass     ("fa-stop")
                    .removeClass  ("fa-play");
            next ();
        };
        var stop = function (event) {
            window.clearInterval (options.play_cb);
            $(options.controls.play, gallery$)
                .unbind   ("click")
                .click    (start)
                .find     (".fa")
                    .addClass     ("fa-play")
                    .removeClass  ("fa-stop");
        };
        var gallery$        = this.closest (options.gallery_selector);
        options.current     = 0;
        options.th_div$     = this;
        options.th_box$     = $(".box", this);
        options.thumbnails$ = $("img",  this);
        options.thumbnails$
            .each ( function (n) { $(this).data ("GTW-gallery-index", n); })
            .click
                ( function (ev) {
                    stop (ev);
                    return show ($(this).data ("GTW-gallery-index"), ev);
                  }
                );
        $(options.controls.next, gallery$)
            .click (function (ev) { stop (ev); return next (ev); });
        $(options.controls.prev, gallery$)
            .click (function (ev) { stop (ev); return prev (ev); });
        $(options.controls.head, gallery$)
            .click (function (ev) { stop (ev); return show (0, ev); });
        $(options.controls.tail, gallery$)
            .click (function (ev) { stop (ev); return show (-1, ev); });
        $(options.controls.play, gallery$)
            .click (start);
        $(options.photo_selector, gallery$)
            .click (function (ev) { stop (ev); return next (ev); });
        $(options.inline_selector, gallery$).show ();
        this.addClass ("inline");
        show (0);
        return this;
    };
  }
) (jQuery);

// __END__ GTW_Gallery.js
