ADD_HEADER = 1
WARN = 2
REJECT = 3

class Problem:
    def __init__(self, name = '<unset>', description = '', explanation = '', level = REJECT):
        self.name = name
        self.description = description
        self.explanation = explanation
        self.level = level
        self.info = {}

    def addinfo(self, info):
        self.info.update(info)
        return self

    def getDescription(self):
        return self.description % self.info
    
    def getExplanation(self):
        return self.explanation % self.info
    

    def getInfoDict(self):
        return {'name': self.name,
                'description': self.getDescription(),
                'explanation': self.getExplanation()}
