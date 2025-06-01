from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
QLineEdit, QPushButton, QLabel, QTextEdit, QCheckBox, QDialog, QRadioButton, QButtonGroup, QDialogButtonBox,QGroupBox)
from path import find_flash_drive_w
from test import measure_flash_speed_generate

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 241, 341, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtWidgets.QComboBox(parent=Dialog)
        self.comboBox.setGeometry(QtCore.QRect(30, 60, 331, 31))
        self.comboBox.setObjectName("comboBox")
        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(30, 20, 331, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 113, 331, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 170, 331, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        
        self.pushButton.clicked.connect(self.on_detection_clicked)
        self.pushButton_2.clicked.connect(self.on_monitoring_clicked)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Обнаружение"))
        self.pushButton_2.setText(_translate("Dialog", "Мониторинг"))

    def on_detection_clicked(self):
        input_text = self.lineEdit.text()
        result = find_flash_drive_w(input_text)
        
        self.comboBox.clear()
        
        if isinstance(result, list): 
            self.comboBox.addItems(result)
        else:
            self.comboBox.addItem(str(result))

    def on_monitoring_clicked(self):
        result_dialog = QtWidgets.QMessageBox()
        result_dialog.setWindowTitle("Результаты тестирования")
        
        read_speed, write_speed = measure_flash_speed_generate("D:\\")
        message = f"Скорость чтения: {read_speed:.2f}\nСкорость записи: {write_speed:.2f}"
        
        result_dialog.setText(message)
        
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setWindowTitle("Обнаружено несоответствие")
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)  
        error_dialog.setText("Данные могут быть некоректные!")
        error_dialog.setInformativeText("Это приложение предназначено для linux, на этой ОС может работать некорректно.")
        error_dialog.exec()
        result_dialog.exec()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())