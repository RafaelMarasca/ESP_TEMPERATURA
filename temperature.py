import PySimpleGUI as sg
from serial.tools import list_ports
import serial

def start_gui(ports, baud_rates):

    sg.theme('DarkPurple1')
    sg.SetOptions(input_elements_background_color='gainsboro',button_color = ('Black', 'gainsboro'))

    font = 'Helvetica 30';

    col = [ [sg.Text('-',key = '-TEMP-',font=font), sg.Text('°C',font=font)],
            [sg.Text('Select COM port:',size=(14,1)),sg.Combo(ports,size=(20,1))],
            [sg.Text('Select baud rate:',size=(14,1)),sg.Combo(baud_rates,size=(20,1))],
            [sg.Text('Disconnected',text_color = '#f50a0a',size=(10,1),key = '-STATUS-'),
             sg.Push(),
             sg.Button('Disconnect',pad=(5,0),disabled = True),
             sg.Button('Connect',pad=(5,0))]]
            
    layout = [[sg.Column(col, element_justification = 'c')]]

    return sg.Window('Temperatura', layout)



if __name__ == '__main__':

    
    ports = [port.name for port in list_ports.comports()]
    baud_rates = ['9600', '19200', '38400', '57600', '115200']

    window = start_gui(ports, baud_rates);

    port = serial.Serial();

    connected = False 
    while True:         
        event, values = window.read(timeout=1000)

        if event == sg.WIN_CLOSED:
            port.close()
            break

        elif event == 'Connect':
            if(values[0] and values[1]):
                port.port = values[0]
                port.baudrate = values[1]

                try:
                    port.open()
                except serial.SerialException as exc :

                    print('Serial Exception: {0}'.format(exc))
                    sg.Popup('Failed to Connect!',text_color = '#f50a0a')

                else:
                    connected = True
                    window['-STATUS-'].update('Conected',text_color='#0af50e')
                    window['Connect'].update(disabled=True)
                    window['Disconnect'].update(disabled=False)

        elif event == 'Disconnect':
                port.close()
                connected = False
                window['-STATUS-'].update('Disconnected',text_color='#f50a0a')
                window['Connect'].update(disabled=False)
                window['Disconnect'].update(disabled=True)

        if connected:
            try:
                bstring = port.read_until()
            except serial.SerialException as exc:
                window['-TEMP-'].update('-')
                window['-STATUS-'].update('Desconnected',text_color='#f50a0a')
                port.close()
                connected = False
                window['Connect'].update(disabled=False)
                print('Serial Exception: {0}'.format(exc))
            else:
                bstring = bstring.decode('ascii').rstrip()
                window['-TEMP-'].update(bstring)