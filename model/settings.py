class Settings:
    def __init__(self):
        self.angle_z_min = 0
        self.angle_z_max = 0
        self.angle_y_min = 0
        self.angle_y_max = 0
        self.angle_x_min = 0
        self.angle_x_max = 0
        self.branch_min = 0
        self.branch_max = 0
        self.generations = 0
        self.base_length = 0
        self.base_radius = 0
        self.bark_path = ""
        self.leaf_path = ""

    def print_settings(self):
        print("Angle-z: " + str(self.angle_z_min) + " - " + str(self.angle_z_max))
        print("Angle-y: " + str(self.angle_y_min) + " - " + str(self.angle_y_max))
        print("Angle-x: " + str(self.angle_x_min) + " - " + str(self.angle_x_max))
        print("branch-shortening: " + str(self.branch_min) + " - " + str(self.branch_max))
        print("generations: " + str(self.generations))
        print("base_length: " + str(self.base_length))
        print("base_radius: " + str(self.base_radius))
        print("bark-texture path: " + str(self.bark_path))
        print("leaf-texture path: " + str(self.leaf_path))