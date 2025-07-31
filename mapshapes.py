
import shapefile

class ShapesBase():

    def __init__(self, shfile = None):
        self.shape_file = shfile
        self.sf = shapefile.Reader(self.shape_file)

    def get_class_name(self):
        return type(self).__name__

    def _use_shape(self, shrec, shape_index):
        """Indicate if this shape should be used in the map.
        """
        return True


    def draw_map(self, map_image):
        """Draw a map using this shapefile

        Draw a map image using the specified projection.
        """
        shape_index = 0
        for shrec in self.sf.iterShapeRecords():
            if (self._use_shape(shrec, shape_index) == False):
                continue
            if (len(shrec.shape.parts) == 1):
                map_image.add_polyline(shrec.shape.points)
            else:
                # Loop through the shape parts.
                # shrec.shape.parts holds the start index
                # of each part.  Create a begin and end
                # index list and loop through the values.
                #
                begin_list = shrec.shape.parts
                end_list = begin_list[1:len(begin_list)]
                end_list.append(len(shrec.shape.points))
                for i in range(len(begin_list)):
                    bidx = begin_list[i]
                    eidx = end_list[i]
                    part_pts = shrec.shape.points[bidx:eidx]
                    map_image.add_polyline(part_pts)
            #
            shape_index += 1


class WorldSmall(ShapesBase):

    def __init__(self):
        shfile = "../shape_files/ne_110m_coastline.zip"
        super().__init__(shfile)


class WorldMedium(ShapesBase):

    def __init__(self):
        shfile = "../shape_files/ne_50m_coastline.zip"
        super().__init__(shfile)


class WorldLarge(ShapesBase):

    def __init__(self):
        shfile = "../shape_files/ne_10m_coastline.zip"
        super().__init__(shfile)

