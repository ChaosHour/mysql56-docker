# MySQL 8 Docker, with primary and replica 


## How To use this project, a little prep work is needed. 
```Go
Working with Docker creds:

Create a file called .env in the root of the project and add the following:
MYSQL_ROOT_PASSWORD=s3cr3t
MYSQL_REPLICA_PASSWORD=slAv3

```

## Replica password
```bash
The replica password used for testing is in the replica.sql file. I would recommend changing this password with an alter user command.
An example of this is in the primary.sql file.
```


## build the docker image
```Go
docker-compose build

```

## docker-compose

```Go
docker-compose up -d --wait

mysql56-docker on  main [?] via 🐳 desktop-linux took 2s 
❯ docker-compose up -d --wait                 
[+] Building 0.0s (0/0)                                                                                                                  docker:desktop-linux
[+] Running 3/3
 ✔ Network mysql56-docker_db-network   Created                                                                                                           0.2s 
 ✔ Container mysql56-docker-primary-1  Healthy                                                                                                           0.1s 
 ✔ Container mysql56-docker-replica-1  Healthy                                                                                                           0.1s 
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

