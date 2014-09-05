from Myro import *
import FindSign82
from timeit import default_timer #debug

#have not yet figured out how to deal with not seeing the green sign at first

findSign = FindSign82

def main():
    timer = default_timer()
    #tester()
    #practice()
    
    small = calibrate("small", 3)
    big = calibrate("big", 3)
    #small = 17
    #big = 36
    aAndM(look(), small, big)
    print("getInFront: main: program took", default_timer - timer)

def look():
    setPicSize("small")
    pic = takePicture()
    show(pic) #debug
    bw = findSign.bwConverter(pic, "green")   
    show(bw) #debug
    #print("look:", findSign.getBlobs(bw)[1])
    bwBlob = findSign.normalize(bw, 0)
    #show(bwBlob) #debug
    coords = findSign.squarify(bwBlob)
    bigBox = findSign.findBiggestBoxes(coords, "box")
    goodLook = makePicture(getWidth(bwBlob), getHeight(bwBlob))
##     debug = findSign.makeNewPhotoCopy(bw)
##     show(debug)
##     i = 0
##     while findSign.inRange(i, coords):
##         box = findSign.boxAtIndex(i, coords)
##         findSign.drawBox(debug, box, makeColor(0, 255, 0))
##         i = i+4
##     print(coords)
##     wait(3)    
    show(goodLook)
    findSign.drawBlackRect(goodLook, [0, 0, getWidth(goodLook), getHeight(goodLook)])
    findSign.drawRect(goodLook, bigBox, makeColor(255, 255, 255))
    #print("look:", findSign.getBlobs(bwBlob)[1])
    return goodLook
    
def reverseTurnToTarget(middle, target, smallTurnAmt, bigTurnAmt):
    off = dD(middle, target)
    print("turnToTarget: off by ", off)
    bigTurns = round(off/bigTurnAmt)
    print("turnToTarget:", middle, target, off, bigTurns)
    #beep(1, 800)
    myTurnRight("big", -bigTurns)
    #beep(1, 600)
    smalloff = off%bigTurnAmt
    print("turnToTarget: off, ", off, "bigTurnAmt", bigTurnAmt, "smalloff", smalloff)
    smallTurns = round(smalloff/smallTurnAmt)
    #beep(1, 1200)
    myTurnRight("small", -smallTurns)
    #beep(1, 1000)
    print("turnToTarget: smallTurns is ", smallTurns) #debug
    
    
def turnToTarget(middle, target, smallTurnAmt, bigTurnAmt): #turns so that the target is in the middle of the picture
    off = dD(middle, target)
    print("turnToTarget: off by ", off)
    bigTurns = round(off/bigTurnAmt)
    print("turnToTarget:", middle, target, off, bigTurns)
    #beep(1, 800)
    myTurnRight("big", bigTurns)
    #beep(1, 600)
    smalloff = off%bigTurnAmt
    print("turnToTarget: off, ", off, "bigTurnAmt", bigTurnAmt, "smalloff", smalloff)
    smallTurns = round(smalloff/smallTurnAmt)
    #beep(1, 1200)
    myTurnRight("small", smallTurns)
    #beep(1, 1000)
    print("turnToTarget: smallTurns is ", smallTurns) #debug

def checkForWalls(pic, smallTurn, bigTurn, smallForward): #returns 0 if there are walls and adjusts, returns 1 if no walls
    checkAmt = 150
    width = getWidth(pic)
    middle = width/2
    target = width-checkAmt
    off = dD(middle, target)
    print("checkForWalls: off", off)
    print("checkForWalls: turning first time")
    turnToTarget(middle, target, smallTurn, bigTurn) #turns right and looks out of the corner of its eye
    pic = look()
    if setTarget(pic) == width:
        print("checkForWalls: saw wall to right, readjusting")
        print("checkForWalls: undoing last turn")
        reverseTurnToTarget(middle, target, smallTurn, bigTurn) #undoes the last turn
        print("checkForWalls: last turn undone")
        print("checkForWalls: turning left 90 deg")
        turnToTarget(360, 0, smallTurn, bigTurn) #turns 90 deg left
        print("checkForWalls: turned left 90 deg")
        print("checkForWalls: going forwards")
        for i in range(int(smallForward)):
            forward(1, .1)
        print("checkForWalls: turning right 90 deg")    
        turnToTarget(0, 360, smallTurn, bigTurn) #turns 90 deg right
        print("checkForWalls: turned right 90 deg")
        return 0
    print("checkForWalls: undoing last turn")
    reverseTurnToTarget(middle, target, smallTurn, bigTurn) #undoes the last turn
    print("checkForWalls: last turn undone")
    target = checkAmt
    off = dD(middle, checkAmt)
    show(takePicture())
    turnToTarget(middle, target, smallTurn, bigTurn) #turns left and looks out of corner of eye
    pic = look()
    if setTarget(pic) == width:
        print("checkForWalls: saw wall to left, readjusting")
        print("checkForWalls: undoing last turn")
        reverseTurnToTarget(middle, target, smallTurn, bigTurn) #undoes the last turn
        show(takePicture())
        print("checkForWalls: last turn undone")
        print("checkForWalls: turning right 90 deg")    
        turnToTarget(0, 360, smallTurn, bigTurn) #turns 90 deg right
        print("checkForWalls: turned right 90 deg")
        print("checkForWalls: going forwards")
        for i in range(int(smallForward)):
            forward(1, .1)
        print("checkForWalls: turning left 90 deg")
        turnToTarget(360, 0, smallTurn, bigTurn) #turns 90 deg left
        print("checkForWalls: turned left 90 deg")
        return 0
    print("checkForWalls: undoing last turn")
    reverseTurnToTarget(middle, target, smallTurn, bigTurn) #undoes the last turn
    show(takePicture())
    print("checkForWalls: last turn undone")
    print("checkForWalls: safe to go!")
    return 1
        

    
def aAndM(pic, smallTurnAmt, bigTurnAmt): #short for analyzeAndmove: figures out how to move so the robot is right on.
    charge = 0
    middle = getWidth(pic)/2
    target = setTarget(pic)
    off = dD(middle, target)
    calibCounter = 0
    print("aAndM:", off)
    while charge == 0:
        while abs(off) > 30:
            target = setTarget(pic)
            if target != getWidth(pic):
                calibCounter = calibCounter + 1
            else:
                calibCounter = 0
            if calibCounter > 3 and off > 50 or calibCounter > 5:
                print("Not finding target: going to calibrate")
                smallTurnAmt = calibrate("small", 2)
                if smallTurnAmt == 0:
                    print("I need some help with my calibration!!")
                    smallTurnAmt = 30
                bigTurnAmt = calibrate("big", 2)
                if bigTurnAmt == 0:
                    print("I need some help with my calibration!!")
                    bigTurnAmt = 30
                calibCounter = 0
                pic = look()
                target = setTarget(pic)
            print("calibCounter is", calibCounter)
            turnToTarget(middle, target, smallTurnAmt, bigTurnAmt)
            pic = look()
            off = dD(middle, setTarget(pic))
            
        print("\n aAndM: Checking for walls! \n")    
        charge = checkForWalls(pic, smallTurnAmt, bigTurnAmt, 2)
        pic = look()
        off = dD(middle, setTarget(pic))    
    
    beep(1, 1800)
    print("CHAAAARGE!")
    forward(1, 5)
    print("aAndM: lost sign. pixel amount is:", findSign.getBlobs(pic)[0])
    
def myTurnRight(size, amount):
    for i in range(abs(int(amount))):
        print("myTurnRight: completed", size, "for", amount)
        if size == "big":
            if amount>0:
                turnRight(.5, .1)
            if amount<0:
                turnRight(-.5, .1)
        if size == "small":
            if amount>0:
                turnRight(.1, .1)
            if amount<0:
                turnRight(-.1, .1)
        
     
def dD(target, actual): #Short for determineDistance: returns how far to the right actual is from the target.
    return (actual-target)

def setTarget(bw): #returns the x position of the target in a black and white photo of -1 if the target is not seen
    bwCopy = findSign.makeNewPhotoCopy(bw) #debug
    show(bwCopy) #debug
    if findSign.getBlobs(bw)[0]>1220: #is the white space big enough to be a target?
        target = findSign.getBlobs(bw)[1]
        findSign.makeX(bwCopy, 2, target, getHeight(bwCopy)/2, makeColor(0, 255, 0)) #debug 
    else:
        target = getWidth(bw) #the target is lost
        print("setTarget: could not find target!")
        print("setTarget: blobCount too low", findSign.getBlobs(bw)[0])
    
    print("setTarget: blobCount", findSign.getBlobs(bw)[0]) #debug    
    return target  
    
def calibrate(size, amnt): #calibrates the motors to turn a specific amount
    diffs = []
    for i in range(amnt):
        pic = look()
        target_one = setTarget(pic)
        print("calibrate: here's where the target is:", target_one)
        if target_one != getWidth(pic):
            if target_one > getWidth(pic)/2:
                myTurnRight(size, 1)
            else:
                myTurnRight(size, -1)
            pic = look()    
            target_two = setTarget(pic)
            if target_two != getWidth(pic):
                if (abs(target_two-target_one) < 100):
                    diffs.append(abs(target_two-target_one))
                    print("calibrate: change was", abs(target_two-target_one))
                else:
                    print("calibrate: change was too big:", abs(target_two-target_one) )
            else:
                print("calibrate: can't find the target!")    
        else:
            print("calibrate: can't find the target!")
            
    print("")        
    if len(diffs)>0:
        turnAmnt = avgList(diffs)
        print("calibrate:", size,"turn amount is", turnAmnt)
    else:
        print("calibration: failed!")
        print("")
        return 0
    print("")
    return turnAmnt
    
def avgList(aList):
    counter = 0
    for i in aList:
        counter = counter + i
    return (counter/(len(aList)))        
             
            
def practice():
    pic = look()
    show(pic)
    target = setTarget(pic)
    print("practice: target is ", target)
    print("practice: middle is", getWidth(pic)/2)
    
    turnToTarget(360, 0, 12, 36)
    
    print("practice: moved")
    newpic = look()
    newtarget = setTarget(newpic)
    print("practice: target is now", newtarget)
    show(newpic)
    print("practice: change was:", newtarget-target)
    
def tester():
    print("in tester")
    pic = takePicture()
    show(pic)
    myTurnRight("big", 5)
    myTurnRight("small", -1)
    wait(2)
    myTurnRight("big", -5)
    myTurnRight("small", 1)
    pic = takePicture()
    turnToTarget(360, 0, 20, 50)
    wait(1)
    reverseTurnToTarget(360, 0, 20, 50)
    
    show(pic) 
           
main()
