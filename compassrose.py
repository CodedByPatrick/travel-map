
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
        

    def draw_four_points(self, id_str, point_length, base_size, half_fill, angle):
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

        # Make one point
        values = [0, 0, -base_x, base_y, 0, point_length]
        pline = svg.Polygon(points = values)
        onept.elements.append(pline)
        values = [0, 0, base_x, base_y, 0, point_length]
        pline = svg.Polygon(points = values)
        if (half_fill == False):
            pline.fill = "white" # "transparent"
        onept.elements.append(pline)

        # Re-USE it and rotate it for the other three
        for num_dup in range(3):
            use_elem = svg.Use()
            use_elem.href = "#" + id_str
            use_elem.transform = "rotate(" + str((num_dup+1)*90) + ")"
            group.elements.append(use_elem)

    def draw_circle(self, radius, width):
        cir = svg.Circle()
        cir.cx = 0
        cir.cy = 0
        cir.r = radius
        cir.stroke_width = width
        cir.fill = "transparent"
        self.top_group.elements.append(cir)
        
    def draw(self):
        self.draw_circle(0.75, "0.1%")
        self.draw_circle(0.72, "0.3%")
        self.draw_circle(0.60, "0.1%")
        self.draw_circle(0.45, "0.1%")
        self.draw_circle(0.42, "0.3%")
        self.draw_four_points("L2_points",   0.9, 0.1, True, 45)
        self.draw_four_points("Main_points", 1.0, 0.20, False, 0)


    def print(self):
        print(self.svg)


if __name__ == "__main__":
    cr = CompassRose()
    cr.draw()
    cr.print()
