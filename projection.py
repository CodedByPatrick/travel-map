
import math

DEG_TO_RAD = math.pi / 180.0

class ProjectionBase():

    def __init__(self):
        pass

    def get_class_name(self):
        return type(self).__name__

    def deg_to_rad(self, coord):
        """Convert a coordinate tuple from degrees to radians.
        """
        return (coord[0] * DEG_TO_RAD, coord[1] * DEG_TO_RAD)

    def project(self, coord_list):
        """Transform the points according to the projection.
        coord_list is list of x,y tuples in degrees.
        """
        
        for coord in coord_list:
            rad_tuple = self.deg_to_rad(coord)
            map_coord = self.project_rad_tuple(rad_tuple)
            
        pass

    def project_rad_tuple(self, rad_tuple):
        """Transform a single coordinate tuple
        """

    def has_inverse(self):
        return False

    def invert(self):
        pass

