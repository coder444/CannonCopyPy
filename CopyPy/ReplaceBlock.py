from mcpi import minecraft
from mcpi import block

import CopyBuild

def replaceLimited():
    print "ReplaceBlock will be called 1 time."
    inpblock = raw_input("Input a block name. If it is invalid then an error will occur. ")
    exec "block = block.%s" % inpblock.upper()
    print block

    ### How2GetMC lel
    mc = CopyBuild.giveMc()
    print mc
    clicked = False
    while clicked == False:
        blocks = mc.events.pollBlockHits()
        for blockk in blocks:
            mc.setBlock(blockk.pos, block)
            clicked = True

def replace():
    while True:
        print "ReplaceBlock will be called forever. To end, press [CTRL] + C."
        inpblock = raw_input("Input a block name. If it is invalid then an error will occur. ")
        exec "block = block.%s" % inpblock.upper()
        print block
        
        ### How2GetMC lel
        mc = CopyBuild.giveMc()
        print mc
        clicked = False
        while clicked == False:
            blocks = mc.events.pollBlockHits()
            for blockk in blocks:
                mc.setBlock(blockk.pos, block)
                clicked = True
