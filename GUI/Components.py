import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np
from cv2 import cvtColor
from cv2 import COLOR_BGR2RGB
from cv2 import imwrite,imread
from threading import Thread
from cv2 import VideoCapture
from cv2 import line
import time
from mrcnn.config import Config
from mrcnn import model as modellib
import os
from threading import Thread
model_filename = "mask_rcnn_pies_0009.h5"
class_names = ['may','Dedo-Primero','Dedo-Segundo','Dedo-Tercero','Dedo-Cuarto','Dedo-Quinto','Cuerpo-Pie','Talon']
min_confidence = 0.6

class CascoConfig(Config):
    NAME = "pies"

    # Train on 1 GPU and 1 image per GPU. Batch size is 1 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 7

    # All of our training images are 512x512
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512

    # You can experiment with this number to see if it improves training
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

class PanelResultado(tk.Frame):
    def __init__(self,title,master=None,V=None):
        tk.Frame.__init__(self,master)
        self.V=V
        self.master.title(title)
        self.btn_estimar = tk.Button(self,text="Estimar",font=("Arial",24),command=self.Estimar)
        self.btn_estimar.place(x=50,y=40,width=120,height=60)
        self.largo = tk.StringVar()
        self.largo.set("Largo Pie: ")
        self.ancho = tk.StringVar()
        self.ancho.set("Ancho Pie: ")
        self.lbl_largo = tk.Label(self,textvariable=self.largo,font=("Arial",24))
        self.lbl_largo.place(x=200,y=40,width=600,height=60)
        self.lbl_largo = tk.Label(self,textvariable=self.ancho,font=("Arial",24))
        self.lbl_largo.place(x=200,y=120,width=600,height=60)
        self.img = np.zeros((1080,1920,3))
    def Estimar(self):
        #self.V.permiso=True
        self.btn_estimar['state']="disable"
        self.img = cvtColor(self.img,COLOR_BGR2RGB)
        imwrite('pie.jpg',self.img.copy())
        result = model.detect([self.img.copy()],verbose=1)
        r=result[0]
        dx=0
        ancho=0
        objs=list()
        Talon=[]
        for i,obj in enumerate(r['rois']):
            box=obj
            label = class_names[r['class_ids'][i]]
            objs.append([box,label])
            if label == 'Cuerpo-Pie':
                ancho = abs(box[0]-box[2])
            if label == 'Talon':
                Talon = box
        for i,value in enumerate(objs):
            aux = abs(Talon[3]-value[0][1])
            if dx < aux:
                dx=aux
        self.largo.set("Largo Pie: "+str(round(dx*0.014561500275786,2)))
        self.ancho.set("Ancho Pie: "+str(round(ancho*0.0155793573515093,2)))
        self.btn_estimar['state']="normal"
        time.sleep(0.01)
class Visor(tk.Frame):
    def __init__(self,title,master=None,vid=None):
        tk.Frame.__init__(self,master)
        self.master.title(title)
        self.vid=vid
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        #self.toolbar.update()
        #self.canvas.get_tk_widget().pack(padx=5,pady=5,fill='both', expand=1)
        self.canvas.draw()
        self.ret,self.frame = self.vid.read()
        self.im = self.axes.imshow(self.frame)
        #self.ret=False
        self.permiso=False
        self.ani = FuncAnimation(self.fig, self.Draw, interval=20,blit=True)
    def Draw(self,i):
        self.ret , self.frame = self.vid.read()
        if self.ret:
            self.frame = cvtColor(self.frame,COLOR_BGR2RGB)
            self.im.set_data(self.frame)
        time.sleep(0.01)
        return self.axes, self.im
