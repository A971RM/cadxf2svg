from dxf2svg import pycore
import os

test_dxf_path = os.path.join(os.path.dirname(__file__), 'Untitled.dxf')
#---
#pycore.save_svg_from_dxf(test_dxf_path, frame_name='drawing1')
#pycore.save_svg_from_dxf(test_dxf_path, frame_name='spam')
#pycore.save_svg_from_dxf(test_dxf_path, frame_name='fig1')
pycore.save_svg_from_dxf(test_dxf_path)
#pycore.extract_all(test_dxf_path)