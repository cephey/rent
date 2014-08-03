# coding: utf-8

# Создаёт конфигурацию для nginx, gunicorn и supervisor

import os
import stat

NGINX_CONF = u"""upstream backend {{
    server unix:{conf_dir}/gunicorn.sock fail_timeout=0;
}}

server {{
    listen 80;
    access_log {log_dir}/{nginx_access_log_file};
    error_log {log_dir}/{nginx_log_file};

    gzip on;
    gzip_min_length 1000;
    gzip_types text/plain text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript image/x-icon image/bmp;
    gzip_proxied any;
    gzip_vary on;
    gzip_disable "msie6";
    gzip_comp_level 8;

    location /static/ {{
        alias {project_dir}/src/static/;
        expires modified +10d;
    }}

    location /media/ {{
        alias {project_dir}/src/media/;
        expires modified +30d;
    }}

    location / {{
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        if (!-f $request_filename) {{
            proxy_pass http://backend;
            break;
        }}
    }}
}}
"""
SUPERVISOR_CONF = u"""[program:{project_name}]
command = {conf_dir}/{gunicorn_script_name} ;
user = {user} ;
stdout_logfile = {log_dir}/{gunicorn_supervisor_log_file} ;
redirect_stderr = true
"""
GUNICORN_CONF = u"""#!/bin/bash

# virtualenv bin directory
VIRTUALENV_DIR={workon_home}/{project_name}/bin

DJANGODIR={project_dir}/src
SOCKFILE=$DJANGODIR/../{name_conf_dir}/gunicorn.sock

echo "Starting {project_name}_app"

# Activate the virtual environment
cd $DJANGODIR
source $VIRTUALENV_DIR/activate
export DJANGO_SETTINGS_MODULE=conf.settings
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start Django Unicorn
exec $VIRTUALENV_DIR/gunicorn conf.wsgi:application \
--name {project_name}_app \
--workers {num_workers} \
--user={user} --group={user} \
--log-level=debug \
--bind=unix:$SOCKFILE
"""

# папка проекта
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_NAME = PROJECT_DIR.replace('\\', '/').rsplit('/', 1)[1]

# папка для всех генерируемых конфигов
NAME_CONF_DIR = 'conf'
CONF_DIR = os.path.join(PROJECT_DIR, NAME_CONF_DIR)

# папка для логов
NAME_LOG_DIR = 'logs'
LOG_DIR = os.path.join(PROJECT_DIR, NAME_LOG_DIR)
LOG_FILE_NAMES = {
    "gunicorn": "gunicorn_supervisor.log",
    "nginx": "nginx-error.log",
    "nginx_access": "nginx-access.log"
}

GUNICORN_SCRIPT_NAME = 'gunicorn_start'
GUNICORN_NUM_WORKERS = 3

USER = os.environ['USER']


def create_file(target_dir, file_name, conf_name, context):
    """
    Создаёт файл конфигурации с именем file_name в директории target_dir
    Файл-шаблон для него храниться в директории template_dir
    Затем мы туда вставляем параметры из context
    """
    target_file = open(os.path.join(target_dir, file_name), 'w')
    target_file.write(conf_name.format(**context))
    target_file.close()

if __name__ == "__main__":

    try:
        WH = os.environ['WORKON_HOME']
    except KeyError:
        print u'У вас не установлен virtualenvwrapper'
        print ur'Воспользуйтесь "sudo apt-get install virtualenvwrapper"'
        exit(0)

    # TODO: необходимо проверить что пользователь зашёл в вируальное окружение

    if os.path.isdir(CONF_DIR):
        # если такая папка существует, ничего не делаю
        print u'Папка с конфигами для nginx и supervisor уже существует'
        print u'Если вы хотите перегенерировать конфиги, удалите папку' \
              u' %s и запустите скрипт ещё раз' % NAME_CONF_DIR
        exit(0)
    else:
        # создаю папку для конфигов
        try:
            os.mkdir(CONF_DIR)
        except OSError:
            print u'Папка с конфигами для nginx и supervisor уже существует'
            print u'Если вы хотите перегенерировать конфиги, удалите папку' \
                  u' %s и запустите скрипт ещё раз' % NAME_CONF_DIR
            exit(0)

        context = {
            "user": USER,
            "workon_home": WH,
            "log_dir": LOG_DIR,
            "conf_dir": CONF_DIR,
            "project_dir": PROJECT_DIR,
            "project_name": PROJECT_NAME,
            "name_conf_dir": NAME_CONF_DIR,
            "num_workers": GUNICORN_NUM_WORKERS,
            "gunicorn_script_name": GUNICORN_SCRIPT_NAME,
            "nginx_log_file": LOG_FILE_NAMES['nginx'],
            "nginx_access_log_file": LOG_FILE_NAMES['nginx_access'],
            "gunicorn_supervisor_log_file": LOG_FILE_NAMES['gunicorn']
        }

        # настройка для nginx
        create_file(CONF_DIR, PROJECT_NAME, NGINX_CONF, context)

        # настройка для gunicorn
        create_file(CONF_DIR, GUNICORN_SCRIPT_NAME, GUNICORN_CONF, context)

        # настройка для supervisor
        create_file(CONF_DIR, '%s.conf' % PROJECT_NAME, SUPERVISOR_CONF, context)

        # делаю скрипт запуска gunicorn исполняемым
        st = os.stat(os.path.join(CONF_DIR, GUNICORN_SCRIPT_NAME))
        os.chmod(os.path.join(CONF_DIR, GUNICORN_SCRIPT_NAME), st.st_mode | stat.S_IEXEC)

        # создаю пустые файлы логов
        if not os.path.isdir(LOG_DIR):
            # создаю папку для логов
            try:
                os.mkdir(LOG_DIR)
            except OSError:
                print u'Ошибка создания папки логов. Вам придется создать её вручную'
                print u'Назовите её %s и поожите в %s' % (NAME_LOG_DIR, PROJECT_DIR,)
                print u'Также вам придётся создать в ней пустые файлы с именами:'
                for k, v in LOG_FILE_NAMES.items():
                    print v
                exit(0)

            for k, v in LOG_FILE_NAMES.items():
                log_file = open(os.path.join(LOG_DIR, v), 'w')
                log_file.close()

        print 'OK'
