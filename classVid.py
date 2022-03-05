from PyQt5 import uic
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QFileDialog


class ClassVidForm(QtWidgets.QDialog):
    def __init__(self):
        super(ClassVidForm, self).__init__()
        uic.loadUi("./ui/ClassVid.ui", self)
        self.setWindowModality(2)
        self.c_init()


    #
    def c_init(self):

        self.dateEdit1.dateChanged.connect(self.DC)
        self.dateEdit2.dateChanged.connect(self.DC)
        self.tWCV.horizontalHeader().setDefaultSectionSize(100)
        self.tWCV.setColumnCount(5)
        self.tWCV.setHorizontalHeaderLabels(["Дата", "Место", "Вид ЧС", "Пострадало", "Из них погибло"])
        self.tWCV.resizeColumnsToContents()
        self.comboBox.currentIndexChanged.connect(self.comb)




    def report_get_results(self):
        self.report_query = QtSql.QSqlQuery()
        self.report_query.prepare(
            "select chs.Data, chs.Mesto, vid.name2, chs.postradalo, chs.pogiblo, class.name "
            "from vid join chs on (vid.id_Vid=chs.id_Vid) "
            "join gruppa on (vid.id_Group=gruppa.id_Group) "
            "join class on (gruppa.id_Class=class.id_Class) "
            "where (chs.Data >=:dateEdit1) and (chs.Data <=:dateEdit2) "
            f"and class.name like '{self.comboBox.currentText()}' "

        )
        self.report_query.bindValue(":dateEdit1", self.dateEdit1.date().toString(QtCore.Qt.ISODate))
        self.report_query.bindValue(":dateEdit2", self.dateEdit2.date().toString(QtCore.Qt.ISODate))
        self.report_query.exec()
        self.tWCV.setRowCount(self.report_query.size())
        i = 0
        while self.report_query.next():
            for j in range(self.tWCV.columnCount()):
                item = QtWidgets.QTableWidgetItem(str(self.report_query.value(j)))
                if j == 0:
                    item = QtWidgets.QTableWidgetItem(self.report_query.value(j).toString(QtCore.Qt.LocalDate))
                    self.tWCV.setItem(i, j, item)
                if j == 1:
                    self.tWCV.setItem(i, j, item)
                if j == 2:
                    self.tWCV.setItem(i, j, item)
                if j == 3:
                    self.tWCV.setItem(i, j, item)
                if j == 4:
                    self.tWCV.setItem(i, j, item)
            i += 1

    def DC(self):
        self.report_get_results()

    def comb(self):
        self.report_get_results()
