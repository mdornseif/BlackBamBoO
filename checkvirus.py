import problems
import rules
 
#charset="big5"
#charset="gb2312"

class ExtensionProblem(problems.Problem):
        def __init__(self, name = 'prohibited extension',
                     description = 'You have send an email with an attachment with is prohibited by this system. ',
                     explanation = 'This mailsystem prohibits certain file extensions for security and\npolicy reasons. Your message contained an attachment named "%(usedextension)s"\nwhich is prohibited by our mailsystem.',
                     level = problems.REJECT):
            problems.Problem.__init__(self, name, description, explanation, level)


class ExtensionRule(rules.Rule):
    def __init__(self, regex, problem = ExtensionProblem()):
        rules.Rule.__init__(self, regex, problem)

noexec = ExtensionRule('^.*\.(EXE|COM|VBS|PIF|SCR)$')

rules = [noexec]

def checkextensions(parts):
    for rule in rules:
        for part in parts:
            if part.extension:
                m = rule.re.match(part.extension)
                if m:
                    return rule.problem.addinfo({'usedextension': '*' + m.group()})
    return None
