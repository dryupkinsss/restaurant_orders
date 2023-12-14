Описание проекта "Ресторанная доставка"
---------------------


##### Содержание  
[Проект "Ресторанная доставка"](#project)
[Зависимости](#req)  
[Запуск приложения](#start)  
[Структура проекта](#struct)  
[Модули приложения](#module)  
[База данных](#db)  
[Экспорт данных в Excel](#excel)  
[Автор](#avtor) 

<a name="project"><h2>Проект "Ресторанная доставка"</h2></a>

Этот проект представляет собой приложение для управления ресторанными заказами и доставкой. 
Он разработан с использованием языка программирования Python и библиотек PyQt5, SQLAlchemy, openpyxl и других.

<a name="req"><h2>Зависимости</h2></a>

Для установки зависимостей проекта, выполните следующую команду в вашей виртуальной среде:
```no-highlight
pip install -r requirements.txt
```

<a name="start"><h2>Запуск приложения</h2></a>

Для запуска приложения нужно запустить главный файл приложения main.py:
```no-highlight
python main.py
```

<a name="struct"><h2>Структура проекта</h2></a>

* main.py: Главный файл приложения.
* database.py: Модуль для работы с базой данных, включая описание схемы и класс для взаимодействия с ней.
* README.md: Файл с описанием проекта и инструкциями по установке.
* requirements.txt: Файл с перечнем зависимостей проекта.

<a name="module"><h2>Модули приложения</h2></a>

* WelcomeWindow: Окно приветствия с возможностью регистрации и входа.
* RegistrationWindow: Окно для регистрации новых пользователей.
* LoginWindow: Окно для входа зарегистрированных пользователей.
* AdminPanel: Панель администратора для управления заказами и экспорта данных в Excel.
* OrderWindow: Окно для создания и оформления заказов.

<a name="db"><h2>База данных</h2></a>

Проект использует PostgreSQL для хранения данных.
Доступ к базе данных организован с использованием библиотеки SQLAlchemy.

<a name="excel"><h2>Экспорт данных в Excel</h2></a>

В админ-панели доступна функция экспорта данных о заказах в Excel. 
Для этого необходимо указать начальную и конечную дату периода, а затем нажать кнопку "Экспорт в Excel".

<a name="avtor"><h2>Автор</h2></a>
[Андрей Седнев 34ИС-21]
