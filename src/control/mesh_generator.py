import math
import control.matrix as matrix
from control.turtle_3d import Turtle3D
from model.constants import BRANCH_MIN_THICKNESS
from model.constants import BRANCH_RATIO_FACTOR
from model.constants import NEW_BRANCH_RATIO_FACTOR
from model.constants import NUM_SIDES_FACTOR
from model.mesh import Mesh

class MeshGenerator:
    def create_leaf(self, turtle3d, line_length):
        """
        Calculates four vertices with the formular for planes. This creates a square which will be rendered as two
        polygons with an alpha-texture.
        :param turtle3d: obect of Turtle3D
        :param line_length: float is the branch length
        :return: leaf: list of four vertices
        """
        leaf = []
        main_vector = (turtle3d.pos[0],turtle3d.pos[1],turtle3d.pos[2])
        vector1 = turtle3d.vector
        vector2 = matrix.rotate_left_z(turtle3d.vector, 90.0)
        y = 0.0
        x = -line_length  * 2 + line_length
        new_point = matrix.add(matrix.add(main_vector, matrix.mult(vector1, x)), matrix.mult(vector2, y))
        leaf.append(new_point)
        y = line_length * 2
        x = 0.0  + line_length
        new_point = matrix.add(matrix.add(main_vector, matrix.mult(vector1, x)), matrix.mult(vector2, y))
        leaf.append(new_point)
        y = 0.0
        x = line_length * 2  + line_length
        new_point = matrix.add(matrix.add(main_vector, matrix.mult(vector1, x)), matrix.mult(vector2, y))
        leaf.append(new_point)
        y = -line_length * 2
        x = 0.0  + line_length
        new_point = matrix.add(matrix.add(main_vector, matrix.mult(vector1, x)), matrix.mult(vector2, y))
        leaf.append(new_point)
        return leaf

    def generate_vertex_model(self, turtle_string, settings):
        """
        Generates the skeleton-tree. Interprets every character. For every "F" a point is calculated. Which is added
        to a branch-list. If a ] is read a new branch-list will be created and the turtle will jump to another point
        on the tree to draw the next branch. Rotations muss be saved (rx,ry,rz) to be used later in generate_poly_model.
        :param turtle_string: list of characters
        :param settings: object of class Settings, which stores necessary information like base branch length.
        :return: list of all vertices of the trunk/branches, leafs and all rotations.
        """
        model = []
        branch = []
        leafs = []
        rotations = []
        position_stack = []
        vector_rotation_stack = []
        ankle_rotation_stack = []
        length_stack = []
        line_length = float(settings.base_length)  / settings.generations
        turtle3d = Turtle3D()
        rx = 0.0
        ry = 0.0
        rz = 0.0
        point = (turtle3d.pos[0],turtle3d.pos[1],turtle3d.pos[2])
        branch.append(point)
        rotations.append((rx, ry, rz))
        for index, char in enumerate(turtle_string):
            if (char == "F" or char == "G"):
                turtle3d.forward(line_length)
                point = (turtle3d.pos[0],turtle3d.pos[1],turtle3d.pos[2])
                branch.append(point)
                rotations.append((rx, ry, rz))
                continue
            if (char == "L"):
                leaf = self.create_leaf(turtle3d, line_length)
                continue
            if (char == "+"):
                temp_index = index
                temp_string = ""
                while (temp_index < len(turtle_string) - 1):
                    temp_index += 1
                    if (turtle_string[temp_index].isdigit()):
                        temp_string += turtle_string[temp_index]
                    else:
                        break
                turtle3d.vector = matrix.rotate_left_z(turtle3d.vector, float(temp_string))
                rz += float(temp_string)
                continue
            if (char == "-"):
                temp_index = index
                temp_string = ""
                while (temp_index < len(turtle_string) - 1):
                    temp_index += 1
                    if (turtle_string[temp_index].isdigit()):
                        temp_string += turtle_string[temp_index]
                    else:
                        break
                turtle3d.vector = matrix.rotate_right_z(turtle3d.vector, float(temp_string))
                rz += -float(temp_string)
                continue
            if (char == "<"):
                temp_index = index
                temp_string = ""
                while (temp_index < len(turtle_string) - 1):
                    temp_index += 1
                    if (turtle_string[temp_index].isdigit()):
                        temp_string += turtle_string[temp_index]
                    else:
                        break
                turtle3d.vector = matrix.rotate_left_y(turtle3d.vector, float(temp_string))
                ry += float(temp_string)
                continue
            if (char == ">"):
                temp_index = index
                temp_string = ""
                while (temp_index < len(turtle_string) - 1):
                    temp_index += 1
                    if (turtle_string[temp_index].isdigit()):
                        temp_string += turtle_string[temp_index]
                    else:
                        break
                turtle3d.vector = matrix.rotate_right_y(turtle3d.vector, float(temp_string))
                ry += -float(temp_string)
                continue
            if (char == "?"):
                temp_index = index
                temp_string = ""
                while (temp_index < len(turtle_string) - 1):
                    temp_index += 1
                    if (turtle_string[temp_index].isdigit()):
                        temp_string += turtle_string[temp_index]
                    else:
                        break
                turtle3d.vector = matrix.rotate_left_x(turtle3d.vector, float(temp_string))
                rx += float(temp_string)
                continue
            if (char == "!"):
                temp_index = index
                temp_string = ""
                while (temp_index < len(turtle_string) - 1):
                    temp_index += 1
                    if (turtle_string[temp_index].isdigit()):
                        temp_string += turtle_string[temp_index]
                    else:
                        break
                turtle3d.vector = matrix.rotate_right_x(turtle3d.vector, float(temp_string))
                rx += -float(temp_string)
                continue
            if (char == "["):
                position_stack.append((turtle3d.pos[0],turtle3d.pos[1],turtle3d.pos[2]))
                vector_rotation_stack.append(turtle3d.vector)
                ankle_rotation_stack.append((rx,ry,rz))
                length_stack.append(line_length)
                continue
            if (char == "]"):
                temp = position_stack.pop()
                turtle3d.pos[0] = temp[0]
                turtle3d.pos[1] = temp[1]
                turtle3d.pos[2] = temp[2]
                turtle3d.vector = vector_rotation_stack.pop()
                ankle = ankle_rotation_stack.pop()
                rx = ankle[0]
                ry = ankle[1]
                rz = ankle[2]
                line_length = length_stack.pop()
                model.append(branch)
                branch = []
                point = (turtle3d.pos[0],turtle3d.pos[1],turtle3d.pos[2])
                branch.append(point)
                rotations.append((rx, ry, rz))
                continue
            if (char == "@"):
                line_length *= float(turtle_string[index+1]+turtle_string[index+2]+turtle_string[index+3])
                continue
            if (char == "{"):
                leaf = []
            if (char == "}"):
                leafs.append(leaf)
        model.append(branch)
        #print model
        return [model,rotations, leafs]

    def generate_poly_model(self, vertex_model, base_radius):
        """
        Generates the tree mesh. Iterates through all points of the skeleton-tree (created in generate_vertex_model()).
        At each point a segment of points is calculated in a circle. The number of points depends on the thickness of
        the branch.
        :param vertex_model: list of vertices of the skeleton-tree.
        :param base_radius: radius of the trunk. branches will be increasingly thinner.
        :return: list of vertices of the tree mesh and leafs.
        """
        branches = vertex_model[0]
        rotations = vertex_model[1]
        leafs = vertex_model[2]
        vertex_model = []
        vertex_radius = {}
        num_elements = 0
        for branch_index, branch in enumerate(branches):
            if len(branch) > 0 and branch[0] in vertex_radius:
                radius = vertex_radius[branch[0]] * NEW_BRANCH_RATIO_FACTOR
            else:
                radius = base_radius
            new_branch = []
            for segment_index, vertex in enumerate(branch):
                branch_segment = []
                if segment_index < len(branch)-1:
                    ankle = 0.0
                    local_radius = radius / ((segment_index+2) * BRANCH_RATIO_FACTOR) # branches get thinner
                    if local_radius < BRANCH_MIN_THICKNESS:
                        local_radius = BRANCH_MIN_THICKNESS
                    vertex_radius[vertex] = local_radius # radius is stored for near branches
                    num_sides = 3 + local_radius / NUM_SIDES_FACTOR # number of sides of a branch depends on it thicknes
                    delta = 360.0 / num_sides
                    while ankle < 360:
                        x = vertex[0] + local_radius * math.cos(ankle * math.pi / 180.0)
                        y = vertex[1]
                        z = vertex[2] + local_radius * math.sin(ankle * math.pi / 180.0)
                        point = (x, y, z)

                        # segments must be rotated so they are not all in a x-z-plane
                        rotation = rotations[num_elements+1]
                        point =  matrix.rotate_left_x_local(point, vertex, rotation[0])
                        #point =  matrix.rotate_left_y_local(point, vertex, rotation[1])
                        point =  matrix.rotate_left_z_local(point, vertex, rotation[2])

                        branch_segment.append((point[0], point[1], point[2]))
                        ankle += delta
                else:
                    branch_segment.append(vertex)
                new_branch.append(branch_segment)
                num_elements += 1
            if len(new_branch) > 0:
                vertex_model.append(new_branch)
        return [vertex_model, leafs]

    def create_vertex_list(self, model, leafs):
        model_list = []
        for branch in model:
            for segment in branch:
                for vertex in segment:
                    model_list.append(vertex)
        leaf_list = []
        for leaf in leafs:
            for vertex in leaf:
                leaf_list.append(vertex)
        return [model_list, leaf_list]

    def poly_indices(self, model, leafs):
        """
        Creates the list of indices necessary for PyGame to render polygons. The proportion of the number of vertices
        between the current segment and the next segment is important. This proportion tells you how many vertices of
        the current segment are connected to one vertex of the next segment. But not all polygons are created this way.
        Some holes can be left. These holes are called inverse triangles and need their own algorithm to be filled.
        :param model: list of vertices of the trunk and branches
        :param leafs: list of vertices of the leafs
        :return: list of indices for the trunk/branches and leafs
        """
        model_indices = []
        triangles = []
        inverse_triangles = []
        i = 0
        for branch in model:
            for segment_index in range(len(branch)-1):
                current_segment = branch[segment_index]
                next_segment = branch[segment_index + 1]
                delta = float(len(current_segment)) / len(next_segment) # proportion of the number of vertices between the current segment and the next segment
                # triangles
                for cur_seg_index in range(len(current_segment)):
                    triangles.append(i + cur_seg_index)
                    triangles.append(i + (cur_seg_index + 1)%len(current_segment))
                    triangles.append(i + len(current_segment) + int(cur_seg_index/delta))
                    #print str(i + cur_seg_index) + "," + str(i + (cur_seg_index + 1)%len(current_segment)) + "," + str(i + len(current_segment) + int(cur_seg_index/delta))
                    #print str(cur_seg_index) + "/" + str(delta) + "=" + str(int(cur_seg_index/delta))
                # inverse triangles
                if len(next_segment) > 1:
                    for next_seg_index in range(len(next_segment)):
                        inverse_triangles.append(i + len(current_segment) + next_seg_index)
                        inverse_triangles.append(i + int(math.ceil((next_seg_index+1) * delta))%len(current_segment))
                        inverse_triangles.append(i + len(current_segment) + (next_seg_index + 1)%len(next_segment))
                        #print str(i + len(current_segment) + next_seg_index) + "," + str(i + int(math.ceil((next_seg_index+1) * delta))%len(current_segment)) + "," + str(i + len(current_segment) + (next_seg_index + 1)%len(next_segment))
                i += len(current_segment)
            i += 1
        model_indices.append(triangles)
        model_indices.append(inverse_triangles)
        leaf_indices = []
        i = 0
        for _ in leafs:
            #first triangle
            leaf_indices.append(i)
            leaf_indices.append(i+1)
            leaf_indices.append(i+2)
            #second triangle
            leaf_indices.append(i+2)
            leaf_indices.append(i+3)
            leaf_indices.append(i)
            i += 4
        return [model_indices, leaf_indices]

    def texture_coordinates(self, indices):
        model_coord = []
        leaf_coord = []
        model_indices = indices[0]
        leafs_indices = indices[1]
        u = 0.1
        v = 1.0
        w = 0
        for i, index in enumerate(model_indices[0]):
            if i % 3 == 0:
                model_coord.append((0,0,w))
            if i % 3 == 1:
                model_coord.append((u,0,w))
            if i % 3 == 2:
                model_coord.append((0,v,w))
        for i, index in enumerate(model_indices[1]):
            if i % 3 == 0:
                model_coord.append((0,v,w))
            if i % 3 == 1:
                model_coord.append((u,0,w))
            if i % 3 == 2:
                model_coord.append((u,v,w))
        for i, index in enumerate(leafs_indices):
            if i % 6 == 0:
                leaf_coord.append((0,0,w))
            elif i % 6 == 1:
                leaf_coord.append((1,0,w))
            elif i % 6 == 2:
                leaf_coord.append((1,1,w))
            elif i % 6 == 3:
                leaf_coord.append((1,1,w))
            elif i % 6 == 4:
                leaf_coord.append((0,1,w))
            elif i % 6 == 5:
                leaf_coord.append((0,0,w))
        return [model_coord, leaf_coord]

    def generate_model(self, turtle_string, settings):
        mesh = Mesh()
        mesh.vertex_model = self.generate_vertex_model(turtle_string, settings)
        mesh.modelAndLeafs = self.generate_poly_model(mesh.vertex_model, settings.base_radius)
        mesh.model = mesh.modelAndLeafs[0]
        mesh.leafs = mesh.modelAndLeafs[1]
        mesh.indices = self.poly_indices(mesh.model, mesh.leafs)
        mesh.vertex_list = self.create_vertex_list(mesh.model, mesh.leafs)
        mesh.tex_coord = self.texture_coordinates(mesh.indices)
        return mesh