#
# Project details are saved as a dictionary
#
#
# currently included
# * List of capsules
# * Main Capsule
# * List of files
# * List of test scripts 

import os.path
def isProject(filename):
    return (os.path.splitext(filename)[1] == '.prj') and Project(filename)

class Project:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            self.capsules = {}
        else:
            details = eval(open(filename).read())
            self.capsules = details['capsules']
    def save(self):
        f = open(self.filename,"w")
        details = {}
        details['capsules'] = self.capsules
        f.write(str(details))
        f.close()
    def addCapsule(self,capsule):
        if capsule not in self.capsuleNames():
            # just add the name to the dictionary
            self.capsules[capsule] = None
    def capsuleNames(self):
        return self.capsules.keys()

