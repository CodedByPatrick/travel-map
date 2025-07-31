
import shapefile
import copy

class ShpReader(shapefile.Reader):

    def __init__(self, sf_name = None):
        super().__init__(sf_name)
        self.file_name = sf_name

    def get_class_name(self):
        return type(self).__name__

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
                    yield shrec


