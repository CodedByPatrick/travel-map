
import shapefile

class ShapesBase():

    def __init__(self, shfile = None):
        self.shape_file = shfile
        self.sf = shapefile.Reader(self.shape_file)

    def get_class_name(self):
        return type(self).__name__

    def plot(self, map_image):
        rec_count = 0
        for shrec in self.sf.iterShapeRecords():
            rec_count += 1
            #print(shrec.record.as_dict(), shrec.shape)
            map_image.add_polyline(shrec.shape.points)
            #if (rec_count == 5):
            #break;


class WorldCoarse(ShapesBase):

    def __init__(self):
        shfile = "../shape_files/ne_110m_coastline.zip"
        super().__init__(shfile)

