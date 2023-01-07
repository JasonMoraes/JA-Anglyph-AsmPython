from pathlib import Path

import PySimpleGUI as sg
import sys
import cv2
import os

from Core import Core

class ViewRenderer:
    core = Core()
    windowDimensions = (1280, 920)
    def __init__(self):
        self.set_theme()
        self.img = 0
        layout_l = [[sg.Column([[sg.Text('Before')], [sg.Image(key="Image")]], size=(640, 450))]]
        layout_r = [[sg.Column([[sg.Text('After')], [sg.Image(key="Result")]], size=(640, 450))]]
        footer = [[sg.Text('Select Image', key="Path"), sg.Button('Select Image')], [sg.Text('Anaglify'), sg.Button('Anaglify')], [sg.Text('Select DLL'), sg.Radio('ASM', "RADIO1", key="asmchosen" , default=False), sg.Radio('C++', "RADIO1", default=True)], [sg.Text('Select No. of threads'), sg.Slider(range=(1, 64), default_value=os.cpu_count(), size=(30, 10), orientation="h", enable_events=True, key="slider")], [sg.Text('Elapsed Time [s]'), sg.Text(self.core.elapsedTime, key="ElapsedTime")]]

        self.layout = [[[sg.Text('Anaglify', size=(8,1), font=('Inter', 20), text_color=sg.TANS[2], justification='center')]], [[sg.Col(layout_l), sg.Col(layout_r)]], [[sg.Frame('Settings', layout=footer, size=(self.windowDimensions[0], 400))]]]
        self.window = sg.Window('Anaglify', self.layout, size=self.windowDimensions)
        while True:
            res = self.render()
            if res == 0:
                break

    def set_theme(self):
        sg.theme('DarkAmber')

    def render(self):
        event, values = self.window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            return 0
        if event == 'Select Image':
            path = sg.popup_get_file("", no_window=True)
            if path == '':
                return 0
            if not Path(path).is_file():
                self.window['Status'].update('Image file not found !')
                return 0
            self.img = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
            # resize to fit to window
            dim = (int(self.windowDimensions[1]/2), int(self.windowDimensions[1]/2/self.img.shape[1] * self.img.shape[0]))
            data = cv2.resize(self.img, dim, interpolation=cv2.INTER_AREA)
            data = cv2.imencode('.png', data)[1].tobytes()
            self.window['Image'].update(data=data)
            self.window['Path'].update(path)
        if event == 'Anaglify':
            self.core.systemThreads = values['slider']
            print(self.window['asmchosen'].get())
            if self.window['asmchosen'].get() == True:
                self.core.chosenASM = True
            print(self.core.systemThreads)
            data = self.core.anaglify(self.img)
            dim = (int(self.windowDimensions[1]/2), int(self.windowDimensions[1]/2/data.shape[1] * data.shape[0]))
            data = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
            data = cv2.imencode('.png', data)[1].tobytes()
            self.window['Result'].update(data=data)
            self.window['ElapsedTime'].update(self.core.elapsedTime)