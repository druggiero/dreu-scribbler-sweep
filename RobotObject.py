#The main RobotObject that has primary algorithm loop in Robot.main(). Robot will make decisions on how to act based on available information

from Myro import *
#import Behaviors
from Behaviors.Guard import Guard
from Behaviors.FollowWall import FollowWall
from Behaviors.ExploreRoom import ExploreRoom

#Constants for states
OFFLINE = 'offline'
EXPLORER = 'explorer'
IDLE = 'idle'
RESPONDING = 'responding'
AWAITING_EXPLORER = 'awaiting_explorer'

#Constants for behaviors
GUARD = 'guard'
WALL = 'follow_wall'
EXPLORE_ROOM = 'explore_room'


#Team Constants
MAX_NUM_AGENTS = 4



class Robot(object):

    def __init__(self, comNum, numRobots):
        self.robotID = comNum
        
        #all myro functions accessed with robo. Makes for some awkward syntax within Behavior classes, but such is life
        self.robo = makeRobot("Scribbler",self.comNum)
        self.robo.setPicSize('small')
        self.robo.takePicture() #for calibration? London's reccomendation. First picture is always dark. look into this.
        
        self.numRobots = numRobots
        self.teamSize = 0 #so how many robots have been activated, presumably. may not need
        self.neighborList = [] #will be filled with robots at intersections in range when location is set
     
        self.myState =  OFFLINE
        self.myLocation = None #controller sets all Robot locations to starting intersection
        

        #Imporant information flags that determines how robot acts, some may be set by Behavior objects through setter functions
        self.incomingRequest = None #will be an intersection object when there is unprocessed request or None when no request
        self.suspectedOpening = False
        
        #Behavior Variables -- these pass in self so the Behaviors have accsess to both the Myro functions(robo.) and some Robot instance varaibles, see class files
        self.followWallBehavior = FollowWall(self)
        self.guardBehavior = Guard(self)
        self.exploreRoomBehavior = ExploreRoom(self)
    
        
    def callForExplorer(self, intersectionObject): #or potentially intersection index number??
        #ask for robot explorer to continue ahead
        for i in self.neighborList:
        	i.addIncomingRequest(intersectionObject)


    def addIncomingRequest(self, intersectionObject):
        #neighboring robots can add requests to other robots when explorer is needed, best robot for the job should respond while others ignore
    	self.incomingRequest = intersectionObject
        
    def suspectOpening(self):
        #this function is called by the FollowWall Behavior when it thinks there is an opening
    	self.suspectedOpening = True

    def setState(self, newState):
        self.myState = newState

    def setLocation(self, inter):
        self.neighborList = [] #empties neighbor list as it must be rebuilt
        self.myLocation = inter
        for i in inter.getInRange():
            #for all intersections in range of new location, will get list of robots present
        	robotsOnInter = i.getRobots()
        	if robotsOnInter != []:
        		for j in robotsOnInter:
        			self.neighborList.append(j) #adds nearby robots to neighborList
                    #I think there will be a bug here, maybe write an "update neighbor list" function
                    #for now just do conditional that checks if self is already in other robot's list
        			if self not in j.neighborList:
                        j.neighborList.append(self) #should add robot to neighborlist of other robots. is there is a risk of adding something twice? must find out. 
       	inter.addRobot(self) #make sure putting this at the end is the right way to go

 

    def behave(self, behavior):
        #executes behavior, takes behavior constant as input. used in main Robot loop
    	if behavior == GUARD:
    		self.guardBehavior.execute()
    	elif behavior == WALL:
    		self.followWallBehavior.execute()
    	elif behavior ==EXPLORE_ROOM:
    		self.exploreRoomBehavior.execute()
 
    
            
    def readIntersection(self):
        #reads the pink sign nearby. muh sweet signReading object
        #needs work. TO DO TO DO TO DO
        pass #lol
        

    def faceWall(self):
        #modify this so it takes the distance away from the intersection sign into account
        #right now this function sucks big time
        #might be included in ExploreRoom behavior, haven't decided yet.
        #will this be the same function for getting the hell out of the way when an explorer is called? I don't know, maybe
        self.robo.forward(1,1.5)
        self.robo.turnRight(1,0.7)
        self.robo.forward(-1,1.6)    
    
    def getLocation(self):
        return self.myLocation

    def exploreRoom():
        #not real, will be incorporated into ExploreRoom Behavior. Ignore this
        self.robo.forward(1,2)
        self.robo.turnLeft(1,1.35)
        self.robo.stop()
        self.robo.wait(1.5)
        self.robo.forward(1,2)

    def __str__(self):
        #just incase you're printing robots. Right now will print Robot COM## since robotID is just comNum
        string = "Robot " + str(self.robotID)
        return(string)
        
        
    
    def main(self) 
        #main is currently designed as loopable in the controller
        #controller iterates through each robot's main in sequence
        #I think that's the only/best way to do it without threading stuff which just sounds annoying
        
        #HEAVILY UNDER CONSTRUCTION, MAIN ALGORITHM IMPLEMENTATION IS HERE
        if self.myState == OFFLINE: #idle will be very similar?
        	
        	if self.incomingRequest != None:
        		#process request function? Decides if it is appropriate to go
        		if shouldRepond: #NOT REAL YET, MUST WRITE THIS, VERY IMPORTANT ******************
            		#checks if any requests for explorers have been made, will only respond if lowest index in queue + a bunch of other conditions I bet
            		self.myState = RESPONDING # HAHA this will only happen if the robots meets all the conditions for response
            		#otherwise he doesn't do anything, because he was offline, but: 
                    #if it were just an idle robot that's in middle of group of robots he might send the message on to his neighbors if he didn't meet criteria for responding. 
            		#but like so he knows he's responding but to what? Keep rquest on hand, uses it in alg. hmmm.
                    #might have some conditional for deciding between IDLE and OFFLINE stuff, they are very similar
            	else:
            		self.incomingRequest = None #decides it shouldn't respond, deletes request. awaits next
            		self.behave(GUARD)
            else: self.behave(GUARD)

        elif self.myState == EXPLORER: # here's the fun part.
            print("yo we explorer now")
        	if self.suspectedOpening == False:
        		self.behave(WALL) #executes one iteration of wall following
                #I think it should go continuously since other robot's mains have them sitting tight, only one robot is moving at a time
        	else:
        		pass # but really takes picture of pink sign to decide how to act

        elif self.myState == IDLE: 
            pass
            #hmm, how is different from being OFFLINE? I mean they are polling in a similar way. might even be able to combine them, have another 
            #condition that asks if IDLE or OFFLINE and does something different then. In fact, that's what I'm going to do.
            #like idle and offline might have different needs in trying to "get on the wall, yeah?" Or who they pass messages to
        elif self.myState == RESPONDING:
            #will just do wall following until it arrives at intended intersection
            pass
        elif self.myState == AWAITING_EXPLORER:
            #not sure if this is even necessary. In any case it isn't moving, but must decide if this requires special treatment.
            #when will the waiting robot get out of the way? Maybe after it has called for an explorer. hmm 
            pass