#!/usr/bin/env python3
#

import sys
import mapshapes

if __name__ == "__main__":
    print("Running as __main__ with args:", sys.argv)

    wc = mapshapes.WorldCoarse()
    wc.plot()

