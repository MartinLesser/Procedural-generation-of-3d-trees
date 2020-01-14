from random import randint, seed
from model.rule import Rule

class TextGenerator:
    """
    This class generates turtle-strings. The function generate_turtle_string_3d replaces symbols with a fitting
    rule each generation. The function post_processing is needed to fill the turtle-string with numbers e.g. degrees
    for rotations.
    """
    def handle_special_constructs(self, string):
        temp = ""
        index = 0
        while index < len(string):
            # | : either ... or ...
            if(string[index] == '('):
                if(randint(0,1) == 0):
                    temp += string[index+1]
                else:
                    temp += string[index+2]
                index += 3
            #elif ...
            else:
                temp += string[index]
            index += 1
        return temp

    def post_processing(self, string, settings):
        temp = ""
        vertex_dict = {}
        branch_level = 0
        vertex_dict[branch_level] = []
        for index, char in enumerate(string):
            # B : leaf
            if(char == 'B'):
                temp += "{L}" #
            # @ : branch-shortening
            elif(char == '@' and not string[index+1].isdigit()):
                temp += char + str(randint(int(settings.branch_min*100), int(settings.branch_max*100))/100.0)
            # + or - : z-rotation
            elif((char == '+' or char == '-' ) and not string[index+1].isdigit()):
                temp += char + str(randint(settings.angle_z_min, settings.angle_z_max))
            # < or > : y-rotation
            elif((char == '<' or char == '>') and not string[index+1].isdigit()):
                temp += char + str(randint(settings.angle_y_min, settings.angle_y_max))
            # < or > : x-rotation
            elif((char == '(' or char == ')') and not string[index+1].isdigit()):
                temp += char + str(randint(settings.angle_x_min, settings.angle_x_max))
            elif(char == "["):
                temp += char
                branch_level += 1
                if vertex_dict.get(branch_level) == None:
                    vertex_dict[branch_level] = []
            elif(char == "]"):
                temp += char
                branch_level -= 1
                #vertex_dict[branch_level+1] = []
            elif(char == 'r'):
                rndm_x_rotation = randint(settings.angle_x_min, settings.angle_x_max)
                rndm_y_rotation = randint(settings.angle_y_min, settings.angle_y_max)
                rndm_z_rotation = randint(settings.angle_z_min, settings.angle_z_max)
                rotations = (rndm_x_rotation, rndm_y_rotation, rndm_z_rotation)
                vertex_dict[branch_level].append(rotations)
                # + or - : z-rotation
                if(randint(0,1) == 0):
                    temp += "+" + str(rndm_z_rotation)
                else:
                    temp += "-" + str(rndm_z_rotation)
                # < or > : y-rotation
                if (randint(0, 1) == 0):
                    temp += "<" + str(rndm_y_rotation)
                #elif (randint(0, 1) == 0):
                else:
                    temp += ">" + str(rndm_y_rotation)
                # < or > : x-rotation
                if (randint(0, 1) == 0):
                    temp += "?" + str(rndm_x_rotation)
                #elif (randint(0, 1) == 0):
                else:
                    temp += "!" + str(rndm_x_rotation)
            else:
                temp += char
        #print vertex_dict
        return temp

    def generate_turtle_string_3d(self, num_generations, seedNumber, grammar, settings):
        seed(seedNumber)
        string = grammar.axiom
        #print("n = 0: {0}".format(string))
        for i in range(num_generations):
            new_string = ""
            for symbol in string:
                if(symbol in grammar.variables):
                    rules = grammar.search_rule_lhs(symbol)
                    chosen_rule = rules[randint(0,len(rules)-1)]
                    new_string = new_string + chosen_rule.rhs
                else:
                    new_string = new_string + symbol
            string = new_string
            #print("n = {0}: {1}".format(i+1,string))
        #print string
        string = self.handle_special_constructs(string)
        #print string
        string = self.post_processing(string, settings)
        print string
        return string

    def generate_turtle_string_2d(self, num_generations, grammar, settings):
        string = grammar.axiom
        #print("n = 0: " + string)
        for i in range(num_generations):
            new_string = ""
            for symbol in string:
                if(symbol in grammar.variables):
                    rules = grammar.search_rule_lhs(symbol)
                    chosen_rule = rules[randint(0,len(rules)-1)]
                    new_string = new_string + chosen_rule.rhs
                else:
                    new_string = new_string + symbol
            string = new_string
            #print("n = " + str(i+1) + ": " + string)
        # @ : branch-shortening
        temp = string.split("@")
        string = ""
        for index, part in enumerate(temp):
            string += part
            if (index < len(temp) - 1):
                string += "@" + str(randint(int(settings.branch_min*100), int(settings.branch_max*100))/100.0)
        # + : xy-rotation
        temp = string.split("+")
        string = ""
        for index, part in enumerate(temp):
            string += part
            if (index < len(temp) - 1):
                string += "+" + str(randint(settings.angle_z_min, settings.angle_z_max))
        # - : xy-rotation
        temp = string.split("-")
        string = ""
        for index, part in enumerate(temp):
            string += part
            if (index < len(temp) - 1):
                string += "-" + str(randint(settings.angle_z_min, settings.angle_z_max))
        return string