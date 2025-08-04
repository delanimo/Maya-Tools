from maya import cmds #type: ignore
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
start = cmds.playbackOptions(q=True, min=True)
end = cmds.playbackOptions(q=True, max=True)
#Set iteration range based on frame range
fr_len = int(end-start)

#Store selection
sel = cmds.ls(sl=True, type='transform')

#For loop - run this on each selected animated object
dist_threshold = 0.1
for each in sel:
    #Empty list to store trimmed keys
    cutFrames = []
    #Distance node to track frames of pruned keys
    dist = cmds.createNode('distanceBetween', n=(each + '_distance'))
    #Temp locator to connect to distance node
    loc = cmds.spaceLocator()[0]
    #Connect animated object and locator to distance node
    cmds.connectAttr((each + '.translate'), (dist + '.point1'), f=True)
    cmds.connectAttr((loc + '.translate'), (dist + '.point2'), f=True)
    #Go to start of playback
    cmds.currentTime(start, e=True)
    #For loop - iterate through time range and store all the keys within distance threshold
    for i in range(fr_len):
        cmds.currentTime(i, e=True)
        #Store current frame
        ct = int(cmds.currentTime(q=True))
        #Go to previous frame and align locator to animated object to track distance
        cmds.currentTime(ct-1, e=True)
        cmds.matchTransform(loc, each, pos=True)
        cmds.currentTime(ct, e=True)
        cmds.select(each, r=True)
        #Print result of distance node and current frame
        dist_len = cmds.getAttr(dist + '.distance')
        print(dist_len, ct)
        #Store frames of trimmed keys in "cutFrames" list
        if dist_len < dist_threshold:
            cutFrames.append(ct)
    #Clean up - remove locator and distance node
    cmds.delete(loc, dist)
    #Iterate through each frame stored in "cutFrames" list and prune keys
    for cutFr in cutFrames:
        cmds.currentTime(cutFr, e=True)
        cmds.select(each, r=True)
        cmds.cutKey(t=(cutFr, cutFr), cl=True)

#Select pruned animated objects and reset to start frame    
cmds.select(sel, r=True)
cmds.currentTime(start, e=True)