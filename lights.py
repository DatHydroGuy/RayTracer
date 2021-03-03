class PointLight:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

    def __eq__(self, other):
        return self.position == other.position and \
               self.intensity == other.intensity
