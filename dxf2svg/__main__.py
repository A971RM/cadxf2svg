'''
--------------------------------------------------------------------------
Copyright (C) 2018 Lukasz Laba <lukaszlab@o2.pl>

This file is part of dxf2svg.

Dxf2svg is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Dxf2svg is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

from dxf2svg.pycore import *

def main():
    console_path = os.getcwd()
    #---
    if len(sys.argv) == 1:
        sys.argv.append(None)
        sys.argv.append(None)
    if len(sys.argv) == 2:
        sys.argv.append(None)
    #---
    if sys.argv[1]:
        dxffilename_to_convert = sys.argv[1]
        dxf_path = os.path.join(console_path, dxffilename_to_convert)
        if os.path.isfile(dxf_path):
            print('Extracting %s ..'%os.path.basename(dxf_path))
            #---
            try:
                size = int(sys.argv[2])
            except:
                print ('!!size parameter wrong format - %s given, default size will be used !!'%sys.argv[2])
                size = None
            #---
            if size:
                extract_all(dxf_path, size=size)
            else:
                extract_all(dxf_path)
        else:
            print('File %s not exist'%dxf_path)

if __name__ == "__main__":
    main()