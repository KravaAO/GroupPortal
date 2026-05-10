# Що було зроблено для підготовки до деплою

## Створені файли:

### 1. requirements.txt
Файл з усіма залежностями Python проєкту:
- Django 5.1.3
- python-decouple (для змінних середовища)
- Pillow (для роботи з зображеннями)
- gunicorn (WSGI сервер для продакшену)
- whitenoise (для статичних файлів)
- psycopg2-binary (для PostgreSQL)

### 2. .env
Файл зі змінними середовища для локальної розробки.
⚠️ Цей файл НЕ додається в Git (вже в .gitignore)

### 3. .env.example
Шаблон .env файлу для інших розробників.
Містить всі необхідні змінні з прикладами значень.

### 4. Procfile
Файл конфігурації для Heroku деплою.
Визначає команду запуску веб-сервера: `gunicorn gp.wsgi`

### 5. runtime.txt
Вказує версію Python для Heroku (Python 3.11.0)

### 6. check_deployment.py
Скрипт для перевірки готовності проєкту до деплою.
Перевіряє:
- Наявність .env файлу
- SECRET_KEY (чи не використовується небезпечний)
- DEBUG режим
- ALLOWED_HOSTS
- requirements.txt
- Статичні файли
- Налаштування бази даних

### 7. DEPLOYMENT_UA.md
Детальна інструкція українською мовою для:
- Локального запуску
- Підготовки до продакшену
- Деплою на Heroku
- Деплою на Railway
- Деплою на VPS (Ubuntu)
- Вирішення типових проблем

## Оновлені файли:

### 1. gp/settings.py
Додано підтримку змінних середовища:
- SECRET_KEY тепер читається з .env
- DEBUG читається з .env
- ALLOWED_HOSTS читається з .env
- Налаштування бази даних читаються з .env
- Додано WhiteNoise для статичних файлів
- Налаштовано STATIC_ROOT для collectstatic

### 2. .gitignore
Додано:
- /staticfiles/ (згенеровані статичні файли)
- /static_root/
- /media/ (завантажені файли користувачів)

### 3. README.md
Додано розділи:
- Детальна інструкція встановлення
- Налаштування змінних середовища
- Інструкції для різних платформ деплою
- Структура проєкту
- Корисні команди

## Наступні кроки:

### Для локальної розробки:
1. ✓ Встановити залежності: `pip install -r requirements.txt`
2. ✓ Файл .env вже створено
3. Запустити міграції: `python manage.py migrate`
4. Створити суперкористувача: `python manage.py createsuperuser`
5. Запустити сервер: `python manage.py runserver`

### Для деплою на продакшен:
1. Згенерувати новий SECRET_KEY:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. Оновити .env файл:
   - SECRET_KEY (новий згенерований)
   - DEBUG=False
   - ALLOWED_HOSTS=ваш-домен.com
   - Налаштувати PostgreSQL замість SQLite

3. Зібрати статичні файли:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. Запустити перевірку:
   ```bash
   python check_deployment.py
   ```

5. Задеплоїти на обрану платформу (див. DEPLOYMENT_UA.md)

## Готово до Git:

Можна комітити нові файли:
```bash
git add requirements.txt .env.example Procfile runtime.txt check_deployment.py DEPLOYMENT_UA.md
git add gp/settings.py .gitignore README.md
git commit -m "Підготовка проєкту до деплою: додано requirements.txt, .env, деплой інструкції"
git push
```

⚠️ ВАЖЛИВО: Файл .env НЕ додається в Git (він в .gitignore)!

## Підтримка

Якщо виникають питання:
1. Прочитайте DEPLOYMENT_UA.md
2. Запустіть `python check_deployment.py`
3. Перевірте логи Django
4. Перегляньте документацію Django

Успішного деплою! 🚀
