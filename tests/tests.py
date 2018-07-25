from dxf2svg import dxf2svg
import os

test_dxf_path = os.path.join(os.path.dirname(__file__), 'drawing.dxf')
#---
dxf2svg.save_svg_from_dxf(test_dxf_path, frame_name='drawing1')
dxf2svg.save_svg_from_dxf(test_dxf_path, frame_name='spam')
dxf2svg.save_svg_from_dxf(test_dxf_path)
dxf2svg.extract_all(test_dxf_path)