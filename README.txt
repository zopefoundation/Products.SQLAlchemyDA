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
out-of-the box that are supported by SQLAlchemy.


Requirements:
-------------

  - Zope 2.8 +

  - SQLAlchemy 0.3.X

  - z3c.sqlalchemy 1.0.0 +


Installation:
-------------

  - download and install z3c.sqlalchemy as egg or from the sources 
    from Cheeseshop (easy_install z3c.sqlalchemy)

  - A z3c.sqlAlchemy SAWrapper must be registered. The best way to do this
    right now to put something like this into your Product's initialize():

    Products/YourProduct/__init__.py:

       def  initialize(context):

           from z3c.sqlalchemy import createSAWrapper
           wrapper = createSAWrapper('postgres://user:password@host/database', 
                                     forZope=True,
                                     name='my-sa-wrapper')

    If you have trouble with the number of connections (5 by default + 10 threshold) you must
    customize the connection pool:

           from sqlalchemy.pool import QueuePool
           from z3c.sqlalchemy import createSAWrapper

           wrapper = createSAWrapper('postgres://user:password@host/database', 
                                     poolclass=QueuePool,
                                     pool_size=20,
                                     max_overflow=10,
                                     forZope=True)

            
    

  - After restarting Zope you go to the ZMI and create an instance of
    "SQLAlchemyDA" (as you would create some DA instance). After
    creating the instance you should see 'my-sa-wrapper' in the properties form of
    the new instance. When creating a new ZSQL method you should be able to use
    this DA instance as connection id.


Using SQLAlchemyDA:
-------------------

  - for using SQLAlchemyDA through object mappers as used in SQLAlchemy
    you can use the getMapper() and getMappers() methods. Check
    the z3c.sqlchemy documentation for details. A SQLAlchemy Session object
    can be obtained by the getSession() method. Sessions are integrated
    with Zope 2 transaction management.
 
  - a SQLAlchemyDA instance can be used as a standard DA together with
    ZSQL methods. 

    WARNING: YOU SHOULD NOT USE ZSQL METHODS AND MAPPERS WITHIN THE SAME
    REQUEST!!!

    Mappers/Sessions and Connections (for ZSQL methods) are totally independent
    and have their own transaction. Mixing both would result in two distinct
    transactions leading to unpredictable results. 


Notices:
-------

    Using SQLAlchemyDA as SQLAlchemy wrapper (means you are working with
    mappers) requires that the API methods must be accessed from trusted code right
    now.  You can not use these methods from PythonScripts or PageTemplates (unless
    you use TrustedExecutables by Dieter Maurer).  At least some of the methods
    might raise Unauthorized exception because the SQLAlchemy internal classes
    don't have security assertions which are necessary for classes to be used
    within RestrictedPython.

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
