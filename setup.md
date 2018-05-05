
# Steps to setup mormo

* [MongoDB setup](#mongodb-setup)
* [Setup auto.sh script](#setup-autosh-script)
* [Setup Django Web UI of Mormo](#setup-django-web-ui-of-mormo)

## MongoDB setup

### Step 1: Install MongoDB.

* How To Install MongoDB on [Centos 7](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7).
* How To Install MongoDB on [Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04).


### Step 2: Edit configuration of mongod.

```sh
$ sudo vi /etc/mongod.conf
```

Uncomment line having __security:__ and add following below security.


__authorization: enabled__

```sh
security:
  authorization: enabled
```

### Step 3: Start the MongoDB instance with access control.

```bash
$ sudo systemctl start mongod

or

$ sudo mongod --fork -f mongod.conf
```

### Step 4: Connect to the instance.

```bash
$ mongo --port 27017 --host localhost
```

### Step 5: Create mongodb root and user administrator.

```js
use admin;

db.createUser({ user: "mongoRoot", pwd: "abc123", roles: [ { role: "root", db: "admin" } ] });

db.auth("mongoRoot","abc123");

db.createUser({ user: "myUserAdmin", pwd: "abc123", roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
```

### Step 6: Connect and authenticate as the user administrator.

```bash
$ mongo --port 27017 -u "myUserAdmin" -p "abc123" --authenticationDatabase "admin"
```

### Step 7: Create users for Mormo's commandlogs database.

```js
use commandlogs;

db.createUser({ user: "mormoDbAdmin", pwd: "passwd#123@QW!", roles: [ { role: "dbOwner", db: "commandlogs" } ] });

db.createUser({ user: "mormow", pwd: "passwd#123@QW!", roles: [ { role: "readWrite", db: "commandlogs" } ] });

db.createUser({ user: "mormor", pwd: "passwd#123@QW!", roles: [ { role: "read", db: "commandlogs" } ] });
```

### Step 8: Connect and authenticate as mormoDbAdmin.

```bash
$ mongo --port 27017 -u "mormoDbAdmin" -p "passwd#123@QW!" --authenticationDatabase "commandlogs" commandlogs
```

If got mongo shell Good to go!.


__NOTE:__

* __Replace All the password according to your convenience.__
* __Mormo require authorization enabled MongoDB.__

After Setting up and Starting MongoDB update all values in `mormo.conf` and `mormo_ui.conf` file.


## Setup auto.sh script

### Step 1: 

Add following line to `/etc/bashrc`.

```bash
$ sudo vi /etc/bashrc

export PROMPT_COMMAND='RETURN_VAL=$?;logger -p local6.debug "$(whoami) [$$]: $(who am i) [$$]: $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//") [$RETURN_VAL]"'
```

### Step 2:

Make a new file `/etc/rsyslog.d/bash.conf` and add folowing.

```bash
$ sudo vi /etc/rsyslog.d/bash.conf

local6.* /var/log/com.log
```

### Step 3:

Make a empty file `/var/log/com.log` .

```bash
$ sudo touch /var/log/com.log
```

### Step 4:

Put `auto.sh` `db_functions.py` `mormo.conf` `requirements.txt` `config.py` `logs_dump_to_mongo.py` in same directory and make `auto.sh`, `logs_dump_to_mongo.py`  executable.

```bash
$ sudo chmod +x auto.sh logs_dump_to_mongo.py 
```

### Step 5:

Install required python packages.

```bash
$ sudo pip install -r requirements.txt
```
### Step 6:

Start `auto.sh` in background.

```bash
$ sudo ./auto.sh &
```


## Setup Django Web UI of Mormo

__NOTE:__ Django web ui have two option for setting usermanagement backend database 

1. sqlite3
2. mysql

If you want `MySQL`/`MariaDB` as usermanagement backend database, setup `MySQL`/`MariaDB` according to belwo [MySQL Setup](#mysql-setup), for [sqlite3 jump to step](#update-mormo-uiconf). 


### MySQL Setup

#### Install MySQL.

* How To Install MySQL on [Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04).
* How To Install MySQL on [CentOS 7](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-centos-7).

#### Create Database and user for mormo, also assign privilages to user on database.

```bash
$ mysql -h localhost -P 3306 -u root -p
mysql> CREATE DATABASE mormo;
mysql> CREATE USER 'mormoadmin'@'localhost' IDENTIFIED BY 'passwd#123@QW!';
mysql> ALL PRIVILEGES ON mormo.* TO 'mormoadmin'@'localhost';
mysql> FLUSH PRIVILEGES;
```

#### Test mysql connection by created user

```bash
$ mysql -h localhost -P 3306 -u mormoadmin -p 'passwd#123@QW!'
```

#### Install MySQL client packages.

```bash
$ sudo apt-get install libmysqlclient-dev
```

If you are using `mariadb`, then run

```bash
$ sudo apt-get install libmariadbclient-dev
```

If on centos

```bash
$ sudo yum install mysql-devel gcc gcc-devel python-devel mysql
```

#### Update mormo_ui.conf

```bash
$ vi mormo_ui.conf

MYSQL:
    USER   : mormoadmin
    PASSWD : passwd#123@QW!
    HOST   : localhost
    PORT   : 3306
    DBNAME : mormo

```

If you are using `sqlite3` comment `MYSQL` in `mormo_ui.conf`. do not remove or comment MONGODB parameters


### Migrate Django databse tables to backend database.

django-web ui has different python library dependencies install them

```bash
$ sudo pip install -r requirements.txt
```

Now migrate db tables

```bash
$ ./manage.py makemigrations
$ ./manage.py migrate
```

### Create Super user for Django

```bash
$ ./manage.py createsuperuser
```

### Run Django web server

```bash
$ ./manage.py runserver 0.0.0.0:8080
```

Open [localhost:8080](http://localhost:8080) in web Browser.

