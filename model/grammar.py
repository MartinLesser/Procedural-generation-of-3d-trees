class Grammar:
    def __init__(self):
        self.variables = set()
        self.rules = set()
        self.axiom = ""

    def print_grammar(self):
        print("Variables: "),
        for variable in self.variables:
            print(variable + ", "),
        print
        print("Axiom: " + self.axiom)
        print("Rules: "),
        for rule in self.rules:
            print(rule.lhs + " -> "),
            print(rule.rhs + ", "),
        print

    def search_rule_lhs(self, lhs):
        result = []
        for rule in self.rules:
            if(rule.lhs == lhs):
                result.append(rule)
        assert len(result) != 0, "Searched for " + lhs
        return result

    def test_search_rule_lhs(self, lhs):
        for rule in self.search_rule_lhs(lhs):
            for rhs in rule.rhs:
                print(rhs + " "),
            print
