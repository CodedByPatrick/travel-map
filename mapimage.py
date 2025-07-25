
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
        self.svg.width = 200
        self.svg.height = 200
        self.svg.elements = []

    def add_polyline(self, pline):
        #
        # pyshp shape data is a list of tuples.
        # svg Polyline needs a list.
        # Perform conversion.
        #
        pts = [item for ltuple in pline for item in ltuple]
        #pts = [0,0,100,200,200,0]
        sp = svg.Polyline(points = pts,
                          stroke_width = 5,
                          stroke = "black",
                          fill = "transparent",
                          )
        self.svg.elements.append(sp)

    def print(self):
        print(self.svg)
