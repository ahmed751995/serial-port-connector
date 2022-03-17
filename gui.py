import PySimpleGUI as sg
from multiprocessing import Process

from app import create_app
from port import SerialPort

def create_gui(app, ser):
    app = app(ser)
    ports_list = ser.get_ports_list()
    port_name = ''
    # set layout
    layout = [  [sg.Text('Choose the port')],
                [sg.Text('named'), sg.Combo(list(ports_list.keys()), s=(15,22), enable_events=True, readonly=True, k='PORT')],
                [sg.Button('Connect'), sg.Button('Disconnect'), sg.Button('Close')] ]

    ## Create the Window
    window = sg.Window('Window Title', layout)
    
    ## Event Loop to process "events" and get the "values" of the inputs
        
    while True:
        event, values = window.read()
        # sg.SystemTray.notify('Notification Title', 'This is the notification message')
        
        if event == 'Connect':
            port_name = values['PORT']
            if port_name :
                port = ports_list[port_name]
            
                port = '/dev/pts/2'
                ser.set_default_port(port)
                conn = ser.connect_port()
                if conn['result'] == True:
                    server = Process(target=app.run)
                    server.start()
                    sg.SystemTray.notify('Success', f'Pot {port_name} connected Successfully')
                    # print(ser.measure_scaler(conn['port']))
                else:
                    sg.SystemTray.notify('Failed', f'Pot {port_name} failed to connect')
            else:
                sg.SystemTray.notify('Error', f'Please select port')
        
        if event == 'Disconnect' or event == sg.WIN_CLOSED or event == 'Close':
            conn = ser.disconnect_port()
            if conn['result'] == True:
                server.terminate()
                server.join()
                sg.SystemTray.notify('Success', f'Port {port_name} disconnected Successfully')
            else:
                sg.SystemTray.notify('Failed', 'Port failed to connect')
        
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break

    window.close()


if __name__ == '__main__':
    create_gui(create_app, SerialPort())
    # window.close()

