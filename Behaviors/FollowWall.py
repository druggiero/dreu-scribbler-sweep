from Behavior import Behavior

class FollowWall(Behavior):

    def execute(self):
    	self.followWall()

    def followWall(self):
        self.obsList = self.robot.robo.getObstacle()  #this is pretty ugly syntax but I think it works
        print(self.obsList)
        if self.obsList[2]<=640:
            print('Suspected opening, checking again')
            self.robot.robo.stop()
            if self.doubleCheck() ==True:
            	#DECIDE HOW YOU ARE HANDLING THIS
                self.robot.robo.beep(1.5, 850) #does calling robot like this even work or even make sense.
                self.robot.suspectOpening() #flags suspectedOpening instance variable as true for next iteration
                #end function here, main alg decides what's next, finds intersection #            
                return()
                    
        if(self.obsList[2]<1920 and self.obsList[2]>640):
            self.robot.robo.motors(0.4,0.2)
            print("turning right")
        if(self.obsList[2]>=1920 and self.obsList[2]<=3840):
            self.robot.robot.motors(0.3,0.3)
        if(self.obsList[2]>3840):
            self.robot.robo.motors(0.2,0.4)
            print("turning left")

    def doubleCheck(self):
        self.obsList = self.robot.robo.getObstacle()
        print(self.obsList[2])
        if self.obsList[2]<640:
            print("Checked it twice, I believe there is an opening")
            return True
        else:
            print('false alarm')
            return False
        