import c4d
import os
import sys
from math import pi, cos
import  math
from c4d import gui, plugins, bitmaps

#Test value for id
PLUGIN_ID = 1234588881

JENS_SCALE = 1000
JENS_ONOFF = 1001
TICK_DISTANCE = 0
ROTATION = pi/100

class MoveType:
    BOUNCE=1
    ROLL=2

class JENS(plugins.TagData):
	pass

	def Init(self, node):
		tag = node
		data = tag.GetDataInstance()
		
		data.SetBool(JENS_ONOFF, True)
		data.SetLong(JENS_SCALE, 1)
		self.MoveType = MoveType.BOUNCE
		return True
	
	def Execute(self, tag, doc, op, bt, priority, flags):
	
		data = tag.GetDataInstance()
		
		onoff = data.GetBool(JENS_ONOFF)
		scale = data.GetLong(JENS_SCALE)
		
		if onoff:
			frame = doc.GetTime().GetFrame(doc.GetFps())
			
			op[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]=op[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]-ROTATION
			#move it sideways
			op[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]=op[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]+TICK_DISTANCE
			
			beta = op[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]
			while beta < 0:
				beta += 2*pi
			
			op[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = beta
			#print beta
			hypo = math.sqrt(200*200 + 200*200)
			hypo = op[c4d.ID_BASEOBJECT_REL_SCALE,c4d.VECTOR_X]*200
			
			
			y = 0
			if self.MoveType == MoveType.BOUNCE:
				angle = beta
				while angle > pi/2:
					angle -= pi/2
				
				if angle > pi/4:
					y = hypo*cos(pi/2-angle)
				else:
					y = hypo*cos(angle)
				
			op[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y]=y
			
			print "Y is ", y, " and angle is ", beta
			
				
		return c4d.EXECUTIONRESULT_OK

if __name__ == "__main__":
	plugins.RegisterTagPlugin(id=PLUGIN_ID, str="Jens demo", info=c4d.TAG_VISIBLE|c4d.TAG_EXPRESSION, g=JENS, description="jens", icon=None)
	print "ok"