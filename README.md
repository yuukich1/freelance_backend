# Freelance Platform Backend

Это backend для сервиса фрилансеров, написанный на Python с использованием FastAPI.

## Технологии

- **FastAPI** — быстрый и удобный веб-фреймворк для создания API
- **Celery** — для выполнения фоновых задач (отправка email, создание навыков)
- **Redis** — используется как брокер сообщений для Celery и для кэширования API
- **SQLAlchemy** — ORM для работы с базой данных
- **aiosqlite** — асинхронный драйвер для SQLite
- **Poetry** — для управления зависимостями и виртуальным окружением
- **Loguru** — для логирования приложения
- **JWT** — для аутентификации и авторизации пользователей
- **Alembic** — для миграций базы данных
- **SlowAPI** — для ограничения частоты запросов (rate limiting)
- **FastAPI Cache** — для кэширования ответов API

## База данных

В проекте используется **SQLite** для простоты и скорости разработки:

- Не нужно настраивать отдельный сервер базы данных
- Удобно для локальной разработки и тестирования
- Все данные хранятся в одном файле — удобно для прототипа

Однако проект поддерживает любую SQL базу данных, поддерживаемую SQLAlchemy (PostgreSQL, MySQL, MariaDB и др.). Для этого достаточно изменить `DATABASE_URL` в файле `.env`.

## Как устроен проект

Проект разделён на части, чтобы код был понятным и удобным для поддержки:

- **Роуты** (`src/routes/`) — принимают HTTP-запросы и отправляют ответы
- **Сервисы** (`src/service/`) — бизнес-логика приложения
- **Репозитории** (`src/repository/`) — операции с базой данных
- **Модели** (`src/models/`) — SQLAlchemy модели для работы с БД
- **Схемы** (`src/schemas/`) — Pydantic схемы для валидации данных
- **Unit of Work** (`src/utils/unit_of_work.py`) — паттерн, который помогает работать с базой данных в рамках одной транзакции, чтобы изменения были атомарными
- **Фоновые задачи** (`src/workers/`) — используются для долгих операций, например, отправки писем и создания навыков

## Паттерн Unit of Work

Используется для того, чтобы:

- Группировать несколько операций с базой в одной транзакции
- Централизованно управлять коммитом и откатом изменений
- Избежать проблем с целостностью данных при ошибках

## API Endpoints

### Аутентификация (`/api/auth`)

- `POST /api/auth/register` — регистрация нового пользователя (rate limit: 5/минуту)
- `GET /api/auth/activate` — активация пользователя по токену
- `POST /api/auth/login` — вход в систему (rate limit: 5/минуту)

### Категории (`/api/categories`)

- `POST /api/categories` — создание категории (только для админов, rate limit: 10/минуту)
- `GET /api/categories` — получение списка всех категорий (кэш: 1 час, rate limit: 100/минуту)
- `GET /api/categories/{category_id}` — получение категории по ID (rate limit: 100/минуту)
- `PUT /api/categories/{category_id}` — обновление категории (только для админов, rate limit: 10/минуту)
- `DELETE /api/categories/{category_id}` — удаление категории (только для админов, rate limit: 10/минуту)

### Услуги (`/api/services`)

- `POST /api/services` — создание услуги (требуется аутентификация)
- `GET /api/services` — получение списка всех услуг
- `GET /api/services/{service_id}` — получение услуги по ID
- `PUT /api/services/{service_id}` — обновление услуги (только владелец или админ)
- `DELETE /api/services/{service_id}` — удаление услуги (только владелец или админ)

### Исполнители (`/api/executers`)

- `POST /api/executers` — создание профиля исполнителя (требуется аутентификация)
- `GET /api/executers` — получение списка всех исполнителей

### Навыки (`/api/skills`)

- `GET /api/skills` — получение списка всех навыков

## Модели данных

### Users (Пользователи)
- `id` — уникальный идентификатор
- `username` — имя пользователя (уникальное)
- `email` — email (уникальный)
- `password` — хешированный пароль
- `is_active` — статус активации
- `role` — роль пользователя (user/admin)
- `created_at` — дата создания

### Categories (Категории)
- `id` — уникальный идентификатор
- `title` — название категории (уникальное)
- `description` — описание
- `created_at` — дата создания

### Services (Услуги)
- `id` — уникальный идентификатор
- `title` — название услуги
- `description` — описание услуги
- `price` — цена
- `category_id` — ID категории
- `buyer_id` — ID покупателя (создателя услуги)
- `delivery_time` — время выполнения
- `status` — статус услуги (Pending по умолчанию)
- `created_at` — дата создания

### Executers (Исполнители)
- `id` — уникальный идентификатор
- `user_id` — ID пользователя (уникальное)
- `skills` — словарь навыков (JSON)
- `created_at` — дата создания

### Skills (Навыки)
- `id` — уникальный идентификатор
- `title` — название навыка (уникальное)
- `created_at` — дата создания

## Логирование

Приложение использует **Loguru** для логирования. Логи записываются:

- В консоль (уровень INFO)
- В файл `logs/app.log` (уровень DEBUG, ротация при достижении 10 МБ)

Логирование покрывает:
- Все HTTP-запросы и ответы
- Операции с базой данных
- Бизнес-логику в сервисах
- Ошибки и исключения
- Старт и остановку приложения

## Установка и запуск

### Требования

- Python 3.14+
- Poetry
- Redis (для Celery и кэширования)

### Установка зависимостей

```bash
poetry install
```

### Настройка окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=sqlite+aiosqlite:///./database.db
SYNC_DATABASE_URL=sqlite:///./database.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACTIVATION_SECRET=your-activation-secret-here
ACTIVATION_URL=http://localhost:8000/api/auth/activate
REDIS_BROKER_URL=redis://localhost:6379/0
REDIS_BACKEND_URL=redis://localhost:6379/0
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASS=your-password
SMTP_USE_TLS=True
```

**Примечание:** Для использования других SQL баз данных измените `DATABASE_URL` и `SYNC_DATABASE_URL`. Например:
- PostgreSQL: `postgresql+asyncpg://user:password@localhost/dbname` и `postgresql://user:password@localhost/dbname`
- MySQL: `mysql+aiomysql://user:password@localhost/dbname` и `mysql://user:password@localhost/dbname`

### Миграции базы данных

```bash
# Создание новой миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head
```

### Запуск приложения

```bash
# Запуск FastAPI сервера
poetry run uvicorn src.main:app --reload

# Запуск Celery worker (в отдельном терминале)
poetry run celery -A src.workers.tasks worker --loglevel=info

# Запуск Flower для мониторинга Celery (опционально)
poetry run celery -A src.workers.tasks flower
```

Приложение будет доступно по адресу: `http://localhost:8000`

Документация API доступна по адресу: `http://localhost:8000/docs`

## Текущий статус

Проект находится в активной разработке. Реализованы:

✅ Аутентификация и авторизация пользователей  
✅ Управление категориями (CRUD)  
✅ Управление услугами (CRUD)  
✅ Профили исполнителей  
✅ Навыки  
✅ Фоновые задачи (Celery) для отправки email и создания навыков  
✅ Кэширование API ответов  
✅ Rate limiting  
✅ Логирование всех операций  
✅ Миграции базы данных  

В планах:
- Расширение функционала услуг
- Система отзывов и рейтингов
- Уведомления
- Поиск и фильтрация
