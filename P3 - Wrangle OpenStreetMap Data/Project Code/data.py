# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:49:25 2016

@author: carvusbyrdiv
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


OSMFILE = '/data/raleigh_north-carolina.osm'
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
postcode_letter_re = re.compile('[a-zA-Z]')

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
            
#function to update the street name using the mapping above
def update_name(name, mapping):
    for key in mapping.keys():
        if name.find(key) != -1:
            name = name[:name.find(key)]+mapping[key]
    return name

#function to update zipcodes based on length logic
def update_code(postal_code):
    #turn postcode into a list split among dash
    split_code = re.split('-',postal_code)
    if len(split_code) > 1:
        #if code is a list, does it have any letters in?
        m = postcode_letter_re.search(split_code[0])
        if m:
            #if the first element has letters, code equals first 5 characters of 2nd element            
            postal_code = split_code[1]
        if len(split_code[-1]) < 5:
            if len(split_code) > 2:
                #if postcode has both prefix letters and dash extension                
                postal_code = split_code[1]
            elif len(split_code) < 3:
                #if it just has an dash extension                
                postal_code = split_code[0]
    else:
        if postcode_letter_re.search(split_code[0]):
            #if anything else, return none            
            postal_code = None    
    return postal_code

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#function to grab nodes and ways and create data for JSON
def shape_element(element):
    node = {}
    node["created"]={}
    node["address"]={}
    node["pos"]=[]
    refs=[]

    if element.tag == "node" or element.tag == "way" :
        if "id" in element.attrib:
            node["id"]=element.attrib["id"]
        node["type"]=element.tag

        if "visible" in element.attrib.keys():
            node["visible"]=element.attrib["visible"]

        for elem in CREATED:
            if elem in element.attrib:
                node["created"][elem]=element.attrib[elem]
        if "lat" in element.attrib:
            node["pos"].append(float(element.attrib["lat"]))
        if "lon" in element.attrib:
            node["pos"].append(float(element.attrib["lon"]))

        for tag in element.iter("tag"):
            if not(problemchars.search(tag.attrib['k'])):
                if tag.attrib['k'] == "addr:housenumber":
                    node["address"]["housenumber"]=tag.attrib['v']
                # updates postcodes                 
                if tag.attrib['k'] == "addr:postcode":
                    node["address"]["postcode"]=tag.attrib['v']                                       
                    node["address"]["postcode"]=update_code(node["address"]["postcode"])
                # updates street address                 
                if tag.attrib['k'] == "addr:street":
                    node["address"]["street"]=tag.attrib['v']          
                    node["address"]["street"]=update_name(node["address"]["street"], mapping)
                if tag.attrib['k'].find("addr")==-1:
                    node[tag.attrib['k']]=tag.attrib['v']
        for nd in element.iter("nd"):
             refs.append(nd.attrib["ref"])
        if node["address"] =={}:
            node.pop("address", None)
        if refs != []:
           node["node_refs"]=refs
        return node
    else:
        return None

# creates JSON file
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map(OSMFILE, False)
    pprint.pprint(data)
    

if __name__ == "__main__":
    test()