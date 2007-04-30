##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################


A shim providing access to registered z3c.sqlalchemy wrapper instances.
The DA also might act as a generic DA for all databases supported through
SQLAlchemy

Requirements:
-------------

  - Zope 2.8 +

  - SQLAlchemy 0.3.X

  - z3c.sqlalchemy 0.1.10 + 


Installation:
-------------

A z3c.sqlAlchemy SAWrapper must be registered. The best way to do this right
now to put something like this into your Product's initialize():

Products/YourProduct/__init__.py:

   def  initialize(context):

       from z3c.sqlalchemy import createSAWrapper, registerSAWrapper
       wrapper = createSAWrapper('postgres://user:password@host/database', forZope=True)
       registerSAWrapper(wrapper, 'my-sa-wrapper')

After restarting Zope you go to the ZMI and create an instance of "SQLAlchemy
Wrapper Integration" (as you would create some DA instance). After creating the
instance you should see 'my-sa-wrapper' in the properties form of the new
instance. When creating a new ZSQL method you should be able to use this DA
instance as connection id.



Exported methods are: getMapper() and getSession().


Notice:
-------

The methods must be accessed from trusted code. You can not use these
methods from PythonScripts (unless you use TrustedExecutables by Dieter Maurer)


Author
======
z3c.sqlalchemy was written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
and ZOPYX Ltd. & Co. KG, Tuebingen, Germany.


License
=======
z3c.sqlalchemy is licensed under the Zope Public License 2.1. 
See LICENSE.txt.


Contact
=======
Andreas Jung, 
E-mail: info at zopyx dot com
Web: http://www.zopyx.com


Credits
=======
No credits (so far) :-)
