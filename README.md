### Описание:
Проект сервиса API для YamDb.
#### Позволяет:
  * создавать новых пользователей;
  * получать, создавать, изменять и удалять пользователей;
  * получать и изменять информацию о своей учетной записи;
  * получать, создавать и удалять категории;
  * получать, создавать и удалять жанры;
  * получать, создавать, изменять и удалять информацию о произведениях;
  * получать, создавать, изменять и удалять отзывы;
  * получать, создавать, изменять и удалять комментарии;
#### Используемые технологии:
  * requests==2.26.0
  * django==2.2.16
  * djangorestframework==3.12.4
  * djangorestframework-simplejwt
  * pytest==6.2.4
  * pytest-django==4.4.0
  * python-dotenv==0.13.0
  * pytest-pythonpath==0.7.3
  * django-filter
### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/DmitriiPugachev/api_yamdb.git
```
```bash
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv env
```
```bash
source env/bin/activate
```
```bash
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python3 manage.py migrate
```
Запустить проект:
```bash
python3 manage.py runserver
```
### Примеры запросов:
#### version 1.0
##### POST запрос на регистрацию пользователя:
```
/api/v1/auth/signup/
```
##### POST запрос на получение токена пользователем:
```
/api/v1/auth/token/
```
##### GET запрос на получение списка категорий:
```
/api/v1/categories/
```
##### POST запрос на добавление категории:
```
/api/v1/categories/
```
##### DELETE запрос на удаление категории:
```
/api/v1/categories/{slug}/
```
##### GET запрос на получение списка жанров:
```
/api/v1/genres/
```
##### POST запрос на добавление жанры:
```
/api/v1/genres/
```
##### DELETE запрос на удаление жанры:
```
/api/v1/genres/{slug}/
```
##### GET запрос на получение списка произведений:
```
/api/v1/titles/
```
##### POST запрос на добавление произведения:
```
/api/v1/titles/
```
##### GET запрос на получение конкретного произведения:
```
/api/v1/titles/{title_id}/
```
##### PATCH запрос на изменения произведения:
```
/api/v1/titles/{title_id}/
```
##### DELETE запрос на удаление произведения:
```
/api/v1/titles/{title_id}/
```
##### GET запрос на получение списка отзывов:
```
/api/v1/titles/{title_id}/reviews/
```
##### POST запрос на добавление отзыва:
```
/api/v1/titles/{title_id}/reviews/
```
##### GET запрос на получение конкретного отзыва:
```
/api/v1/titles/{title_id}/reviews/{review_id}/
```
##### PATCH запрос на изменения отзыва:
```
/api/v1/titles/{title_id}/reviews/{review_id}/
```
##### DELETE запрос на удаление отзыва:
```
/api/v1/titles/{title_id}/reviews/{review_id}/
```
##### GET запрос на получение списка комментариев:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
##### POST запрос на добавление комментария:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
##### GET запрос на получение конкретного комментария:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
##### PATCH запрос на изменения комментария:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
##### DELETE запрос на удаление комментария:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
##### GET запрос на получение списка пользователей:
```
/api/v1/users/
```
##### POST запрос на добавление пользователя:
```
/api/v1/users/
```
##### GET запрос на получение конкретного пользователя:
```
/api/v1/users/{username}/
```
##### PATCH запрос на изменения пользователя:
```
/api/v1/users/{username}/
```
##### DELETE запрос на удаление пользователя:
```
/api/v1/users/{username}/
```
##### GET запрос на получение данных своей учетной записи:
```
/api/v1/users/me/
```
##### PATCH запрос на изменение данных своей учетной записи:
```
/api/v1/users/me/
```
