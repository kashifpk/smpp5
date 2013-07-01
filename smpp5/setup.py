from setuptools import setup, find_packages

requires = ['sqlalchemy', 'zope.sqlalchemy', 'pymysql3']

setup(
    name='smpp5',
    version='0.1',
    description='SMPP Version 5 library, client and server',
    long_description="""
    SMPP Version 5 library, client and server implementation
    """,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: SMPP",
    ],
    author='',
    author_email='',
    url='',
    keywords='smpp version 5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
