from PyQt5 import QtWidgets, uic, QtSql, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from datetime import datetime, timedelta
import sys
from PyQt5.QtSql import QSqlDatabase
from Class import ClassForm
from Report import ReportForm
from feature import FeatureForm
from Podzhog import PodzhogForm
from classVid import ClassVidForm


# инициализация главной формы родительский метод
class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()

        uic.loadUi("./ui/MainForm.ui", self)
        self.db_init()  # вызов этого метода
        self.Class = None
        self.Report = None
        self.feature = None
        self.Podzhog = None
        self.classVid = None
        self.model_chs_init()
        self.model_report_init()

        self.BtnClass.clicked.connect(self.btnClickClass)
        self.BtnFeature.clicked.connect(self.btnClickFeature)
        self.BtnReport.clicked.connect(self.btnClickReport)
        self.BtnP.clicked.connect(self.btnClickpodzhog)
        self.BtnCV.clicked.connect(self.btnClickCV)

        self.BtnAddChs.clicked.connect(self.btnClickAddChs)
        self.BtnDelChs.clicked.connect(self.btnClickDelChs)
        self.BtnSaveChs.clicked.connect(self.btnClickSaveChs)

        self.tVChs.setModel(self.model_chs)
        self.tVChs.setItemDelegateForColumn(3, QtSql.QSqlRelationalDelegate(self.tVChs))
        self.tVChs.verticalHeader().setVisible(False)
        self.tVChs.setSortingEnabled(True)
        self.tVChs.hideColumn(0)
        # self.tVChs.hideColumn(3)
        self.tVChs.resizeColumnsToContents()
        self.lEChs.textEdited.connect(self.LEChs)

        self.BtnAddReport.clicked.connect(self.btnClickAddReport)
        self.BtnDelReport.clicked.connect(self.btnClickDelReport)
        self.BtnSaveReport.clicked.connect(self.btnClickSaveReport)
        self.tVReport.setModel(self.model_report)
        # self.tVReport.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.tVReport))
        self.tVReport.setItemDelegateForColumn(2, QtSql.QSqlRelationalDelegate(self.tVReport))
        self.tVReport.verticalHeader().setVisible(False)
        self.tVReport.hideColumn(0)
        self.tVReport.hideColumn(1)
        self.tVReport.resizeColumnsToContents()

        self.dateEdit1.dateChanged.connect(self.DateEChanged)
        self.dateEdit2.dateChanged.connect(self.DateEChanged)
        self.dateEdit1.setDate(datetime.today() - timedelta(days=30))
        self.dateEdit2.setDate(datetime.today())

        self.tVChs.clicked.connect(self.tVReportClick)
        self.tVReportClick()

    def tVReportClick(self):
        if self.model_chs.rowCount():
            cur_row = self.tVChs.currentIndex().row()
            self.id_Chs = self.model_chs.record(cur_row).value("id_Chs")
        else:
            self.id_Chs = -1
        self.model_report.setFilter(f"id_Chs = {self.id_Chs}")

    def model_chs_init(self):
        self.model_chs = QtSql.QSqlRelationalTableModel(self)
        self.model_chs.setTable("chs")
        self.model_chs.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model_chs.setRelation(3, QtSql.QSqlRelation("vid", "id_Vid", "name2"))
        self.model_chs.select()
        self.model_chs.setHeaderData(1, QtCore.Qt.Horizontal, "Дата")
        self.model_chs.setHeaderData(2, QtCore.Qt.Horizontal, "Местонахождение")
        self.model_chs.setHeaderData(3, QtCore.Qt.Horizontal, "Вид ЧС")
        self.model_chs.setHeaderData(4, QtCore.Qt.Horizontal, "Пострадало")
        self.model_chs.setHeaderData(5, QtCore.Qt.Horizontal, "Из них погибло")

    def model_report_init(self):
        self.model_report = QtSql.QSqlRelationalTableModel(self)
        self.model_report.setTable("report")
        self.model_report.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        # self.model_report.setRelation(1, QtSql.QSqlRelation("chs", "id_Chs", "Data"))
        self.model_report.setRelation(2, QtSql.QSqlRelation("feature", "id_feature", "name3"))
        self.model_report.select()
        # self.model_report.setHeaderData(1, QtCore.Qt.Horizontal,"Дата ЧС")
        self.model_report.setHeaderData(2, QtCore.Qt.Horizontal, "Причины ЧС")
        self.model_report.setHeaderData(3, QtCore.Qt.Horizontal, "Результаты расследование")

    def db_init(self):
        self.db = QSqlDatabase().addDatabase("QMYSQL")
        self.db.setHostName("127.0.0.1")
        self.db.setDatabaseName("inf")
        self.db.setUserName("root")
        self.db.setPassword("password")
        if not self.db.open():
            QMessageBox.critical(self, "Ошибка",
                                 "Соединение с БД не установлено " + str(self.db.lastError().text()),
                                 QMessageBox.Ok)

    # Функция кнопки в котором открывается форма класса
    def btnClickClass(self):
        if not self.Class:
            self.Class = ClassForm()
        self.Class.show()

    def btnClickFeature(self):
        if not self.feature:
            self.feature = FeatureForm()
        self.feature.show()

    def btnClickpodzhog(self):
        if not self.Podzhog:
            self.Podzhog = PodzhogForm()
        self.Podzhog.report_get_results()
        self.Podzhog.show()

    def btnClickReport(self):
        if not self.Report:
            self.Report = ReportForm()
        self.Report.dateEdit1.setDate(self.dateEdit1.date())
        self.Report.dateEdit2.setDate(self.dateEdit2.date())
        self.Report.report_get_results()
        self.Report.show()

    def btnClickCV(self):
        if not self.classVid:
            self.classVid = ClassVidForm()
        self.classVid.dateEdit1.setDate(self.dateEdit1.date())
        self.classVid.dateEdit2.setDate(self.dateEdit2.date())
        self.classVid.report_get_results()
        self.classVid.show()

    def btnClickAddChs(self):
        record = self.model_chs.record()
        record.remove(record.indexOf("id_Chs"))
        self.model_chs.insertRecord(-1, record)
        index = self.model_chs.index(self.model_chs.rowCount() - 1, 1)
        self.tVChs.edit(index)

    def btnClickDelChs(self):
        cur_row = self.tVChs.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить?",
                                QMessageBox.Cancel, QMessageBox.Ok) == QMessageBox.Ok:
            self.model_chs.removeRow(cur_row)
            if not self.model_chs.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_chs.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)

    def btnClickSaveChs(self):
        if not self.model_chs.submitAll():
            QMessageBox(self,
                        "Ошибка",
                        self.model_chs.lastError().text() + "\nСохранение не были сохранены",
                        QMessageBox.Ok
                        )

    def DateEChanged(self):
        self.model_chs.setFilter(f"(Data >= '{self.dateEdit1.date().toString(QtCore.Qt.ISODate)}')AND"
                                 f"(Data <= '{self.dateEdit2.date().toString(QtCore.Qt.ISODate)}')")

    def btnClickAddReport(self):
        record = self.model_report.record()
        record.remove(record.indexOf("id_report"))
        record.setValue("id_Chs", self.id_Chs)
        self.model_report.insertRecord(-1, record)
        index = self.model_report.index(self.model_report.rowCount() - 1, 1)
        self.tVReport.edit(index)

    def btnClickDelReport(self):
        cur_row = self.tVReport.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить?",
                                QMessageBox.Cancel, QMessageBox.Ok) == QMessageBox.Ok:
            self.model_report.removeRow(cur_row)
            if not self.model_report.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_report.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)
        self.model_report.removeRow(cur_row)

    def btnClickSaveReport(self):
        if not self.model_report.submitAll():
            QMessageBox(self,
                        "Ошибка",
                        self.model_report.lastError().text() + "\nСохранение не были сохранены",
                        QMessageBox.Ok
                        )

    def LEChs(self):
        if self.lEChs.text() != " ":
            self.tVChs.selectionModel().clearSelection()
            start = self.model_chs.index(0, 3)
            matches = self.model_chs.match(
                start,
                QtCore.Qt.DisplayRole,
                self.lEChs.text(),
                -1,
                QtCore.Qt.MatchStartsWith,
            )
            for match in matches:
                self.tVChs.selectionModel().select(
                    match,
                    QtCore.QItemSelectionModel.Select
                )


# запуск окна
def main():
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec_())


# инициализация функции окна
if __name__ == '__main__':
    main()
