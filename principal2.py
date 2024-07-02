# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'principal.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from cv2 import cvtColor
from puerto import *
from cv2 import imwrite
from cv2 import COLOR_BGR2RGB
from cv2 import getRotationMatrix2D
from cv2 import warpAffine
import time
import numpy as np
from mrcnn.config import Config
from mrcnn import model as modellib
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from cv2 import VideoCapture
from matplotlib.animation import FuncAnimation
T = np.array([[0,1,1],[1,0,-1]],dtype=np.float32)
co = ControlIluminacion()
model_filename = "mask_rcnn_pies_0009.h5"
class_names = ['may','Dedo-Primero','Dedo-Segundo','Dedo-Tercero','Dedo-Cuarto','Dedo-Quinto','Cuerpo-Pie','Talon']
min_confidence = 0.6
class CascoConfig(Config):
    NAME = "pies"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 7
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    STEPS_PER_EPOCH = 500
    VALIDATION_STEPS = 5
    BACKBONE = 'resnet50'
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)
    TRAIN_ROIS_PER_IMAGE = 32
    MAX_GT_INSTANCES = 50 
    POST_NMS_ROIS_INFERENCE = 500 
    POST_NMS_ROIS_TRAINING = 1000 
config = CascoConfig()
config.display()
class InferenceConfig(CascoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    #IMAGE_MIN_DIM = 512
    #IMAGE_MAX_DIM = 512
    DETECTION_MIN_CONFIDENCE = min_confidence
inference_config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference", config=inference_config,  model_dir='logs')
model_path = os.path.join('logs/pies20210806T1743', model_filename)
model.load_weights(model_path, by_name=True)
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=4, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

class Ui_MainWindow(object):
    def pasar(self):
        while True:
            if self.ret and self.ret2:
                self.img=self.frame.copy()
                self.img2=self.frame2.copy()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.vid = VideoCapture(0)
        self.vid2= VideoCapture(1)
        self.vid.set(3,1920)
        self.vid.set(4,1080)
        self.vid2.set(3,1920)
        self.vid2.set(4,1080)
        self.frame = np.zeros((1080,1920,3))
        self.frame2= np.zeros((1080,1920,3))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Camaras = QtWidgets.QWidget(self.centralwidget)
        self.Camaras.setGeometry(QtCore.QRect(0, 0, 1920, 900))
        self.Camaras.setStyleSheet("QWidget{\n"
"background-color: rgb(54,54,54);\n"
"}")
        self.Camaras.setObjectName("Camaras")
        self.CamaraIzquierda = QtWidgets.QWidget(self.Camaras)
        self.CamaraIzquierda.setGeometry(QtCore.QRect(200, 50, 600, 800))
        self.CamaraIzquierda.setStyleSheet("background-color:white")
        self.CamaraIzquierda.setObjectName("CamaraIzquierda")
        self.CamaraDerecha = QtWidgets.QWidget(self.Camaras)
        self.CamaraDerecha.setGeometry(QtCore.QRect(1020, 50, 600, 800))
        self.CamaraDerecha.setStyleSheet("background-color:white")
        self.CamaraDerecha.setObjectName("CamaraDerecha")
        self.PanelControl = QtWidgets.QWidget(self.centralwidget)
        self.PanelControl.setGeometry(QtCore.QRect(0, 900, 1920, 180))
        self.PanelControl.setStyleSheet("QWidget{\n"
"    background-color: rgb(254,172,0)\n"
"}")
        self.PanelControl.setObjectName("PanelControl")
        self.btn_captura = QtWidgets.QPushButton(self.PanelControl)
        self.btn_captura.setGeometry(QtCore.QRect(870, 0, 180, 180))
        self.btn_captura.setStyleSheet("QPushButton{\n"
"    background-color: rgb(54,54,54);\n"
"    color: white;\n"
"    border: 1px solid rgb(54,54,54);\n"
"    border-radius: 80%;\n"
"    box-sizing: border-box;\n"
"    margin: 10px 0 10px 0;\n"
"    font-size: 36px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(84,84,84);\n"
"}")
        self.btn_captura.setObjectName("btn_captura")
        self.btn_captura.clicked.connect(self.Captura)
        self.frame = np.zeros((1080,1920,3))
        self.frame2= np.zeros((1080,1920,3))
        self.btn_captura.setObjectName("btn_captura")
        self.sc = MplCanvas(parent=self.CamaraDerecha,width=5, height=10, dpi=100)
        self.sc2 = MplCanvas(parent=self.CamaraIzquierda,width=5, height=10, dpi=100)
        self.im=self.sc.axes.imshow(self.frame)
        self.im2=self.sc2.axes.imshow(self.frame2)

        la=QtWidgets.QVBoxLayout()
        la2=QtWidgets.QVBoxLayout()
        la.addWidget(self.sc)
        la2.addWidget(self.sc2)
        self.CamaraDerecha.setLayout(la)
        self.CamaraIzquierda.setLayout(la2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.ret=False
        self.ret2=False
        self.ani = FuncAnimation(self.sc.fig, self.Draw1, interval=20,blit=True)
        self.ani2 = FuncAnimation(self.sc2.fig, self.Draw2, interval=20,blit=True)
    def Draw2(self,i):
        self.ret2 , self.frame2 = self.vid2.read()
        if self.ret2:
            self.frame2 = cvtColor(self.frame2,COLOR_BGR2RGB)
            img = warpAffine(self.frame2,T,(1080,1920))
            self.im2.set_data(self.frame)
        time.sleep(0.001)
        return self.sc2.axes,
    def Captura(self):
        imwrite('pie.jpg',self.frame.copy())
    def Draw1(self,i):
        self.ret , self.frame = self.vid.read()
        if self.ret:
            self.frame = cvtColor(self.frame,COLOR_BGR2RGB)
            img2 = warpAffine(self.frame,T,(1080,1920))
            self.im.set_data(img2)
        time.sleep(0.001)
        return self.sc.axes,
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_captura.setText(_translate("MainWindow", "CAPTURA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

