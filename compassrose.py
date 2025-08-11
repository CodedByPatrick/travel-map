
import svg
import math


class CompassRose():

    def __init__(self):
        self.svg = svg.SVG()
        self.svg.width = 500
        self.svg.height = 500
        self.svg.viewBox = svg.ViewBoxSpec(-2, -2, 4, 4)
        self.svg.elements = []

        self.top_group = svg.G()
        self.top_group.stroke = "black"
        self.top_group.elements = []
        self.svg.elements.append(self.top_group)
        
    def draw_circle(self, radius, width):
        cir = svg.Circle()
        cir.cx = 0
        cir.cy = 0
        cir.r = radius
        cir.stroke_width = width
        cir.fill = "transparent"
        self.top_group.elements.append(cir)
        
    def draw_principal_points(self,
                              id_str,
                              point_length,
                              base_size,
                              half_fill,
                              angle):
        """
        size - length of point
        base - radius of base circle
        angle - angle in degrees of points
        """
        group = svg.G()
        group.id = id_str + "_group"
        group.stroke = "black"
        group.stroke_width = "0.1%"
        group.transform = "rotate(" + str(angle) + ")"
        group.elements = []
        self.top_group.elements.append(group)

        base_x = base_size * math.cos(math.pi / 4)
        base_y = base_size * math.sin(math.pi / 4)

        onept = svg.G()
        onept.id = id_str
        onept.elements = []
        group.elements.append(onept)

        # Draw one point
        values = [0, 0, -base_x, base_y, 0, point_length]
        pline = svg.Polygon(points = values)
        onept.elements.append(pline)
        values = [0, 0, base_x, base_y, 0, point_length]
        pline = svg.Polygon(points = values)
        if (half_fill == False):
            pline.fill = "white" # "transparent"
        onept.elements.append(pline)

        # Re-USE it and rotate it for the other three
        for rot_ang in [90, 180, 270]:
            use_elem = svg.Use()
            use_elem.href = "#" + id_str
            use_elem.transform = "rotate(" + str(rot_ang) + ")"
            group.elements.append(use_elem)

    def draw_small_pts(self, id_str, angle, draw_cir = True):
        """
        """
        start_len = 0.575
        end_len = 0.705
        pt_len = 0.76
        pt_rad = 0.02

        group = svg.G()
        group.id = id_str + "_group"
        group.stroke = "black"
        group.stroke_width = "0.1%"
        group.transform = "rotate(" + str(angle) + ")"
        group.elements = []
        self.top_group.elements.append(group)

        # Draw one point
        onept = svg.G()
        onept.id = id_str
        onept.elements = []
        group.elements.append(onept)

        values = [0, start_len, 0, end_len]
        pline = svg.Polygon(points = values)
        onept.elements.append(pline)
        if (draw_cir == True):
            cir = svg.Circle()
            cir.cx = 0
            cir.cy = pt_len
            cir.r = pt_rad
            cir.stroke_width = 0
            onept.elements.append(cir)

        # Re-USE it and rotate it for the other three
        for use_idx in range(7):
            use_elem = svg.Use()
            use_elem.href = "#" + id_str
            use_elem.transform = "rotate(" + str((use_idx + 1) * 45) + ")"
            group.elements.append(use_elem)

        
    def draw(self):
        self.draw_circle(0.68, "0.1%")
        self.draw_circle(0.65, "0.3%")
        self.draw_circle(0.575, "0.1%")
        self.draw_circle(0.45, "0.1%")
        self.draw_circle(0.42, "0.3%")
        self.draw_small_pts("pt32nd_1", 22.5 * 0.5, False)
        self.draw_small_pts("pt32nd_2", 22.5 * 1.5, False)
        self.draw_small_pts("sixteenth", 22.5)
        self.draw_principal_points("Ordinal_dir",   0.8, 0.1   , True, 45)
        self.draw_principal_points("Cardinal_dir",  1.0, 0.1875, False, 0)


    def print(self):
        print(self.svg)


if __name__ == "__main__":
    cr = CompassRose()
    cr.draw()
    cr.print()
