from PyQt5 import QtCore      # core Qt functionality
from PyQt5 import QtWidgets       # extends QtCore with GUI functionality
from PyQt5 import QtOpenGL    # provides QGLWidget, a special OpenGL QWidget
import OpenGL.GL as gl        # python wrapping of OpenGL
from OpenGL import GLU        # OpenGL Utility Library, extends OpenGL functionality
from PyQt5 import QtGui
import sys                    # we'll need this later to run our Qt application

from OpenGL.arrays import vbo
import numpy as np
from GUI.objloader import *


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.width = 1366
        self.height = 600
        self.viewport = (1366,600)    
    def initializeGL(self):
        width,height = self.viewport
        self.qglClearColor(QtGui.QColor(0, 0, 255))    # initialize the screen to blue
        gl.glLightfv(GL_LIGHT0, GL_POSITION,  (0, 20, 30, 0.0))
        gl.glLightfv(GL_LIGHT0, GL_AMBIENT, (0.32, 0.3, 0.25, 1.0))
        gl.glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        gl.glEnable(GL_LIGHT0)
        gl.glEnable(GL_LIGHTING)
        gl.glEnable(GL_COLOR_MATERIAL)
        gl.glEnable(GL_DEPTH_TEST)
        gl.glShadeModel(GL_SMOOTH)
        gl.glMatrixMode(GL_PROJECTION)
        gl.glLoadIdentity()
        GLU.gluLookAt(0.0,0.0,-2.0,0.0,0.0,0.0,0.0,0.0,1.0)
        GLU.gluPerspective(45.0, width/float(height), 1, 100.0)
        gl.glEnable(GL_DEPTH_TEST)
        gl.glMatrixMode(GL_MODELVIEW)
        self.initGeometry()
        self.trasZ= 1.85
        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
         
    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glPushMatrix()
        gl.glTranslate(0.0, 0.0, -self.trasZ)
        #gl.glScale(20.0, 20.0, 20.0)
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glCallList(self.obj.gl_list)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix()    # restore the previous modelview matrix
        
    def initGeometry(self):
        self.obj = OBJ('modelo3D/pie.obj', swapyz=True, glgen=gl.glGenLists(1))

    def setRotX(self, val):
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val

        
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class
        
        self.resize(1366, 1000)
        self.setWindowTitle('Hello OpenGL App')

        self.glWidget = GLWidget(self)
        #self.glWidget.init.connect(self.on_init)
        self.initGUI()
        
        timer = QtCore.QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start() 
    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

        sliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        sliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        sliderZ = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        
        gui_layout.addWidget(sliderX)
        gui_layout.addWidget(sliderY)
        gui_layout.addWidget(sliderZ)

        
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
    
