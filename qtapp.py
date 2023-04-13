#!/bin/python3
import sys
import subprocess
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, \
    QRadioButton, QPushButton, QLCDNumber, QLabel, QHBoxLayout, QVBoxLayout


class DummyButton():
    def move(self, *args):
        pass

    def resize(self, *args):
        pass

    def setFont(self, *args):
        pass

class App(QWidget):
    def GetDeviceIDs(self):
        proc = subprocess.Popen(['xsetwacom', '--list',  'devices'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = str(proc.communicate()[0].decode())

        lines = output.split("\n")

        for line in lines:
            if "type: PAD" in line:
                self.pad_id = line.split()[6]
            if "type: STYLUS" in line:
                self.stylus_id = line.split()[6]
            if "type: ERASER" in line:
                self.eraser_id = line.split()[6]
            if "type: CURSOR" in line:
                self.cursor_id = line.split()[6]

    def MapToOutput(self):
        print(self.output_line_edit.text())

        for id in [self.pad_id, self.stylus_id, self.eraser_id, self.cursor_id]:
            proc = subprocess.Popen(['xsetwacom', '--set', str(id), "MapToOutput", self.output_line_edit.text()], 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    def PadButtonsRebind(self):
        keys = [self.pad_button_textbox1.text(),
                self.pad_button_textbox2.text(),
                self.pad_button_textbox3.text(),
                self.pad_button_textbox4.text()]
        
        for num, key in enumerate(keys):
            if num == 3:
                num = 7
            print("Button: ", num, ", key:", key)
            proc = subprocess.Popen(['xsetwacom', '--set', str(self.pad_id), "button", str(num + 1), "key", key], 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    def CreateMapLayout(self):
        self.map_layout = QVBoxLayout()

        self.output_label = QLabel(self)
        self.output_line_edit = QLineEdit(self)
        self.map_to_output_button = QPushButton("Map", self)

        self.output_label.setText("Output device")
        self.output_line_edit.setText("HEAD-0")
        self.map_to_output_button.clicked.connect(self.MapToOutput)

        self.map_layout.addWidget(self.output_label)
        self.map_layout.addWidget(self.output_line_edit)
        self.map_layout.addWidget(self.map_to_output_button)

    def CreatePadLayout(self):
        self.pad_button_textbox1 = QLineEdit(self)
        self.pad_button_textbox2 = QLineEdit(self)
        self.pad_button_textbox3 = QLineEdit(self)
        self.pad_button_textbox4 = QLineEdit(self)
        self.pad_button_label1 = QLabel(self)
        self.pad_button_label2 = QLabel(self)
        self.pad_button_label3 = QLabel(self)
        self.pad_button_label4 = QLabel(self)
        self.pad_button_rebind = QPushButton("Rebind", self)
        self.pad_button_rebind.clicked.connect(self.PadButtonsRebind)

        text_width = 50
        
        self.pad_layout = QVBoxLayout()
        self.pad_button_layout1 = QHBoxLayout()
        self.pad_button_layout2 = QHBoxLayout()
        self.pad_button_layout3 = QHBoxLayout()
        self.pad_button_layout4 = QHBoxLayout()

        self.pad_button_label1.setText("Button 1")
        self.pad_button_label2.setText("Button 2")
        self.pad_button_label3.setText("Button 3")
        self.pad_button_label4.setText("Button 4")

        self.pad_button_layout1.addWidget(self.pad_button_label1)
        self.pad_button_layout1.addWidget(self.pad_button_textbox1)
        self.pad_button_layout2.addWidget(self.pad_button_label2)
        self.pad_button_layout2.addWidget(self.pad_button_textbox2)
        self.pad_button_layout3.addWidget(self.pad_button_label3)
        self.pad_button_layout3.addWidget(self.pad_button_textbox3)
        self.pad_button_layout4.addWidget(self.pad_button_label4)
        self.pad_button_layout4.addWidget(self.pad_button_textbox4)

        self.pad_layout.addLayout(self.pad_button_layout1)
        self.pad_layout.addLayout(self.pad_button_layout2)
        self.pad_layout.addLayout(self.pad_button_layout3)
        self.pad_layout.addLayout(self.pad_button_layout4)
        self.pad_layout.addWidget(self.pad_button_rebind)

        self.pad_layout.setSpacing(10)

    def __init__(self):
        super().__init__()

        self.title = "Wacom thingy"
        self.setWindowTitle(self.title)

        self.left = 750
        self.top = 250
        self.width = 400
        self.height = 150
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.GetDeviceIDs()

        self.main_layout = QHBoxLayout()
        self.CreateMapLayout()
        self.CreatePadLayout()

        self.main_layout.addLayout(self.map_layout)
        self.main_layout.addLayout(self.pad_layout)
        self.setLayout(self.main_layout)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    program = App()
    app.exec_()
