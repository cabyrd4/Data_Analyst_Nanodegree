# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 17:04:35 2016

@author: carvusbyrdiv
"""
import xml.etree.cElementTree as ET
import pprint
import re

OSMFILE = '/data/raleigh_north-carolina.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#function to count and aggregate tags with potential errors
def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib['k']
        if re.match(lower, key) != None:
            keys['lower'] += 1
        elif re.match(lower_colon, key) != None:
            keys['lower_colon'] += 1
        elif re.match(problemchars, key) != None:
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map(OSMFILE)
    pprint.pprint(keys)


if __name__ == "__main__":
    test()