##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################

import os

from Shared.DC import ZRDB

from .config import ADD_SA_WRAPPER_PERMISSION
from .da import SAWrapper
from .da import manage_addSAWrapper
from .da import manage_addSAWrapperForm


def initialize(context):
    icon_path = os.path.join(os.path.dirname(ZRDB.__file__), 'www',
                             'DBAdapterFolder_icon.gif')
    context.registerClass(SAWrapper,
                          constructors=(manage_addSAWrapperForm,
                                        manage_addSAWrapper),
                          icon=icon_path,
                          permission=ADD_SA_WRAPPER_PERMISSION)
