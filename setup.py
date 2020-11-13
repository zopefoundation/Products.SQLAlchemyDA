##########################################################################
# SQLAlchemyDA
# (C) 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

from setuptools import find_packages
from setuptools import setup


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Zope Public License',
    'Operating System :: OS Independent',
    'Framework :: Zope',
    'Framework :: Zope :: 3',
    'Framework :: Zope :: 4',
    'Framework :: Zope :: 5',
    'Programming Language :: Python',
    'Topic :: Database',
    'Topic :: Database :: Front-Ends',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

version = '1.0.0'

readme_file = 'README.rst'
changes_file = 'CHANGES.rst'
desc = open(readme_file).read().strip()
changes = open(changes_file).read().strip()
long_description = desc + "\n\nCHANGES\n=======\n\n" + changes


setup(name='Products.SQLAlchemyDA',
      version=version,
      url='https://github.com/zopefoundation/Products.SQLAlchemyDA',
      project_urls={
          'Issue Tracker': ('https://github.com/zopefoundation/'
                            'Products.SQLAlchemyDA/issues'),
          'Sources': 'https://github.com/zopefoundation/Products.SQLAlchemyDA',
      },
      license='ZPL 2.1',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      maintainer='Zope Foundation and Contributors',
      maintainer_email='zope-dev@zope.org',
      classifiers=CLASSIFIERS,
      keywords='Zope Database adapter SQLAlchemy',
      description='A generic database adapter for Zope',
      long_description=long_description,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      install_requires=[
        'setuptools',
        'six',
        'z3c.sqlalchemy >1.5.1',
        'Products.ZSQLMethods'],
      extras_require={'test': ['testfixtures', 'mock']},
      namespace_packages=['Products'],
      )
