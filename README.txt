##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################


What is SQLAlchemyDA?
---------------------

SQLAlchemyDA is both a tiny frontend to the z3c.sqlalchemy SQLAlchemy package
for Zope 2 and Zope 3. In addition it acts as a database adapter for ZSQL
methods. Since it is based on SQLAlchemy, SQLAlchemy supports all databases
out-of-the box that are supported by SQLAlchemy (Postgres, MySQL, Oracle,
SQLite, MS-SQL, Firebird, Informix). 


Requirements:
-------------

  - Zope 2.8 +

  - SQLAlchemy 0.3.X (+ database specific low-level Python drivers)

  - z3c.sqlalchemy 1.0.0 +


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



Using SQLAlchemyDA:
-------------------

    SQLAlchemyDA works as a database adapter as documented within "The Zope Book"

    http://www.plope.com/Books/2_7Edition/RelationalDatabases.stx

    and can be used like any other DA together with ZSQL methods.


Tested with databases:
----------------------

    - Postgres 7.4, 8.1

    - SQLite 3.3.X


Notices:
-------

    When using SQLAlchemyDA as a DA for ZSQL methods there should not be any
    limitations.


Author
======
SQLAlchemyDA was written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
and ZOPYX Ltd. & Co. KG, Tuebingen, Germany.


License
=======
SQLAlchemyDA is  licensed under the Zope Public License 2.1. 
See LICENSE.txt.


Contact
=======
Andreas Jung
E-mail: info at zopyx dot com
Web: http://www.zopyx.com


Credits
=======
No credits (so far) :-)
