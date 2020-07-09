web_file_sharing
====

Файлхостинг с функцией хэширования.

Приложение было написано с использованием микрофреймворка Flask. Приложение в первую очередь нацелено на использование
в Ru сегменте, по этой причине все комментарии и описание на Русском языке.

Для запуска проекта на вашем компьютере вам понадобится Python3.6+.

Установка на локальном сервере.
----

Создайте виртуальное окружение и активируйте его. После установите все необходимые зависимости:

.. code-block:: text

    pip install -r requirements.txt

Создайте в корне проекта файл config.py:

.. code-block:: python

    SECRET_KEY = 'Введите сложный набор символов который будет служить ключем защищающим от атак CSRF.'

Запуск
----

.. code-block:: text

    python3 wsgi.py
    
Деплой
----

Разверните сервер на хостинг провайдере и создайте нового юзера с правами администратора.

.. code-block:: text

    adduser <имя юзера>
    
Добавляем пользователя в группу sudo

.. code-block:: text

    usermod -aG sudo <имя юзера>
    
Готово, теперь необходимо зайти под созданным пользователем. Приступаем к настройке.

установите git.

.. code-block:: text

    sudo apt-get install git
    
клонируйте туда репозиторий.

.. code-block:: text

    git clone https://github.com/Gelion91/web_file_sharing.git

Скачайте модуль python3-venv и создайте виртуальное окружение в папке с проектом.

.. code-block:: text
    
    sudo apt-get update
    sudo apt-get install python3-venv
    python3 -m venv env
    
И активируйте его.

.. code-block:: text
    
    source env/bin/activate

Установите все необходимые зависимости.

.. code-block:: text

    pip install -r requirements.txt

После этого необходимо установить nginx

.. code-block:: text

    sudo apt-get install nginx
    
Меняем конфигурацию nginx в файле default

.. code-block:: text

    sudo nano /etc/nginx/site-enabled/default
    
В "location" добавляем запись

.. code-block:: text

    proxy_pass http://127.0.0.1:5000;
    
После изменения необходимо перезагрузить nginx

.. code-block:: text

    sudo service nginx reload
    
Устанавливаем supervisor

.. code-block:: text

    sudo apt-get install supervisor
    
Убеждаемся, что виртуальное окружение все еще активированно и устанавливаем gunicorn

.. code-block:: text

    pip install gunicorn
    
Переходим к настройке supervisor, для этого создаем файл кофигурации нашего приложения.

.. code-block:: text

    sudo nano /etc/supervisor/conf.d/flask.conf
    
И там создаем необходимую конфигурацию для запуска нашего приложения.

.. code-block:: text

    [program=flask]
    command=/home/<имя юзера>/web_file_sharing/env/bin/gunicorn wsgi:app -b 127.0.0.1:5000 -w 3
    directory=/home/<имя юзера>/web_file_sharing/
    user=<имя юзера>
    
Сохраняем.

Заходим в панель управления supervisor

.. code-block:: text

    sudo supervisorctl
    reread
    update
    status - Смотрим запущено ли наше приложение. Если работает - ок, если нет вводим еще одну команду.
    start flask
    
Готово. Можете выйти из терминала и проверить.


    

 