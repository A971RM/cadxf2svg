================================ 
Dxf2svg - dxf to svg conventer
================================
Dxf2svg is a dxf to svg format conventer.

Changelog
---------

dxf2svg 0.1

- first public release (alfa stage)

Requirements
------------
1. Python 2 or 3
#. svgwrite (https://pypi.python.org/pypi/svgwrite)
#. dxfstructure (https://pypi.python.org/pypi/dxfstructure)

How to install
--------------
Dxf2svg is available through PyPI and can be install with pip command. To install Tebe use pip by typing::

  pip install dxf2svg

Using dxf2svg
-------------
The syntax of the dxf2svg command is ::

  dxf2svg dxffilename [size]

In the most simple case, set the current directory to the location of your drwing.dxf and execute::

  dxf2svg drwing.dxf

you can also specife output svg size you want, for example::

  dxf2svg drwing.dxf 300

After that you will get output svg files in the same directory where your drwing.dxf is.

Licence
-------
Dxf2svg is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Copyright (C) 2018 Lukasz Laba <lukaszlab@o2.pl>

Contributions
-------------
If you want to help out, create a pull request or write email.

More information
----------------
Project website: https://bitbucket.org/lukaszlaba/dxf2svg

Code repository: https://bitbucket.org/lukaszlaba/dxf2svg

PyPI package: https://pypi.python.org/pypi/dxf2svg

Contact: Lukasz Laba <lukaszlab@o2.pl>