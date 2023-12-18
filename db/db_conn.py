from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, MetaData, Table, Float, func, DateTime, \
    Boolean, update
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self):
        engine = create_engine('postgresql://postgres:59723833@localhost/restaurant')
        metadata = MetaData()

        self.users = Table('users', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('phone_number', String),
                           Column('username', String),
                           Column('password', String),
                           Column('is_admin', Boolean, default=False),
                           )

        self.categories = Table('categories', metadata,
                                Column('id', Integer, primary_key=True),
                                Column('name', String),
                                )

        self.dishes = Table('dishes', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String),
                            Column('category_id', Integer, ForeignKey('categories.id')),  # Внешний ключ на категории
                            Column('price', Float),
                            )

        self.orders = Table('orders', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('user_id', Integer, ForeignKey('users.id')),
                            Column('created_date', DateTime, default=func.now()),
                            Column('status', String, default='В обработке'),
                            )

        self.order_details = Table('order_details', metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('order_id', Integer, ForeignKey('orders.id')),
                                   Column('dish_id', Integer, ForeignKey('dishes.id')),
                                   Column('quantity', Integer),
                                   Column('total_price', Float),
                                   )

        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def populate_data(self):
        # Проверяем, сколько записей в таблице users
        user_count = self.session.query(func.count()).select_from(self.users).scalar()

        if user_count == 0:
            # Если таблица users пуста, вставляем данные
            self.session.execute(self.users.insert(), [
                {'phone_number': '12345678999', 'username': 'admin', 'password': 'admin', 'is_admin': True},
            ])

        # Проверяем, сколько записей в таблице categories
        category_count = self.session.query(func.count()).select_from(self.categories).scalar()

        if category_count == 0:
            # Если таблица categories пуста, вставляем данные
            self.session.execute(self.categories.insert(), [
                {'name': 'Пицца'},
                {'name': 'Суши'},
                {'name': 'Бургеры'},
                {'name': 'Десерты'},
            ])

        # Проверяем, сколько записей в таблице dishes
        dish_count = self.session.query(func.count()).select_from(self.dishes).scalar()

        if dish_count == 0:
            # Если таблица dishes пуста, вставляем данные
            self.session.execute(self.dishes.insert(), [
                {'name': 'Маргарита', 'category_id': 1, 'price': 650},
                {'name': 'Пепперони', 'category_id': 1, 'price': 800},
                {'name': 'Гавайская', 'category_id': 1, 'price': 600},
                {'name': 'Ролл с лососем', 'category_id': 2, 'price': 550},
                {'name': 'Филадельфия', 'category_id': 2, 'price': 600},
                {'name': 'Унаги', 'category_id': 2, 'price': 500},
                {'name': 'Чизбургер', 'category_id': 3, 'price': 250},
                {'name': 'Вегетарианский', 'category_id': 3, 'price': 200},
                {'name': 'Бекон бургер','category_id': 3, 'price': 350},
                {'name': 'Чизкейк', 'category_id': 4, 'price': 400},
                {'name': 'Тирамису', 'category_id': 4, 'price': 450},
                {'name': 'Шоколадный фондан', 'category_id': 4, 'price': 390}
            ])

        order_count = self.session.query(func.count()).select_from(self.orders).scalar()

        if order_count > 0:
            # Если таблица заказов не пуста, обновите статус для существующих заказов
            self.session.execute(update(self.orders).values({'status': 'В обработке'}))

        self.session.commit()

db = Database()
db.populate_data()