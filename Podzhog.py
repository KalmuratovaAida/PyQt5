from PyQt5 import uic
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QFileDialog


class PodzhogForm(QtWidgets.QDialog):
    def __init__(self):
        super(PodzhogForm, self).__init__()
        uic.loadUi("./ui/P.ui", self)
        self.setWindowModality(2)
        self.p_init()

    def p_init(self):
        self.tWPodzhog.horizontalHeader().setDefaultSectionSize(100)
        self.tWPodzhog.setColumnCount(3)
        self.tWPodzhog.setHorizontalHeaderLabels(["Место", "ЧС","Причины"])
        self.tWPodzhog.resizeColumnsToContents()

    def report_get_results(self):
        self.report_query = QtSql.QSqlQuery()
        self.report_query.prepare(
            "select chs.Mesto, vid.name2, feature.name3 "
            "from (vid join chs on (vid.id_Vid=chs.id_Vid) "
            "join report on(chs.id_Chs = report.id_Chs)) "
            "join feature on(feature.id_feature = report.id_feature) "
            "where(feature.name3 = 'поджог') "            "group by chs.Mesto"
        )
        # self.query.bindvalue(":feature.name3","поджог")
        self.report_query.exec()
        self.tWPodzhog.setRowCount(self.report_query.size())
        i = 0
        while self.report_query.next():
            for j in range(self.tWPodzhog.columnCount()):
                item = QtWidgets.QTableWidgetItem(str(self.report_query.value(j)))
                if j == 0:
                    self.tWPodzhog.setItem(i, j, item)
                if j == 1:
                    self.tWPodzhog.setItem(i, j, item)
                if j == 2:
                    self.tWPodzhog.setItem(i, j, item)

                #self.tWPodzhog.setItem(i, j, item)
            i += 1
