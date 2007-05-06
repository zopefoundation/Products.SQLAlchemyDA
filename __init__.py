##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################

try:
    import z3c.sqlalchemy
except ImportError:
    raise ImportError('The z3c.sqlalchemy is not installed properly')

from config import ADD_SA_WRAPPER_PERMISSION


def initialize(context):

    from da import (SAWrapper, manage_addSAWrapper, 
                   manage_addSAWrapperForm)

    context.registerClass(SAWrapper, 
                          constructors=(manage_addSAWrapperForm, 
                                        manage_addSAWrapper),
                          permission=ADD_SA_WRAPPER_PERMISSION)                          


    # make sqlalchemy classes available to untrusted code
    from AccessControl.SecurityInfo import ModuleSecurityInfo, allow_module, allow_class

    from sqlalchemy.orm.session import Session
    from sqlalchemy.orm.query import Query

    allow_class(Session)
    allow_class(Query)
