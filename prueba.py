import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtOpenGL import QGLWidget
from PyQt5 import QtCore, QtGui
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *
#from simple_viewer import SimpleViewer
width = 800
height = 600
viewport = (800,600)
#T = np.array([[0,1,1],[1,0,-1]],dtype=np.float32)
aspect = width/height
class MyQGLWidget(QGLWidget):
    initialize_cb    = QtCore.pyqtSignal()
    resize_cb        = QtCore.pyqtSignal(int,int)
    idle_cb          = QtCore.pyqtSignal()
    render_cb        = QtCore.pyqtSignal()
    mouse_move_cb    = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_press_cb   = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_release_cb = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_wheel_cb   = QtCore.pyqtSignal( QtGui.QWheelEvent )
    key_press_cb     = QtCore.pyqtSignal( QtGui.QKeyEvent )
    key_release_cb   = QtCore.pyqtSignal( QtGui.QKeyEvent )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def glInit(self):
        super().glInit()
        self.initialize_cb.emit()

    def gl_gen_lists(self, size):
        return glGenLists(size)
    def mouseMoveEvent( self, evt ):
        self.mouse_move_cb.emit( evt )

    def mousePressEvent( self, evt ):
        self.mouse_press_cb.emit( evt )

    def mouseReleaseEvent( self, evt ):
        self.mouse_release_cb.emit( evt )

    def keyPressEvent( self, evt ):
        self.key_press_cb.emit(evt)

    def keyReleaseEvent( self, evt ):
        self.key_release_cb.emit(evt)

    def initializeGL(self):
        self.initialize_cb.emit()

    def resizeGL(self, width, height):
        if height == 0: height = 1
        self.resize_cb.emit(width,height)

    def paintGL(self):
        self.render_cb.emit()

class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.tx=0.0
        self.ty=0.0
        self.zpos=42.0
        self.tras=False
        self.viewer = MyQGLWidget()        
        self.viewer.resize_cb.connect( self.resize )
        self.viewer.initialize_cb.connect( self.initialize )
        self.viewer.render_cb.connect(self.render )
        self.viewer.key_press_cb.connect( self.key_press )
        self.viewer.key_release_cb.connect( self.key_release )
        self.viewer.mouse_press_cb.connect( self.mouse_press )
        self.viewer.mouse_release_cb.connect(self.mouse_release )
        self.viewer.mouse_move_cb.connect( self.mouse_move )
        self.viewer.resize( width, height )
        self.viewer.show()
        self.obj = OBJ(sys.argv[1], swapyz=True, glgen=self.viewer.gl_gen_lists(1))
    def resize(self,w, h ):
        width = w
        height = h
        #glViewport( 0, 0, width, height )
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
    def initialize(self):
        self.viewer.makeCurrent()
        glLightfv(GL_LIGHT0, GL_POSITION,  (0, 20, 30, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.32, 0.3, 0.25, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, width/float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
    def render(self):
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glPushMatrix()  
        glTranslate(self.tx/20., self.ty/20., -self.zpos)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glCallList(self.obj.gl_list)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()
        print(self.tx,",",self.ty)
    def mouse_move(self, evt ):
        if self.tras:
            self.tx += evt.x()
            self.ty -= evt.y()
    def mouse_press(self, evt ):
        if evt.button() == 1:
            self.tras=True
    def mouse_release(self, evt ):
        self.tras=False
    def key_press(self, evt ):
        print('Key press {}'.format(evt.key()) )
    def key_release(self, evt ):
        print('Key release {}'.format(evt.key()) )
if __name__ == "__main__":
    app = App([])
    sys.exit(app.exec_())