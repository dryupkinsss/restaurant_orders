Проект "Ресторанная доставка"
Этот проект представляет собой приложение для управления ресторанными заказами и доставкой. 
Он разработан с использованием языка программирования Python и библиотек PyQt5, SQLAlchemy, openpyxl и других.

# Установка зависимостей
Для установки зависимостей проекта, выполните следующую команду в вашей виртуальной среде:

bash
Copy code
pip install -r requirements.txt

Запуск приложения
Запустите главный файл приложения main.py:

bash
Copy code
python main.py

Структура проекта
main.py: Главный файл приложения.
database.py: Модуль для работы с базой данных, включая описание схемы и класс для взаимодействия с ней.
README.md: Файл с описанием проекта и инструкциями по установке.
requirements.txt: Файл с перечнем зависимостей проекта.

Модули приложения
WelcomeWindow: Окно приветствия с возможностью регистрации и входа.
RegistrationWindow: Окно для регистрации новых пользователей.
LoginWindow: Окно для входа зарегистрированных пользователей.
AdminPanel: Панель администратора для управления заказами и экспорта данных в Excel.
OrderWindow: Окно для создания и оформления заказов.

База данных
Проект использует PostgreSQL для хранения данных. Доступ к базе данных организован с использованием библиотеки SQLAlchemy.

Экспорт данных в Excel
В админ-панели доступна функция экспорта данных о заказах в Excel. 
Для этого необходимо указать начальную и конечную дату периода, а затем нажать кнопку "Экспорт в Excel".

Автор
[Андрей Седнев 34ИС-21]