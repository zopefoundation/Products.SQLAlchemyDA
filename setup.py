##########################################################################
# SQLAlchemyDA
# (C) 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

from setuptools import setup


CLASSIFIERS = [
    'Programming Language :: Python',
    'Framework :: Zope2',
    'Topic :: Database',
]

version = '0.6.1b1'

readme_file = 'README.rst'
changes_file = 'CHANGES.rst'
desc = open(readme_file).read().strip()
changes = open(changes_file).read().strip()

long_description = desc + "\n\nCHANGES\n=======\n\n" + changes

print(long_description)


setup(name='Products.SQLAlchemyDA',
      version=version,
      license='ZPL (see LICENSE.txt)',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      maintainer='Sheila Allen',
      maintainer_email='sallen@zeomega.com',
      classifiers=CLASSIFIERS,
      keywords='Zope2 Database adapter SQLAlchemy',
      url='https://github.com/zopefoundation/Products.SQLAlchemyDA',
      description='A generic database adapter for Zope 2',
      long_description=long_description,
      packages=['Products', 'Products.SQLAlchemyDA'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools', 'z3c.sqlalchemy'],
      extras_require={'test': ['Zope2', 'Products.ZSQLMethods']},
      namespace_packages=['Products'],

      )
