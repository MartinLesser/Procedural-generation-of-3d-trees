from model.grammar import Grammar
from model.settings import Settings
from model.rule import Rule

class Interface:
    def read_file(self, file_src):
        """
        Loads the content from a file and scans for certain words. If one of these words is found the string after the
        word will be stored into a grammar or settings object.
        :param file_src: String contains the path to a file
        :return: list which contains the grammar and settings object
        """
        with open(file_src, "r") as fobj:
            grammar = Grammar()
            settings = Settings()
            for line in fobj:
                rhs = None #right-hand-side of a rule
                lhs = None #left-hand-side of a rule
                state = "lhs"
                words = line.rstrip().split()
                for word in words:
                    if (words.index(word) == 0 and word == "axiom:"):
                        words.remove(word)
                        grammar.axiom = ' '.join(words)
                    elif (words.index(word) > 0 and words[0] == "angle_z:"):
                        settings.angle_z_min = int(words[1])
                        settings.angle_z_max = int(words[3])
                    elif (words.index(word) > 0 and words[0] == "angle_y:"):
                        settings.angle_y_min = int(words[1])
                        settings.angle_y_max = int(words[3])
                    elif (words.index(word) > 0 and words[0] == "angle_x:"):
                        settings.angle_x_min = int(words[1])
                        settings.angle_x_max = int(words[3])
                    elif (words.index(word) > 0 and words[0] == "branch-shortening:"):
                        settings.branch_min = float(words[1])
                        settings.branch_max = float(words[3])
                    #elif (words.index(word) > 0 and words[0] == "num_sides:"):
                        #grammar.num_sides = int(words[1])
                    elif (words.index(word) > 0 and words[0] == "base_radius:"):
                        settings.base_radius = float(words[1])
                    elif (words.index(word) > 0 and words[0] == "rules:"):
                        if(state == "lhs"):
                            lhs = word
                            if(lhs not in grammar.variables):
                                grammar.variables.add(lhs)
                            state = "rhs"
                            continue
                        if(state == "rhs" and word != "->"):
                            rhs = word
                            if("," in rhs):
                                rhs = rhs.replace(",", "")
                            grammar.rules.add(Rule(lhs,rhs))
                            state = "lhs"
                    elif (words.index(word) > 0 and words[0] == "generations:"):
                        settings.generations = int(words[1])
                    elif (words.index(word) > 0 and words[0] == "base_length:"):
                        settings.base_length = float(words[1])
                    elif (words.index(word) > 0 and words[0] == "bark_texture:"):
                        settings.bark_path = words[1]
                    elif (words.index(word) > 0 and words[0] == "leaf_texture:"):
                        settings.leaf_path = words[1]
            return [grammar, settings]

    def write_file(self, file_src, turtle_string):
        with open(file_src, "a") as fobj:
            fobj.write("\n"+turtle_string)