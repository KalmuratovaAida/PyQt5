from PyQt5 import uic
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog


class FeatureForm(QDialog):
    def __init__(self):
        super(FeatureForm, self).__init__()
        uic.loadUi("./ui/FP.ui", self)
        self.setWindowModality(2)

        self.model_feature_init()
        self.model_possible_init()
        self.feature_init()

    def feature_init(self):
        self.BtnAddFeature.clicked.connect(self.btnClickAddFeature)
        self.BtnSaveFeature.clicked.connect(self.btnClickSaveFeature)
        self.BtnDelFeature.clicked.connect(self.btnClikDelFeature)


        self.BtnAddPossible.clicked.connect(self.btnClickAddPossible)
        self.BtnSavePossible.clicked.connect(self.btnClickSavePossible)
        self.BtnDelPossible.clicked.connect(self.btnClikDelPossible)

        self.tVFeature.setModel(self.model_feature)
        self.tVFeature.hideColumn(0)
        self.tVFeature.verticalHeader().setVisible(False)
        self.tVFeature.resizeColumnsToContents()
        self.tVFeature.clicked.connect(self.SelectFeature)
        self.SelectFeature()
        self.tVPossible.setModel(self.model_possible)
        #self.tVPossible.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.tVPossible))
        self.tVPossible.hideColumn(0)
        self.tVPossible.hideColumn(1)
        self.tVPossible.verticalHeader().setVisible(False)
        self.tVPossible.resizeColumnsToContents()


    def SelectFeature(self):
        if self.model_feature.rowCount():
            cur_row = self.tVFeature.currentIndex().row()
            self.id_feature = self.model_feature.record(cur_row).value("id_feature")
        else:
            self.id_feature = -1
        self.model_possible.setFilter(f"id_feature={self.id_feature}")

    def model_feature_init(self):
        self.model_feature = QtSql.QSqlRelationalTableModel(self)
        self.model_feature .setTable("feature")
        self.model_feature.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model_feature.select()
        self.model_feature.setHeaderData(1, QtCore.Qt.Horizontal, "Причины ЧС")

    def model_possible_init(self):
        self.model_possible = QtSql.QSqlRelationalTableModel(self)
        self.model_possible.setTable("possible")
        self.model_possible.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        #self.model_feature.setRelation(1, QtSql.QSqlRelation("feature", "id_feature", "name3"))
        self.model_possible.select()
        #self.model_possible.setHeaderData(1, QtCore.Qt.Horizontal, "Причины ЧС")
        self.model_possible.setHeaderData(2, QtCore.Qt.Horizontal, "Дополнительные причины")

    def btnClickAddFeature(self):
        record = self.model_feature.record()
        record.remove(record.indexOf("id_feature"))
        self.model_feature.insertRecord(-1, record)
        index = self.model_feature.index(self.model_feature.rowCount() - 1, 1)
        self.tVFeature.edit(index)

    def btnClickSaveFeature(self):
        if not self.model_feature.submitAll():
            QMessageBox(self,
                        "Ошибка",
                        self.model_feature.lastError().text() + "\nСохранение не были сохранены",
                        QMessageBox.Ok
                        )

    def btnClikDelFeature(self):
        cur_row = self.tVFeature.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить?",
                                QMessageBox.Cancel, QMessageBox.Ok) == QMessageBox.Ok:
            self.model_feature.removeRow(cur_row)
            if not self.model_feature.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_feature.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)

    def btnClickAddPossible(self):
        record = self.model_possible.record()
        record.remove(record.indexOf("id_possible"))
        record.setValue("id_feature", self.id_feature)
        self.model_possible.insertRecord(-1, record)
        index = self.model_possible.index(self.model_possible.rowCount() - 1, 1)
        self.tVPossible.edit(index)

    def btnClickSavePossible(self):
        if not self.model_possible.submitAll():
            QMessageBox(self,
                        "Ошибка",
                        self.model_possible.lastError().text() + "\nСохранение не были сохранены",
                        QMessageBox.Ok
                        )

    def btnClikDelPossible(self):
        cur_row = self.tVPossible.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить?",
                                QMessageBox.Cancel, QMessageBox.Ok) == QMessageBox.Ok:
            self.model_possible.removeRow(cur_row)
            if not self.model_possible.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_possible.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)
