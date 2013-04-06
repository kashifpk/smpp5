smpp5
=====

SMPP Version 5 Library, client and server

Note:
=====

This package works with python 3.x and is not compatible with python 2.x

Setting up a python 3 virtualenv for development
=================================================

These instructions are for debian/ubuntu based systems. Users of other distributions should modify these according
to their distribution.

1. Install python setuptools if not already present on your system::

    sudo apt-get install python-setuptools

2. Install pip if not already present::

    sudo easy_install pip

3. Install virtualenv::

    sudo pip install virtualenv

4. Setup a python3.x virtual env::

    virtualenv -p /usr/bin/python3 py3env

5. Activate the environment::

    source py3env/bin/activate

6. Install nose (for running a test cases)

    pip install nose
