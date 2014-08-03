rent
====

> **Установка:**
>
> - pip install -r requirements.txt
> - ./manage.py collectstatic
> - python run.py
> - chmod +x gunicorn_start
> - cd /etc/supervisor/conf.d
> - sudo ln -s ~/works/rent/conf/rent.conf
> - sudo supervisorctl reread
> - sudo supervisorctl update
> - sudo supervisorctl status rent
> - sudo supervisorctl stop/start/restart rent
> - cd /etc/nginx/sites-enabled
> - sudo ln -s ~/works/rent/conf/rent
> - sudo /etc/init.d/nginx restart