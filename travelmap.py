import sys
import shpreader
import mapimage
import pprint
import math

DEG_TO_RAD = math.pi / 180.0
AREA_SPHERE = 4.0 * math.pi * 1 * 1


class AnyMap():

    def __init__(self, shfile):
        self.shape_file = shfile
        self.sfr = shpreader.ShpReader(self.shape_file)

    def get_class_name(self):
        return type(self).__name__

    def bbox_area_estimate(self, shrec):
        """Estimate the area of the bounding box.
        Works well for small areas.
        Return as a percent of the whole earth.
        
        With coordinates in radians, at the equator, the area of a small
        bounding box is approximately dx * dy since sin(dx) ~= dx.  As
        the box moves towards the poles, the width (difference between
        longitude values) decreases with the cosine of the latitude, so
        that must be added to the equation.  Finally, the area of a
        sphere is 4*pi*r^2.
        """
        # shapefile returns all data in degrees
        #
        dx = (shrec.shape.bbox[2] - shrec.shape.bbox[0]) * DEG_TO_RAD
        dy = (shrec.shape.bbox[3] - shrec.shape.bbox[1]) * DEG_TO_RAD
        # Select one value for the latitude.
        lat_adj = math.cos(shrec.shape.bbox[1] * DEG_TO_RAD)
        # Area estimate
        area = dx * dy * lat_adj
        # Percent
        percent = area / AREA_SPHERE
        return percent
        
    def shape_includes_naukan(self, shrec):
        """Specify if the shape includes Naukan in eastern Russia.
        Bounding box is [min_x, min_y, max_x, max_y].
        """
        min_lat = +64.0
        max_lon = -169.6
        if (shrec.shape.bbox[1] > min_lat and
            shrec.shape.bbox[2] < max_lon):
            return True
        else:
            return False

    def shape_includes_antarctica(self, shrec):
        """Specify if the shape includes Antarctica.
        """
        max_lat = -60.0
        if (shrec.shape.bbox[3] < max_lat):
            return True
        else:
            return False

    def move_naukan(self, shrec):
        """Move Naukan to the other side of the world.
        """
        lon_incr = 360.0
        new_points = []
        for coord in shrec.shape.points:
            new_coord = (coord[0] + lon_incr, coord[1])
            new_points.append(new_coord)
        shrec.shape.points = new_points

    def use_shape(self, shrec):
        """Specify if this shape should be used in the map.
        """
        return True

    def transform_shape(self, shrec):
        """Transform a shape before using in a map.
        """
        pass

    def draw(self, mimg):
        """Draw the map
        """
        for shrec in self.sfr.iterShapeRecParts():
            if (self.use_shape(shrec) == False):
                continue
            self.transform_shape(shrec)
            #pprint.pprint(vars(shrec.record))
            #pprint.pprint(vars(shrec.shape))
            mimg.add_polyline(shrec.shape.points)

    def print(self):
        self.mimg.print()


class StdWorld(AnyMap):

    def __init__(self, shfile):
        super().__init__(shfile)
        self.area_threshold = 3.0E-6

    def use_shape(self, shrec):
        """
        if (shrec.shape.bbox[3] < 0):
            return False
        if (shrec.shape.bbox[0] > -160):
            return False
        if (self.shape_includes_antarctica(shrec)):
            return False
        """
        area = self.bbox_area_estimate(shrec)
        if (area < self.area_threshold):
            return False
        return True

    def transform_shape(self, shrec):
        """Transform a shape before using in a map.
        """
        if (self.shape_includes_naukan(shrec)):
            self.move_naukan(shrec)


class WorldSmall(StdWorld):

    def __init__(self):
        shfile = "../shape_files/ne_110m_coastline.zip"
        super().__init__(shfile)


class WorldMedium(StdWorld):

    def __init__(self):
        shfile = "../shape_files/ne_50m_coastline.zip"
        super().__init__(shfile)


class WorldLarge(StdWorld):

    def __init__(self):
        shfile = "../shape_files/ne_10m_coastline.zip"
        super().__init__(shfile)

    
if __name__ == "__main__":
    #print("Running as __main__ with args:", sys.argv)

    mimg = mapimage.SvgImage()
    
    wm = WorldMedium();
    wm.draw(mimg)
    mimg.print()
