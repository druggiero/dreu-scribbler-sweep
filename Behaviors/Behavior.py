from Myro import *
#do I gotta import RobotObect somehow? Don't think so

class Behavior(object):
    """This is a base class which represents movement behaviors."""

    def __init__(self, robotObject):
        self.robot = robotObject
        