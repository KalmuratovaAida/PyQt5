from PyQt5 import uic
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog
from datetime import datetime, timedelta


# создается класс формы Класса ЧС
class VidForm(QDialog):
    def __init__(self):
        super(VidForm, self).__init__()
        uic.loadUi("./ui/Vid.ui", self)
        self.setWindowModality(1)

        self.model_vid_init()
        self.model_directory_init()
        self.vid_init()

    def vid_init(self):
        self.tVVid.setModel(self.model_vid)
        self.tVVid.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.tVVid))
        self.BtnAddVid.clicked.connect(self.btnClickAddVid)
        self.BtnDelVid.clicked.connect(self.btnClickDelVid)
        self.BtnSaveVid.clicked.connect(self.btnClickSaveVid)
        self.tVDirectory.setModel(self.model_directory)
        self.BtnAddDirect.clicked.connect(self.btnClickAddDirect)
        self.BtnDelDirect.clicked.connect(self.btnClickDelDirect)
        self.BtnSaveDirect.clicked.connect(self.btnClickSaveDirect)
        self.BtnRefreshDirect.clicked.connect(self.btnClickRefreshDirect)
        self.BtnCancelDirect.clicked.connect(self.btnClickCancelDirect)
        #self.tVDirectory.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.tVDirectory))
        self.tVDirectory.setItemDelegateForColumn(2, QtSql.QSqlRelationalDelegate(self.tVDirectory))
        self.tVVid.clicked.connect(self.tVDirectoryClick)
        self.tVVid.resizeColumnsToContents()
        self.tVDirectory.resizeColumnsToContents()
        self.tVDirectoryClick()
        self.tVVid.hideColumn(0)
        self.tVVid.hideColumn(1)
        self.tVVid.verticalHeader().setVisible(False)
        self.tVDirectory.hideColumn(0)
        self.tVDirectory.hideColumn(1)
        self.tVDirectory.verticalHeader().setVisible(False)
        self.lEVid.textEdited.connect(self.LEVid)

    def model_vid_init(self):
        self.model_vid = QtSql.QSqlRelationalTableModel(self)
        self.model_vid.setTable("vid")
        self.model_vid.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model_vid.setRelation(1, QtSql.QSqlRelation("gruppa", "id_Group", "name1"))
        self.model_vid.select()
        self.model_vid.setHeaderData(1, QtCore.Qt.Horizontal, "Группа ЧС")
        self.model_vid.setHeaderData(2, QtCore.Qt.Horizontal, "Вид ЧС")

    def model_directory_init(self):
        self.model_directory = QtSql.QSqlRelationalTableModel(self)
        self.model_directory.setTable("directory")
        self.model_directory.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        #self.model_directory.setRelation(1, QtSql.QSqlRelation("vid", "id_Vid", "name2"))
        self.model_directory.setRelation(2, QtSql.QSqlRelation("feature", "id_feature", "name3"))
        self.model_directory.select()
        #self.model_directory.setHeaderData(1, QtCore.Qt.Horizontal, "Вид ЧС")
        self.model_directory.setHeaderData(2, QtCore.Qt.Horizontal, "Характеристика ЧС")



    def btnClickAddVid(self):
        record = self.model_vid.record()
        record.remove(record.indexOf("id_Vid"))
        self.model_vid.insertRecord(-1, record)
        index = self.model_vid.index(self.model_vid.rowCount() - 1, 1)
        self.tVVid.edit(index)

    def btnClickDelVid(self):
        cur_row = self.tVVid.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить?",
                                QMessageBox.Cancel, QMessageBox.Ok) == QMessageBox.Ok:

            if not self.model_vid.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_vid.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)
            self.model_vid.removeRow(cur_row)

    def btnClickSaveVid(self):
        if not self.model_vid.submitAll():
            QMessageBox(self,
                        "Ошибка",
                        self.model_vid.lastError().text() + "\nСохранение не были сохранены",
                        QMessageBox.Ok
                        )
        self.model_vid.select()

    def tVDirectoryClick(self):
        if self.tVVid.selectedIndex():
            cur_row = self.tVVid.currentIndex().row()
            self.id_Vid = self.model_vid.record(cur_row).value("id_Vid")
        else:
            self.id_Vid = self.model_vid.record(0).value("id_Vid")
        self.model_directory.setFilter(f"id_Vid = {self.id_Vid}")

    def btnClickAddDirect(self):
        record = self.model_directory.record()
        record.remove(record.indexOf("id_directory"))
        record.setValue("id_Vid", self.id_Vid)
        self.model_directory.insertRecord(-1, record)
        index = self.model_directory.index(self.model_directory.rowCount() - 1, 1)
        self.tVDirectory.edit(index)


    def btnClickDelDirect(self):
        cur_row = self.tVDirectory.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить группу?",
                                QMessageBox.Cancel, QMessageBox.Ok) == QMessageBox.Ok:
            if not self.model_directory.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_directory.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)
            self.model_directory.removeRow(cur_row)

    def btnClickSaveDirect(self):
        if not self.model_directory.submitAll():
            QMessageBox(self,
                        "Ошибка",
                        self.model_directory.lastError().text() + "\nСохранение не были сохранены",
                        QMessageBox.Ok
                        )
        self.model_directory.select()


    def btnClickRefreshDirect(self):
        self.model_directory.select()

    def btnClickCancelDirect(self):
        self.model_directory.revertAll()

    def LEVid(self):
        if self.lEVid.text() != "":
            self.tVVid.selectionModel().clearSelection()
            start = self.model_vid.index(0, 2)
            matches = self.model_vid.match(
                start,
                QtCore.Qt.DisplayRole,
                self.lEVid.text(),
                -1,
                QtCore.Qt.MatchStartsWith,
            )
            for match in matches:
                self.tVVid.selectionModel().select(
                    match,
                    QtCore.QItemSelectionModel.Select
                )

