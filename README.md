# ShareVito

**ShareVito** — это веб-приложение для обмена вещами между пользователями. Платформа позволяет публиковать объявления и
предлагать обмены, создавая экологичную и экономичную альтернативу покупке новых вещей.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white&style=for-the-badge&logoSize=20)
![Django](https://img.shields.io/badge/Django-4.2.20-darkgreen?logo=django&logoColor=white&style=for-the-badge&logoSize=20)
![Django REST Framework](https://img.shields.io/badge/DRF-3.15.2-darkorange?logo=django&logoColor=white&style=for-the-badge&logoSize=20)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue?logo=postgresql&logoColor=white&style=for-the-badge&logoSize=20)
![Docker](https://img.shields.io/badge/docker-darkblue?logo=docker&logoColor=white&style=for-the-badge&logoSize=20)
![Nginx](https://img.shields.io/badge/nginx-darkgreen?logo=nginx&logoColor=white&style=for-the-badge&logoSize=20)
![Gunicorn](https://img.shields.io/badge/gunicorn-green?logo=gunicorn&logoColor=white&style=for-the-badge&logoSize=20)
![Django Unfold](https://img.shields.io/badge/UNFOLD-darkblue?&logoColor=white&style=for-the-badge&logoSize=20)
![Djoser](https://img.shields.io/badge/djoser-darkblue?logoColor=white&style=for-the-badge&logoSize=20)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-purple?logo=tailwindcss&logoColor=white&style=for-the-badge&logoSize=20)

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

#### Важно! Перед установкой надо обязательно поставить ⭐️, иначе ничего не запустится)

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

#### Важно! 
Перед запуском убедитесь, что `DEBUG` в файле `.env` установлен в
`True`, для того, чтобы при запуске приложение отображало `static` и
`media` файлы. В противном случае, для доступа к статическим и медиафайлам, необходимо настроить сервер Nginx в файле
`nginx.conf` и прописать конфиг в Docker Compose.

Проект можно запускать как с использованием PostgreSQL, так и с использованием SQLite, для этого используется переменная окружения `USE_POSTGRESQL`


## 📃 API-документация

Документация к API доступна по адресу:

```
http://127.0.0.1/api/docs/
```

Данная документация автоматически генерируется с помощью библиотеки `drf-yasg` и предоставляет подробную информацию о
доступных эндпоинтах, методах и параметрах запросов.

#### Важно! Данная документация является примером и не содержит полной информации о проекте. Разработка проекта еще не закончена.

### Базовые эндпоинты API:

#### Пользователи

Для работы с пользователями используется библиотека `djoser`, которая предоставляет готовые эндпоинты для
регистрации, авторизации и управления пользователями.

```
POST /api/v1/users/              # Регистрация нового пользователя (Any)
POST /api/v1/auth/jwt/create/    # Получение JWT-токена (Any). В теле запроса передаются username и password.
GET /api/v1/users/me/            # Получение информации о текущем пользователе (Authenticated)
PUT /api/v1/users/me/            # Обновление информации о текущем пользователе (Authenticated)
```

#### Объявления

```
GET /api/v1/ads/                 # Получение списка объявлений (Any)
POST /api/v1/ads/                # Создание нового объявления (Authenticated)
GET /api/v1/ads/{id}/            # Получение информации об объявлении по ID (Any)
PUT /api/v1/ads/{id}/            # Обновление объявления по ID (Authenticated, Owner)
DELETE /api/v1/ads/{id}/         # Удаление объявления по ID (Authenticated, Owner)
POST /api/v1/ads/{id}/propose/   # Предложение обмена для объявления (Authenticated, Owner)
```

#### Обмены

```
GET /api/v1/exchanges/           # Получение списка обменов (Authenticated)
POST /api/v1/exchanges/          # Создание нового обмена (Authenticated)
GET /api/v1/exchanges/{id}/      # Получение информации об обмене по ID (Authenticated)
PUT /api/v1/exchanges/{id}/      # Обновление обмена по ID (Authenticated, Owner)
DELETE /api/v1/exchanges/{id}/   # Удаление обмена по ID (Authenticated, Owner)
POST /api/v1/exchanges/{id}/accept/  # Принятие предложенного обмена (Authenticated, Owner)
POST /api/v1/exchanges/{id}/reject/  # Отклонение предложенного обмена (Authenticated, Owner)
```

#### Категории

```
GET /api/v1/categories/          # Получение списка категорий (Any)
GET /api/v1/categories/{id}/      # Получение информации о категории по ID (Any)
```

#### Важно!

Категории для объявлений может создавать только администратор. Для этого необходимо зайти в панель администратора по
адресу `http://127.0.0.1:8000/admin/` (8008 для Docker Compose) и создать категории в разделе "Категории объявлений".

## 📦 Технологии

Проект использует следующие ключевые зависимости:

- **Django** — основной фреймворк для разработки веб-приложения.
- **Django REST Framework** — для создания API.
- **Djoser** — для управления пользователями и аутентификацией.
- **drf-yasg** — для автоматической генерации документации API.
- **Tailwind CSS** — для стилизации интерфейса.
- **django-tailwind** — для интеграции Tailwind CSS в проект.
- **Django Unfold** — для создания интерфейса администратора.
- **Flowbite** — для компонентов пользовательского интерфейса.
- **PostgreSQL** — в качестве базы данных.
- **Docker** и **Docker Compose** — для контейнеризации и управления сервисами.

## 📫 Контакты

Если у вас есть вопросы или предложения по проекту, вы можете связаться со мной по электронной
почте [dwizard80@gmail.com](mailto:dwizard80@gmail.com) или [Telegram](https://t.me/forbxpg).








