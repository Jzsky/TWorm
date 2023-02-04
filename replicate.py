import shutil, platform


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
            if "windows" in target.lower():
                self.replicate_on_windows()
            elif "linux" in target.lower():
                self.replicate_on_linux()
            else:
                print("replicate failed - platform unidentify")
        except Exception as e:
            print("replicate error: {}".format(e))
            
    def replicate_on_windows(self, source="container/tworm.exe", path_name="C:\\Users\\tworm.exe"):
        with open(source, 'rb') as file:
                with open(path_name, 'wb') as clone:
                    clone.write(file.read())
        print("finished")
    
    def replicate_on_linux(self, source="container/tworm.elf", path_name="/temp/tworm.elf"):
        with open(source, 'rb') as file:
                with open(path_name, 'wb') as clone:
                    clone.write(file.read())
        print("finished")