import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'PyCK',
    'pyramid',
    'sqlalchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_handlers',
    'zope.sqlalchemy',
    'wtforms',
    'wtdojo',
    'pymysql'
    ]

if sys.version_info[:3] < (2, 5, 0):
    requires.append('pysqlite')

setup(name='smpp5web',
      version='0.0',
      description='smpp5web',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='smpp5web',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = smpp5web:main
      [console_scripts]
      populate_smpp5web = smpp5web.scripts.populate:main
      smpp5web_newapp = smpp5web.scripts.newapp:main
      """,
      )
