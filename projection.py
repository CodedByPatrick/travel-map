
import math

DEG_TO_RAD = math.pi / 180.0


class ProjectionBase():

    def __init__(self):
        pass

    def get_class_name(self):
        return type(self).__name__

    def deg_to_rad(self, coord):
        """Convert a coordinate tuple from degrees to radians.
        Returns the converted tuple in radians.
        """
        return (coord[0] * DEG_TO_RAD, coord[1] * DEG_TO_RAD)

    def project_points(self, points):
        """Transform a list of geographic coordinate system tuples.
        points is a list of coordinate tuples in degrees.
        Returns a list of cartesian coordinates tuples in the
        selected map projection.
        """
        pcs_points = []
        for gcs_pt in points:
            rad_pt = self.deg_to_rad(gcs_pt)
            pcs_pt = self.project(rad_pt)
            pcs_points.append(pcs_pt)
        return pcs_points

    def project(self, gcs_coord):
        """Transform an x,y tuple according to the projection.
        Convert from Geographic Coordinate System (GCS) to a
        Projected Coordinate System (PCS)
        gcs_coord is a coordinate tuple in radians.
        Returns a cartesian coordinate tuple in the map projection.
        """
        return gcs_coord

    def has_inverse(self):
        return False

    def invert(self):
        pass


class Resize(ProjectionBase):

    def __init__(self, cx, cy = None):
        self.cx = cx
        if (cy == None):
            self.cy = cx
        else:
            self.cy = cy

    def project(self, gcs_coord):
        """Resize the coordinate.
        """
        return (gcs_coord[0] * self.cx,
                gcs_coord[1] * self.cy)


class Rotate(ProjectionBase):

    def __init__(self, rad_angle):
        self.angle = rad_angle
        self.cos_a = math.cos(rad_angle)
        self.sin_a = math.sin(rad_angle)

    def project(self, gcs_coord):
        """Rotate the coordinate.
        """
        x, y = gcs_coord
        xp =  x * self.cos_a - y * self.sin_a
        yp =  x * self.sin_a + y * self.cos_a
        return (xp, yp)


class Translate(ProjectionBase):

    def __init__(self, cx, cy = None):
        self.cx = cx
        if (cy == None):
            self.cy = cx
        else:
            self.cy = cy

    def project(self, gcs_coord):
        """Translate the coordinate.
        """
        return (gcs_coord[0] + self.cx,
                gcs_coord[1] + self.cy)


