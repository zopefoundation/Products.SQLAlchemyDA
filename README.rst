Zope ZSQL-SQLAlchemy Integration Wrapper
========================================


About SQLAlchemyDA
------------------

SQLAlchemyDA is a generic database adapter for Zope ZSQL methods, which are
an older/legacy SQL templating feature for executing relational database queries
from with in a Zope to transaction context.

SQLAlchemyDA provides an implementation in the form of a Zope2 "product" which
wraps `z3c.sqlalchemy <https://pypi.python.org/pypi/zope.sqlalchemy>`_, so that
database connections are installable as objects in the Zope2 ZMI. Such
connection objects can be set up to connect to any kind of database backend
supported by SQLAlchemy using a database URI, such as Postgres, MySQL, Oracle,
SQLite, MS-SQL, Firebird, Informix. However, some of these database backends
have not been tested with the SQLAlchemyDA, so your mileage may vary.

In addition to ZSQL support, the SQLAlchemyDA makes it possible to use the
standard SQLAlchemy API within a Zope2 context and participate in Zope
transactions.

However, if you do not require ZSQL support, and only wish to call 'normal'
SQLAlchemy APIs within Zope transactions, this package adds no value. Instead,
you would be better off trying out `zope.sqlalchemy`, as recommended in the
`Zope2 book chapter on relational database
connectivity <http://docs.zope.org/zope2/zope2book/RelationalDatabases.html>`_.


Requirements:
-------------

- Zope 2.10+
- SQLAlchemy >= 0.5.0 (+ database specific low-level Python drivers)
- z3c.sqlalchemy >= 1.2.0

Testing: py.test and testfixtures are needed to run tests.


Installation:
-------------

- Download and install SQLAlchemy as egg or from the sources
  from PyPI (pip sqlalchemy). See
    
    http://www.sqlalchemy.org

    for details

- Download and install z3c.sqlalchemy as egg or from the sources 
  from PyPI (pip z3c.sqlalchemy). See

    http://pypi.python.org/pypi/z3c.sqlalchemy/

  for details.

- Unpack the archive containing SQLAlchemyDA inside the "Products"
  directory of your Zope instance home.

- After restarting Zope you go to the ZMI and create an instance of
  "SQLAlchemyDA" (as you would create some DA instance)

- Click on the new created SQLAlchemyDA instance within the ZMI
  and configure your database connection through the "Properties" tab.
  The connection parameter 'dsn' must be specified as a valid SQLAlchemy DSN 
  like

         <dbschema>://<username>:<password>@<hostname>/<databasename>

    Example:
        
        postgres://admin:123@localhost:5432/TestDB

- ZSQL methods should see the new DA through the selection widget of available
  database adapters

- NOTE: you must have the low-level Python DB drivers installed in order to 
  access a particular database. See 

        http://www.sqlalchemy.org/docs/dbengine.html#dbengine_supported

  for details.


Configuration of SQLAlchemyDA:
------------------------------

- 'dsn' - SQLAlchemy compliant Database Set Name (see www.sqlalchemy.org/docs)

- 'transactional' - uncheck this property if you are working with a non-transactional
   database like older versions of MySQL. Uncheck this property *only* if you see any
   commit() related error. Otherwise leave this property checked. Changing this
   property *requires* a Zope restart.

- 'quoting_style' - affects how strings are quoted in SQL. By default 'standard' 
   quotes strings correctly. Setting the value to 'no-quote' might solve quoting issues
   with some databases.


Using SQLAlchemyDA:
-------------------

SQLAlchemyDA works as a database adapter as documented within "The Zope Book"

http://www.plope.com/Books/2_7Edition/RelationalDatabases.stx

and can be used like any other DA together with ZSQL methods.


Tested with databases:
----------------------

- Postgres 7.4, 8.0-8.2
- SQLite 3.3.X
- Oracle 10g
- MySQL is *only* supported for MySQL databases with transaction support.
  (see also z3c/sqlalchemy/README.txt)      
- MSSQL 2008
 

Known issues:
-------------

""" Database connection could not be opened ((ProgrammingError) (1064, You
have an error in your SQL syntax near 'COMMIT .
"""

This bug might appear with older MySQL versions when opening/closing
the connections manually through the ZMI. It should not affect the
functionality of SQLAlchemyDA.
    

Author
------

SQLAlchemyDA was written by Andreas Jung for Haufe Mediengruppe, Freiburg,
Germany and ZOPYX Ltd. & Co. KG, Tuebingen, Germany.

Currently the package is maintained by Sheila Allen in Texas, USA,
on behalf of ZeOmega, Inc.


License
-------

SQLAlchemyDA is  licensed under the Zope Public License 2.1. 
See LICENSE.txt.


Contact
-------

| Sheila Allen
| E-mail: sallen at zeomega.com


Credits
-------

Parts of the SQLAlchemyDA V 0.3.X development has been sponsored by Wayne
Volkmuth (renovis.com).

More recent SQLAlchemy support and maintenance sponsored by ZeOmega.com.
