from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, MetaData, Table, Float, func, DateTime, Boolean
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
