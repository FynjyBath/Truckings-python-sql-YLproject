import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
from PyQt5.QtGui import QPixmap


class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.but_enter = QtWidgets.QPushButton(self)
        self.but_enter.move(200, 660)
        self.but_enter.resize(1000, 100)
        self.but_enter.setFont(font)
        self.but_enter.setObjectName("pushButton")

        font.setItalic(True)
        self.label = QtWidgets.QLabel(self)
        self.label.move(450, 10)
        self.label.setFont(font)
        self.label.resize(900, 80)
        self.label.setText("Грузоперевозки SimpleWay")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.but_enter.setText(_translate("MainWindow", "Начать работу"))
        self.but_enter.clicked.connect(self.f_enter)

        self.pixmap = QPixmap('main_photo.png')
        self.image = QLabel(self)
        self.image.move(180, 80)
        self.image.resize(1000, 550)
        self.image.setPixmap(self.pixmap)

    def f_enter(self):
        self.hide()
        self.form = Enter()
        self.form.show()


class Enter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('transportation.db')
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 50, 1291, 651))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.password = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.password.setFont(font)
        self.password.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.password, 1, 1, 1, 1)

        self.login_box = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.login_box.setFont(font)
        self.login_box.setObjectName("comboBox")
        self.gridLayout.addWidget(self.login_box, 0, 1, 1, 1)

        self.but_enter = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.but_enter.setFont(font)
        self.but_enter.setObjectName("pushButton")
        self.gridLayout.addWidget(self.but_enter, 2, 0, 1, 2)

        self.but_registration = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.but_registration.setFont(font)
        self.but_registration.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.but_registration.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.but_registration, 3, 0, 1, 2)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.but_enter.setText(_translate("MainWindow", "Вход"))
        self.label.setText(_translate("MainWindow", "Логин:"))
        self.but_registration.setText(_translate("MainWindow", "Регистрация"))
        self.label_2.setText(_translate("MainWindow", "Пароль:"))

        self.pixmap = QPixmap('key.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(50, 50)
        self.image.setPixmap(self.pixmap)

        cur = self.con.cursor()
        p = cur.execute(f"""SELECT name FROM users""").fetchall()
        for i in sorted(p):
            self.login_box.addItem(str(i[0]))
        self.but_registration.clicked.connect(self.f_registration)
        self.but_enter.clicked.connect(self.f_enter)

    def f_enter(self):
        cur = self.con.cursor()
        p = cur.execute(f"""SELECT password, user_id FROM users
                    WHERE name = '{self.login_box.currentText()}'""").fetchall()[0]
        if str(p[0]) != self.password.text():
            self.statusbar.show()
            self.statusbar.setStyleSheet("background-color:red;")
            self.statusbar.showMessage('Неверный пароль')
            f = open('logs.txt', encoding='utf-8')
            text = f.read()
            f.close()
            f = open('logs.txt', 'w', encoding='utf-8')
            print(text + 'Ошибка входа: ' + self.login_box.currentText() + ' ' + str(datetime.datetime.now()), file=f)
            f.close()
            return

        f = open('logs.txt', encoding='utf-8')
        text = f.read()
        f.close()
        f = open('logs.txt', 'w', encoding='utf-8')
        print(text + 'Успешный вход: ' + self.login_box.currentText() + ' ' + str(datetime.datetime.now()), file=f)
        f.close()

        self.hide()
        self.form = TruckerClient(p[1])
        self.form.show()

    def f_registration(self):
        self.hide()
        self.form = Registration()
        self.form.show()


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 40, 1291, 681))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.password = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.password.setFont(font)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 1, 1, 1)

        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.but_reg = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.but_reg.setFont(font)
        self.but_reg.setObjectName("but_reg")
        self.gridLayout.addWidget(self.but_reg, 2, 0, 1, 2)

        self.but_return = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.gridLayout.addWidget(self.but_return, 3, 0, 1, 2)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.but_reg.setText(_translate("MainWindow", "Создать аккаунт"))
        self.label.setText(_translate("MainWindow", "Логин:"))
        self.label_2.setText(_translate("MainWindow", "Пароль:"))
        self.but_return.setText(_translate("MainWindow", "Назад"))

        self.pixmap = QPixmap('key.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(50, 50)
        self.image.setPixmap(self.pixmap)

        self.con = sqlite3.connect('transportation.db')
        self.but_reg.clicked.connect(self.f_reg)
        self.but_return.clicked.connect(self.f_return)

    def f_reg(self):
        cur = self.con.cursor()
        p = cur.execute(f"""SELECT name FROM users
                            WHERE name = '{self.name.text()}'""").fetchall()
        if len(p) > 0:
            self.statusbar.show()
            self.statusbar.setStyleSheet("background-color:red;")
            self.statusbar.showMessage('Это имя пользователя уже существует')
            return

        if self.password.text() == '' or self.name.text() == '':
            self.statusbar.show()
            self.statusbar.setStyleSheet("background-color:red;")
            self.statusbar.showMessage('Не все данные введены')
            return

        cur.execute(f"""INSERT INTO users(name, password)
                        VALUES ('{self.name.text()}', '{self.password.text()}')""")
        self.con.commit()
        self.hide()
        self.form = Success('', 'Enter')
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = Enter()
        self.form.show()


class TruckerClient(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.but1 = QtWidgets.QPushButton(self.centralwidget)
        self.but1.setGeometry(QtCore.QRect(50, 130, 1279, 101))
        self.but1.setFont(font)
        self.but1.setObjectName("but1")

        self.but2 = QtWidgets.QPushButton(self.centralwidget)
        self.but2.setGeometry(QtCore.QRect(50, 290, 1279, 101))
        self.but2.setFont(font)
        self.but2.setObjectName("but2")

        self.but_return = QtWidgets.QPushButton(self.centralwidget)
        self.but_return.setGeometry(QtCore.QRect(50, 540, 1279, 81))
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.but1.setText(_translate("MainWindow", "Меню клиента"))
        self.but2.setText(_translate("MainWindow", "Меню грузоперевозчика"))
        self.but_return.setText(_translate("MainWindow", "Назад"))

        self.pixmap = QPixmap('choose.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(50, 50)
        self.image.setPixmap(self.pixmap)

        self.but1.clicked.connect(self.open_client_menu)
        self.but2.clicked.connect(self.open_trucker_menu)
        self.but_return.clicked.connect(self.f_return)

    def open_trucker_menu(self):
        self.hide()
        self.form = TruckTrucking(self.user_id)
        self.form.show()

    def open_client_menu(self):
        self.hide()
        self.form = AddDelOrder(self.user_id)
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = Enter()
        self.form.show()


class AddDelOrder(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.but1 = QtWidgets.QPushButton(self.centralwidget)
        self.but1.setGeometry(QtCore.QRect(50, 130, 1279, 101))
        self.but1.setFont(font)
        self.but1.setObjectName("but1")

        self.but2 = QtWidgets.QPushButton(self.centralwidget)
        self.but2.setGeometry(QtCore.QRect(50, 290, 1279, 101))
        self.but2.setFont(font)
        self.but2.setObjectName("but2")

        self.but_return = QtWidgets.QPushButton(self.centralwidget)
        self.but_return.setGeometry(QtCore.QRect(50, 540, 1279, 81))
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.but1.setText(_translate("MainWindow", "Просмотреть/удалить/изменить заказы"))
        self.but2.setText(_translate("MainWindow", "Добавить заказ"))
        self.but_return.setText(_translate("MainWindow", "Назад"))

        self.pixmap = QPixmap('order.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(80, 54)
        self.image.setPixmap(self.pixmap)

        self.but1.clicked.connect(self.open_del_order)
        self.but2.clicked.connect(self.open_add_order)
        self.but_return.clicked.connect(self.f_return)

    def open_del_order(self):
        self.hide()
        self.form = DelOrder(self.user_id)
        self.form.show()

    def open_add_order(self):
        self.hide()
        self.form = AddOrder(self.user_id)
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = TruckerClient(self.user_id)
        self.form.show()


class DelOrder(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(20)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 50, 1291, 651))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.but_return = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.verticalLayout.addWidget(self.but_return)

        self.but_delete = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_delete.setFont(font)
        self.but_delete.setObjectName("but_delete")
        self.verticalLayout.addWidget(self.but_delete)

        self.but_change = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_change.setFont(font)
        self.but_change.setObjectName("but_delete")
        self.verticalLayout.addWidget(self.but_change)

        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("widget", "SimpleWay"))
        self.but_return.setText(_translate("widget", "Назад"))
        self.but_delete.setText(_translate("widget", "Удалить"))
        self.but_change.setText(_translate("widget", "Изменить"))

        self.but_change.clicked.connect(self.change_item)
        self.con = sqlite3.connect("transportation.db")
        self.cur = self.con.cursor()
        self.but_delete.clicked.connect(self.delete_elem)
        self.but_return.clicked.connect(self.f_return)
        self.update_result()

    def change_item(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) != 1:
            self.statusbar.setStyleSheet("background-color:red;")
            self.statusbar.showMessage("Выберите только один вариант")
            return
        self.hide()
        self.form = ChangeOrder(self.user_id, ids[0])
        self.form.show()

    def update_result(self):
        result = self.cur.execute("SELECT * FROM orders WHERE user_id=?",
                             (self.user_id,)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['id заказа', 'ваш id', 'id перевозки', 'объём', 'комментарии'])
        self.titles = [description[0] for description in self.cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) == 0:
            self.statusbar.setStyleSheet("background-color:red;")
            self.statusbar.showMessage("Выберите, что хотите удалить")
            return
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids) + '?',
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            for i in ids:
                now = self.cur.execute(f"""SELECT * FROM orders
                                           WHERE order_id = {i}""").fetchall()[0]
                k = self.cur.execute(f'''SELECT quadratic_metres_left FROM truckings
                                         WHERE trucking_id = {now[2]}''').fetchall()[0][0]
                self.cur.execute(f'''UPDATE truckings
                                     SET quadratic_metres_left = {k + now[3]}
                                     WHERE trucking_id = {now[2]}''')
            self.cur.execute("DELETE FROM orders WHERE order_id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()
        self.update_result()

    def f_return(self):
        self.hide()
        self.form = AddDelOrder(self.user_id)
        self.form.show()


class ChangeOrder(QMainWindow):
    def __init__(self, user_id, order_id):
        super().__init__()
        self.user_id = user_id
        self.order_id = order_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(320, 180, 751, 461))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.double_capacity = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.double_capacity.setFont(font)
        self.double_capacity.setObjectName("double_capacity")
        self.gridLayout.addWidget(self.double_capacity, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.but_change = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.but_change.setFont(font)
        self.but_change.setObjectName("but_change")
        self.gridLayout.addWidget(self.but_change, 2, 0, 1, 2)
        self.line_comments = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.line_comments.setFont(font)
        self.line_comments.setObjectName("line_comments")
        self.gridLayout.addWidget(self.line_comments, 1, 1, 1, 1)
        self.but_return = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.gridLayout.addWidget(self.but_return, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(320, 70, 749, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.label_3.setText(_translate("MainWindow", "Комментарии:"))
        self.label_2.setText(_translate("MainWindow", "Объём, м²:"))
        self.but_change.setText(_translate("MainWindow", "Изменить"))
        self.but_return.setText(_translate("MainWindow", "Назад"))
        self.label.setText(_translate("MainWindow", "Введите новые данные заказа:"))

        self.con = sqlite3.connect("transportation.db")
        self.cur = self.con.cursor()
        self.but_return.clicked.connect(self.f_return)
        self.but_change.clicked.connect(self.f_change)

        now = self.cur.execute(f"""SELECT * FROM orders
                                   WHERE order_id = {self.order_id}""").fetchall()[0]
        self.double_capacity.setValue(now[3])
        k = self.cur.execute(f'''SELECT quadratic_metres_left FROM truckings
                                 WHERE trucking_id = {now[2]}''').fetchall()[0][0]
        self.double_capacity.setRange(0.01, k + now[3])
        self.line_comments.setText(str(now[4]))

    def f_change(self):
        ids = [self.order_id]
        i = ids[0]

        now = self.cur.execute(f"""SELECT * FROM orders
                                                   WHERE order_id = {i}""").fetchall()[0]
        k = self.cur.execute(f'''SELECT quadratic_metres_left FROM truckings
                                                 WHERE trucking_id = {now[2]}''').fetchall()[0][0]

        valid = QMessageBox.question(
            self, '', "Действительно изменить элемент с id " + ",".join(ids) + '?',
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.cur.execute(f'''UPDATE truckings
                                 SET quadratic_metres_left = {k + now[3] - self.double_capacity.value()}
                                 WHERE trucking_id = {now[2]}''')

            self.cur.execute(f'''UPDATE orders
                                 SET capacity = {self.double_capacity.value()}
                                 WHERE order_id = {i}''')
            self.cur.execute(f'''UPDATE orders
                                 SET comments = '{self.line_comments.text()}'
                                 WHERE order_id = {i}''')

            self.con.commit()

        self.hide()
        self.form = DelOrder(self.user_id)
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = DelOrder(self.user_id)
        self.form.show()


class AddOrder(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("QMainWindow")
        self.resize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 20, 1301, 761))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.double_capacity = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.double_capacity.setFont(font)
        self.double_capacity.setObjectName("double_capacity")
        self.gridLayout.addWidget(self.double_capacity, 7, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_9.setFont(font)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_6.setFont(font)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 1, 1, 1)
        self.calendar_departure_date = QtWidgets.QCalendarWidget(self.gridLayoutWidget)
        self.calendar_departure_date.setObjectName("departure_date")
        self.gridLayout.addWidget(self.calendar_departure_date, 5, 1, 1, 1)
        now = datetime.datetime.now()
        now1 = datetime.datetime.now() + datetime.timedelta(365)
        self.calendar_departure_date.setDateRange(now, now1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(3)
        self.label_7.setFont(font)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 10, 1, 1, 1)
        self.line_arrival_city = QtWidgets.QComboBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.line_arrival_city.setFont(font)
        self.line_arrival_city.setObjectName("line_arrival_city")
        self.gridLayout.addWidget(self.line_arrival_city, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.but_return = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.gridLayout.addWidget(self.but_return, 12, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 9, 0, 1, 1)
        self.line_comments = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.line_comments.setFont(font)
        self.line_comments.setObjectName("line_comments")
        self.gridLayout.addWidget(self.line_comments, 9, 1, 1, 1)
        self.line_departure_city = QtWidgets.QComboBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.line_departure_city.setFont(font)
        self.line_departure_city.setObjectName("line_departure_city")
        self.gridLayout.addWidget(self.line_departure_city, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.but_view_variants = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.but_view_variants.setFont(font)
        self.but_view_variants.setObjectName("but_view_variants")
        self.gridLayout.addWidget(self.but_view_variants, 11, 0, 1, 2)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 7, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_8.setFont(font)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 6, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_11.setFont(font)
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 8, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "SimpleWay"))
        self.label_5.setText(_translate("Form", "Дата отправления:"))
        self.label_3.setText(_translate("Form", "Город прибытия:"))
        self.but_return.setText(_translate("Form", "Назад"))
        self.label_4.setText(_translate("Form", "Комментарии:"))
        self.label_2.setText(_translate("Form", "Город отправления:"))
        self.label_10.setText(_translate("Form", "Объём груза:"))
        self.but_view_variants.setText(_translate("Form", "Далее"))
        self.label.setText(_translate("Form", "Введите данные:"))

        self.con = sqlite3.connect('transportation.db')
        self.cur = self.con.cursor()

        p = self.cur.execute(f'''SELECT DISTINCT departure_city FROM truckings''').fetchall()
        for i in sorted(p):
            self.line_departure_city.addItem(i[0])

        p = self.cur.execute(f'''SELECT DISTINCT arrival_city FROM truckings''').fetchall()
        for i in sorted(p):
            self.line_arrival_city.addItem(i[0])

        self.double_capacity.setRange(0.01, 1000.0)
        self.but_view_variants.clicked.connect(self.open_complete_order)
        self.but_return.clicked.connect(self.f_return)

    def open_complete_order(self):
        self.hide()
        self.form = CompleteOrder(self.user_id, (self.line_departure_city.currentText(),
                                                 self.line_arrival_city.currentText(),
                                                 str(self.calendar_departure_date.selectedDate().day()) + '.' +
                                                 str(self.calendar_departure_date.selectedDate().month()) + '.' +
                                                 str(self.calendar_departure_date.selectedDate().year()),
                                                 self.double_capacity.value(),
                                                 self.line_comments.text()))
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = AddDelOrder(self.user_id)
        self.form.show()


class CompleteOrder(QMainWindow):
    def __init__(self, user_id, data):
        super().__init__()
        self.user_id = user_id
        self.data = data
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(20)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 50, 1291, 651))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.but_return = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.verticalLayout.addWidget(self.but_return)

        self.but_choose = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_choose.setFont(font)
        self.but_choose.setObjectName("but_delete")
        self.verticalLayout.addWidget(self.but_choose)

        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("widget", "SimpleWay"))
        self.but_return.setText(_translate("widget", "Назад"))
        self.but_choose.setText(_translate("widget", "Выбрать"))

        self.con = sqlite3.connect("transportation.db")
        self.cur = self.con.cursor()
        self.but_choose.clicked.connect(self.choose_elem)
        self.but_return.clicked.connect(self.f_return)
        self.update_result()

    def update_result(self):
        result = self.cur.execute(f'''SELECT * FROM truckings 
            WHERE departure_city = "{self.data[0]}" AND arrival_city = "{self.data[1]}"
            AND quadratic_metres_left >= {self.data[3]}''').fetchall()
        result = [i for i in result if i[4].split('.')[::-1] >= self.data[2].split('.')[::-1]]
        for i in range(len(result)):
            result[i] = result[i][:10] + (result[i][10] * self.data[3], result[i][11])
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['id грузоперевозки', 'id пользователя', 'комментарии',
                                                    'город вывоза',
                                                    'дата вывоза', 'время вывоза', 'город ввоза', 'дата ввоза',
                                                    'время ввоза', 'id машины', 'стоимость',
                                                    'осталось места'])
        self.titles = [description[0] for description in self.cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def choose_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) != 1:
            self.statusbar.setStyleSheet("background-color:red;")
            self.statusbar.showMessage("Выберите только один вариант")
            return
        cost = self.cur.execute(f'''SELECT cost_per_quadratic_meter FROM truckings
                                             WHERE trucking_id = {ids[0]}''').fetchall()[0][0] * self.data[3]
        valid = QMessageBox.question(
            self, '', f"Действительно выбрать способ перевозки с id {ids[0]} и стоимостью {cost}?",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            k = self.cur.execute(f'''SELECT quadratic_metres_left FROM truckings
                                     WHERE trucking_id = {ids[0]}''').fetchall()[0][0]
            self.cur.execute(f'''UPDATE truckings
                                 SET quadratic_metres_left = {k - self.data[3]}
                                 WHERE trucking_id = {ids[0]}''')
            self.cur.execute(f'''INSERT INTO orders(user_id, trucking_id, capacity, comments) 
                                 VALUES({self.user_id}, {ids[0]}, {self.data[3]}, "{self.data[-1]}")''')

            fname = QFileDialog.getSaveFileName(self, 'Сохранить чек', '', '*.txt')
            print(fname[0])
            if fname[0]:
                k = max(self.cur.execute(f'''SELECT order_id FROM orders''').fetchall())[0]
                f = open(fname[0], mode='w', encoding='utf-8')
                print(f'''***
Кассовый чек №{k}
Отправление из {self.data[0]} в {self.data[1]}
Зарезервировано {self.data[3]} объёма
Оплата на сумму {cost} рублей
***''', file=f)
                f.close()

            self.con.commit()
            self.update_result()

            self.hide()
            self.form = Success(self.user_id, 'Order')
            self.form.show()

    def f_return(self):
        self.hide()
        self.form = AddDelOrder(self.user_id)
        self.form.show()


class TruckTrucking(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.but1 = QtWidgets.QPushButton(self.centralwidget)
        self.but1.setGeometry(QtCore.QRect(50, 130, 1279, 101))
        self.but1.setFont(font)
        self.but1.setObjectName("but1")

        self.but2 = QtWidgets.QPushButton(self.centralwidget)
        self.but2.setGeometry(QtCore.QRect(50, 290, 1279, 101))
        self.but2.setFont(font)
        self.but2.setObjectName("but2")

        self.but_return = QtWidgets.QPushButton(self.centralwidget)
        self.but_return.setGeometry(QtCore.QRect(50, 540, 1279, 81))
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.but1.setText(_translate("MainWindow", "Работа с машинами"))
        self.but2.setText(_translate("MainWindow", "Работа с грузоперевозками"))
        self.but_return.setText(_translate("MainWindow", "Назад"))

        self.pixmap = QPixmap('bus.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(100, 57)
        self.image.setPixmap(self.pixmap)

        self.but1.clicked.connect(self.open_add_del_truck)
        self.but2.clicked.connect(self.open_add_del_trucking)
        self.but_return.clicked.connect(self.f_return)

    def open_add_del_truck(self):
        self.hide()
        self.form = AddDelTruck(self.user_id)
        self.form.show()

    def open_add_del_trucking(self):
        self.hide()
        self.form = AddDelTrucking(self.user_id)
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = TruckerClient(self.user_id)
        self.form.show()


class AddDelTruck(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.but1 = QtWidgets.QPushButton(self.centralwidget)
        self.but1.setGeometry(QtCore.QRect(50, 130, 1279, 101))
        self.but1.setFont(font)
        self.but1.setObjectName("but1")

        self.but2 = QtWidgets.QPushButton(self.centralwidget)
        self.but2.setGeometry(QtCore.QRect(50, 290, 1279, 101))
        self.but2.setFont(font)
        self.but2.setObjectName("but2")

        self.but_return = QtWidgets.QPushButton(self.centralwidget)
        self.but_return.setGeometry(QtCore.QRect(50, 540, 1279, 81))
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.but1.setText(_translate("MainWindow", "Добавить машину"))
        self.but2.setText(_translate("MainWindow", "Удалить/просмотреть машину"))
        self.but_return.setText(_translate("MainWindow", "Назад"))

        self.pixmap = QPixmap('bus.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(100, 57)
        self.image.setPixmap(self.pixmap)

        self.but1.clicked.connect(self.open_add_truck)
        self.but2.clicked.connect(self.open_del_truck)
        self.but_return.clicked.connect(self.f_return)

    def open_add_truck(self):
        self.hide()
        self.form = AddTruck(self.user_id)
        self.form.show()

    def open_del_truck(self):
        self.hide()
        self.form = DelTruck(self.user_id)
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = TruckTrucking(self.user_id)
        self.form.show()


class AddTruck(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 80, 1291, 651))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.line_comments = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_comments.setFont(font)
        self.line_comments.setObjectName("list_name")
        self.gridLayout.addWidget(self.line_comments, 2, 1, 1, 1)

        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.but_return = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.gridLayout.addWidget(self.but_return, 4, 0, 1, 2)

        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.line_model = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_model.setFont(font)
        self.line_model.setText("")
        self.line_model.setObjectName("line_model")
        self.gridLayout.addWidget(self.line_model, 0, 1, 1, 1)

        self.but_add_truck = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.but_add_truck.setFont(font)
        self.but_add_truck.setObjectName("but_add_truck")
        self.gridLayout.addWidget(self.but_add_truck, 3, 0, 1, 2)

        self.double_capacity = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.double_capacity.setFont(font)
        self.double_capacity.setObjectName("double_capacity")
        self.gridLayout.addWidget(self.double_capacity, 1, 1, 1, 1)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 20, 537, 81))
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "SimpleWay"))
        self.label.setText(_translate("Form", "Введите данные:"))
        self.but_return.setText(_translate("Form", "Назад"))
        self.label_2.setText(_translate("Form", "Введите модель:"))
        self.label_3.setText(_translate("Form", "Введите вместимость, м²:"))
        self.but_add_truck.setText(_translate("Form", "Добавить машину"))
        self.label_4.setText(_translate("Form", "Введите комментарии:"))

        self.con = sqlite3.connect('transportation.db')
        self.but_return.clicked.connect(self.f_return)
        self.but_add_truck.clicked.connect(self.f_add_truck)
        self.double_capacity.setRange(0.01, 1000.0)

    def f_add_truck(self):
        if self.line_comments.text() == '' or self.line_model.text() == '':
            self.statusbar.showMessage("Введены не все данные")
            self.statusbar.setStyleSheet("background-color:red;")
            return

        cur = self.con.cursor()
        cur.execute(f"""INSERT INTO trucks(user_id, comments, model, load_capacity)
            VALUES ('{self.user_id}', '{self.line_comments.text()}', '{self.line_model.text()}',
             '{self.double_capacity.value()}')""")
        self.con.commit()

        self.hide()
        self.form = Success(self.user_id, 'Truck')
        self.form.show()

    def f_return(self):
        try:
            self.dialog.hide()
        except Exception:
            pass
        self.hide()
        self.form = AddDelTruck(self.user_id)
        self.form.show()


class DelTruck(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(20)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 50, 1291, 651))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.but_return = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.verticalLayout.addWidget(self.but_return)

        self.but_delete = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_delete.setFont(font)
        self.but_delete.setObjectName("but_delete")
        self.verticalLayout.addWidget(self.but_delete)

        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "SimpleWay"))
        self.but_return.setText(_translate("widget", "Назад"))
        self.but_delete.setText(_translate("widget", "Удалить"))

        self.con = sqlite3.connect("transportation.db")
        self.but_delete.clicked.connect(self.delete_elem)
        self.but_return.clicked.connect(self.f_return)
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM trucks WHERE user_id=?",
                             (self.user_id,)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['id машины', 'id пользователя', 'комментарии', 'модель',
                                                    'вместимость'])
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) == 0:
            self.statusbar.setStyleSheet("background-color:red;")
            self.statusbar.showMessage("Выберите, что хотите удалить")
            return
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM trucks WHERE truck_id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)

            p = cur.execute("SELECT trucking_id FROM truckings WHERE truck_id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids).fetchall()
            cur.execute("DELETE FROM orders WHERE trucking_id IN (" + ", ".join(
                '?' * len(p)) + ")", p)
            cur.execute("DELETE FROM truckings WHERE truck_id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)

            self.con.commit()
        self.update_result()

    def f_return(self):
        self.hide()
        self.form = AddDelTruck(self.user_id)
        self.form.show()


class AddDelTrucking(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(25)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.but1 = QtWidgets.QPushButton(self.centralwidget)
        self.but1.setGeometry(QtCore.QRect(50, 130, 1279, 101))
        self.but1.setFont(font)
        self.but1.setObjectName("but1")

        self.but2 = QtWidgets.QPushButton(self.centralwidget)
        self.but2.setGeometry(QtCore.QRect(50, 290, 1279, 101))
        self.but2.setFont(font)
        self.but2.setObjectName("but2")

        self.but_return = QtWidgets.QPushButton(self.centralwidget)
        self.but_return.setGeometry(QtCore.QRect(50, 540, 1279, 81))
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "SimpleWay"))
        self.but1.setText(_translate("MainWindow", "Добавить грузоперевозку"))
        self.but2.setText(_translate("MainWindow", "Удалить/просмотреть грузоперевозку"))
        self.but_return.setText(_translate("MainWindow", "Назад"))

        self.pixmap = QPixmap('bus.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(100, 57)
        self.image.setPixmap(self.pixmap)

        self.but1.clicked.connect(self.open_add_trucking)
        self.but2.clicked.connect(self.open_del_trucking)
        self.but_return.clicked.connect(self.f_return)

    def open_add_trucking(self):
        self.hide()
        self.form = AddTrucking(self.user_id)
        self.form.show()

    def open_del_trucking(self):
        self.hide()
        self.form = DelTrucking(self.user_id)
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = TruckTrucking(self.user_id)
        self.form.show()


class AddTrucking(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 50, 1301, 681))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_12.setFont(font)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 4, 1, 1, 1)
        self.box_truck_id = QtWidgets.QComboBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.box_truck_id.setFont(font)
        self.box_truck_id.setObjectName("box_truck_id")
        self.gridLayout_2.addWidget(self.box_truck_id, 7, 3, 1, 1)
        self.line_comments = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_comments.setFont(font)
        self.line_comments.setObjectName("line_comments")
        self.gridLayout_2.addWidget(self.line_comments, 9, 2, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox.setFont(font)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_2.addWidget(self.doubleSpinBox, 7, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 9, 1, 1, 1)
        self.but_add_trucking = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.but_add_trucking.setFont(font)
        self.but_add_trucking.setObjectName("but_add_trucking")
        self.gridLayout_2.addWidget(self.but_add_trucking, 11, 0, 1, 4)
        self.but_return = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.but_return.setFont(font)
        self.but_return.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.but_return, 13, 0, 1, 4)

        now = datetime.datetime.now()
        now1 = datetime.datetime.now() + datetime.timedelta(365)

        self.calendar_departure_date = QtWidgets.QCalendarWidget(self.gridLayoutWidget)
        self.calendar_departure_date.setDateRange(now, now1)
        self.calendar_departure_date.setObjectName("calendar_departure_date")
        self.gridLayout_2.addWidget(self.calendar_departure_date, 3, 1, 1, 1)
        self.calendar_departure_date.selectionChanged.connect(self.f_update_calendar)

        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 2, 1, 1)
        self.calendar_arrival_date = QtWidgets.QCalendarWidget(self.gridLayoutWidget)
        self.calendar_arrival_date.setObjectName("calendar_arrival_date")
        self.calendar_arrival_date.setDateRange(now, now1)
        self.gridLayout_2.addWidget(self.calendar_arrival_date, 3, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 7, 0, 1, 1)
        self.line_arrival_time = QtWidgets.QTimeEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_arrival_time.setFont(font)
        self.line_arrival_time.setObjectName("line_arrival_time")
        self.gridLayout_2.addWidget(self.line_arrival_time, 5, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 5, 0, 1, 1)
        self.line_departure_time = QtWidgets.QTimeEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_departure_time.setFont(font)
        self.line_departure_time.setObjectName("line_departure_time")
        self.gridLayout_2.addWidget(self.line_departure_time, 5, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_15.setFont(font)
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 10, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_13.setFont(font)
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 6, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_14.setFont(font)
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 8, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 7, 2, 1, 1)
        self.line_departure_city = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_departure_city.setFont(font)
        self.line_departure_city.setObjectName("line_departure_city")
        self.gridLayout_2.addWidget(self.line_departure_city, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.line_arrival_city = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_arrival_city.setFont(font)
        self.line_arrival_city.setObjectName("line_arrival_city")
        self.gridLayout_2.addWidget(self.line_arrival_city, 1, 3, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_11.setFont(font)
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 2, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_16.setFont(font)
        self.label_16.setText("")
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 12, 0, 1, 1)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("but_add_trucking_2", "SimpleWay"))
        self.label.setText(_translate("but_add_trucking_2", "Город отправления:"))
        self.label_2.setText(_translate("but_add_trucking_2", "Город прибытия:"))
        self.label_3.setText(_translate("but_add_trucking_2", "Дата прибытия:"))
        self.label_4.setText(_translate("but_add_trucking_2", "Дата отправления:"))
        self.label_5.setText(_translate("but_add_trucking_2", "Время отправления:"))
        self.label_6.setText(_translate("but_add_trucking_2", "Время прибытия:"))
        self.label_8.setText(_translate("but_add_trucking_2", "ID машины:"))
        self.label_7.setText(_translate("but_add_trucking_2", "Введите данные:"))
        self.but_add_trucking.setText(_translate("but_add_trucking_2", "Добавить грузоперевозку"))
        self.label_9.setText(_translate("but_add_trucking_2", "Комментарии:"))
        self.label_10.setText(_translate("but_add_trucking_2", "Стоимость за м², руб:"))
        self.but_return.setText('Назад')

        self.doubleSpinBox.setRange(0.01, 100000.0)
        self.con = sqlite3.connect('transportation.db')
        self.but_add_trucking.clicked.connect(self.f_add_trucking)
        self.but_return.clicked.connect(self.f_return)
        self.cur = self.con.cursor()
        p = self.cur.execute(f"""SELECT truck_id FROM trucks""").fetchall()
        for i in p:
            self.box_truck_id.addItem(str(i[0]))

    def f_update_calendar(self):
        now = datetime.datetime.now() + datetime.timedelta(1000)
        self.calendar_arrival_date.setDateRange(self.calendar_departure_date.selectedDate(), now)

    def f_add_trucking(self):
        p = self.cur.execute(f"""SELECT load_capacity FROM trucks
                            WHERE truck_id = '{self.box_truck_id.currentText()}'""").fetchall()[0][0]

        c = (str(self.user_id),
             self.line_comments.text(),
             self.line_departure_city.text(),
             str(self.calendar_departure_date.selectedDate().day()) + '.' +
             str(self.calendar_departure_date.selectedDate().month()) + '.' +
             str(self.calendar_departure_date.selectedDate().year()),
             self.line_departure_time.text(),
             self.line_arrival_city.text(),
             str(self.calendar_arrival_date.selectedDate().day()) + '.' +
             str(self.calendar_arrival_date.selectedDate().month()) + '.' +
             str(self.calendar_arrival_date.selectedDate().year()),
             self.line_arrival_time.text(),
             self.box_truck_id.currentText(),
             str(self.doubleSpinBox.value()),
             p)

        if '' in c[2:] or 0 in c[2:] or\
                (c[3] == c[6] and self.line_departure_time.time() > self.line_arrival_time.time()):
            self.statusbar.showMessage("Неверно введены данные")
            self.statusbar.setStyleSheet("background-color:red;")
            return

        self.cur.execute(f"""INSERT INTO truckings(user_id, comments, departure_city, departure_date, departure_time,
                    arrival_city, arrival_date, arrival_time, truck_id, cost_per_quadratic_meter, quadratic_metres_left)
                    VALUES {c}""")
        self.con.commit()

        self.hide()
        self.form = Success(self.user_id, 'Trucking')
        self.form.show()

    def f_return(self):
        self.hide()
        self.form = AddDelTrucking(self.user_id)
        self.form.show()


class DelTrucking(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")

        font = QtGui.QFont()
        font.setPointSize(20)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 50, 1291, 651))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.but_return = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.verticalLayout.addWidget(self.but_return)

        self.but_delete = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_delete.setFont(font)
        self.but_delete.setObjectName("but_delete")
        self.verticalLayout.addWidget(self.but_delete)

        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("widget", "SimpleWay"))
        self.but_return.setText(_translate("widget", "Назад"))
        self.but_delete.setText(_translate("widget", "Удалить"))

        self.con = sqlite3.connect("transportation.db")
        self.but_delete.clicked.connect(self.delete_elem)
        self.but_return.clicked.connect(self.f_return)
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM truckings WHERE user_id=?",
                             (self.user_id,)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['id грузоперевозки', 'id пользователя', 'комментарии',
                                                    'город вывоза',
                                                    'дата вывоза', 'время вывоза', 'город ввоза', 'дата ввоза',
                                                    'время ввоза', 'id машины', 'стоимость за м²',
                                                    'осталось места'])
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) == 0:
            self.statusbar.setStyleSheet("background-color:red;")
            self.statusbar.showMessage("Выберите, что хотите удалить")
            return
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids) + '?',
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM truckings WHERE trucking_id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            cur.execute("DELETE FROM orders WHERE trucking_id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()
        self.update_result()

    def f_return(self):
        self.hide()
        self.form = AddDelTrucking(self.user_id)
        self.form.show()


class Success(QDialog):
    def __init__(self, user_id, way):
        super().__init__()
        self.user_id = user_id
        self.way = way
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(400, 238)
        self.setStyleSheet("background-color: rgb(154, 210, 186)")
        self.but_return = QtWidgets.QPushButton(self)
        self.but_return.setGeometry(QtCore.QRect(50, 140, 301, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.but_return.setFont(font)
        self.but_return.setObjectName("but_return")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(150, 60, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "SimpleWay"))
        self.but_return.setText(_translate("Dialog", "Готово"))
        self.label.setText(_translate("Dialog", "Успешно!"))

        self.but_return.clicked.connect(self.f_return)

    def f_return(self):
        self.hide()
        if self.way == 'Enter':
            self.form = Enter()
        elif self.way == 'Truck':
            self.form = DelTruck(self.user_id)
        elif self.way == 'Trucking':
            self.form = DelTrucking(self.user_id)
        elif self.way == 'Order':
            self.form = DelOrder(self.user_id)
        else:
            self.form = TruckerClient(self.user_id)
        self.form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWindow()
    ex.show()
    sys.exit(app.exec_())
