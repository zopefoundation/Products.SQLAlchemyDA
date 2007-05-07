##########################################################################
# A DA-like integration of SQLAlchemy based on z3c.sqlalchemy
#
# (C) Zope Corporation and Contributors
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################

import os
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

# maps Python DB-API types to Zope types
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

    manage_options = ({'label' : 'Info', 'action' : 'manage_workspace'},) +\
                     PropertyManager.manage_options + \
                     SimpleItem.manage_options

    _properties = (
        {'id' : 'sqlalchemy_wrapper_name', 'type' : 'selection', 'mode' : 'rw', 
         'select_variable' : 'registeredWrappers'},
        {'id' : 'title', 'type' : 'string', 'mode' : 'rw'}, 
    )

    meta_type = 'SQLAlchemyDA '
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

    @property
    def _wrapper(self):
        return getSAWrapper(self.sqlalchemy_wrapper_name)


    security.declareProtected(view, 'getMapper')
    def getMapper(self, name):
        """ return a mapper class """
        return self._wrapper.getMapper(name)


    security.declareProtected(view, 'getMappers')
    def getMappers(self, *names):
        """ return a mapper class """
        return self._wrapper.getMappers(*names)


    security.declareProtected(view, 'getSession')
    def getSession(self):
        """ return a session instance """
        return self._wrapper.session
        

    security.declareProtected(view_management_screens, 'getInfo')
    def getInfo(self):
        """ return a dict with additional information """
        d = self._wrapper.kw
        d['DSN'] = self._wrapper.dsn
        return d


    def _typesMap(self, proxy):
        """ Obtain types map from the underlying DB-API. I
            hope that is portable code.
        """

        if not hasattr(self, '_v_types_map'):
            dbapi = proxy.dialect.dbapi

            map = dict()
            for name  in types_mapping.keys():
                type_obj = getattr(dbapi, name, None)
                if type_obj is not None:
                    for v in type_obj.values:
                        map[v] = name
            self._v_types_map = map  
        return self._v_types_map


    def query(self, query_string, max_rows=None, query_data=None):
        """ *The* query() method as used by the internal ZSQL
            machinery.
        """

        c = self._wrapper.connection

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


    security.declareProtected(view_management_screens, 'connected')
    def connected(self):
        return self._wrapper._engine.connection_provider._pool.checkedin() > 0


    security.declareProtected(view_management_screens, 'getPoolSize')
    def getPoolSize(self):
        """ """
        return self._wrapper._engine.connection_provider._pool.size() 


    security.declareProtected(view_management_screens, 'getCheckedin')
    def getCheckedin(self):
        """ """
        return self._wrapper._engine.connection_provider._pool.checkedin() 


    security.declareProtected(view_management_screens, 'manage_start')
    def manage_start(self, RESPONSE=None):
        """ start engine """               
        try:
            self.query('BEGIN; COMMIT;');
            if RESPONSE:
                msg = 'Database connection opened'
                RESPONSE.redirect(self.absolute_url() + '/manage_workspace?manage_tabs_message=%s' % msg)
        except Exception, e:
            if RESPONSE:
                msg = 'Database connection could not be opened (%s)' % e
                RESPONSE.redirect(self.absolute_url() + '/manage_workspace?manage_tabs_message=%s' % msg)
            else: 
                raise


    security.declareProtected(view_management_screens, 'manage_stop')
    def manage_stop(self, RESPONSE=None):
        """ close engine """
        self._wrapper._engine.connection_provider._pool.dispose()
        if RESPONSE:
            msg = 'Database connections closed'
            RESPONSE.redirect(self.absolute_url() + '/manage_workspace?manage_tabs_message=%s' % msg)

    
    security.declareProtected(view_management_screens, 'getVersion')
    def getVersion(self):
        """ return version.txt """
        return open(os.path.join(os.path.dirname(__file__), 'version.txt')).read()

 
    manage_workspace = PageTemplateFile('pt/info', 
                                        globals(), 
                                        __name__='manage_workspace')

InitializeClass(SAWrapper)



def manage_addSAWrapper(self, id, title, RESPONSE=None):
    """ create a new SAWrapper instance """
    
    wrapper = SAWrapper(id, title)
    self._setObject(id, wrapper.__of__(self))
    if RESPONSE:
        RESPONSE.redirect(wrapper.absolute_url() + '/manage_workspace')
    else:
        return wrapper 


manage_addSAWrapperForm = PageTemplateFile('pt/addSAWrapperForm', 
                                           globals(), 
                                           __name__='addSAWrapperForm')
