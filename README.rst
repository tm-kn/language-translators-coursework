###############################
Language Translators Coursework
###############################

Using JavaCup v0.10g for generating parsers.

*******************
Repository Contents
*******************
This package contains three parts. Each of the parts contains:

* ``unit_tests`` - folder with unit tests.
* ``test_programmes`` - folder with example programmes.
* ``parser.cup`` - JavaCUP file with grammar.
* ``scanner.java`` - Scanner/lexer/lexical analyser.

======
Part 1
======
Simple parser for the following grammar.

::

    <w> ::=  <w> & <p>  |  <w> + <p>  |  <p>
    <p> ::=  ! <p>  |  0  |  1  |  ?  |  <v>
    <v> ::=  k  |  n

It prints pase trees for input and validates whether string is part of the language.

======
Part 2
======


======
Part 3
======



*****
Usage
*****
========
Makefile
========
Every part has a ``Makefile`` included with.

-------
Compile
-------

.. code:: bash

    make # or "make compile"


--------------
Run Unit Tests
--------------
Make sure you have Python 3 installed.

.. code:: bash

    make test

---------------
Clean Directory
---------------
Deletes compiled files, e.g. when you want to compile from scratch again.

.. code:: bash

    make clean

============
Using parser
============
After you successfully compiled the parser (i.e. parser.class is present) you can use it in the following way.

.. code:: bash

    java parser < test_programmes/valid1

Where ``test_programmes/valid1`` is just a file with programme we want to parse.
