from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class RegistrationWindow(QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        layout = QVBoxLayout()

        self.phone_label = QLabel('Номер телефона:', self)
        self.phone_input = QLineEdit(self)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        self.username_label = QLabel('Логин:', self)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Пароль:', self)
        self.password_input = QLineEdit(self)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton('Зарегистрироваться', self)
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_user(self):
        phone_number = self.phone_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if phone_number and username and password:
            user_data = {
                'phone_number': phone_number,
                'username': username,
                'password': password,
            }

            self.db.session.execute(self.db.users.insert().values(user_data))
            self.db.session.commit()

            QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно.')
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля.')