# Инструмент для конкурсов Instagram

Скрипт выводит список участников, выполнивших условия конкурса:

1. Подписаться на [Instagram](https://www.instagram.com/) аккаунт автора поста;

2. Поставить лайк под постом;
   
3. Отметить друга в комментарии к посту. Аккаунт друга должен быть существующий.


### Как установить

Учетные данные Инстаграм берутся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны следующие переменные:
- `INSTAGRAM_LOGIN` — логин.
- `INSTAGRAM_PASSWORD` — пароль.

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Аргументы

* `post_link` — ссылка на пост;
* `post_author` — автор поста (Instagram логин).

Пример команды запуска: 

`python manage.py --post_link https://www.instagram.com/p/B9OiN-lJlSc/ --post_author yuliya.polienko`

В результате скрипт определит участников, выполнивших условия конкурса, напечатает их логины: 

![](https://github.com/Piar1986/instagram_contest_tool/raw/master/result_example.png)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).