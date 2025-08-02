
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
        # Not verified since port, so return False.
        return False

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
        # Not verified since port.
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord
        theta = math.asin(y / self.cy)
        yp = math.asin((theta
                        + math.sin(theta) * math.cos(theta)
                        + 2.0 * math.sin(theta)) /
                       (2.0 + PI_DIV_TWO))
        xp = x / self.cx / (1 + math.cos(theta))
        return (xp, yp)


class GallPeters(ProjectionBase):

    def __init__(self):
        pass

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        https://en.wikipedia.org/wiki/Gall%E2%80%93Peters_projection
        Project with R = 1
        """
        x, y = gcs_coord
        xp = x
        yp = 2.0 * math.sin(y)
        return (xp, yp)

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord
        xp = x
        yp = math.asin(y/ 2.0)
        return (xp, yp)


class Mollweide(ProjectionBase):

    def __init__(self):
        self.EPS = 1.0E-11

    def __solve_theta(self, phi):
        pi_sin_phi = math.pi * math.sin(phi)
        theta = phi
        for loop in range(1000):
            two_t = 2.0 * theta
            num = two_t + math.sin(two_t) - pi_sin_phi
            den = 2 + 2.0 * math.cos(two_t)
            if (den == 0.0):
                break
            diff = num / den
            theta -= diff
            if (abs(diff) < self.EPS):
                break
        #
        return theta

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        """
        x, y = gcs_coord
        theta = self.__solve_theta(y)
        xp = TWO_DIV_PI * x * math.cos(theta)
        yp = math.sin(theta)
        return (xp, yp)

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord
        return (xp, yp)


class NaturalEarth2(ProjectionBase):

    def __init__(self):
        self.A0 =  0.84719
        self.A1 = -0.13063
        self.A2 = -0.04515
        self.A3 =  0.05494
        self.A4 = -0.02326
        self.A5 =  0.00331
        self.B0 =  1.01183
        self.B1 = -0.02625
        self.B2 =  0.01926
        self.B3 = -0.00396

        self.C0 = self.B0
        self.C1 = 9 * self.B1
        self.C2 = 11 * self.B2
        self.C3 = 13 * self.B3
        self.EPS = 1e-11
        self.MAX_Y = 0.84719 * 0.5351175 * math.pi

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        """
        x, y = gcs_coord
        phi2 = y * y
        phi4 = phi2 * phi2
        phi6 = phi4 * phi2
        xp = x * (self.A0 + self.A1 * phi2 + phi6 * phi6 * (self.A2 + self.A3 * phi2 + self.A4 * phi4 + self.A5 * phi6))
        yp = y * (self.B0 + phi4 * phi4 * (self.B1 + self.B2 * phi2 + self.B3 * phi4))
        return (xp, yp)

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord
        # Make sure y is inside valid range
        if (y > self.MAX_Y):
            y = self.MAX_Y
        elif (y < -self.MAX_Y):
            y = -self.MAX_Y

        # Latitude
        yc = y
        for loop in range(1000):
            # Newton-Raphson
            y2 = yc * yc
            y4 = y2 * y2
            f = (yc * (self.B0 + y4 * y4 * (self.B1 + self.B2 * y2 + self.B3 * y4))) - y
            fder = self.C0 + y4 * y4 * (self.C1 + self.C2 * y2 + self.C3 * y4)
            tol = f / fder
            yc -= tol
            if (abs(tol) < self.EPS):
                break;
        #
        yp = yc

        # Longitude
        y2 = yc * yc
        y4 = y2 * y2
        y6 = y4 * y2
        phi = self.A0 + self.A1 * y2 + y6 * y6 * (self.A2 + self.A3 * y2 + self.A4 * y4 + self.A5 * y6)
        xp = x / phi

        return (xp, yp)


class NaturalEarth(ProjectionBase):

    def __init__(self):
        self.A0 =  0.8707
        self.A1 = -0.131979
        self.A2 = -0.013791
        self.A3 =  0.003971
        self.A4 = -0.001529
        self.B0 =  1.007226
        self.B1 =  0.015085
        self.B2 = -0.044475
        self.B3 =  0.028874
        self.B4 = -0.005916

        self.C0 = self.B0
        self.C1 = (3 * self.B1)
        self.C2 = (7 * self.B2)
        self.C3 = (9 * self.B3)
        self.C4 = (11 * self.B4)
        self.EPS = 1e-11
        self.MAX_Y = (0.8707 * 0.52 * math.pi)

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        """
        x, y = gcs_coord
        phi2 = y * y
        phi4 = phi2 * phi2

        xp = x * (self.A0 + phi2 * (self.A1 + phi2 * (self.A2 + phi4 * phi2 * (self.A3 + phi2 * self.A4))))
        yp = y * (self.B0 + phi2 * (self.B1 + phi4 * (self.B2 + self.B3 * phi2 + self.B4 * phi4)))

        return (xp, yp)

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord

        # Make sure y is inside valid range.
        if (y > self.MAX_Y):
            y = self.MAX_Y
        elif (y < -self.MAX_Y):
            y = -self.MAX_Y

        # Latitude
        yc = y
        for loop in range(1000):
            # Newton-Raphson
            y2 = yc * yc
            y4 = y2 * y2
            f = (yc * (self.B0 + y2 * (self.B1 + y4 * (self.B2 + self.B3 * y2 + self.B4 * y4)))) - y
            fder = self.C0 + y2 * (self.C1 + y4 * (self.C2 + self.C3 * y2 + self.C4 * y4))
            tol = f / fder
            yc -= tol
            if (abs(tol) < self.EPS):
                break;
        #
        yp = yc

        # Longitude
        y2 = yc * yc
        xp = x / (self.A0 + y2 * (self.A1 + y2 * (self.A2 + y2 * y2 * y2 * (self.A3 + y2 * self.A4))))
        return (xp, yp)


class Patterson(ProjectionBase):

    def __init__(self):
        self.C1 =  1.0148
        self.C2 =  0.23185
        self.C3 = -0.14499
        self.C4 =  0.02406

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        """
        x, y = gcs_coord
        phi = y
        phi2 = phi * phi
        xp = x
        yp = phi * (self.C1 + phi2 * phi2 * (self.C2 + phi2 * (self.C3 + phi2 * self.C4)))
        return (xp, yp)

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord
        return (xp, yp)


class Robinson(ProjectionBase):

    def __init__(self):
        self.A0 =  0.8507
        self.A1 =  0.9642
        self.A2 = -0.1450
        self.A3 = -0.0013
        self.A4 = -0.0104
        self.A5 = -0.0129

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        """
        x, y = gcs_coord
        phi2 = y * y
        xp = x * (self.A0 + phi2 * (self.A2 + phi2 * self.A4))
        yp = y * (self.A1 + phi2 * (self.A3 + phi2 * self.A5))
        return (xp, yp)

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord
        return (xp, yp)


class VanDerGrinten(ProjectionBase):

    def __init__(self):
        self.EPS = 1E-11

    def project(self, gcs_coord):
        """
        gcs_coord is a coordinate tuple in RADIANS.
        """
        x, y = gcs_coord

        lam = x
        phi = y

        if (phi == 0.0):
            return gcs_coord

        theta = math.asin(abs(2.0 * phi / math.pi))
        if ((lam == 0.0) or (abs(PI_DIV_TWO - abs(phi)) < self.EPS)):
            xp = 0
            yp = math.pi * tan(theta / 2)
            if (phi < 0.0):
                yp = -yp
            return (xp, yp)

        A = 0.5 * abs(math.pi / lam - lam / math.pi)
        G = math.cos(theta) / (math.sin(theta) + math.cos(theta) - 1)
        P = G * (2.0 / math.sin(theta) - 1)
        Q = A * A + G

        A2 = A * A
        G2 = G * G
        P2 = P * P
        Q2 = Q * Q
        P2A2 = P2 + A2

        GmP2 = G - P2
        t1 = A * GmP2
        t2 = A2 * GmP2 * GmP2
        t3 = P2A2 * (G2 - P2)

        xp = math.pi * (t1 + math.sqrt(t2 - t3)) / P2A2
        if (lam < 0.0):
            xp = -xp

        t1 = P * Q
        t2 = (A2 + 1) * P2A2

        yp = math.pi * abs(t1 - A * math.sqrt(t2 - Q2)) / P2A2
        if (phi < 0.0):
            yp = -yp

        return (xp, yp)

    def has_inverse(self):
        return False

    def invert(self, pcs_coord):
        x, y = pcs_coord

        x = x / math.pi
        y = y / math.pi

        if (x == 0.0 and y == 0.0):
            return (x, y)

        x2 = x * x
        y2 = y * y
        x2py2 = x2 + y2
        x2my2 = x2 - y2

        c1 = - abs(y) * (1 + x2 + y2)
        c2 = c1 - 2.0 * y2 + x2
        c3 = -2.0 * c1 + 1 + 2.0 * y2 + x2py2 * x2py2
        c2_2 = c2 * c2
        c2_3 = c2_2 * c2
        c3_2 = c3 * c3
        c3_3 = c3_2 * c3

        t1 = 2 * c2_3 / c3_3
        t2 = 9 * c1 * c2 / c3_2
        d = y2 / c3 + (1/27)*(t1 - t2)
        a1 = (1/c3) * (c1 - c2_2 / (3 * c3))
        m1 = 2 * math.sqrt((-1/3) * a1)
        theta = (1/3) * math.acos(3 * d / (a1 * m1))

        phi = math.pi * (-m1 * math.cos(theta + (1/3)*math.pi) - (c2 / (3 * c3)))
        if (y < 0.0):
            phi = -phi

        t1 = 1 + 2 * x2my2 + x2py2 * x2py2
        if (x == 0.0):
            lam = 0.0
        else:
            lam = math.pi * (x2py2 - 1 + math.sqrt(t1)) / (2 * x)

        xp = lam
        yp = phi

        return (xp, yp)
