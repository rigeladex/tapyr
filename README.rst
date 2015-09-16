README for the Tapyr repository
================================

:Authors:

    Christian Tanzer
    <tanzer@swing.co.at>

This is `Christian Tanzer's <https://github.com/tanzer>`_
Python `repository <https://github.com/Tapyr/tapyr>`_
aka `Tapyr`. Tapyr is BSD licensed.

Tapyr comprises a number of package namespaces (see `TFL.Package_Namespace`),
including:

- `MOM` implements a meta object model for the specification and
  implementation of essential object models.

  `MOM` supports multiple database backends, one of them is based on
  `sqlalchemy <http://www.sqlalchemy.org/>`_

- `GTW` implements a `Werkzeug-based <http://werkzeug.pocoo.org/>`_
  framework for RESTful web applications built on top of `MOM`.

- `JNJ` provides a `Jinja-based <http://jinja.pocoo.org/>`_
  template framework for `GTW`.

- `CAL` provides classes for dealing with date, time, and
  calendars.

- `PMA` provides classes for dealing with emails.

- `ReST` provides `docutils-based <https://pypi.python.org/pypi/docutils/>`_
  classes and functions for dealing with re-structured text.

- `ATAX` provides classes and functions for doing simple
  accounting according to Austrian tax laws.

- `TFL` provides utility classes and functions used by the other
  package namespaces.

Contact
-------

Christian Tanzer <tanzer@swing.co.at>
