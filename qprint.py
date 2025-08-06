#!/usr/bin/env python3
#

import argparse
import shapefile
from pprint import pprint


def print_obj_dir(obj):
    for name in dir(obj):
        if not name.startswith('_'):
            print("   ", name)

#
# shfile = "../shape_files/ne_50m_admin_0_countries_lakes.zip"
# sf = shapefile.Reader(shfile)
#

def shapefile_info(sf):
    print("type(sf):", type(sf))
    pprint(vars(sf))


def shapeRec_info(sf, index = 0):
    sr = sf.shapeRecord(index)
    print("shapeRec:")
    pprint(vars(sr))
    print("shapeRec.record:")
    pprint(vars(sr.record))
    print("shapeRec.shape:")
    pprint(vars(sr.shape))
    print_obj_dir(sr.shape)




if __name__ == "__main__":
    #
    shfile = "../shape_files/ne_50m_coastline.zip"
    #print_shapefile_info(shfile)
    print_shapeRec_info(shfile)
