from skimage import io
import time
import os
from OpenGL.GL import *
import numpy as np
def MTL(spath2, filename):
	contents = {}
	mtl = None
	rpath=os.path.dirname(os.path.abspath(__file__)) + '\\' + spath2
	print("MTL: " + filename)
	print("rpath: " + rpath)
	for line in open(rpath+'\\'+filename, "r"):
		if line.startswith('#'): continue		
		values = line.split()
		if not values: continue
		if values[0] == 'newmtl':
			mtl = contents[values[1]] = {}
		elif mtl is None:
			raise ValueError("mtl file doesn't start with newmtl stmt")
		elif values[0] == 'map_Kd':
			# load the texture referred to by this declaration
			mtl[values[0]] = values[1]
			smatpath=mtl['map_Kd']			
			smatpath=smatpath.replace("\\","/")
			print(rpath + smatpath)
			surf = io.imread(rpath + smatpath)
			image = np.fromstring(surf.tostring(),np.uint8)
			ix, iy = surf.shape
			print(ix,",",iy)
			texid = mtl['texture_Kd'] = glGenTextures(1)
			glBindTexture(GL_TEXTURE_2D, texid)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		else:
			mtl[values[0]] = map(float, values[1:])
	return contents

class OBJ:
	def __init__(self, filename, swapyz=False,glgen=None):
		"""Loads a Wavefront OBJ file. """
		self.trasX = 0.0
		self.trasY = 0.0
		self.trasZ = 0.0
		self.rotX  = 0.0
		self.rotY  = 0.0
		self.rotZ  = 0.0
		self.scaleX = 1.0
		self.scaleY = 1.0
		self.scaleZ = 1.0
		self.vertices = []
		self.normals = []
		self.texcoords = []
		self.faces = []
		material = None
		print(">>" + filename)
		i=filename.rfind("/")
		spath2=""
		if(i==-1):
			spath2=""
		else:
			spath2=filename[0:i] + '\\'
		for line in open(os.path.dirname(os.path.abspath(__file__)) + '\\' + filename, "r"):
			if line.startswith('#'): continue
			values = line.split()
			if not values: continue
			if values[0] == 'v':
				v = list(map(float, values[1:4]))
				if swapyz:
					v = v[0], v[2], v[1]
				self.vertices.append(v)
			elif values[0] == 'vn':
				v = list(map(float, values[1:4]))
				if swapyz:
					v = v[0], v[2], v[1]
				self.normals.append(v)
			elif values[0] == 'vt':
				self.texcoords.append(list(map(float, values[1:3])))
			elif values[0] in ('usemtl', 'usemat'):
				material = values[1]
			elif values[0] == 'mtllib':
				self.mtl = MTL(spath2, values[1])
			elif values[0] == 'f':
				face = []
				texcoords = []
				norms = []
				for v in values[1:]:
					w = v.split('/')
					face.append(int(w[0]))
					if len(w) >= 2 and len(w[1]) > 0:
						texcoords.append(int(w[1]))
					else:
						texcoords.append(0)
					if len(w) >= 3 and len(w[2]) > 0:
						norms.append(int(w[2]))
					else:
						norms.append(0)
				self.faces.append((face, norms, texcoords, material))
		
	def init_geometri(self):
		self.gl_list = glGenLists(1)
		print(self.gl_list)
		glNewList(self.gl_list, GL_COMPILE)
		glEnable(GL_TEXTURE_2D)
		glFrontFace(GL_CCW)
		for face in self.faces:
			vertices, normals, texture_coords, material = face
			mtl = self.mtl[material]
			#print("#   ")
			#print(mtl)
			if 'texture_Kd' in mtl:
				# use diffuse texmap
				glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
			else:
				# just use diffuse colour
				#glColor(*mtl['Kd'])
				glColor(1, 1, 1, 0.5)

			glBegin(GL_POLYGON)
			for i in range(len(vertices)):
				if normals[i] > 0:
					glNormal3fv(self.normals[normals[i] - 1])
				if texture_coords[i] > 0:
					glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
				glVertex3fv(self.vertices[vertices[i] - 1])
			glEnd()
		glDisable(GL_TEXTURE_2D)
		glEndList()
	def Animacion(self,anX,anY,anZ,disx,disy,disz,scx,scy,scz,t=2.0):
		m=int(t/0.005)
		dx = (anX - self.rotX)/m
		dy = (anY - self.rotY)/m
		dz = (anZ - self.rotZ)/m
		dsx = (disx-self.trasX)/m
		dsy = (disy-self.trasY)/m
		dsz = (disz-self.trasZ)/m
		sx  = (scx - self.scaleX)/m
		sy  = (scy - self.scaleY)/m
		sz  = (scz - self.scaleZ)/m
		for l in range(m):
			self.rotX += dx
			self.rotY += dy
			self.rotZ += dz
			self.trasX += dsx
			self.trasY += dsy
			self.trasZ += dsz
			self.scaleX += sx
			self.scaleY += sy
			self.scaleZ += sz
			time.sleep(0.005)
		print('dx:{},dy:{},dz:{},rotx:{},roty:{},rotz:{},scx:{},scy:{},scz:{}'.format(self.trasX,self.trasY,self.trasZ,self.rotX,self.rotY,self.rotZ,self.scaleX,self.scaleY,self.scaleZ))
	def draw(self):
		glPushMatrix()
		glTranslate(self.trasX,0,0)
		glTranslate(0,self.trasY,0)
		glTranslate(0,0,self.trasZ)
		glRotate(self.rotX,1.0,0.0,0.0)
		glRotate(self.rotY,0.0,1.0,0.0)
		glRotate(self.rotZ,0.0,0.0,1.0)
		glScale(self.scaleX,self.scaleY,self.scaleZ)
		glCallList(self.gl_list)
		glPopMatrix()
