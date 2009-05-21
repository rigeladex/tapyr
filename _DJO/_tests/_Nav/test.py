# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@smangari.org
#
#++
# Name
#    test
#
# Purpose
#    Test the navigation using py.test and the test client from Django
#
# Revision Dates
#     6-Oct-2008 (MG) Creation
#    ««revision-date»»···
#--

import  os
os.environ ["DJANGO_SETTINGS_MODULE"] = "_DJO._test._Nav.settings_test"

from   _DJO                    import DJO
import _DJO._Test.Client
import _DJO._Test.Database

from   _TFL.predicate          import pairwise

c = DJO.Test.Client ()

TOP_LEVEL_MENU_ITEMS = 7

def test_404_error () :
    response = c.get ("/page-does-not-exist", status_code = 404)
    assert response.check_templates ("404.html")
# end def test_404_error

def check_menu_entries_vs_links ( response, difference
                                , current       = None
                                , match_current = "current-"
                                ) :
    ownlinks_li = response.lxml.xpath ("//div[@id='ownlinks']//li")
    ownlinks_a  = response.lxml.xpath ("//div[@id='ownlinks']//li//a")
    ### check the all menu items are in the HTML file
    assert len (ownlinks_li) == TOP_LEVEL_MENU_ITEMS
    ### and one menu item is active (has no `a` node)
    assert len (ownlinks_li) - len (ownlinks_a) == difference
    if current is not None :
        if not isinstance (current, (tuple, list)) :
            current = (current, )
        for c in current :
            assert match_current in ownlinks_li [c].get ("class")
# end def check_menu_entries_vs_links

def test_root () :
    response = c.get ("/", status_code = 200)
    assert response.context ["page"] is response.context ["nav_page"]
    assert response.check_templates ("static.html")
    yield check_menu_entries_vs_links, response, 1, 0, "current-link"
# end def test_root

def test_news () :
    response_n = c.get ("/news/", status_code = 200)
    response_1 = c.get ("/news/20080901.html", status_code = 200)
    response_2 = c.get ("/news/20080830.html", status_code = 200)
    for r in response_n, response_1, response_2 :
        assert r.context ["page"] is r.context ["nav_page"]
        assert r.check_templates ("news.html", "! no_news.html")
    #yield check_menu_entries_vs_links, response_n, 2, (2, 3)
    #yield check_menu_entries_vs_links, response_1, 2, (2, 3)
    #Yield check_menu_entries_vs_links, response_2, 2, (2, 4)
# end def test_news

def test_empty_dir () :
    response = c.get ("/no-entries-test/", status_code = 200)
    assert response.context ["page"] is response.context ["nav_page"]
    assert response.check_templates ("! news.html", "no_news.html")
    ownlinks_li = response.lxml.xpath ("//div[@id='ownlinks']//li")
    ownlinks_a  = response.lxml.xpath ("//div[@id='ownlinks']//li//a")
    assert len (ownlinks_li) == TOP_LEVEL_MENU_ITEMS
    assert len (ownlinks_li) - len (ownlinks_a) == 1
# end def test_news

def check_static (response, text) :
    assert text in response.content
# end def check_static

def test_static () :
    for url, text in ( ("/static-dir/text-1.html", "static text from a file")
                     , ("/static-dir/text-2.html", "A different static text")
                     ) :
        response = c.get (url, status_code = 200)
        yield check_static, response, text
# end def test_static

def test_alias () :
    response = c.get ("/alias-dir/alias-static-1.html", status_code = 200)
    nav_page = response.context ["nav_page"]
    page     = response.context ["page"]
    assert  nav_page        != page
    assert  nav_page.target is page
    response = c.get ("/alias-dir/pic-of-the-day.html", status_code = 200)
    nav_page = response.context ["nav_page"]
    page     = response.context ["page"]
    assert  nav_page        != page
    assert  nav_page.target is page
    assert  isinstance (nav_page, DJO.Navigation.Alias)
    assert  isinstance (page,     DJO.Navigation.Photo)
# end def test_alias

def test_gallery () :
    response = c.get ("/gallery/nature/", status_code = 200)
    gallery  = response.context ["page"]
    assert isinstance (gallery, DJO.Navigation.Gallery)
    assert len (gallery._photos) == 3
    assert len (gallery._thumbs) == 3
    for l, r in pairwise (gallery.photos) :
        assert l.next == r
        assert r.prev == l
    assert response.check_templates ("!photo.html", "gallery.html")
    assert gallery.photos [ 0].prev is None
    assert gallery.photos [-1].next is None
    response = c.get ("/gallery/nature/GreenMeadow.html", status_code = 200)
    photo    = response.context ["page"]
    assert isinstance (photo, DJO.Navigation.Photo)
    assert photo.parent is gallery
    assert response.check_templates ("photo.html", "!gallery.html")
# end def test_gallery

@DJO.Test.DB.setup_database (flush = True)
def test_admin_news () :
    response = c.get         ("/Admin/news/", status_code = 200)
    assert response.check_templates ("model_admin_list.html")
    assert not response.context ["objects"]
    response = c.get         ("/Admin/news/create", status_code = 200)
    assert response.check_templates ("model_admin_change.html")
    ### test if from errors are flagged
    response = c.post        ("/Admin/news/create", status_code = 200)
    assert response.check_templates ("model_admin_change.html")
    response = c.post \
        ( "/Admin/news/create"
        , data = dict ( text        = "This is a text"
                      , title       = "This is the title"
                      )
        )
    response.check_redirect ("/Admin/news/#pk-1")
    ### test if the instance has been created
    response = c.get         ("/Admin/news/", status_code = 200)
    objects  = response.context ["objects"]
    assert len (objects) == 1
    assert objects [0].title == "This is the title"
# end def test_admin_news

@DJO.Test.DB.setup_database (flush = True)
def test_admin_news_change_and_delete () :
    ### first check that no object is in the database
    response = c.get         ("/Admin/news/", status_code = 200)
    assert not response.context ["objects"]
    ### now, let's create 3 entries
    for i in range (1, 4) :
        response = c.post \
            ( "/Admin/news/create"
            , data = dict ( text        = "This is text no %04d" % (i, )
                          , title       = "This is titel %d"     % (i, )
                          )
            )
        response.check_redirect ("/Admin/news/#pk-%d" % (i, ))
    ### make sure all 3 objects are in the `list`
    response = c.get         ("/Admin/news/", status_code = 200)
    objects  = response.context ["objects"]
    assert len (objects) == 3
    ### and that the 3rd object  has the currect title
    assert objects [2].title == "This is titel 3"
    ### now we change the title and text of entry 3
    response = c.post \
        ( "/Admin/news/change/3"
        , data = dict ( text        = "New text of the third entry"
                      , title       = "New title of the 3rd entry"
                      )
        )
    response.check_redirect ("/Admin/news/#pk-3")
    ### make sure that the title has changed
    response = c.get         ("/Admin/news/", status_code = 200)
    objects  = response.context ["objects"]
    assert len (objects) == 3
    ### and that the 3rd object  has the currect title
    assert objects [2].title == "New title of the 3rd entry"

    ### now we delete the second entry :
    response = c.get         ("/Admin/news/delete/2")
    response.check_redirect  ("/Admin/news/")
    ### and make sure that the correct item was deleted
    response = c.get         ("/Admin/news/", status_code = 200)
    objects  = response.context ["objects"]
    assert len (objects) == 2
    ### and that the 3rd object  has the currect title
    assert objects [0].title == "This is titel 1"
    assert objects [1].title == "New title of the 3rd entry"
# end def test_admin_news_change_and_delete

@DJO.Test.DB.setup_database (flush = True)
def test_admin_404 () :
    response = c.get ("/Admin/news/delete/1", status_code = 404)
    response = c.get ("/Admin/news/change/1", status_code = 404)
# end def test_admin_404

### __END__ test
