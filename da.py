##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################


from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile



class SAWrapper(SimpleItem, PropertyManager):

    manage_options = PropertyManager.manage_options + \
                     SimpleItem.manage_options

    _properties = (
        {'id' : 'wrapper_name', 'type' : 'string', 'value' : '', 'mode' : 'rw'},
    )

    id = 'sqlalchemy_da'
    meta_type = 'SQLAlchemy Wrapper Integration'
    wrapper_name = ''

    security = ClassSecurityInfo()


InitializeClass(SAWrapper)



def manage_addSAWrapper(self, id, title, RESPONSE=None):
    """ create a new SAWrapper instance """
    
    wrapper = SAWrapper(id, title)
    self._setObject(id, wrapper.__of__(self))
    if RESPONSE:
        RESPONSE.redirect(wrapper.absolute_url() + '/manage_main')
    else:
        return wrapper 


manage_addSAWrapperForm = PageTemplateFile('pt/addSAWrapperForm', globals(), __name__='addSAWrapperForm')
