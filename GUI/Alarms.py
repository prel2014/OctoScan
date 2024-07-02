from Threadding import Timer
import serial
class Signal():
    def __init__(self,name=None,duration=0,color=None):
        self.name=name
        self.duration=duration
        self.color=color
        self.description=''
        self.ser = serial.Serial('/dev/ttyACM0')
    def pintarLed(self):
        
        
class Fail(Signal):
    def __init__(self,description):
        super().__init__(name='Error',duration=0.1,color='red')
        self.description=description
    def execute(self):
        hilo = Timer(self.duration,self.pintarLed,args=None)
        hilo.start()

class Warning(Signal):
    def __init__(self,description):
        super().__init__(name='Advertencia',duration=0.1,color='yellow')
        self.description=description
    def execute(self):
        hilo = Timer(self.duration,self.pintarLed,args=None)
        hilo.start()

class Progress(Signal):
    def __init__(self,description):
        super().__init__(name='Progreso',duration=0.1,color='yellow')
        self.description=description
    def execute(self):
        hilo = Timer(self.duration,self.pintarLed,args=None)
        hilo.start()    