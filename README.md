# Sistema Ciudad Inteligente

Como descargar

## Github

```shell
git clone git@github.com:murillo-fcpn/dbIbackend.git backend
cd backend
```

```shell
python -m venv venv
# linux
source  venv/bin/activate
# windows
./venv/scripts/activate.bat
```

cuando tengamos activado nuestro entorno virtual cargaremos las librerias necesarias en nuestro entorno virtual

```shell
pip install -r requirements.txt
```

necesitamos crear un archvivo .env

```shell
# linux 
touch .env
vim .env
```

en windows crear y editar el archivo .env igual en linux

```txt
FLASK_CONFIG=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgresql://username:contrasenia@localhost/servicios_db
```

```shell
psql -U postgres
```

```sql
CREATE DATABASE servicios_db;
\q
```

Ahora migramos los datos luego de tener el entorno virtual en la terminal

```shell
flask db init
flask db migrate -m "first  migrate"
flask db upgrade
```

ya tenemos cargada nuestra base de datos, ahora corremos el proyecto

```shell
python run.py
```
