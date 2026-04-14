# Foodgram — сервис для работы с кулинарными рецептами

[![Django](https://img.shields.io/badge/Django-6.0-darkred)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-17-blue)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.10-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10-blue)](https://www.docker.com/)

**Foodgram** — это веб-приложение с REST API, предназначенное для публикации, хранения и поиска рецептов. Сервис позволяет пользователям делиться своими блюдами, подписываться на авторов, добавлять рецепты в избранное и формировать список покупок на основе выбранных рецептов.

---

## Возможности приложения

### Для всех пользователей
- Просмотр ленты рецептов на главной странице
- Открытие детальной информации о рецепте
- Просмотр профилей авторов
- Фильтрация рецептов по тегам
- Постраничный вывод (пагинация)

### Для зарегистрированных пользователей

#### Работа с рецептами
- Добавление новых рецептов
- Редактирование и удаление своих публикаций
- Добавление рецептов в список избранного
- Формирование списка покупок на основе рецептов

#### Подписки
- Подписка на других пользователей
- Просмотр списка подписок
- Возможность отписаться от автора

#### Список покупок
- Добавление и удаление рецептов из списка покупок
- Формирование и скачивание списка ингредиентов
- Автоматическое объединение одинаковых ингредиентов

#### Профиль пользователя
- Смена пароля
- Обновление или удаление аватара
- Выход из аккаунта

### Для администраторов
- Управление всеми сущностями через админ-панель Django
- Поиск пользователей по имени и email
- Поиск рецептов по названию и автору
- Фильтрация рецептов по тегам
- Просмотр статистики добавлений в избранное
- Управление списком ингредиентов

---

## Установка и запуск

### Установка локально
1. **Клонирование репозитория**  
   Клонируйте репозиторий и перейдите в директорию проекта:
   ```bash
   git clone https://github.com/sokems/foodgram.git
   ```

2. **Переменные окружения**  
   В корневой папке создайте файл `.env` с необходимыми переменными окружения (пример структуры см. в `.env.example`).

3. **Создание виртуального окружения**  
   Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

4. **Установка зависимостей**  
   Установите зависимости из файла `requirements.txt`:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Применение миграций**  
   Настройте базу данных:
   ```bash
   python manage.py migrate
   ```

6. Соберите статику:
    ```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
    ```

7. Импортируйте ингредиенты и теги:
    ```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_ingredients
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_tags
    ```

8. Создайте суперпользователя:
    ```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
    ```
    
9. **Локально запуск сервера**  
   Запустите локальный сервер:
   ```bash
   python manage.py runserver
   ```
   Проект будет доступен по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

### Работа с Docker

- Остановить:
    ```bash
    docker-compose -f docker-compose.production.yml down
    ```
- Перезапустить:
    ```bash
    docker-compose -f docker-compose.production.yml restart
    ```
- Логи:
    ```bash
    docker-compose -f docker-compose.production.yml logs -f
    ```
---

## Спецификация API

После запуска проекта документация API доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/).  

Основные эндпоинты:
- **Регистрация и аутентификация**: `/api/users/`, `/api/auth/token/login/`.
- **Рецепты**: `/api/recipes/`, `/api/recipes/{id}/favorite/`.
- **Подписки**: `/api/users/subscriptions/`, `/api/users/{id}/subscribe/`.
- **Список покупок**: `/api/recipes/download_shopping_cart/`.

---

## CI/CD

В проекте настроен автоматический деплой через GitHub Actions.
Конфигурация находится в .github/workflows/main.yml.

---

## Особенности

- **Аутентификация**: Используется токен (Djoser).
- **Роли пользователей**: Анонимные пользователи — просмотр рецептов. Аутентифицированные пользователи — создание рецептов, подписки, избранное. Администраторы — полный доступ к данным.
- **Изображения**: Поддержка загрузки аватаров и изображений для рецептов через Base64 или файловые поля.
- **Список покупок**: Генерация текстового файла для скачивания (с ингредиентами из выбранных рецептов).

---

## Технологический стек

- **Backend**: Python 3.12, Django, Django REST Framework
- **Frontend**: React
- **Контейнеризация**: Docker, Docker Compose
- **База данных**: PostgreSQL
- **Web Server**: Nginx
- **CI/CD**: GitHub Actions  

---

## Домен
https://watch-match.online/

---
## Автор
**[Роман Кремешный](https://github.com/sokems)**