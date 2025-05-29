import maya.cmds as mc
#Switch TR
last = mc.ls(sl=True, type='transform', tl=True)[0]
mc.select(last, tgl=True)
sel = mc.ls(sl=True, type='transform')
#Disable Viewport
mc.refresh(suspend=True)
#Time to Space Switch
src = sel[0]
tgt = last
ct = mc.currentTime(q=True)
mc.currentTime((ct-1), e=True)
mc.setKeyframe(src, at=['translate', 'rotate'])
mc.currentTime(ct, e=True)
mc.setKeyframe(src, at=['translate', 'rotate'])
mc.parentConstraint(tgt, src, mo=True)
cnBlend = mc.listAttr(src, k=True, u=True)[-1]
blendAttr = src + '.' + cnBlend
mc.setAttr(blendAttr, 1)
mc.setKeyframe(blendAttr)
mc.currentTime((ct-1), e=True)
mc.setAttr(blendAttr, 0)
mc.setKeyframe(blendAttr)
mc.currentTime(ct, e=True)
mc.select(src, r=True)
#Enable Viewport
mc.refresh(suspend=False)