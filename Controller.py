from Myro import *
from IntersectionObject import Intersection
from RobotObject import Robot

###############################################################################
#All code within this block is to be adjusted for particular experiment/run

#before running put the port number of all robots you intend to use
#comPortList = ['COM41', 'COM44']
comPortList = ['COM44'] 

#make every intersection, specify if it is the start, if it leads to a room, or if it leads to hallway
in0 = Intersection(0,'start')
in1 = Intersection(1,'room')
in2 = Intersection(2,'room')
in3 = Intersection(3,'room')

#manual map buildling right here, neighboring intersections are set manually
in0.setInRange(in1)
in1.setInRange(in2)
in2.setInRange(in3)
in3.setInRange(in0) 

#all intersections placed in intersectionList
#intersection in lowest index ([0]) should be the starting intersection and will be treated as such
intersectionList = [in0,in1,in2,in3]

##############################################################################

#change this so it will keep trying to add robots until it gets all of them. Will require some playing around.
#all robots begin in OFFLINE STATE 
def connectToRobots(comPorts):
    robotList = []
    for i in comPorts:
            rob = Robot(i, len(comPortList))
            robotList.append(rob)
    return robotList
            
robotList = connectToRobots(comPortList)

#sets all robots' position to be at start
for i in robotList:
    i.setLocation(intersectionList[0]) 
    print(str(i) + " is at " + str(i.getLocation()))



###########Algorithm Control begins here, but main loop definition is in the Robot class ############

#suppose it starts by setting first robot's State as explorer
#big while loop that keeps calling main() for each robot, checking statues of the start intersection or something
robotList[0].setState('explorer')
while(True): # while algorithm is still running -- ie, final robot has not yet found exit/start
    robotList[0].main()
