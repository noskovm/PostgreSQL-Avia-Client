import csv
import os
from PyQt5.QtGui import QIcon
from untitled import *
from main import *
import sys
import psycopg2
from psycopg2 import OperationalError
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


# QTableWidget, QTreeWidgetItem, QFileDialog
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('AviaClient')

        self.ui.pushButton.clicked.connect(self.sql_connect)

    def sql_connect(self):
        # принятие имени бд и всего прочего для подключения
        db_name = self.ui.lineEdit.text()
        db_user = self.ui.lineEdit_2.text()
        db_pass = self.ui.lineEdit_3.text()
        db_host = self.ui.lineEdit_4.text()
        db_port = self.ui.lineEdit_5.text()

        connection = create_connection(db_name, db_user, db_pass, db_host, db_port)

        if (connection):
            self.ui.new_window = MainWindow(connection, db_name)
            self.ui.new_window.show()
            self.close()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Предупреждение")
            msg.setText("Введены неправильные данные. Повторите попытку снова")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()


class MainWindow(QtWidgets.QWidget):
    def __init__(self, connection, db_name):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('AviaClient')

        # некоторые данные с других окон
        self.db_name = db_name
        self.connection = connection

        # отрисовка таблиц clients, flights, ledger
        self.print_all_tables()
        self.role = 'update'

        # иконка для запуска исполнения запроса
        self.ui.sql_go.setIcon(QIcon('check.png'))

        # СИГНАЛЫ для нажатия кнопок быстрого доступа SELECT, INSERT, CREATE, UPDATE
        self.ui.sql_go.clicked.connect(self.sql_query_go)
        self.ui.SELECTbut.clicked.connect(self.select_query_for_but)
        self.ui.INSERTbut.clicked.connect(self.insert_query_for_but)
        self.ui.CREATEbut.clicked.connect(self.create_query_for_but)
        self.ui.UPDATEbut.clicked.connect(self.update_query_for_but)

    # слоты для SELECT, INSERT, CREATE, UPDATE
    def select_query_for_but(self):
        self.ui.textEdit.setText("SELECT * FROM table_name;")

    def insert_query_for_but(self):
        self.ui.textEdit.setText(
            "INSERT INTO table_name (column1, column2, column3, ...)VALUES (value1, value2, value3, ...);")

    def create_query_for_but(self):
        self.ui.textEdit.setText(
            "CREATE TABLE table_name (column1 datatype,column2 datatype,column3 datatype,....);")

    def update_query_for_but(self):
        self.ui.textEdit.setText(
            "UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition;")

    def update_table(self):
        self.print_all_tables()

    # def change_role(self, tableWidget):
    #     self.update_table()
    #     self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
    #     self.role = 'insert'
    def change_role(self, tableWidget):
        self.update_table()
        tableWidget.insertRow(tableWidget.rowCount())
        self.role = 'insert'

    # отрисовка таблиц в Tabs
    def print_all_tables(self):
        # Таблица Clients
        clients_show_query = 'SELECT * FROM avia.clients ORDER BY client_number'
        clients = execute_read_query(self.connection, clients_show_query)
        self.ui.tableWidget.setRowCount(len(clients))
        self.ui.tableWidget.setColumnCount(len(clients[0]))

        # имена колонок
        self.columns_c = ['client_number', 'full_name', 'pass_number', 'sex', 'birthday']
        self.ui.tableWidget.setHorizontalHeaderLabels(self.columns_c)

        self.source_table_c = [[''] * len(clients[0]) for i in range(len(clients))]
        for row in range(len(clients)):
            for col in range(len(clients[0])):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(clients[row][col])))
                self.source_table_c[row][col] = self.ui.tableWidget.item(row, col).text()

        # для сохранения данных из таблицы clients
        self.ui.clients_save_button.clicked.connect(
            lambda: self.save_data_changes(self.ui.tableWidget, self.source_table_c, self.columns_c, 'avia.clients',
                                           'client_number',
                                           [1, 3, 4], 4, self.role))
        self.ui.save_data_clients.clicked.connect(
            lambda: self.handleSave(self.ui.tableWidget))

        self.ui.clients_update_button.clicked.connect(self.update_table)

        self.ui.add_row.clicked.connect(
            lambda: self.change_role(self.ui.tableWidget))

        # Таблица Flights
        flights_show_query = 'SELECT * FROM avia.flights ORDER BY flight_number'
        flights = execute_read_query(self.connection, flights_show_query)
        self.ui.tableWidget_2.setRowCount(len(flights))
        self.ui.tableWidget_2.setColumnCount(len(flights[0]))

        # имена колонок
        self.columns_f = ['flight_number', 'plane_type', 'flight_type', 'arrival_point', 'departure_date',
                          'departure_time']
        self.ui.tableWidget_2.setHorizontalHeaderLabels(self.columns_f)
        self.source_table_f = [[''] * len(flights[0]) for i in range(len(flights))]
        for row in range(len(flights)):
            for col in range(len(flights[0])):
                self.ui.tableWidget_2.setItem(row, col, QTableWidgetItem(str(flights[row][col])))
                self.source_table_f[row][col] = self.ui.tableWidget_2.item(row, col).text()

        # для сохранения данных из таблицы flights
        self.ui.flights_save_button.clicked.connect(
            lambda: self.save_data_changes(self.ui.tableWidget_2, self.source_table_f, self.columns_f, 'avia.flights',
                                           'flight_number',
                                           [1, 2, 3, 4, 5], 5, self.role))
        self.ui.save_data_flights.clicked.connect(
            lambda: self.handleSave(self.ui.tableWidget_2))

        self.ui.flights_update_button.clicked.connect(self.update_table)

        self.ui.add_row_flights.clicked.connect(
            lambda: self.change_role(self.ui.tableWidget_2))

        # Таблица Ledger
        ledger_show_query = 'SELECT * FROM avia.ledger ORDER BY id'
        ledger = execute_read_query(self.connection, ledger_show_query)
        self.ui.tableWidget_3.setRowCount(len(ledger))
        self.ui.tableWidget_3.setColumnCount(len(ledger[0]))

        # имена колонок
        self.columns_l = ['id', 'cost', 'delay_time', 'ticket_refund', 'flight_number', 'client_number', 'seat_code']
        self.ui.tableWidget_3.setHorizontalHeaderLabels(self.columns_l)
        self.source_table_l = [[''] * len(ledger[0]) for i in range(len(ledger))]
        for row in range(len(ledger)):
            for col in range(len(ledger[0])):
                item = QTableWidgetItem(str(ledger[row][col]))
                self.ui.tableWidget_3.setItem(row, col, item)
                self.source_table_l[row][col] = self.ui.tableWidget_3.item(row, col).text()

        # для сохранения данных из таблицы ledger
        self.ui.ledger_save_button.clicked.connect(
            lambda: self.save_data_changes(self.ui.tableWidget_3, self.source_table_l, self.columns_l, 'avia.ledger',
                                           'id',
                                           [2, 3], 6, self.role))

        self.ui.save_data_ledger.clicked.connect(
            lambda: self.handleSave(self.ui.tableWidget_3))

        self.ui.ledger_update_button.clicked.connect(self.update_table)

        self.ui.add_row_ledger.clicked.connect(
            lambda: self.change_role(self.ui.tableWidget_3))

    # сохранить таблицу в csv формате
    def handleSave(self, tableWidget):
        path, ok = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if ok:
            columns = range(tableWidget.columnCount())
            header = [tableWidget.horizontalHeaderItem(column).text()
                      for column in columns]
            with open(path, 'w') as csvfile:
                writer = csv.writer(
                    csvfile, dialect='excel', lineterminator='\n')
                writer.writerow(header)
                for row in range(tableWidget.rowCount()):
                    writer.writerow(
                        tableWidget.item(row, column).text()
                        for column in columns)

    # исполнить запрос
    def sql_query_go(self):
        self.ui.output.update()
        # todo если запрос неправильный то продумать предупреждение
        query = self.ui.textEdit.toPlainText()

        # формирование столбцов для любых таблиц
        columns = query.split()  # разделяется на слова запрос
        columns.pop(0)  # удаляется слово select
        columns_temp = list()  # тут будем хранить столбцы

        if columns[0] == '*':
            if 'avia.ledger' in columns or 'avia.ledger,' in columns or 'avia.ledger;' in columns:
                columns_temp += self.columns_l
            if 'avia.clients' in columns or 'avia.clients,' in columns or 'avia.clients;' in columns:
                columns_temp += self.columns_c
            if 'avia.flights' in columns or 'avia.flights,' in columns or 'avia.flights;' in columns:
                columns_temp += self.columns_f
        else:
            for i in columns:
                if i == 'FROM':
                    break
                columns_temp.append(i)

        # если запрос предполагает возврат данных
        if 'SELECT' in query or 'select' in query:
            result = execute_read_query(self.connection, query)
            self.ui.output.setRowCount(len(result))
            self.ui.output.setColumnCount(len(result[0]))
            self.ui.output.setHorizontalHeaderLabels(columns_temp)

            for row in range(len(result)):
                for col in range(len(result[0])):
                    self.ui.output.setItem(row, col, QTableWidgetItem(str(result[row][col])))

        # если запрос предполагает запросы create, insert и тд
        else:
            execute_query(self.connection, query)
            self.ui.output.setRowCount(1)
            self.ui.output.setColumnCount(1)

            for row in range(1):
                for col in range(1):
                    self.ui.output.setItem(row, col, QTableWidgetItem(str('Успешно')))

    # сохранить данные, если таблица была редактирована
    def save_data_changes(self, tableWidget, source_table, table_headers, table_name, where_atr, varchar_cols, end_col,
                          role):

        if role == 'update':
            # формируем данные редактированные таблицы
            res = [[''] * tableWidget.columnCount() for i in range(tableWidget.rowCount())]
            for row in range(tableWidget.rowCount()):
                for col in range(tableWidget.columnCount()):
                    res[row][col] = (tableWidget.item(row, col).text())

            # структуры для обновления таблицы по номеру строки
            change = list(list())
            for row in range(tableWidget.rowCount()):
                if res[row] != source_table[row]:
                    change.append([row, res[row]])
            print(change)
            # формируем запрос для обновления таблицы в бд
            for j, update in enumerate(change):

                update_query = "UPDATE %s SET " % (table_name)
                for i, header in enumerate(table_headers):
                    if i == end_col:
                        if i in varchar_cols:
                            update_query += (header + "=" + "'" + change[j][1][i] + "'")
                        else:
                            update_query += (header + "=" + change[j][1][i])
                    elif i in varchar_cols:
                        update_query += (header + "=" + "'" + change[j][1][i] + "'" + ", ")
                    else:
                        update_query += (header + "=" + change[j][1][i] + ", ")
                update_query += ' WHERE %s = ' % (where_atr) + tableWidget.item(change[j][0], 0).text()

                execute_query(self.connection, update_query)
        elif role == 'insert':
            insert_list = list()
            for i in range(self.ui.tableWidget.columnCount()):
                insert_list.append(self.ui.tableWidget.item(self.ui.tableWidget.rowCount() - 1, i).text())

            print(insert_list)
            query = "INSERT INTO {} (".format(table_name)
            for j, header in enumerate(table_headers):
                if j == end_col:
                    query += header + ' '
                else:
                    query += header + ', '
            query += ') VALUES ('
            for i in range(self.ui.tableWidget.columnCount()):
                if i == end_col:
                    if i in varchar_cols:
                        query += "'" + insert_list[i] + "'"
                    else:
                        query += insert_list[i] + " "
                elif i in varchar_cols:
                    query += "'" + insert_list[i] + "'" + ", "
                else:
                    query += insert_list[i] + ", "

            query += ')'

            execute_query(self.connection, query)
            self.update_table()
            self.role = 'update'


# -------------------------------------SQL FUNCTIONS------------------------------------------

# создает соединение с базой данных
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


# если запрос предполагает возвращение данных
def execute_read_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# если запрос предполагает запросы create, insert и тд(без вовзрата таблицы)
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except OperationalError as e:
        print(f"The error '{e}' occurred")


app = QtWidgets.QApplication([])
app.setStyle('Fusion')
application = MyWindow()
application.show()
sys.exit(app.exec())
