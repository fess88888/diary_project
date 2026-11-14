# 📖 Личный дневник (Django + PostgreSQL + Docker)

Веб-приложение для ведения личного дневника: регистрация, создание и редактирование
записей, поиск, адаптивный интерфейс на Bootstrap 5.

## Возможности

- Регистрация, вход и выход (встроенная аутентификация Django)
- CRUD записей дневника — каждый видит только свои записи
- Поиск по заголовку и тексту записей
- Пагинация списка
- Админ-панель Django (`/admin/`) с управлением записями и пользователями

## Стек

| Компонент        | Версия/решение          |
|------------------|-------------------------|
| Python           | 3.12                    |
| Django           | 5.x                     |
| БД               | PostgreSQL 16           |
| Стилизация       | Bootstrap 5 (CDN)       |
| Статические файлы| WhiteNoise              |
| Прод-сервер      | Gunicorn                |
| Контейнеризация  | Docker + docker compose |

## Структура проекта

- `config/` — настройки и корневые URL
- `accounts/` — регистрация и аутентификация, тесты (`tests.py`)
- `diary/` — модель записей, CRUD-вьюхи, поиск, миграции
- `templates/` — HTML-шаблоны на Bootstrap 5
- `static/` — стили и изображения (фон главной — `static/img/home.jpeg`)

## Быстрый старт (Docker)

1. Клонируйте репозиторий и скопируйте `.env.example` в `.env`,
   укажите `SECRET_KEY`:

   ```bash
   git clone https://github.com/fess88888/diary_project.git
   cd diary_project
   cp .env.example .env
   ```

2. Соберите и запустите контейнеры:

   ```bash
   docker compose up -d --build
   ```

3. Примените миграции и создайте суперпользователя:

   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```

4. Откройте в браузере: <http://localhost:8000>

## Статические файлы

Статика раздаётся через WhiteNoise: в Dockerfile уже включён
`python manage.py collectstatic --noinput`. Если добавляете файлы в
`static/` — пересоберите образ:

```bash
docker compose up -d --build
```

## Тесты
Покрытие кода — 95%

```bash
docker compose exec web python manage.py test
```

Тесты проверяют: регистрацию с автологином, что главная страница
показывает кнопку «Войти» анониму и что список записей доступен
только после входа.

## Переменные окружения

Секреты хранятся в `.env` (в репозиторий не попадает, см. `.gitignore`).
Список переменных и плейсхолдеры — в `.env.example`.
