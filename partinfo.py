# information regarding message parts

import os.path

class MessagePart:
    def __init__(self, filename, mimetype = 'unknown', providedFilename = 'none', size = 0):
        self.filename = filename
        self.mimetype = mimetype
        self.providedFilename = providedFilename 
        self.size = size
        self.extension = os.path.splitext(self.filename)[1]

