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
import sys
from math import sqrt, sin, cos, pi

import ezdxf
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
    svg = svgwrite.Drawing(size = size, viewBox="%s %s %s %s"%(minx, miny, width, height))
    return svg

def get_empty_svg(alerttext='! nothing to display !'):
    svg = svgwrite.Drawing(size = (SVG_MAXSIZE, SVG_MAXSIZE), viewBox="0 0 %s %s"%(SVG_MAXSIZE, SVG_MAXSIZE))
    svg.add(svgwrite.Drawing().text(alerttext, insert=[50, 50], font_size = 20))
    return svg

#--------------------------------------------------

def trans_line(dxf_entity):
    line_start = dxf_entity.dxf.start[:2]
    line_end = dxf_entity.dxf.end[:2]
    svg_entity = svgwrite.Drawing().line(start=line_start, end=line_end, stroke = "black", stroke_width = 1.0/SCALE )
    svg_entity.scale(SCALE,-SCALE)
    return svg_entity

def trans_circle(dxf_entity):
    circle_center = dxf_entity.dxf.center[:2]
    circle_radius = dxf_entity.dxf.radius
    svg_entity = svgwrite.Drawing().circle(center=circle_center, r=circle_radius, stroke = "black", fill="none", stroke_width = 1.0/SCALE )
    svg_entity.scale(SCALE,-SCALE)
    return svg_entity

def trans_arc(dxf_entity):
    circle_center = dxf_entity.dxf.center[:2]
    circle_radius = dxf_entity.dxf.radius
    svg_entity = svgwrite.Drawing().circle(center=circle_center, r=circle_radius, stroke = "black", fill="none", stroke_width = 1.0/SCALE )
    svg_entity.scale(SCALE,-SCALE)
    return svg_entity

def trans_text(dxf_entity):
    text_text = dxf_entity.dxf.text
    text_insert = dxf_entity.dxf.insert[:2]
    text_height = dxf_entity.dxf.height * 1.4 # hotfix - 1.4 to fit svg and dwg
    svg_entity = svgwrite.Drawing().text(text_text, insert=[0, 0], font_size = text_height*SCALE)
    svg_entity.translate(text_insert[0]*(SCALE), -text_insert[1]*(SCALE))
    return svg_entity

def trans_lwpolyline(dxf_entity):
    points = [(x[0], x[1]) for x in dxf_entity.get_points()]
    if dxf_entity.CLOSED == 1:
        svg_entity = svgwrite.Drawing().polyline(points=points, stroke='black', fill='none', stroke_width=1.0/SCALE)
    else:
        svg_entity = svgwrite.Drawing().polyline(points=points, stroke='black', fill='none', stroke_width=1.0/SCALE)
    svg_entity.scale(SCALE, -SCALE)
    return svg_entity

def trans_polyline(dxf_entity):
    points = [(x[0], x[1]) for x in dxf_entity.points()]
    if dxf_entity.CLOSED == 1:
        svg_entity = svgwrite.Drawing().polygon(points=points, stroke='black', fill='none', stroke_width=1.0/SCALE)
    else:
        svg_entity = svgwrite.Drawing().polyline(points=points, stroke='black', fill='none', stroke_width=1.0/SCALE)
    svg_entity.scale(SCALE, -SCALE)
    return svg_entity

#--------------------------------------------------

def entity_filter(dxffilepath, frame_name=None):
    dxf = get_dxf_dwg_from_file(dxffilepath)
    #----
    frame_rect_entity = None
    name_text_entity = None
    #---
    if frame_name:
        for e in dxf.modelspace():
            if e.dxftype() == 'TEXT' and e.dxf.layer == LAYER:
                if e.dxf.text == frame_name:
                    name_text_entity = e
    if name_text_entity:
        text_point = name_text_entity.dxf.insert[:2]
        text_height = name_text_entity.dxf.height
        for e in dxf.modelspace():
            if e.dxftype() == 'LWPOLYLINE' and e.dxf.layer == LAYER:
                points = list(e.get_points())
                for p in points:
                    dist = sqrt((p[0] - text_point[0])**2+(p[1] - text_point[1])**2)
                    if dist < 1.0 * text_height:
                        frame_rect_entity = e
    #---
    if frame_rect_entity and name_text_entity:
        frame_points = list(frame_rect_entity.get_points())
        entitys_in_frame = []
        xmin = min([i[0] for i in frame_points])
        xmax = max([i[0] for i in frame_points])
        ymin = min([i[1] for i in frame_points])
        ymax = max([i[1] for i in frame_points])
        for e in dxf.modelspace():
            point = None
            if e.dxftype() == 'LINE': point = e.dxf.start[:2]
            if e.dxftype() == 'CIRCLE': point = e.dxf.center[:2]
            if e.dxftype() == 'TEXT': point = e.dxf.insert[:2]
            if e.dxftype() == 'ARC':
                center = e.dxf.center[:2]
                radius = e.dxf.radius
                start_angle = e.dxf.start_angle/ 360.0 * 2 * pi
                delta_x = radius * cos(start_angle)
                delta_y = radius * sin(start_angle)
                point = (center[0]+delta_x, center[1]+delta_y)
            if e.dxftype() == 'LWPOLYLINE':
                x = [p[0] for p in e.get_points()]
                y = [p[1] for p in e.get_points()]
                point = (x[0], y[0])
            if point:
                if (xmin <= point[0] <= xmax) and (ymin <= point[1] <= ymax):
                    if not e.dxf.layer == LAYER:
                        entitys_in_frame.append(e)
        return entitys_in_frame, [xmin, xmax, ymin, ymax]
    elif frame_name:
        return [], [300, 600, 300, 600]
    elif not frame_name:
        entitys = []
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        for e in dxf.modelspace():
            if not e.dxf.layer == LAYER:
                entitys.append(e)
                if e.dxftype() == 'LINE':
                    try:
                        xmin = min(xmin, e.dxf.start[0], e.dxf.end[0])
                        xmax = max(xmax, e.dxf.start[0], e.dxf.end[0])
                        ymin = min(ymin, e.dxf.start[1], e.dxf.end[1])
                        ymax = max(ymax, e.dxf.start[1], e.dxf.end[1])
                    except:
                        xmin = min(e.dxf.start[0], e.dxf.end[0])
                        xmax = max(e.dxf.start[0], e.dxf.end[0])
                        ymin = min(e.dxf.start[1], e.dxf.end[1])
                        ymax = max(e.dxf.start[1], e.dxf.end[1])
                if e.dxftype() == 'CIRCLE':
                    e.dxf.center[:2]
                    e.dxf.radius
                    try:
                        xmin = min(xmin, e.dxf.center[0] - e.dxf.radius)
                        xmax = max(xmax, e.dxf.center[0] + e.dxf.radius)
                        ymin = min(ymin, e.dxf.center[1] - e.dxf.radius)
                        ymax = max(ymax,  e.dxf.center[1] + e.dxf.radius)
                    except:
                        xmin = min(e.dxf.center[0] - e.dxf.radius)
                        xmax = max(e.dxf.center[0] + e.dxf.radius)
                        ymin = min(e.dxf.center[1] - e.dxf.radius)
                        ymax = max(e.dxf.center[1] + e.dxf.radius)
                if e.dxftype() == 'TEXT':
                    try:
                        xmin = min(xmin, e.dxf.insert[0])
                        xmax = max(xmax, e.dxf.insert[0])
                        ymin = min(ymin, e.dxf.insert[1])
                        ymax = max(ymax,  e.dxf.insert[1])
                    except:
                        xmin = min(e.dxf.insert[0])
                        xmax = max(e.dxf.insert[0])
                        ymin = min(e.dxf.insert[1])
                        ymax = max(e.dxf.insert[1])
                if e.dxftype() == 'ARC':
                    center = e.dxf.center[:2]
                    radius = e.dxf.radius
                if e.dxftype() == 'LWPOLYLINE':
                    x = [p[0] for p in e.get_points()]
                    y = [p[1] for p in e.get_points()]
                    try:
                        xmin = min(xmin, min(x))
                        xmax = max(xmax, max(x))
                        ymin = min(ymin, min(y))
                        ymax = max(ymax, max(y))
                    except:
                        xmin = min(min(x))
                        xmax = max(max(x))
                        ymin = min(min(y))
                        ymax = max(max(y))
                if e.dxftype() == 'POLYLINE':
                    x = [p[0] for p in e.points()]
                    y = [p[1] for p in e.points()]
                    try:
                        xmin = min(xmin, min(x))
                        xmax = max(xmax, max(x))
                        ymin = min(ymin, min(y))
                        ymax = max(ymax, max(y))
                    except:
                        xmin = min(min(x))
                        xmax = max(max(x))
                        ymin = min(min(y))
                        ymax = max(max(y))
        xmargin = 0.05*abs(xmax - xmin)
        ymargin = 0.05*abs(ymax - ymin)
        print ([xmin - xmargin, xmax + xmargin, ymin - ymargin, ymax + ymargin])
        return entitys, [xmin - xmargin, xmax + xmargin, ymin - ymargin, ymax + ymargin]

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
    svg.saveas(svgfilepath)
    print ('      .. saved as %s'%os.path.basename(svgfilepath))
    #---
    SVG_MAXSIZE = _oldsize

def extract_all(dxffilepath, size = 300):
    dxf = get_dxf_dwg_from_file(dxffilepath)
    #---
    frame_list = []
    for e in dxf.modelspace():
        if e.dxftype() == 'TEXT' and e.dxf.layer == LAYER:
            frame_list.append(e.dxf.text)
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