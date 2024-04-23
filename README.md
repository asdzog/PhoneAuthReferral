# Проект сервиса авторизации по номеру телефона с реферальной системой

---
### Общая логика работы.

---
Авторизация - по номеру телефона.Первый запрос - ввод номера телефона.
На адрес 
- <your_server_address>/api/send-code/ 

производится POST-запрос вида

```json
{
  "phone_number": "+7ХХХХХХХХХХ"
}
```

Далее - имитация отправки 4-значного кода авторизации (с задержкой
на сервере 1-2 сек). Второй запрос - на ввод кода авторизации.

Адрес:
- <your_server_address>/api/verify-phone/

POST-запрос:
```json
{
  "phone_number": "+7ХХХХХХХХХХ",
  "confirmation_code": "ХХХХ"
}
```

Если пользователь ранее не авторизовывался, то он записывается в базу данных.
Пользователю при первой авторизации присваивается случайно сгенерированный
6-значный инвайт-код (цифры и символы).

В профиле у пользователя есть возможность ввести чужой инвайт-код
(при вводе проверяется на существование).

В своем профиле можно 
активировать только 1 инвайт-код, если пользователь уже когда-то 
активировал инвайт код, то он выводится в соответствующем 
поле в запросе на профиль пользователя.

Адрес для отправки запроса на активацию инвайт-кода:

- <your_server_address>/api/update-referrer/

PUT-запрос:

```json
{
  "referrer": "ХХХХХХ"
}
```

В API профиля выводится список пользователей (номеров телефона),
которые ввели инвайт-код текущего пользователя.

Адрес для отправки GET-запроса:

- <your_server_address>/api/profile/


---
### Запуск проекта

---

Склонируйте репозиторий, создайте в проекте виртуальное окружение
и установите зависимости из файла _requirements.txt_.  
Команда для установки зависимостей:

```pip install -r requirements.txt```

Выполните индивидуальные настройки проекта 
в файле _.env_ по прилагаемому шаблону  _.env_sample_

Примените миграции с помощью команды:

```python manage.py migrate```

Для запуска сервера запустите команду:

```python manage.py runserver```

---
### Запуск проекта в Docker

---
Чтобы запустить проект с предварительным развертыванием
контейнера в Docker, запустите команду:

```docker-compose up --build```
