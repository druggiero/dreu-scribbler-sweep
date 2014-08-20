from Myro import *
#do I gotta import RobotObect somehow? Don't think so

class Behavior(object):
    """This is a base class which represents movement behaviors."""

    def __init__(self, robotObject):
        self.robot = robotObject
        #like can i reference this shit this way? I'm actually not sure. like do i have to make a new Robot? i don't want to do that./