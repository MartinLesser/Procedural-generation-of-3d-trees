import control.matrix as matrix

class Turtle3D:
    def __init__(self):
        self.pos = [0.0, 0.0, 0.0]
        self.vector = [0.0, 1.0, 0.0]

    def forward(self, line_length):
        self.pos = matrix.add(self.pos, matrix.mult(self.vector, line_length))