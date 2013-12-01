#!/usr/bin/env python

from lxml import etree
import json, sys

tree = etree.parse("doc.kml")

def recursive_dict(element):
    return element.tag, \
        dict(map(recursive_dict, element)) or element.text

all_points = []

color_codes = {"Active Satellites": 0, "Inactive Satellites": 1, "Debris": 2}

for folder in tree.findall('.//Folder'):
    group_name = folder.find('.//name').text

    if group_name not in color_codes.keys():
        continue

    group_number = color_codes[group_name]

    points = []

    for placemark in folder.findall('.//Placemark'):
        name = placemark.find('.//name').text
        coords = placemark.find('.//Point/coordinates').text

        lon, lat, alt = map(float, coords.split(','))

        points.append(lat)
        points.append(lon)
        points.append(alt)
        points.append(group_number)

    all_points.extend(points)

# Earth's radius in meters
earth_radius = 6378100.0

for i in xrange(2, len(all_points), 4):
    all_points[i] = float(all_points[i]) / (earth_radius)

print json.dumps(all_points)
