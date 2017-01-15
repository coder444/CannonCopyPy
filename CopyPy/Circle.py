from mcpi import minecraft
import math

def Draw():
    from MinecraftRemoteScript import returnMc
    mc = returnMc()
    for size in range(1, 5):
        size = 25 - (size * 5)
        for y in range(0, 25 - size):
            for deg in range(1, 360):
                x = math.cos(deg) * size
                z = math.sin(deg) * size
                mc.setBlock(x, y, z, 35, y + x + z)
    
