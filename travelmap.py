import sys
import shpreader
import mapimage
import pprint


class AnyMap():

    def __init__(self,
                 shfile
                 ):
        self.shape_file = shfile
        self.sfr = shpreader.ShpReader(self.shape_file)
        self.mimg = mapimage.SvgImage()


    def draw(self):
        """Draw the map
        """
        for shrec in self.sfr.iterShapeRecParts():
            #pprint.pprint(vars(shrec.record))
            #pprint.pprint(vars(shrec.shape))
            self.mimg.add_polyline(shrec.shape.points)


    def print(self):
        self.mimg.print()


class WorldSmall(AnyMap):

    def __init__(self):
        shfile = "../shape_files/ne_110m_coastline.zip"
        super().__init__(shfile)


class WorldMedium(AnyMap):

    def __init__(self):
        shfile = "../shape_files/ne_50m_coastline.zip"
        super().__init__(shfile)


class WorldLarge(AnyMap):

    def __init__(self):
        shfile = "../shape_files/ne_10m_coastline.zip"
        super().__init__(shfile)

    
if __name__ == "__main__":
    #print("Running as __main__ with args:", sys.argv)

    wm = WorldMedium();
    wm.draw()
    wm.print()
