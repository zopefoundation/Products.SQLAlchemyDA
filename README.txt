##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################


A shim providing access to registered  z3c.sqlalchemy wrapper instances.

Exported methods are: getMapper() and getSession().


The methods must be accessed from trusted code. You can not use these
methods from PythonScripts (unless you use TrustedExecutables by Dieter Maurer)
