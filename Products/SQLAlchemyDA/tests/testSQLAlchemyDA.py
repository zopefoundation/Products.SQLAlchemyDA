###########################################################################
# SQLAlchemyDA tests
###########################################################################

"""
Tests for SQLAlchemyDA
"""


import sys
import os
import unittest
from Testing import ZopeTestCase

import transaction
from Products.SQLAlchemyDA.da import SAWrapper
from Products.ZSQLMethods.SQL import manage_addZSQLMethod
from z3c.sqlalchemy import createSAWrapper
from z3c.sqlalchemy.mapper import MappedClassBase
from sqlalchemy import MetaData, Table, Column, Integer, String, Unicode
from sqlalchemy.orm import mapper

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
        factory = self.app.manage_addProduct['SQLAlchemyDA']
        factory.manage_addSAWrapper(id='da', title='da',
                                    dsn=self.dsn,
                                    **kw)
        return self.app['da']


class SQLAlchemyDATests(TestBase):

    def afterSetUp(self):

        self.dsn = os.environ.get('TEST_DSN', 'sqlite:///test')
        wrapper = createSAWrapper(self.dsn)
        metadata.bind = wrapper.engine
        metadata.create_all()
        session = wrapper.session
        t1 = Test(id=1, utext=u'Hello world', text='hello world')
        t2 = Test(id=2, utext=u'foo', text='far')
        session.add(t1)
        session.add(t2)

    def testSimpleSelect(self):
        da = self.createDA()
        rows = da.query('select * from test')
        self.assertEqual(len(rows), 2)

    def testSimpleInsert(self):
        da = self.createDA()
        rows = da.query("insert into test (id, text) values(42, 'foo')")

    def testSimpleUpdate(self):
        da = self.createDA()
        rows = da.query("update test set text='bar'")

    def testExtraEngineOptions(self):
        da = self.createDA()
        da.add_extra_engine_options((('echo', True),
                                     ('pool_size', 20)))
        self.assertEqual(da.engine_options['pool_size'], 20)


class SQLAlchemyDAFunctionalTests(TestBase, ZopeTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.folder_path = '/' + self.folder.absolute_url(1)
        self.dsn = os.environ.get('TEST_DSN', 'sqlite:///test')
        wrapper = createSAWrapper(self.dsn)
        metadata.bind = wrapper.engine
        metadata.create_all()
        self.session = wrapper.session

    def testZsqlInsertWithCommit(self):
        da = self.createDA()
        template = "INSERT INTO test (id, text) VALUES (07, 'bar')"
        manage_addZSQLMethod(self.app, 'zsql_id', 'title', 'da', '', template)
        self.app['zsql_id']()
        self.publish(self.folder_path)
        rows = self.session.query(Test).all()
        self.assertEqual(len(rows), 1)
        
    def testZsqlInsertWithRollback(self):
        da = self.createDA()
        template = "INSERT INTO test (id, text) VALUES (07, 'bar')"
        manage_addZSQLMethod(self.app, 'zsql_id', 'title', 'da', '', template)
        self.app['zsql_id']()
        transaction.abort()
        rows = self.session.query(Test).all()
        self.assertEqual(len(rows), 0)
        
    def testORMInsertWithCommit(self):
        t1 = Test(id=8, utext=u'Hello world', text='hello world')
        t2 = Test(id=9, utext=u'foo', text='far')
        self.session.add(t1)
        self.session.add(t2)
        self.publish(self.folder_path)
        rows = self.session.query(Test).all()
        self.assertEqual(len(rows), 2)
        
    def testORMInsertWithRollback(self):
        t1 = Test(id=8, utext=u'Hello world', text='hello world')
        t2 = Test(id=9, utext=u'foo', text='far')
        self.session.add(t1)
        self.session.add(t2)
        transaction.abort()
        rows = self.session.query(Test).all()
        self.assertEqual(len(rows), 0)
        
    def beforeTearDown(self):
        metadata.drop_all()


def test_suite():
    s = unittest.TestSuite()
    s.addTests([unittest.makeSuite(SQLAlchemyDATests),
               unittest.makeSuite(SQLAlchemyDAFunctionalTests)])
    return s


def main():
    unittest.TextTestRunner().run(test_suite())


def debug():
    test_suite().debug()


def pdebug():
    import pdb
    pdb.run('debug()')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        globals()[sys.argv[1]]()
    else:
        main()
