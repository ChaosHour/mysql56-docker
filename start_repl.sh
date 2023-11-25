#!/usr/bin/env zsh
#set -xv

# Get the output of SHOW MASTER STATUS;
OUTPUT=$(docker exec -it mysql56-docker-primary-1 mysql -u root -ps3cr3t -e "FLUSH TABLES; FLUSH TABLES WITH READ LOCK; SHOW MASTER STATUS; SELECT SLEEP(1); UNLOCK TABLES" | grep -v W)

# Parse the output to get the MASTER_LOG_FILE and MASTER_LOG_POS
MASTER_LOG_FILE=$(echo "$OUTPUT" | grep 'mysql-bin' | cut -d'|' -f2 | tr -d '[:space:]')
MASTER_LOG_POS=$(echo "$OUTPUT" | grep 'mysql-bin' | cut -d'|' -f3 | tr -d '[:space:]')

# Configure the replica
docker exec -it mysql56-docker-replica-1 mysql -u root -ps3cr3t -e "STOP SLAVE;CHANGE MASTER TO MASTER_HOST='172.22.0.3',MASTER_USER='repl',MASTER_PASSWORD='slAv3',MASTER_LOG_FILE='${MASTER_LOG_FILE}',MASTER_LOG_POS=${MASTER_LOG_POS};SELECT SLEEP (10);START SLAVE" | grep -v W

# Wait for the slave to start and show its status
sleep 1
mysql --defaults-group-suffix=_replica1 -e "show slave status\G" | egrep "Slave_IO_Running:|Slave_SQL_Running:|Seconds_Behind_Master:|Master_Host:" | grep -v W