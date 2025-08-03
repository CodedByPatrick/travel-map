
import svg


class MapImage():

    def __init__(self):
        pass

    def add_polyline(self, pline):
        pass

    def print(self):
        pass


class SvgImage(MapImage):

    def __init__(self):
        super().__init__()

        self.svg = svg.SVG()
        self.curr_group = self.svg
        self.top_group = self.svg

        # Width and height of final image
        #
        self.svg.width = 1000
        self.svg.height = 750

        # View Box on the elements in the image.
        # This view box is expanded to fill the final image.
        #
        #self.svg.viewBox = svg.ViewBoxSpec(-180, -90, 370, 180)
        self.svg.viewBox = svg.ViewBoxSpec(-3.5, -1.5, 7, 3)

        self.svg.elements = []

        self.add_group("top_scale")
        self.top_group = self.curr_group
        self.top_group.transform = [ svg.Scale(1, -1) ]

    def add_group(self, gid):
        new_group = svg.G()

        new_group.id = gid
        new_group.stroke = "red"
        new_group.stroke_width = "0.1%"
        new_group.stroke_linecap = "round"
        new_group.fill = "transparent"
        new_group.fill = "green"
        new_group.elements = []

        self.top_group.elements.append(new_group)
        self.curr_group = new_group

    def set_group_attr(self, color):
        """ TODO - FIX THIS
        """
        self.curr_group.stroke = "blue"
        

    def add_polyline(self, pline):
        """
        pyshp shape data is a list of tuples.
        svg Polyline needs a list.
        Perform conversion.
        """
        pts = [item for ltuple in pline for item in ltuple]
        #pts = [0,0,100,200,200,0]
        sp = svg.Polyline(points = pts)
        self.curr_group.elements.append(sp)

    def add_polygon(self, pline):
        """
        pyshp shape data is a list of tuples.
        svg Polyline needs a list.
        Perform conversion.
        """
        pts = [item for ltuple in pline for item in ltuple]
        sp = svg.Polygon(points = pts)
        self.curr_group.elements.append(sp)

    def print(self):
        print(self.svg)
