# Configuração para deploy

python manage.py collectstatic

## Primeiros passos

- Prepare o local_settings.py
Comando para gerar SECRET_KEY

```
python -c "import string as s;from secrets import SystemRandom as SR;print(''.join(SR().choices(s.ascii_letters + s.digits + s.punctuation, k=64)));"
```
SECRET_KEY = acima
DEGUB = False
ALLOWED_HOSTS = ['servidor']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'projeto_agenda_servidor',
        'USER': 'usuario_agenda_servidor',
        'PASSWORD': 'senha_usuario_agenda_servidor',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

- Crie o seu servidor Ubuntu 20.04 LTS (onde preferir)


## Criando sua chave SSH

```
ssh-keygen -C 'COMENTÁRIO'
```

## No servidor

### Conectando

```
ssh usuário@IP_SERVIDOR
```

### Comandos iniciais

```
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y
sudo apt install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.14 python3.14-venv -y
sudo ln -s /usr/bin/python3.14 /usr/bin/python

sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y # usado para certificado ngnix
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install git -y
```

### Configurando o git

```
git config --global user.name 'Seu nome'
git config --global user.email 'seu_email@gmail.com'
git config --global init.defaultBranch main
```

Criando as pastas do projeto e repositório

```
mkdir ~/agendarepo ~/agendaapp
```

Configurando os repositórios

```
cd ~/agendarepo
git init --bare
cd ..
cd ~/agendaapp
git init
git remote add agendarepo ~/agendarepo
git add .
git commit -m 'Initial'
git push agendarepo main -u # erro
```

No seu computador local

```
git remote add agendarepo usuario@IP_SERVIDOR:~/agendarepo
git push agendarepo main
```

No servidor

```
cd ~/agendaapp
git pull agendarepo main
```

## Configurando o Postgresql

```
sudo -u postgres psql

postgres=# create role meu_usuario with login superuser createdb createrole password 'senha_do_usuario';
CREATE ROLE
postgres=# create database base_de_dados with owner meu_usuario;
CREATE DATABASE
postgres=# grant all privileges on database base_de_dados to meu_usuario;
GRANT
postgres=# \q

sudo systemctl restart postgresql
```

## Criando o local_settings.py no servidor

```
nano ~/agendaapp/project/local_settings.py
```

Cole os dados.

## Configurando o Django no servidor

```
cd ~/agendaapp
python3.11 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install django
pip install pillow
pip install gunicorn # sobe as aplicações com ele em vez de python manage.py runserver => comunicação do ngnix com django
pip install psycopg # para usar o postgresql
pip install faker
pip install whitenoise

python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
    WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
    For more information on production servers see: https://docs.djangoproject.com/en/6.0/howto/deployment/

```
## Vai pro arquivo gunicorn.txt
## Vai por arquivo nginx-http.txt
va no terminal do servidor
    cd /etc/nginx/sites-enabled/
    apagar tudo, normalmente so o default
    sudo rm -f default
    cd ..
    cd sites-available/
    sudo nano agenda
        pega o texto do arquivo nginx-http
    cd ..sites-enabled/
    sudo ln -s /etc/nginx/sites-available/agenda /etc/nginx/sites-enabled/
    sudo systemctl restart nginx

    Já está acessivel sem os static
        chmod o+x /home
    chmod o+x /home/aislan.penha
    chmod o+x /home/aislan.penha/agendaapp

    chmod -R o+r /home/aislan.penha/agendaapp/static
    sudo nginx -t
    sudo systemctl restart nginx

## Adicione no local_settings.py
    ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # 'dominio.com.br' se tiver
]

## Permitir arquivos maiores no nginx

```
sudo nano /etc/nginx/nginx.conf
```

Adicione em http {}:

```
client_max_body_size 30M;
```

```
sudo systemctl restart nginx
```
## Para o SSL arquivos maiores no nginx

https://letsencrypt.org/ cria de modo seguro e gratuito em SSL

vai para o nginx-https.txt

# Para olhar os errors
tail -f /var/log/nginx/subdominio.dominio.com.br-error.log