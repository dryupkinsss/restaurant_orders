from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from sqlalchemy import select
from panel.admin_panel import AdminPanel
from windows.order_window import OrderWindow


class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        layout = QVBoxLayout()

        self.username_label = QLabel('Логин:', self)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Пароль:', self)
        self.password_input = QLineEdit(self)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Войти', self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            user = self.db.session.execute(select(self.db.users).where(self.db.users.c.username == username)).fetchone()

            if user and user.password == password:
                if user.is_admin:
                    # Открываем окно админ-панели
                    self.close()
                    self.show_admin_panel()
                else:
                    self.current_user_id = user.id
                    self.close()
                    self.show_order_window()
                    print("Username:", username)
                    print("Password:", password)
                    print("User:", user)
            else:
                QMessageBox.warning(self, 'Ошибка', f'Неверные логин или пароль.')

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка: {str(e)}')
            print("An error occurred:", e)
            import traceback
            traceback.print_exc()

    def show_admin_panel(self):
        self.admin_panel = AdminPanel(self.db)
        self.admin_panel.show()

    def show_order_window(self):
        self.order_window = OrderWindow(self.db, self.current_user_id)
        self.order_window.show()