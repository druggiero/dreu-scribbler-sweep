from Myro import *
from timeit import default_timer #debug

def main():
    print(findRobots())


def isGreen(R,G,B):
    if ((R<190 and G>99 and B>80 and G>(R+32)) or (G<100 and G>50 and (G>(R+9) and G>(B+9)) or (G>(R+30) and G>(B-6))) ): #These define the colors. The values can be changed for better recognition
        return True

def isNewPink(R,G,B):
    if ((R>82 and G<190 and B<210 and R>(G+32) and R>(10+B)) or (R>60 and R<125 and G<190 and B<210 and R>(G+31) and R>(B))): #CHANGER 100 170 210.100190210
        return True

def setColorN(pixel, color): #dependencies: isPink, isYellow, isGreen. Converts a pixel to b&w based on color.
    rgb = getRGB(pixel)
    R = rgb[0]
    G = rgb[1]
    B = rgb[2]
    newrgb = [0, 0, 0]
    
    if color=="pink":
        if isPink(R,G,B):
            newrgb = [255, 255, 255] #white
            
    if color=="yellow":
        if isYellow(R,G,B):
            newrgb = [255, 255, 255] #white
            
    if color=="green":  
        if isGreen(R,G,B):
            newrgb = [255, 255, 255]
            
    if color=="new pink":
        if isNewPink(R,G,B):
            newrgb = [255, 255, 255] 

    return newrgb #makes a pixel white if it is the given color
  
#AC  
def bwConverter(p, colorfind): #depends on setColorN #converts picture to black and white based on pink and blobs it blobAmount
    blackwhite = makePicture(getWidth(p), getHeight(p))
    for i in range(getWidth(p)):
        for j in range(getHeight(p)):
            pix = getPixel(p, i, j)
            color = setColorN(pix, colorfind) #converts to black&white based on pink (or other color chosen)
            if (color != None):
                setColor(getPixel(blackwhite, i, j), makeColor(color[0], color[1], color[2]))       
    #show(blackwhite) #debug
    #wait(1) #debug
    #show(blackwhite)
    return blackwhite
#AC

def getBlobs(blbpic): #Takes a b&w picture and returns the number of white pixels, avg x value, and avg y value of those pixels
    white = 0
    total_x = 0
    total_y = 0
    for i in range(getWidth(blbpic)):
        for j in range(getHeight(blbpic)):
            if getRGB(getPixel(blbpic, i, j))==(255,255,255):
                white = white + 1
                total_x = total_x + i
                total_y = total_y + j
    if white==0:
        #print("nah blob yo") I wasn't quite sure what this does, but it says there's no blob when there is one so I commmented it out.
        white =1
    return white, int(total_x/white), int(total_y/white) 
     
#AC 
def normalize(p, pixnum): #blobs a black and white photo (p) pixnum amount. May not be perfect. No loger rewrites over the photo. Dependencies: none   
    newp = makeNewPhotoCopy(p)
    if pixnum == 0:
        return newp
    
    for i in range(0,getWidth(newp)-1,pixnum):
        for j in range(0,getHeight(newp)-1,pixnum):
            black = 0
            white = 0
            pixels = []
            for x in range(pixnum):
                for y in range(pixnum):
                    pixels.append(getPixel(newp, i+x, j+y))
            for pix in pixels:
                if (getRGB(pix) == (255,255,255)):
                    white = white + 1
                else:
                    black = black + 1
            if(white < black):
                for pix in pixels:
                    setColor(pix, makeColor(0,0,0))
            else:
                for pix in pixels:
                    setColor(pix, makeColor(255,255,255))
    return newp

def decodeLines(pic, blb, avX): #uses a line of sight (avX), a color picture to read the binary (pic), a b&w picture differentiate between the lines and the sign (bw) (used to include signColor but it was never used so it was deleted as a parameter.) Returns the binary interpretation of the sign in a list. It reads top to bottom.
    number=[] #holds the binary interpretation of the sign
    bands=[] #[signstart, signend, band1start, band1end, band2start, band2end,...] just the y coordinates
    done=0 #Have I found all the bands and the sign?
    green = makeColor(0, 255, 0)
    blbMark = makeNewPhotoCopy(pic) #debug
    y=0
    print("decodeLines: This is the picture I am using.") #debug
    show(blb) #debug
    #wait(1) #debug
    print("decodeLines: This is where I will show what I'm doing.") #debug
    show(blbMark) #debug
    #wait(1) #debug
    print("decodeLines: My line of sight is ", avX) #debug
    #makeX(blbMark, 1, avX, 0, green) #debug
    
    while len(bands)==0: #has not found the top of the sign
        pixel = getPixel(blb, avX, y)#defines the pixel we're looking at
        bw = getRed(pixel)#uses the getRed function to see if the pixel is white
        if bw==255:
            bands.append(y)
            print("decodeLines: Found top of sign at ",y) #debug
            makeX(blbMark, 1, avX, y, green) #debug
        y = y+1
        if y > getHeight(pic):
            print("decodeLines: FAILED: could not find top of sign") #debug
            return [-1]

    y = getHeight(pic)
    while len(bands)==1: #while I've found the top of the sign but not the bottom
        pixel = getPixel(blb, avX, y)
        bw = getRed(pixel)
        if bw==255:
            bands.append(y)
            print("decodeLines: Found bottom of sign at ",y)
            makeX(blbMark, 1, avX, y, green)
        y = y-1
        if y < 0:
            #print("decodeLines: FAILED: could not find bottom of sign") #debug
            return [-1]

    #print("decodeLines: Sign has been found. Here is bands: ",bands) #debug
    #print("decodeLines: getRed at the top of the sign is: ", getRed(getPixel(blb, avX, bands[0])))
    y=bands[0]
    color=0 #tells the program the color it should be looking for next. 255 is white, 0 is black
    while y<bands[1]: #while I haven't hit the bottom of the sign
        pixel = getPixel(blb, avX, y)
        bw = getRed(pixel)
        if bw==color:
            #print("decodeLines: Found a spot where the picture is: ", color)
            if bw==0:
                print("decodeLines: Top of band found at ",y) #debug
                makeX(blbMark, 1, avX, y, green) #debug
                color = 255
                bands.append(y)
            if bw==255:
                print("decodeLines: Bottom of band found at ",y-1) #debug
                makeX(blbMark, 1, avX, y-1, green) #debug
                color = 0
                bands.append(y-1)
        y = y+1
        #Looks for a black band, then white (the bottom of the band) then black for another band, and repeats this until it gets to the bottom of the sign

    print("decodeLines: Bands have been found. Here is bands: ",bands) #debug
    #print("decodeLines: The length of bands is: ",len(bands))
    if len(bands)%2==1 or len(bands) <= 6: #found an extra line that shouldn't exist
        #print("decodeLines: FAILED: found extra line") #debug
        return [-1]
    done=1
    i = 2
    
    number = readBands(pic, avX, bands)
    
    if number == []:
        number = [-1]

    print("decodeLines: final answer:", number) #debug
    return(number)

def readBands(pic, avX, coords): #returns the value of the bands
    answer = []
    i = 2
    while i<len(coords):
        total = 0
        startpoint = coords[i]
        endpoint = coords [i+1]
        length = pixelRepeatAmount(startpoint, endpoint)
        for k in range(length):
            total = total + getBand(pic, avX, startpoint+k)
        if total>length/2:
            answer.append(1)
        else:
            answer.append(0)
        print("readBands: ", total, "pixels were black", length-total, "were white")
        print("readBands:", total, "/", length/2)           
        i = i+2
    return answer
    
def pixelRepeatAmount(a, b):
    return (abs(b-a)+1)


def getBand(pic,avgX, y): #takes a pixel and determines whether it's closer to white or black and returns the binary value (white = 1, black = 1)
    colorPixel = getPixel(pic, avgX, y)
    r,g,b = getRGB(colorPixel)
    bwc = (r + g + b)/3
    if bwc >100: #CHANGER 150 100
        band = 0
    else:
        band = 1
    #print("getBand: Sample taken from ",y," with a color value of ",round(bwc))
    return band

def binToNum(binList): #converts a list of binary into a single base 10 number. Relies on flipList.
    i=0
    num = 0
    binList = flipList(binList)
    while i<len(binList):
        num = num + binList[i]*(2**i)
        i=i+1
    return num

    
def findBlobs(pic): #finds objects of interest in a black and white photo. Inputs: black and white photo. Outputs: list [x1.1, y1.1, x1.2, y1.2, x2.1, y2.1, x2.2 ...] where xa.1, ya.1 defines the top left corner of rectangle of interest a, and xa.2, ya.2 is the lower right corner. Dependecies: normalize, group, squarify. 
    mypic = makeNewPhotoCopy(pic)
    timer = default_timer() #debug
    show(pic) #debug
    print("findBlobs: took ", (default_timer() - timer), "seconds to take picture") #debug
    #wait(1)
    timer = default_timer() #debug 
    mypic = normalize(pic, 7)#CHANGER 5 7 9
    show(mypic)
    print("findBlobs: First blob success!")
    print("findBlobs: took ", (default_timer() - timer), "seconds to blob picture") #debug
    #wait(1)
    timer = default_timer() #debug
    grouppic = group(mypic) #CHANGER grouppic = pic
    print("findBlobs: took ", (default_timer() - timer), "seconds to group picture") #debug
    show(grouppic)
    print ("findBlobs: Picture sucessfully grouped")
    #wait(1)
    #normalize(grouppic, 7) #CHANGER
    #show(grouppic)
    #print("findBWsigns: Picture sucessfully blobbed twice")
    #wait(1)
    #start_two = default_timer() #debug
    timer = default_timer() #debug
    rectcoords = squarify(grouppic)
    print("findBlobs: took ", (default_timer() - timer), "seconds to squarify picture") #debug
    #print("findBlobs: time to squarify was", (default_timer() - start_two)) #debug
    #print ("findBWsigns: coordinates found!: ",rectcoords)
##     markblobpic = grouppic
##     i=0
##     while i<len(rectcoords): #debug
##         makeX(markblobpic, 1, rectcoords[i], rectcoords[i+1], makeColor(0, 255, 0))
##         i=i+2
##     show(markblobpic) #CHANGER
##     wait(1) #CHANGER
##     rectcoords = sizeCheck(rectcoords, size) #did not want this to take out the small boxes
##     i=0
##     while i<len(rectcoords): #debug
##         makeX(markblobpic, 1, rectcoords[i], rectcoords[i+1], makeColor(255, 0, 0))
##         i=i+2
##     show(markblobpic) #debug
##     wait(1) #debug
    return rectcoords    
    



def group(bw):
    mybw = makeNewPhotoCopy(bw)
    #print("getHeight(bw) is",getHeight(bw))
    #print("getWidth(bw) is",getWidth(bw))
    counter = 0 #how far have I gone without seeing white?
    jumpBack = 0 #is there a space I need to fill in? 0 means no, 1 means I've found a starting point, 2 means I've found an empty spot, 3 means I've found an ending.
    saveX = 0
    saveY = 0 #coordinates of last seen white pixel
    for i in range(getWidth(mybw)-1):
        for j in range(getHeight(mybw)-1):
            pix=getPixel(mybw, i, j)
            if getRed(pix)==255: #if pixel is white (this is a black and white picture)
                if jumpBack==0:
                    jumpBack = 1
                if jumpBack==2:
                    jumpBack = 3
                if jumpBack == 3:
                    while not((saveY)==j and saveX==i):
                        #print("group: repainting y from",saveX, saveY,"to",i, j)
                        repix = getPixel(mybw, saveX, saveY)
                        setColor(repix, makeColor(255, 255, 255))
                        if saveY==getHeight(mybw):
                            saveX=saveX+1
                        #print("group: repainting done, showing new pic.")
                        #show(bw)
                        saveY=saveY+1 #Goes back and repaints the pixels white
                    jumpBack = 1
                counter = 50 #CHANGE
                #print("saved point at", i, j)
                saveX = i
                saveY = j
            else:
                if counter>0:
                    jumpBack = 2 #if it sees a black pixel
                else:
                    jumpBack = 0 #if the counter is too low it doesn't jump back anymore.
            counter = counter-1
            if j==(getHeight(mybw)-2):
                #print("group: changing lines y")
                #print("group: new line is", j)
                counter = 0
                jumpBack = 0
    return mybw
def squarify(pic): #finds blobs and comes up with rectangles for them.
    mypic = makeNewPhotoCopy(pic)
    #print("squarify: started") 
    rect=[] #list of the rectangle coordinates
    for j in range(getHeight(mypic)):
        for i in range(getWidth(mypic)):
            pix = getPixel(mypic, i, j)
            if getRed(pix)==255:
                #print("squarify: found white pixel and about to call bwEdge")
                lastrect = bwEdge(mypic, [i, j])
                #print("squarify: bwEdge finished")
                #print("squarify: here's rect and lastrect", rect, lastrect)
                rect = rect+lastrect
                drawBlackRect(mypic, lastrect)
                #show(pic) #debug
                #print("squarify: here's rect: ",rect) 
    return rect             
                
                

def bwEdge(pic, coord): #follows edge of shape and returns max&min x&y values (the values that will make a rectangle covering the shape). It takes a black and white photo and the coordinates of a pixel inside the shape.
    #print("bwEdge: started, here's coord: ",coord)
    while not(move(0, pic, coord)=="no"):
        coord = move(0, pic, coord)
    edge = 0
    initcoord = coord
    #print("bwEdge: initcoord is ",initcoord)
    highlowval = [coord[0], coord[1], coord[0], coord[1]]
    
    while True:
        if not(move(edge, pic, coord)=="no"): #if the edge I thought was there is not there
            #print("bwEdge: Error:edge lost at", coord)
            #print("bwEdge: direction was", edge)
            return "error"
        else:
            if not(move((edge+1)%4, pic, coord)=="no"): #if I can move sideways along the edge
                coord = move((edge+1)%4, pic, coord) #move sideways
                highlowval = coordmaxmin(coord, highlowval) #update my max and min values
                #print("bwEdge: moved sideways to ", coord)
                if not(move(edge, pic, coord)=="no"): #if my edge has dissappeared, it must a turn so
                    coord = move(edge, pic, coord) #move in the direction my edge used to be (forward)
                    highlowval = coordmaxmin(coord, highlowval)#update my max and min
                    edge = (edge-1)%4 #and follow the edge to my left
                    #print("bwEdge: turning on open turn at",coord)
                    #print("bwEdge: edge I'm following now is", edge)
            else: #if I can't move sideways,
                edge = (edge+1)%4 #follow the edge to my side
                #print("bwEdge: tight turn", coord)
                #print("bwEdge: edge I'm following now is", edge)
        if edge==0 and coord==initcoord: #if I've returned back to the start and am following the same egde as I started
            return highlowval #return the rectangle coordinates (max and mins)
##         else:
##             piccolor=getRGB(getPixel(pic, coord[0], coord[1]))
##             if piccolor==(255, 255, 255):
##                 setColor(getPixel(pic, coord[0], coord[1]), makeColor(0,255,0))
##                 print("bwEdge: printed color green")
##             if piccolor==(0, 255, 0):
##                 setColor(getPixel(pic, coord[0], coord[1]), makeColor(0,0,0))
##                 print("bwEdge: printed white")
##             print("bwEdge: piccolor is", piccolor)
            

def coordmaxmin(coord, val):
    #print("coordmaxmin: here's coord and val: ",coord, val)
    if coord[0]<val[0]:
        val[0]=coord[0]
    if coord[1]<val[1]:
        val[1]=coord[1]
    if coord[0]>val[2]:
        val[2]=coord[0]
    if coord[1]>val[3]:
        val[3]=coord[1]
    #print("coordmaxmin: here's val: ",val)
    return val



def move(direction, photo, position):
    x = position[0]
    y = position[1]
    h=(getHeight(photo)-1)
    w=(getWidth(photo)-1)
    if direction == 0:
        if y == 0:
            return "no"

        if getRed(getPixel(photo, x, y-1)) == 0:
            return "no"

        return [x, y-1]

    if direction == 1:
        if x >= w:
            return "no"

        if getRed(getPixel(photo, x+1, y)) == 0:
            return "no"

        return [x+1, y]

    if direction == 2:
        if y >= h:
            return "no"

        if getRed(getPixel(photo, x, y+1)) == 0:
            return "no"

        return [x, y+1]

    if direction == 3:
        if x == 0:
            return "no"

        if getRed(getPixel(photo, x-1, y)) == 0:
            return "no"

        return [x-1, y]

def drawBlackRect(pic, coords): #draws a black rectangle on the picture from the coordinates. Overwrites the photo.
    #print("drawBlackRect: started. Here's coords: ",coords)
    drawRect(pic, coords, makeColor(0, 0, 0))
    #print("drawBlackRect: done. About to show finished pic")
    #show(pic)

def drawRect(pic, coords, color):
    try:
        startx = coords[0]
        starty = coords[1]
        for j in range((coords[3]-coords[1])+1):
            for i in range((coords[2]-coords[0])+1):
                setColor(getPixel(pic, startx+i, starty+j), color)
    except IndexError:
        return
    

def makeNewPhotoCopy(old): #creates and returns a new photo which is a copy of another one.
    new = makePicture(getWidth(old), getHeight(old))
    new = copyPhoto(new, old)
    return new

def copyPhoto(new, old): #copies one photo to another. overwrites the photo being copied to.
    for j in range(getHeight(old)):
        for i in range(getWidth(old)):
            newpix = getPixel(new, i, j)
            oldpix = getPixel(old, i, j)
            oldrgb = getRGB(oldpix)
            oldr = oldrgb[0]
            oldg = oldrgb[1]
            oldb = oldrgb[2]
            #print("copyPhoto: getRGB: ", getRGB(oldpix))
            setColor(newpix, makeColor(oldr, oldg, oldb))                     
    return new

def indexSmallBox(coords, size):
    i = 0
    answer = []
    while not(i>(len(coords)-1)):
        box = boxAtIndex(i, coords)
        boxSize = calcBoxSize(box)
        if boxSize < size:
            answer.append(i)    
        i = i+4
    return answer

    
def calcBoxSize(box): #calculates the size of the box given the coordinates
    return abs(box[2]-box[0])*abs(box[3]-box[1])
                    
def makeX(photo, size, x, y, color): #makes an x on the photo of the given size and color and coordinates. Overwrites the photo.
    #print ("makeX: here are the parameters I recieved:", photo, size, x, y, color)
    i=0
    while i<=(size*2):
        pix = getPixel(photo, x-size+i, y-size+i)
        setColor(pix, color)
        i=i+1
    i=0
    while i<=(size*2):
        pix = getPixel(photo, x+size-i, y-size+i)
        setColor(pix, color)
        i=i+1
        
            
def findRobots():
    start = default_timer() #debug
    size = 850
    setPicSize("small")
    pic = takePicture()
    show(pic) #debug
    #wait(1) #debug
    print("findRobots: converting to bw")
    bw = bwConverter(pic, "new pink") #new pink
    print("findRobots: done") #took 19.09 seconds (20 seconds)
    show(bw) #debug
    #wait(1) #debug
    #print("findRobots: time was", (default_timer()-start)) #debug
    print("findRobots: finding blobs")
    #start_two = default_timer() #debug
    coords = findBlobs(bw)
    print("findRobots: done") #took 2:09.31 minutes (2 minutes and 10 seconds)
    #print("findRobots: time was", (default_timer()-start_two)) #debug
    print("findRobots: here is coords ", coords)
    smallBoxes = indexSmallBox(coords, size)
    print("findRobots: the boxes at indexes", smallBoxes, "were too small")
    lookBoxes = indexBoxesToLookAt(len(coords), smallBoxes)
    print("findRobots: These are the boxes I'm looking at:", lookBoxes)
    print("findRobots: crossing out and reading boxes")
    #stuff below this is new
    bwBlob = normalize(bw, 7)
    signsRead = blockoutAndRead(coords, lookBoxes, bwBlob, pic)
    print("findRobots: done") #took 3:14.13 minutes (3 minutes and 15 seconds)
    print("findRobots: time was", (default_timer()-start)) #debug     
    return signsRead #overall took 5:43.14 (5 minutes and 45 seconds)
 
def blockoutAndRead(allBoxes, lookBoxes, bw, pic): #Blocks out the boxes and reads the lookBoxes in order. returns the base ten interpretation    
    signsRead = []
    i = 0
    allBlocked = makeNewPhotoCopy(bw)
    while inRange(i, allBoxes):
        blockBox = boxAtIndex(i, allBoxes) #define the box
        drawBlackRect(allBlocked, blockBox) #block it out
        i = i+4
    for j in lookBoxes: #for each box I want to look at
        markbw = makeNewPhotoCopy(allBlocked)
        theBox = boxAtIndex(j, allBoxes)
        markbw = pasteRect(bw, markbw, theBox) #mark bw now has just the part we want to look at and background
        number = decodeLines(pic, markbw, getBlobs(markbw)[1])
        #print("findRobots: converting from binary")
        if not(number == [-1]): #if decoding the lines didn't fail,
            signsRead.append(binToNum(number)) #add the sign number (in base ten) to the signs read.  
    return signsRead
def pasteRect(fromThis, toThis, coords): #pastes a rectangle of image from fromThis(picture) to toThis(picture). does not overwrite either picture; returns toThis with the pasted part on it.   
    old = fromThis
    new = makeNewPhotoCopy(toThis)
    fx = coords[0] #first x
    fy = coords[1]
    sx = coords[2] #second x
    sy = coords[3] 
    for j in range(abs(sy-fy)+1):
        for i in range(abs(sx-fx)+1):
            newpix = getPixel(new, i+fx, j+fy)
            oldpix = getPixel(old, i+fx, j+fy)
            oldrgb = getRGB(oldpix)
            oldr = oldrgb[0]
            oldg = oldrgb[1]
            oldb = oldrgb[2]
            #print("copyPhoto: getRGB: ", getRGB(oldpix))
            setColor(newpix, makeColor(oldr, oldg, oldb))                     
    return new

                
def indexBoxesToLookAt(amountOfCoords, removeBoxes): #makes a list of the box indexes you do want to look at given the indexes of the ones you don't and the length of all the coordinates          
    lookBoxes = []
    i = 0
    while not(i>(amountOfCoords-1)): #puts the indexes of all the boxes into a list
        lookBoxes.append(i)
        i = i+4
    for i in removeBoxes: #remove the boxes I don't want to look at
        lookBoxes.remove(i)
    return lookBoxes
    
def inRange(index, aList):
    try:
        aList[index] = aList[index]
        return True
    except IndexError:
        return False
        
def boxAtIndex(i, aList): #takes the coordinates of the box at that index from a list
    return [aList[i], aList[i+1], aList[i+2], aList[i+3]]
    
def findBiggestBoxes(coords, returnVal):
    bigSize = 0 #saves the size of the biggest box
    bigBoxIndexes = [] #saves the indexes of the biggest boxes
    bigBoxCoords = []
    i = 0
    while inRange(i, coords): #while there are boxes to be looked at
        box = boxAtIndex(i, coords) #this is the box I look at
        boxSize = calcBoxSize(box) #size of the box
        if boxSize > bigSize: #if it's the biggest box
            bigSize = boxSize #it sets the bar
            bigBoxIndexes = [i] #then its index is saved
        if boxSize == bigSize: #if it's tied for the biggest box
            bigBoxIndexes.append(i) #then I add its index to the list of biggest boxes           
        i = i+4
        
    if returnVal == "box": #if I should return a box, convert the indexes back into boxes
        for i in bigBoxIndexes:
            bigBoxCoords.extend(boxAtIndex(i, coords))
        return bigBoxCoords
    else:
        return bigBoxIndexes    

def drawBox(pic, coords, color): #draws a box of the given color with the coordinates x1, y1, x2, y2 where (x1, y1) is the top left corner and (x2, y2) is the bottom right. Overwrites the photo.
    x = coords[0]
    y = coords[1]
    while not(x==(coords[2])):
        pix = getPixel(pic, x, y)
        setColor(pix, color)
        x=x+1
    x = coords[2]
    while not (y==(coords[3])):
        pix = getPixel(pic, x, y)
        setColor(pix, color)
        y=y+1
    y = coords[3]
    while not(x==(coords[0])):
        pix = getPixel(pic, x, y)
        setColor(pix, color)
        x=x-1
    while not (y==(coords[1])):
        pix = getPixel(pic, x, y)
        setColor(pix, color)
        y=y-1
    return pic    

        
def flipList(aList):
    answer = []
    for i in aList:
        answer.insert(0, i)
    #print("flipList: got ", aList, "flipped it to", answer) #debug
    return answer
                
main()   





