#!/usr/bin/env python3

import mysql.connector
import os
import logging

def setup_logging():
    logging.basicConfig(filename='latin1_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

def connect_to_proxysql():
    return mysql.connector.connect(user='admin', password='admin', host='127.0.0.1', port=6032, charset='utf8')

def get_rows(cnx):
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM stats.stats_mysql_query_digest WHERE digest_text LIKE '%SET NAMES latin1%'")
    rows = cursor.fetchall()
    cursor.close()
    return rows

def write_to_file(rows):
    with open('output.sql', 'w', encoding='utf-8') as f:
        rule_id = 1
        for row in rows:
            username = row[2]
            logging.info(f"Found 'SET NAMES latin1' for user: {username}")
            f.write(f"INSERT INTO mysql_query_rules (rule_id, active, username, match_pattern, destination_hostgroup, apply) VALUES ({rule_id}, 1, '{username}', '^INSERT INTO chaos.|^UPDATE chaos.|^DELETE FROM chaos.', 9999, 1) ON DUPLICATE KEY UPDATE active=VALUES(active), username=VALUES(username), match_pattern=VALUES(match_pattern), destination_hostgroup=VALUES(destination_hostgroup), apply=VALUES(apply);\n")
            rule_id += 1
        f.write("LOAD MYSQL USERS TO RUNTIME;\n")
        f.write("LOAD MYSQL QUERY RULES TO RUNTIME;\n")
        f.write("SAVE MYSQL USERS TO DISK;\n")
        f.write("SAVE MYSQL QUERY RULES TO DISK;\n")

def feed_sql_to_proxysql():
    os.system("mysql -h 127.0.0.1 -P 6032 -u admin -padmin < output.sql")

def main():
    setup_logging()
    cnx = connect_to_proxysql()
    rows = get_rows(cnx)
    cnx.close()
    write_to_file(rows)
    feed_sql_to_proxysql()

if __name__ == "__main__":
    main()