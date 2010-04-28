##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################

import os
try:
    import z3c.sqlalchemy
except ImportError:
    raise ImportError('The z3c.sqlalchemy is not installed properly')

from config import ADD_SA_WRAPPER_PERMISSION



def initialize(context):
    from da import (SAWrapper, manage_addSAWrapper,
                   manage_addSAWrapperForm)
    from Shared.DC import ZRDB

    icon_path = os.path.join(os.path.dirname(ZRDB.__file__), 'www', 'DBAdapterFolder_icon.gif')
    context.registerClass(SAWrapper,
                          constructors=(manage_addSAWrapperForm,
                                        manage_addSAWrapper),
                          icon=icon_path,
                          permission=ADD_SA_WRAPPER_PERMISSION)
