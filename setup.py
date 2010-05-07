##########################################################################
# SQLAlchemyDA
# (C) 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

import os
from setuptools import setup, find_packages


CLASSIFIERS = [
    'Programming Language :: Python',
    'Framework :: Zope2',
    'Topic :: Database',
]

version = '0.5.0'

readme_file= os.path.join('Products', 'SQLAlchemyDA', 'README.txt')
changes_file = os.path.join('Products', 'SQLAlchemyDA', 'CHANGES.txt')
desc = open(readme_file).read().strip()
changes = open(changes_file).read().strip()

long_description = desc  + "\n\nCHANGES\n=======\n\n" + changes

#print long_description

setup(name='Products.SQLAlchemyDA',
      version=version,
      license='ZPL (see LICENSE.txt)',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      maintainer='Andreas Jung',
      maintainer_email='info@zopyx.com',
      classifiers=CLASSIFIERS,
      keywords='Zope2 Database adapter SQLAlchemy',
      url='http://opensource.zopyx.com/projects/SQLAlchemyDA',
      description='A generic database adapter for Zope 2',
      long_description=long_description,
      packages=['Products', 'Products.SQLAlchemyDA'],
      include_package_data = True,
      zip_safe=False,
      install_requires=['setuptools', 'z3c.sqlalchemy'],
      extras_require = {'test': ['Zope2']},
      namespace_packages=['Products'],

      )
