# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VisorPies3D.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtOpenGL
import OpenGL.GL as gl
from OpenGL import GLU
from objloader import *
from threading import Thread
import time
class Visor(QtOpenGL.QGLWidget):
    init=pyqtSignal()
    def __init__(self,parent=None):
        self.parent=parent
        QtOpenGL.QGLWidget.__init__(self,parent)
        self.width = 1366
        self.height = 700
        self.viewport = (1366,700)   
        self.trasZ = -1.4
        self.trasX = -0.5
        self.trasY = -0.2
        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
        self.scX = 1.0
        self.scY = 1.0
        self.scZ = 1.0
        self.permiso = False
    def glInit(self):
        super().glInit()
        self.init.emit()
    def gl_gen_lists(self,size):
        return gl.glGenLists(size)
    def initializeGL(self):
        width,height = self.viewport
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION,  (0, 20, 30, 0.0))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, (0.32, 0.3, 0.25, 1.0))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        GLU.gluLookAt(0.0,0.0,-2.0,0.0,0.0,0.0,0.0,0.0,1.0)
        GLU.gluPerspective(45.0, width/float(height), 1, 100.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        h=Thread(target=self.initGeometry)
        h.start()
        time.sleep(5)
    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)
        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    def initGeometry(self):
        self.obj = OBJ('../modelo3D/pie.obj', swapyz=True, glgen=gl.glGenLists(1))
    def setRotX(self, val):
        self.rotX = val

    def setRotY(self, val):
        self.rotY = val

    def setRotZ(self, val):
        self.rotZ = val

    def paintGL(self):
        self.permiso=True
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glPushMatrix()
        gl.glTranslate(self.trasX,self.trasY,self.trasZ)
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glScale(self.scX,self.scY,self.scZ)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        self.obj.draw()
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glPopMatrix()
        self.permiso = False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1366, 1000)
        MainWindow.setMinimumSize(QSize(1366, 1000))
        MainWindow.setMaximumSize(QSize(1366, 1000))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(85, 170, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Light, brush)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush)
        brush2 = QBrush(QColor(82, 84, 90, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush2)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Active, QPalette.Text, brush3)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush4 = QBrush(QColor(53, 53, 53, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush4)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush3)
        brush5 = QBrush(QColor(0, 0, 127, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush5)
        brush6 = QBrush(QColor(0, 85, 127, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush6)
        brush7 = QBrush(QColor(255, 255, 220, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush3)
        brush8 = QBrush(QColor(0, 0, 0, 128))
        brush8.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush9 = QBrush(QColor(85, 85, 255, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush3)
        brush10 = QBrush(QColor(0, 120, 215, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        MainWindow.setPalette(palette)
        self.actionestilos = QAction(MainWindow)
        self.actionestilos.setObjectName(u"actionestilos")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(0, 1000))
        self.centralwidget.setMaximumSize(QSize(1366, 1000))
        self.Visor3D = QWidget(self.centralwidget)
        self.Visor3D.setObjectName(u"Visor3D")
        self.Visor3D.setGeometry(QRect(0, 0, 1350, 700))
        self.Visor3D.setMaximumSize(QSize(1350, 700))
        self.horizontalLayout_3 = QHBoxLayout(self.Visor3D)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Canvas3D = Visor(self.Visor3D)
        self.Canvas3D.setObjectName(u"Canvas3D")
        self.Canvas3D.setStyleSheet(u"QOpenGLWidget{\n"
"background-color: rgb(2012,210,215);\n"
"border: 2px solid rgb(255,255,255);\n"
"}")

        self.horizontalLayout_3.addWidget(self.Canvas3D)

        self.GUIControls = QWidget(self.centralwidget)
        self.GUIControls.setObjectName(u"GUIControls")
        self.GUIControls.setGeometry(QRect(0, 700, 1366, 300))
        self.GUIControls.setMinimumSize(QSize(1366, 0))
        self.GUIControls.setMaximumSize(QSize(1366, 300))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush11 = QBrush(QColor(254, 172, 0, 255))
        brush11.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush11)
        palette1.setBrush(QPalette.Active, QPalette.Light, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Dark, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush11)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush11)
        palette1.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Active, QPalette.AlternateBase, brush3)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipText, brush3)
        brush12 = QBrush(QColor(255, 255, 255, 128))
        brush12.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush11)
        palette1.setBrush(QPalette.Inactive, QPalette.Light, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Dark, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush11)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush11)
        palette1.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush11)
        palette1.setBrush(QPalette.Disabled, QPalette.Light, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Dark, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush11)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush11)
        palette1.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        self.GUIControls.setPalette(palette1)
        self.GUIControls.setStyleSheet(u"background-color: rgb(254,172,0);color: white;")
        self.horizontalLayout_10 = QHBoxLayout(self.GUIControls)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.PanelRow3_2 = QWidget(self.GUIControls)
        self.PanelRow3_2.setObjectName(u"PanelRow3_2")
        self.PanelRow3_2.setMaximumSize(QSize(320, 300))
        self.PanelRow3 = QVBoxLayout(self.PanelRow3_2)
        self.PanelRow3.setObjectName(u"PanelRow3")
        self.btn_guardar = QPushButton(self.PanelRow3_2)
        self.btn_guardar.setObjectName(u"btn_guardar")
        self.btn_guardar.setMaximumSize(QSize(320, 320))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush13 = QBrush(QColor(54, 54, 54, 255))
        brush13.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush13)
        palette2.setBrush(QPalette.Active, QPalette.Text, brush)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush13)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush13)
        brush14 = QBrush(QColor(255, 255, 255, 128))
        brush14.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush13)
        palette2.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush13)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush13)
        brush15 = QBrush(QColor(255, 255, 255, 128))
        brush15.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush13)
        palette2.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush13)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush13)
        brush16 = QBrush(QColor(255, 255, 255, 128))
        brush16.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        self.btn_guardar.setPalette(palette2)
        self.btn_guardar.setStyleSheet(u"QPushButton{\n"
"background-color: rgb(54,54,54);\n"
"font-size:64px;\n"
"border: 1px solid rgb(54,54,54);\n"
"border-radius: 25%\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(76,76,76);\n"
"}")

        self.PanelRow3.addWidget(self.btn_guardar)


        self.horizontalLayout_10.addWidget(self.PanelRow3_2)

        self.PanelRow2 = QWidget(self.GUIControls)
        self.PanelRow2.setObjectName(u"PanelRow2")
        self.PanelRow2.setMinimumSize(QSize(300, 300))
        self.PanelRow2.setMaximumSize(QSize(320, 300))
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush17 = QBrush(QColor(254, 190, 40, 255))
        brush17.setStyle(Qt.SolidPattern)
        palette3.setBrush(QPalette.Active, QPalette.Button, brush17)
        palette3.setBrush(QPalette.Active, QPalette.Light, brush3)
        palette3.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        palette3.setBrush(QPalette.Active, QPalette.Dark, brush3)
        palette3.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette3.setBrush(QPalette.Active, QPalette.Text, brush)
        palette3.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush17)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush17)
        palette3.setBrush(QPalette.Active, QPalette.Shadow, brush3)
        palette3.setBrush(QPalette.Active, QPalette.AlternateBase, brush3)
        palette3.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette3.setBrush(QPalette.Active, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette3.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Button, brush17)
        palette3.setBrush(QPalette.Inactive, QPalette.Light, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.Dark, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush17)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush17)
        palette3.setBrush(QPalette.Inactive, QPalette.Shadow, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette3.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette3.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Button, brush17)
        palette3.setBrush(QPalette.Disabled, QPalette.Light, brush3)
        palette3.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette3.setBrush(QPalette.Disabled, QPalette.Dark, brush3)
        palette3.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette3.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush17)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush17)
        palette3.setBrush(QPalette.Disabled, QPalette.Shadow, brush3)
        palette3.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush3)
        palette3.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette3.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        self.PanelRow2.setPalette(palette3)
        self.PanelRow2.setStyleSheet(u"background-color: rgb(254,190,40);")
        self.verticalLayout_3 = QVBoxLayout(self.PanelRow2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalWidget_7 = QWidget(self.PanelRow2)
        self.horizontalWidget_7.setObjectName(u"horizontalWidget_7")
        self.horizontalWidget_7.setMaximumSize(QSize(300, 60))
        self.horizontalLayout_12 = QHBoxLayout(self.horizontalWidget_7)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.btn_dedo_primero = QPushButton(self.horizontalWidget_7)
        self.btn_dedo_primero.setObjectName(u"btn_dedo_primero")
        self.btn_dedo_primero.setMinimumSize(QSize(50, 50))
        self.btn_dedo_primero.setMaximumSize(QSize(50, 50))
        self.btn_dedo_primero.setStyleSheet(u"QPushButton{\n"
"background-color:rgb(54,54,54);\n"
"font-size:24px;\n"
"border: 1px solid rgb(54,54,54);\n"
"border-radius: 10%\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(74,74,74);\n"
"}")
        self.btn_dedo_primero.clicked.connect(self.ComandDP)
        self.horizontalLayout_12.addWidget(self.btn_dedo_primero)

        self.txt_dedo_primero = QLabel(self.horizontalWidget_7)
        self.txt_dedo_primero.setObjectName(u"txt_dedo_primero")
        self.txt_dedo_primero.setMaximumSize(QSize(300, 60))
        font = QFont()
        font.setFamily(u"Arial")
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.txt_dedo_primero.setFont(font)
        self.txt_dedo_primero.setStyleSheet(u"QLabel{\n"
"	color:white;\n"
"    font-size: 36px;\n"
"    font-family: Arial;\n"
"    text-decoration: underline;\n"
"}")

        self.horizontalLayout_12.addWidget(self.txt_dedo_primero)


        self.verticalLayout_3.addWidget(self.horizontalWidget_7)

        self.PanelCol5 = QWidget(self.PanelRow2)
        self.PanelCol5.setObjectName(u"PanelCol5")
        self.PanelCol5.setMaximumSize(QSize(300, 60))
        self.horizontalLayout_11 = QHBoxLayout(self.PanelCol5)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.btn_dedo_segundo = QPushButton(self.PanelCol5)
        self.btn_dedo_segundo.setObjectName(u"btn_dedo_segundo")
        self.btn_dedo_segundo.setMinimumSize(QSize(50, 50))
        self.btn_dedo_segundo.setMaximumSize(QSize(50, 50))
        self.btn_dedo_segundo.setStyleSheet(u"QPushButton{\n"
"background-color:rgb(54,54,54);\n"
"font-size:24px;\n"
"border: 1px solid rgb(54,54,54);\n"
"border-radius: 10%\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(74,74,74);\n"
"}")

        self.horizontalLayout_11.addWidget(self.btn_dedo_segundo)

        self.txt_dedo_segundo = QLabel(self.PanelCol5)
        self.txt_dedo_segundo.setObjectName(u"txt_dedo_segundo")
        self.txt_dedo_segundo.setMaximumSize(QSize(300, 60))
        self.txt_dedo_segundo.setFont(font)
        self.txt_dedo_segundo.setStyleSheet(u"QLabel{\n"
"	color:white;\n"
"    font-size: 36px;\n"
"    font-family: Arial;\n"
"    text-decoration: underline;\n"
"}")

        self.horizontalLayout_11.addWidget(self.txt_dedo_segundo)


        self.verticalLayout_3.addWidget(self.PanelCol5)

        self.panelCol6 = QWidget(self.PanelRow2)
        self.panelCol6.setObjectName(u"panelCol6")
        self.panelCol6.setMaximumSize(QSize(300, 60))
        self.horizontalLayout_9 = QHBoxLayout(self.panelCol6)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.btn_dedo_tercero = QPushButton(self.panelCol6)
        self.btn_dedo_tercero.setObjectName(u"btn_dedo_tercero")
        self.btn_dedo_tercero.setMinimumSize(QSize(50, 50))
        self.btn_dedo_tercero.setMaximumSize(QSize(50, 50))
        self.btn_dedo_tercero.setStyleSheet(u"QPushButton{\n"
"background-color:rgb(54,54,54);\n"
"font-size:24px;\n"
"border: 1px solid rgb(54,54,54);\n"
"border-radius: 10%\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(74,74,74);\n"
"}")

        self.horizontalLayout_9.addWidget(self.btn_dedo_tercero)

        self.txt_dedo_tercero = QLabel(self.panelCol6)
        self.txt_dedo_tercero.setObjectName(u"txt_dedo_tercero")
        self.txt_dedo_tercero.setMaximumSize(QSize(300, 60))
        self.txt_dedo_tercero.setFont(font)
        self.txt_dedo_tercero.setStyleSheet(u"QLabel{\n"
"	color:white;\n"
"    font-size: 36px;\n"
"    font-family: Arial;\n"
"    text-decoration: underline;\n"
"}")

        self.horizontalLayout_9.addWidget(self.txt_dedo_tercero)


        self.verticalLayout_3.addWidget(self.panelCol6)

        self.PanelCol4 = QWidget(self.PanelRow2)
        self.PanelCol4.setObjectName(u"PanelCol4")
        self.PanelCol4.setMaximumSize(QSize(300, 60))
        self.horizontalLayout_8 = QHBoxLayout(self.PanelCol4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btn_dedo_cuarto = QPushButton(self.PanelCol4)
        self.btn_dedo_cuarto.setObjectName(u"btn_dedo_cuarto")
        self.btn_dedo_cuarto.setMinimumSize(QSize(50, 50))
        self.btn_dedo_cuarto.setMaximumSize(QSize(50, 50))
        self.btn_dedo_cuarto.setStyleSheet(u"QPushButton{\n"
"background-color:rgb(54,54,54);\n"
"font-size:24px;\n"
"border: 1px solid rgb(54,54,54);\n"
"border-radius: 10%\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(74,74,74);\n"
"}")

        self.horizontalLayout_8.addWidget(self.btn_dedo_cuarto)

        self.txt_dedo_cuarto = QLabel(self.PanelCol4)
        self.txt_dedo_cuarto.setObjectName(u"txt_dedo_cuarto")
        self.txt_dedo_cuarto.setMaximumSize(QSize(300, 60))
        self.txt_dedo_cuarto.setFont(font)
        self.txt_dedo_cuarto.setStyleSheet(u"QLabel{\n"
"	color:white;\n"
"    font-size: 36px;\n"
"    font-family: Arial;\n"
"    text-decoration: underline;\n"
"}")

        self.horizontalLayout_8.addWidget(self.txt_dedo_cuarto)


        self.verticalLayout_3.addWidget(self.PanelCol4)


        self.horizontalLayout_10.addWidget(self.PanelRow2)

        self.PanelRow1 = QWidget(self.GUIControls)
        self.PanelRow1.setObjectName(u"PanelRow1")
        self.PanelRow1.setEnabled(True)
        self.PanelRow1.setMinimumSize(QSize(300, 300))
        self.PanelRow1.setMaximumSize(QSize(320, 300))
        palette4 = QPalette()
        palette4.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Button, brush17)
        palette4.setBrush(QPalette.Active, QPalette.Light, brush3)
        palette4.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        palette4.setBrush(QPalette.Active, QPalette.Dark, brush3)
        palette4.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette4.setBrush(QPalette.Active, QPalette.Text, brush)
        palette4.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette4.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Base, brush17)
        palette4.setBrush(QPalette.Active, QPalette.Window, brush17)
        palette4.setBrush(QPalette.Active, QPalette.Shadow, brush3)
        palette4.setBrush(QPalette.Active, QPalette.AlternateBase, brush3)
        palette4.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette4.setBrush(QPalette.Active, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette4.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Button, brush17)
        palette4.setBrush(QPalette.Inactive, QPalette.Light, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.Dark, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Base, brush17)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush17)
        palette4.setBrush(QPalette.Inactive, QPalette.Shadow, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette4.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        palette4.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.Button, brush17)
        palette4.setBrush(QPalette.Disabled, QPalette.Light, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.Dark, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush17)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush17)
        palette4.setBrush(QPalette.Disabled, QPalette.Shadow, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette4.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
#endif
        self.PanelRow1.setPalette(palette4)
        self.PanelRow1.setStyleSheet(u"background-color: rgb(254,190,40);")
        self.verticalLayout = QVBoxLayout(self.PanelRow1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.PanelCol1 = QWidget(self.PanelRow1)
        self.PanelCol1.setObjectName(u"PanelCol1")
        self.PanelCol1.setMaximumSize(QSize(300, 60))
        self.horizontalLayout_7 = QHBoxLayout(self.PanelCol1)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.btn_dedo_quinto = QPushButton(self.PanelCol1)
        self.btn_dedo_quinto.setObjectName(u"btn_dedo_quinto")
        self.btn_dedo_quinto.setMinimumSize(QSize(50, 50))
        self.btn_dedo_quinto.setMaximumSize(QSize(50, 50))
        self.btn_dedo_quinto.setStyleSheet(u"QPushButton{\n"
"background-color:rgb(54,54,54);\n"
"font-size:24px;\n"
"border: 1px solid rgb(54,54,54);\n"
"border-radius: 10%\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(74,74,74);\n"
"}")

        self.horizontalLayout_7.addWidget(self.btn_dedo_quinto)

        self.txt_dedo_quinto = QLabel(self.PanelCol1)
        self.txt_dedo_quinto.setObjectName(u"txt_dedo_quinto")
        self.txt_dedo_quinto.setMaximumSize(QSize(300, 60))
        self.txt_dedo_quinto.setFont(font)
        self.txt_dedo_quinto.setStyleSheet(u"QLabel{\n"
"	color:white;\n"
"    font-size: 36px;\n"
"    font-family: Arial;\n"
"    text-decoration: underline;\n"
"}")

        self.horizontalLayout_7.addWidget(self.txt_dedo_quinto)


        self.verticalLayout.addWidget(self.PanelCol1)

        self.PanelCol2 = QWidget(self.PanelRow1)
        self.PanelCol2.setObjectName(u"PanelCol2")
        self.PanelCol2.setMaximumSize(QSize(300, 60))
        self.horizontalLayout_6 = QHBoxLayout(self.PanelCol2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_cuerpo_pie = QPushButton(self.PanelCol2)
        self.btn_cuerpo_pie.setObjectName(u"btn_cuerpo_pie")
        self.btn_cuerpo_pie.setMinimumSize(QSize(50, 50))
        self.btn_cuerpo_pie.setMaximumSize(QSize(50, 50))
        self.btn_cuerpo_pie.setStyleSheet(u"QPushButton{\n"
"background-color:rgb(54,54,54);\n"
"font-size:24px;\n"
"border: 1px solid rgb(54,54,54);\n"
"border-radius: 10%\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(74,74,74);\n"
"}")

        self.horizontalLayout_6.addWidget(self.btn_cuerpo_pie)

        self.txt_cuerpo_pie = QLabel(self.PanelCol2)
        self.txt_cuerpo_pie.setObjectName(u"txt_cuerpo_pie")
        self.txt_cuerpo_pie.setMaximumSize(QSize(300, 60))
        self.txt_cuerpo_pie.setFont(font)
        self.txt_cuerpo_pie.setStyleSheet(u"QLabel{\n"
"	color:white;\n"
"    font-size: 36px;\n"
"    font-family: Arial;\n"
"    text-decoration: underline;\n"
"}")

        self.horizontalLayout_6.addWidget(self.txt_cuerpo_pie)


        self.verticalLayout.addWidget(self.PanelCol2)

        self.PanelCol3 = QWidget(self.PanelRow1)
        self.PanelCol3.setObjectName(u"PanelCol3")
        self.PanelCol3.setMaximumSize(QSize(300, 60))
        self.horizontalLayout_5 = QHBoxLayout(self.PanelCol3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btn_talon = QPushButton(self.PanelCol3)
        self.btn_talon.setObjectName(u"btn_talon")
        self.btn_talon.setMinimumSize(QSize(50, 50))
        self.btn_talon.setMaximumSize(QSize(50, 50))
        self.btn_talon.setStyleSheet(u"QPushButton{\n"
"background-color:rgb(54,54,54);\n"
"font-size:24px;\n"
"border: 1px solid rgb(54,54,54);\n"
"border-radius: 10%\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(74,74,74);\n"
"}")

        self.horizontalLayout_5.addWidget(self.btn_talon)

        self.txt_talon = QLabel(self.PanelCol3)
        self.txt_talon.setObjectName(u"txt_talon")
        self.txt_talon.setMaximumSize(QSize(300, 60))
        self.txt_talon.setFont(font)
        self.txt_talon.setStyleSheet(u"QLabel{\n"
"	color:white;\n"
"    font-size: 36px;\n"
"    font-family: Arial;\n"
"    text-decoration: underline;\n"
"}")

        self.horizontalLayout_5.addWidget(self.txt_talon)


        self.verticalLayout.addWidget(self.PanelCol3)


        self.horizontalLayout_10.addWidget(self.PanelRow1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionestilos.setText(QCoreApplication.translate("MainWindow", u"estilos", None))
#if QT_CONFIG(tooltip)
        self.actionestilos.setToolTip(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_guardar.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
        self.btn_dedo_primero.setText(QCoreApplication.translate("MainWindow", u"DP", None))
        self.txt_dedo_primero.setText(QCoreApplication.translate("MainWindow", u"Dedo Primero", None))
        self.btn_dedo_segundo.setText(QCoreApplication.translate("MainWindow", u"DS", None))
        self.txt_dedo_segundo.setText(QCoreApplication.translate("MainWindow", u"Dedo Segundo", None))
        self.btn_dedo_tercero.setText(QCoreApplication.translate("MainWindow", u"DT", None))
        self.txt_dedo_tercero.setText(QCoreApplication.translate("MainWindow", u"Dedo Tercero", None))
        self.btn_dedo_cuarto.setText(QCoreApplication.translate("MainWindow", u"DC", None))
        self.txt_dedo_cuarto.setText(QCoreApplication.translate("MainWindow", u"dedo Cuarto", None))
        self.btn_dedo_quinto.setText(QCoreApplication.translate("MainWindow", u"DQ", None))
        self.txt_dedo_quinto.setText(QCoreApplication.translate("MainWindow", u"Dedo Quinto", None))
        self.btn_cuerpo_pie.setText(QCoreApplication.translate("MainWindow", u"CP", None))
        self.txt_cuerpo_pie.setText(QCoreApplication.translate("MainWindow", u"Cuerpo Pie", None))
        self.btn_talon.setText(QCoreApplication.translate("MainWindow", u"TA", None))
        self.txt_talon.setText(QCoreApplication.translate("MainWindow", u"Talon", None))
        self.btn_talon.clicked.connect(self.ComandT)
    # retranslateUi
    def ComandDP(self):
        hilo = Thread(target=self.Canvas3D.obj.Animacion,args=(-60.0,0.0,-90.0,0.5,0.1,-4.2,5.0,5.0,5.0))
        hilo.start()
    def ComandT(self):
        hilo = Thread(target=self.Canvas3D.obj.Animacion,args=(180.0,0.0,0.0,-3.0,0.0,0.0,6.0,6.0,6.0))
        hilo.start()
    def ComandCP(slef):
        pass
    def Animacion(self,anX,anY,anZ,disx,disy,disz,scx,scy,scz,t=2.0):
        m=int(t/0.005)
        dx = (anX - self.Canvas3D.rotX)/m
        dy = (anY - self.Canvas3D.rotY)/m
        dz = (anZ - self.Canvas3D.rotZ)/m
        dsx = (disx-self.Canvas3D.trasX)/m
        dsy = (disy-self.Canvas3D.trasY)/m
        dsz = (disz-self.Canvas3D.trasZ)/m
        sx  = (scx - self.Canvas3D.scX)/m
        sy  = (scy - self.Canvas3D.scY)/m
        sz  = (scz - self.Canvas3D.scZ)/m
        for l in range(m):
            self.Canvas3D.rotX += dx
            self.Canvas3D.rotY += dy
            self.Canvas3D.rotZ += dz
            self.Canvas3D.trasX += dsx
            self.Canvas3D.trasY += dsy
            self.Canvas3D.trasZ += dsz
            self.Canvas3D.scX += sx
            self.Canvas3D.scY += sy
            self.Canvas3D.scZ += sz
            time.sleep(0.005)
        print('dx:{},dy:{},dz:{},rotx:{},roty:{},rotz:{},scx:{},scy:{},scz:{}'.format(self.Canvas3D.trasX,self.Canvas3D.trasY,self.Canvas3D.trasZ,self.Canvas3D.rotX,self.Canvas3D.rotY,self.Canvas3D.rotZ,self.Canvas3D.scX,self.Canvas3D.scY,self.Canvas3D.scZ))
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    timer = QTimer(MainWindow)
    timer.setInterval(5)
    timer.timeout.connect(ui.Canvas3D.updateGL)
    timer.start()
    MainWindow.show()
    sys.exit(app.exec_())
