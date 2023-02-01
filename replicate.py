import shutil
import os

class replicate:

    def __init__(self,data=None):
        self.file = data


    def getfile(self):
        return self.file

    def replicate_file(self, path="%temp%", ostype="windows"):
        shutil.copy(__file__, 'temp/copied_script_name.py') 

    def self_replicate(self):
        pass


r = replicate()
r.self_replicate()