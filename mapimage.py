
import svg


class MapAttr():

    def __init__(self):
        self.line_color = None
        self.line_width = None
        self.area_fill = None

    def set_default_attr(self):
        self.line_color = "black"
        self.line_width = "1%"
        self.area_fill = "transparent"
        
    def set_line_color(self, color):
        """Set line color.
        color is an SVG color ("stroke") string.
        """
        self.line_color = color

    def set_line_width(self, width):
        """Set line width.
        width is an SVG width ("stroke_width") string.
        """
        self.line_width = width

    def set_area_fill(self, fill_type):
        """Set area fill type.
        fill_type is an SVG "fill" string: "transparent" or a color.
        """
        self.area_fill = fill_type

    
class MapImage():
    """Base class for map images.
    Currently, (and probably always) there is only one.
    """

    def __init__(self):
        pass

    def add_polyline(self, pline):
        pass

    def print(self):
        pass


class SvgImage(MapImage):
    """SVG Map Image.
    """

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
        self.top_group.stroke_linecap = "round"

    def __set_obj_attr(self, obj, attr):
        """Set attributes on an SVG object.
        obj is any SVG object that supports "stroke", "stroke_width", etc.
        attr is MapAttr class object
        """
        if (attr.line_color != None):
            obj.stroke = attr.line_color
        if (attr.line_width != None):
            obj.stroke_width = attr.line_width
        if (attr.area_fill != None):
            obj.fill = attr.area_fill
        
    def add_group(self, gid, attr = None):
        """Add a new SVG group ("g" element) to the top level group.
        gid is a Group ID string.
        attr is a MapAttr class object.
        """
        new_group = svg.G()
        new_group.id = gid
        new_group.elements = []

        new_attr = attr
        if (new_attr == None):
            new_attr = MapAttr()
            new_attr.set_default_attr()
        self.__set_obj_attr(new_group, new_attr)

        '''
        # Example SVG group attributes:
        new_group.stroke = "red"
        new_group.stroke_width = "0.1%"
        new_group.fill = "transparent"
        new_group.fill = "green"
        '''

        self.top_group.elements.append(new_group)
        self.curr_group = new_group

    def set_group_attr(self, attr):
        """Set attributes on the current SVG group element.
        attr is a MapAttr class object.
        """
        self.__set_obj_attr(self.curr_group, attr)

    def add_polyline(self, pline, attr = None):
        """Add a polyline (set of connected points) to the map image.
        pline is a list of tuples
        attr is a MapAttr class object
        """
        """
        pyshp shape data consists of a list of tuples.
        svg Polyline needs a list of values "[x1 y1 x2 y2 ...]".
        The following list comprehension performs the conversion.
        """
        pts = [item for ltuple in pline for item in ltuple]
        #pts = [0,0,100,200,200,0]
        sp = svg.Polyline(points = pts)
        self.curr_group.elements.append(sp)

    def add_polygon(self, pline, attr = None):
        """Add a polygon to the SVG map image.
        See add_polyline for additional information.
        """
        pts = [item for ltuple in pline for item in ltuple]
        sp = svg.Polygon(points = pts)
        self.curr_group.elements.append(sp)

    def add_points(self, point_list, attr = None):
        """Add a set of points to the map image.
        Points will be added as circles.
        """
        for point in point_list:
            scir = svg.Circle(
                cx = point[0],
                cy = point[1],
                r = 0.01
            )
        self.curr_group.elements.append(scir)

    def print(self):
        print(self.svg)
