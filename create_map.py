#!/usr/bin/env python3
#

import sys
import mapshapes
import mapimage


if __name__ == "__main__":
    #print("Running as __main__ with args:", sys.argv)

    mi = mapimage.SvgImage()
    #ws = mapshapes.WorldSmall()
    ws = mapshapes.WorldMedium()
    #ws = mapshapes.WorldLarge()
    ws.plot(mi)
    mi.print()


