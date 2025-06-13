from maya import mel, cmds

'''
Transfer Keys - Time Slider

Usage: 
1. Select animated object(s)...
2. Drag select frame length on Time Slider to define the length of the hold...
3. Run the script!
'''

slider = mel.eval('$tmpVar = $gPlayBackSlider;')
range = cmds.timeControl(slider, q=True, rangeArray=True)
start = range[0]
end = range[1]
mel.eval('timeSliderClearKey;')
cmds.currentTime(start-1, e=True)
mel.eval('timeSliderCopyKey;')
cmds.currentTime(end, e=True)
mel.eval('timeSliderPasteKey false;')
cmds.keyTangent(itt='auto', ott='auto')