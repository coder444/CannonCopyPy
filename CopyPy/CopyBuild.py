import json
import numpy as np
import math
import time
import os
import random
from mcpi import minecraft
import cPickle as pickle



class BlockCollection:
    def __init__(self, blockData, xlength, ylength, zlength, numB):
        """The BlockData is the x, y, z, blockID, and the blockData in that order. 
        Since block data is not necessarily needed there may not be a 5th element?"""   
        self.blockData = blockData
        self.xLen = xlength
        self.yLen = ylength
        self.zLen = zlength
        self.numBlocks = numB
        """the maxVals are the highest x, y, and z values out of all of the ."""
### Edit coder444
### Create def for askForMc, called by MinecraftRemoteScript
def askForMc():
    global mc
    import MinecraftRemoteScript
    mc = MinecraftRemoteScript.getMc()

"""Default current pad"""

def getPad():
    return currentPad
"""Iterate through every list and use it to place blocks relative to input"""
def placeBlockCollection(BC , x, y, z):
    for block in BC.blockData:
        mc.setBlock(x + block[0], y + block[1], z + block[2], block[3], block[4])

"""Make a platform for something to be on. pass starting corner of rectangle to place, end place, block to use, and block data."""
def buildPlatform(x, y, z, ex, ey, ez, BID, BD):
    print ("building platform")
    
    for platX in range (int(x),int(ex)): 
        for platZ in range(int(z), int(ez)):
            platY = y;
            v = mc.getBlock(platX, platY, platZ)
            while ((v == 0 or v == 9 or v == 10 or v == 8 or v == 78 or v == 79)and platY <= ey):
                mc.setBlock(platX, platY, platZ, BID, BD)
                platY -= 1
                v = mc.getBlock(platX, platY, platZ)
"""Build a block collection on top of a platform"""
def buildStructure(BC, qx, qy, qz, platBlock, platID):
    x = math.floor(qx)
    y = math.floor(qy)
    z = math.floor(qz)
    buildPlatform(x, y - 1, z , x + BC.xLen , y - 1, z + BC.zLen , platBlock, platID)
    placeBlockCollection(BC, x, y, z)

def buildStructureLowest(BC, x, y, z, platBlock, platID):
    x = int(x)
    y = int(y)
    z = int(z)

    maxAmount = (BC.xLen * BC.zLen) / 2
    amount = 0

    cY = y

    while(not(mc.getBlock(x, cY, z) == 0)):
        cY += 1
    while(amount < maxAmount):
        for cX in range(x, x + BC.xLen):
            for cZ in range(z, z + BC.zLen):
                s = mc.getBlock(cX, cY, cZ)
                if (not(s ==0 or s == 18 or s == 17)):
                    amount += 1
                else:
                    mc.setBlock(cX, cY, cZ, 0, 0)
                if(amount >= maxAmount):
                    buildPlatform(x, cY, z , x + BC.xLen , cY, z + BC.zLen , platBlock, platID)
                    placeBlockCollection(BC, x, cY + 1, z)
                    return
        cY -= 1
    buildPlatform(x, y - 1, z , x + BC.xLen , y - 1, z + BC.zLen , platBlock, platID)
    placeBlockCollection(BC, x, y, z)
"""store a block collection from a pad."""
def makeBlockCollectionFromPad(padX, padY, padZ, padLenX, padlenY, padLenZ):
    global currentPad
    
    padX = int(padX)
    pady = int(padY)
    padz = int(padZ)
    padLenX = int(padLenX)
    padLenY = int(padlenY)
    padLenZ = int(padLenZ)

    padMat = []

    for x in range(int(padX), int(padX + padLenX)):
        for z in range(int(padZ), int(padZ + padLenZ)):
            for y in range(int(padY + 1), int(padY + padLenY + 1)):
                if(mc.getBlock(x, y, z) != 0):
                    blocky = mc.getBlockWithData(x, y, z)
                    padMat.append([x - padX, y - padY - 1, z - padZ, mc.getBlock(x, y, z), blocky.data])
    currentPad = BlockCollection(padMat, padLenX, padLenY, padLenZ, len(padMat))

"""This is a test house."""
currentPad = BlockCollection(

    [
        [0,0,0,35,0],
        [1,0,0,35,1],
        [2,0,0,35,2],

        [0,0,1,35,3],
        [1,0,1,35,4],
        [2,0,1,35,5],

        [0,0,2,35,6],
        [1,0,2,35,7],
        [2,0,2,35,8]

    ]
    ,
    3, 1, 3, 9
)

"""This is the copy function. this copys a structure on a pad."""
def copy():
    global mc
    global blockEv
    
    blockEv = []
    mc.postToChat("Make a wool rectangle under your house, then")
    mc.postToChat("right click your wool platform under the front of your house. ")
    while(len(blockEv) == 0):
        blockEv = mc.events.pollBlockHits()
        """Check if the event was on a wool block and a hit"""
        if(len(blockEv) != 0):
            if(blockEv[0].type == 0):
                if(mc.getBlock(blockEv[0].pos) == 35):
                    mc.postToChat("Platform Selected. Copying structure...")
                    blockEv = blockEv[0]
                    x = blockEv.pos.x
                    y = blockEv.pos.y
                    z = blockEv.pos.z
                    ###print("hello")

                    direction = 1

                    left = False
                    up = False
                    
                    lenX = 0
                    lenZ = 0
                    
                    xCounter = 0
                    zCounter = 0
          
                    while(mc.getBlock(x - 1, y, z) == 35):
                        x -= 1
                        xCounter += 1
                    while(mc.getBlock(x , y, z - 1) == 35):
                        z -= 1
                        zCounter += 1
                    while(mc.getBlock(x + lenX, y, z) == 35):
                          lenX = lenX + 1
                    
                    while(mc.getBlock(x, y, z + lenZ) == 35):
                          lenZ = lenZ + 1
                    lenY = 10;

                    center = lenZ / float(2)

                    ###if hit is farther left than right, on which side of center (lenX / 2)
                    if(xCounter < center):
                        ###is on left
                        left = True
                    if(zCounter > center):
                        up = True

                    xDistance = abs(xCounter - center)
                    zDistance = abs(zCounter - center)
                    if(xDistance > zDistance):
                        if(left == True):
                            direction = 4
                            
                        else:
                            direction = 2
                    else:
                        if(up == True):
                            direction = 1
                        else:
                            direction = 3
                    if(xCounter == 0):
                        direction = 2
                    
                    st = "the direction selected is "
                    print(st)
                    print(direction)
                    makeBlockCollectionFromPad(x, y, z, lenX, lenY, lenZ, )
                    Turn(currentPad, direction, 1)
                    blockEv = [1]
                    mc.postToChat("Structure copied.")
                    logic = raw_input("Overwrite this structure to Save file? (y/n)")
                    if(logic == "y"):
                        save();
###open("Save.p", "wb")
def save():
    global masterList
    filee = raw_input("name of save:")
    folder = raw_input("folder for save:")
    path = "Saves/" + folder
    if not os.path.isdir(path):
        os.makedirs(path)
    filee = path + "/" + filee
    filee = filee + ".p"
    print("Saving to file...")
    try:
        f = open(filee, 'wb')
        pickle.dump(currentPad, f)
        f.close()
    except:
        print("Could not save file. try again.")

    try:
        p = open("Saves/" + folder + "/MasterList.p", 'rb')
        masterList = pickle.load(p)
        p.close()
    except:
        h = open("Saves/" + folder + "MasterList.p", 'wb')
        masterList = []
        h.close()

    masterList.append(filee)
    g = open("Saves/" + folder + "/MasterList.p", 'wb')
    pickle.dump(masterList, g)
    g.close()
    '''
        g = open("Saves/MasterList.p", 'wb')
        print("Masterlist reset.")
        masterList = []
        pickle.dump(masterList, g)
        g.close()
    '''
    ### print("could not write to master list.")
def load():
    global currentPad
    filee = raw_input("file to load: ") + ".p"
    folder = raw_input("foler of save: ")
    filee =os.path.join(os.path.abspath("Saves") , folder ,  filee)
    g =open(filee, "rb")
    currentPad = pickle.load(g)
    g.close()
    logic = raw_input("start building with loaded file? (y/n)")
    if(logic == "y"):
        build()
    
        
def build():
    global mc
    #from MinecraftRemoteScript import mc
    mc.postToChat("Building structure.")
   
    placeToBuild = (mc.player.getPos())
    structure = currentPad

    buildStructureLowest(structure, int(placeToBuild.x) + 1, int(placeToBuild.y) + 1, int(placeToBuild.z), 35, int(placeToBuild.z))

###North = 1
###East = 2
    
###South = 3
###West = 4


def Turn(BC, currentDirection, newDirection):
    if(currentDirection == 1):
        if(newDirection == 2):
            Rotate(BC, 1)
        elif(newDirection == 3):
            Rotate(BC, 2)
        elif(newDirection == 4):
            Rotate(BC, 3)
    elif(currentDirection == 2):
        if(newDirection == 1):
            Rotate(BC, 3)
        elif(newDirection == 3):
            Rotate(BC,1)
        elif(newDirection == 4):
            Rotate(BC,2)
    elif(currentDirection == 3):
        if(newDirection == 1):
            Rotate(BC,2)
        elif(newDirection == 2):
            Rotate(BC,3)
        elif(newDirection == 4):
            Rotate(BC,1)
    elif(currentDirection == 4):
        if(newDirection == 1):
            Rotate(BC,1)
        elif(newDirection == 2):
            Rotate(BC,2)
        elif(newDirection == 3):
            Rotate(BC,3)
            
def FlipOpp(BC):
    for block in BC.blockData:
        original = block
        block[0] = (original[0] * -1) + BC.xLen - 1
        block[2] = (original[2] * -1) + BC.zLen - 1

def FlipAdj(BC):
    print("flipping adjacent")
    for block in BC.blockData:
        x = block[0]
        z = block[2]
        block[0] = z
        block[2] = x

def Rotate(BC, times):
    for i in range(0, times):
        TurnN(BC)

def TurnN(BC):
    print(BC.blockData)
    for block in BC.blockData:
        ###x,y ---> y, -x
        x = block[0]
        z = block[2]
        block[0] = (z * -1) + BC.zLen - 1
        block[2] = x
    print(BC.blockData)

def BuildCityTwo():
    global mc
    from MinecraftRemoteScript import mc

    laneSpace = 2
    
    placeToBuild = (mc.player.getTilePos())
    x =placeToBuild.x
    y =placeToBuild.y - 2
    z =placeToBuild.z
    
    folder = raw_input("folder to make city from:")
    f = open("Saves/" + folder + "/" + "MasterList.p", 'rb')
    masterList = pickle.load(f)

    
    
def BuildCity():
    global mc
    from MinecraftRemoteScript import mc

    laneSpace = 2
    
    placeToBuild = (mc.player.getTilePos())
    x =placeToBuild.x
    y =placeToBuild.y - 2
    z =placeToBuild.z
    sizeX = input("length of city:")
    sizeY = 20
    sizeZ = input("width of city:")
    ###mc.setBlocks(x, y, z, x + sizeX, y, z + sizeZ, 35, 15)
    ###mc.setBlocks(x, y + 1, z - 8, x + sizeX, y + sizeY, z + sizeZ, 0, 0)

    folder = raw_input("folder to make city from:")
    f = open("Saves/" + folder + "/" + "MasterList.p", 'rb')
    masterList = pickle.load(f)
    
    f.close()
    bx = x
    bz = z + sizeZ
    zCounter = 0

    while(bz >= z):
        for structureF in masterList:
            if(random.randint(0, 10) > 6):
                g = open(structureF, "rb")
                structure = pickle.load(g)
                if(random.randint(0,10) > 2):
                    buildStructureLowest(structure, bx, y + 1, bz - structure.zLen, 35, bz)
                bx += structure.xLen - 1 + laneSpace
                g.close()
                if(structure.zLen > zCounter):
                    zCounter = structure.zLen
                if(bx + structure.xLen > x + sizeX):
                    bx = x
                    bz =bz - zCounter - laneSpace
            
                ### buildStructure(structure, bx, y + 2, bz - structure.zLen, 35, bz)






        
