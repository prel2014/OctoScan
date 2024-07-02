import kivy
from threading import Thread
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
from kivy.graphics import RenderContext, Callback, PushMatrix, PopMatrix, \
    Color, Translate, Rotate,Scale, Mesh, UpdateNormalMatrix
from objloader import ObjFile
from kivy.config import Config
import os
import time
os.environ['KIVY_GLES_LIMITS'] = "0"
Window.size = (1920,1080)
#Window.fullscreen = 0.1
Builder.load_file('main.kv')

class Renderer(Widget):
    def setG(self,t,r,s):
        self.anX = t[0]
        self.anY = t[1] 
        self.anZ = t[2]
        self.dsx = r[0]
        self.dsy = r[1]
        self.dsz = r[2]
        self.dx  = s[0] 
        self.dy  = s[1]
        self.dz  = s[2]
        self.drx  = (self.anX   - self.rx.angle)/10
        self.dry  = (self.anY   - self.ry.angle)/10
        self.drz  = (self.anZ   - self.rz.angle)/10
        self.dex  = (self.disx  - self.t.x)/10
        self.dey  = (self.disy  - self.t.y)/10
        self.dez  = (self.disz  - self.t.z)/10
        self.scx  = (self.dx   - self.s.x)/10
        self.scy  = (self.dy   - self.s.y)/10
        self.scz  = (self.dz   - self.s.z)/10
    def Animacion(self,delta):
        self.rx.angle += self.scene.dx#*delta
        self.ry.angle += self.scene.dy#*delta
        self.rz.angle += self.scene.dz#*delta
        self.t.x += self.scene.dsx#*delta
        self.t.y += self.scene.dsy#*delta
        self.t.z += self.scene.dsz#*delta
        self.s.x += self.scene.sx#*delta
        self.s.y += self.scene.sy#*delta
        self.s.z += self.scene.sz#*delta
        time.sleep(0.001)
        #print('dx:{},dy:{},dz:{},rotx:{},roty:{},rotz:{},scx:{},scy:{},scz:{}'.format(self.t.x,self.t.y,self.t.z,self.rx.angle,self.ry.angle,self.rz.angle,self.s.x,self.s.y,self.s.z))
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('../modelo3D/simple.glsl')
        self.scene = ObjFile(resource_find("../modelo3D/pie2.obj"))
        self.nun=0
        self.n=0
        self.m = list()
        super(Renderer, self).__init__(**kwargs)
        self.anX = -60.0
        self.anY = 0.0
        self.anZ = -90.0
        self.dsx = 0.5
        self.dsy = 0.1
        self.dsz = -4.2
        self.dx  = 5.0
        self.dy  = 5.0
        self.dz  = 5.0
        self.dex=0.0
        self.dey=0.0
        self.dez=0.0
        self.drx=0.0
        self.dry=0.0
        self.drz=0.0
        self.scx=0.0
        self.scy=0.0
        self.scz=0.0
        self.disx = 0.5
        self.disy = 0.1
        self.disz = -4.2
        self.rx=None
        self.ry=None
        self.rz=None
        self.t=None
        self.s=None
        self.permiso=False
        self.m0=2.0/0.016
        #self.delta=0.0
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            Translate(0, -2, -3)
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        Clock.schedule_interval(self.update_glsl, 1 / 60.)
    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)
    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)
    def calculo(self,transformacion):
        if transformacion == 'rx':
            if abs(self.anX-self.rx.angle) > 1:
                if self.anX > self.rx.angle:
                    self.rx.angle += 1
                else:
                    self.rx.angle -= 1
        if transformacion=='ry':
            if abs(self.anY-self.ry.angle) > 1:
               if self.anY > self.ry.angle:
                    self.ry.angle += 1
               else:
                    self.ry.angle -= 1
        if transformacion=='rz':
            if abs(self.anZ - self.rz.angle) > 1:
               if self.anZ > self.rz.angle:
                   self.rz.angle += 1
               else:
                   self.rz.angle -= 1
        if transformacion=='tx':
            if abs(self.dsx - self.t.x) > 0.1:
               if self.dsx > self.t.x:
                   self.t.x += 0.1
               else:
                   self.t.x -= 0.1
        if transformacion=='ty' :
            if abs(self.dsy - self.t.y) > 0.1:
               if self.dsy > self.t.y:
                   self.t.y += 0.1
               else:
                   self.t.y -= 0.1
        if transformacion=='tz':
            if abs(self.dsz - self.t.z) > 0.1:
               if self.dsz > self.t.z:
                   self.t.z += 0.1
               else:
                   self.t.z -= 0.1
        if transformacion=='sx':
            if abs(self.scx - self.s.x) > 0.1:
               if self.scx > self.s.x:
                   self.s.x += 0.1
               else:
                   self.s.x -= 0.1
        if transformacion=='sy':
            if abs(self.scy-self.s.y) > 0.1:
               if self.scy > self.s.y:
                   self.s.y += 0.1
               else:
                   self.s.z -= 0.1
        if transformacion=='sz':
            if abs(self.scz - self.s.z) > 0.1:
               if self.scz > self.s.z:
                   self.s.z += 0.1
               else:
                   self.s.z -= 0.1
    def update_glsl(self, delta):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self.canvas['projection_mat'] = proj
        self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
        self.canvas['ambient_light'] = (0.1, 0.1, 0.1)
        #self.calculo('rx')
        self.rx.angle += self.drx
        self.ry.angle += self.dry
        self.rz.angle += self.drz
        self.t.x      += self.dex
        self.t.y      += self.dey
        self.t.z      += self.dez
        self.s.x      += self.scy
        self.s.z      += self.scy
        self.s.y      += self.scy
        if abs(self.anX-self.rx.angle) < 1:
            self.drx=0.0
        """
        self.rx.angle = self.anX
        self.ry.angle = self.anY
        self.rz.angle = self.anZ
        self-.t.x = self.dsx
        self.t.y = self.dsy
        self.t.z = self.dsz
        self.s.x = self.dx
        self.s.y = self.dy
        self.s.z = self.dz
        """         
        print('dx:{},dy:{},dz:{},rotx:{},roty:{},rotz:{},scx:{},scy:{},scz:{}'.format(self.t.x,self.t.y,self.t.z,self.rx.angle,self.ry.angle,self.rz.angle,self.s.x,self.s.y,self.s.z))
    def setup_scene(self):
        print('inicio')
        Color(1, 1, 1, 1)
        PushMatrix()
        self.t=Translate(0.5,0.1,-4.2)
        self.rx=Rotate(-60.0,1,0,0)
        self.ry=Rotate(0.0,0,1,0)
        self.rz=Rotate(-90.0,0,0,1)
        self.s=Scale(5.0,5.0,5.0)
        self.m = list(self.scene.objects.values())[0]
        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=self.m.vertices,
            indices=self.m.indices,
            fmt=self.m.vertex_format,
            mode='triangles'
        )
        PopMatrix()
class Botonera(GridLayout):
    def __init__(self,**kwargs):
        super(Botonera,self).__init__(**kwargs) 
class Panel(BoxLayout):
    def __init__(self,**kwargs):
        super(Panel, self).__init__(**kwargs)
        #self.btn_dp.bind(on_render=self.ToDP)

class Contenedor_01(BoxLayout):
    def __init__(self,**kwargs):
        super(Contenedor_01, self).__init__(**kwargs)
        self.render = Renderer(**kwargs)
    def ToDP(self):
        self.render.m0=int(2.0/0.008)
        self.render.setG([-60.0,0.0,-90.0],[0.5,0.1,-4.2],[5.0,5.0,5.0])
        
    def ToDS(self):
        self.render.m0=int(2.0/0.008)
        #self.render.setG([0.0,0.0,-144.0],[0.5,0.1,-4.2],[8.0,8.0,8.0])
        self.render.drx = 1
    def ToDT(self):
        pass
    def ToDC(self):
        pass
    def ToDQ(self):
        pass
    def ToCP(self):
        pass
    def ToTA(self):
        pass
class MainApp(App):
    tilte='OctoScan'
    def build(self):
        return Contenedor_01()

if __name__ == '__main__':
    MainApp().run()
