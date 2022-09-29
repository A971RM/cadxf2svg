==============================
CADxf2svg - dxf to svg converter
==============================

CADxf2svg is a dxf to svg format converter.

This project comes from: https://bitbucket.org/lukaszlaba
And Thanks to Łukasz Laba.
Please refer to the url for origin code.

Changelog
---------

cadxf2svg 1.0.0

- support INSERT
- support ARC
- support Color
- DONOT support frame filter

dxf2svg 0.1.4

- python 2 support dropped
- POLYLINE support added

dxf2svg 0.1.1

- first public release (alfa stage)
- LINE, CIRCE, TEXT dxf entity supported
- all entities go to one linetype, color and weight

Requirements
------------
1. svgwrite (https://pypi.python.org/pypi/svgwrite)
2. ezdxf (https://pypi.python.org/pypi/ezdxf)
2. numpy (https://pypi.python.org/pypi/numpy)

How to install
--------------
Dxf2svg is available through PyPI and can be install with pip command. To install dxf2svg and needed requirements use pip by typing ::

  pip install svgwrite

Using dxf2svg
-------------

In the most simple case, set the current directory to the location of your drawing.dxf and execute::

  python -m dxf2svg drawing.dxf.dxf

You can also specify output svg size you want, for example ::

  python -m dxf2svg drawing.dxf.dxf 300

After that you will get output svg files in the same directory where your drawing.dxf is.
Please check project website for more information.

Limitation
----------
At the moment not all dxf entitie types are supported during converting. It convert LINE, CIRCE, TEXT, POLYLINE and all those entities go to one linetype, color and weight in produced SVG.

Licence
-------
Dxf2svg is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Copyright (C) 2018 - 2022 Lukasz Laba <lukaszlaba@gmail.com>

Contributions
-------------
If you want to help out, create a pull request or write email.

