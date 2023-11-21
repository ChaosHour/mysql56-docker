# Percona's Percona-Server56 Docker, with primary and replica 

## Do not use this project for anything other than testing.  It is not secure. It is not production ready.  It is not for anything other than testing.

> I needed to test ProxySQL and needed a quick and dirty project to do so.  This is it.  It is not secure.  It is not production ready.  It is not for anything other than testing.


Passwords are insecure and only used for testing.


## I am using this project to test the following:
```bash
[client_proxysql1]
user=klarsen
password=ou812
host=192.168.50.75
port=6033
default-character-set  =  latin1

A python script is inlcuded that will insert data into 2 tables for testing ProxySQL.
```

## How To use this project, a little prep work is needed. 
```Go
Working with Docker creds:

Create a file called .env in the root of the project and add the following:
MYSQL_ROOT_PASSWORD=s3cr3t
MYSQL_REPLICA_PASSWORD=slAv3

```

## Replica password
```bash
This is a quick and dirty project for testing.  Change or keep the passwords.
No very secure, but it is a test project.

```


## build the docker image
```bash

make up
```

## Using the ~/.my.cnf
```bash
[client_primary1]
user=root
password=xxxx
host=192.168.50.50
port=3306
[client_replica1]
user=root
password=xxxx
host=192.168.50.50
port=3307
```


## Connect to the primary
```bash
mysql --defaults-group-suffix=_primary1 -e "show variables like 'char%'; show variables like 'collation%'"
+--------------------------+-------------------------------------+
| Variable_name            | Value                               |
+--------------------------+-------------------------------------+
| character_set_client     | utf8                                |
| character_set_connection | utf8                                |
| character_set_database   | utf8                                |
| character_set_filesystem | binary                              |
| character_set_results    | utf8                                |
| character_set_server     | utf8                                |
| character_set_system     | utf8                                |
| character_sets_dir       | /usr/share/percona-server/charsets/ |
+--------------------------+-------------------------------------+
+----------------------+-----------------+
| Variable_name        | Value           |
+----------------------+-----------------+
| collation_connection | utf8_unicode_ci |
| collation_database   | utf8_unicode_ci |
| collation_server     | utf8_unicode_ci |
+----------------------+-----------------+


mysql --defaults-group-suffix=_replica1 -e "show variables like 'char%'; show variables like 'collation%'"
+--------------------------+-------------------------------------+
| Variable_name            | Value                               |
+--------------------------+-------------------------------------+
| character_set_client     | utf8                                |
| character_set_connection | utf8                                |
| character_set_database   | utf8                                |
| character_set_filesystem | binary                              |
| character_set_results    | utf8                                |
| character_set_server     | utf8                                |
| character_set_system     | utf8                                |
| character_sets_dir       | /usr/share/percona-server/charsets/ |
+--------------------------+-------------------------------------+
+----------------------+-----------------+
| Variable_name        | Value           |
+----------------------+-----------------+
| collation_connection | utf8_unicode_ci |
| collation_database   | utf8_unicode_ci |
| collation_server     | utf8_unicode_ci |
+----------------------+-----------------+


mysql --defaults-group-suffix=_replica1 -e "show slave status\G" | egrep "Slave_IO_Running:|Slave_SQL_Running:|Seconds_Behind_Master:|Master_Host:" | grep -v W
                  Master_Host: 172.22.0.3
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
        Seconds_Behind_Master: 0

```

## When done, clean up
```bash

make down
```