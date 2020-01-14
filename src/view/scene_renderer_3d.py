import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

class SceneRenderer:
    def __init__(self, settings):
        self.settings = settings
        self.text_width = 340
        self.window_width = 900
        self.window_height = 700
        self.texture1_id = 0
        self.texture2_id = 0

    def initialize_openGL(self, Width, Height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT, GL_FILL)
        glPolygonMode(GL_BACK, GL_FILL)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable( GL_MULTISAMPLE )
        #glEnable(GL_LIGHTING)

    def initialize_renderer(self):
        pygame.init()
        pygame.key.set_repeat(1,30)
        glutInit()
        display = (self.window_width,self.window_height)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        self.initialize_openGL(self.window_width,self.window_height)
        self.texture1_id = self.load_texture(self.settings.bark_path, "RGB")
        self.texture2_id = self.load_texture(self.settings.leaf_path, "RGBA")
        glTranslatef(0.0, -5.2, -14)
        glRotatef(180,0,1,0)

    def load_texture(self, path, mode):
        if mode == "RGB":
            gl = GL_RGB
        else:
            gl = GL_RGBA
        textureSurface = pygame.image.load(path)
        textureData = pygame.image.tostring(textureSurface, mode, 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()

        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, gl, width, height, 0, gl, GL_UNSIGNED_BYTE, textureData)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        return texid

    def draw_axis(self):
        glBegin(GL_LINES)
        # x-axis
        glColor3f(1.0, 0.0, 0.0)
        glVertex3fv((0.0, 0.0, 0.0))
        glVertex3fv((1.0, 0.0, 0.0))
        # y-axis
        glColor3f(0.0, 1.0, 0.0)
        glVertex3fv((0.0, 0.0, 0.0))
        glVertex3fv((0.0, 1.0, 0.0))
        # z-axis
        glColor3f(0.0, 0.0, 1.0)
        glVertex3fv((0.0, 0.0, 0.0))
        glVertex3fv((0.0, 0.0, 1.0))
        glEnd()
        self.glut_print( 10 , 40 , GLUT_BITMAP_9_BY_15 , "X-Axis", 1.0 , 0.0 , 0.0 , 1.0 )
        self.glut_print( 10 , 25 , GLUT_BITMAP_9_BY_15 , "Y-Axis", 0.0 , 1.0 , 0.0 , 1.0 )
        self.glut_print( 10 , 10 , GLUT_BITMAP_9_BY_15 , "Z-Axis", 0.0 , 0.0 , 1.0 , 1.0 )
        glColor3f(1.0, 1.0, 1.0)

    def draw_lines(self, model, leafs):
        self.draw_axis()
        i = 0
        glColor3f(1.0, 1.0, 1.0)
        for branch in model:
            glBegin(GL_LINE_STRIP)
            for vertex in branch:
                glVertex3fv(vertex)
                i += 1
            glEnd()
        glColor3f(0.0, 1.0, 0.0)
        j = 0
        for leaf in leafs:
            glBegin(GL_LINE_LOOP)
            for vertex in leaf:
                glVertex3fv(vertex)
                j += 1
            j += 1
            glEnd()
        self.glut_print( 10 , 55 , GLUT_BITMAP_9_BY_15 , "Lines = "+str(i+j-2) , 1.0 , 1.0 , 1.0 , 1.0 )

    def draw_triangles(self, vertex_list, indices, tex_coord):
        self.draw_axis()
        model_vertices = vertex_list[0]
        leafs_vertices = vertex_list[1]
        model_indices = indices[0]
        leafs_indices = indices[1]
        model_coord = tex_coord[0]
        leafs_coord = tex_coord[1]

        # trunk and branches
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture1_id)
        glBegin(GL_TRIANGLES)
        for i, index in enumerate(model_indices[0]):
            glTexCoord2f(model_coord[i][0],model_coord[i][1])
            glVertex3fv(model_vertices[index])
        for i, index in enumerate(model_indices[1]):
            glTexCoord2f(model_coord[i+len(model_indices[0])][0],model_coord[i+len(model_indices[0])][1])
            glVertex3fv(model_vertices[index])
        glEnd()

        # leafs
        glDepthMask(GL_FALSE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.texture2_id)
        glBegin(GL_TRIANGLES)
        for i, index in enumerate(leafs_indices):
            glTexCoord2f(leafs_coord[i][0],leafs_coord[i][1])
            glVertex3fv(leafs_vertices[index])
        glEnd()
        glDisable(GL_BLEND)
        glDepthMask(GL_TRUE)
        glDisable(GL_TEXTURE_2D)

        self.glut_print( 10 , 55 , GLUT_BITMAP_9_BY_15 , "Triangles = "+str(len(model_indices[0]+model_indices[1])/3 + len(leafs_indices)/3) , 1.0 , 1.0 , 1.0 , 1.0 )

    def draw_wireframe(self, vertex_list, indices):
        self.draw_axis()
        model_vertices = vertex_list[0]
        leafs_vertices = vertex_list[1]
        model_indices = indices[0]
        leafs_indices = indices[1]
        # trunk and branches
        glColor4f(1.0, 1.0, 1.0, 1.0)
        for i, index in enumerate(model_indices[0]):
            if i % 3 == 0:
                glBegin(GL_LINE_LOOP)
                glVertex3fv(model_vertices[model_indices[0][i]])
                glVertex3fv(model_vertices[model_indices[0][i+1]])
                glVertex3fv(model_vertices[model_indices[0][i+2]])
                glEnd()
        for i, index in enumerate(model_indices[1]):
            if i % 3 == 0:
                glBegin(GL_LINE_LOOP)
                glVertex3fv(model_vertices[model_indices[1][i]])
                glVertex3fv(model_vertices[model_indices[1][i+1]])
                glVertex3fv(model_vertices[model_indices[1][i+2]])
                glEnd()
        # leafs
        glColor4f(0.0, 1.0, 0.0, 1.0)
        for i, index in enumerate(leafs_indices):
            if i % 3 == 0:
                glBegin(GL_LINE_LOOP)
                glVertex3fv(leafs_vertices[leafs_indices[i]])
                glVertex3fv(leafs_vertices[leafs_indices[i+1]])
                glVertex3fv(leafs_vertices[leafs_indices[i+2]])
                glEnd()
        self.glut_print( 10 , 55 , GLUT_BITMAP_9_BY_15 , "Edges = "+str(len(model_indices)+len(leafs_indices)) , 1.0 , 1.0 , 1.0 , 1.0 )

    def draw_points(self, model, leafs):
        self.draw_axis()
        glBegin(GL_POINTS)
        i = 0
        for branch in model:
            for segment in branch:
                for vertex in segment:
                    glVertex3fv(vertex)
                    i += 1
        glColor3f(0.0, 1.0, 0.0)
        for leaf in leafs:
            for vertex in leaf:
                glVertex3fv(vertex)
                i += 1
        glEnd()
        self.glut_print( 10 , 55 , GLUT_BITMAP_9_BY_15 , "Vertices = "+str(i) , 1.0 , 1.0 , 1.0 , 1.0 )

    def glut_print(self, x,  y,  font,  text, r,  g , b , a):
        glColor4f(r,g,b,a)
        glWindowPos2f(x,y)
        for ch in text :
            glutBitmapCharacter( font , ctypes.c_int( ord(ch) ) )

    def rotate(self, angle, x, y, z):
        glRotatef(angle, x, y, z)

    def translate(self, x, y, z):
        glTranslatef(x, y, z)

    def render_scene(self, mesh, draw_function, exported, saved, num_generations):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.glut_print( 10 , 70 , GLUT_BITMAP_9_BY_15 , "Iterations = {0}".format(num_generations) , 1.0 , 1.0 , 1.0 , 1.0 )
        self.glut_print( self.window_width-self.text_width , 10 , GLUT_BITMAP_9_BY_15 , "Press Space to generate a new model " , 1.0 , 1.0 , 1.0 , 1.0 )
        self.glut_print( self.window_width-self.text_width , 25 , GLUT_BITMAP_9_BY_15 , "Press e to export the model " , 1.0 , 1.0 , 1.0 , 1.0 )
        self.glut_print( self.window_width-self.text_width , 40 , GLUT_BITMAP_9_BY_15 , "Press s to save the model as a string" , 1.0 , 1.0 , 1.0 , 1.0 )
        self.glut_print( self.window_width-self.text_width , 55 , GLUT_BITMAP_9_BY_15 , "Press Enter to change draw-mode " , 1.0 , 1.0 , 1.0 , 1.0 )
        self.glut_print( self.window_width-self.text_width , 70 , GLUT_BITMAP_9_BY_15 , "Press Arrow-Keys to rotate the model" , 1.0 , 1.0 , 1.0 , 1.0 )
        self.glut_print( self.window_width-self.text_width , 85 , GLUT_BITMAP_9_BY_15 , "Press + or - to change the iterations" , 1.0 , 1.0 , 1.0 , 1.0 )
        if exported:
            self.glut_print( self.window_width/2-150 , self.window_height-15 , GLUT_BITMAP_9_BY_15 , "The model was exported successfully!" , 1.0 , 1.0 , 1.0 , 1.0 )
        if saved:
            self.glut_print( self.window_width/2-150 , self.window_height-30 , GLUT_BITMAP_9_BY_15 , "The model was saved successfully!" , 1.0 , 1.0 , 1.0 , 1.0 )

        if draw_function == self.draw_points:
            draw_function(mesh.model, mesh.leafs)
        elif draw_function == self.draw_lines:
            draw_function(mesh.vertex_model[0], mesh.leafs)
        elif draw_function == self.draw_wireframe:
            draw_function(mesh.vertex_list, mesh.indices)
        elif draw_function == self.draw_triangles:
            draw_function(mesh.vertex_list, mesh.indices, mesh.tex_coord)