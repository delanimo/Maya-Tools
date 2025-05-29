import maya.cmds as mc # type: ignore
'''
Usage: This leverages Maya's Parent Constraint to animate a seamless space-switch.  
It keys the frame before with a weight of zero, and the current frame with a weight of 1.

Instructions: select the child object(s) (targets), then the parent object (target) and run the script...
'''
#Switch TR
last = mc.ls(sl=True, type='transform', tl=True)[0]
mc.select(last, tgl=True)
sel = mc.ls(sl=True, type='transform')
mc.setKeyframe(sel, at=['translate', 'rotate'])
ct = mc.currentTime(q=True)
mc.currentTime((ct-1), e=True)
mc.setKeyframe(sel, at=['translate', 'rotate'])
mc.currentTime(ct, e=True)
#Disable Viewport
mc.refresh(suspend=True)
#Query frame before current frame
for each in sel:
    #Time to Space Switch
    src = last
    tgt = each
    mc.setKeyframe(tgt, at=['translate', 'rotate'])
    mc.parentConstraint(src, tgt, mo=True)
    #Key Parent Blend Channel
    mc.currentTime((ct), e=True)
    cnBlend = mc.listAttr(tgt, k=True, u=True)[-1]
    blendAttr = tgt + '.' + cnBlend
    mc.setAttr(blendAttr, 1)
    mc.setKeyframe(blendAttr)
    mc.currentTime((ct-1), e=True)
    mc.setAttr(blendAttr, 0)
    mc.setKeyframe(blendAttr)
    #Now, back to the current frame
    mc.currentTime(ct, e=True)
#Select target objects
mc.select(sel, r=True)
#Enable Viewport
mc.refresh(suspend=False)