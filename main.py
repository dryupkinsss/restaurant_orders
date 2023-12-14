from datetime import timedelta

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QListWidget, QDateEdit
from PyQt5.QtCore import Qt
from sqlalchemy import select, func
from openpyxl import Workbook
from db.db_conn import Database
from panel.admin_panel import AdminPanel
from windows.login_window import LoginWindow
from windows.registration_window import RegistrationWindow


class WelcomeWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.db = db

        self.setWindowTitle('Ресторанная доставка')
        self.setGeometry(200, 200, 800, 400)

        layout = QVBoxLayout()

        self.label = QLabel('Добро пожаловать! Вы зарегистрированы?', self)
        layout.addWidget(self.label)

        self.register_button = QPushButton('Регистрация', self)
        self.register_button.clicked.connect(self.show_registration_window)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton('Вход', self)
        self.login_button.clicked.connect(self.show_login_window)
        layout.addWidget(self.login_button)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_registration_window(self):
        self.registration_window = RegistrationWindow(self.db)
        self.registration_window.show()

    def show_login_window(self):
        self.login_window = LoginWindow(self.db)
        self.login_window.show()




if __name__ == '__main__':
    app = QApplication([])
    db = Database()
    welcome_window = WelcomeWindow(db)
    welcome_window.show()
    app.exec_()
