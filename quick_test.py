#!/usr/bin/env python3
#

import argparse
import shapefile
from pprint import pprint


def print_obj_dir(obj):
    for name in dir(obj):
        if not name.startswith('_'):
            print("   ", name)


def print_shapefile_info(shfile):
    sf = shapefile.Reader(shfile)
    print("type(sf):", type(sf))
    pprint(vars(sf))


def print_shapeRec_info(shfile, index = 0):
    sf = shapefile.Reader(shfile)
    shapeRec = sf.shapeRecord(index)
    print("shapeRec:")
    pprint(vars(shapeRec))
    print("shapeRec.record:")
    pprint(vars(shapeRec.record))
    print("shapeRec.shape:")
    pprint(vars(shapeRec.shape))
    print_obj_dir(shapeRec.shape)


if __name__ == "__main__":
    #
    shfile = "../shape_files/ne_50m_coastline.zip"
    #print_shapefile_info(shfile)
    print_shapeRec_info(shfile)
