###########################################################################
# SQLAlchemyDA tests
###########################################################################

"""
Tests for SQLAlchemyDA
"""


import sys, os, unittest
from Testing import ZopeTestCase

import transaction
from Products.SQLAlchemyDA.da import SAWrapper
from z3c.sqlalchemy import createSAWrapper
from z3c.sqlalchemy.mapper import MappedClassBase
from sqlalchemy import MetaData, Table, Column, Integer, String, Unicode
from sqlalchemy.orm import mapper

ZopeTestCase.installProduct('SQLAlchemyDA', 1)

class SQLAlchemyDATests(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):

        self.dsn = os.environ.get('TEST_DSN', 'sqlite:///test')
        wrapper = createSAWrapper(self.dsn)
        metadata = MetaData(bind=wrapper.engine)

        test_table = Table('test', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('utext', Unicode(255)),
                      Column('text', String(255)))

        class Test(MappedClassBase): pass
        mapper(Test, test_table)

        metadata.create_all()
        session = wrapper.session
        t1 = Test(id=1, utext=u'Hello world', text='hello world')
        t2 = Test(id=2, utext=u'foo', text='far')
        session.save(t1)
        session.save(t2)


    def makeOne(self, **kw):
        factory = self.app.manage_addProduct['SQLAlchemyDA']
        factory.manage_addSAWrapper(id='da', title='da',        
                                    dsn=self.dsn,
                                    **kw)
        return self.app['da']

    def testSimpleSelect(self):
        da = self.makeOne()
        rows = da.query('select * from test')
        self.assertEqual(len(rows), 2)
        
    def testSimpleInsert(self):
        da = self.makeOne()
        rows = da.query("insert into test (id, text) values(42, 'foo')")
        
    def testSimpleUpdate(self):
        da = self.makeOne()
        rows = da.query("update test set text='bar'")

def test_suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(SQLAlchemyDATests))
    return s

def main():
    unittest.TextTestRunner().run(test_suite())

def debug():
    test_suite().debug()

def pdebug():
    import pdb
    pdb.run('debug()')

if __name__=='__main__':
    if len(sys.argv) > 1:
        globals()[sys.argv[1]]()
    else:
        main()
