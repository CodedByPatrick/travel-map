
import shapefile
import copy

class ShpReader(shapefile.Reader):

    def __init__(self, sf_name = None):
        super().__init__(sf_name)
        self.file_name = sf_name

    def get_class_name(self):
        return type(self).__name__

    def calc_part_bbox(self, part_pts):
        """Calculate the bounding box for the shape part.
        Loop through the set of points and pick the largest
        and smallest.
        """
        x_lo =  180.0
        y_lo =   90.0
        x_hi = -180.0
        y_hi =  -90.0
        for coord in part_pts:
            # x
            if (coord[0] < x_lo):
                x_lo = coord[0]
            elif (coord[0] > x_hi):
                x_hi = coord[0]
            # y
            if (coord[1] < y_lo):
                y_lo = coord[1]
            elif (coord[1] > y_hi):
                y_hi = coord[1]
        #
        return [x_lo, y_lo, x_hi, y_hi]
        
    def iterShapeRecParts(self, fields=None, bbox=None):
        """Return shapefile ShapeRecord one part at a time.
        """
        for shrec in self.iterShapeRecords(fields, bbox):
            if (len(shrec.shape.parts) == 1):
                # If there is only one part, return it.
                #
                yield shrec
            else:
                # Loop through multiple shape parts.
                # shrec.shape.parts holds the start index of each part.
                # Create a begin and end index list and loop through
                # the values.
                #
                begin_list = shrec.shape.parts
                end_list = begin_list[1:len(begin_list)]
                end_list.append(len(shrec.shape.points))
                #
                # Make a copy of the original points so we can
                # overwrite the values in shrec.
                #
                orig_pts = copy.deepcopy(shrec.shape.points)
                #
                for i in range(len(begin_list)):
                    bidx = begin_list[i]
                    eidx = end_list[i]
                    part_pts = orig_pts[bidx:eidx]
                    shrec.shape.points = part_pts
                    shrec.shape.parts = [0]
                    shrec.shape.bbox = self.calc_part_bbox(part_pts)
                    yield shrec


