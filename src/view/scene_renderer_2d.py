from control.text_generator import TextGenerator
from control.interface import Interface
import turtle
import time
from random import randint

def initialize_turtle():
    turtle.clearscreen()
    turtle.hideturtle()
    turtle.speed(0)
    turtle.pencolor("green")
    turtle.penup()
    turtle.setpos(0,-100) #turtle.window_width() / 2, turtle.window_height() / 2
    turtle.setheading(90)
    turtle.pendown()

def draw_2d_scene(turtle_string, line_length):
    position_stack = []
    angle_stack = []
    length_stack = []
    for index, char in enumerate(turtle_string):
        if (char == "F" or char == "G"):
            turtle.forward(line_length)
            continue
        if (char == "-"):
            temp_index = index
            temp_string = ""
            while(temp_index < len(turtle_string)-1):
                temp_index += 1
                if(turtle_string[temp_index].isdigit()):
                    temp_string += turtle_string[temp_index]
                else:
                    break
            turtle.left(float(temp_string))
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
            turtle.right(float(temp_string))
            continue
        if (char == "["):
            position_stack.append(turtle.pos())
            angle_stack.append(turtle.heading())
            length_stack.append(line_length)
            continue
        if (char == "]"):
            turtle.penup()
            turtle.setpos(position_stack.pop())
            turtle.setheading(angle_stack.pop())
            line_length = length_stack.pop()
            turtle.pendown()
            continue
        if (char == "@"):
            line_length *= float(turtle_string[index+1]+turtle_string[index+2]+turtle_string[index+3])
            continue
    #turtle.exitonclick()


if __name__ == "__main__":
    # koch_curve sierpinski_triangle dragon_curve fractal_plant simple_tree tree_experiment
    data = Interface().read_file("../resources/grammars/2d/simple_tree.txt")
    grammar = data[0]
    settings = data[1]
    num_generations = settings.generations
    line_length = settings.base_length / num_generations
    text_generator = TextGenerator()
    while(True):
        initialize_turtle()
        turtle_string = text_generator.generate_turtle_string_2d(num_generations, grammar, settings)
        #turtle_string = "F-20F"
        print(turtle_string)
        draw_2d_scene(turtle_string, line_length)
        time.sleep(1)