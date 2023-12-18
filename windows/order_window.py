from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QComboBox, QListWidget
from sqlalchemy import select, func


class OrderWindow(QMainWindow):
    def __init__(self, db, current_user_id):
        super().__init__()

        self.db = db
        self.current_user_id = current_user_id

        self.setWindowTitle('Ресторанная доставка')
        self.setGeometry(200, 200, 800, 400)

        layout = QVBoxLayout()

        self.category_label = QLabel('Выберите категорию:', self)
        self.category_combo = QComboBox(self)
        categories = self.db.session.execute(select(self.db.categories)).fetchall()
        for category in categories:
            self.category_combo.addItem(category.name)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_combo)

        self.dish_label = QLabel('Выберите блюдо:', self)
        self.dish_combo = QComboBox(self)
        layout.addWidget(self.dish_label)
        layout.addWidget(self.dish_combo)

        self.quantity_label = QLabel('Количество:', self)
        self.quantity_input = QLineEdit(self)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)

        self.add_to_cart_button = QPushButton('Добавить в корзину', self)
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        layout.addWidget(self.add_to_cart_button)

        # Добавим атрибут selected_items
        self.selected_items = []

        # Добавим QListWidget для отображения выбранных товаров
        self.cart_list = QListWidget(self)
        layout.addWidget(self.cart_list)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.view_cart_button = QPushButton('Просмотреть корзину', self)
        self.view_cart_button.clicked.connect(self.view_cart)
        layout.addWidget(self.view_cart_button)

        self.category_combo.currentIndexChanged.connect(self.update_dishes)

        self.update_dishes()

        self.checkout_button = QPushButton('Оформить заказ', self)
        self.checkout_button.clicked.connect(self.checkout)
        layout.addWidget(self.checkout_button)

    def update_dishes(self):
        self.dish_combo.clear()

        category_name = self.category_combo.currentText()

        category_id = self.db.session.execute(
            select(self.db.categories.c.id).where(self.db.categories.c.name == category_name)).scalar()

        dishes = self.db.session.execute(
            select(self.db.dishes).where(self.db.dishes.c.category_id == category_id)).fetchall()

        for dish in dishes:
            self.dish_combo.addItem(f"{dish.name} - {dish.price:.2f} руб.", userData=dish.id)

    def add_to_cart(self):
        category_name = self.category_combo.currentText()
        dish_id = self.dish_combo.currentData()
        quantity_text = self.quantity_input.text()


        try:
            quantity = int(quantity_text)
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным числом")
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Укажите корректное количество блюд.')
            return

        dish = self.db.session.execute(
            select(self.db.dishes).where(self.db.dishes.c.id == dish_id)).fetchone()

        if dish:
            price = dish.price

            total_price = quantity * price

            item_text = f"{quantity} x {dish.name} ({category_name}) - {total_price:.2f} руб."
            self.selected_items.append(item_text)
            self.cart_list.addItem(item_text)

            QMessageBox.information(self, 'Успех', 'Блюдо добавлено в корзину.')
        else:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось найти информацию о блюде: {dish_id}')

    def view_cart(self):
        cart_contents = '\n'.join(self.selected_items)
        if cart_contents:
            QMessageBox.information(self, 'Корзина', f'Ваш заказ:\n{cart_contents}')
        else:
            QMessageBox.warning(self, 'Корзина', 'Добавьте блюда в корзину.')

    def checkout(self):
        try:
            # Создаем новый заказ
            order_data = {
                'user_id': self.current_user_id,
                'created_date': func.now(),
            }
            result = self.db.session.execute(self.db.orders.insert().values(order_data))
            order_id = result.inserted_primary_key[0]

            # Добавляем детали заказа (блюда)
            for item_text in self.selected_items:
                # Разбираем информацию о блюде из текста
                parts = item_text.split(' ')
                quantity = int(parts[0])
                dish_name = parts[2]
                category_name = parts[3][1:-1]  # Убираем скобки
                total_price = float(parts[-2])

                # Получаем id блюда из базы данных
                dish_id = self.db.session.query(self.db.dishes.c.id).join(
                    self.db.categories, self.db.dishes.c.category_id == self.db.categories.c.id
                ).filter(
                    self.db.dishes.c.name == dish_name,
                    self.db.categories.c.name == category_name
                ).scalar()

                if dish_id:
                    # Добавляем информацию о блюде в таблицу order_details
                    order_detail_data = {
                        'order_id': order_id,
                        'dish_id': dish_id,
                        'quantity': quantity,
                        'total_price': total_price,
                    }
                    self.db.session.execute(self.db.order_details.insert().values(order_detail_data))

            # Получаем номер заказа
            order_id = result.inserted_primary_key[0]

            self.selected_items = []
            self.cart_list.clear()

            # Фиксируем изменения в базе данных
            self.db.session.commit()
            QMessageBox.information(self, 'Успех', f'Заказ №{order_id} успешно оформлен!')

        except Exception as e:
            # Откатываем транзакцию в случае ошибки
            self.db.session.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка при оформлении заказа: {str(e)}')
            print("An error occurred:", e)
            import traceback
            traceback.print_exc()