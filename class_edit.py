from PyQt5 import uic
from PyQt5 import QtWidgets, QtSql, QtCore


class ClassEdit(QtWidgets.QDialog):
    def __init__(self):
        super(ClassEdit, self).__init__()
        uic.loadUi("./ui/EditClass.ui", self)
        self.setWindowModality(2)




