"""
Tests for SQLAlchemyDA
"""

import copy
import os
from unittest.mock import patch

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy.orm import mapper
from testfixtures import LogCapture

import transaction
from Products.ZSQLMethods.SQL import manage_addZSQLMethod
from Testing import ZopeTestCase

from z3c.sqlalchemy.base import ZopeWrapper
from z3c.sqlalchemy.mapper import MappedClassBase


ZopeTestCase.installProduct('SQLAlchemyDA', 1)


metadata = MetaData()
test_table = Table('test', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('utext', Unicode(255)),
                   Column('text', String(255)))


class Test(MappedClassBase):
    pass


mapper(Test, test_table)


class TestBase(ZopeTestCase.ZopeTestCase):

    def createDA(self, **kw):
        obj_id = kw.pop('id', 'da')
        factory = self.app.manage_addProduct['SQLAlchemyDA']
        factory.manage_addSAWrapper(id=obj_id, title='da',
                                    dsn=self.dsn,
                                    **kw)
        return self.app[obj_id]


class SQLAlchemyDATests(TestBase):

    def afterSetUp(self):
        from z3c.sqlalchemy import createSAWrapper

        self.dsn = os.environ.get('TEST_DSN', 'sqlite:///sqlitetestdb1')
        wrapper = createSAWrapper(self.dsn)
        metadata.bind = wrapper.engine
        metadata.create_all()
        session = wrapper.session
        t1 = Test(id=1, utext='Hello world', text='hello world')
        t2 = Test(id=2, utext='foo', text='far')
        session.add(t1)
        session.add(t2)

    def testSimpleSelect(self):
        da = self.createDA()
        rows = da.query('select * from test')
        self.assertEqual(len(rows), 2)

    def testSimpleInsert(self):
        da = self.createDA()
        da.query("insert into test (id, text) values(42, 'foo')")

    def testSimpleUpdate(self):
        da = self.createDA()
        da.query("update test set text='bar'")

    def testExtraEngineOptions(self):
        da = self.createDA()
        da.add_extra_engine_options((('echo', True),
                                     ('pool_size', 20)))
        self.assertEqual(da.engine_options['pool_size'], 20)

    def testDeGhostify(self):
        da = self.createDA(id='spam')
        from ..da import clear_sa_wrapper_registry
        from ..da import lookup_sa_wrapper
        wrapper = lookup_sa_wrapper('spam')
        assert wrapper
        clear_sa_wrapper_registry()
        # ensure registry is clear
        with self.assertRaises(LookupError):
            lookup_sa_wrapper('spam')
        # call unpickling code directly, to simulate restoring from ZODB
        fake_pickle_input = copy.deepcopy(da.__dict__)
        assert da.dsn
        da.aq_self.__setstate__(fake_pickle_input)
        assert da.dsn
        # registry should have regenerated upon call to unpickling __setstate__
        looked_up_wrapper = lookup_sa_wrapper('spam')
        assert looked_up_wrapper is da._supply_z3c_sa_wrapper()

    def test_supply_z3c_sa_wrapper(self):
        da = self.createDA(id='spam')
        wrapper = da._supply_z3c_sa_wrapper()
        assert type(wrapper) is ZopeWrapper

    def test_supply_z3c_sa_wrapper_no_dsn(self):
        da = self.createDA(id='spam')
        da.dsn = None
        wrapper = da._supply_z3c_sa_wrapper()
        assert wrapper is None

    def test_supply_z3c_sa_wrapper_no_util_id(self):
        da = self.createDA(id='spam')
        da.util_id = None
        wrapper = da._supply_z3c_sa_wrapper()
        # should have created a new ZopeWrapper instance
        assert type(wrapper) is ZopeWrapper

    def test_sa_zope_wrapper_lost_attrs(self):
        da = self.createDA(id='spam')
        da.util_id = None
        da.dsn = ''
        with LogCapture() as loggy:
            wrapper = da.sa_zope_wrapper()
            log_msg = str(loggy)
            assert str(type(da)) in log_msg
            assert "dsn is ''" in log_msg
            assert "util_id is 'None'" in log_msg
            assert type(wrapper) is ZopeWrapper

    @patch('Products.SQLAlchemyDA.da.createSAWrapper')
    def test_sa_zope_wrapper_round_and_round(self, mock_func):
        mock_func.side_effect = ValueError
        da = self.createDA(id='oonique')
        with LogCapture() as loggy:
            wrapper = da._supply_z3c_sa_wrapper()
            log_msg = str(loggy)
            assert "Unexpected failure" in log_msg
            assert "found or created" in log_msg
            assert wrapper is None

    def test_sa_zope_wrapper(self):
        da = self.createDA(id='spam')
        wrapper = da.sa_zope_wrapper()
        assert type(wrapper) is ZopeWrapper

    def test_legacy_property__wrapper(self):
        da = self.createDA(id='spam')
        wrapper = da.sa_zope_wrapper()
        assert type(wrapper) is ZopeWrapper


class SQLAlchemyDAFunctionalTests(TestBase, ZopeTestCase.FunctionalTestCase):

    def afterSetUp(self):
        from z3c.sqlalchemy import createSAWrapper
        self.folder_path = '/' + self.folder.absolute_url(1)
        self.dsn = os.environ.get('TEST_DSN', 'sqlite:///sqlitetestdb2')
        wrapper = createSAWrapper(self.dsn)
        metadata.bind = wrapper.engine
        metadata.create_all()
        self.session = wrapper.session

    def testZsqlInsertWithCommit(self):
        self.createDA()
        template = "INSERT INTO test (id, text) VALUES (07, 'bar')"
        manage_addZSQLMethod(self.app, 'zsql_id', 'title', 'da', '', template)
        self.app['zsql_id']()
        self.publish(self.folder_path)
        rows = self.session.query(Test).all()
        self.assertEqual(len(rows), 1)

    def testZsqlInsertWithRollback(self):
        self.createDA()
        template = "INSERT INTO test (id, text) VALUES (07, 'bar')"
        manage_addZSQLMethod(self.app, 'zsql_id', 'title', 'da', '', template)
        self.app['zsql_id']()
        transaction.abort()
        rows = self.session.query(Test).all()
        self.assertEqual(len(rows), 0)

    def testORMInsertWithCommit(self):
        t1 = Test(id=8, utext='Hello world', text='hello world')
        t2 = Test(id=9, utext='foo', text='far')
        self.session.add(t1)
        self.session.add(t2)
        self.publish(self.folder_path)
        rows = self.session.query(Test).all()
        self.assertEqual(len(rows), 2)

    def testORMInsertWithRollback(self):
        t1 = Test(id=8, utext='Hello world', text='hello world')
        t2 = Test(id=9, utext='foo', text='far')
        self.session.add(t1)
        self.session.add(t2)
        transaction.abort()
        rows = self.session.query(Test).all()
        self.assertEqual(len(rows), 0)

    def beforeTearDown(self):
        from ..da import clear_sa_wrapper_registry
        clear_sa_wrapper_registry()
        metadata.drop_all()

    def test_lookup_sa_wrapper(self):
        from ..da import lookup_sa_wrapper
        da = self.createDA(id='da')
        wrapper = lookup_sa_wrapper('da')
        assert wrapper is da.sa_zope_wrapper()

    def test_lookup_two_sa_wrappers(self):
        from ..da import lookup_sa_wrapper
        da1 = self.createDA(id='da1')
        da2 = self.createDA(id='da2')
        wrapper1 = lookup_sa_wrapper('da1')
        assert wrapper1 is da1.sa_zope_wrapper()
        wrapper2 = lookup_sa_wrapper('da2')
        assert wrapper2 is da2.sa_zope_wrapper()

    def test_lookup_nonexistent_sa_wrapper(self):
        from ..da import lookup_sa_wrapper
        with self.assertRaises(LookupError):
            lookup_sa_wrapper('dada')

    def test_deregister_nonexistent_da(self):
        from ..da import deregister_sa_wrapper
        from ..da import lookup_sa_wrapper

        # nonexistent deregistrations have no effect
        deregister_sa_wrapper('yada-yada')
        self.assertRaises(LookupError, lookup_sa_wrapper, 'yada-yada')

    def test_clear_sa_wrapper_registry(self):
        from ..da import clear_sa_wrapper_registry
        from ..da import lookup_sa_wrapper
        da = self.createDA(id='ya-ya')
        wrapper = lookup_sa_wrapper('ya-ya')
        assert wrapper is da.sa_zope_wrapper()
        clear_sa_wrapper_registry()
        with self.assertRaises(LookupError):
            lookup_sa_wrapper('ya-ya')
