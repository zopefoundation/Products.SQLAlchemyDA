A-like integration of SQLAlchemy based on z3c.sqlalchemy
========================================================

What is SQLAlchemyDA?
---------------------

SQLAlchemyDA is a generic database adapter for ZSQL methods. Since it is based
on SQLAlchemy, SQLAlchemyDA supports all databases out-of-the box that are
supported by SQLAlchemy (Postgres, MySQL, Oracle, SQLite, MS-SQL, Firebird,
Informix). 


Requirements:
-------------

- Zope 2.10+
- SQLAlchemy >= 0.5.0 (+ database specific low-level Python drivers)
- z3c.sqlalchemy >= 1.2.0


Installation:
-------------

- download and install SQLAlchemy as egg or from the sources
  from Cheeseshop (easy_install sqlalchemy). See
    
    http://www.sqlalchemy.org

    for details

- download and install z3c.sqlalchemy as egg or from the sources 
  from Cheeseshop (easy_install z3c.sqlalchemy). See

    http://cheeseshop.python.org/pypi/z3c.sqlalchemy/

  for details.

- unpack the archive containing SQLAlchemyDA inside the "Products"
  directory of your Zope instance home.

- after restarting Zope you go to the ZMI and create an instance of
  "SQLAlchemyDA" (as you would create some DA instance)

- click on the new created SQLAlchemyDA instance within the ZMI
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
 

Known issues:
-------------

""" Database connection could not be opened ((ProgrammingError) (1064, You
have an error in your SQL syntax near 'COMMIT .
"""

This bug might appear with older MySQL versions when opening/closing
the connections manually through the ZMI. It should not affect the
functionality of SQLAlchemyDA.
    

Author
======
SQLAlchemyDA was written by Andreas Jung for Haufe Mediengruppe, Freiburg,
Germany and ZOPYX Ltd. & Co. KG, Tuebingen, Germany.


License
=======
SQLAlchemyDA is  licensed under the Zope Public License 2.1. 
See LICENSE.txt.


Contact
=======

| ZOPYX Ltd. & Co. KG
| Andreas Jung
| E-mail: info at zopyx dot com
| Web: http://www.zopyx.com


Credits
=======
Parts of the SQLAlchemyDA V 0.3.X development has been sponsored by Wayne
Volkmuth (renovis.com)
