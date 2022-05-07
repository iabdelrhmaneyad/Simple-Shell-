from asyncio.windows_events import NULL
from importlib.resources import contents
import os
import sys


#help function
class Path:
    def help(self,command=None):
    #dictionary about the commands with small brief about them
        self.help_list={"cd":"Change the current default directory to.\n     If the argument is not present, report the current directory.\n     If the directory does not exist an appropriate error should be reported.\n",
               "clear":"Clear the screen",
               "dir":"List the contents of directory and subdirectories in a directory.",
               "quit":"Quit the shell.",
               "copy":"Copies one or more files to another location",
               "del":"Deletes one or more files.",
               "help":"Provides Help information for commands.",
               "md":"Creates a directory.","rd":"Removes a directory.",
               "rename":"Renames a file.","type":"Displays the contents of a text file.",
               "import":"import text file(s) from your computer.",
               "export":"export text file(s) to your computer."
               }
            
        if self.command in self.help_list :
            print(self.command + " - "+self.help_list[command])
    
        elif self.command==None:
            for commnd , description in self.help_list.items(): 
                print("{} - {}".format(commnd,description))



    def __init__(self):
        print("(c) Shell project. All rights reserved to (Muharram Othman, Abdelrahman Eyad, Maryam).\n\n")
        while True:
            #Get input from user whatever the command lower or upper case (not key sensetive)
            self.path = input('F:\>').lower().split()
            #if the user doesn`t write any command and press enter the shell will go in new line waiting for a command to execute
            if len(self.path) == 0:
                continue
            #if the user type "Quit" the shell will quit 
            if self.path[0] == "quit":
                quit()
            
                
        
            #if the user type "Clear" the shell will clear the screen
            elif self.path[0] == "clear":
                os.system("cls")
                print("(c) Shell project. All rights reserved to (Muharram Othman, Abdelrahman Eyad, Maryam).\n")
        
            #if the user type "Help" by default the shell will say to you all the commands
            elif self.path[0] == "help":
                if len(self.path) == 1:
                    self.help()
            #but if the user give another attribute the shell will give a small brief about the specific attribute
                elif len(self.path) > 1:
                    if self.path[1] == "cd":
                        self.help("cd")
                    elif self.path[1] == "clear":
                        self.help("clear")
                    elif self.path[1] == "dir":
                        self.help("dir")
                    elif self.path[1] == "copy":
                        self.help("copy")
                    elif self.path[1] == "quit":
                        self.help("quit")
                    elif self.path[1] == "type":
                        self.help("type")
                    elif self.path[1] == "rd":
                        self.help("rd")
                    elif self.path[1] == "del":
                        self.help("del")
                    elif self.path[1] == "help":
                        self.help("help")
                    elif self.path[1] == "md":
                        self.help("md")
                    elif self.path[1] == "rename":
                        self.help("rename")
                    elif self.path[1] == "import":
                        self.help("import")
                    elif self.path[1] == "export":
                        self.help("export")
                    
            #if the user give unvalid command the shell will give a message that the command is not recognized 
            else:
                print('"{}" is not recognized as an internal or external command\n'.format(self.path[0]))



class Virtual_Disk:
        def initialize(self,name):
            if os.path.exists(name):
                self.file = open(name,"rwb")
                Mini_FAT.ReadFat()
                # Thec fill exist
                # // calls the method from the Mini_FAT class to read the fat from the virtual disk.
            else :
                self.file = open(name,"rwb")
                Mini_FAT.PrepareFAT()
                Mini_FAT.WriteFat()
        def WriteCluster(self,ClusterIndex, b = [None for _ in range(1024)]):
            self.file.seek(ClusterIndex*1024,0) # 0: means your reference point is the beginning of the file https://stackoverflow.com/questions/11696472/seek-function
            self.file.write(bytes(bytearray(b))) #covert the list to bytes and write in file
            self.file.flush()

        def ReadCluster(self,ClusterIndex):
            self.file.seek(ClusterIndex*1024,0)
            return self.file.read(1024)
       










class Mini_FAT (Virtual_Disk):
    fat = [None for _ in range(1024)]
    def PrepareFAT(self):
        for i in range(0,1024):
            if i == 0 or i == 4:
                self.fat[i]=-1
            elif i == 1 or i== 2 or i ==3:
                self.fat[i] = i+1
            else:
                self.fat[i] = 0    
    
    def check_clusterIndex(self,clusterIndex):
        if self.fat[clusterIndex]==0:
            return clusterIndex
        else:
            return -1 
    # we add a method to print the index of avalivble cluster 
    def index_available_cluster(self):
        isEmpty=False
        for num ,cluster in  zip(range(0,1024),self.fat):
            if cluster ==0:
                isEmpty=True
                return num
            else:
                isEmpty=False
        if isEmpty==False:
            return -1
    
    def printFAT(self):
        print(self.fat)
        
    def setFat(self,arr):
        self.fat = arr
    #|||
    # 4-A method for getting a cluster pointer it takes the cluster number which you will use it as an index to a FAT array item to get the value
    def get_ClusterPointer(self,clusterIndex):
        ClusterPointer=[]
        if self.fat[clusterIndex]==0 :            # if the cluster is empty 
            return 0
        elif self.fat[clusterIndex]==-1:
            return -1                               # if it is full and it the the end of the content 
        else:
            while True:
                ClusterPointer.append(clusterIndex)#5
                clusterIndex = self.fat[clusterIndex]
                if self.fat[clusterIndex]==-1 :
                    ClusterPointer.append(clusterIndex)
                    break
        return ClusterPointer
                      

    #VVV
    def set_ClusterPointer(self,clusterIndex,pointer):
        self.fat[clusterIndex] = pointer
    
        
    def get_emptyCluster(self):
        for i in range(1024):
            if self.fat[i] == 0:
                return i
        return -1
    
    def WriteFat(self):
        for i in range(1,5):
            self.WriteCluster(i,self.fat)
    #loop from 1 to 5 
    def ReadFat(self,ClusterIndex):
        self.ReadCluster(ClusterIndex)    



class Directory_Entry:
    dir_name = [None for _ in range(11)]
    dir_attr = None
    dir_empty = [None for _ in range(12)]
    dir_firstCluster = None
    dir_filesize = None
    
    def __init__(self):
        pass
    
    def __init__(self,name,dir_attr,dir_firstCluster):
        self.dir_attr = dir_attr
        if self.dir_attr == '0x0':
            fileName = name.split('.')
            self.assignFileName(fileName[0].split(),fileName[0].split())
        elif self.dir_attr == '0x10':
            self.assignDIRName(name.split())
        self.dir_firstCluster = dir_firstCluster    
    
     
    def assignFileName(self,name,extension):
        if len(name) <= 7 and len(extension) == 3:
            pos = 0
            for i in range(len(name)):
                pos+=1
                self.dir_name[i] = name[i]
            pos+=1 # to complet to the original size and put the dot 
            self.dir_name[pos] = '.'
            for i in range(len(extension)):
                pos+=1
                self.dir_name[pos] = extension[i]

            for i in range(pos+1,len(self.dir_name)): # to comple the rest of with withe spaces 
                self.dir_name[i] = ' '
        else:
            for i in range(7):
                self.dir_name[i] = name[i]
            self.dir_name[7] = '.'
            pos = 8
            for i in range(0,len(extension)):
                self.dir_name[pos] = extension[i]
                pos+=1
    
    
    def assignDIRName(self,name):
        if len(name) <= 11:
            pos = 0
            for i in range(len(name)):
                pos+=1
                self.dir_name[i] = name[i]
            for i in range(pos+1,len(self.dir_name)):
                self.dir_name[i] = ' '
        else:   # to handell the case that the director name the more than 11 char, so it's keep 11 char of the name only
            pos = 0
            for i in range(11):
                pos+=1
                self.dir_name[i] = name[i]
                
class Directory(Directory_Entry):
    dirFiles = []
    
    def __init__(self, name, attr, firstCluster, pa):
        super().__init__(name, attr, firstCluster)
        self.parent = Directory()
        if pa != None:
            self.parent = pa
        
    def updateContent(self,d = Directory_Entry()):
        index = self.searchDirectory(d.dir_name)
        if index!=-1:
            self.dirFiles.pop(index)
            self.dirFiles.insert(index,d) 
               
    def getDirectoryEntry(self):
        me = Directory_Entry(self.dir_name,self.dir_attr,self.dir_firstCluster)
        return me 

                   
    def canAddEntry(self,Direct = Directory_Entry()):
        can = False
        needSize = (len(self.dirFiles)+1)*32
        needClusters = needSize * 1024
        rem = needSize % 1024
        if rem > 0:
            needClusters+=1
        needClusters += Direct.dir_filesize / 1024
        rem2 = Direct.dir_filesize%1024
        
        if rem2 > 0:
            needClusters+=1
        if self.getMySizeOnDisk()+Mini_FAT.get_emptyCluster() > needClusters:
            can = True
        
        return can
    
    
    
    def getMySizeOnDisk(self):
        size = 0
        clusterIndex = self.dir_firstCluster
        next = Mini_FAT.get_ClusterPointer(clusterIndex)
        while clusterIndex != -1:
            size+=1
            clusterIndex = next
            if clusterIndex != -1:
                next = Mini_FAT.get_ClusterPointer(clusterIndex)
        return size  
      
        
        
    def clearDirSize(self):
        clusterIndex = self.dir_firstCluster
        next = Mini_FAT.get_ClusterPointer(clusterIndex)
        if clusterIndex == 5 and next == 0:
            return None
        while clusterIndex != -1:
            temp = clusterIndex
            clusterIndex = next
            Mini_FAT.set_ClusterPointer(clusterIndex,0)
            if clusterIndex != -1:
                next = Mini_FAT.get_ClusterPointer(clusterIndex)



    def deleteDirectory(self):
        if self.dir_firstCluster !=0:
            cluster_index = self.dir_firstCluster
            cluster_pointer = Mini_FAT.get_ClusterPointer(cluster_index)
            while True:
                Mini_FAT.set_ClusterPointer(cluster_index,0)
                cluster_index = cluster_pointer
                if cluster_index != -1:
                    cluster_pointer = Mini_FAT.get_ClusterPointer(cluster_index)
                if cluster_index == -1:
                     break
        '''
         if (this.parent != null)
            {
                int index = this.parent.searchDirectory(new string(this.dir_name));
                if (index != -1)
                {
                    this.parent.DirOrFiles.RemoveAt(index);
                    this.parent.writeDirectory();
                }
            }
            if (Program.current == this && this.parent != null)
            {
                Program.current = this.parent;
                Program.currentPath = Program.currentPath.Substring(0, Program.currentPath.LastIndexOf('\\'));
                Program.current.readDirectory();
            }
            Mini_FAT.writeFAT(); 
        
        '''    

        
        '''
        public int searchDirectory(string name)
        {
            if (name.Length < 11)
            {
                name += "\0";
                for (int index = name.Length + 1; index < 12; ++index)
                    name += " ";
            }
            else
                name = name.Substring(0, 11);
            for (int index = 0; index < this.DirOrFiles.Count; ++index)
            {
                if (new string(this.DirOrFiles[index].dir_name).Equals(name))
                    return index;
            }
            return -1;
        }
        '''
    def searchDirectory(self,Name):
        for i in range(len(self.dirFiles)):
            name = self.dirFiles[i].dir_name
            if name == Name:
                return i
        return -1
    
    
    
    def addEntry(self,direct = Directory_Entry()):
        self.dirFiles.append(direct)
        self.writeDirectory()
    
    
    
    def removeEntry(self,direct = Directory_Entry()):
        self.ReadDirectory()
        index = self.searchDirectory(direct.dir_name)
        self.dirFiles.pop(index)
        self.writeDirectory()
       
        
        
   
    
    
    
    

    def writeDirectory(self):
        dirorfileBYTES = [None for _ in range(len(self.dirFiles) * 32)]
        for i in range(len(self.dirFiles)):
            b = bytearray(self.dirFiles[i])
            j = i*32
            for k in range(len(b)):
                dirorfileBYTES[j] = b[k]
                j+=1
        self.bytesls = bytearray(dirorfileBYTES)       
        clusterFATindex = None
        if self.dir_firstCluster != 0:
            clusterFATindex = self.dir_firstCluster
        else:
            clusterFATindex = Mini_FAT.get_emptyCluster()
            self.dir_firstCluster = clusterFATindex
        lastCluster = -1
        for i in range(len(self.bytesls)):
            if clusterFATindex != -1:
                #$$$$$$$$$$$$$$$ Potinatal Error
                Virtual_Disk.WriteCluster(clusterFATindex,self.bytesls[i])
                Mini_FAT.set_Clu4sterPointer(clusterFATindex,-1)
                if lastCluster != -1:
                    Mini_FAT.set_ClusterPointer(lastCluster,clusterFATindex)
                lastCluster = clusterFATindex
                clusterFATindex = Mini_FAT.get_emptyCluster()
        if self.parent != None:
            self.parent.updateContent(self.getDirectoryEntry())
            self.parent.writeDirectory()
        Mini_FAT.WriteFat()
    '''
           public void readDirectory()
        {
            if (this.dir_firstCluster == 0)
                return;
            this.DirOrFiles = new List<Directory_Entry>();
            int clusterIndex = this.dir_firstCluster;
            int clusterPointer = Mini_FAT.getClusterPointer(clusterIndex);
            List<byte> byteList = new List<byte>();
            do
            {
                byteList.AddRange((IEnumerable<byte>)Virtual_Disk.readCluster(clusterIndex));
                clusterIndex = clusterPointer;
                if (clusterIndex != -1)
                    clusterPointer = Mini_FAT.getClusterPointer(clusterIndex);
            }

            while (clusterPointer != -1);
            for (int index1 = 0; index1 < byteList.Count; ++index1)
            {
                byte[] bytes = new byte[32];
                int index2 = index1 * 32;
                for (int index3 = 0; index3 < bytes.Length && index2 < byteList.Count; ++index2)
                {
                    bytes[index3] = byteList[index2];
                    ++index3;
                }
                if (bytes[0] != (byte)0)
                    this.DirOrFiles.Add(Converter.BytesToDirectory_Entry(bytes));
                else
                    break;
            }
        }

    '''
    def ReadDirectory(self):
        if self.dir_firstCluster != 0:
            self.DirOrFiles = []
            cluster = self.dir_firstCluster
            next = Mini_FAT.get_ClusterPointer(cluster)
                

            ls = []
            while next != -1:
                ls.append(Virtual_Disk.ReadCluster(cluster))
                cluster = next
                if cluster != -1:
                    next = Mini_FAT.get_ClusterPointer(cluster)
            for i in range(len(ls)):
                b = [ None for _ in range(32) ]
                for j,k in zip(range(i*32,len(ls)),range(0,len(b))):
                    b[k] = ls[k]
                if b[0] == 0:
                    break
                self.DirOrFiles.append(bytearray(bytes(b)))
   
    
class File_Entry(Directory_Entry):
    content = None
    parent = Directory()
    def __init__(self, name, attr, firstCluster, Parent = None):
        super().__init__(name, attr, firstCluster)
        self.content = ""
        if Parent != None:
            self.parent = Parent
        
    def GetDirectory_Entry(self):
        me = Directory_Entry(self.dir_name,self.dir_attr,self.dir_firstCluster)
        return me
    
    def writeFileContent(self):
        contentBytes = bytes(self.content)
        bytels = bytearray(contentBytes)
        clusterFATIndex = None
        if self.dir_firstCluster!=0:
            clusterFATIndex = self.dir_firstCluster
        else:
            clusterFATIndex = Mini_FAT.get_emptyCluster()
            self.dir_firstCluster = clusterFATIndex
        lastCluster = -1
        for i in range(len(bytels)):
            if clusterFATIndex != -1:
                Virtual_Disk.WriteCluster(clusterFATIndex,bytels)
                Mini_FAT.set_ClusterPointer(clusterFATIndex,-1)
                if lastCluster !=-1:
                    Mini_FAT.set_ClusterPointer(lastCluster,clusterFATIndex)
                lastCluster = clusterFATIndex
                clusterFATIndex = Mini_FAT.get_emptyCluster()
    
    def readFileContent(self):
        if self.dir_firstCluster !=0:
            self.content = ""
            cluster = self.dir_firstCluster
            next = Mini_FAT.get_ClusterPointer(cluster)
            ls = []
            while next != -1:
                ls.append(Virtual_Disk.ReadCluster(cluster))
                cluster = next
                if cluster != -1:
                    next = Mini_FAT.get_ClusterPointer(cluster)
            self.content = bytes(bytearray(ls))
    
    def deleteFile(self):
        if self.dir_firstCluster!=0:
            cluster = self.dir_firstCluster
            next = Mini_FAT.get_ClusterPointer(cluster)
            while cluster != -1:
                Mini_FAT.set_ClusterPointer(cluster,0)
                cluster = next
                if cluster !=-1:
                    next = Mini_FAT.get_ClusterPointer(cluster)
        if self.parent != None:
            index = self.parent.searchDirectory(self.dir_name)
            if index != -1:
                self.parent.dirFiles.pop(index)
                self.parent.writeDirectory()
                Mini_FAT.WriteFat()


        
            
    
        
main = Path()
