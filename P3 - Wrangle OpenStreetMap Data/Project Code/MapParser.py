# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 16:20:08 2016

@author: carvusbyrdiv
"""
import xml.etree.cElementTree as ET
import pprint

OSMFILE = '/data/raleigh_north-carolina.osm'

#function to count tags by tag type (node, way, etc.)
def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags


def test():

    tags = count_tags(OSMFILE)
    pprint.pprint(tags)

    

if __name__ == "__main__":
    test()
