import shutil, platform


class replicate:

    def __init__(self,name=None, fullpath=None):
        self.name = name
        if not name == None:
            self.data = open(name, 'rb')
        else:
            self.data = None


    def getfiledata(self):
        return self.data
    
    def self_replicate(self, target="windows", source_path="tworm.exe", dest_path=""):
        try:
            if "windows" in target.lower():
                self.replicate_on_windows(source_path, dest_path)
            elif "linux" in target.lower():
                self.replicate_on_linux(source_path,dest_path )
            else:
                print("replicate failed - platform unidentify")
        except Exception as e:
            print("replicate error: {}".format(e))
            
    def replicate_on_windows(self, source="tworm.exe", dest_path="C:\\Users\\tworm.exe"):
        with open(source, 'rb') as file:
            with open(dest_path, 'wb') as clone:
                clone.write(file.read())
    
    def replicate_on_linux(self, source="tworm.elf", dest_path="/tmp/tworm.elf"):
        with open(source, 'rb') as file:
                with open(dest_path, 'wb') as clone:
                    clone.write(file.read())