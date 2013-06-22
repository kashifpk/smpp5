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

    
Setting up a python 2.7.x virtualenv for PyCK based web interface
=================================================================

1. Make sure you're logged in as a normal user and there is no virtual environment activated for your current shell (run deactivate if you're in a virtualenv)

2. Setup a python 2.7.x virtual env::

    virtualenv pyckenv

3. Activate the environment::

    source pyck/bin/activate

4. Install pyck::

    pip install pyck

5. (optional) - If you have not yet created the pyck project you can start doing that now.

How to work on the project
==========================

1. Open up two terminals (Konsole)

2. Activate the python 3 virtual environment in first terminal. We will use this to work on the SMPP part of the project::

    source py3env/bin/activate

3. Activate the pyckenv in the second terminal. This will be used for running the web interface etc::

    source pyckenv/bin/activate

* Whenever you need to do something related to the web portion of the project, use the second terminal (pyckenv)

* All work that you do on the SMPP code etc should be done in the first terminal (py3env)

    