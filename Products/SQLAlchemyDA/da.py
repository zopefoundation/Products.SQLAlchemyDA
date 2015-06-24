"""
A DA-like integration of SQLAlchemy based on z3c.sqlalchemy

(C) Zope Corporation and Contributors
Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
"""

import os
import logging
import random
import time
import warnings

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view_management_screens
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from z3c.sqlalchemy import getSAWrapper, createSAWrapper
from z3c.sqlalchemy.interfaces import ISQLAlchemyWrapper


logger = logging.getLogger('SQLAlchemyDA')

# maps Python DB-API types to Zope types
types_mapping = {
    'DATE': 'd',
    'TIME': 'd',
    'DATETIME': 'd',
    'STRING': 's',
    'LONGINTEGER': 'i',
    'INTEGER': 'i',
    'NUMBER': 'n',
    'BOOLEAN': 'n',
    'ROWID': 'i',
    'BINARY': None,  # ????
}


# Global registry of named Zope SQLAlchemyDA instances created to
# work around unique anonymous/random names assigned to such wrappers
# by the legacy DA code
_wrapper_registry = {}


def register_sa_wrapper(name, wrapper):
    """
    Register an SQLAlchemy `ZopeWrapper` database adapter by name as part of a
    module level dict.

    Args:
        name(str): a globally unique name for the given `da_instance`). This
                   is generally a Zope object id, automatically registered when
                   instances of `SAWrapper` are initialized.  If this name is
                   not unique, the most recently registered name will take
                   effect. This registration API is not designed to be used
                   with multiple `SAWrapper` instances sharing the same Zope
                   object ids. An error will not be raised, to prevent problems
                   for the majority of users who don't make use of this
                   registration API (and use Acquisition instead).
        wrapper(`SAWrapper`): a configured instance of
                              `z3c.sqlalchemy.ZopeWrapper`

    This might be called early in Zope startup, so this type of registration is
    necessary instead of a zope.component registration.  (The same reason
    z3c.sqlalchemy claims for using a module dict for registration)

    Returns:
        None
    """
    _wrapper_registry[name] = wrapper


def deregister_sa_wrapper(name):
    """
    Remove a named `SAWrapper` instance from the DA registry, if it exists.
    Either way, the return value is None.
    """
    _wrapper_registry.pop(name, None)


def lookup_sa_wrapper(name):
    """
    Look up and return an `z3c.sqlalchemy.ZopeWrapper` instance registered by
    name.

    These instances are registered by the `SAWrapper` during initialization
    of `ZopeWrapper` instances.

    Returns:
        'SAWrapper' instance.
    """
    da = _wrapper_registry.get(name)
    if not da:
        raise LookupError("No SAWrapper instance registered under name "
                          + name)
    return da


def clear_sa_wrapper_registry():
    """
    Completely empty out the registry of `SAWrapper` instances.
    """
    global _wrapper_registry
    _wrapper_registry = {}


class SAWrapper(SimpleItem, PropertyManager):

    """ A shim around z3c.sqlalchemy implementing something DA-ish """

    # TODO document any special DA-ish hooks or places where Zope
    #      automatically makes calls, or at least link to docs on
    #      what makes it DA-ish. Is there a documented protocol?

    manage_options = (({'label': 'Info', 'action': 'manage_workspace'},) +
                      ({'label': 'Test', 'action': 'manage_test'},) +
                      PropertyManager.manage_options +
                      SimpleItem.manage_options)
    _properties = (
        {'id': 'dsn', 'type': 'string', 'mode': 'rw', },
        {'id': 'title', 'type': 'string', 'mode': 'rw'},
        {'id': 'encoding', 'type': 'string', 'mode': 'rw'},
        {'id': 'transactional', 'type': 'boolean', 'mode': 'rw'},
        {'id': 'convert_unicode', 'type': 'boolean', 'mode': 'rw'},
        {'id': 'quoting_style', 'type': 'selection', 'mode': 'rw',
               'select_variable': 'allQuotingStyles'},
    )

    meta_type = 'SQLAlchemyDA '
    dsn = ''
    encoding = 'iso-8859-15'
    convert_unicode = 0
    transactional = True
    quoting_style = 'standard'
    _isAnSQLConnection = True
    extra_engine_options = ()

    security = ClassSecurityInfo()

    def __init__(self, id, title=''):
        self.id = id
        self.title = title

    def __setstate__(self, *args, **kwargs):
        """
        When an instance of SAWrapper is unpickled, perform the normal
        'wakeup', but also ensure that the instance is in the module
        registry of instances.
        """
        # Don't use 'super' when old-style classes are involved.
        SimpleItem.__setstate__(self, *args, **kwargs)
        wrapper = self.sa_zope_wrapper()
        if wrapper:
            register_sa_wrapper(self.id, wrapper)

    def manage_afterAdd(self, item, container):
        """ Ensure that a new utility id is assigned after creating
            or copying an instance.
        """
        self._new_utilid()
        wrapper = self.sa_zope_wrapper()
        if wrapper:
            register_sa_wrapper(self.id, wrapper)
        return SimpleItem.manage_afterAdd(self, item, container)

    def _new_utilid(self):
        """ Assign a new unique utility ID """
        self.util_id = '%s.%s' % (time.time(), random.random())

    def allQuotingStyles(self):
        return ('standard', 'no-quote')

    @property
    def _wrapper(self):
        """
        Legacy API for accessing the underlying z3c.sqlalchemy `ZopeWrapper`.

        This API should no longer be used because:

            1. Python property decorators can interfere with acquisition context
            2. It's not really private so is misnamed.

        Instead use self.sa_zope_wrapper
        """
        # can't use deprecation decorator, due to interference with acquisition context
        warnings.warn("SAWrapper._wrapper deprecated; instead call SAWrapper.sa_zope_wrapper()",
                      DeprecationWarning)
        return self.sa_zope_wrapper()

    def sa_zope_wrapper(self):
        """
        Public API for accessing the underlying z3c.sqlalchemy `ZopeWrapper`.

        The first attempt will be to lookup the wrapper via attributes
        accessible in the Zope context (self.util_id); if it does not exist,
        the wrapper will be created and return.

        If Zope acquisition context has been lost, fall back to the module
        dict registration mechanism (which might not always be available
        very early in the startup process, but should be available most
        other times).
        """
        wrapper = self._supply_z3c_sa_wrapper()
        if wrapper is not None:
            return wrapper
        else:
            # we've got trouble; log relevant info and fallback on module dict registration
            selftype = type(self)
            try:
                # don't reveal DSN contents in a log file
                dsn = 'nonempty' if self.dsn else self.dsn
            except AttributeError:
                dsn = 'AttributeError'
            try:
                util_id = self.util_id
            except AttributeError:
                util_id = 'AttributeError'
            msg = ("SAWrapper failed to get a handle to live connection.\n"
                   "Did we lose Acquisition context? type(self) is %s.\n"
                   "The self.dsn is '%s' and self.util_id is '%s'.")
            logger.exception(msg, selftype, dsn, util_id)
            # Now that we've logged what we need, try recovering by using
            # the module dict lookup.
            try:
                return lookup_sa_wrapper(self.id)
            except LookupError:
                # no such luck
                return None

    def _supply_z3c_sa_wrapper(self):
        """
        Look up or create the underlying z3c.sqlalchemy `ZopeWrapper`.
        """
        if self.dsn:
            try:
                return getSAWrapper(self.util_id)
            except ValueError:
                wrapper = createSAWrapper(self.dsn,
                                          forZope=True,
                                          transactional=self.transactional,
                                          extension_options={'initial_state': 'invalidated'},
                                          engine_options=self.engine_options,
                                          name=self.util_id)
                register_sa_wrapper(self.id, wrapper)
                return wrapper
        else:
            return None

    @property
    def engine_options(self):
        engine_options = dict(self.extra_engine_options)
        engine_options.update(convert_unicode=self.convert_unicode,
                              encoding=self.encoding)
        return engine_options

    def add_extra_engine_options(self, engine_options):
        """ engine_options is a tuple containing additional
            options for sqlalchemy.create_engine.
            Say you need to pass some engine options
            to SQLAlchemy.create_engine::
            wrapper = SAWrapper(id)
            wrapper.add_extra_engine_options((('echo', True),
                                              ('pool_size', 20)))
        """
        self.extra_engine_options = engine_options

    security.declareProtected(view_management_screens, 'getInfo')
    def getInfo(self):
        """ return a dict with additional information """
        wrapper = self.sa_zope_wrapper()
        if wrapper is not None:
            d = self.sa_zope_wrapper().__dict__.copy()
            d['DSN'] = self.sa_zope_wrapper().dsn
            for k in d.keys()[:]:
                if k.startswith('_'):
                    del d[k]
            return d
        else:
            return {}

    def _typesMap(self, proxy):
        """ Obtain types map from the underlying DB-API. I hope
            that is portable code.
        """

        if not hasattr(self, '_v_types_map'):
            dbapi = self.sa_zope_wrapper().engine.dialect.dbapi

            map = dict()
            for name in types_mapping.keys():
                type_obj = getattr(dbapi, name, None)
                if type_obj:
                    if hasattr(type_obj, 'values'):
                        for v in type_obj.values:
                            map[v] = name
                    else:
                        try:
                            for v in type_obj:
                                map[v] = name
                        except TypeError:
                            # ATT: fix this:->
                            pass

            self._v_types_map = map
        return self._v_types_map

    def query(self, query_string, max_rows=None, query_data=None):
        """ *The* query() method as used by the internal ZSQL
            machinery.
        """
        conn = self.sa_zope_wrapper().connection
        cursor = conn.cursor()

        rows = []
        desc = None
        nselects = 0

        ts_start = time.time()

        for qs in [x for x in query_string.split('\0') if x]:

            logger.debug(qs)
            if query_data:
                proxy = cursor.execute(qs, query_data)
            else:
                proxy = cursor.execute(qs)

            description = cursor.description

            if description is not None:
                nselects += 1

                if nselects > 1:
                    raise ValueError("Can't execute multiple SELECTs "
                                     "within a single query")

                if max_rows:
                    rows = cursor.fetchmany(max_rows)
                else:
                    rows = cursor.fetchall()

                desc = description
                types_map = self._typesMap(proxy)

        logger.debug('Execution time: %3.3f seconds' % (time.time() - ts_start))

        if desc is None:
            return [], None

        items = []
        for name, type_code, width, internal_size, precision, scale, null_ok in desc:

            items.append({'name': name,
                          'type': types_mapping.get(types_map.get(type_code, None), 's'),
                          'null': null_ok,
                          'width': width, })

        return items, rows

    def __call__(self, *args, **kv):
        return self

    def sql_quote__(self, s):
        if self.quoting_style == 'standard':
            if "\'" in s:
                s = "''".join(s.split("\'"))
            return "'%s'" % s
        else:
            return s

    security.declareProtected(view_management_screens, 'connected')
    def connected(self):
        try:
            return self.sa_zope_wrapper()._engine.pool.checkedin() > 0
        except Exception:
            return 'n/a'

    security.declareProtected(view_management_screens, 'getPoolSize')
    def getPoolSize(self):
        """ """
        return self.sa_zope_wrapper()._engine.pool.size()

    security.declareProtected(view_management_screens, 'getCheckedin')
    def getCheckedin(self):
        """ """
        try:
            return self.sa_zope_wrapper()._engine.pool.checkedin()
        except Exception:
            return 'n/a'

    security.declareProtected(view_management_screens, 'manage_start')
    def manage_start(self, RESPONSE=None):
        """ start engine """
        try:
            self.query('COMMIT')
            if RESPONSE:
                msg = 'Database connection opened'
                RESPONSE.redirect(self.absolute_url() +
                              '/manage_workspace?manage_tabs_message=%s' % msg)
        except Exception, e:
            if RESPONSE:
                msg = 'Database connection could not be opened (%s)' % e
                RESPONSE.redirect(self.absolute_url() +
                              '/manage_workspace?manage_tabs_message=%s' % msg)
            else:
                raise

    security.declareProtected(view_management_screens, 'manage_stop')
    def manage_stop(self, RESPONSE=None):
        """ close engine """
        self.sa_zope_wrapper()._engine.pool.dispose()
        if RESPONSE:
            msg = 'Database connections closed'
            RESPONSE.redirect(self.absolute_url() +
                              '/manage_workspace?manage_tabs_message=%s' % msg)

    security.declareProtected(view_management_screens, 'manage_doQuery')
    def manage_doQuery(self, query):
        """ perform a query through the ZMI"""
        return self.query(query)

    security.declareProtected(view_management_screens, 'manage_formatItem')
    def manage_formatItem(self, s):
        """ used by query form """
        if isinstance(s, unicode):
            return s
        if isinstance(s, str):
            return unicode(s, self.encoding, 'ignore')
        return str(s)

    security.declareProtected(view_management_screens, 'getVersion')
    def getVersion(self):
        """ return version.txt """
        return open(os.path.join(os.path.dirname(__file__),
                                 'version.txt')).read()

    security.declareProtected(view_management_screens, 'manage_editProperties')
    def manage_editProperties(self, REQUEST):
        """ Intercept changed properties in order to perform
            further actions.
        """
        try:
            # zope 2.10
            from zope.component import unregisterUtility
            unregisterUtility(name=self.util_id)
            self._new_utilid()
        except ImportError:
            try:
                # zope 2.8
                from zope.component.servicenames import Utilities
                from zope.app import zapi
                s = zapi.getGlobalServices().getService(Utilities)
                s.register((), ISQLAlchemyWrapper, self.util_id, None)
                self._new_utilid()
            except Exception:
                # Zope 2.9 ATT: fix this
                self._new_utilid()

        return super(SAWrapper, self).manage_editProperties(REQUEST)

    manage_workspace = PageTemplateFile('pt/info', globals(),
                                        __name__='manage_workspace')
    manage_test = PageTemplateFile('pt/query', globals(),
                                        __name__='manage_test')


InitializeClass(SAWrapper)


def manage_addSAWrapper(self, id, dsn, title, encoding='iso-8859-15',
                        convert_unicode=0, RESPONSE=None):
    """ create a new SAWrapper instance """
    wrapper = SAWrapper(id, title)
    wrapper.dsn = dsn
    wrapper.convert_unicode = convert_unicode
    wrapper.encoding = encoding
    # this will call manage_afterAdd
    self._setObject(id, wrapper.__of__(self))
    if RESPONSE:
        return RESPONSE.redirect(self._getOb(id).absolute_url()
                                 + '/manage_workspace')
    else:
        return wrapper

manage_addSAWrapperForm = PageTemplateFile('pt/addSAWrapperForm',
                                           globals(),
                                           __name__='addSAWrapperForm')
