import problems
import re

class Rule:
    def __init__(self, regex, problem = None):
        self.reges = regex
        self.re = re.compile(regex, re.IGNORECASE)
        if not problem:
            problem = problems.Problem()
        self.problem = problem

