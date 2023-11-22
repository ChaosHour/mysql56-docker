# Percona's Percona-Server56 Docker, with primary and replica 



## Do not use this project for anything other than testing. Unless you clean it up.




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


## build the docker images and run them.
```bash

make up
docker-compose up -d --build --wait
✔ Network mysql56-docker_db-network    Created                                                                                                                                  0.0s
 ✔ Container mysql56-docker-primary-1   Healthy                                                                                                                                  0.0s
 ✔ Container mysql56-docker-replica-1   Healthy                                                                                                                                  0.0s
 ✔ Container mysql56-docker-proxysql-1  Healthy                                                                                                                                  0.0s
```

## Check the status of the containers
```bash
docker-compose ps
NAME                        IMAGE                     COMMAND                  SERVICE    CREATED         STATUS                   PORTS
mysql56-docker-primary-1    mysql56-docker-primary    "/docker-entrypoint.…"   primary    3 minutes ago   Up 3 minutes (healthy)   0.0.0.0:3306->3306/tcp
mysql56-docker-proxysql-1   mysql56-docker-proxysql   "bash /entrypoint.sh"    proxysql   3 minutes ago   Up 3 minutes             0.0.0.0:6032-6033->6032-6033/tcp, 0.0.0.0:6080->6080/tcp
mysql56-docker-replica-1    mysql56-docker-replica    "/docker-entrypoint.…"   replica    3 minutes ago   Up 3 minutes (healthy)   0.0.0.0:3307->3306/tcp
```


## Using in my ~/.my.cnf for testing
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
[client_proxysql1]
user=klarsen
password=ou812
host=192.168.50.75
port=6033
default-character-set=latin1
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

## Connect to the proxysql
```bash
docker exec -it mysql56-docker-proxysql-1 bash
root@a41e1300f8a4:/# mysql -h 127.0.0.1 -P 6032 -u admin -padmin --prompt 'ProxySQL Admin >'
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 1
Server version: 5.5.30 (ProxySQL Admin Module)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

ProxySQL Admin >ProxySQL Admin >SELECT * FROM mysql_users\G
*************************** 1. row ***************************
              username: repl
              password: slAv3
                active: 1
               use_ssl: 0
     default_hostgroup: 20
        default_schema:
         schema_locked: 0
transaction_persistent: 1
          fast_forward: 0
               backend: 1
              frontend: 1
       max_connections: 10000
            attributes:
               comment:
*************************** 2. row ***************************
              username: klarsen
              password: ou812
                active: 1
               use_ssl: 0
     default_hostgroup: 10
        default_schema:
         schema_locked: 0
transaction_persistent: 1
          fast_forward: 0
               backend: 1
              frontend: 1
       max_connections: 10000
            attributes:
               comment:
2 rows in set (0.00 sec)
```

## Time for testing... in the ProxySQL Container we will start ngrep to listen to the traffic
```bash
root@a41e1300f8a4:/# ngrep -q -t -W byline -i 'SELECT|INSERT|UPDATE|SET' port 6033
interface: eth0 (172.22.0.0/255.255.0.0)
filter: ( port 6033 ) and ((ip || ip6) || (vlan && (ip || ip6)))
match (JIT): SELECT|INSERT|UPDATE|SET

T 2023/11/22 04:33:42.614288 192.168.65.1:34009 -> 172.22.0.4:6033 [AP] #125
=....INSERT INTO employees (name, salary) VALUES ('Chaos2', 5000)

T 2023/11/22 04:33:42.621886 192.168.65.1:34009 -> 172.22.0.4:6033 [AP] #128
.....INSERT INTO test_table (name, additional_info) VALUES ('Chaos2', 'Some additional info with German umlauts: ., ., ., .. Here are some words: sch.n, fr.ulein, gr..en')

T 2023/11/22 04:34:57.284057 192.168.65.1:34066 -> 172.22.0.4:6033 [AP] #147
!....select @@version_comment limit 1

T 2023/11/22 04:34:57.284342 192.168.65.1:34066 -> 172.22.0.4:6033 [AP] #150

....select $$

T 2023/11/22 04:34:57.285451 192.168.65.1:34066 -> 172.22.0.4:6033 [AP] #153
%....select @@hostname, @@version, @@port

T 2023/11/22 04:34:57.286048 192.168.65.1:34066 -> 172.22.0.4:6033 [AP] #156
8....select * from chaos.employees, chaos.test_table limit 3
```

## In a seperate terminal, we will run the Python script, insert some data, watch the traffic and validate the data
```bash
mysql56-docker on  main via 🐳 desktop-linux via 🐍 v3.11.5 (mysql56-docker) 
❯ ./test.py                           
Connected to server 192.168.100.75 on port 6033
Current character set: latin1 and collation: latin1_swedish_ci
[(1,)]
Attempting to connect to the database with character set latin1 and collation latin1_swedish_ci
Attempting to connect to the database with character set latin1 and collation latin1_swedish_ci
Latin1 character set is accepted when adding an employee.
Connected to the database. Adding employee Chaos2 with salary 5000
Employee Chaos2 added successfully. Committing the transaction.


mysql --defaults-group-suffix=_proxysql1 -e "select @@hostname, @@version, @@port; select * from chaos.employees, chaos.test_table limit 3"
+--------------+-----------------+--------+
| @@hostname   | @@version       | @@port |
+--------------+-----------------+--------+
| ab1fe00558db | 5.6.51-91.0-log |   3306 |
+--------------+-----------------+--------+
+----+------------------------------------------------------------------------------------------------------+
| id | name   | salary | id | name   | additional_info                                                                                                                   +----+--------+--------+----+--------
| 62 | Chaos2 |   5000 | 62 | Chaos2 | Some additional info with German umlauts: � , , � Here are some words: schn, fr�lein, gr�n |
| 63 | Chaos2 |   5000 | 62 | Chaos2 | Some additional info with German umlauts: � , , � Here are some words: schn, fr�lein, gr�n |
| 64 | Chaos2 |   5000 | 62 | Chaos2 | Some additional info with German umlauts: � , , � Here are some words: schn, fr�lein, gr�n |
+----+----+-------------------------------------------------------------------------------------------------+
```

## Using go-utf8 to validate the data
(go-utf8)[https://github.com/ChaosHour/go-utf8]

```bash 
go-utf8 -s 192.168.50.75 -d chaos
Connected to 192.168.50.75 (ab1fe00558db): ✔


Current table: test_table
Column: additional_info
Count of records that need to be fixed: 10


mysql --defaults-group-suffix=_proxysql1 -e "select @@hostname, @@version, @@port; select count(*) from chaos.test_table"
+--------------+-----------------+--------+
| @@hostname   | @@version       | @@port |
+--------------+-----------------+--------+
| a0c9a33a221a | 5.6.51-91.0-log |   3306 |
+--------------+-----------------+--------+
+----------+
| count(*) |
+----------+
|       10 |
+----------+
```


## When done, clean up
```bash

make down
docker-compose down
[+] Running 4/3
 ✔ Container mysql56-docker-proxysql-1  Removed                                                                                                                                  0.5s
 ✔ Container mysql56-docker-replica-1   Removed                                                                                                                                  2.5s
 ✔ Container mysql56-docker-primary-1   Removed                                                                                                                                  3.8s
 ✔ Network mysql56-docker_db-network    Removed                                                                                                                                  0.1s
```