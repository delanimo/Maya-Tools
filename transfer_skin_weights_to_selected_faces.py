from maya import cmds, mel #type: ignore

'''
Transfer Skin Weights to Selected Faces

Usage: this re-weights selected faces to selected joints in Maya

Instructions:
    1. Select faces on skinned mesh...
    2. Select skin joints to re-weight the faces to...
    3. Run the script
'''

#Store selected faces
fcs = cmds.ls(sl=True, fl=True)
#Store selected joints
jts = cmds.ls(sl=True, type='joint')
#Toggle off joint selection
cmds.select(jts, tgl=True)
#Convert selected faces to vertices
mel.eval('PolySelectConvert 3;')
#Store selected vertices - these are the target points to re-weight
pts = cmds.ls(sl=True, fl=True)
#Store shape node of selected points
shp = cmds.listRelatives(pts[0], p=True)[0]
#Store transform node of shape node 
xfm = cmds.listRelatives(shp, p=True)[0]
#Duplicate transform node of skinned mesh to create projection cage
cmds.select(xfm, r=True)
cmds.duplicate(rr=True)
cln_xfm = cmds.ls(sl=True, type='transform')[0]
#Transfer selected points of skinned mesh to cage mesh to eventually trim the cage mesh using the selected points
cl_cmp = []
for pt in pts:
    cmp = pt.replace(xfm, cln_xfm)
    cl_cmp.append(cmp)
#Trim the cage mesh based on the selected points.  The cage should be the volume of the selected faces
cmds.select(cl_cmp, r=True)
mel.eval('InvertSelection;')
#Store inverted point selection to delete
del_cln_pts = cmds.ls(sl=True, fl=True)
#Select cage mesh and convert selection to vertices
cmds.select(cln_xfm, r=True)
mel.eval('PolySelectConvert 3;')
#Convert selection to faces and delete the excess faces.  The cage should now be the volume of the selected face
cmds.select(del_cln_pts, tgl=True)
mel.eval('InvertSelection;')
mel.eval('PolySelectConvert 1;')
cmds.delete()
#Create  temporary Selection Sets to project weights with Maya's Copy Skin Weights tool
#Selection Set for target vertex to re-weight
cmds.select(pts, r=True)
cmds.sets(n='tgt')
#Selection Set for points of cage mesh to project weights from
cmds.select(cln_xfm, r=True)
mel.eval('PolySelectConvert 3;')
cmds.sets(n='src')
#Skin cage mesh to selected joints
cmds.select(cln_xfm, jts, r=True)
cmds.skinCluster(tsb=True, bm=0, sm=0, mi=3)
#Select 'src' set, then 'tgt' set and run Copy Skin Weights
cmds.select('src', 'tgt', r=True)
cmds.copySkinWeights(noMirror=True, sa='closestPoint', ia=['closestJoint', 'oneToOne', 'oneToOne'])
'''
Cleanup
'''
#Delete temp Selection Sets and cage mesh
cmds.delete('src', 'tgt', cln_xfm)
#Print a message on completion
print('Weight Transfer Successful!')
#Clear selection
cmds.select(cl=True)