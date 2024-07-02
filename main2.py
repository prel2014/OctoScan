import tkinter as tk
from GUI.VerticalComponents import Visor,PanelResultado
from cv2 import VideoCapture
import time
from threading import Thread
class Principal():
    def __init__(self,root=None):
        self.vid = VideoCapture(1)
        self.vid2= VideoCapture(0)
        self.vid.set(3,1920)
        self.vid.set(4,1080)
        self.vid2.set(3,1920)
        self.vid2.set(4,1080)
        self.V = Visor("OctoScan",master=root,vid=self.vid,vid2=self.vid2)
        self.V.place(x=0,y=0,width=1500,height=1080)
        self.P = PanelResultado("Resultado",master=root,V=self.V)
        self.P.place(x=1420,y=0,width=500,height=1080)
        self.h=Thread(target=self.pasar)
        self.h.start()
    def pasar(self):
        while True:
            if self.V.ret:
                self.P.img=self.V.frame.copy()
                self.P.img2=self.V.frame2.copy()
                self.V.permiso=False
root = tk.Tk()
root.geometry("1920x1080+0+0")
P=Principal(root=root)
root.mainloop()
