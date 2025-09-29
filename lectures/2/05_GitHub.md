# Начало работы с GitHub

## Регистрация на GitHub

[Сайт GitHub](https://github.com/)

## Настройка пользователя Git

Откройте PowerShell или CMD и пропиши свои имя и email:

``
git config --global user.name "Ваше Имя"
git config --global user.email "email@example.com"
``

Проверьте настройки:
``
git config --global --list
``

## Генерация Personal Access Token (PAT) на GitHub

Перейдите в Settings → Developer settings → Personal access tokens → Tokens (classic)

Нажмите Generate new token (classic)

Выберите нужные права (например, repo для работы с репозиториями)

Скопируйте токен сразу, он больше не покажется

## Сохранение токена в Git Credential Manager (рекомендовано для Windows)

Windows использует Git Credential Manager (GCM) для хранения логина/токена. Он идёт с последними версиями Git for Windows.

Включаем:
```
git config --global credential.helper manager-core
```
Теперь при первом git push GitHub попросит логин и токен:
```
Username: твой GitHub логин и
Password: твой токен
```

После этого GCM сохранит их, и при следующих действиях Git токен вводить не будет.

Если GCM настроен правильно, запрос токена больше не появится.

## Как загрузить изменения в репозитории с локального компьютера на GitHub

```
git add .
git commit -m "."
git push origin main
```