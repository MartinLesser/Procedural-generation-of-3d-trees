from control.text_generator import TextGenerator
from control.mesh_generator import MeshGenerator
from control.interface import Interface
from view.scene_renderer_3d import SceneRenderer
from control.export import *
from random import randint
import pygame

class GeneratorManager:
    """
    This class is the core of the tree generation system. It loads the necessary data from a file. Generates a
    turtle-string and generates a mesh from it. The scene renderer renders the object.
    """
    def __init__(self):
        self.interface = Interface()
        self.text_generator = TextGenerator()
        self.mesh_generator = MeshGenerator()
        self.scene = None
        self.num_generations = 0
        self.grammar = None
        self.settings = None
        self.turtle_string = None
        self.mesh = None
        self.seed = 0
        self.draw_function = None
        self.exported = False
        self.saved = False

    def generate_mesh(self):
        self.turtle_string = self.text_generator.generate_turtle_string_3d(self.num_generations, self.seed, self.grammar, self.settings)
        self.mesh = self.mesh_generator.generate_model(self.turtle_string, self.settings)

    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.scene.rotate(1, 0, 1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.scene.rotate(-1, 0, 1, 0)
                    if event.key == pygame.K_UP:
                        self.scene.translate(0,0.25,0)
                    if event.key == pygame.K_DOWN:
                        self.scene.translate(0,-0.25,0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scene.translate(0,0,-1.0)
                    if event.button == 5:
                        self.scene.translate(0,0,1.0)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.seed = randint(0, 9999)
                        self.generate_mesh()
                    if event.key == pygame.K_KP_PLUS:
                        if(self.num_generations <= 10):
                            self.num_generations += 1
                            self.generate_mesh()
                    if event.key == pygame.K_KP_MINUS:
                        if(self.num_generations > 2):
                            self.num_generations -= 1
                            self.generate_mesh()
                    if event.key == pygame.K_e:
                        export_model_obj(self.mesh.vertex_list, self.mesh.indices, self.mesh.tex_coord)
                        self.exported = True
                    if event.key == pygame.K_s:
                        self.interface.write_file("../resources/nice_trees.txt", self.turtle_string)
                        self.saved = True
                    if event.key == pygame.K_RETURN:
                        if self.draw_function ==  self.scene.draw_triangles:
                            self.draw_function = self.scene.draw_wireframe
                        elif self.draw_function ==  self.scene.draw_wireframe:
                            self.draw_function = self.scene.draw_points
                        elif self.draw_function ==  self.scene.draw_points:
                            self.draw_function = self.scene.draw_lines
                        elif self.draw_function ==  self.scene.draw_lines:
                            self.draw_function = self.scene.draw_triangles

    def generate_tree(self, file_src):
        """
        Loads the data from a file. Sets up the scene renderer. Generates a turtle-string and a
        tree mesh and renders it.
        :param file_src: String which contains the path to the file which contains the grammar and settings data
        """
        data = self.interface.read_file(file_src)
        self.grammar = data[0]
        self.settings = data[1]
        #grammar.print_grammar()
        #settings.print_settings()
        self.seed = randint(0, 9999)
        self.num_generations = self.settings.generations
        self.scene = SceneRenderer(self.settings)

        self.turtle_string = self.text_generator.generate_turtle_string_3d(self.num_generations, self.seed, self.grammar, self.settings)
        self.mesh = self.mesh_generator.generate_model(self.turtle_string, self.settings)
        self.scene.initialize_renderer()

        export_timer = 0
        saved_timer = 0
        self.draw_function = self.scene.draw_triangles
        while True:
            self.handle_input()
            self.scene.render_scene(self.mesh, self.draw_function, self.exported, self.saved, self.num_generations)
            if self.exported:
                # counts time to show the "exported" string on screen for a while
                export_timer += 1
            if self.saved:
                # counts time to show the "saved" string on screen for a while
                saved_timer += 1
            if export_timer == 30:
                export_timer = 0
                self.exported = False
            if saved_timer == 30:
                saved_timer = 0
                self.saved = False

            pygame.display.flip()
            pygame.time.wait(1)

if __name__ == "__main__":
     GeneratorManager().generate_tree("../resources/grammars/3d/tree_01.txt")
     # tree_01 tree_02 conifer bush simple_3d_tree