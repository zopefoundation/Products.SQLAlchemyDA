Change log
==========

1.1.0 (unreleased)
------------------

- Add support for Python 3.10.

1.0.2 (2021-11-02)
------------------

- fix unexpected NoneType return on sql-update
  (`#12 <https://github.com/zopefoundation/Products.SQLAlchemyDA/pull/12>`_)


1.0.1 (2021-05-03)
------------------

- fix test failures under Python 3.5 by pinning SQLAlchemy.
  Pin can be dropped when support for Zope 4 is dropped.

- change package structure to move package code into a ``src`` subfolder


1.0.0 (2020-11-13)
------------------

- add linting configurations and apply results

- Package cleanup

- Add support for Python 3.5-3.9
  (`#8 <https://github.com/zopefoundation/Products.SQLAlchemyDA/pull/8>`_)


0.6.2b3 (2017-04-03)
--------------------
URL fix in add form.


0.6.2b2 (2015-06-24)
--------------------

Workarounds for edge case error conditions looking up or
creating underlying z3c.sqlalchemy ZopeWrapper instances.


0.6.2b1 (2015-06-23)
--------------------

Beta Release: If you try out this version, please provide feedback!

Added public API for use within Zope acquisition context to access
the underlying zc3.sqlalchemy `ZopeWrapper` instance, with added
error handling and logging to deal with situations where Zope
context may have been lost.

Tests now assume a testrunner such as nose or py.test, and
testfixtures has been added as a testing dependency.


0.6.1b1 (2015-06-19)
--------------------

Improved safety of non-acquisition public API by making registry no longer
contain Zope Persistent objects; instead storing and returning only the
underlying zc3.sqlalchemy `ZopeWrapper` instances. These objects
are plain Python objects in memory with no Persistent connection to ZODB.
(Thanks to Tres Seaver for the suggestion!)


0.6.0b7 (2015-04-27)
--------------------

This is a more stable beta, with several fixes. It has been tested
with SQLAlchemy 0.9.8, Zope2.13, and Python 2.7.9.

Fixes from beta 1-7 include:

- Manifest now includes the .rst, .txt, and .zpt files required
  for installation via ZMI in Zope2.
- The new `lookup_da` registry was failing to populate after
  Zope restarts; now the registry populates when the DA instance
  unpickles. (TODO: needs test coverage; this feature is not
  as robust as it could be, since the registry could be
  called before unpickling). UPDATE for beta 7: Still no
  test coverage, but after manual testing fixed bug with
  switched key and values in registry.
- Added a new `clear_da_registry` to support test teardown.
- NOTE: Beta6 release was taken from the wrong branch,
  and contained experimental untested code. DO not use beta6.

Some non-public patches to support MSSQL have been tested; please inquire if
interested in having them merged to public code.


0.6.0b (2015-03-23)
-------------------

- Added alternative lookup API to get a handle on SAWrapper instances.  To use
  the new lookup mechanism, see Products.SQLAlchemyDA.da.py and look for the
  function `lookup_da`. This was created to allow avoiding Zope Acquisition as
  a lookup mechanism, and to work around the issue that the underlying
  z3c.sqlalchemy `getSAWrapper` function is non-usable when created by the
  SAWrapper DA. This is because API consumers have no access to the random
  internally generated name ('util_id' attribute) under which the utility
  is registered...at least not without resorting to Acquisition calls.
- Tested with SQLAlchemy 0.7.6, Zope 2.13, and Python 2.7.9, and SQLite.
  Your mileage may vary with other databases and versions, but most likely
  it will run with older versions of Zope and Python as old as 2.5 (running
  tests requires at least Python 2.5). Newer versions of SQLAlchemy will be
  tested for the next release.


0.5.2 (unreleased)
------------------
- Fixed LP #639597

0.5.1 (2010-08-05)
------------------
- fixed typo in type mapping

0.5.0 (2010-05-07)
------------------

- Fixed LP #570208
- Added a method 'add_extra_engine_options' to set additional engine
  options for SQLAlchemy.create_engine.
- Removed SOFTWARE_HOME dependency
- Requires SQLAlchemy >= 0.5.0

0.4.1 (2008-06-01)
------------------

- fixed issue with version.txt file

0.4.0 (2008-01-24)
------------------

- requires z3c.sqlalchemy (2.0.0 or higher)
- requires SQLAlchemy 0.4.4 or higer


0.3.0 (2007-06-10)
------------------

- fixed some security assertions
- added "Test" tab for executing SQL queries directly
- better error handling for ZMI screens
- no longer depending on a pre-registered SQLAlchemy wrapper. SQLAlchemyDA
  now accepts (as any other DA) a DSN as property 'dsn'
- DSN can be passed through the add form
- redirect directly to "Info" tab after creating an instance through the ZMI
- catching some low-level exceptions from the sqlite interface in order to
  make it work with SQLite
- new properties 'transactional' and 'quoting_style'
- improved support for Oracle and MySQL
- SQLAlchemyDA no longer provides access to mapper related functionalities.
  It now acts as a DA for executing SQL statements *only*.
- fixed unregistration code for a wrapper (hopefully works with Zope 2.8 or
  higher)

- updated documentation

0.2.1 (2007-05-06)
------------------

- connections can be closed/opened through the ZMI
- some code cleanup
- fixed a *very* stupid typo causing ZODB conflict errors

0.2.0 (2007-05-05)
------------------

- first public release

0.1.0 (2007-04-30)
------------------

- initial coding
