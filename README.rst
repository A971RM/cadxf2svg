==============================
Dxf2svg - dxf to svg converter
==============================

Dxf2svg is a dxf to svg format converter.

Changelog
---------

dxf2svg 0.1.3

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

More information
----------------
Project website: https://bitbucket.org/lukaszlaba/dxf2svg/wiki

Code repository: https://bitbucket.org/lukaszlaba/dxf2svg

PyPI package: https://pypi.python.org/pypi/dxf2svg

Contact: Lukasz Laba <lukaszlaba@gmail.com>