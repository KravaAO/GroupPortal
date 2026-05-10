# Інструкція з розгортання GroupPortal

## Швидкий старт для розробки

1. **Встановіть залежності**
   ```bash
   pip install -r requirements.txt
   ```

2. **Налаштуйте змінні середовища**
   ```bash
   copy .env.example .env
   ```
   
   Відредагуйте файл `.env` за потребою

3. **Запустіть міграції**
   ```bash
   python manage.py migrate
   ```

4. **Створіть адміністратора**
   ```bash
   python manage.py createsuperuser
   ```

5. **Запустіть сервер**
   ```bash
   python manage.py runserver
   ```

Відкрийте http://localhost:8000

## Підготовка до продакшену

### 1. Генерація SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Скопіюйте результат в `.env` файл як `SECRET_KEY`

### 2. Налаштування .env для продакшену

```env
SECRET_KEY=ваш-згенерований-ключ
DEBUG=False
ALLOWED_HOSTS=ваш-домен.com,www.ваш-домен.com

# PostgreSQL (рекомендовано)
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=groupportal_db
DATABASE_USER=groupportal_user
DATABASE_PASSWORD=надійний-пароль
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 3. Збірка статичних файлів

```bash
python manage.py collectstatic --noinput
```

### 4. Перевірка готовності

```bash
python check_deployment.py
```

Цей скрипт перевірить чи все налаштовано правильно.

## Розгортання на Heroku

### Крок 1: Підготовка

```bash
# Встановіть Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Увійдіть в акаунт
heroku login
```

### Крок 2: Створення додатку

```bash
# Створіть додаток
heroku create назва-вашого-додатку

# Додайте PostgreSQL
heroku addons:create heroku-postgresql:mini
```

### Крок 3: Налаштування змінних

```bash
# Згенеруйте та встановіть SECRET_KEY
heroku config:set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# Налаштуйте інші змінні
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=назва-вашого-додатку.herokuapp.com
```

### Крок 4: Деплой

```bash
# Відправте код на Heroku
git push heroku main

# Запустіть міграції
heroku run python manage.py migrate

# Створіть суперкористувача
heroku run python manage.py createsuperuser

# Зберіть статичні файли
heroku run python manage.py collectstatic --noinput
```

### Крок 5: Відкрийте додаток

```bash
heroku open
```

## Розгортання на Railway

1. Зайдіть на https://railway.app
2. Під'єднайте ваш GitHub репозиторій
3. Додайте PostgreSQL в розділі "New"
4. Налаштуйте змінні середовища:
   - `SECRET_KEY` - згенеруйте новий ключ
   - `DEBUG` - встановіть `False`
   - `ALLOWED_HOSTS` - ваш домен на Railway
   - `DATABASE_ENGINE` - `django.db.backends.postgresql`
   - Railway автоматично встановить змінні DATABASE_URL
5. В Settings встановіть:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn gp.wsgi`
6. Deploy!

## Розгортання на VPS (Ubuntu)

### 1. Підключіться до сервера

```bash
ssh root@ваш-сервер-ip
```

### 2. Встановіть необхідне ПЗ

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

### 3. Налаштуйте PostgreSQL

```bash
sudo -u postgres psql
```

В psql виконайте:
```sql
CREATE DATABASE groupportal_db;
CREATE USER groupportal_user WITH PASSWORD 'надійний_пароль';
ALTER ROLE groupportal_user SET client_encoding TO 'utf8';
ALTER ROLE groupportal_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE groupportal_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE groupportal_db TO groupportal_user;
\q
```

### 4. Клонуйте проєкт

```bash
cd /var/www
sudo git clone https://github.com/ваш-username/GroupPortal.git groupportal
cd groupportal
```

### 5. Налаштуйте віртуальне середовище

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Налаштуйте .env

```bash
nano .env
```

Вставте:
```env
SECRET_KEY=згенеруйте-новий-ключ
DEBUG=False
ALLOWED_HOSTS=ваш-домен.com,www.ваш-домен.com

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=groupportal_db
DATABASE_USER=groupportal_user
DATABASE_PASSWORD=надійний_пароль
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 7. Запустіть міграції

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 8. Налаштуйте Gunicorn

```bash
sudo nano /etc/systemd/system/groupportal.service
```

Вставте:
```ini
[Unit]
Description=GroupPortal Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/groupportal
Environment="PATH=/var/www/groupportal/venv/bin"
ExecStart=/var/www/groupportal/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 gp.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start groupportal
sudo systemctl enable groupportal
```

### 9. Налаштуйте Nginx

```bash
sudo nano /etc/nginx/sites-available/groupportal
```

Вставте:
```nginx
server {
    listen 80;
    server_name ваш-домен.com www.ваш-домен.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/groupportal/staticfiles/;
    }

    location /media/ {
        alias /var/www/groupportal/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/groupportal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. Налаштуйте SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d ваш-домен.com -d www.ваш-домен.com
```

Готово! Ваш сайт доступний на https://ваш-домен.com

## Корисні команди

### Оновлення коду на сервері

```bash
cd /var/www/groupportal
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart groupportal
```

### Перегляд логів

```bash
# Gunicorn логи
sudo journalctl -u groupportal -f

# Nginx логи
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Резервне копіювання БД

```bash
# Створення бекапу
pg_dump -U groupportal_user groupportal_db > backup_$(date +%Y%m%d).sql

# Відновлення з бекапу
psql -U groupportal_user groupportal_db < backup_20240510.sql
```

## Вирішення проблем

### Помилка 500
- Перевірте логи: `sudo journalctl -u groupportal -n 50`
- Переконайтесь що DEBUG=False та ALLOWED_HOSTS налаштовано
- Перевірте права доступу до media/ та staticfiles/

### Статичні файли не завантажуються
- Запустіть: `python manage.py collectstatic --noinput`
- Перевірте права доступу: `sudo chown -R www-data:www-data staticfiles/`
- Перезапустіть Nginx: `sudo systemctl restart nginx`

### База даних не підключається
- Перевірте налаштування в .env
- Переконайтесь що PostgreSQL запущено: `sudo systemctl status postgresql`
- Перевірте доступ: `psql -U groupportal_user -d groupportal_db -h localhost`

## Підтримка

Якщо виникли питання або проблеми:
1. Перевірте логи сервера
2. Запустіть `python check_deployment.py`
3. Перегляньте документацію Django
4. Створіть issue в GitHub репозиторії
