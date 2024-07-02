import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot, image, transforms
from scipy import ndimage
import numpy as np
from cv2 import cvtColor
from cv2 import COLOR_BGR2RGB
from cv2 import ROTATE_90_CLOCKWISE
from cv2 import rotate
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
M = getRotationMatrix2D((0,0),-90,1.0) 
T = np.array([[0,1,1],[1,0,-1]],dtype=np.float32)
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
r=model.detect([cvtColor(imread('GUI/muestra.jpg'),COLOR_BGR2RGB)],verbose=1)
import pymysql
class Cliente():
    def __init__(self,name,AppellidoPaterno,ApellidoMaterno,TallaDerecha,TallaIzquierda,dni=None):
        self.name = name
        self.ApellidoPaterno = AppellidoPaterno
        self.ApellidoMaterno = ApellidoMaterno
        self.dni = dni
        self.TallaDerecha   = TallaDerecha
        self.TallaIzquierda =TallaIzquierda
class DataBase():
    def __init__(self):
        self.connections = pymysql.connect(
            host='localhost',
            user='root',
            password='fores753***',
            db='medidas'
        )
        self.cursor = self.connections.cursor()
        print("Coneccion exitosa")
    def select_user(self,dni):
        sql = 'SElECT nombre, apellidoPaterno, apellidoMaterno ,dni ,tallaDerecha,tallaIzquierda FROM clientes WHERE dni = {dni}'.format(dni)
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
        except Exception as e:
            print("No se consulto bien!")
    def insert_user(self,cli:Cliente):
        NAME = cli.name
        AP = cli.ApellidoPaterno
        AM = cli.ApellidoMaterno
        TD = cli.TallaDerecha
        TI = cli.TallaIzquierda
        DNI= cli.dni
        if DNI == None:
            sql = 'INSERT INTO clientes(nombre,apellidoPaterno,apellidoMaterno,tallaDerecha,tallaIzquierda) VALUES({name},{AP},{AM},{TD},{TI})'.format(NAME,AP,AM,TD,TI)
        else:
            sql = 'INSERT INTO clientes(nombre,apellidoPaterno,apellidoMaterno,tallaDerecha,tallaIzquierda,dni) VALUES({name},{AP},{AM},{TD},{TI},{DNI})'.format(NAME,AP,AM,TD,TI,DNI)
        try:
            self.cursor.execute(sql)
            resp=self.cursor.fetchone()
        except Exception as e:
            print("No se pudo insertar")
        
class Dilog():
    def __init__(self,parent):
        self.top = tk.Toplevel(parent)
        self.top.geometry("800x600+0+0")
        self.top.transient(parent)
        self.top.grab_set()
        #self.db = DataBase()
        self.lbl_name = tk.Label(self.top,text='Nombre:     ')
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
        self.btn_Guardar(self.top,text="Guardar",command=self.Guardar)
    def Guardar(self):
        cli=Cliente(self.in_name.get(),self.in_ApellidoP.get(),self.in_ApellidoM.get(),self.in_DNI.get())
        #self.db.insert_user(cli)

class PanelResultado(tk.Frame):
    def __init__(self,title,master=None,V=None):
        tk.Frame.__init__(self,master)
        self.root=master
        self.V=V
        self.master.title(title)
        self.load   = Image.open("GUI/descarga.png")
        self.load.resize((80, 80), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(self.load)
        self.frame_derecho = tk.Frame(self)
        self.frame_derecho.place(x=0,y=20,width=500,height=280)
        self.frame_izquierdo = tk.Frame(self)
        self.frame_izquierdo.place(x=0,y=280,width=500,height=280)
        self.btn_estimar = tk.Button(self,command=self.Estimar,image=self.render)
        self.btn_estimar.place(x=150,y=600,width=200,height=200)
        self.lbl_btn_estimar = tk.Label(self,text="ESTIMAR",font=("Arial",28))
        self.lbl_btn_estimar.place(x=150,y=800,width=200,height=80)
        self.btn_ingresar = tk.Button(self,text="Ingresar Cliente",font=("Arial",32),command=self.Ingresar)
        self.btn_ingresar.place(x=0,y=900,width=500,height=100)
        self.lbl_pie_derecho = tk.Label(self.frame_derecho,text='Pie Derecho:',font=("Arial",28),fg='red',justify=tk.LEFT)
        self.lbl_pie_derecho.place(x=0,y=0,width=500,height=60)
        self.lbl_pie_izquierdo = tk.Label(self.frame_izquierdo,text='Pie Izquierdo:',font=("Arial",28),fg='red',justify=tk.LEFT)
        self.lbl_pie_izquierdo.place(x=0,y=0,width=500,height=60)
        self.largo = tk.StringVar()
        self.largo.set("Largo Pie: ")
        self.ancho = tk.StringVar()
        self.ancho.set("Ancho Pie: ")
        self.lbl_largo = tk.Label(self.frame_derecho,textvariable=self.largo,font=("Arial",24),justify=tk.LEFT)
        self.lbl_largo.place(x=0,y=60,width=500,height=60)
        self.lbl_ancho = tk.Label(self.frame_derecho,textvariable=self.ancho,font=("Arial",24),justify=tk.LEFT)
        self.lbl_ancho.place(x=0,y=120,width=500,height=60)
        self.largo2 = tk.StringVar()
        self.largo2.set("Largo Pie: ")
        self.ancho2 = tk.StringVar()
        self.ancho2.set("Ancho Pie: ")
        self.lbl_largo2 = tk.Label(self.frame_izquierdo,textvariable=self.largo2,font=("Arial",24),justify=tk.LEFT)
        self.lbl_largo2.place(x=0,y=60,width=500,height=60)
        self.lbl_ancho2 = tk.Label(self.frame_izquierdo,textvariable=self.ancho2,font=("Arial",24),justify=tk.LEFT)
        self.lbl_ancho2.place(x=0,y=120,width=500,height=60)
        self.img = np.zeros((1080,1920,3))
        self.img2 = np.zeros((1080,1920,3))
        self.derecho   = [0,0,0,0,0,0,0]
        self.izquierdo = [0,0,0,0,0,0,0]
    def Ingresar(self):
        d = Dilog(parent=self.root)
        self.master.wait_window(d.top)
    def Estimar(self):
        #self.V.permiso=True
        t0 = time.time()
        self.img = cvtColor(self.img,COLOR_BGR2RGB)
        self.img2= cvtColor(self.img2,COLOR_BGR2RGB)
        #imwrite('pieD.jpg',self.img.copy())
        result = model.detect([self.img.copy()],verbose=1)
        result2= model.detect([self.img2.copy()],verbose=1)
        r =result[0]
        r2=result2[0]
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
            if label=="Deo-Primero":
                self.derecho[0]=abs(box[0]-box[2])
            if label=="Deo-Segundo":
                self.derecho[1]=abs(box[0]-box[2])
            if label=="Deo-Tercero":
                self.derecho[2]=abs(box[0]-box[2])
            if label=="Deo-Cuarto":
                self.derecho[3]=abs(box[0]-box[2])
            if label=="Deo-Quinto":
                self.derecho[4]=abs(box[0]-box[2])
            if label == 'Cuerpo-Pie':
                ancho = abs(box[0]-box[2])
                self.derecho[5]=ancho
            if label == 'Talon':
                Talon = box
                self.derecho[6]=abs(box[0]-box[2])
        for i,value in enumerate(objs):
            aux = abs(Talon[3]-value[0][1])
            if dx < aux:
                dx=aux
        for i,obj in enumerate(r2['rois']):
            box=obj
            label = class_names[r2['class_ids'][i]]
            objs2.append([box,label])
            if label=="Deo-Primero":
                self.izquierdo[0]=abs(box[0]-box[2])
            if label=="Deo-Segundo":
                self.izquierdo[1]=abs(box[0]-box[2])
            if label=="Deo-Tercero":
                self.izquierdo[2]=abs(box[0]-box[2])
            if label=="Deo-Cuarto":
                self.izquierdo[3]=abs(box[0]-box[2])
            if label=="Deo-Quinto":
                self.izquierdo[4]=abs(box[0]-box[2])
            if label == 'Cuerpo-Pie':
                ancho2 = abs(box[0]-box[2])
                self.izquierdo[5]=ancho2
            if label == 'Talon':
                Talon2 = box
                self.izquierdo[6]=abs(box[0]-box[2])
        for i,value in enumerate(objs2):
            aux = abs(Talon2[3]-value[0][1])
            if dx2 < aux:
                dx2=aux
        self.largo.set("Largo Pie: "+str(round(dx*0.014561500275786,2))+'cm')
        self.ancho.set("Ancho Pie: "+str(round(ancho*0.0155793573515093,2))+'cm')
        self.largo2.set("Largo Pie: "+str(round(dx2*0.014561500275786,2))+'cm')
        self.ancho2.set("Ancho Pie: "+str(round(ancho2*0.0155793573515093,2))+'cm')
        time.sleep(0.01)
        t1 = time.time()
        print(t1-t0)
class Visor(tk.Frame):
    def __init__(self,title,master=None,vid=None,vid2=None):
        tk.Frame.__init__(self,master)
        self.master.title(title)
        self.vid=vid
        self.vid2=vid2
        self.fig = Figure(figsize=(5, 8), dpi=100)
        self.axes = [self.fig.add_axes([0.0,0.1,0.4,0.8]),self.fig.add_axes([0.4,0.1,0.4,0.8])]
        self.axes[0].axis('off')
        self.axes[1].axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()
        self.frame = np.zeros((1080,1920,3))
        self.frame2= np.zeros((1080,1920,3))
        img = warpAffine(self.frame , T, (1080,1920))
        img2= warpAffine(self.frame2, T, (1080,1920))
        print(img.shape)
        self.im = self.axes[0].imshow(img2)
        self.im2 = self.axes[1].imshow(img)
        self.ret=False
        self.ret2=False
        self.permiso=False
        self.ani = FuncAnimation(self.fig, self.Draw, interval=20,blit=True)
    def Draw(self,i):
        self.ret , self.frame = self.vid.read()
        self.ret2 , self.frame2 = self.vid2.read()
        if self.ret2 and self.ret:
            self.frame2 = cvtColor(self.frame2,COLOR_BGR2RGB)
            img2= warpAffine(self.frame2, T, (1080,1920))
            self.frame = cvtColor(self.frame,COLOR_BGR2RGB)
            img = warpAffine(self.frame, T, (1080,1920))
            self.im2.set_data(img)
            self.im.set_data(img2)
        time.sleep(0.001)
        return self.axes
