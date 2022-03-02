from flask import Flask
from multiprocessing import Process
import PySimpleGUI as sg
import serial.tools.list_ports
import time


default_port = ''

class SerialPort:

    def __init__(self):
        self.ports = serial.tools.list_ports.comports()
        self.ports_list = {}
        self.default_port = ''
        
    def get_ports_list(self):
        for p in self.ports:
            self.ports_list[str(p).split('-')[1].strip()] = str(p).split('-')[0].strip()
        return self.ports_list
    
    def set_default_port(self, port):
        self.default_port = port
        
    def connect_port(self, port=''):
        '''
            connect and configure port 
            return serial port(serial), and result status(boolean)
        '''
        if port == '':
            port = self.default_port
        serialPort = serial.Serial(port)
        try:
            if not serialPort.isOpen():
                serialPort.open()  
            return {'port': serialPort, 'result': True}
        except:
            return {'port': '', 'result': False}
            
    def measure_scaler(self, serial_port):
        '''
            read data from serial port
            serial_port: serial.Serial
            return measured data (str)
        '''
        while(True):
            if serial_port.in_waiting:
                s = serial_port.readline()
                # print(s)
                time.sleep(.2)
                serial_port.reset_input_buffer()
                serial_port.reset_output_buffer()
                if(s == serial_port.readline()):
                    value = float(s.decode())
                    return value

def test_class(port):    
    s = SerialPort()
    s.set_default_port(port)
    port  = s.connect_port()['port']
    print(s.measure_scaler(port))



# Serial port configurations


# serialPort = serial.Serial('/dev/pts/5')


        
        
    
# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.

# layout = [  [sg.Text('Choose the port'), sg.InputText()],
            # [sg.Text('named'), sg.Combo(ports_list.keys(), s=(15,22), enable_events=True, readonly=True, k='PORT')],
            # [sg.Button('Ok'), sg.Button('Cancel')] ]

# ## Create the Window
# window = sg.Window('Window Title', layout)
# ## Event Loop to process "events" and get the "values" of the inputs
# while True:
    # event, values = window.read()
    # if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        # break
    # # sg.SystemTray.notify('Notification Title', 'This is the notification message')
    
    # # port = values['PORT']
    # # print(ports_list[port])
    
    # while(True):
        # if serialPort.in_waiting:
            # s = serialPort.readline()
            # print(s)
            # if(s == serialPort.readline()):
                # value = float(s.decode())
                # print(value)
                # break
            # time.sleep(1)

# window.close()

