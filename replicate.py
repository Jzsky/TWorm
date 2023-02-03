import shutil, platform
import os

class replicate:

    def __init__(self,filepath=None):
        if not filepath == None:
            self.data = open(filepath, 'rb')
        else:
            self.data = None


    def getfiledata(self):
        return self.data
    
    def self_replicate(self, target="windows"):
        print("start")
        try:
            if target == "windows":
                self.replicate_on_windows()
            else:
                self.replicate_on_linux()
        except Exception as e:
            print("replicate error: {}".format(e))
            
    def replicate_on_windows(self, source="container/testhello.exe"):
        with open(source, 'rb') as file:
                with open('testhello2.exe', 'wb') as clone:
                    clone.write(file.read())
        print("finished")
    
    def replicate_on_linux(self, source="container/tworm_linux.elf"):
        with open(source, 'rb') as file:
                with open('testhello2.elf', 'wb') as clone:
                    clone.write(file.read())
        print("finished")
        
        
            

# r = replicate()
# r.self_replicate()
        
    