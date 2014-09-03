from Myro import *
from IntersectionObject import Intersection
from RobotObject import Robot

###############################################################################
#All code within this block is to be adjusted for particular experiment/run

#before running put the port number of all robots you intend to use
#comPortList = ['COM40','COM41', 'COM42', 'COM44']
comPortList = ['COM40']

#make every intersection, specify if it is the start, if it leads to a room, or if it leads to hallway
in0 = Intersection(0,'start')
in1 = Intersection(1,'room')
in2 = Intersection(2,'hall')
in3 = Intersection(3,'hall')
in4 = Intersection(4,'room')
in5 = Intersection(5,'hall')
in6 = Intersection(6,'room')
in7 = Intersection(7,'room')

#manual map buildling right here, neighboring intersections are set manually
in0.setInRange(in1)
in1.setInRange(in2)
in2.setInRange(in3)
in3.setInRange(in4)
in5.setInRange(in2)
in5.setInRange(in3)
in6.setInRange(in5)
in7.setInRange(in2)
in7.setInRange(in0) 

#all intersections placed in intersectionList which is passed into robots when they are initilized as objects
#thus the robots can consult the list when they arrive at a particular intersection and need to know things about it
#this kind of knowledge about the enviornment lets the robots know if something has been explored or not, a functionality similar to the beacons in the original algorithm
#intersection in lowest index ([0]) should be the starting intersection and will be treated as such
intersectionList = [in0,in1,in2,in3,in4,in5,in6,in7]

##############################################################################

#all robots begin in OFFLINE STATE 
def connectToRobots(comPorts):
    robotList = []
    for i in comPorts:
            rob = Robot(i, len(comPortList), intersectionList)
            robotList.append(rob)
    return robotList
            
robotList = connectToRobots(comPortList)

#sets all robots' position to be at start
for i in robotList:
    i.setLocation(intersectionList[0]) 
    print(str(i) + " is at " + str(i.getLocation()))



###########Algorithm Control begins here, but main loop definition is in the Robot class ############

#starts by setting first robot's State as explorer
#big while loop that keeps calling main() for each robot, also should check if robots have finished (by looking at start intersection?)
robotList[0].setState('explorer')
print(str(robotList[0]) + " is now EXPLORER")
allOffline = False
while(allOffline==False): # while algorithm is still running -- ie, final robot has not yet found exit/start
    stateList = []
    for robot in robotList:
        robot.main()
        stateList.append(robot.myState) #builds statelist every iteration just to check if all robots happen to be offline
    if all(stateList)=='offline': #robots would set themselves to offline once they have found start again
        intersectionList[0].setAsExplored()
        allOffline = True