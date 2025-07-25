#!/usr/bin/env python3
#

import sys
import mapshapes
import mapimage


if __name__ == "__main__":
    #print("Running as __main__ with args:", sys.argv)

    mi = mapimage.SvgImage()
    wc = mapshapes.WorldCoarse()
    wc.plot(mi)
    mi.print()


