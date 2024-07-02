import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
from cv2 import getRotationMatrix2D
from cv2 import warpAffine
import time
from mrcnn.config import Config
from mrcnn import model as modellib
import os
from threading import Thread
model_filename = "mask_rcnn_pies_0009.h5"
class_names = ['may','Dedo-Primero','Dedo-Segundo','Dedo-Tercero','Dedo-Cuarto','Dedo-Quinto','Cuerpo-Pie','Talon']
min_confidence = 0.6
M = getRotationMatrix2D((1920//2,1080//2),90,1)
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

class Dilog():
    def __init__(self,parent:tk.Tk):
        self.top = tk.Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        self.db = DataBase()
        self.lbl_name = tk.Label(self,text='Nombre:     ')
        self.lbl_name.place(x=20,y=50,width=100,height=50)
        self.lbl_ApellidoP = tk.Label(self.top,text='Apellido P: ')
        self.lbl_ApellidoP.place(x=20,y=110,width=100,height=50)
        self.lbl_ApellidoM = tk.Label(self.top,text='Apellido M: ')
        self.lbl_ApellidoM.place(x=20,y=170,width=100,height=50)
        self.lbl_DNI = tk.Label(self.top,text='DNI:        ')
        self.lbl_DNI.place(x=20,y=230,width=100,height=50)
        self.in_name = tk.Entry(self.top)
        self.in_name.place(x=200,y=50,width=200,height=50)
        self.in_ApellidoP = tk.Entry(self.top)
        self.in_ApellidoP.place(x=200,y=110,width=200,height=50)
        self.in_ApellidoM = tk.Entry(self.top)
        self.in_ApellidoM.place(x=200,y=170,width=200,height=50)
        self.in_DNI = tk.Entry(self.top)
        self.in_DNI.place(x=200,y=230,width=200,height=50)
    def Guardar(self):
 	pass


class PanelResultado(tk.Frame):
    def __init__(self,title,master=None,V=None):
        tk.Frame.__init__(self,master)
        self.V=V
        self.master.title(title)
        self.btn_estimar = tk.Button(self,text="Estimar",font=("Arial",24),command=self.Estimar)
        self.btn_estimar.place(x=0,y=760,width=400,height=60)
        self.btn_ingresar = tk.Button(self,text="Ingresar Cliente",font=("Arial",24),command=self.Ingresar)
        #self.btn_ingresar.place(x=0,y=20,width=400,height=60)

    def Ingresar(self):
        d = Dilog(parent=self.master)
        self.master.wait_window(d)
    def Estimar(self):
        #self.V.permiso=True
        self.img = cvtColor(self.img,COLOR_BGR2RGB)
        self.img2= cvtColor(self.img2,COLOR_BGR2RGB)
        #imwrite('pieD.jpg',self.img.copy())
        result = model.detect([self.img.copy()],verbose=1)
        result2= model.detect([self.img2.copy()],verbose=1)
        r =result[0]
        r2=result2[1]
        dx=0
        ancho=0
        objs=list()
        Talon=[]
        dx2=0
        ancho2=0
        objs2=list()
        Talon2=[]
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
        for i,obj in enumerate(r2['rois']):
            box=obj
            label = class_names[r2['class_ids'][i]]
            objs2.append([box,label])
            if label == 'Cuerpo-Pie':
                ancho2 = abs(box[0]-box[2])
            if label == 'Talon':
                Talon2 = box
        for i,value in enumerate(objs2):
            aux = abs(Talon2[3]-value[0][1])
            if dx2 < aux:
                dx2=aux
        self.largo.set("Largo Pie: "+str(round(dx*0.014561500275786,2))+'cm')
        self.ancho.set("Ancho Pie: "+str(round(ancho*0.0155793573515093,2))+'cm')
        self.largo2.set("Largo Pie: "+str(round(dx2*0.014561500275786,2))+'cm')
        self.ancho2.set("Ancho Pie: "+str(round(ancho2*0.0155793573515093,2))+'cm')
        time.sleep(0.01)


class Visor(tk.Frame):
    def __init__(self,title,master=None,vid=None,vid2=None):
        tk.Frame.__init__(self,master)
        #self.master=master
        self.master.title(title)
        self.vid=vid
        self.vid2=vid2
        self.fig = Figure(figsize=(8, 10), dpi=100)
        self.axes = [self.fig.add_subplot(121),self.fig.add_subplot(122)]
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.frame = np.zeros((1080,1920,3))
        self.frame2= np.zeros((1080,1920,3))
        self.im = self.axes[0].imshow(self.frame)
        self.im2 = self.axes[1].imshow(self.frame2)
        self.ret=False
        self.ret2=False
        self.permiso=False
        self.ani = FuncAnimation(self.fig, self.Draw, interval=20,blit=True)
    def Draw(self,i):
        self.ret , self.frame = self.vid.read()
        self.ret2 , self.frame2 = self.vid2.read()
        if self.ret2:
            self.frame2 = cvtColor(self.frame2,COLOR_BGR2RGB)
            img = warpAffine(self.frame2,M,(1920//2,1080//2))
            self.im2.set_data(img)
        if self.ret:
            self.frame = cvtColor(self.frame,COLOR_BGR2RGB)
            img2 = warpAffine(self.frame,M,(1920//2,1080//2))
            self.im.set_data(img2)
        time.sleep(0.001)
        return self.axes
