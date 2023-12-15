from datetime import timedelta

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QDateEdit
from sqlalchemy import func
from openpyxl import Workbook


class AdminPanel(QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        self.setWindowTitle('Панель администратора')
        self.setGeometry(200, 200, 800, 400)

        layout = QVBoxLayout()

        # Добавьте элементы интерфейса для выбора периода
        self.start_date_label = QLabel('Начальная дата:', self)
        self.start_date_edit = QDateEdit(self)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_edit)

        self.end_date_label = QLabel('Конечная дата:', self)
        self.end_date_edit = QDateEdit(self)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_edit)

        # Кнопка запроса выгрузки в Excel
        self.export_button = QPushButton('Экспорт в Excel', self)
        self.export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

    def export_to_excel(self):
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()

        print(f"Exporting orders from {start_date} to {end_date}")

        try:
            # Получите данные для выгрузки в Excel
            orders_data = self.db.session.query(
                self.db.orders.c.id,
                self.db.orders.c.user_id,
                self.db.users.c.phone_number,
                func.sum(self.db.order_details.c.total_price).label('total_price')
            ).join(
                self.db.order_details, self.db.orders.c.id == self.db.order_details.c.order_id
            ).join(
                self.db.users, self.db.orders.c.user_id == self.db.users.c.id  # Добавлен JOIN с таблицей users
            ).filter(
                self.db.orders.c.created_date.between(start_date, end_date + timedelta(days=1))
            ).group_by(
                self.db.orders.c.id, self.db.orders.c.user_id, self.db.users.c.phone_number
                # Включаем номер телефона в GROUP BY
            ).all()

            print("Orders data:", orders_data)

            # Создайте новую книгу Excel и получите активный лист
            workbook = Workbook()
            sheet = workbook.active

            # Заголовки столбцов
            sheet['A1'] = 'Номер заказа'
            sheet['B1'] = 'Идентифиактор пользователя'
            sheet['C1'] = 'Номер телефона'
            sheet['D1'] = 'Сумма заказа'

            # Сумма всех заказов
            total_orders_price = sum(order.total_price for order in orders_data)

            # Заполните данные из orders_data
            for row_index, order in enumerate(orders_data, start=2):
                sheet.cell(row=row_index, column=1, value=order.id)
                sheet.cell(row=row_index, column=2, value=order.user_id)
                sheet.cell(row=row_index, column=3, value=order.phone_number)
                sheet.cell(row=row_index, column=4, value=order.total_price)  # Используйте общую сумму заказа

            # Добавьте ячейку для отображения суммы всех заказов в столбце D1
            sheet.cell(row=1, column=4, value=f'Сумма всех заказов: {total_orders_price}')

            # Выравнивание текста в ячейках
            for column in sheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                sheet.column_dimensions[column[0].column_letter].width = adjusted_width

            # Сохраните книгу Excel
            workbook.save('orders_data.xlsx')

            QMessageBox.information(self, 'Успех', 'Выгрузка в Excel выполнена успешно.')
        except Exception as e:
            # Попробуем добавить вывод информации об ошибке для отладки
            print("An error occurred:", e)
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка: {str(e)}')
            import traceback
            traceback.print_exc()