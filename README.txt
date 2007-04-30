##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################


A shim providing access to registered z3c.sqlalchemy wrapper instances.

Requirements:
-------------

  - Zope 2.8 +

  - SQLAlchemy 0.3.X

  - z3c.sqlalchemy 0.1.10 + 



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
