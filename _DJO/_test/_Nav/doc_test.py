# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@smangari.org
#
#++
# Name
#    doc_test
#
# Purpose
#    Simple doc-test for the navigation
#
# Revision Dates
#    10-Oct-2008 (MG) Creation
#    ««revision-date»»···
#--
"""
>>> TOP_LEVEL_MENU_ITEMS = 7
>>> c = DJO.Test.Client ("_DJO._test._Nav.settings_test")

### make a request and check the status code
>>> r = c.get ("/")
>>> r.status_code
200

### check some parts of the context
>>> r.context ["page"] is r.context ["nav_page"]
True
>>> r.context ["page"].title
u'Home'

### check if the correct template was used
>>> r.check_templates ("static.html")
True

### check the news part of the site
>>> for url in "/news/", "/news/20080901.html", "/news/20080830.html" :
...    r = c.get (url)
...    r.status_code, r.context ["nav_page"] is r.context ["page"]
(200, True)
(200, True)
(200, True)

### check that the `empty_template` works
>>> r = c.get ("/no-entries-test/")
>>> r.status_code, r.check_templates ("! news.html", "no_news.html")
(200, True)

### check how many links of the menu are active
>>> ownlinks_li = r.lxml.xpath ("//div[@id='ownlinks']//li")
>>> ownlinks_a  = r.lxml.xpath ("//div[@id='ownlinks']//li//a")
>>> len (ownlinks_li) == TOP_LEVEL_MENU_ITEMS
True
>>> len (ownlinks_li) - len (ownlinks_a)
1

### check the static text rendering
>>> r = c.get ("/static-dir/text-1.html")
>>> r.status_code, "static text from a file" in r.content
(200, True)
>>> r = c.get ("/static-dir/text-2.html")
>>> r.status_code, "A different static text" in r.content
(200, True)

### check the Alias Navigation elements
>>> r = c.get ("/alias-dir/alias-static-1.html")
>>> r.status_code
200
>>> nav_page = r.context ["nav_page"]
>>> page     = r.context ["page"]
>>> nav_page.target is page
True
>>> r = c.get ("/alias-dir/pic-of-the-day.html")
>>> r.status_code
200
>>> nav_page = r.context ["nav_page"]
>>> page     = r.context ["page"]
>>> nav_page.target is page
True
>>> nav_page.__class__.__name__
'Alias'
>>> page.__class__.__name__
'Photo'

### test the gallery
>>> r = c.get ("/gallery/nature/")
>>> g = r.context ["page"]
>>> g.__class__.__name__
'Gallery'
>>> len (g._photos), len (g._thumbs)
(3, 3)
>>> g.photos [0].prev,      g.photos [0].next.name
(None, u'GreenMeadow.html')
>>> g.photos [1].prev.name, g.photos [1].next.name
(u'FreshFlower.html', u'OpenFlower.html')
>>> g.photos [2].prev.name, g.photos [2].next
(u'GreenMeadow.html', None)
>>> r.check_templates ("!photo.html", "gallery.html")
True
>>> r = c.get ("/gallery/nature/GreenMeadow.html")
>>> r.status_code
200
>>> photo = r.context ["page"]
>>> photo.__class__.__name__
'Photo'
>>> photo.parent is g
True
>>> r.check_templates ("photo.html", "!gallery.html")
True

### test the admin interface
>>> DJO.Test.DB.setup (flush = True) ### clear the database
>>> r = c.get         ("/Admin/news/")
>>> r.status_code
200
>>> r.check_templates ("model_admin_list.html")
True
>>> r.context ["objects"]
[]
>>> for i in range (1, 4) :
...     r = c.post \\
...        ( "/Admin/news/create"
...        , data = dict ( text        = "This is text no %04d" % (i, )
...                      , title       = "This is titel %d"     % (i, )
...                      )
...         )
...     i, r.redirect_info ()
(1, 'Redirect: http://testserver/Admin/news/#pk-1 [302] --> [200]')
(2, 'Redirect: http://testserver/Admin/news/#pk-2 [302] --> [200]')
(3, 'Redirect: http://testserver/Admin/news/#pk-3 [302] --> [200]')
>>> r = c.get         ("/Admin/news/create")
>>> r.status_code
200
>>> r.check_templates ("model_admin_change.html")
True

### test if from errors are flagged
>>> r = c.post        ("/Admin/news/create")
>>> r.check_templates ("model_admin_change.html")
True
>>> sorted (r.context ["form"].errors.iteritems ())
[('text', [u'This field is required.']), ('title', [u'This field is required.'])]

### test if the instance has been created
>>> r        = c.get     ("/Admin/news/")
>>> objects  = r.context ["objects"]
>>> len (objects)
3
>>> for o in objects : o.title
u'This is titel 1'
u'This is titel 2'
u'This is titel 3'

### test if we can change an object
>>> r = c.post \\
...     ( "/Admin/news/change/3"
...     , data = dict ( text        = "New text of the third entry"
...                   , title       = "New title of the 3rd entry"
...                   )
...     )
>>> r.redirect_info ()
'Redirect: http://testserver/Admin/news/#pk-3 [302] --> [200]'

### make sure that the title has changed
>>> r = c.get            ("/Admin/news/")
>>> objects  = r.context ["objects"]
>>> len (objects)
3
>>> for o in objects : o.title
u'This is titel 1'
u'This is titel 2'
u'New title of the 3rd entry'

### now we delete the second entry :
>>> r = c.get         ("/Admin/news/delete/2")
>>> r.redirect_info ()
'Redirect: http://testserver/Admin/news/ [302] --> [200]'

### and make sure that the correct item was deleted
>>> r = c.get         ("/Admin/news/")
>>> objects  = r.context ["objects"]
>>> len (objects)
2
>>> for o in objects : o.title
u'This is titel 1'
u'New title of the 3rd entry'

### test of the deleter and changer of the admin raise a 404 error if the
### object does not exist
>>> r = c.get ("/Admin/news/delete/0")
>>> r.status_code
404
>>> r = c.get ("/Admin/news/change/0")
>>> r.status_code
404
"""
from   _DJO                    import DJO
import _DJO._Test.Client

from   _TFL.predicate          import pairwise

import  os
os.environ ["DJANGO_SETTINGS_MODULE"] = ""

### __END__ doc_test
