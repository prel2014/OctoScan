import serial
from threading import Timer
class ControlIluminacion():
    def __init__(self):
        self.ser   = serial.Serial('/dev/ttyUSB0',9600)
        self.frec  = 'F1500'
        self.frecaux=''
        self.duty='D050'
        self.dutyaux=''
        self.ceros = ''
        self.ser.write(self.frec.encode('utf-8'))
#        self.loop()
#        self.Time=Timer(0.001,self.loop)
    def init_Frec(self,frec):
        self.frec = frec
    def loop(self):
        self.ser.write(self.duty.encode('utf-8'))
co = ControlIluminacion()
while True:
    co.duty=input()
    co.loop()
