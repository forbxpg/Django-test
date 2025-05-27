# ShareVito

**ShareVito** — это веб-приложение для обмена вещами между пользователями. Платформа позволяет публиковать объявления и предлагать обмены, создавая экологичную и экономичную альтернативу покупке новых вещей.

## Функциональные возможности
- 👤 Регистрация и авторизация пользователей
- 📝 Создание и управление объявлениями
- 🔄 Формирование предложений обмена
- 📊 Отслеживание статуса обменов
- 💬 Фильтрация и поиск объявлений
- 📱 Адаптивный дизайн и красивый интерфейс
- 🔒 Безопасность данных и конфиденциальность пользователей

## Структура проекта
```
.
├── src
│   ├── api                    # API приложения
│   │   └── v1
│   │       ├── views          # Представления API
│   │       ├── serializers    # Сериализаторы для API
│   │       ├── urls.py        # URL маршруты API
│   │       └── __init__.py
│   ├── core                   # Модуль для базовых констант
│   │   ...
│   ├── ads                    # Приложение объявлений
│   │   ├── migrations         # Миграции базы данных
│   │   ├── models.py          # Модели объявлений
│   │   ├── views.py           # Представления объявлений
│   │   ├── urls.py            # URL маршруты объявлений
│   │   ├── forms.py           # Формы для работы с объявлениями
│   │   ...
│   ├── exchanges              # Приложение обменов
│   │   ├── migrations         # Миграции базы данных
│   │   ├── models.py          # Модели обменов
│   │   ├── views.py           # Представления обменов
│   │   ├── urls.py            # URL маршруты обменов
│   │   ├── forms.py           # Формы для работы с обменами
│   │   ...
│   │   share_platform.py      # Модуль настройки платформы обменов
│   │   ├── settings.py        # Настройки приложения 
│   │   ...     
│   ├── users                  # Приложение пользователей
│   │   ├── migrations         # Миграции базы данных
│   │   ├── models.py          # Модели пользователей
│   │   ├── views.py           # Представления пользователей
│   │   ├── urls.py            # URL маршруты пользователей
│   │   ├── forms.py           # Формы для работы с пользователями
│   │   ...
│   ├── templates              # Шаблоны HTML
│   │   ├── ads                # Шаблоны для объявлений
│   │   ├── exchanges          # Шаблоны для обменов
│   │   ├── users              # Шаблоны для пользователей
│   │   └── _base.html         # Базовый шаблон
│   ├── theme                  # Tailwind CSS и другие стили
│   │   └── static # Конфигурация Tailwind CSS
│   ├── manage.py              # Файл управления проектом Django
│   ├── requirements.txt       # Зависимости проекта
│   ├── .env.example           # Пример файла переменных окружения
│   ├── Dockerfile             # Файл сборки Docker-образа
│   ...
│       
├── server                     # Docker compose
│   └── docker-compose.yml     # Файл конфигурации Docker Compose
└──nginx                       # Конфигурация Nginx
    └── nginx.conf             # Файл конфигурации Nginx
```

## ⚙️ Установка и запуск

### I. С помощью Docker Compose 🐳


1. Клонируйте репозиторий:
```bash
git clone https://github.com/forbxpg/Django-test.git
```
2. Cоздайте файл `.env` на основе `.env.example` и настройте переменные окружения.
3. Перейдите в директорию `server`:
```bash
cd server
```
4. Запустите Docker Compose:
```bash
docker compose up --build
```
5. Выполните следующие команды для создания и применения миграций:
```bash
docker compose exec sharings_backend python manage.py migrate
docker compose exec sharings_backend python manage.py tailwind install
docker compose exec sharings_backend python manage.py tailwind build
docker compose exec sharings_backend python manage.py collectstatic --noinput
```
6. Создайте суперпользователя:
```bash
docker compose exec sharings_backend python manage.py createsuperuser
```
7. Откройте браузер и перейдите по адресу `http://127.0.0.1:8008` для доступа к приложению.


### II. Локальный запуск 🚀
1. Разверните виртуальное окружение и установите зависимости:
```bash
cd src
python -m venv .venv
source .venv/bin/activate  # Для Linux/Mac
source .venv/Scripts/activate  # Для Windows
pip install -r requirements.txt
```
2. Создайте файл `.env` на основе `.env.example` и настройте переменные окружения.
3. Примените миграции базы данных:
```bash
python manage.py migrate
```
4. Установите Tailwind CSS:
```bash
python manage.py tailwind install
python manage.py tailwind build
```
5. Соберите статические файлы:
```bash
python manage.py collectstatic --noinput
```
6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```
7. Запустите сервер разработки:
```bash
python manage.py runserver
```
8. Откройте браузер и перейдите по адресу `http://127.0.0.1:8000` для доступа к приложению.

#### Важно! Перед запуском убедитесь, что `DEBUG` в файле `.env` установлен в `True`, для того, чтобы при запуске приложение отображало `static` и `media` файлы. В противном случае, для доступа к статическим и медиафайлам, необходимо настроить сервер Nginx в файле `nginx.conf` и прописать конфиг в Docker Compose.


## 📃 API-документация






