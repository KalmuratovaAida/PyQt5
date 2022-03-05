from PyQt5 import uic
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog
from class_edit import ClassEdit


# создается класс формы Класса ЧС
class ClassForm(QDialog):
    def __init__(self):
        super(ClassForm, self).__init__()
        uic.loadUi("./ui/Class.ui", self)
        self.setWindowModality(1)

        self.model_class_init()
        self.ClassEdit = None
        self.model_group_init()
        self.model_vid_init()
        self.model_directory_init()

        self.BtnAddClass.clicked.connect(self.btnClickAddClass)
        self.BtnSaveClass.clicked.connect(self.btnClickSaveClass)
        self.BtnDelClass.clicked.connect(self.btnClikDelClass)
        self.tVClass.doubleClicked.connect(self.btnEditClass)
        self.tVClass.setModel(self.model_class)
        self.tVClass.hideColumn(0)
        self.tVClass.verticalHeader().setVisible(False)
        self.tVClass.resizeColumnsToContents()

        self.BtnAddGroup.clicked.connect(self.btnClickAddGroup)
        self.BtnSaveGroup.clicked.connect(self.btnClickSaveGroup)
        self.BtnDelGroup.clicked.connect(self.btnClikDelGroup)
        self.tVGroup.setModel(self.model_group)
        self.tVGroup.hideColumn(0)
        self.tVGroup.hideColumn(2)
        self.tVGroup.verticalHeader().setVisible(False)
        self.tVGroup.resizeColumnsToContents()

        self.tVVid.setModel(self.model_vid)
        self.tVVid.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.tVVid))
        self.BtnAddVid.clicked.connect(self.btnClickAddVid)
        self.BtnDelVid.clicked.connect(self.btnClickDelVid)
        self.BtnSaveVid.clicked.connect(self.btnClickSaveVid)
        self.tVVid.resizeColumnsToContents()
        self.tVVid.hideColumn(0)
        self.tVVid.hideColumn(1)
        self.tVVid.verticalHeader().setVisible(False)
        self.tVClass.clicked.connect(self.select)
        self.select()

        self.BtnAddDirect.clicked.connect(self.btnClickAddDirect)
        self.BtnDelDirect.clicked.connect(self.btnClickDelDirect)
        self.BtnSaveDirect.clicked.connect(self.btnClickSaveDirect)
        self.BtnRefreshDirect.clicked.connect(self.btnClickRefreshDirect)
        self.BtnCancelDirect.clicked.connect(self.btnClickCancelDirect)
        self.tVDirectory.setModel(self.model_directory)
        self.tVDirectory.setItemDelegateForColumn(2, QtSql.QSqlRelationalDelegate(self.tVDirectory))
        self.tVDirectory.resizeColumnsToContents()
        self.tVDirectory.hideColumn(0)
        self.tVDirectory.hideColumn(1)
        self.tVDirectory.verticalHeader().setVisible(False)
        self.tVVid.clicked.connect(self.tVDirectoryClick)
        self.tVDirectoryClick()
        self.tVGroup.clicked.connect(self.select1)
        self.select1()

    def select(self):
        if self.model_class.rowCount():
            cur_row = self.tVClass.currentIndex().row()
            self.id_Class = self.model_class.record(cur_row).value("id_Class")
        else:
            self.id_Class = -1
        self.model_group.setFilter(f"id_Class={self.id_Class}")

    def select1(self):
        if self.model_group.rowCount():
            cur_row = self.tVGroup.currentIndex().row()
            self.id_Group = self.model_group.record(cur_row).value("id_Group")
        else:
            self.id_Group = -1
        self.model_vid.setFilter(f"id_Group={self.id_Group}")


    def tVDirectoryClick(self):
        if self.model_vid.rowCount():
            cur_row = self.tVVid.currentIndex().row()
            self.id_Vid = self.model_vid.record(cur_row).value("id_Vid")
        else:
            self.id_Vid = -1
        self.model_directory.setFilter(f"id_Vid = {self.id_Vid}")


    def model_class_init(self):
        self.model_class = QtSql.QSqlTableModel(self)
        self.model_class.setTable("class")
        self.model_class.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model_class.select()
        self.model_class.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование класса")

    def model_group_init(self):
        self.model_group = QtSql.QSqlRelationalTableModel(self)
        self.model_group.setTable("gruppa")
        self.model_group.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        # self.model_group.setRelation(2, QtSql.QSqlRelation("class", "id_Class", "name"))
        self.model_group.select()
        self.model_group.setHeaderData(1, QtCore.Qt.Horizontal, "Группа ЧС")
        #self.model_group.setHeaderData(2, QtCore.Qt.Horizontal, "Класс ЧС")

    def model_vid_init(self):
        self.model_vid = QtSql.QSqlRelationalTableModel(self)
        self.model_vid.setTable("vid")
        self.model_vid.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        #self.model_vid.setRelation(1, QtSql.QSqlRelation("gruppa", "id_Group", "name1"))
        self.model_vid.select()
        #self.model_vid.setHeaderData(1, QtCore.Qt.Horizontal, "Группа ЧС")
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


    def btnClickAddClass(self):
        if not self.ClassEdit:
            self.ClassEdit = ClassEdit()

        self.ClassEdit.lEClass.clear()

        if self.ClassEdit.exec_():
            record = self.model_class.record()
            # record.remove(0)
            record.remove(record.indexOf("id_Class"))
            record.setValue("name", self.ClassEdit.lEClass.text())
            self.model_class.insertRecord(-1, record)
            if not self.model_class.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_class.lastError().text() + "\nЗапись не была добавлена",
                                     QMessageBox.Ok)

    def btnEditClass(self):
        cur_row = self.tVClass.currentIndex().row()
        if not self.ClassEdit:
            self.ClassEdit = ClassEdit()

        self.ClassEdit.lEClass.setText(self.model_class.record(cur_row).value("name"))
        if self.ClassEdit.exec_():
            self.model_class.setData(self.model_class.index(cur_row, 1), self.ClassEdit.lEClass.text())
            if not self.model_class.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_class.lastError().text() + "\nЗапись не была изменена",
                                     QMessageBox.Ok)

    def btnClickSaveClass(self):
        if not self.model_class.submitAll():
            QMessageBox.critical(self,
                                 "Ошибка",
                                 self.model_class.lastError().text() + "\nСохранение не было выполнена",
                                 QMessageBox.Ok)

    def btnClikDelClass(self):
        cur_row = self.tVClass.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить класс" + self.model_class.record(cur_row).value(
                                    "name") + "?",
                                QMessageBox.Cancel, QMessageBox.Ok):
            self.model_class.removeRow(cur_row)
            if not self.model_class.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_class.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)

    def btnClickAddVid(self):
        record = self.model_vid.record()
        record.remove(record.indexOf("id_Vid"))
        record.setValue("id_Group", self.id_Group)
        self.model_vid.insertRecord(-1, record)
        index = self.model_vid.index(self.model_vid.rowCount() - 1, 1)
        self.tVVid.edit(index)

    def btnClickDelVid(self):
        cur_row = self.tVVid.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить?",
                                QMessageBox.Cancel, QMessageBox.Ok) == QMessageBox.Ok:
            self.model_vid.removeRow(cur_row)
            if not self.model_vid.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_vid.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)

    def btnClickSaveVid(self):
        if not self.model_vid.submitAll():
            QMessageBox(self,
                        "Ошибка",
                        self.model_vid.lastError().text() + "\nСохранение не были сохранены",
                        QMessageBox.Ok
                        )
        self.model_vid.select()

    def btnClickAddGroup(self):
        record = self.model_group.record()
        record.remove(record.indexOf("id_Group"))
        record.setValue("id_Class", self.id_Class)
        self.model_group.insertRecord(-1, record)
        index = self.model_group.index(self.model_group.rowCount() - 1, 1)
        self.tVGroup.edit(index)

    def btnClickSaveGroup(self):
        if not self.model_group.submitAll():
            QMessageBox(self,
                        "Ошибка",
                        self.model_group.lastError().text() + "\nСохранение не были сохранены",
                        QMessageBox.Ok
                        )

    def btnClikDelGroup(self):
        cur_row = self.tVGroup.currentIndex().row()
        if QMessageBox.question(self, "Подтвердите удаление",
                                "Вы действительно хотите удалить?",
                                QMessageBox.Cancel, QMessageBox.Ok) == QMessageBox.Ok:
            self.model_group.removeRow(cur_row)
            if not self.model_group.submitAll():
                QMessageBox.critical(self,
                                     "Ошибка",
                                     self.model_group.lastError().text() + "\nУдаление не было выполнена",
                                     QMessageBox.Ok)



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
