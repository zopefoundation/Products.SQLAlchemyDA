###########################################################################
# SQLAlchemyDA tests
###########################################################################

"""
Tests for SQLAlchemyDA
"""


import sys, os, unittest
from Testing import ZopeTestCase
ZopeTestCase.installProduct('SQLAlchemyDA', 1)

from Products.SQLAlchemyDA.da import SAWrapper
from z3c.sqlalchemy import createSAWrapper
from sqlalchemy import MetaData, Table, Column, Integer, String, Unicode
from sqlalchemy.orm import mapper


class SQLAlchemyDATests(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):

        self.dsn = os.environ.get('TEST_DSN', 'sqlite:///test')
        wrapper = createSAWrapper(self.dsn, name='foo')
        metadata = MetaData(bind=wrapper.engine)

        test_table = Table('test', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('utext', Unicode(255)),
                      Column('text', String(255)))

        class Test(object): pass
        mapper(Test, test_table)

        metadata.create_all()
        session = wrapper.session
        session.save(Test(id=1, utext=u'Hello world', text='hello world'))
        session.save(Test(id=2, utext=u'foo', text='far'))


    def makeOne(self, **kw):
        factory = self.app.manage_addProduct['SQLAlchemyDA']
        factory.manage_addSAWrapper(id='da', title='da',        
                                    dsn=self.dsn,
                                    **kw)
        return self.app['da']

    def test1(self):
        da = self.makeOne()
        


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


