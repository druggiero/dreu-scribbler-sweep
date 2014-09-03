'''IntersectionObject keeps track of whether or not an intersection has been explored,
as well as what robots are current stationed at that intersection (and what other intersections
are within range). Storing this data within the intersection object is part of the system
that emulates robot connection range. 
The robots can just "talk" to the Intersection objects instead of appealing to the controller
to find out what other robots are nearby. Not such a big deal conceptually but
really just a matter of implementation.
'''


class Intersection(object):
    def __init__(self,n, roomOrHall):
        #does the intersection lead into a 'room' or a 'hall' or is it the 'start'?
        self.num = n
        self.kind = roomOrHall
        self.explored = False
        self.beingExplored = False
        self.intersInRange = [self] # can I do this? I think I can. Check later if this causes problems down the road
        self.robotsPresent = []

    def getInRange(self):
        return self.intersInRange

    def addRobot(self, robot):
        #simply adds a robot to the list of robots currently stationed at an intersection
        #this is called by a robot when its location is set with RobotObject.setLocation()
        self.robotsPresent.append(robot)

    def isExplored(self):
        return self.explored
    
    def markAsExploring(self):
        self.beingExplored = True
    
    def getRobots(self):
        #returns list of robots at intersection, used by Robot to find neighboring robots to whom it can send messages 
        return self.robotsPresent
    
    def setAsExplored(self):
        #will be set when robot finishes exploring intersection--when this happens will be determined by main loop I believe
        #tricky part comes when you have hallways and rooms interacting--for rooms it is easy but hallways a bit more complicated
        self.explored = True
        self.beingExplored = False
    
    def setInRange(self,otherIntersection): 
        #this has to be done by hand in controller, one by one. 
        #setting an intersection in range of another will update the range lists of both intersections
        self.intersInRange.append(otherIntersection) 
        otherIntersection.intersInRange.append(self)

    def getNum(self):
        return self.num
        
    def __cmp__(self,otherIntersection):
        if self.num < otherIntersection.getNum():
            return -1
        elif self.num > otherIntersection.getNum():
            return 1
        else:
            return 0
    
    def neighborListToString(self):
        string = ''
        for i in self.intersInRange:          
            string = string +(str(i.getNum())) + ', '
        return string[:-2]
        
    def __str__(self):
        string = "Intersection " + str(self.num) +'. Leads to a ' + str(self.kind) + ", in range of " + self.neighborListToString()
        return(string)
        
    