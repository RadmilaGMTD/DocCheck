# DocCheck
DocCheck - это сервис для обработки документов, который позволяет:

* Зарегистрированным пользователям загружать документы через API
* Администраторам проверять и подтверждать/отклонять документы
* Автоматически отправлять email-уведомления при изменениях статуса документов

# Технологический стек

* Backend: Django + Django REST Framework
* База данных: PostgreSQL
* Очереди задач: Celery + Redis
* Документация API: Swagger/OpenAPI
* Контейнеризация: Docker + Docker Compose


## Запуск проекта через Docker Compose

1. Клонируйте репозиторий:
```
git@github.com:RadmilaGMTD/DocCheck.git
```
2. Создайте файл .env в корне проекта на основе примера `.env.example`

3. Запустите проект командой:
```
docker-compose up --build
```
4. После запуска выполните миграции:
```
docker-compose exec web python manage.py migrate
```
5. После запуска веб-приложение будет доступно по адресу: http://localhost:8000

## Локальный запуск (для разработки)

1. Установите зависимости:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

2. Настройте базу данных:

* Установите PostgreSQL
* Создайте базу данных doc_check
* Настройте доступ в .env

3. Запустите Redis (для Celery):

```docker run -d -p 6379:6379 redis```

4. Примените миграции:

```python manage.py migrate```

5. Запустите сервер:

```python manage.py runserver```

6. В отдельном терминале запустите Celery:

```celery -A config worker -l INFO -P eventlet```

## Важные команды
bash
- Остановка всех контейнеров
```docker-compose down```

- Просмотр запущенных контейнеров
```docker-compose ps```

- Пересборка конкретного сервиса
```docker-compose up -d --build doccheck```

- Очистка системы Docker
```docker system prune -a --volumes```

## Проверка работоспособности сервисов

1. Django-приложение (web)
Откройте в браузере: http://localhost:8000/admin/

Войдите с данными суперпользователя

Убедитесь, что интерфейс администратора доступен

2. API endpoints
Получение списка курсов:
* Регистрация.(`users/create/`)
* Авторизация.(`users/token/`)


3. Celery worker
Проверьте логи Celery на выполнение задач:
```
docker-compose logs -f celery
```

4. PostgreSQL (db)
Подключитесь к БД для проверки:

```
docker-compose exec db psql -U your_db_user -d your_db_name
```

5. Redis
Проверьте подключение:

```
docker-compose exec redis redis-cli ping
```

Должен вернуться PONG

## Дополнительные команды:

Для просмотра запущенных контейнеров:

`docker-compose ps`

Для просмотра логов всех контейнеров:

`docker-compose logs`

Для остановки сервисов и удаления контейнеров:

`docker-compose down`

## Тестирование

* Запуск тестов:

```python manage.py test```

* Проверка покрытия:

```coverage run --source='.' manage.py test ```

```coverage report```

## Документация
Доступна по адресу: `/swagger/` и `/redoc/`
