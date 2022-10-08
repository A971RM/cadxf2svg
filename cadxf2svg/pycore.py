'''
--------------------------------------------------------------------------
Copyright (C) 2018-2022 Lukasz Laba <lukaszlab@o2.pl>

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

import os
import queue
import sys
from math import sqrt, sin, cos, pi

import ezdxf
import numpy as np
import svgwrite

LAYER = 'svgframe'
SVG_MAXSIZE = 300
SCALE = 1.0

def get_dxf_dwg_from_file(dxffilepath):
    return ezdxf.readfile(dxffilepath)

def get_clear_svg(minx=43.5, miny=-135.6, width=130.1, height=105.2):
    if width > height:
        size = (SVG_MAXSIZE, height/width*SVG_MAXSIZE)
    else:
        size = (width/height*SVG_MAXSIZE, SVG_MAXSIZE)
    svg = svgwrite.Drawing(size = size, viewBox="%s %s %s %s"%(minx, miny, width, height), style="background-color: #000;")
    return svg

def get_empty_svg(alerttext='! nothing to display !'):
    svg = svgwrite.Drawing(size = (SVG_MAXSIZE, SVG_MAXSIZE), viewBox="0 0 %s %s"%(SVG_MAXSIZE, SVG_MAXSIZE))
    svg.add(svgwrite.Drawing().text(alerttext, insert=[50, 50], font_size = 20))
    return svg

#--------------------------------------------------
def get_entity_rgb(entity):
    """
    得到颜色信息
    :param entity:
    :return:
    """
    if entity.rgb:
        r, g, b = entity.rgb
    elif entity.dxf.color == ezdxf.lldxf.const.BYLAYER:
        layer = entity.doc.layers.get(entity.dxf.layer)
        aci = layer.get_color()
        rgb24 = ezdxf.colors.DXF_DEFAULT_COLORS[aci]
        r, g, b = ezdxf.colors.int2rgb(rgb24)
    else:
        aci = entity.dxf.color
        rgb24 = ezdxf.colors.DXF_DEFAULT_COLORS[aci]
        r, g, b = ezdxf.colors.int2rgb(rgb24)
    return r, g, b


#--------------------------------------------------
def trans_line(dxf_entity):
    r, g, b = get_entity_rgb(dxf_entity)
    strock = f"rgb({r},{g},{b})"    
    start = dxf_entity.ocs().to_wcs(dxf_entity.dxf.start)
    end = dxf_entity.ocs().to_wcs(dxf_entity.dxf.end)
    line_start = list(start)[:2]
    line_end = list(end)[:2]
    d = f"M {line_start[0]},{line_start[1]} L {line_end[0]},{line_end[1]}"
    svg_entity = svgwrite.Drawing().path(d=d, stroke = strock, fill="none", stroke_width = 1.0/SCALE )
    svg_entity.scale(SCALE,-SCALE)
    return svg_entity

def trans_circle(dxf_entity):
    r, g, b = get_entity_rgb(dxf_entity)
    strock = f"rgb({r},{g},{b})"    
    center = dxf_entity.ocs().to_wcs(dxf_entity.dxf.center)
    circle_center = list(center)[:2]
    circle_radius = dxf_entity.dxf.radius
    svg_entity = svgwrite.Drawing().circle(center=circle_center, r=circle_radius, stroke = strock, fill="none", stroke_width = 1.0/SCALE )
    svg_entity.scale(SCALE,-SCALE)
    return svg_entity

def trans_arc(dxf_entity):
    r, g, b = get_entity_rgb(dxf_entity)
    strock = f"rgb({r},{g},{b})"    
    center = dxf_entity.dxf.center
    radius = dxf_entity.dxf.radius

    start_angle=dxf_entity.dxf.start_angle
    end_angle=dxf_entity.dxf.end_angle
    rad = np.deg2rad(start_angle)
    startX = center.x + radius * np.cos(rad)
    startY = center.y + radius * np.sin(rad)

    rad = np.deg2rad(end_angle)
    endX = center.x + radius * np.cos(rad)
    endY = center.y + radius * np.sin(rad)

    start = dxf_entity.ocs().to_wcs([startX, startY, 0])
    end = dxf_entity.ocs().to_wcs([endX, endY, 0])

    clock = dxf_entity.ocs().to_wcs([1, 1, 0])
    sweep_flag = 1 if np.sign(clock[0]) > 0 else 0

    d = f"M {start[0]},{start[1]} A {radius} {radius} 0 0 {sweep_flag} {end[0]},{end[1]}"
    svg_entity = svgwrite.Drawing().path(d=d, stroke = strock, fill="none", stroke_width = 1.0/SCALE )
    svg_entity.scale(SCALE,-SCALE)
    return svg_entity

def trans_text(dxf_entity):
    r, g, b = get_entity_rgb(dxf_entity)
    strock = f"rgb({r},{g},{b})"    
    text_text = dxf_entity.dxf.text
    insert = dxf_entity.ocs().to_wcs(dxf_entity.dxf.insert)
    text_insert = list(insert)[:2]
    text_height = dxf_entity.dxf.height * 1.4 # hotfix - 1.4 to fit svg and dwg
    svg_entity = svgwrite.Drawing().text(text_text, insert=[0, 0], font_size = text_height*SCALE, fill=strock)
    svg_entity.translate(text_insert[0]*(SCALE), -text_insert[1]*(SCALE))
    return svg_entity

def trans_lwpolyline(dxf_entity):
    r, g, b = get_entity_rgb(dxf_entity)
    strock = f"rgb({r},{g},{b})"    
    points = [(dxf_entity.ocs().to_wcs(x)[0], dxf_entity.ocs().to_wcs(x)[1]) for x in dxf_entity.get_points('xy')]
    if dxf_entity.is_closed:
        points.append(points[0])
    svg_group = svgwrite.container.Group()
    for i in range(1, len(points)):
        line_start = points[i-1]
        line_end = points[i]
        d = f"M {line_start[0]},{line_start[1]} L {line_end[0]},{line_end[1]}"
        svg_entity = svgwrite.Drawing().path(d=d, stroke = strock, fill="none", stroke_width = 1.0/SCALE )
        svg_entity.scale(SCALE,-SCALE)
        svg_group.add(svg_entity)
    return svg_group

def trans_polyline(dxf_entity):
    r, g, b = get_entity_rgb(dxf_entity)
    strock = f"rgb({r},{g},{b})"    
    points = [(dxf_entity.ocs().to_wcs(x)[0], dxf_entity.ocs().to_wcs(x)[1]) for x in dxf_entity.points()]
    if dxf_entity.is_closed:
        points.append(points[0])
    svg_group = svgwrite.container.Group()
    for i in range(1, len(points)):
        line_start = points[i-1]
        line_end = points[i]
        d = f"M {line_start[0]},{line_start[1]} L {line_end[0]},{line_end[1]}"
        svg_entity = svgwrite.Drawing().path(d=d, stroke = strock, fill="none", stroke_width = 1.0/SCALE )
        svg_entity.scale(SCALE,-SCALE)
        svg_group.add(svg_entity)
    return svg_group

#--------------------------------------------------

def entity_filter(dxffilepath, frame_name=None):
    dxf = get_dxf_dwg_from_file(dxffilepath)
    #----
    # 返回的数据
    entities = []
    xmin = float('inf')
    xmax = float('-inf')
    ymin = float('inf')
    ymax = float('-inf')

    # 使用队列，先进先出遍历
    q = queue.Queue()
    for e in dxf.modelspace():
        q.put(e)

    while not q.empty():
        entity = q.get()
        if entity.dxftype() != 'INSERT':
            entities.append(entity)
            continue

        # INSERT时，为块参考
        try:
            for ve in entity.virtual_entities():
                q.put(ve)
        except Exception as e:
            print("EXPLOID Error. ", e)

    for e in entities:
        if e.dxftype() == 'LINE':
            start = e.ocs().to_wcs(e.dxf.start)
            end = e.ocs().to_wcs(e.dxf.end)
            xmin = min(xmin, start[0], end[0])
            xmax = max(xmax, start[0], end[0])
            ymin = min(ymin, start[1], end[1])
            ymax = max(ymax, start[1], end[1])
        elif e.dxftype() == 'CIRCLE':
            center = e.ocs().to_wcs(e.dxf.center)
            # e.dxf.radius
            xmin = min(xmin, center[0] - e.dxf.radius)
            xmax = max(xmax, center[0] + e.dxf.radius)
            ymin = min(ymin, center[1] - e.dxf.radius)
            ymax = max(ymax, center[1] + e.dxf.radius)
        elif e.dxftype() == 'TEXT':
            insert = e.ocs().to_wcs(e.dxf.insert)
            xmin = min(xmin, insert[0])
            xmax = max(xmax, insert[0])
            ymin = min(ymin, insert[1])
            ymax = max(ymax, insert[1])
        elif e.dxftype() == 'ARC':
            # center = e.dxf.center[:2]
            radius = e.dxf.radius
        elif e.dxftype() == 'LWPOLYLINE':
            x = [e.ocs().to_wcs(p)[0] for p in e.get_points('xy')]
            y = [e.ocs().to_wcs(p)[1] for p in e.get_points('xy')]
            xmin = min(xmin, min(x))
            xmax = max(xmax, max(x))
            ymin = min(ymin, min(y))
            ymax = max(ymax, max(y))
        elif e.dxftype() == 'POLYLINE':
            x = [e.ocs().to_wcs(p)[0] for p in e.points()]
            y = [e.ocs().to_wcs(p)[1] for p in e.points()]
            xmin = min(xmin, min(x))
            xmax = max(xmax, max(x))
            ymin = min(ymin, min(y))
            ymax = max(ymax, max(y))


    xmargin = 0.05*abs(xmax - xmin)
    ymargin = 0.05*abs(ymax - ymin)
    print ([xmin - xmargin, xmax + xmargin, ymin - ymargin, ymax + ymargin])
    return entities, [xmin - xmargin, xmax + xmargin, ymin - ymargin, ymax + ymargin]

#--------------------------------------------------

def get_svg_form_dxf(dxffilepath, frame_name=None):
    global SCALE
    #---
    entites_filter = entity_filter(dxffilepath, frame_name)
    entites = entites_filter[0]
    frame_coord = entites_filter[1]
    #---
    if not entites:
        return get_empty_svg()
    #---
    minx= frame_coord[0]
    miny= -frame_coord[3]
    width= abs(frame_coord[0] - frame_coord[1])
    height=abs(frame_coord[2] - frame_coord[3])
    SCALE = 1.0*SVG_MAXSIZE/max(width, height)
    #---
    svg = get_clear_svg(minx*SCALE, miny*SCALE, width*SCALE, height*SCALE)
    for e in entites:
        if e.dxftype() == 'LINE': svg.add(trans_line(e))
        if e.dxftype() == 'LWPOLYLINE': svg.add(trans_lwpolyline(e))
        if e.dxftype() == 'POLYLINE': svg.add(trans_polyline(e))
        if e.dxftype() == 'CIRCLE': svg.add(trans_circle(e))
        if e.dxftype() == 'TEXT': svg.add(trans_text(e))
        if e.dxftype() == 'ARC': svg.add(trans_arc(e))
    return svg

#--------------------------------------------------

def save_svg_from_dxf(dxffilepath, svgfilepath=None, frame_name=None, size = 300):
    global SVG_MAXSIZE
    _oldsize = SVG_MAXSIZE
    SVG_MAXSIZE = size
    #---
    if frame_name:
        print('>>making %s svgframe for %s ...'%(frame_name, os.path.basename(dxffilepath)))
    else:
        print('making svg for %s ...'%(os.path.basename(dxffilepath)))
        pass
    #---
    svg = get_svg_form_dxf(dxffilepath, frame_name)
    if frame_name: postfix = '_%s'%frame_name
    else: postfix = ''
    if not svgfilepath:
        svgfilepath = dxffilepath.replace('.dxf', '%s.svg'%postfix)
    svg.saveas(svgfilepath, pretty=True)
    print ('      .. saved as %s'%os.path.basename(svgfilepath))
    #---
    SVG_MAXSIZE = _oldsize

def extract_all(dxffilepath, size = 300):
    # dxf = get_dxf_dwg_from_file(dxffilepath)
    #---
    frame_list = []
    # for e in dxf.modelspace():
    #     if e.dxftype() == 'TEXT' and e.dxf.layer == LAYER:
    #         frame_list.append(e.dxf.text)
    #---
    if frame_list:
        for frame in frame_list:
            try:
                save_svg_from_dxf(dxffilepath, frame_name = frame, size = size)
            except:
                pass
    else:
            try:
                save_svg_from_dxf(dxffilepath, size = size)
            except:
                pass