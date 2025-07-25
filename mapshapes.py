

class ShapesBase():

    def __init__(self):
        self.shape_file = None

    def get_class_name(self):
        return type(self).__name__

    def plot(self):
        pass


class WorldCoarse(ShapesBase):

    def __init__(self):
        super().__init__()

