from mcpi import minecraft
import warnings
import Circle
import CopyBuild
warnings.filterwarnings("ignore")

running = True

def getMc():
    global mc
    try:
        ip = raw_input("what is the ip?")
        ipp = ip
        port = 4711
        mc = minecraft.Minecraft.create(ipp, port)
        mc.postToChat("CityBuilder HOST Connection %s" % ipp)
    except:
        print("could not create world instance. Try again.")
    ### Edit coder444
    ### Make MRS return MC as it getMc() is now called by CopyBuild (LN25)
    return mc
def returnMc():
    return mc

### Edit coder444
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
        print("starting flood")
        x = 0
        y = 0
        z = 0
        for x in range(-10, 10):
                for z in range(-10, 10):
                    mc.setBlock(x * 10, 50, z * 10, 10, 0)
                    mc.setBlock(x * 10, 49, z * 10, 4, 0)
    elif(action == "terraform"):
        block = input("What block number?")
        data = input("what data number?")
        print("terraforming world...")
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
        cd = input("current direction: ")
        nd = input("new direction")
        CopyBuild.Turn(CopyBuild.currentPad, cd, nd)
        CopyBuild.build()
