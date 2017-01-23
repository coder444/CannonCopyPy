from mcpi import minecraft
import warnings
import Circle
import CopyBuild

import ReplaceBlock

import sys

warnings.filterwarnings("ignore")

running = True

def getMc():
    global mc
    try:
        ip = raw_input("Please Enter IP Address Here: ")
        ipp = ip
        port = 4711
        mc = minecraft.Minecraft.create(ipp, port)
        mc.postToChat("CityBuilder HOST Connection %s" % ipp)
    except:
        print("Failed to connected to %s. Is %s running Minecraft Pi Edition?" % (ipp, ipp))
        sys.exit()
    ### Make MRS return MC as it getMc() is now called by CopyBuild (LN25)
    return mc
def returnMc():
    return mc

### Following 2 lines: Ask CopyBuild to ask MinecraftRemoteScript to ask for an
### IP and return MC
CopyBuild.askForMc()
#getMc()

first = True

while(running == True):
    global running

    
    
    
    action = raw_input("choose an action.")
    actions = [
        "start",
        "flood",
        "circle",
        "random",
        "terraform",
        "copy",
        "build",
        "save",
        "load",
        "city",
        "quit"
    ]
    if(action == "start"):
        getMc()
    

    if(action == "quit"):
       running = False
    if(action == "list"):
        print(actions)
        
    elif (action== "circle"):
        Circle.Draw()
    elif(action == "flood"):
        print("Starting Flood...")
        x = 0
        y = 0
        z = 0
        for x in range(-10, 10):
                for z in range(-10, 10):
                    mc.setBlock(x * 10, 50, z * 10, 10, 0)
                    mc.setBlock(x * 10, 49, z * 10, 4, 0)
    elif(action == "terraform"):
        block = input("What block ID?")
        data = input("What data value?")
        print("Terraforming World...")
        for y in range(10, 0):
            for x in range(-25, 25):
                for z in range(-25, 25):
                    if(mc.getBlock(x, y, z) != 0):
                        mc.setBlock(x, y, z, block, data)
    elif(action == "copy"):
        CopyBuild.copy()
        
    elif(action == "build"):
        CopyBuild.build()
    elif(action == "save"):
        CopyBuild.save()
    elif(action == "load"):
        CopyBuild.load()
    elif(action == "city"):
        CopyBuild.BuildCity()
    elif(action == "quit"):
        running = False
    elif(action == "turn"):
        cd = input("Current Direction: ")
        nd = input("New Direction: ")
        CopyBuild.Turn(CopyBuild.currentPad, cd, nd)
        CopyBuild.build()
    elif(action == "replace"):
        ReplaceBlock.replaceLimited()
    elif(action == "replacef"):
        ReplaceBlock.replace()
        
