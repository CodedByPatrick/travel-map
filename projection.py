
import math

DEG_TO_RAD = math.pi / 180.0
TWO_DIV_PI = 2.0 / math.pi
PI_DIV_TWO = math.pi / 2.0


class ProjectionBase():

    def __init__(self):
        pass

    def get_class_name(self):
        return type(self).__name__

    def deg_to_rad(self, value):
        """Convert a value from degrees to radians.
        Returns the converted value in radian value.
        """
        return value * DEG_TO_RAD

    def coord_to_rad(self, coord):
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
            rad_pt = self.coord_to_rad(gcs_pt)
            pcs_pt = self.project(rad_pt)
            pcs_points.append(pcs_pt)
        return pcs_points

    def project(self, gcs_coord):
        """Transform an x,y tuple according to the projection.
        Convert from Geographic Coordinate System (GCS) to a
        Projected Coordinate System (PCS)
        gcs_coord is a coordinate tuple in RADIANS.
        Returns a cartesian coordinate tuple in the map projection.
        """
        return gcs_coord

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
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

    def __init__(self, angle):
        """Rotation angle in DEGREES
        """
        self.angle = self.deg_to_rad(angle)
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


class Rect(Resize):

    def __init__(self, cx = 1, cy = None):
        super().__init__(cx, cy)


# Albers Projection
#
# Defaults for
# World: [20, 50, 0, 0]
# Alaska 55 & 65
# Hawaii 8 & 18
# Rule of thumb - 1/6th from each end of central meridian.
#
# US? [45.5, 29.5, -96, 37.5]
#
class Albers(ProjectionBase):

    def __init__(self,
                 std_phi1, std_phi2,
                 ref_lam, ref_phi):

        # std_phi1 - standard parallel
        # std_phi2 - standard parallel
        # ref_lam  - reference longitue
        # ref_phi  - reference latitude
        #
        self.std_phi1 = self.deg_to_rad(std_phi1)
        self.std_phi2 = self.deg_to_rad(std_phi2)
        self.ref_lam  = self.deg_to_rad(ref_lam)
        self.ref_phi  = self.deg_to_rad(ref_phi)

        self.n = 0.5 * (  math.sin(self.std_phi1)
                        + math.sin(self.std_phi2))
        self.n2 = 2.0 * self.n
        self.nin = 1.0 / self.n

        cos_phi1 = math.cos(self.std_phi1)
        self.C = cos_phi1 * cos_phi1 + self.n2 * math.sin(self.std_phi1)

        temp_sqrt = math.sqrt(self.C - self.n2 * math.sin(self.ref_phi))
        self.rho0 = self.nin * temp_sqrt

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        """
        x, y = gcs_coord
        theta = self.n * (x - self.ref_lam)
        temp_sqrt = math.sqrt(self.C - self.n2 * math.sin(y))
        rho = self.nin * temp_sqrt
        xp = rho * math.sin(theta)
        yp = self.rho0 - rho * math.cos(theta)
        return (xp, yp)

    def has_inverse(self):
        return True

    def invert(self, pcs_coord):
        x, y = pcs_coord
        theta = math.atan2(x, self.rho0 - y)
        lambdav = self.nin * theta + self.ref_lam

        rho = (self.rho0 - y) / math.cos(theta)
        rn2 = rho * self.n
        rn2 = rn2 * rn2
        phi = math.asin((self.C - rn2) / self.n2)

        xp = lambdav
        yp = phi
        return (xp, yp)


class EckertIV(ProjectionBase):

    def __init__(self):
        self.cx = 2.0 / math.sqrt(4 * math.pi + math.pi * math.pi)
        self.cy = 2.0 * math.sqrt(math.pi / (4 + math.pi))
        self.EPS = 1.0E-11

    def __solve_theta(self, phi):
        theta = phi
        for loop in range(1000):
            num = (theta + math.sin(theta) * math.cos(theta)
                   + 2.0 * math.sin(theta)
                   - (2.0 + PI_DIV_TWO) * math.sin(phi))
            den = 2.0 * math.cos(theta) + math.cos(2.0 * theta) + 1
            diff = num / den
            #print "theta num den diff \n"
            theta = theta - diff
            if (abs(diff) < self.EPS):
                break;
        #
        return theta

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        https://en.wikipedia.org/wiki/Eckert_IV_projection
        Project with R = 1
        Scaling will occur later.
        """
        x, y = gcs_coord
        theta = self.__solve_theta(y)
        xp = self.cx * x * (1 + math.cos(theta))
        yp = self.cy * math.sin(theta)
        return (xp, yp)

    def has_inverse(self):
        return True

    def invert(self, pcs_coord):
        x, y = pcs_coord
        theta = math.asin(y / self.cy)
        yp = math.asin((theta
                        + math.sin(theta) * math.cos(theta)
                        + 2.0 * math.sin(theta)) /
                       (2.0 + PI_DIV_TWO))
        xp = x / self.cx / (1 + math.cos(theta))
        return (xp, yp)

'''    
class Projname(ProjectionBase):

    def __init__(self):
        pass

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        """
        x, y = gcs_coord
        return (xp, yp)

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord
        return (xp, yp)
'''
