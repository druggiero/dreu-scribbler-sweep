from Behavior import Behavior
#if we don't have time to do this properly then just have it get a read on the green sign and mark the room as explored.
#So ExploreRoom gets called as soon as the robot decides if it needs to explore the room,
#which means it still has it's right side to the wall. First it must 'get in front'

class ExploreRoom(Behavior):
    
            
	#explores a room, looks for green sign. signSize is the size of the pink sign it saw
    def execute(self):
        signSize = self.robot.getSignSize()
        self.robot.robo.beep(1,900)
        self.faceRoom(signSize)
        explored = False
        print(str(self.robot) + " is exploring room")
        while(explored == False):
            boxCoor = self.findGreen()
            if boxCoor != []:
                #green sign found, room explored.
                explored = True
            else:
                self.robot.robo.turnRight(0.2,0.3)
        self.robot.robo.turnLeft(1,1) # not good, but should end up looking down the hallway again as if the robot left room and turned right
        
    def faceRoom(self,signSize):
        #time = signSize something something. Basically want the time it moves forward to depend on how close the pink sign is. How many pixels it sees
        time = 1
        self.robot.robo.forward(1,time)
        self.robo.robo.turnRight(1,1) # eehhh
        
        
    def findGreen(self):
        pic = self.robot.robo.takePicture()
        bw = self.robot.robo.signReader.bwConverter(pic, "green")   
        bwBlob = self.robot.robo.signReader.normalize(bw, 0)
        coords = self.robot.robo.signReader.squarify(bwBlob)
        bigBox = self.robot.robo.signReader.findBiggestBoxes(coords, "box")
        return bigBox
        
  
           
          