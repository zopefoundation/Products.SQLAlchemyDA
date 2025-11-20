##########################################################################
# SQLAlchemyDA
# (C) 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

from setuptools import setup


readme_file = 'README.rst'
changes_file = 'CHANGES.rst'
desc = open(readme_file).read().strip()
changes = open(changes_file).read().strip()
long_description = desc + "\n\nCHANGES\n=======\n\n" + changes


setup(name='Products.SQLAlchemyDA',
      version='3.1.dev0',
      url='https://github.com/zopefoundation/Products.SQLAlchemyDA',
      project_urls={
          'Issue Tracker': ('https://github.com/zopefoundation/'
                            'Products.SQLAlchemyDA/issues'),
          'Sources': 'https://github.com/zopefoundation/Products.SQLAlchemyDA',
      },
      license='ZPL-2.1',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      maintainer='Zope Foundation and Contributors',
      maintainer_email='zope-dev@zope.dev',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Operating System :: OS Independent',
          'Framework :: Zope',
          'Framework :: Zope :: 5',
          'Programming Language :: Python',
          'Topic :: Database',
          'Topic :: Database :: Front-Ends',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Programming Language :: Python :: 3.14',
      ],
      keywords='Zope Database adapter SQLAlchemy',
      description='A generic database adapter for Zope',
      long_description=long_description,
      python_requires='>=3.10',
      install_requires=[
          'SQLAlchemy',
          'z3c.sqlalchemy >1.5.1',
          'Products.ZSQLMethods'],
      extras_require={'test': ['testfixtures']},
      include_package_data=True,
      )
