# Документация REST API


# Сервис регистрации


## Базовый ендпоинт: '/authorization/'


## Registration:
Ресурс для регистрации пользователя.


> POST '/authorization/registration'


Принимает: phone_number, email, hash_password.


| Name | Type |
|:-------------:|:-------:|
| phone_number | str |
| email | str |
| hash_password | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Login/Email:
Ресурс для авторизации пользователя в системе с помощью почты и пароля.


> POST '/authorization/login/email'


Принимает: email, hash_password.


| Name | Type |
|:------------:|:---------:|
| email | str |
| hash_password | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Login/Phone_number:
Ресурс для авторизации пользователя в системе с помощью номера телефона и пароля.


> POST '/authorization/login/phone/number'


Принимает: phone_number, hash_password.


| Name | Type |
|:------------:|:---------:|
| phone_number | str |
| hash_password | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Базовый ендпоинт: '/vk/'


## Link:
Ресурс для получения ссылки авторизации vk.


> GET '/vk/link'

Ничего не принимает.


Пример ответа:
'https://id.vk.com/authorize?response_type=code&client_id=52896748&scope=email&redirect_uri=https://register-666-ramzer.onrender.com/vk/callback&state=xxrDRfZ-b3o1bLqfXX_ej9FQihsMhqrMgE1BHC-Es8tlWH_mU&code_challenge=p3wIzymBaGNuLY--fifRtLlbYUf7rkgu50TJkkx-mWU&code_challenge_method=s256'


## Get/Token:
Ресурс для получения access токена vk.


> GET '/vk/get/token'


Принимает параметры: code, device_id.


| Name | Type |
|:------------:|:---------:|
| code | str |
| device_id | str |


Пример ответа:
'{
    access_token: ********,
    refresh_token: *******,
    expire_in: *****,
}'


## Registration:
Ресурс для регистрации пользователя используя полученные данные от vk.


> GET '/vk/registration'


Принимает параметр: access_token.


| Name | Type |
|:------------:|:---------:|
| access_token | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Login:
Ресурс для авторизации пользователя используя полученные данные от vk.


> GET '/vk/login'


Принимает параметр: access_token.


| Name | Type |
|:------------:|:---------:|
| access_token | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Базовый ендпоинт: '/mail.ru/'


## Link:
Ресурс для получения ссылки авторизации mail.ru.


> GET '/mail.ru/link'

Ничего не принимает.


Пример ответа:
'https://oauth.mail.ru/login?client_id=80dcc118c6b44d57916fec6760aadefb&response_type=code&scope=userinfo&redirect_uri=https://register-666-ramzer.onrender.com/mail.ru/callback&state=7R14kQMwEdCB6myfBOywxZgD51xnudvIAbsg8USgIJX3i&prompt_force=1'


## Get/Token:
Ресурс для получения access токена mail.ru.


> GET '/mail.ru/get/token'


Принимает параметры: code.


| Name | Type |
|:------------:|:---------:|
| code | str |

Пример ответа:
'{
    access_token: ********,
    refresh_token: *******,
    expire_in: *****,
}'


## Registration:
Ресурс для регистрации пользователя используя полученные данные от mail.ru.


> GET '/mail.ru/registration'


Принимает параметр: access_token.


| Name | Type |
|:------------:|:---------:|
| access_token | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Login:
Ресурс для авторизации пользователя используя полученные данные от mail.ru.


> GET '/mail.ru/login'


Принимает параметр: access_token.


| Name | Type |
|:------------:|:---------:|
| access_token | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Базовый ендпоинт: '/yandex/'


## Link:
Ресурс для получения ссылки авторизации yandex.


> GET '/yandex/link'

Ничего не принимает.


Пример ответа:
'https://oauth.yandex.ru/authorize?response_type=code&client_id=4421f9793cae4d529b9e045ba22ca3b6'


## Get/Token:
Ресурс для получения access токена yandex.


> GET '/yandex/get/token'


Принимает параметры: code.


| Name | Type |
|:------------:|:---------:|
| code | str |


Пример ответа:
'{
    access_token: ********,
    refresh_token: *******,
    expire_in: *****,
}'


## Registration:
Ресурс для регистрации пользователя используя полученные данные от yandex.


> GET '/yandex/registration'


Принимает параметр: access_token.


| Name | Type |
|:------------:|:---------:|
| access_token | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Login:
Ресурс для авторизации пользователя используя полученные данные от yandex.


> GET '/yandex/login'


Принимает параметр: access_token.

| Name | Type |
|:------------:|:---------:|
| access_token | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImMwMTM4NDYxLWY5YjUtNDI1NS04OTI1LTg1YzI2NjMxYThjZiJ9LCJleHAiOjE3MzkyMzAxOTQsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.SgqAnJSa2yqf6Wevwt44RK2rJ9q9SfKd5fbQ9JhWslI",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWdtZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImVmNTg2MjdjLWQwMmUtNDRmOS05ZmQzLTMzNzYyNzQ4ZjdhMSJ9LCJleHAiOjE3MzkyNDA5OTQsIm1vZGUiOiJyZWZyZXNoX3Rva2VuIn0.miwX5cHKF_ZykUMTOJ66gujbsTTtJKhQQBzZmyDknPQ"
}'


## Базовый ендпоинт: '/validate/jwt/'


## Refresh:
Ресурс для валидации refresh токена и получения нового access токена.


> GET '/validate/jwt/refresh'


Принимает параметр: refresh.


| Name | Type |
|:------------:|:---------:|
| refresh | str |


Пример ответа:
'{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhbmRyZWptZWR2ZWRldjI3MTNAZ21haWwuY29tIiwiaGVhZGVyIjp7ImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIiwidXVpZCI6ImE1ZWQyMGEyLTZlMzktNGExMy1hZGNkLTVlZDViNTkwODQzNSJ9LCJleHAiOjE3MzkyMzE5NDMsIm1vZGUiOiJhY2Nlc3NfdG9rZW4ifQ.PfhN-NI2_FWbuQkeR6wdcLDRhu5sK5EdCi9KRf5saRs",
  "email": "andrejmedvedev2713@gmail.com"
}'


## Access:
Ресурс для валидации access токена.


> GET '/validate/jwt/access'


Принимает параметр: access.


| Name | Type |
|:------------:|:---------:|
| access | str |


Пример ответа:
'false'