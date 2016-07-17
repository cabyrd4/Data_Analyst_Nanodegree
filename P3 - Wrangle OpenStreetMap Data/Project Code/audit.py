# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 20:40:47 2016

@author: carvusbyrdiv
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = '/data/raleigh_north-carolina.osm'
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
postcode_letter_re = re.compile('[a-zA-Z]')


# Street values I would expect to see on a map
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Way", "Walk", "Pike", "Terrace", "Circle", "Alley", 
            "Park", "Manor", "West", "Bypass", "Crossing", "Crescent", "East", "Loop", "Plaza", "Run",
            "Highway"]

# Street values I have found that should be edited programmatically
mapping = { "St": "Street",
            "St.": "Street",
            "ST": "Street",
            "St,": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "blvd": "Boulevard",
            "Courth": "Court",
            "Ct": "Court",
            "DR": "Drive",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ln": "Lane",
            "Ter": "Terrace",
            "drive": "Drive",
            "broadway": "Broadway",
            "CIrcle": "Circle",
            "Cir": "Circle",
            "Pl": "Place",
            "Pkwy": "Parkway",
            "Pky": "Parkway",
            "Pl": "Place",
            }

#function to determine if street name is within expected street values
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

#function to determine if postcode is not normal 5 digit code
def audit_postal_code(invalid_postal_codes, postal_code):
    if len(postal_code) != 5:
        invalid_postal_codes[postal_code] += 1

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
    
def is_postal_code(elem):
    """ returns if postcode like """
    return 'post' in elem.attrib['k']

#function to iterate through file and find incorrect values for street and postcodes
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    invalid_postal_codes = defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        #iteration through nodes or ways for both streets and postcodes
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postal_code(tag):
                    audit_postal_code(invalid_postal_codes, tag.attrib['v'])

    return street_types, invalid_postal_codes
    
#function to run everything
def test():
    st_types, invalid_postal_codes = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    pprint.pprint(dict(invalid_postal_codes))

"""
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
"""

if __name__ == '__main__':
    test()