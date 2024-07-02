import os
import json
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton,QMessageBox
from mrcnn.config import Config
from mrcnn import model as modellib
import numpy as np
import time
import requests
from threading import Thread
import cv2
from cv2 import COLOR_BGR2RGB
from cv2 import cvtColor
from cv2 import VideoCapture
from cv2 import warpAffine
from cv2 import imread
from threading import Timer
import imutils
T = np.array([[0,1,1],[1,0,-1]],dtype=np.float32)
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
    DETECTION_MIN_CONFIDENCE = min_confidence

inference_config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference", config=inference_config,  model_dir='logs')
model_path = os.path.join('logs/pies20210806T1743', model_filename)
model.load_weights(model_path, by_name=True)
im = imread('pie.jpg')
im = cvtColor(im,COLOR_BGR2RGB)
re=model.detect([im],verbose=1)

class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Soy un popup")
        self.setFixedSize(200, 100)

class Ui_MainWindow(object):
    def __init__(self):
        pass
    def apagarLuces(self):
        response = requests.get('http://192.168.0.31:5000/comandos?command=Apagar')
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.vid  = VideoCapture('http://192.168.0.31:5000/video_feed1')
        self.vid2 = VideoCapture('http://192.168.0.31:5000/video_feed2')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1920, 900))
        self.widget.setStyleSheet("background-color: rgb(54,54,54)\n")
        self.widget.setObjectName("widget")
        self.CamaraDerecha = QtWidgets.QLabel(self.widget)
        self.CamaraDerecha.setGeometry(QtCore.QRect(300, 60, 450, 800))
        self.CamaraDerecha.setStyleSheet("background-color:white")
        self.CamaraDerecha.setText("")
        self.CamaraDerecha.setObjectName("CamaraDerecha")
        self.CamaraIzquierda = QtWidgets.QLabel(self.widget)
        self.CamaraIzquierda.setGeometry(QtCore.QRect(1170, 60, 450, 800))
        self.CamaraIzquierda.setStyleSheet("background-color:white")
        self.CamaraIzquierda.setText("")
        self.CamaraIzquierda.setObjectName("CamaraIzquierda")        
        self.panel_botones = QtWidgets.QWidget(self.centralwidget)
        self.panel_botones.setGeometry(QtCore.QRect(0, 900, 1920, 180))
        self.panel_botones.setStyleSheet("background-color: rgb(204,122,0);")
        self.panel_botones.setObjectName("panel_botones")
        self.icono = QtWidgets.QLabel(self.panel_botones)
        self.icono.setGeometry(QtCore.QRect(1520, 0, 400, 150))
        self.icono.setText("")
        self.icono.setObjectName("LOGO")
        self.btn_captura = QtWidgets.QPushButton(self.widget)
        self.btn_captura.setGeometry(QtCore.QRect(860, 440, 200, 200))
        self.btn_captura.setStyleSheet("QPushButton{\n"
                                    "    background-color: rgb(20,20,20);\n"
                                    "    color:  white;\n"
                                    "    font-size: 28px;\n"
                                    "    box-sizing: border-box;\n"
                                    "    border-radius:15%;\n"
                                    "    width: 200px;\n"
                                    "    height: 200px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "    background-color: rgb(84,84,84);\n"
                                    "}")
        self.btn_captura.setObjectName("btn_captura")
        self.btn_captura.clicked.connect(self.Estimar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.img = np.zeros((800,450,3),dtype=np.uint8)
        self.logo=imread('OCTOSCAN.png')
        self.logo=cvtColor(self.logo,COLOR_BGR2RGB)
        self.logo = imutils.resize(self.logo,width=400)
        logo = QImage(self.logo,self.logo.shape[1],self.logo.shape[0],self.logo.strides[0],QImage.Format_RGB888)
        self.icono.setPixmap(QPixmap.fromImage(logo))
        image = QImage(self.img,self.img.shape[1],self.img.shape[0],self.img.strides[0],QImage.Format_RGB888)
        self.CamaraIzquierda.setPixmap(QPixmap.fromImage(image))
        self.img2 = np.zeros((800,450,3),dtype=np.uint8)
        image = QImage(self.img2,self.img2.shape[1],self.img2.shape[0],self.img2.strides[0],QImage.Format_RGB888)
        self.derecho=[0,0,0,0,0,0,0]
        self.izquierdo=[0,0,0,0,0,0,0]
        self.CamaraIzquierda.setPixmap(QPixmap.fromImage(image))
        hilo = Thread(target=self.Captura)
        hilo.daemon = True
        hilo2 = Thread(target=self.Captura2)
        hilo2.daemon = True
        hilo2.start()
        hilo.start()
        self.aux=''
        self.aux2=''
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def Estimar(self):
        response=requests.get('http://192.168.0.31:5000/comandos?command=Iniciar')
        t0 = time.time()
        img = self.aux.copy()
        img2= self.aux2.copy()
        result = model.detect([img],verbose=1)
        result2= model.detect([img2],verbose=1)
        r =result[0]
        r2=result2[0]
        m = [r,r2]
        data={}
        data['derecho']={}
        data['izquierdo']={}
        data['derecho']['largo']=''
        data['derecho']['ancho']=''
        data['derecho']['talla']=''
        data['izquierdo']['largo']=''
        data['izquierdo']['ancho']=''
        data['izquierdo']['talla']=''
        if len(m[0]['class_ids']) != 0 and len(m[1]['class_ids']) != 0:
            for l,mc in enumerate(m):
                largos=list()
                co=np.zeros((1080,1920))
                ca=0
                for j,p in enumerate(mc):
                    co = np.array(mc['masks'][:,:,j].copy(),dtype=np.uint8)
                    co = np.where(co==1,255,co)
                    print(co.shape)
                    contours, _ = cv2.findContours(co,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    label = class_names[mc['class_ids'][j]]
                    (cx,cy),(w,h),angle = cv2.minAreaRect(contours[0])
                    if 'Dedo-Primero' == label:
                        py=cy - h/2
                        px=cx - w/2
                        largos.append([px,py]) 
                    if 'Talon' == label:
                        ty = cy + h/2
                        tx = cx + w/2
                        largos.append([tx,ty])
                    if 'Cuerpo-Pie' == label:
                        if w < h:
                            ca = w
                        else:
                            ca = h
                if l==0:
                    largo = ((largos[0][1]-largos[1][1])**2 + (largos[0][0]-largos[1][0])**2)**0.5 
                    data['derecho']['largo'] = str(largo)+'cm'
                    data['derecho']['ancho'] = str(ca)+'cm'
                    talla=0
                    if largo >= 25.33 and largo < 26:
                        dtalla=38
                    if largo >= 26 and largo < 26.67:
                        talla=39
                    if 26.67 <= largo and 27.33 > largo:
                        talla=40
                    if 27.33 <= largo and largo < 28:
                        talla=41
                    data['derecho']['talla']=str(talla)
                if  l==1:
                    largo = ((largos[0][1]-largos[1][1])**2 + (largos[0][0]-largos[1][0])**2)**0.5
                    data['izquierdo']['largo'] = str(largo)+'cm'
                    data['izquierdo']['ancho'] = str(ca)+'cm'
                    talla=0
                    if largo >= 25.33 and largo < 26:
                        talla=38
                    if largo >= 26 and largo < 26.67:
                        talla=39
                    if 26.67 <= largo and 27.33 > largo:
                        talla=40
                    if 27.33 <= largo and largo < 28:
                        talla=41
                    data['izquierdo']['talla']=str(talla)
                print(l)
        with open('Medidas\\Muestra.json','a') as file:
            json.dump(data,file)
        response=requests.get('http://192.168.0.31:5000/comandos?command=Acabado')
        #self.showDialog(data)
    def show_dialog(self):
        dialog = Dialog(self)  # self hace referencia al padre
        dialog.show()
    def showDialog(self,data):
        QMessageBox.warning(self, "Warning Dialog", "Peligro Alto Voltage")
        
    def Captura2(self):
        while True:
            self.ret2,self.img2 = self.vid2.read()
            if not self.ret2:
                continue
            self.img2 = cvtColor(self.img2,COLOR_BGR2RGB)
            self.aux2 = self.img2.copy()
            self.img2 = imutils.resize(self.img2,width=800)
            self.img2 = warpAffine(self.img2,T,(450,800))
            image = QImage(self.img2,self.img2.shape[1],self.img2.shape[0],self.img2.strides[0],QImage.Format_RGB888)
            self.CamaraDerecha.setPixmap(QPixmap.fromImage(image))
    def Captura(self):
        while True:
            self.ret,self.img = self.vid.read()
            if not self.ret:
                continue
            self.img = cvtColor(self.img,COLOR_BGR2RGB)
            self.aux = self.img.copy()
            self.img = imutils.resize(self.img,width=800)
            self.img = warpAffine(self.img,T,(450,800))
            image = QImage(self.img,self.img.shape[1],self.img.shape[0],self.img.strides[0],QImage.Format_RGB888)
            self.CamaraIzquierda.setPixmap(QPixmap.fromImage(image))
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_captura.setText(_translate("MainWindow", "CAPTURA"))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.apagarLuces()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())