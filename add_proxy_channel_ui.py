from maya import cmds, mel # type:ignore
#Proxy Channel Connect
wdw = 'win_prx_chl'
if cmds.window(wdw, ex=True):
    cmds.deleteUI(wdw, wnd=True)
cmds.window(wdw, t='Create Proxy Channel UI', s=False)
cmds.columnLayout(adj=True, rs=10)
cmds.separator()
cmds.textFieldButtonGrp('tfbg_src_id', l='Source of Proxy Channel? ', pht='Path to Source channel, ex: obj.tx', bl='Load Selected Channel', bc='load_sel_chl()')
cmds.separator
cmds.textFieldGrp('tfg_prx_id', l='Name of Proxy Channel? ', pht='Ex: customChannel')
cmds.separator()
cmds.button(l='Add Proxy Channel to Selected Object(s)', h=40, bgc=[0.5, 0.5, 0.1], c='mk_prx_chl()')
cmds.showWindow(wdw)
cmds.window(wdw, e=True, wh=[510, 135])

def chName():
    #Get Maya's Channel Box
    chBx = mel.eval('global string $gChannelBoxName; $tmpVar = $gChannelBoxName;')
    #Store Selected Channel Names
    chSel = cmds.channelBox(chBx, q=True, sma=True)
    #Output the data stored in "chSel" once the function is executed
    return chSel

def load_sel_chl():
    sel = cmds.ls(sl=True)[0]
    chBx = chName()
    tfbg_src_chl = cmds.textFieldButtonGrp('tfbg_src_id', e=True, tx=(sel + '.' + chBx[0]))
    cmds.select(cl=True)
    return tfbg_src_chl
    
def mk_prx_chl():
    src = cmds.textFieldButtonGrp('tfbg_src_id', q=True, tx=True)
    prx_id = cmds.textFieldGrp('tfg_prx_id', q=True, tx=True)
    sel = cmds.ls(sl=True, type='transform')
    for each in sel:
        cmds.addAttr(each, ln=prx_id, proxy=src)