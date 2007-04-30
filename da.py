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

from z3c.sqlalchemy import allSAWrapperNames, getSAWrapper

class SAWrapper(SimpleItem, PropertyManager):

    manage_options = PropertyManager.manage_options + \
                     SimpleItem.manage_options

    _properties = (
        {'id' : 'sqlalchemy_wrapper_name', 'type' : 'selection', 'mode' : 'rw', 
         'select_variable' : 'registeredWrappers'},
    )

    id = 'sqlalchemy_da'
    meta_type = 'SQLAlchemy Wrapper Integration'
    sqlalchemy_wrapper_name = ''

    security = ClassSecurityInfo()

    def registeredWrappers(self):
        """ return a list of registered wrapper names """
        return allSAWrapperNames()


    def getMapper(self, name):
        """ return a mapper class """
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        return wrapper.getMapper(name)


    def getSession(self):
        """ return a session instance """
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        return wrapper.session
        

    def test(self):
        """ test """
        return self.getSession()            

InitializeClass(SAWrapper)



def manage_addSAWrapper(self, id, title, RESPONSE=None):
    """ create a new SAWrapper instance """
    
    wrapper = SAWrapper(id, title)
    self._setObject(id, wrapper.__of__(self))
    if RESPONSE:
        RESPONSE.redirect(wrapper.absolute_url() + '/manage_main')
    else:
        return wrapper 


manage_addSAWrapperForm = PageTemplateFile('pt/addSAWrapperForm', 
                                           globals(), 
                                           __name__='addSAWrapperForm')
