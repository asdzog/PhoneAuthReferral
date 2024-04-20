# Проект небольшого сервиса авторизации по номеру телефона с реферальной системой

---
### Общая логика работы.

---
Авторизация - по номеру телефона.Первый запрос - ввод номера телефона.
На адрес 
- <your_server_address>>/api/send-code/ 

производится POST-запрос вида

- {"phone_number": "+7ХХХХХХХХХХ"}

Далее - имитация отправки 4-значного кода авторизации (с задержкой
на сервере 1-2 сек). Второй запрос - на ввод кода авторизации.
Адрес:
- <your_server_address>>/api/verify-phone/

POST-запрос:
- {"phone_number": "+7ХХХХХХХХХХ",
    "confirmation_code": "ХХХХ"}

Если пользователь ранее не авторизовывался, то он записывается в базу данных.
Пользователю при первой авторизации присваивается случанйно сгенерированный
6-значный инвайт-код (цифры и символы).

В профиле у пользователя есть возможность ввести чужой инвайт-код
(при вводе проверяется на существование). В своем профиле можно 
активировать только 1 инвайт-код, если пользователь уже когда-то 
активировал инвайт код, то он выводится его в соответсвующем 
поле в запросе на профиль пользователя.
Адрес для отправки GET-запроса:
- <your_server_address>>/api/profile/

В API профиля выводится список пользователей (номеров телефона),
которые ввели инвайт-код текущего пользователя.