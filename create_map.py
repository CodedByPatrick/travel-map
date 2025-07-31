#!/usr/bin/env python3
#

import sys
import shpreader
import mapimage
import pprint

if __name__ == "__main__":
    #print("Running as __main__ with args:", sys.argv)

    mi = mapimage.SvgImage()
    #ws = shpreader.WorldSmall()
    ws = shpreader.WorldMedium()
    #ws = shpreader.WorldLarge()
    for shrec in ws.iterShapeRecParts():
        #pprint.pprint(vars(shrec.record))
        #pprint.pprint(vars(shrec.shape))
        mi.add_polyline(shrec.shape.points)

    mi.print()
