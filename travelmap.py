import sys
import shpreader
import projection
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

    def shape_in_bounding_box(self, shrec, bound):
        """Determine if the bounding box of a shape lies
        entirely inside the provided bounding box.
        Bounding box is [min_x, min_y, max_x, max_y].
        Returns True or False
        """
        if (shrec.shape.bbox[0] >= bound[0] and
            shrec.shape.bbox[1] >= bound[1] and
            shrec.shape.bbox[2] <= bound[2] and
            shrec.shape.bbox[3] <= bound[3]):
            return True
        else:
            return False
        
    def shape_includes_naukan(self, shrec):
        """Specify if the shape includes Naukan in eastern Russia.
        Bounding box is [min_x, min_y, max_x, max_y].
        """
        bound = [-180.1, +64.0, -169.6, 89.0]
        return self.shape_in_bounding_box(shrec, bound)

    def shape_includes_antarctica(self, shrec):
        """Specify if the shape includes Antarctica.
        """
        bound = [ -180.1, -90.0, +180.1, -60.0]
        return self.shape_in_bounding_box(shrec, bound)

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

    def draw(self, proj, mimg):
        """Draw the map
        """
        for shrec in self.sfr.iterShapeRecParts():
            if (self.use_shape(shrec) == False):
                continue
            self.transform_shape(shrec)
            #pprint.pprint(vars(shrec.record))
            #pprint.pprint(vars(shrec.shape))
            pcs_points = proj.project_points(shrec.shape.points)
            mimg.add_polyline(pcs_points)

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

    #proj = projection.Rect(1)
    #proj = projection.Albers(50, 20, 0, 0)
    #proj = projection.EckertIV()
    #proj = projection.GallPeters()
    #proj = projection.Mollweide()
    #proj = projection.NaturalEarth2()
    #proj = projection.NaturalEarth()
    #proj = projection.Patterson()
    #proj = projection.Robinson()
    proj = projection.VanDerGrinten()
    mimg = mapimage.SvgImage()
    
    wm = WorldMedium();
    wm.draw(proj, mimg)
    mimg.print()
