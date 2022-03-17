import serial.tools.list_ports
import time


class SerialPort:

    def __init__(self):
        self.ports = serial.tools.list_ports.comports()
        self.ports_list = {}
        self.default_port = ''
        self.default_serial_port = ''
        
    def get_ports_list(self):
        '''
            return list of ports as dict {'name': 'port'}
        '''
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
        self.default_serial_port = serial.Serial(port)
        try:
            if not self.default_serial_port.isOpen():
                self.default_serial_port.open()  
            return {'port': self.default_serial_port, 'result': True}
        except:
            return {'port': '', 'result': False}
    
    def disconnect_port(self, serial_port=''):
        if serial_port == '':
            serial_port = self.default_serial_port
        try:
            serial_port.close()
            return {'result': True}

        except:
            return {'result': False}
        
    def measure_scaler(self, serial_port=''):
        '''
            read data from serial port
            serial_port: serial.Serial
            return measured data (str)
        '''
        if not serial_port:
            serial_port = self.default_serial_port
            
        while(True):
            if serial_port.in_waiting:
                s = serial_port.readline()
                # print(s)

                end = time.time() + 0.5
                while(end > time.time()):
                    serial_port.readline()
                serial_port.reset_input_buffer()
                serial_port.reset_output_buffer()
                if(s == serial_port.readline() and s != 0):
                    value = float(s.decode())
                    return value



def test_class(port):    
    s = SerialPort()
    s.set_default_port(port)
    conn = s.connect_port()['port']
    print(s.measure_scaler(port))

