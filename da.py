##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################

import logging
import time

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view, view_management_screens
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from z3c.sqlalchemy import allSAWrapperNames, getSAWrapper


LOG = logging.getLogger('SQLAlchemyDA')

types_mapping = {
    'DATE' : 'd',
    'IME' : 'd',
    'DATETIME' : 'd',
    'STRING' : 's',
    'LONGINTEGER' : 'i',
    'INTEGER' : 'i',
    'NUMBER' : 'n',
    'BOOLEAN' : 'n',
    'ROWID' : 'i',
    'BINARY' : None, #????
}


class SAWrapper(SimpleItem, PropertyManager):
    """ A shim around z3c.sqlalchemy implementing something DA-ish """

    manage_options = PropertyManager.manage_options + \
                     ({'label' : 'Info', 'action' : 'manage_info'},) +\
                     SimpleItem.manage_options

    _properties = (
        {'id' : 'sqlalchemy_wrapper_name', 'type' : 'selection', 'mode' : 'rw', 
         'select_variable' : 'registeredWrappers'},
        {'id' : 'title', 'type' : 'string', 'mode' : 'rw'}, 
    )

    meta_type = 'SQLAlchemy Wrapper Integration'
    sqlalchemy_wrapper_name = None
    _isAnSQLConnection = True

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


    security.declareProtected(view, 'getMappers')
    def getMappers(self, *names):
        """ return a mapper class """
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        return wrapper.getMappers(*names)


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


    def _typesMap(self, proxy):
        """ Obtain types map from the underlying DB-API. I
            hope that is portable code.
        """

        if not hasattr(self, '__v__types_map'):
            dbapi = proxy.dialect.dbapi

            map = dict()
            for name  in types_mapping.keys():
                type_obj = getattr(dbapi, name, None)
                if type_obj is not None:
                    for v in type_obj.values:
                        map[v] = name
            self.__v__types_map = map  
        return self.__v__types_map


    def query(self, query_string, max_rows=None, query_data=None):
        """ *The* query() method as used by the internal ZSQL
            machinery.
        """

        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        c = wrapper.connection

        rows = []
        desc = None
        nselects = 0

        ts_start = time.time()

        for qs in [x for x in query_string.split('\0') if x]:

            LOG.debug(qs)
               
            if query_data:
                proxy = c.execute(qs, query_data)
            else:
                proxy = c.execute(qs)

            description = proxy.cursor.description

            if description is not None:
                nselects += 1
        
                if nselects > 1:
                    raise ValueError("Can't execute multiple SELECTs within a single query")

                if max_rows:
                    rows = proxy.fetchmany(max_rows)
                else:
                    rows = proxy.fetchall()

                desc = description  
                types_map = self._typesMap(proxy)

        LOG.debug('Execution time: %3.3f seconds' % (time.time() - ts_start))

        if desc is None:            
            return [], None

        items = []
        for  name, type_code, width, internal_size, precision, scale, null_ok in desc:
    
            items.append({'name' : name,
                          'type' : types_mapping.get(types_map.get(type_code, None), 's'),
                          'null' : null_ok,
                          'width' : width,
                         }) 

        return items, rows


    def __call__(self, *args, **kv):
        return self    


    def sql_quote__(self, s):
        return s


    def connected(self):
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        return wrapper.engine is not None

    def manage_stop(self):
        """ close engine """
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        wrapper._engine = None
        return 'All engines stopped'
        
    def manage_start(self):
        """ Re(start) engine """
        wrapper = getSAWrapper(self.sqlalchemy_wrapper_name)
        wrapper._createEngine()
        return 'All engines started'

 
    manage_info = PageTemplateFile('pt/info', 
                                   globals(), 
                                   __name__='manage_info')

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
