
# Steps to setup mormo

* [MongoDB setup](#mongodb-setup)
* [Setup auto.sh script](#setup-autosh-script)
* [Setup Django Web UI of Mormo](#setup-django-web-ui-of-mormo)

## MongoDB setup

### Step 1: Install MongoDB 

* How To Install MongoDB on [Centos 7](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7)
* How To Install MongoDB on [Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04)


### Step 2: Edit configuration of mongod

```sh
# vi /etc/mongod.conf
```

Uncomment line having __security:__ and add following below security.


__authorization: enabled__

```sh
security:
  authorization: enabled
```

### Step 3: Start the MongoDB instance with access control.

```bash
# systemctl start mongod

or

# mongod --fork -f mongod.conf
```

### Step 4: Connect to the instance.

```bash
# mongo --port 27017 --host localhost
```

### Step 5: Create mongodb root and user administrator.

```js
use admin;

db.createUser({ user: "mongoRoot", pwd: "abc123", roles: [ { role: "root", db: "admin" } ] });

db.auth("mongoRoot","abc123");

db.createUser({ user: "myUserAdmin", pwd: "abc123", roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
```

### Step 6: Connect and authenticate as the user administrator

```bash
# mongo --port 27017 -u "myUserAdmin" -p "abc123" --authenticationDatabase "admin"
```

### Step 7: Create users for Mormo's commandlogs database.

```js
use commandlogs;

db.createUser({ user: "mormoDbAdmin", pwd: "passwd#123@QW!", roles: [ { role: "dbOwner", db: "commandlogs" } ] });

db.createUser({ user: "mormow", pwd: "passwd#123@QW!", roles: [ { role: "readWrite", db: "commandlogs" } ] });

db.createUser({ user: "mormor", pwd: "passwd#123@QW!", roles: [ { role: "read", db: "commandlogs" } ] });
```

### Step 8: Connect and authenticate as mormoDbAdmin

```bash
# mongo --port 27017 -u "mormoDbAdmin" -p "passwd#123@QW!" --authenticationDatabase "commandlogs"
```

If got mongo shell Good to go!.


__NOTE:__

* __Replace All the password according to your convenience.__
* __Mormo require authorization enabled MongoDB.__

After Setting up and Starting MongoDB update all values in __mormo.conf__ file


## Setup auto.sh script

### Step 1: 

Add following line to __/etc/bashrc__ 

```bash
export PROMPT_COMMAND='RETURN_VAL=$?;logger -p local6.debug "$(whoami) [$$]: $(who am i) [$$]: $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//") [$RETURN_VAL]"'
```

### Step 2:

Make a new file "/etc/rsyslog.d/bash.conf" and add folowing

```bash
local6.* /var/log/com.log
```

### Step 3:

Make a empty file "/var/log/com.log"

```bash
# touch /var/log/com.log
```

### Step 4:

Start auto.sh in background


## Setup Django Web UI of Mormo

