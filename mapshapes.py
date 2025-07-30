
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

            first_tuple = shrec.shape.points[0]
            if (first_tuple[0] < 0 or first_tuple[1] < 0):
                continue

            '''
            prev_x = shrec.shape.points[0][0]
            for tup in shrec.shape.points:
                if (abs(tup[0] - prev_x) > 90):
                    print("found at ", rec_count)
                    prev_x = tup[0]
            '''
            if (rec_count != 1388):
                continue
            #if (rec_count < 1387 or rec_count > 1389):
            #    continue
            #print(shrec.record.as_dict(), shrec.shape)
            map_image.add_polyline(shrec.shape.points[0:390])
            map_image.add_polyline(shrec.shape.points[392:10600])
            if (False and rec_count == 5):
                break;


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

