#The main RobotObject that has primary algorithm loop in Robot.main(). 
#Robot will make decisions on how to act based on available information

from Myro import *
from SignReaderObject import SignReader
#import Behaviors
from Behaviors.Guard import Guard
from Behaviors.FollowWall import FollowWall
from Behaviors.ExploreRoom import ExploreRoom

#Constants for states
OFFLINE = 'offline'
EXPLORER = 'explorer'
IDLE = 'idle'
RESPONDING = 'responding'

#Constants for behaviors
GUARD = 'guard'
WALL = 'follow_wall'
EXPLORE_ROOM = 'explore_room'



class Robot(object):

    def __init__(self, comNum, numRobots, intersectionList):
        self.robotID = comNum
        
        #all myro functions accessed with robo. Makes for some awkward syntax at points unfortunately 
        self.robo = makeRobot("Scribbler",comNum)
        self.robo.setPicSize('small')
        self.robo.takePicture() #for calibration? London's reccomendation. First picture is always dark and he says taking one as soon as the robot turns on would help
        self.signReader = SignReader(self)
        self.numRobots = numRobots
        self.intersectionList = intersectionList
        self.teamSize = 0 #so how many robots have been activated, presumably. may not need? I don't think this gets updated anywhere in my code
        self.neighborList = [] #will be filled with robots at intersections in range when location is set
     
        self.myState =  OFFLINE
        self.myLocation = None #controller sets all Robot locations to starting intersection
        self.hallway = None #if robot is in a hallway, will be stored here. Not sure if necessary, I think I put this here in an attempt to solve hallway problems        

        
        #Imporant information flags that determines how robot acts, some may be set by Behavior objects through setter functions
        self.incomingRequest = None #will be an intersection object when there is unprocessed request or None when no request
        self.suspectedOpening = False #usually turns true when "wall drops away" but may also be useful to set as true when robot exits a room and continues to it's right after taking picture
        self.signSize = 0 #will be set once robot has seen pink size, used by ExploreRoom behavior
        
        #Behavior Variables -- these pass in self so the Behaviors have accsess to both the Myro functions(robo.) and some Robot instance varaibles, see class files
        self.followWallBehavior = FollowWall(self)
        self.guardBehavior = Guard(self)
        self.exploreRoomBehavior = ExploreRoom(self)
    
        
    def callForExplorer(self, intersectionObject): #or potentially intersection index number?? guess it doesn't matter
        #ask for robot explorer to continue ahead
        for i in self.neighborList:
            i.addIncomingRequest(intersectionObject)


    def addIncomingRequest(self, intersectionObject):
        #this is for other robots to call on a robot it is in range of
        #neighboring robots can add requests to other robots when explorer is needed, best robot for the job should respond while others ignore
        self.incomingRequest = intersectionObject
        
    def suspectOpening(self):
        #this function is called by the FollowWall Behavior when it thinks there is an opening
        self.suspectedOpening = True

    def setState(self, newState):
        self.myState = newState

    def setLocation(self, inter):
        #would be called when robot arrives at new place and identifies the intersection number.
        #neighborList construction may have some glitches, I'm not sure. Something seems fishy to me about how it fills the neighbor list
        self.neighborList = [] #empties neighbor list as it must be rebuilt
        self.myLocation = inter
        
        for i in inter.getInRange():
            #for all intersections in range of new location, will get list of robots present
            robotsOnInter = i.getRobots()
            if robotsOnInter != []:
                for j in robotsOnInter:
                    self.neighborList.append(j)
                    if (self not in j.neighborList):
                        j.neighborList.append(self)
        #then finally adds the robot to the intersection's list of robots. does this at end so robot doesn't add itself as neighbor
        inter.addRobot(self) #make sure putting this at the end is the right way to go?

 

    def behave(self, behavior):
        #executes behavior, takes behavior constant as input. used in main Robot loop
        if behavior == GUARD:
            self.guardBehavior.execute()
        elif behavior == WALL:
            self.followWallBehavior.execute()
        elif behavior ==EXPLORE_ROOM:
            self.exploreRoomBehavior.execute()

    
    def getLocation(self):
        return self.myLocation
        
    def getSignSize(self):
        return self.signSize

    def __str__(self):
        #just incase you're printing robots. Right now will print Robot COM## since robotID is just comNum
        string = "Robot " + str(self.robotID)
        return(string)
            
    def main(self): 
        #main is currently designed as loopable in the controller
        #controller iterates through each robot's main in sequence
        #I think that's the only/best way to do it without threading stuff which just sounds annoying
        
        #HEAVILY UNDER CONSTRUCTION, MAIN ALGORITHM IMPLEMENTATION IS HERE
        if self.myState == OFFLINE or self.myState == IDLE: 
            if self.incomingRequest != None:
                if self.myState == OFFLINE:
                    if shouldRespond == True: #checks if any requests for explorers have been made, will only respond if lowest index in queue + a bunch of other conditions I bet
                        self.robo.beep(2,850) #otherwise he doesn't do anything, because he was offline, but: 
                        #if it were just an idle robot that's in middle of group of robots he might send the message on to his neighbors if he didn't meet criteria for responding. 
                        #but like so he knows he's responding but to what? Keep rquest on hand, uses it in alg. hmmm.
                        self.myState = RESPONDING 
                        #might have some conditional for deciding between IDLE and OFFLINE stuff, they are very similar
                    else:
                        #ignores request, stays in guard behavior.
                        self.incomingRequest = None #decides it shouldn't respond, deletes request. awaits next
                        self.behave(GUARD)
                elif self.myState == IDLE:
                    if shouldRespond: #shouldRespond for idle robots is different from shouldRespond for offlines, must check if there are robots behind
                        #find Wall, get on wall.
                        self.myState = RESPONDING
                    else:
                        #send message to robots in range that are not in range of where the message came from. so maybe just robots behind it
                        for i in self.neighborList:
                            #how to decide if location is behind a robot?
                            if i.getLocation()< self.myLocation(): #probably not the best way to do this, just comparing intersection numbers
                                i.addIncomingRequest(self.incomingRequest)                       
                        self.incomingRequest = None
                        self.behave(GUARD)
            else: self.behave(GUARD)

        elif self.myState == EXPLORER or self.myState == RESPONDING:  
            
            if self.suspectedOpening == False:
                self.behave(WALL) #executes one iteration of wall following
                #It should go continuously since other robot's mains have them sitting tight, only one robot is moving at a time
            else:
                #turnright a little bit, search for the pink signm
                signInfo = self.signReader.readPink() # takes picture of pink sign to decide how to act
                #signInfo is a list with [signNumber, center coordinates, boxsize] see SignReaderObjcet line 488
                if signInfo[0] == []: #questionable conditional, might not work as intended
                    #it means the signReader didn't see a sign to read. Either keep looking or decide there isn't an opening
                    self.suspectedOpening = False
                else:    
                    num = signInfo[0]
                    print(num)
                    signNum = num[0]
                    intersection = self.intersectionList[signNum]
                    self.setLocation(intersection)
                    self.signSize = signInfo[2] # should set signSize to number of pixels
                    
                    if intersection.kind == 'start':
                        #send call messsage to intersection0 for all robots in range
                        print(str(self) + " arrived at exit, calling next robot. Going offine.")
                        self.myState == OFFLINE
                        
                    elif intersection.kind == 'room':
                    
                        if intersection.isExplored() == True:
                            print(str(self) + " found explored room #" + str(signNum) +", proceeding ahead")
                            #maybe here is just goes toward the pink sign? to cross the chasm. or just forward
                            self.behave(WALL)
                        
                        elif intersection.isExplored() == False:
                            if self.myState == EXPLORER:
                                print(self.neighborList)
                                if self.neighborList != []: #see if there are robots around it to recieve message
                                    for i in self.neighborList:
                                        i.addIncomingRequest(intersection)
                                    self.robo.forward(1,2) #these commands are meant to get IDLE robot out of the way for responder
                                    self.robo.turnRight(1,1)
                                    self.robo.forward(-1,1)
                                    self.myState == IDLE 
                                else:
                                    self.behave(EXPLORE_ROOM)
                                    self.suspectOpening()# suspectsOpening upon finishing exploration of room as it should look and take a picture
                                    #of coures this means the robot has to end up facing to it's right after finishing exploration
                                    
                            elif self.myState == RESPONDING and signNum == self.incomingRequest.num:
                                 print(str(self) + " responder found target room, commencing exploration")
                                 self.behave(EXPLORE_ROOM)
                                 self.suspectOpening()
                                 
                    elif intersection.kind == 'hall':
                        pass
                        #LAST ROBOT OUT MARKS HALL AS EXPLORED!!!!!!
                        #robot won't mark as explored until it gets called again.
                        #implement hall behavior