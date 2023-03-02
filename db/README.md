# MySQL Database
Database for x5.

## MySQL Installation

```bash
# purge old install
sudo apt purge mysql*
sudo apt autoremove
sudo rm -rf /etc/mysql/ /var/lib/mysql/

# new install
sudo apt upgrade
sudo apt install mysql-server

# setup mysql root 
sudo mysql
```

```mysql
-- set password for root
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'I_love_stew!12';
```

To configure other safety settings
```bash
sudo mysql_secure_installation
```

Install (`mysql_secure_installation` onwards is deprecated)
https://www.linode.com/docs/guides/installing-and-configuring-mysql-on-ubuntu-2004/

Change root password
https://ostechnix.com/fix-mysql-error-1819-hy000-your-password-does-not-satisfy-the-current-policy-requirements/
https://devanswers.co/how-to-fix-failed-error-set-password-has-no-significance-for-user-rootlocalhost/#:~:text=As%20of%20May%202022%2C%20running,use%20a%20password%20by%20default.

---

## Setting up db

```bash
mysql -u root -p
```

```mysql
CREATE DATABASE x5db;
USE x5db;

\. x5db.sql
```
make sure x5db is in working directory.


---

## Docker involvement

```bash
sudo docker build -t ubuntu/x5db:1.0 .
sudo docker run -it -p 3306:3306 ubuntu/x5db:1.0 /bin/bash
```
Inside the container
```bash
/etc/init.d/mysql start
```

Not sure why this needs to be done again when it is being done during the build