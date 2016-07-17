#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.
    f_data = open(filename, 'r')

    file_count = 0

    f_name = "{0}-{1}".format(PATENTS, file_count)
    f_open = open(f_name, 'w')

    # Write first line of XML file.
    f_open.write('<?xml version="1.0" encoding="UTF-8"?>')
    is_first_line = True

    # For each line in root:
    for line in f_data:
        if is_first_line:
            is_first_line = False
            continue

        if line[:5] == '<?xml':
            f_open.close()
            file_count += 1
            f_name = "{0}-{1}".format(PATENTS, file_count)
            f_open = open(f_name, 'w')
    
        f_open.write(line)

    f_open.close()
    pass


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()