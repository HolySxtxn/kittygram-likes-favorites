# Kittygram: Лайки и избранное

Расширение серверной части Kittygram для поддержки социальных механик — лайков, избранного и заметок.

## Основной функционал

- Регистрация и аутентификация пользователей (токены)
- Просмотр списка котиков с флагами `is_liked` и `is_favorited`
- Постановка и снятие лайка
- Добавление и удаление котиков из избранного
- Просмотр количества лайков у кота
- Просмотр личных списков избранного и лайкнутых котов
- Создание и редактирование заметок к избранным котам
- Удаление записей из избранного
- Полная CRUD-документация через Swagger/ReDoc

## Используемые технологии

- Python 3.12, Django 5.1, Django REST Framework, djoser
- SQLite (по умолчанию, для разработки)
- Docker, Docker Compose
- Swagger (drf-yasg)

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/HolySxtxn/kittygram-likes-favorites.git
cd kittygram-likes-favorites
```

2. Создайте и активируйте виртуальное окружение:
```bash
cd kittygram_backend
python -m venv venv
source venv/bin/activate
```

Для Windows:
```bash
venv\Scripts\activate
```

Установите зависимости:
```bash
pip install -r requirements.txt
```
Выполните миграции и запустите сервер:

```bash
python manage.py migrate
python manage.py runserver
```
Для запуска фронтенда (в отдельном терминале):
```bash
cd ../kittygram_frontend
npm install
npm start
```
Запуск через Docker
Скопируйте .env.example в .env и отредактируйте при необходимости.

Запустите контейнеры:
```bash
docker-compose -f docker-compose.production.yml up -d --build
```
Примените миграции и соберите статику:
```bash
docker-compose -f docker-compose.production.yml exec backend python manage.py migrate
docker-compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
```
Проект будет доступен по адресу http://localhost.

Документация API
Swagger UI: http://localhost/swagger/

Примеры запросов

Получение токена:
POST /api/token/login/
{"username": "user", "password": "pass"}

Постановка лайка:
POST /api/cats/1/like/
Authorization: Token <токен>

Добавление в избранное:
POST /api/cats/1/favorite/
Authorization: Token <токен>

Список избранного с заметками:
GET /api/favorites-detail/
Authorization: Token <токен>

Редактирование заметки:

PATCH /api/favorites-detail/4/
{"note": "Очень пушистый!"}
Authorization: Token <токен>
Количество лайков у кота (доступно без авторизации):

GET /api/cats/1/likes-count/
Переменные окружения
Пример конфигурации — в файле .env.example.