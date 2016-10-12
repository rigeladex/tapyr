JNJ provides a Jinja2-based template framework.

JNJ manages a set of jinja template/macro files with their associated media
fragments (CSS and Javascript). JNJ combines the media fragments of all jinja
files used by a toplevel jinja template — each toplevel jinja template loads
only thse media fragments it needs.

JNJ supports the calling of jinja macros by Python code — this allows the code
responding to a AJAX request to use the same jinja macros as the template that
rendered the original page request.

JNJ is distributed under the conditions of the `BSD 3-Clause
License <http://www.c-tanzer.at/license/bsd_3c.html>`_.

JNJ is available as a `git repository`_.
You can clone that repository with::

    git clone git@github.com:Tapyr/tapyr.git

Reports of bugs in JNJ should be submitted to the `git repository`_.

.. _`git repository`: https://github.com/Tapyr/tapyr
