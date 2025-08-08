from maya import cmds
'''
Prune Keys Over Time

Usage:
This removes keys based on a distance threshold.  Great for mocap baked to controls.

Instructions: 
    1. Choose playback range to prune...
    2. Select animated objects to prune...
    3. Run script
'''

#Query playback start and end frames
start = int(cmds.playbackOptions(q=True, min=True))
end = int(cmds.playbackOptions(q=True, max=True))
#Set iteration range based on frame range
fr_len = end-start

#Store selection
sel = cmds.ls(sl=True, type='transform')

#For loop - run this on each selected animated object
dist_threshold = 0.2
#Store trimmed keys
cutFrames = []

for each in sel:
    #Distance node to track frames of pruned keys
    distance = cmds.createNode('distanceBetween', n=(each + '_distance'))
    #Temp locator to connect to distance node
    loc = cmds.spaceLocator(n=each + '_prune_loc')[0]
    #Connect animated object and locator to distance node
    cmds.connectAttr((each + '.translate'), (distance + '.point1'), f=True)
    cmds.connectAttr((loc + '.translate'), (distance + '.point2'), f=True)
    #Go to start of playback
    cmds.currentTime(start, e=True)
    currentT = cmds.currentTime(q=True)
    #For loop - iterate through time range and store all the keys within distance threshold
    for i in range(fr_len):
        cmds.currentTime((currentT + i), e=True)
        #Store current frame
        ct = int(cmds.currentTime(q=True))
        #Go to previous frame and align locator to animated object to track distance
        cmds.currentTime(ct-1, e=True)
        cmds.matchTransform(loc, each, pos=True)
        cmds.currentTime(ct, e=True)
        cmds.select(each, r=True)
        #Print result of distance node and current frame
        dist_len = cmds.getAttr(distance + '.distance')
        print(dist_len, ct)
        #Store frames of trimmed keys in "cutFrames"
        if dist_len < dist_threshold:
            cutFrames.append(ct)
    #Clean up - remove locator and distance node
    cmds.delete(loc, distance)
    #Iterate through each frame stored in "cutFrames" and prune keys
    for cutFr in cutFrames:
        cmds.currentTime(cutFr, e=True)
        cmds.select(each, r=True)
        cmds.cutKey(t=(cutFr, cutFr), cl=True)

#Select pruned animated objects and reset to start frame    
cmds.select(sel, r=True)
cmds.currentTime(start, e=True)