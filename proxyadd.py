#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import re
import os
import logging

logging.basicConfig(level=logging.INFO)

def process_output(output):
    print(output)  # print out the entire output
    match = re.search(r"(SET NAMES 'latin1' COLLATE 'latin1_swedish_ci'|.....SET NAMES latin1)", output)
    if match:
        logging.info(f"Match found: {match.group()}")
        flyway_match = re.search(r"flyway", output)
        if flyway_match:
            logging.info(f"flyway match found: {flyway_match.group()}")
            username = 'flyway'
        else:
            username = 'flyway'
        # Create SQL file with the captured information
        with open('output.sql', 'w') as f:
            f.write(f"REPLACE INTO mysql_query_rules (rule_id, active, username, match_pattern, destination_hostgroup, apply) VALUES (1, 1, '{username}', '^INSERT INTO chaos.|^UPDATE chaos.|^DELETE FROM chaos.', 9999, 1);\n")
            f.write("LOAD MYSQL USERS TO RUNTIME;\n")
            f.write("LOAD MYSQL QUERY RULES TO RUNTIME;\n")
            f.write("SAVE MYSQL USERS TO DISK;\n")
            f.write("SAVE MYSQL QUERY RULES TO DISK;\n")
        # Feed the SQL file back into ProxySQL
        os.system("mysql -h 127.0.0.1 -P 6032 -u admin -padmin < output.sql")

def main():
    logging.info("Starting packet sniffing...")
    process = subprocess.Popen(['ngrep', '-q', '-t', '-W', 'byline', '-i', 'user|pass|SET', 'port', '6033'], stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        process_output(line.decode('utf-8'))

if __name__ == "__main__":
    main()