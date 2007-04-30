##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################


from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view, view_management_screens
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from z3c.sqlalchemy import allSAWrapperNames, getSAWrapper

class SAWrapper(SimpleItem, PropertyManager):

    manage_options = PropertyManager.manage_options + \
                     ({'label' : 'Info', 'action' : 'manage_info'},) +\
                     SimpleItem.manage_options

    _properties = (
        {'id' : 'sqlalchemy_wrapper_name', 'type' : 'selection', 'mode' : 'rw', 
         'select_variable' : 'registeredWrappers'},
        {'id' : 'title', 'type' : 'string', 'mode' : 'rw'}, 
    )

    meta_type = 'SQLAlchemy Wrapper Integration'
    sqlalchemy_wrapper_name = ''

    security = ClassSecurityInfo()

    def __init__(self, id, title=''):
        self.id = id
        self.title = title

    security.declareProtected(view_management_screens, 'registeredWrappers')
    def registeredWrappers(self):
        """ return a list of registered wrapper names """
        return allSAWrapperNames()


    security.declareProtected(view, 'getMapper')
    def getMapper(self, name):
        """ return a mapper class """
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        return wrapper.getMapper(name)


    security.declareProtected(view, 'getSession')
    def getSession(self):
        """ return a session instance """
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        return wrapper.session
        

    security.declareProtected(view_management_screens, 'getInfo')
    def getInfo(self):
        """ return a dict with additional information """
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        d = wrapper.kw
        d['DSN'] = wrapper.dsn
        return d
 
    manage_info = PageTemplateFile('pt/info', globals(), __name__='manage_info')

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
